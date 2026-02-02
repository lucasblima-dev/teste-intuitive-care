import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

def get_engine():
    return create_engine(DB_URL)

def load_data():
    csv_path = "data/processed/consolidado_despesas.csv"
    
    if not os.path.exists(csv_path):
        logger.error("Arquivo CSV não encontrado. Rode a Fase 1 primeiro.")
        return

    logger.info("Lendo CSV processado...")
    df = pd.read_csv(csv_path)

    df.columns = [c.strip().upper() for c in df.columns]
    
    logger.info("Normalizando Operadoras")
    df_ops = df[['REG_ANS']].drop_duplicates().copy()
    
    # Razão social como null apenas para teste
    if 'RAZAO_SOCIAL' in df.columns:
        df_ops['razao_social'] = df['RAZAO_SOCIAL']
    else:
        df_ops['razao_social'] = None 
        
    df_ops.columns = ['reg_ans', 'razao_social'] if 'razao_social' in df_ops.columns else ['reg_ans', 'razao_social']

    logger.info("Preparando Despesas")
    df_desp = df.copy()
    
    col_map = {
        'REG_ANS': 'reg_ans',
        'DESCRICAO': 'descricao_conta',
        'VL_SALDO_FINAL': 'valor',
        'ANO': 'ano',
        'TRIMESTRE': 'trimestre'
    }
    df_desp = df_desp.rename(columns=col_map)
    
    df_desp['valor'] = pd.to_numeric(df_desp['valor'], errors='coerce')
    
    cols_to_keep = ['reg_ans', 'descricao_conta', 'ano', 'trimestre', 'valor']
    df_desp = df_desp[cols_to_keep]

    engine = get_engine()
    
    try:
        with engine.connect() as conn:
            with open("src/db/schema.sql", "r") as f:
                conn.execute(text(f.read()))
                conn.commit()
                        
            logger.info("Inserindo Operadoras")

            existing_ops = pd.read_sql("SELECT reg_ans FROM operadoras", conn)
            df_ops = df_ops[~df_ops['reg_ans'].isin(existing_ops['reg_ans'])]
            
            df_ops.to_sql('operadoras', engine, if_exists='append', index=False)
            
            logger.info("Inserindo Despesas")

            df_desp.to_sql('despesas', engine, if_exists='append', index=False)
            
            conn.commit()
            logger.info("Carga concluída com sucesso!")
            
    except Exception as e:
        logger.error(f"Erro no banco de dados: {e}")

if __name__ == "__main__":
    load_data()