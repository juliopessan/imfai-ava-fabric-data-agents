# Streaming Job: Python → Databricks (Real-time Lineage)
# Generated: 2026-06-16
# Source: Python application
# Target: Databricks - procedencia.raw.tb_linhagem_dados

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, struct
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
import logging

logger = logging.getLogger(__name__)

class LineageStreamingJob:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("lineage-streaming-databricks") \
            .getOrCreate()
    
    def setup_schema(self):
        """Define lineage event schema."""
        schema = StructType([
            StructField("id_linhagem", StringType(), False),
            StructField("tabela_origem", StringType(), False),
            StructField("tabela_destino", StringType(), False),
            StructField("algoritmo", StringType(), True),
            StructField("data_processamento", TimestampType(), False)
        ])
        return schema
    
    def read_from_kafka(self):
        """Read lineage events from Kafka."""
        logger.info("Starting Kafka stream reader")
        
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", "lineage-events") \
            .option("startingOffsets", "latest") \
            .load()
        
        return df
    
    def write_to_databricks(self, df):
        """Write stream to Databricks."""
        logger.info("Starting stream write to Databricks")
        
        query = df \
            .writeStream \
            .format("delta") \
            .option("path", "/mnt/data/procedencia/tb_linhagem_dados") \
            .option("checkpointLocation", "/mnt/data/checkpoints/lineage") \
            .outputMode("append") \
            .start()
        
        query.awaitTermination()
    
    def run(self):
        """Execute streaming pipeline."""
        try:
            logger.info("Starting lineage streaming pipeline")
            df = self.read_from_kafka()
            self.write_to_databricks(df)
        except Exception as e:
            logger.error(f"Streaming pipeline failed: {e}")

if __name__ == "__main__":
    job = LineageStreamingJob()
    job.run()
