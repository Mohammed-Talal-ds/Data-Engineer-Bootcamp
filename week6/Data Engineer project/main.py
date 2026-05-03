# main.py
from scripts.extract.sqlite_to_stage import run_extraction
from scripts.transform.dim_loader import DimensionLoader
from scripts.transform.fact_loader import FactLoader
import logging

def main():
    logging.info("--- STARTING ETL PIPELINE ---")
    
    run_extraction()
    
    dim_loader = DimensionLoader()
    dim_loader.run_all()
    
    fact_loader = FactLoader()
    fact_loader.run_all()
    
    logging.info("--- ETL PIPELINE COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    main()