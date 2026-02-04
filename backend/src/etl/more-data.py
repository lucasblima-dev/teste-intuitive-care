import pandas as pd
import requests
import io
import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

if not all([DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT]):
    logger.error("ERRO: Variáveis de ambiente não encontradas")
    exit(1)

URL_CADASTRO = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

def get_db_engine():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def find_header_and_read(csv_content):
    attempts = [0, 1, 2, 3] # Ajuste para corrigir pulo de linhas nos arquivos da ANS
    encodings = ['latin1', 'utf-8']
    separators = [';', ',']

    for enc in encodings:
        for sep in separators:
            for skip in attempts:
                try:
                    csv_content.seek(0)
                    df = pd.read_csv(csv_content, sep=sep, encoding=enc, skiprows=skip, on_bad_lines='skip', nrows=5)
                    
                    cols = [c.strip().replace('"', '').upper() for c in df.columns]
                    
                    has_reg = any("REGISTRO" in c for c in cols)
                    has_razao = any("RAZAO" in c or "RAZÃO" in c for c in cols)
                    
                    if has_reg and has_razao:
                        csv_content.seek(0)
                        return pd.read_csv(csv_content, sep=sep, encoding=enc, skiprows=skip, on_bad_lines='skip')
                except:
                    continue
    return None

def enrich_operadoras():    
    try:
        response = requests.get(URL_CADASTRO, timeout=60)
        response.raise_for_status()
        csv_content = io.BytesIO(response.content)

        df = find_header_and_read(csv_content)

        if df is None:
            logger.error("ERRO: Não foi possível detectar o formato do CSV")
            return

        df.columns = [c.strip().replace('"', '').upper() for c in df.columns]
        
        col_reg = next((c for c in df.columns if "REGISTRO" in c), None)
        col_razao = next((c for c in df.columns if "RAZAO" in c or "RAZÃO" in c), None)
        col_uf = next((c for c in df.columns if "UF" == c), None)

        df_clean = df[[col_reg, col_razao, col_uf]].copy()
        df_clean.columns = ['reg_ans', 'razao_social', 'uf']
        df_clean['reg_ans'] = pd.to_numeric(df_clean['reg_ans'], errors='coerce')
        df_clean = df_clean.dropna(subset=['reg_ans'])

        engine = get_db_engine()
        with engine.connect() as conn:
            conn.execute(text("UPDATE operadoras SET razao_social = NULL, uf = NULL;"))
            conn.commit()

            df_clean.to_sql('temp_cadop_ans', engine, if_exists='replace', index=False)
            
            logger.info("Atualizando registros...")
            sql_update = text("""
                UPDATE operadoras o
                SET razao_social = t.razao_social, uf = t.uf
                FROM temp_cadop_ans t
                WHERE o.reg_ans = t.reg_ans;
            """)
            conn.execute(sql_update)
            conn.execute(text("DROP TABLE temp_cadop_ans"))
            conn.commit()
            
    except Exception as e:
        logger.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    enrich_operadoras()