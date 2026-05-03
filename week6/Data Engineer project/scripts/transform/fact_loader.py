import pandas as pd
import logging
from scripts.common.db_utils import load_config, get_engine
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FactLoader:
    def __init__(self):
        self.config = load_config()
        self.stg_engine = get_engine('staging_db', self.config)
        self.dw_engine = get_engine('dw_db', self.config)

    def to_date_key(self, series):
        """Converts datetime series to YYYYMMDD integer keys."""
        return pd.to_datetime(series).dt.strftime('%Y%m%d').fillna(-1).astype(int)

    def load_fact_orders(self):
        logging.info("Loading fact_orders...")
        
        # 1. Prepare the data in memory first
        orders = pd.read_sql("SELECT * FROM orders", self.stg_engine)
        customers = pd.read_sql("SELECT customer_key, customer_id FROM dim_customer WHERE is_current = True", self.dw_engine)
        statuses = pd.read_sql("SELECT order_status_key, order_status FROM dim_order_status", self.dw_engine)
        
        df = orders.merge(customers, on='customer_id', how='left').merge(statuses, on='order_status', how='left')
        df = df.dropna(subset=['customer_key', 'order_status_key'])

        for col in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        df['purchase_date_key'] = self.to_date_key(df['order_purchase_timestamp'])
        df['approval_date_key'] = self.to_date_key(df['order_approved_at'])
        df['delivery_date_key'] = self.to_date_key(df['order_delivered_customer_date'])
        df['estimated_delivery_date_key'] = self.to_date_key(df['order_estimated_delivery_date'])
        
        df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days.fillna(0).astype(int)
        df['approval_delay'] = (df['order_approved_at'] - df['order_purchase_timestamp']).dt.total_seconds() / 3600
        df['approval_delay'] = df['approval_delay'].fillna(0).astype(int)

        final_df = df[['order_id', 'customer_key', 'order_status_key', 'purchase_date_key', 
                    'approval_date_key', 'delivery_date_key', 'estimated_delivery_date_key', 
                    'delivery_days', 'approval_delay']]

        # 2. CLEAR AND COMMIT (The critical step)
        with self.dw_engine.begin() as conn:
            logging.info("Truncating fact_orders table...")
            conn.execute(text("TRUNCATE TABLE fact_orders CASCADE"))
        
        # 3. INSERT
        try:
            final_df.to_sql('fact_orders', self.dw_engine, if_exists='append', index=False, chunksize=1000)
            logging.info(f"Successfully loaded {len(final_df)} rows into fact_orders.")
        except Exception as e:
            logging.error(f"Failed to load fact_orders: {e}")
    def load_fact_order_items(self):
        logging.info("Loading fact_order_items...")
        
        # 1. Get Staging Data
        items = pd.read_sql("SELECT * FROM order_items", self.stg_engine)
        orders = pd.read_sql("SELECT order_id, customer_id, order_status, order_purchase_timestamp FROM orders", self.stg_engine)
        
        # 2. Get DW Keys
        cust = pd.read_sql("SELECT customer_key, customer_id FROM dim_customer WHERE is_current = True", self.dw_engine)
        prod = pd.read_sql("SELECT product_key, product_id FROM dim_product WHERE is_current = True", self.dw_engine)
        sell = pd.read_sql("SELECT seller_key, seller_id FROM dim_seller WHERE is_current = True", self.dw_engine)

        # 3. Merging (Use 'left' joins to avoid losing data if a key is missing)
        df = items.merge(orders, on='order_id', how='inner')
        df = df.merge(cust, on='customer_id', how='left')
        df = df.merge(prod, on='product_id', how='left')
        df = df.merge(sell, on='seller_id', how='left')

        # 4. Handle missing keys with your -1 default
        fill_cols = ['customer_key', 'product_key', 'seller_key']
        for col in fill_cols:
            df[col] = df[col].fillna(-1).astype(int)

        # 5. Dates & Values
        df['order_date_key'] = self.to_date_key(df['order_purchase_timestamp'])
        df['shipping_limit_date_key'] = self.to_date_key(df['shipping_limit_date'])
        df['total_item_value'] = df['price'] + df['freight_value']

        final_df = df[['order_id', 'customer_key', 'product_key', 'seller_key', 
                       'order_date_key', 'shipping_limit_date_key', 'price', 'freight_value', 'total_item_value']]

        # 6. Clear and Load
        with self.dw_engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE fact_order_items"))
            
        final_df.to_sql('fact_order_items', self.dw_engine, if_exists='append', index=False, chunksize=1000)
        logging.info(f"Successfully loaded {len(final_df)} rows into fact_order_items.")
def load_fact_payments(self):
    logging.info("Starting load for fact_payments...")
    try:
        pay = pd.read_sql("SELECT order_id, payment_type, payment_value, payment_installments FROM order_payments", self.stg_engine)
        types = pd.read_sql("SELECT payment_type_key, payment_type FROM dim_payment_type", self.dw_engine)
        
        df = pay.merge(types, on='payment_type', how='left')
        df['payment_type_key'] = df['payment_type_key'].fillna(-1).astype(int)
        
        final_df = df[['order_id', 'payment_type_key', 'payment_value', 'payment_installments']]
        
        with self.dw_engine.begin() as conn:
            logging.info("Truncating fact_payments table...")
            conn.execute(text("TRUNCATE TABLE fact_payments"))
            
        final_df.to_sql('fact_payments', self.dw_engine, if_exists='append', index=False)
        logging.info(f"SUCCESS: Loaded {len(final_df)} rows into fact_payments.")
    except Exception as e:
        logging.error(f"FAILED to load fact_payments: {e}")

    def load_fact_reviews(self):
        logging.info("Starting load for fact_reviews...")
        try:
            # 1. Get Data
            rev = pd.read_sql("SELECT order_id, review_id, review_score, review_creation_date FROM order_reviews", self.stg_engine)
            dim_r = pd.read_sql("SELECT review_dim_key, review_id FROM dim_review", self.dw_engine)
            
            # 2. Merge to get the Surrogate Key
            df = rev.merge(dim_r, on='review_id', how='left')
            
            # 3. Handle Nulls and Dates
            df['review_dim_key'] = df['review_dim_key'].fillna(-1).astype(int)
            df['review_date_key'] = self.to_date_key(df['review_creation_date'])
            
            final_df = df[['order_id', 'review_date_key', 'review_dim_key', 'review_score']]
            
            # 4. Truncate and Load
            with self.dw_engine.begin() as conn:
                logging.info("Truncating fact_reviews table...")
                conn.execute(text("TRUNCATE TABLE fact_reviews"))
                
            final_df.to_sql('fact_reviews', self.dw_engine, if_exists='append', index=False)
            logging.info(f"SUCCESS: Loaded {len(final_df)} rows into fact_reviews.")
            
        except Exception as e:
            logging.error(f"FAILED to load fact_reviews: {e}")

def load_fact_leads_funnel(self):
    logging.info("Starting load for fact_leads_funnel...")
    try:
        query = """
            SELECT q.mql_id, q.first_contact_date, c.won_date, c.seller_id, 
                   c.declared_monthly_revenue, c.declared_product_catalog_size
            FROM leads_qualified q
            LEFT JOIN leads_closed c ON q.mql_id = c.mql_id
        """
        stg_leads = pd.read_sql(query, self.stg_engine)
        dim_l = pd.read_sql("SELECT lead_key, mql_id FROM dim_lead WHERE is_current = True", self.dw_engine)
        dim_s = pd.read_sql("SELECT seller_key, seller_id FROM dim_seller WHERE is_current = True", self.dw_engine)

        df = stg_leads.merge(dim_l, on='mql_id', how='inner').merge(dim_s, on='seller_id', how='left')
        
        df['first_contact_date_key'] = self.to_date_key(df['first_contact_date'])
        df['won_date_key'] = self.to_date_key(df['won_date'])
        df['conversion_flag'] = df['won_date'].notnull().astype(int)
        df['seller_key'] = df['seller_key'].fillna(-1).astype(int)

        final_df = df[['lead_key', 'seller_key', 'first_contact_date_key', 'won_date_key', 
                       'conversion_flag', 'declared_monthly_revenue', 'declared_product_catalog_size']]
        
        with self.dw_engine.begin() as conn:
            logging.info("Truncating fact_leads_funnel table...")
            conn.execute(text("TRUNCATE TABLE fact_leads_funnel"))
            
        final_df.to_sql('fact_leads_funnel', self.dw_engine, if_exists='append', index=False)
        logging.info(f"SUCCESS: Loaded {len(final_df)} rows into fact_leads_funnel.")
    except Exception as e:
        logging.error(f"FAILED to load fact_leads_funnel: {e}")

    def run_all(self):
        self.load_fact_orders()
        self.load_fact_order_items()
        self.load_fact_payments()
        self.load_fact_reviews()
        self.load_fact_leads_funnel()

