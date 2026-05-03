import pandas as pd
import logging
from scripts.common.db_utils import load_config, get_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_extraction():
    config = load_config()
    sqlite_engine = get_engine('sqlite', config)
    staging_engine = get_engine('staging_db', config)
    
    for table_name in config['tables_to_extract']:
        try:
            logging.info(f"--- Starting Extraction: {table_name} ---")
            

            for chunk in pd.read_sql_table(table_name, sqlite_engine, chunksize=10000):

                chunk.to_sql(
                    name=table_name,
                    con=staging_engine,
                    if_exists='append', # Update to 'replace' if DDL isn't pre-created
                    index=False,
                    method='multi'
                )
            
            logging.info(f"Successfully moved {table_name} to staging.")
            
        except Exception as e:
            logging.error(f"Error during extraction of {table_name}: {e}")
            raise
