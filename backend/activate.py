import logging
import time
from src.etl.process import run_etl
from src.db.import_data import load_data
from src.etl.enrich_data import enrich_operadoras

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Pipeline")

def run_full_pipeline():

    try:
        logger.info(">Download dos dados...")
        run_etl()
        logger.info(f"Tudo certo!")

        logger.info(">Persistência dos dados...")
        load_data()
        logger.info(f"Tudo certo!")

        logger.info(">Dados reais (razão social e ufs)...")
        enrich_operadoras()
        logger.info(f"Tudo certo!")

        logger.info(f"Processo ok!")

    except Exception as e:
        exit(1)

if __name__ == "__main__":
    run_full_pipeline()