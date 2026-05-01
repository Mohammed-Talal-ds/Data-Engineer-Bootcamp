import pandas as pd
from datetime import datetime
import logging
from sqlalchemy import text
from scripts.common.db_utils import load_config, get_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DimensionLoader:
    def __init__(self):
        self.config = load_config()
        self.stg_engine = get_engine('staging_db', self.config)
        self.dw_engine = get_engine('dw_db', self.config)
        self.today = datetime.now().date()

    def load_scd2_dim(self, table_name, natural_key, stg_query, columns_to_compare):
        """Generic SCD Type 2 logic for scalability and code reuse."""
        logging.info(f"Processing SCD Type 2 for {table_name}...")
        
        # 1. Fetch Staging and DW Active Data
        stg_df = pd.read_sql(stg_query, self.stg_engine)
        dw_df = pd.read_sql(f"SELECT * FROM {table_name} WHERE is_current = True", self.dw_engine)

        # 2. Identify New Records
        new_records = stg_df[~stg_df[natural_key].isin(dw_df[natural_key])].copy()

        # 3. Identify Changes in Existing Records
        merged = pd.merge(
            stg_df, 
            dw_df[[natural_key, f"{table_name.replace('dim_', '')}_key"] + columns_to_compare], 
            on=natural_key, 
            suffixes=('_stg', '_dw')
        )

        change_mask = False
        for col in columns_to_compare:
            change_mask |= (merged[f"{col}_stg"] != merged[f"{col}_dw"])
        
        changed_ids = merged.loc[change_mask, natural_key].tolist()
        expired_keys = merged.loc[change_mask, f"{table_name.replace('dim_', '')}_key"].tolist()

        # 4. Atomic Database Updates
        with self.dw_engine.begin() as conn:
            if expired_keys:
                conn.execute(text(f"""
                    UPDATE {table_name} SET is_current = False, end_date = :today 
                    WHERE {table_name.replace('dim_', '')}_key = ANY(:keys)
                """), {"today": self.today, "keys": expired_keys})

            to_insert = pd.concat([new_records, stg_df[stg_df[natural_key].isin(changed_ids)]])
            if not to_insert.empty:
                to_insert['start_date'] = self.today
                to_insert['end_date'] = None
                to_insert['is_current'] = True
                to_insert.to_sql(table_name, conn, if_exists='append', index=False)
        
        logging.info(f"Finished {table_name}: {len(to_insert)} inserts, {len(expired_keys)} expires.")

    def load_type1_dims(self):
        """Simple Overwrite/Append for static lookup tables."""
        # dim_order_status
        statuses = pd.read_sql("SELECT DISTINCT order_status FROM orders", self.stg_engine)
        statuses.to_sql('dim_order_status', self.dw_engine, if_exists='append', index=False, method='multi')

        # dim_payment_type
        payments = pd.read_sql("SELECT DISTINCT payment_type FROM order_payments", self.stg_engine)
        payments.to_sql('dim_payment_type', self.dw_engine, if_exists='append', index=False, method='multi')

        # dim_review (Metadata only)
        reviews = pd.read_sql("""
            SELECT DISTINCT review_id, review_comment_title, review_comment_message 
            FROM order_reviews
        """, self.stg_engine)
        reviews.to_sql('dim_review', self.dw_engine, if_exists='append', index=False, method='multi')

    def run_all(self):
        # 1. Static Dims
        self.load_type1_dims()

        # 2. SCD Type 2 - Product
        self.load_scd2_dim(
            'dim_product', 'product_id',
            """SELECT p.product_id, p.product_category_name as category_name, t.product_category_name_english as category_name_english,
               p.product_weight_g as weight_g, p.product_length_cm as length_cm, p.product_height_cm as height_cm, p.product_width_cm as width_cm
               FROM products p LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name""",
            ['category_name', 'weight_g', 'length_cm', 'height_cm', 'width_cm']
        )

        # 3. SCD Type 2 - Customer
        self.load_scd2_dim(
            'dim_customer', 'customer_id',
            "SELECT customer_id, customer_unique_id, customer_zip_code_prefix as zip_code_prefix, customer_city as city, customer_state as state FROM customers",
            ['zip_code_prefix', 'city', 'state']
        )

        # 4. SCD Type 2 - Seller
        self.load_scd2_dim(
            'dim_seller', 'seller_id',
            "SELECT seller_id, seller_zip_code_prefix as zip_code_prefix, seller_city as city, seller_state as state FROM sellers",
            ['zip_code_prefix', 'city', 'state']
        )

        # 5. SCD Type 2 - Lead
        self.load_scd2_dim(
            'dim_lead', 'mql_id',
            """SELECT q.mql_id, q.origin, q.landing_page_id, c.lead_type, c.business_segment 
               FROM leads_qualified q LEFT JOIN leads_closed c ON q.mql_id = c.mql_id""",
            ['lead_type', 'business_segment']
        )

if __name__ == "__main__":
    loader = DimensionLoader()
    loader.run_all()