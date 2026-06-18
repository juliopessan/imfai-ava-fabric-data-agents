# Spark Job: Hive → Databricks (rentabilidade_diaria)
# Generated: 2026-06-16
# Source: Cloudera Hive
# Target: Databricks - rentabilidade.raw.tb_rentabilidade_diaria

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HiveToDatabricksMigration:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("hive-to-databricks-rentabilidade") \
            .config("spark.databricks.delta.merge.enableLowShuffle", "true") \
            .config("spark.sql.adaptive.enabled", "true") \
            .getOrCreate()
    
    def read_from_hive(self, table_name):
        """Read data from Hive."""
        logger.info(f"Reading from Hive: {table_name}")
        try:
            df = self.spark.table(f"hive_legacy.{table_name}")
            logger.info(f"Read {df.count()} records from {table_name}")
            return df
        except Exception as e:
            logger.error(f"Error reading from Hive: {e}")
            raise
    
    def transform_data(self, df):
        """Apply transformations."""
        logger.info("Applying transformations")
        
        # Clean and validate data
        df_transformed = df \
            .dropna(subset=['id_cliente', 'data_calculo']) \
            .withColumn('rentabilidade', col('rentabilidade').cast('decimal(15,4)')) \
            .withColumn('comissao', col('comissao').cast('decimal(15,4)')) \
            .withColumn('data_atualizacao', current_timestamp())
        
        logger.info(f"Transformed {df_transformed.count()} records")
        return df_transformed
    
    def write_to_databricks(self, df, table_name):
        """Write to Databricks Delta table."""
        logger.info(f"Writing to Databricks: {table_name}")
        
        df.write \
            .format("delta") \
            .mode("append") \
            .partitionBy("data_calculo") \
            .option("mergeSchema", "true") \
            .saveAsTable(table_name)
        
        logger.info(f"Successfully wrote to {table_name}")
    
    def migrate(self, source_table, target_table):
        """Execute complete migration."""
        try:
            logger.info(f"Starting migration: {source_table} → {target_table}")
            
            # Read
            df = self.read_from_hive(source_table)
            
            # Transform
            df_transformed = self.transform_data(df)
            
            # Write
            self.write_to_databricks(df_transformed, target_table)
            
            logger.info("Migration completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False

if __name__ == "__main__":
    migrator = HiveToDatabricksMigration()
    
    # Migrate rentabilidade_diaria
    success = migrator.migrate(
        source_table="rentabilidade_diaria",
        target_table="rentabilidade.raw.tb_rentabilidade_diaria"
    )
    
    exit(0 if success else 1)
