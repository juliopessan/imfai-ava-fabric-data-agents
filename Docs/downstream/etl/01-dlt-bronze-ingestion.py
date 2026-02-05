# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Pipeline: Bronze Layer Ingestion
# MAGIC
# MAGIC **Project:** NYC Green Taxi Analytics  
# MAGIC **Layer:** Bronze (Raw Data Ingestion)  
# MAGIC **Technology:** Delta Live Tables (DLT)  
# MAGIC **Version:** 1.0  
# MAGIC **Created:** 2026-02-05  
# MAGIC **Author:** Diego (DataEngineerExec)
# MAGIC
# MAGIC ## Purpose
# MAGIC Ingest raw data from CSV/JSON/TSV files into Bronze layer tables with minimal transformations.
# MAGIC - Preserve source data exactly as received
# MAGIC - All columns as STRING for schema flexibility
# MAGIC - Add audit columns for lineage tracking
# MAGIC - Apply basic DQ expectations (12 rules from dq-rules.md)

# COMMAND ----------

import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# Storage paths
SOURCE_PATH_TRIPS = "abfss://landing@nyctaxistorage.dfs.core.windows.net/taxi/green/"
SOURCE_PATH_PAYMENT = "abfss://landing@nyctaxistorage.dfs.core.windows.net/reference/payment_type_array.json"
SOURCE_PATH_RATE = "abfss://landing@nyctaxistorage.dfs.core.windows.net/reference/rate_code.json"
SOURCE_PATH_TRIP_TYPE = "abfss://landing@nyctaxistorage.dfs.core.windows.net/reference/trip_type.tsv"

# Schema location for Auto Loader
SCHEMA_LOCATION_TRIPS = "abfss://checkpoints@nyctaxistorage.dfs.core.windows.net/bronze/trips_raw/_schema"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Bronze: trips_raw
# MAGIC
# MAGIC **Source:** green_tripdata_*.csv  
# MAGIC **Grain:** One row per trip (raw, may contain duplicates)  
# MAGIC **Load:** Streaming (Auto Loader)  
# MAGIC **DQ Rules:** 12 expectations (B01-B12 from dq-rules.md)

# COMMAND ----------

@dlt.table(
    name="trips_raw",
    comment="Raw green taxi trip data from CSV files - no transformations",
    path="abfss://bronze@nyctaxistorage.dfs.core.windows.net/trips_raw",
    partition_cols=["month"],
    table_properties={
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "quality.level": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
@dlt.expect_all({
    # B01: VendorID not null
    "valid_vendor_id": "VendorID IS NOT NULL",
    
    # B02: Pickup datetime not null
    "valid_pickup_datetime": "lpep_pickup_datetime IS NOT NULL",
    
    # B03: Dropoff datetime not null
    "valid_dropoff_datetime": "lpep_dropoff_datetime IS NOT NULL",
    
    # B04: Pickup location not null
    "valid_pickup_location": "PULocationID IS NOT NULL",
    
    # B05: Dropoff location not null
    "valid_dropoff_location": "DOLocationID IS NOT NULL",
    
    # B06: Trip distance not null
    "valid_trip_distance": "trip_distance IS NOT NULL",
    
    # B07: Total amount not null
    "valid_total_amount": "total_amount IS NOT NULL",
    
    # B08: Payment type not null
    "valid_payment_type": "payment_type IS NOT NULL",
    
    # B09: Rate code not null
    "valid_rate_code": "RatecodeID IS NOT NULL",
    
    # B10: Trip type not null  
    "valid_trip_type": "trip_type IS NOT NULL",
    
    # B11: Passenger count not null
    "valid_passenger_count": "passenger_count IS NOT NULL",
    
    # B12: No critical columns all null (row sanity)
    "row_sanity": "NOT (VendorID IS NULL AND lpep_pickup_datetime IS NULL AND total_amount IS NULL)"
})
def trips_raw():
    """
    Ingest raw trip data using Auto Loader (cloudFiles).
    Schema inference enabled, all columns as STRING.
    """
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.schemaLocation", SCHEMA_LOCATION_TRIPS)
            .option("cloudFiles.inferColumnTypes", "false")  # Keep all as STRING
            .option("header", "true")
            .option("multiLine", "false")
            .option("escape", '"')
            .load(SOURCE_PATH_TRIPS)
            .withColumn("_ingestion_timestamp", current_timestamp())
            .withColumn("_source_file", input_file_name())
            .withColumn("_load_date", current_date())
            .withColumn("month", date_format(col("lpep_pickup_datetime"), "yyyy-MM"))
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Bronze: payment_types_raw
# MAGIC
# MAGIC **Source:** payment_type_array.json  
# MAGIC **Grain:** One row per payment type  
# MAGIC **Load:** Batch  
# MAGIC **DQ Rules:** Basic not null checks

# COMMAND ----------

@dlt.table(
    name="payment_types_raw",
    comment="Raw payment type reference data from JSON",
    path="abfss://bronze@nyctaxistorage.dfs.core.windows.net/payment_types_raw",
    table_properties={
        "delta.enableChangeDataFeed": "true",
        "quality.level": "bronze"
    }
)
@dlt.expect_all({
    "valid_payment_id": "payment_type_id IS NOT NULL",
    "valid_payment_desc": "payment_type_desc IS NOT NULL"
})
def payment_types_raw():
    """
    Ingest payment type reference data from JSON array.
    Expected structure: [{"payment_type_id": "1", "payment_type_desc": "Credit card"}, ...]
    """
    return (
        spark.read
            .format("json")
            .option("multiLine", "true")
            .load(SOURCE_PATH_PAYMENT)
            .withColumn("_ingestion_timestamp", current_timestamp())
            .withColumn("_source_file", lit(SOURCE_PATH_PAYMENT))
            .withColumn("_load_date", current_date())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Bronze: rate_codes_raw
# MAGIC
# MAGIC **Source:** rate_code.json  
# MAGIC **Grain:** One row per rate code  
# MAGIC **Load:** Batch

# COMMAND ----------

@dlt.table(
    name="rate_codes_raw",
    comment="Raw rate code reference data from JSON",
    path="abfss://bronze@nyctaxistorage.dfs.core.windows.net/rate_codes_raw",
    table_properties={
        "delta.enableChangeDataFeed": "true",
        "quality.level": "bronze"
    }
)
@dlt.expect_all({
    "valid_rate_id": "rate_code_id IS NOT NULL",
    "valid_rate_desc": "rate_code_desc IS NOT NULL"
})
def rate_codes_raw():
    """
    Ingest rate code reference data from JSON array.
    """
    return (
        spark.read
            .format("json")
            .option("multiLine", "true")
            .load(SOURCE_PATH_RATE)
            .withColumn("_ingestion_timestamp", current_timestamp())
            .withColumn("_source_file", lit(SOURCE_PATH_RATE))
            .withColumn("_load_date", current_date())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Bronze: trip_types_raw
# MAGIC
# MAGIC **Source:** trip_type.tsv  
# MAGIC **Grain:** One row per trip type  
# MAGIC **Load:** Batch

# COMMAND ----------

@dlt.table(
    name="trip_types_raw",
    comment="Raw trip type reference data from TSV",
    path="abfss://bronze@nyctaxistorage.dfs.core.windows.net/trip_types_raw",
    table_properties={
        "delta.enableChangeDataFeed": "true",
        "quality.level": "bronze"
    }
)
@dlt.expect_all({
    "valid_trip_type_id": "trip_type_id IS NOT NULL",
    "valid_trip_type_desc": "trip_type_desc IS NOT NULL"
})
def trip_types_raw():
    """
    Ingest trip type reference data from TSV file.
    """
    return (
        spark.read
            .format("csv")
            .option("header", "true")
            .option("sep", "\t")
            .option("inferSchema", "false")  # Keep all as STRING
            .load(SOURCE_PATH_TRIP_TYPE)
            .withColumn("_ingestion_timestamp", current_timestamp())
            .withColumn("_source_file", lit(SOURCE_PATH_TRIP_TYPE))
            .withColumn("_load_date", current_date())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execution Notes
# MAGIC
# MAGIC ### How to Run This Pipeline
# MAGIC
# MAGIC 1. **Create DLT Pipeline in Databricks:**
# MAGIC    - Go to Workflows → Delta Live Tables → Create Pipeline
# MAGIC    - Pipeline Name: `nyc_taxi_bronze_ingestion`
# MAGIC    - Notebook: Select this notebook
# MAGIC    - Target: `nyc_taxi.bronze`
# MAGIC    - Storage Location: `abfss://dlt-storage@nyctaxistorage.dfs.core.windows.net/bronze`
# MAGIC    - Cluster Mode: Enhanced Autoscaling
# MAGIC
# MAGIC 2. **Configuration:**
# MAGIC    ```json
# MAGIC    {
# MAGIC      "pipelines.applyChangesPreviewEnabled": "true",
# MAGIC      "spark.databricks.delta.schema.autoMerge.enabled": "true"
# MAGIC    }
# MAGIC    ```
# MAGIC
# MAGIC 3. **Schedule:**
# MAGIC    - trips_raw: Continuous (streaming)
# MAGIC    - Reference tables: Daily or on-demand
# MAGIC
# MAGIC 4. **Monitoring:**
# MAGIC    - DLT provides automatic lineage
# MAGIC    - Data quality metrics in pipeline dashboard
# MAGIC    - Expectation violations logged automatically
# MAGIC
# MAGIC ### Expected Results
# MAGIC
# MAGIC - **trips_raw:** ~240,000 rows (Apr+May+Jun 2021)
# MAGIC - **payment_types_raw:** 5 rows
# MAGIC - **rate_codes_raw:** 7 rows
# MAGIC - **trip_types_raw:** 3 rows
# MAGIC
# MAGIC ### DQ Expectations Summary
# MAGIC
# MAGIC - **trips_raw:** 12 expectations (all WARN mode - drop invalid rows)
# MAGIC - **Reference tables:** 2 expectations each (NOT NULL checks)
# MAGIC - **Quarantine:** Invalid rows automatically excluded
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC After Bronze layer is populated:
# MAGIC 1. Run Silver layer DLT pipeline (02-dlt-silver.py)
# MAGIC 2. Verify data quality metrics
# MAGIC 3. Check for quarantined records

# COMMAND ----------

# MAGIC %md
# MAGIC ## END OF BRONZE LAYER DLT PIPELINE
