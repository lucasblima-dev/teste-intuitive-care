import os
import requests
import zipfile
import pandas as pd
import logging
import re
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Decidir depois se vou deixar hardcoded ou fazer um scraper
URLS_FONTE = [
    {"ano": 2025, "trimestre": "1T", "url": "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/1T2025.zip"},
    {"ano": 2025, "trimestre": "2T", "url": "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/2T2025.zip"},
    {"ano": 2025, "trimestre": "3T", "url": "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/3T2025.zip"},
]

def download_and_extract(url_info: dict):
    filename = f"{url_info['ano']}_{url_info['trimestre']}.zip"
    filepath = os.path.join(RAW_DIR, filename)
    extract_path = os.path.join(RAW_DIR, f"{url_info['ano']}_{url_info['trimestre']}")
    
    logger.info(f"Iniciando download: {url_info['trimestre']}/{url_info['ano']}")
    
    try:
        response = requests.get(url_info['url'], stream=True, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            
        logger.info(f"Sucesso ao baixar e extrair: {filename}")
        return extract_path
    except Exception as e:
        logger.error(f"Erro ao processar {url_info['url']}: {e}")
        return None

def normalize_csv(file_path: str, ano: int, trimestre: str) -> pd.DataFrame:
    try:
        try:
            df = pd.read_csv(file_path, sep=';', encoding='latin1', on_bad_lines='skip')
        except:
            df = pd.read_csv(file_path, sep=',', encoding='utf-8', on_bad_lines='skip')

        df.columns = [c.strip().upper() for c in df.columns]

        colunas_necessarias = ['REG_ANS', 'CD_CONTA_CONTABIL', 'DESCRICAO', 'VL_SALDO_FINAL']
        
        if not set(['VL_SALDO_FINAL']).issubset(df.columns):
            return pd.DataFrame()

        if 'DESCRICAO' in df.columns:
            df = df[df['DESCRICAO'].astype(str).str.contains('EVENTOS|SINISTROS|DESPESA', na=False, case=False)]
        
        df['ANO'] = ano
        df['TRIMESTRE'] = trimestre
        
        return df

    except Exception as e:
        logger.warning(f"Não foi possível ler o arquivo {file_path}: {e}")
        return pd.DataFrame()

def run_etl():
    all_data = []

    for item in URLS_FONTE:
        path = download_and_extract(item)
        if not path: continue

        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.csv', '.txt')):
                    full_path = os.path.join(root, file)
                    logger.info(f"Processando arquivo: {file}")
                    df_temp = normalize_csv(full_path, item['ano'], item['trimestre'])
                    
                    if not df_temp.empty:
                        all_data.append(df_temp)

    if not all_data:
        logger.error("Nenhum dado foi processado.")
        return

    logger.info("Consolidando dados...")
    df_final = pd.concat(all_data, ignore_index=True)

    df_final['VL_SALDO_FINAL'] = pd.to_numeric(df_final['VL_SALDO_FINAL'].astype(str).str.replace(',', '.'), errors='coerce')
    df_final = df_final[df_final['VL_SALDO_FINAL'] > 0]

    output_csv = os.path.join(PROCESSED_DIR, 'consolidado_despesas.csv')
    df_final.to_csv(output_csv, index=False, encoding='utf-8')
    
    with zipfile.ZipFile(os.path.join(PROCESSED_DIR, 'consolidado_despesas.zip'), 'w') as zipf:
        zipf.write(output_csv, arcname='consolidado_despesas.csv')
    
    logger.info(f"Processo concluído. Arquivo salvo em {output_csv}")

if __name__ == "__main__":
    run_etl()