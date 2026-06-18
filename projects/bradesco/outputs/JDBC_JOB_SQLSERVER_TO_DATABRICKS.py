# Job: SQL Server → Databricks via JDBC
# Generated: 2026-06-16
# Source: SQL Server
# Target: Databricks - rentabilidade.processed.tb_rentabilidade_consolidada

from pyspark.sql import SparkSession
import logging

logger = logging.getLogger(__name__)

class SQLServerToDatabricksMigration:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("sqlserver-to-databricks-rentabilidade") \
            .getOrCreate()
        
        self.jdbc_url = "jdbc:sqlserver://sqlserver-legacy:1433;database=rentabilidade"
        self.jdbc_driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    
    def read_from_sqlserver(self, table_name, user, password):
        """Read from SQL Server via JDBC."""
        logger.info(f"Reading from SQL Server: {table_name}")
        
        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", user) \
            .option("password", password) \
            .option("driver", self.jdbc_driver) \
            .load()
        
        logger.info(f"Read {df.count()} records")
        return df
    
    def write_to_databricks(self, df, target_table):
        """Write to Databricks."""
        logger.info(f"Writing to Databricks: {target_table}")
        
        df.write \
            .format("delta") \
            .mode("append") \
            .partitionBy("periodo") \
            .saveAsTable(target_table)
        
        logger.info("Write completed")
    
    def migrate(self, source_table, target_table, user, password):
        """Execute migration."""
        try:
            df = self.read_from_sqlserver(source_table, user, password)
            self.write_to_databricks(df, target_table)
            return True
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False

if __name__ == "__main__":
    migrator = SQLServerToDatabricksMigration()
    success = migrator.migrate(
        source_table="dbo.rentabilidade_consolidada",
        target_table="rentabilidade.processed.tb_rentabilidade_consolidada",
        user="dbuser",
        password="<password>"  # Use Databricks secrets
    )
    exit(0 if success else 1)
