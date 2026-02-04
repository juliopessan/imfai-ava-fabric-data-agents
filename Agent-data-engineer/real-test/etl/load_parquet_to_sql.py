"""
load_parquet_to_sql.py - Carregador de Parquet para SQL Server
============================================================================
Propósito: Ler arquivos Parquet e carregar em SQL Server Landing Layer
Requisito: 2a (LANDING.TRIP_DATA_PARQUET)
Autor: DataFlow Agent
Data: 17 de Novembro de 2025
============================================================================
"""

import pyarrow.parquet as pq
import pandas as pd
import pyodbc
from pathlib import Path
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
CONFIG = {
    'server': 'localhost',  # Ajuste conforme necessário
    'database': 'TEST_PIPELINE',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes',
    'parquet_base_path': r'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files',
    'partitions': ['month=04', 'month=05', 'month=06']
}

# ============================================================================
# CONEXÃO COM SQL SERVER
# ============================================================================
def get_connection():
    """Criar conexão com SQL Server"""
    conn_string = (
        f"DRIVER={CONFIG['driver']};"
        f"SERVER={CONFIG['server']};"
        f"DATABASE={CONFIG['database']};"
        f"Trusted_Connection={CONFIG['trusted_connection']};"
    )
    return pyodbc.connect(conn_string)

# ============================================================================
# LEITURA DE ARQUIVOS PARQUET
# ============================================================================
def read_parquet_partition(partition_path, partition_key):
    """Ler todos os arquivos Parquet de uma partição"""
    logger.info(f"Lendo partição: {partition_key}")
    
    # Encontrar arquivos .parquet na partição
    parquet_files = list(Path(partition_path).glob('*.parquet'))
    
    if not parquet_files:
        logger.warning(f"Nenhum arquivo Parquet encontrado em {partition_path}")
        return pd.DataFrame()
    
    logger.info(f"Encontrados {len(parquet_files)} arquivo(s) Parquet")
    
    # Ler todos os arquivos e combinar
    dfs = []
    for file_path in parquet_files:
        logger.info(f"  • Lendo: {file_path.name}")
        table = pq.read_table(file_path)
        df = table.to_pandas()
        
        # Adicionar metadados
        df['source_file'] = file_path.name
        df['partition_key'] = partition_key
        
        dfs.append(df)
    
    # Combinar todos os DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total de registros lidos: {len(combined_df):,}")
    
    return combined_df

# ============================================================================
# CONVERSÃO PARA VARCHAR (todos os campos)
# ============================================================================
def convert_to_varchar(df):
    """Converter todos os campos para string (VARCHAR)"""
    logger.info("Convertendo todos os campos para VARCHAR...")
    
    # Colunas esperadas
    expected_columns = [
        'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
        'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
        'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
        'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
        'total_amount', 'payment_type', 'trip_type', 'congestion_surcharge'
    ]
    
    # Converter todos para string
    for col in expected_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
            # Substituir 'nan' e 'None' por NULL
            df[col] = df[col].replace(['nan', 'None', 'NaN'], None)
    
    logger.info("✅ Conversão para VARCHAR concluída")
    return df

# ============================================================================
# INSERÇÃO EM SQL SERVER
# ============================================================================
def insert_to_sql(df, conn):
    """Inserir DataFrame em LANDING.TRIP_DATA_PARQUET"""
    logger.info(f"Inserindo {len(df):,} registros em SQL Server...")
    
    cursor = conn.cursor()
    
    # SQL de inserção
    insert_sql = """
    INSERT INTO LANDING.TRIP_DATA_PARQUET (
        VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
        store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
        passenger_count, trip_distance, fare_amount, extra, mta_tax,
        tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
        total_amount, payment_type, trip_type, congestion_surcharge,
        source_file, partition_key
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Preparar dados para inserção em lotes
    batch_size = 1000
    total_inserted = 0
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        # Converter DataFrame para lista de tuplas
        values = [
            tuple(row) for row in batch[[
                'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
                'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
                'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
                'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
                'total_amount', 'payment_type', 'trip_type', 'congestion_surcharge',
                'source_file', 'partition_key'
            ]].values
        ]
        
        # Inserir lote
        cursor.executemany(insert_sql, values)
        conn.commit()
        
        total_inserted += len(batch)
        if total_inserted % 10000 == 0:
            logger.info(f"  • Progresso: {total_inserted:,}/{len(df):,} registros")
    
    logger.info(f"✅ Inserção concluída: {total_inserted:,} registros")
    return total_inserted

# ============================================================================
# PROCESSO PRINCIPAL
# ============================================================================
def main():
    """Processo principal de carregamento"""
    start_time = datetime.now()
    
    logger.info("="*80)
    logger.info("CARREGAMENTO DE PARQUET PARA SQL SERVER")
    logger.info("="*80)
    logger.info("")
    
    try:
        # Conectar ao SQL Server
        logger.info("Conectando ao SQL Server...")
        conn = get_connection()
        logger.info("✅ Conexão estabelecida")
        logger.info("")
        
        total_records = 0
        
        # Processar cada partição
        for partition in CONFIG['partitions']:
            logger.info(f"--- Processando {partition} ---")
            logger.info("")
            
            # Caminho da partição
            partition_path = Path(CONFIG['parquet_base_path']) / partition
            
            if not partition_path.exists():
                logger.warning(f"⚠️  Partição não encontrada: {partition_path}")
                logger.info("")
                continue
            
            # Ler Parquet
            df = read_parquet_partition(partition_path, partition)
            
            if df.empty:
                logger.warning(f"⚠️  Nenhum dado na partição {partition}")
                logger.info("")
                continue
            
            # Converter para VARCHAR
            df = convert_to_varchar(df)
            
            # Inserir no SQL Server
            inserted = insert_to_sql(df, conn)
            total_records += inserted
            
            logger.info("")
        
        # Fechar conexão
        conn.close()
        
        # Sumário
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("="*80)
        logger.info("CARREGAMENTO CONCLUÍDO COM SUCESSO")
        logger.info("="*80)
        logger.info("")
        logger.info(f"Estatísticas:")
        logger.info(f"  • Total de registros carregados: {total_records:,}")
        logger.info(f"  • Partições processadas: {len(CONFIG['partitions'])}")
        logger.info(f"  • Duração: {duration:.2f} segundos")
        logger.info(f"  • Taxa: {total_records/duration:.0f} registros/segundo")
        logger.info("")
        logger.info("Próximo passo:")
        logger.info("  → Execute: 03-load-landing-parquet.sql (finalizar no SQL)")
        logger.info("="*80)
        
    except Exception as e:
        logger.error(f"❌ ERRO: {str(e)}")
        raise

# ============================================================================
# EXECUÇÃO
# ============================================================================
if __name__ == "__main__":
    main()
