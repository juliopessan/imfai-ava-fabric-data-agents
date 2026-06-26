# ============================================
# Financeiro — PySpark ETL Job
# Source: Legacy Cloudera
# Target: Databricks Delta Lake
# Generated: 2026-06-23T09:49:30.635393
# ============================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType

# Initialize Spark
spark = SparkSession.builder \
    .appName("Financeiro-etl-rentabilidade") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.databricks.delta.properties.defaults.enableChangeDataFeed", "true") \
    .getOrCreate()

# 1. READ: Ingest from legacy Cloudera Hive table via JDBC
source_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:hive2://cloudera-host:10000/default") \
    .option("dbtable", "rentabilidade_fact") \
    .option("user", "legacy_user") \
    .option("password", secret("legacy-db-password")) \
    .load()

print(f"✓ Read {source_df.count()} rows from Cloudera")

# 2. TRANSFORM: Cleanse and validate
transformed_df = source_df \
    .where(col("produto_id").isNotNull()) \
    .where(col("periodo_mes") >= "2020-01-01") \
    .withColumn("revenue_brl", col("revenue_brl").cast("decimal(18,2)")) \
    .withColumn("cost_brl", col("cost_brl").cast("decimal(18,2)")) \
    .withColumn("margin_pct", (col("revenue_brl") - col("cost_brl")) / col("revenue_brl") * 100) \
    .withColumn("dw_insert_ts", current_timestamp()) \
    .dropDuplicates(["rentabilidade_id", "periodo_mes"])

print(f"✓ Transformed {transformed_df.count()} rows")

# 3. WRITE: Store in Databricks Delta Lake
transformed_df.write \
    .mode("merge") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .partitionBy("periodo_mes") \
    .option("path", "/mnt/databricks/gold/Financeiro/rentabilidade_facts") \
    .saveAsTable("Financeiro_curated.analytics.rentabilidade_facts")

print("✓ Wrote to Delta Lake with ACID guarantees")

# 4. VALIDATE: Data quality checks
final_count = spark.table("Financeiro_curated.analytics.rentabilidade_facts").count()
null_check = spark.sql('''
SELECT COUNT(*) as nulls 
FROM Financeiro_curated.analytics.rentabilidade_facts 
WHERE produto_id IS NULL OR periodo_mes IS NULL
''').collect()[0][0]

assert null_check == 0, "Found NULL values in key columns"
assert final_count > 0, "No data written to target"

print(f"✓ Data quality passed: {final_count} records, 0 nulls")
print("✓ ETL job completed successfully")
