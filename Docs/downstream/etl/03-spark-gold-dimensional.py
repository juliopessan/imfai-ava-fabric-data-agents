# Databricks notebook source
# MAGIC %md
# MAGIC # Spark SQL: Gold Layer - Dimensional Model Build
# MAGIC
# MAGIC **Project:** NYC Green Taxi Analytics  
# MAGIC **Layer:** Gold (Business-Ready Star Schema)  
# MAGIC **Technology:** Spark SQL (Batch Processing)  
# MAGIC **Version:** 1.0  
# MAGIC **Created:** 2026-02-05  
# MAGIC **Author:** Diego (data-engineer-exec)
# MAGIC
# MAGIC ## Purpose
# MAGIC Build Star Schema dimensional model from Silver layer:
# MAGIC - Generate dim_date (calendar table 2021-2025)
# MAGIC - Load dim_location (NYC Taxi Zones)
# MAGIC - Build dimensions from Silver reference tables
# MAGIC - Build fact_trips with FK joins and validations
# MAGIC - Create aggregated fact for performance
# MAGIC - Apply 15 Gold DQ expectations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG nyc_taxi;
# MAGIC USE SCHEMA gold;

# COMMAND ----------

# Python config
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime, timedelta

# Date range for dim_date
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2025, 12, 31)

# NYC Taxi Zones source (public dataset)
NYC_ZONES_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Build dim_date (Calendar Dimension)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1 Generate Date Spine

# COMMAND ----------

def generate_date_dimension(start_date, end_date):
    """
    Generate complete calendar dimension from start_date to end_date.
    Includes year, quarter, month, week, day attributes and business day flags.
    """
    from datetime import timedelta
    import calendar
    
    # Generate date list
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append((current_date,))
        current_date += timedelta(days=1)
    
    # Create DataFrame
    df_dates = spark.createDataFrame(date_list, ["full_date"])
    
    # Add all calendar attributes
    df_calendar = (
        df_dates
        # Surrogate key (YYYYMMDD format)
        .withColumn("date_key", date_format(col("full_date"), "yyyyMMdd").cast("int"))
        
        # Year attributes
        .withColumn("year", year(col("full_date")))
        .withColumn("year_name", year(col("full_date")).cast("string"))
        
        # Quarter attributes
        .withColumn("quarter", quarter(col("full_date")))
        .withColumn("quarter_name", concat(lit("Q"), quarter(col("full_date")), lit(" "), year(col("full_date"))))
        
        # Month attributes
        .withColumn("month", month(col("full_date")))
        .withColumn("month_name", date_format(col("full_date"), "MMMM"))
        .withColumn("month_abbr", date_format(col("full_date"), "MMM"))
        .withColumn("year_month", date_format(col("full_date"), "yyyy-MM"))
        
        # Week attributes
        .withColumn("week_of_year", weekofyear(col("full_date")))
        .withColumn("week_of_month", 
                   ((dayofmonth(col("full_date")) - 1) / 7).cast("int") + 1)
        
        # Day attributes
        .withColumn("day_of_month", dayofmonth(col("full_date")))
        .withColumn("day_of_year", dayofyear(col("full_date")))
        .withColumn("day_of_week", dayofweek(col("full_date")))  # 1=Sunday, 7=Saturday
        .withColumn("day_name", date_format(col("full_date"), "EEEE"))
        .withColumn("day_abbr", date_format(col("full_date"), "EEE"))
        
        # Business day flags
        .withColumn("is_weekend", when(col("day_of_week").isin(1, 7), True).otherwise(False))
        .withColumn("is_weekday", when(col("day_of_week").between(2, 6), True).otherwise(False))
        
        # Holiday flags (simplified - major US federal holidays)
        .withColumn("is_holiday", lit(False))  # Can be enhanced with holiday calendar
        .withColumn("holiday_name", lit(None).cast("string"))
        
        # Fiscal calendar (optional - can customize)
        .withColumn("fiscal_year", col("year"))
        .withColumn("fiscal_quarter", col("quarter"))
        .withColumn("fiscal_month", col("month"))
        
        # Audit
        .withColumn("_created_timestamp", current_timestamp())
    )
    
    return df_calendar

# COMMAND ----------

# Generate and write dim_date
df_dim_date = generate_date_dimension(START_DATE, END_DATE)

df_dim_date.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("dim_date")

print(f"✅ dim_date created: {df_dim_date.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Build dim_location (NYC Taxi Zones)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.1 Load NYC Taxi Zone Lookup

# COMMAND ----------

# Load NYC Taxi Zones from public dataset
df_taxi_zones = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(NYC_ZONES_URL)
)

# Build dim_location
df_dim_location = (
    df_taxi_zones
    # Surrogate key (same as natural key for simplicity)
    .withColumn("location_key", col("LocationID").cast("int"))
    .withColumn("zone_id", col("LocationID").cast("int"))
    .withColumn("zone_name", col("Zone"))
    .withColumn("borough", col("Borough"))
    .withColumn("service_zone", col("service_zone"))
    
    # Derived attributes
    .withColumn("is_airport", 
               when(col("zone_name").rlike("(?i)(JFK|LaGuardia|Newark)"), True).otherwise(False))
    .withColumn("is_manhattan",
               when(col("borough") == "Manhattan", True).otherwise(False))
    
    # Placeholders for geospatial (can be enhanced)
    .withColumn("latitude", lit(None).cast("decimal(10,6)"))
    .withColumn("longitude", lit(None).cast("decimal(10,6)"))
    
    # Audit
    .withColumn("_created_timestamp", current_timestamp())
    .withColumn("_updated_timestamp", lit(None).cast("timestamp"))
    .withColumn("_updated_by", lit(None).cast("string"))
    
    .select(
        "location_key",
        "zone_id",
        "zone_name",
        "borough",
        "service_zone",
        "is_airport",
        "is_manhattan",
        "latitude",
        "longitude",
        "_created_timestamp",
        "_updated_timestamp",
        "_updated_by"
    )
)

df_dim_location.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("dim_location")

print(f"✅ dim_location created: {df_dim_location.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Build Dimension Tables from Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 3.1 dim_payment
# MAGIC CREATE OR REPLACE TABLE dim_payment
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
#MAGIC   ROW_NUMBER() OVER (ORDER BY payment_type_id) AS payment_key,
#  MAGIC   payment_type_id,
#  MAGIC   payment_type_desc,
#  MAGIC   is_card_payment,
#  MAGIC   CASE WHEN payment_type_id = 2 THEN TRUE ELSE FALSE END AS is_cash_payment,
#  MAGIC   is_card_payment AS records_tip,  -- Card payments record tips
#  MAGIC   is_active,
#  MAGIC   CURRENT_TIMESTAMP() AS _created_timestamp,
#  MAGIC   CAST(NULL AS TIMESTAMP) AS _updated_timestamp,
#  MAGIC   CAST(NULL AS STRING) AS _updated_by
#  MAGIC FROM silver.payment_types;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 3.2 dim_rate
# MAGIC CREATE OR REPLACE TABLE dim_rate
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
#  MAGIC   ROW_NUMBER() OVER (ORDER BY rate_code_id) AS rate_key,
#  MAGIC   rate_code_id,
#  MAGIC   rate_code_desc,
#  MAGIC   is_airport_trip,
#  MAGIC   CASE WHEN rate_code_id = 5 THEN TRUE ELSE FALSE END AS is_negotiated,
#  MAGIC   CASE WHEN rate_code_id = 1 THEN TRUE ELSE FALSE END AS is_standard,
#  MAGIC   is_active,
#  MAGIC   CURRENT_TIMESTAMP() AS _created_timestamp,
#  MAGIC   CAST(NULL AS TIMESTAMP) AS _updated_timestamp,
#  MAGIC   CAST(NULL AS STRING) AS _updated_by
#  MAGIC FROM silver.rate_codes;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 3.3 dim_trip_type
# MAGIC CREATE OR REPLACE TABLE dim_trip_type
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
#  MAGIC   ROW_NUMBER() OVER (ORDER BY trip_type_id) AS trip_type_key,
#  MAGIC   trip_type_id,
#  MAGIC   trip_type_desc,
#  MAGIC   is_dispatch,
#  MAGIC   CASE WHEN trip_type_id = 1 THEN TRUE ELSE FALSE END AS is_street_hail,
#  MAGIC   is_active,
#  MAGIC   CURRENT_TIMESTAMP() AS _created_timestamp,
#  MAGIC   CAST(NULL AS TIMESTAMP) AS _updated_timestamp,
#  MAGIC   CAST(NULL AS STRING) AS _updated_by
#  MAGIC FROM silver.trip_types;

# COMMAND ----------

print("✅ All dimensions created:")
spark.sql("SELECT 'dim_payment' as dim, COUNT(*) as rows FROM dim_payment UNION ALL SELECT 'dim_rate', COUNT(*) FROM dim_rate UNION ALL SELECT 'dim_trip_type', COUNT(*) FROM dim_trip_type").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Build fact_trips (Star Schema Fact Table)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1 Initial Load (Full)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE fact_trips
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (year, month)
# MAGIC AS
# MAGIC SELECT
#  MAGIC   -- Surrogate key
#  MAGIC   t.trip_id AS trip_key,
#  MAGIC   
#  MAGIC   -- Dimension foreign keys
#  MAGIC   d.date_key,
#  MAGIC   pl.location_key AS pickup_location_key,
#  MAGIC   dl.location_key AS dropoff_location_key,
#  MAGIC   p.payment_key,
#  MAGIC   r.rate_key,
#  MAGIC   tt.trip_type_key,
#  MAGIC   
#  MAGIC   -- Degenerate dimensions
#  MAGIC   t.vendor_id,
#  MAGIC   t.store_and_fwd_flag,
#  MAGIC   
#  MAGIC   -- Temporal measures
#  MAGIC   t.pickup_datetime,
#  MAGIC   t.dropoff_datetime,
#  MAGIC   t.trip_duration_minutes,
#  MAGIC   HOUR(t.pickup_datetime) AS pickup_hour,
#  MAGIC   DAYOFWEEK(t.pickup_datetime) AS pickup_day_of_week,
#  MAGIC   
#  MAGIC   -- Distance measures
#  MAGIC   t.trip_distance_miles,
#  MAGIC   
#  MAGIC   -- Passenger measures
#  MAGIC   t.passenger_count,
#  MAGIC   
#  MAGIC   -- Financial measures
#  MAGIC   t.fare_amount,
#  MAGIC   t.extra,
#  MAGIC   t.mta_tax,
#  MAGIC   t.tip_amount,
#  MAGIC   t.tolls_amount,
#  MAGIC   t.improvement_surcharge,
#  MAGIC   t.congestion_surcharge,
#  MAGIC   t.total_amount,
#  MAGIC   
#  MAGIC   -- Derived metrics
#  MAGIC   t.revenue_per_mile,
#  MAGIC   CASE 
#  MAGIC     WHEN t.trip_duration_minutes > 0 THEN t.total_amount / t.trip_duration_minutes
#  MAGIC     ELSE NULL
#  MAGIC   END AS revenue_per_minute,
#  MAGIC   t.avg_speed_mph,
#  MAGIC   CASE 
#  MAGIC     WHEN t.fare_amount > 0 THEN (t.tip_amount / t.fare_amount) * 100
#  MAGIC     ELSE 0
#  MAGIC   END AS tip_percentage,
#  MAGIC   
#  MAGIC   -- Analysis flags
#  MAGIC   CASE WHEN t.tip_amount > 0 THEN TRUE ELSE FALSE END AS has_tip,
#  MAGIC   CASE WHEN t.trip_distance_miles > 10 THEN TRUE ELSE FALSE END AS is_long_trip,
#  MAGIC   CASE WHEN t.trip_distance_miles < 1 THEN TRUE ELSE FALSE END AS is_short_trip,
#  MAGIC   r.is_airport_trip,
#  MAGIC   
#  MAGIC   -- DQ score
#  MAGIC   CASE 
#  MAGIC     WHEN t.dq_checks_passed + t.dq_checks_failed > 0 
#  MAGIC     THEN ROUND((t.dq_checks_passed * 100.0) / (t.dq_checks_passed + t.dq_checks_failed), 2)
#  MAGIC     ELSE 100.0
#  MAGIC   END AS dq_score,
#  MAGIC   
#  MAGIC   -- Partitioning columns
#  MAGIC   YEAR(t.pickup_datetime) AS year,
#  MAGIC   MONTH(t.pickup_datetime) AS month,
#  MAGIC   
#  MAGIC   -- Audit
#  MAGIC   t.trip_id AS _source_trip_id,
#  MAGIC   CURRENT_TIMESTAMP() AS _inserted_timestamp,
#  MAGIC   CAST(NULL AS TIMESTAMP) AS _updated_timestamp
#  MAGIC   
#  MAGIC FROM silver.trips_cleaned t
#  MAGIC LEFT JOIN dim_date d 
#  MAGIC   ON t.pickup_date = d.full_date
#  MAGIC LEFT JOIN dim_location pl 
#  MAGIC   ON t.pickup_location_id = pl.zone_id
#  MAGIC LEFT JOIN dim_location dl 
#  MAGIC   ON t.dropoff_location_id = dl.zone_id
#  MAGIC LEFT JOIN dim_payment p 
#  MAGIC   ON t.payment_type_id = p.payment_type_id
#  MAGIC LEFT JOIN dim_rate r 
#  MAGIC   ON t.rate_code_id = r.rate_code_id
#  MAGIC LEFT JOIN dim_trip_type tt 
#  MAGIC   ON t.trip_type_id = tt.trip_type_id
#  MAGIC WHERE t.dq_status = 'VALID';  -- Only valid records

# COMMAND ----------

print(f"✅ fact_trips created: {spark.table('fact_trips').count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2 Incremental MERGE (for daily updates)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Example incremental MERGE (run daily for new data)
# MAGIC -- MERGE INTO fact_trips AS target
# MAGIC -- USING (
# MAGIC --   SELECT ... FROM silver.trips_cleaned t
# MAGIC --   WHERE t.pickup_date >= CURRENT_DATE - INTERVAL 7 DAYS
# MAGIC --   ... (same joins as above)
# MAGIC -- ) AS source
# MAGIC -- ON target.trip_key = source.trip_key
# MAGIC -- WHEN MATCHED THEN UPDATE SET *
# MAGIC -- WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Build Aggregated Fact (for Performance)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE fact_trips_daily_summary
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (date_key)
# MAGIC AS
# MAGIC SELECT
#  MAGIC   date_key,
#  MAGIC   pickup_location_key,
#  MAGIC   payment_key,
#  MAGIC   pickup_hour,
#  MAGIC   
#  MAGIC   -- Aggregated measures
#  MAGIC   COUNT(*) AS total_trips,
#  MAGIC   SUM(passenger_count) AS total_passengers,
#  MAGIC   SUM(trip_distance_miles) AS total_distance_miles,
#  MAGIC   SUM(total_amount) AS total_revenue,
#  MAGIC   SUM(tip_amount) AS total_tips,
#  MAGIC   AVG(trip_duration_minutes) AS avg_trip_duration,
#  MAGIC   AVG(total_amount) AS avg_revenue_per_trip,
#  MAGIC   AVG(trip_distance_miles) AS avg_distance,
#  MAGIC   
#  MAGIC   CURRENT_TIMESTAMP() AS _summarized_timestamp
#  MAGIC   
#  MAGIC FROM fact_trips
#  MAGIC GROUP BY date_key, pickup_location_key, payment_key, pickup_hour;

# COMMAND ----------

print(f"✅ fact_trips_daily_summary created: {spark.table('fact_trips_daily_summary').count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Optimize Tables (Z-ORDER)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Optimize fact_trips for query performance
# MAGIC OPTIMIZE fact_trips
# MAGIC ZORDER BY (date_key, pickup_location_key, payment_key);

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Optimize aggregated fact
# MAGIC OPTIMIZE fact_trips_daily_summary
# MAGIC ZORDER BY (date_key, pickup_location_key);

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Validation & DQ Checks

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validation: Row counts
# MAGIC SELECT 'Row Count Comparison' as check,
# MAGIC   (SELECT COUNT(*) FROM silver.trips_cleaned WHERE dq_status = 'VALID') AS silver_valid,
# MAGIC   (SELECT COUNT(*) FROM fact_trips) AS gold_fact,
# MAGIC   CASE 
# MAGIC     WHEN (SELECT COUNT(*) FROM silver.trips_cleaned WHERE dq_status = 'VALID') = (SELECT COUNT(*) FROM fact_trips)
# MAGIC     THEN '✅ PASS' 
# MAGIC     ELSE '❌ FAIL' 
# MAGIC   END AS status;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validation: Revenue reconciliation
# MAGIC SELECT 'Revenue Reconciliation' as check,
# MAGIC   ROUND((SELECT SUM(CAST(total_amount AS DECIMAL(18,2))) FROM bronze.trips_raw), 2) AS bronze_total,
# MAGIC   ROUND((SELECT SUM(total_amount) FROM silver.trips_cleaned), 2) AS silver_total,
# MAGIC   ROUND((SELECT SUM(total_amount) FROM fact_trips), 2) AS gold_total,
# MAGIC   CASE 
# MAGIC     WHEN ABS(
# MAGIC       (SELECT SUM(CAST(total_amount AS DECIMAL(18,2))) FROM bronze.trips_raw) - 
# MAGIC       (SELECT SUM(total_amount) FROM fact_trips)
# MAGIC     ) <= 1.00  -- Allow $1 tolerance due to rounding
# MAGIC     THEN '✅ PASS' 
# MAGIC     ELSE '❌ FAIL' 
# MAGIC   END AS status;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validation: FK integrity
# MAGIC SELECT 'FK Integrity Check' as check,
# MAGIC   COUNT(*) AS rows_with_null_fk
# MAGIC FROM fact_trips
# MAGIC WHERE date_key IS NULL 
# MAGIC   OR pickup_location_key IS NULL 
# MAGIC   OR dropoff_location_key IS NULL
# MAGIC   OR payment_key IS NULL
# MAGIC   OR rate_key IS NULL
# MAGIC   OR trip_type_key IS NULL;
# MAGIC   
# MAGIC -- Should be 0

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Summary statistics
# MAGIC SELECT 
# MAGIC   '=== GOLD LAYER BUILD COMPLETE ===' AS summary,
# MAGIC   (SELECT COUNT(*) FROM dim_date) AS dim_date_rows,
# MAGIC   (SELECT COUNT(*) FROM dim_location) AS dim_location_rows,
# MAGIC   (SELECT COUNT(*) FROM dim_payment) AS dim_payment_rows,
# MAGIC   (SELECT COUNT(*) FROM dim_rate) AS dim_rate_rows,
# MAGIC   (SELECT COUNT(*) FROM dim_trip_type) AS dim_trip_type_rows,
# MAGIC   (SELECT COUNT(*) FROM fact_trips) AS fact_trips_rows,
# MAGIC   (SELECT COUNT(*) FROM fact_trips_daily_summary) AS fact_summary_rows;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execution Notes
# MAGIC
# MAGIC ### How to Run
# MAGIC
# MAGIC 1. **As Databricks Job:**
# MAGIC    - Create job: `nyc_taxi_gold_build`
# MAGIC    - Type: Notebook
# MAGIC    - Cluster: Job cluster (Standard_DS3_v2, 2 workers)
# MAGIC    - Schedule: Daily at 5:30 AM (after Silver completes)
# MAGIC
# MAGIC 2. **Manual Execution:**
# MAGIC    - Run all cells in sequence
# MAGIC    - Monitor for DQ validation failures
# MAGIC    - Check row counts and reconciliation
# MAGIC
# MAGIC ### Expected Runtime
# MAGIC
# MAGIC - **Initial load:** 5-7 minutes (238K rows)
# MAGIC - **Incremental (daily):** 3-5 minutes
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC 1. Verify all tables created successfully
# MAGIC 2. Run unit tests (01-unit-tests.sql)
# MAGIC 3. Configure Power BI connection
# MAGIC 4. Set up monitoring dashboards
# MAGIC
# MAGIC ## END OF GOLD LAYER BUILD
