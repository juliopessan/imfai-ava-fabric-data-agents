-- ========================================
-- DDL Script: GOLD LAYER TABLES
-- ========================================
-- Project: NYC Green Taxi Analytics
-- Platform: Azure Databricks (Unity Catalog)
-- Layer: Gold (Business-Ready Star Schema)
-- Version: 1.0
-- Created: 2026-02-05
-- Author: Diego (DataEngineerExec)
-- ========================================

-- Gold layer contains business-ready dimensional model
-- Star Schema (Kimball methodology)
-- Optimized for analytics and BI consumption

USE CATALOG nyc_taxi;
CREATE SCHEMA IF NOT EXISTS gold
  COMMENT 'Gold layer - Business-ready dimensional model (Star Schema)';

-- ========================================
-- DIMENSION: dim_date
-- ========================================
-- Type: Generated dimension (calendar table)
-- Grain: One row per day
-- Range: 2021-01-01 to 2025-12-31
-- SCD: Type 0 (static)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.dim_date (
  -- Surrogate Key
  date_key INT NOT NULL COMMENT 'Surrogate key (YYYYMMDD format)',
  
  -- Natural Key
  full_date DATE NOT NULL COMMENT 'Full date (PK)',
  
  -- Year Attributes
  year INT NOT NULL COMMENT 'Year (YYYY)',
  year_name STRING COMMENT 'Year name (e.g., "2021")',
  
  -- Quarter Attributes
  quarter INT NOT NULL COMMENT 'Quarter (1-4)',
  quarter_name STRING COMMENT 'Quarter name (e.g., "Q2 2021")',
  
  -- Month Attributes
  month INT NOT NULL COMMENT 'Month (1-12)',
  month_name STRING COMMENT 'Month name (e.g., "April")',
  month_abbr STRING COMMENT 'Month abbreviation (e.g., "Apr")',
  year_month STRING COMMENT 'Year-Month (e.g., "2021-04")',
  
  -- Week Attributes
  week_of_year INT COMMENT 'Week of year (1-53)',
  week_of_month INT COMMENT 'Week of month (1-6)',
  
  -- Day Attributes
  day_of_month INT NOT NULL COMMENT 'Day of month (1-31)',
  day_of_year INT COMMENT 'Day of year (1-366)',
  day_of_week INT COMMENT 'Day of week (1=Sunday, 7=Saturday)',
  day_name STRING COMMENT 'Day name (e.g., "Monday")',
  day_abbr STRING COMMENT 'Day abbreviation (e.g., "Mon")',
  
  -- Business Day Flags
  is_weekend BOOLEAN COMMENT 'True if Saturday or Sunday',
  is_weekday BOOLEAN COMMENT 'True if Monday-Friday',
  is_holiday BOOLEAN COMMENT 'True if US Federal holiday',
  holiday_name STRING COMMENT 'Holiday name (if applicable)',
  
  -- Fiscal Calendar (if needed)
  fiscal_year INT COMMENT 'Fiscal year',
  fiscal_quarter INT COMMENT 'Fiscal quarter',
  fiscal_month INT COMMENT 'Fiscal month',
  
  -- Audit
  _created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
USING DELTA
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/dim_date'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'false',
  'layer' = 'gold',
  'dimension_type' = 'conformed',
  'scd_type' = 'type_0'
)
COMMENT 'Date dimension (calendar table) for time intelligence';

-- ========================================
-- DIMENSION: dim_location
-- ========================================
-- Type: Generated from NYC Taxi Zone Lookup
-- Grain: One row per location (taxi zone)
-- SCD: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.dim_location (
  -- Surrogate Key
  location_key INT NOT NULL COMMENT 'Surrogate key (auto-increment)',
  
  -- Natural Key
  zone_id INT NOT NULL COMMENT 'TLC Taxi Zone ID (PK from source)',
  
  -- Location Attributes
  zone_name STRING COMMENT 'Taxi zone name (e.g., "East Harlem North")',
  borough STRING COMMENT 'Borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island, EWR)',
  service_zone STRING COMMENT 'Service zone (Boro Zone, Yellow Zone, Airports, EWR)',
  
  -- Derived Attributes
  is_airport BOOLEAN COMMENT 'True if airport zone (JFK, LGA, EWR)',
  is_manhattan BOOLEAN COMMENT 'True if Manhattan borough',
  
  -- Geospatial (Optional - for future)
  latitude DECIMAL(10,6) COMMENT 'Latitude (centroid)',
  longitude DECIMAL(10,6) COMMENT 'Longitude (centroid)',
  
  -- SCD Type 1 Audit
  _created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_timestamp TIMESTAMP,
  _updated_by STRING
)
USING DELTA
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/dim_location'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'gold',
  'dimension_type' = 'conformed',
  'scd_type' = 'type_1'
)
COMMENT 'Location dimension (NYC Taxi Zones)';

-- ========================================
-- DIMENSION: dim_payment
-- ========================================
-- Type: Derived from silver.payment_types
-- Grain: One row per payment type
-- SCD: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.dim_payment (
  -- Surrogate Key
  payment_key INT NOT NULL COMMENT 'Surrogate key (auto-increment)',
  
  -- Natural Key
  payment_type_id INT NOT NULL COMMENT 'Payment type code (PK from source)',
  
  -- Payment Attributes
  payment_type_desc STRING NOT NULL COMMENT 'Payment description',
  is_card_payment BOOLEAN COMMENT 'True if card payment',
  is_cash_payment BOOLEAN COMMENT 'True if cash payment',
  records_tip BOOLEAN COMMENT 'True if payment method records tips',
  
  -- SCD Type 1 Audit
  is_active BOOLEAN DEFAULT TRUE,
  _created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_timestamp TIMESTAMP,
  _updated_by STRING
)
USING DELTA
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/dim_payment'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'gold',
  'dimension_type' = 'dimension',
  'scd_type' = 'type_1'
)
COMMENT 'Payment type dimension';

-- ========================================
-- DIMENSION: dim_rate
-- ========================================
-- Type: Derived from silver.rate_codes
-- Grain: One row per rate code
-- SCD: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.dim_rate (
  -- Surrogate Key
  rate_key INT NOT NULL COMMENT 'Surrogate key (auto-increment)',
  
  -- Natural Key
  rate_code_id INT NOT NULL COMMENT 'Rate code ID (PK from source)',
  
  -- Rate Attributes
  rate_code_desc STRING NOT NULL COMMENT 'Rate code description',
  is_airport_trip BOOLEAN COMMENT 'True if airport-related',
  is_negotiated BOOLEAN COMMENT 'True if negotiated fare',
  is_standard BOOLEAN COMMENT 'True if standard rate',
  
  -- SCD Type 1 Audit
  is_active BOOLEAN DEFAULT TRUE,
  _created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_timestamp TIMESTAMP,
  _updated_by STRING
)
USING DELTA
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/dim_rate'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'gold',
  'dimension_type' = 'dimension',
  'scd_type' = 'type_1'
)
COMMENT 'Rate code dimension';

-- ========================================
-- DIMENSION: dim_trip_type
-- ========================================
-- Type: Derived from silver.trip_types
-- Grain: One row per trip type
-- SCD: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.dim_trip_type (
  -- Surrogate Key
  trip_type_key INT NOT NULL COMMENT 'Surrogate key (auto-increment)',
  
  -- Natural Key
  trip_type_id INT NOT NULL COMMENT 'Trip type code (PK from source)',
  
  -- Trip Type Attributes
  trip_type_desc STRING NOT NULL COMMENT 'Trip type description',
  is_dispatch BOOLEAN COMMENT 'True if dispatch trip',
  is_street_hail BOOLEAN COMMENT 'True if street-hail trip',
  
  -- SCD Type 1 Audit
  is_active BOOLEAN DEFAULT TRUE,
  _created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_timestamp TIMESTAMP,
  _updated_by STRING
)
USING DELTA
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/dim_trip_type'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'gold',
  'dimension_type' = 'dimension',
  'scd_type' = 'type_1'
)
COMMENT 'Trip type dimension';

-- ========================================
-- FACT TABLE: fact_trips
-- ========================================
-- Type: Transaction Fact Table
-- Grain: One row per trip
-- Partitioning: BY year, month
-- Refresh: Daily incremental (MERGE)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.fact_trips (
  -- Surrogate Key
  trip_key BIGINT NOT NULL COMMENT 'Surrogate key (fact table PK)',
  
  -- Dimension Foreign Keys
  date_key INT NOT NULL COMMENT 'FK to dim_date (pickup date)',
  pickup_location_key INT COMMENT 'FK to dim_location (pickup)',
  dropoff_location_key INT COMMENT 'FK to dim_location (dropoff)',
  payment_key INT COMMENT 'FK to dim_payment',
  rate_key INT COMMENT 'FK to dim_rate',
  trip_type_key INT COMMENT 'FK to dim_trip_type',
  
  -- Degenerate Dimensions (from source)
  vendor_id INT COMMENT 'Vendor ID (degenerate dim)',
  store_and_fwd_flag STRING COMMENT 'Store and forward flag',
  
  -- Temporal Measures
  pickup_datetime TIMESTAMP NOT NULL COMMENT 'Pickup datetime',
  dropoff_datetime TIMESTAMP NOT NULL COMMENT 'Dropoff datetime',
  trip_duration_minutes INT COMMENT 'Trip duration (minutes)',
  pickup_hour INT COMMENT 'Pickup hour (0-23) for analysis',
  pickup_day_of_week INT COMMENT 'Pickup day of week',
  
  -- Distance Measures
  trip_distance_miles DECIMAL(8,2) COMMENT 'Trip distance (miles)',
  
  -- Passenger Measures
  passenger_count INT COMMENT 'Number of passengers',
  
  -- Financial Measures (Additive)
  fare_amount DECIMAL(10,2) COMMENT 'Base fare',
  extra DECIMAL(10,2) COMMENT 'Extra charges',
  mta_tax DECIMAL(10,2) COMMENT 'MTA tax',
  tip_amount DECIMAL(10,2) COMMENT 'Tip amount',
  tolls_amount DECIMAL(10,2) COMMENT 'Tolls',
  improvement_surcharge DECIMAL(10,2) COMMENT 'Improvement surcharge',
  congestion_surcharge DECIMAL(10,2) COMMENT 'Congestion surcharge',
  total_amount DECIMAL(10,2) NOT NULL COMMENT 'Total amount (must be >= 0)',
  
  -- Derived Metrics (Semi-Additive/Non-Additive)
  revenue_per_mile DECIMAL(10,2) COMMENT 'Revenue per mile',
  revenue_per_minute DECIMAL(10,2) COMMENT 'Revenue per minute',
  avg_speed_mph DECIMAL(8,2) COMMENT 'Average speed (mph)',
  tip_percentage DECIMAL(5,2) COMMENT 'Tip as % of fare',
  
  -- Flags for Analysis
  has_tip BOOLEAN COMMENT 'True if tip > 0',
  is_long_trip BOOLEAN COMMENT 'True if distance > 10 miles',
  is_short_trip BOOLEAN COMMENT 'True if distance < 1 mile',
  is_airport_trip BOOLEAN COMMENT 'True if airport rate code',
  
  -- Data Quality Metrics
  dq_score DECIMAL(5,2) COMMENT 'DQ score (0-100)',
  
  -- Partitioning Columns
  year INT NOT NULL COMMENT 'Year (for partitioning)',
  month INT NOT NULL COMMENT 'Month (for partitioning)',
  
  -- Audit
  _source_trip_id BIGINT COMMENT 'Original trip_id from silver',
  _inserted_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_timestamp TIMESTAMP
)
USING DELTA
PARTITIONED BY (year, month)
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/fact_trips'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true',
  'delta.dataSkippingNumIndexedCols' = '10',
  'layer' = 'gold',
  'fact_type' = 'transaction',
  'grain' = 'one_row_per_trip',
  'refresh_pattern' = 'daily_incremental'
)
COMMENT 'Trip fact table - transaction grain, one row per trip';

-- ========================================
-- AGGREGATED FACT (Optional for Performance)
-- ========================================

CREATE TABLE IF NOT EXISTS gold.fact_trips_daily_summary (
  -- Dimension Keys
  date_key INT NOT NULL,
  pickup_location_key INT,
  payment_key INT,
  hour_of_day INT,
  
  -- Aggregated Measures
  total_trips INT COMMENT 'COUNT(*)',
  total_passengers INT COMMENT 'SUM(passenger_count)',
  total_distance_miles DECIMAL(12,2) COMMENT 'SUM(trip_distance_miles)',
  total_revenue DECIMAL(12,2) COMMENT 'SUM(total_amount)',
  total_tips DECIMAL(12,2) COMMENT 'SUM(tip_amount)',
  avg_trip_duration INT COMMENT 'AVG(trip_duration_minutes)',
  avg_revenue_per_trip DECIMAL(10,2) COMMENT 'AVG(total_amount)',
  avg_distance DECIMAL(8,2) COMMENT 'AVG(trip_distance_miles)',
  
  -- Update tracking
  _summarized_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
USING DELTA
PARTITIONED BY (date_key)
LOCATION 'abfss://gold@nyctaxistorage.dfs.core.windows.net/fact_trips_daily_summary'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'false',
  'layer' = 'gold',
  'fact_type' = 'aggregate',
  'grain' = 'daily_summary'
)
COMMENT 'Daily aggregated trip metrics for fast querying';

-- ========================================
-- CONSTRAINTS & INDEXES
-- ========================================

-- Note: Delta Lake doesn't support traditional PK/FK constraints
-- Use Delta Lake constraints for NOT NULL and CHECK constraints

-- ALTER TABLE gold.fact_trips ADD CONSTRAINT chk_total_amount CHECK (total_amount >= 0);
-- ALTER TABLE gold.fact_trips ADD CONSTRAINT chk_distance CHECK (trip_distance_miles >= 0);

-- ========================================
-- Z-ORDERING (for query performance)
-- ========================================

-- Optimize fact table with Z-ORDER on commonly filtered columns
-- OPTIMIZE gold.fact_trips ZORDER BY (date_key, pickup_location_key, payment_key);

-- ========================================
-- GRANTS & PERMISSIONS
-- ========================================

GRANT SELECT ON SCHEMA gold TO `data-engineers`;
GRANT SELECT ON SCHEMA gold TO `data-analysts`;
GRANT SELECT ON SCHEMA gold TO `bi-developers`;
GRANT MODIFY ON SCHEMA gold TO `data-pipeline-service-principal`;

-- ========================================
-- METADATA & TAGGING
-- ========================================

ALTER TABLE gold.fact_trips SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC', 'BusinessReady' = 'YES');
ALTER TABLE gold.dim_date SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC', 'ConformedDim' = 'YES');
ALTER TABLE gold.dim_location SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE gold.dim_payment SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE gold.dim_rate SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE gold.dim_trip_type SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');

-- ========================================
-- VALIDATION QUERIES
-- ========================================

-- Check table creation
SHOW TABLES IN gold;

-- Sample data check
SELECT * FROM gold.fact_trips LIMIT 10;
SELECT * FROM gold.dim_date LIMIT 10;
SELECT * FROM gold.dim_location LIMIT 10;

-- Row counts
SELECT 'fact_trips' as table_name, COUNT(*) as row_count FROM gold.fact_trips
UNION ALL
SELECT 'dim_date', COUNT(*) FROM gold.dim_date
UNION ALL
SELECT 'dim_location', COUNT(*) FROM gold.dim_location
UNION ALL
SELECT 'dim_payment', COUNT(*) FROM gold.dim_payment
UNION ALL
SELECT 'dim_rate', COUNT(*) FROM gold.dim_rate
UNION ALL
SELECT 'dim_trip_type', COUNT(*) FROM gold.dim_trip_type;

-- ========================================
-- END OF GOLD LAYER DDL
-- ========================================
