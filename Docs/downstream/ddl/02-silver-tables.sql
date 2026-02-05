-- ========================================
-- DDL Script: SILVER LAYER TABLES
-- ========================================
-- Project: NYC Green Taxi Analytics
-- Platform: Azure Databricks (Unity Catalog)
-- Layer: Silver (Cleaned & Validated Data)
-- Version: 1.0
-- Created: 2026-02-05
-- Author: Diego (DataEngineerExec)
-- ========================================

-- Silver layer contains typed, validated, quality-checked data
-- Proper data types applied
-- Includes DQ validation flags
-- Business rules validated

USE CATALOG nyc_taxi;
CREATE SCHEMA IF NOT EXISTS silver
  COMMENT 'Silver layer - Cleaned, typed, and validated data';

-- ========================================
-- TABLE: silver.trips_cleaned
-- ========================================
-- Source: bronze.trips_raw (via DLT pipeline)
-- Grain: One row per trip (duplicates removed)
-- Load: Streaming (Delta Live Tables with DQ Expectations)
-- Partitioning: BY pickup_date (DATE)
-- ========================================

CREATE TABLE IF NOT EXISTS silver.trips_cleaned (
  -- Surrogate & Natural Keys
  trip_id BIGINT COMMENT 'Generated unique trip identifier (MD5 hash of natural keys)',
  vendor_id INT NOT NULL COMMENT 'Vendor identifier (1=Creative Mobile, 2=VeriFone)',
  
  -- Temporal Fields (Properly Typed)
  pickup_datetime TIMESTAMP NOT NULL COMMENT 'Pickup datetime (validated)',
  dropoff_datetime TIMESTAMP NOT NULL COMMENT 'Dropoff datetime (validated)',
  pickup_date DATE COMMENT 'Pickup date (derived for partitioning)',
  trip_duration_minutes INT COMMENT 'Trip duration in minutes (calculated)',
  
  -- Location Fields (Typed & FK Validated)
  pickup_location_id INT COMMENT 'Pickup location ID (validated against dim_location)',
  dropoff_location_id INT COMMENT 'Dropoff location ID (validated against dim_location)',
  
  -- Trip Details (Typed & Range Validated)
  passenger_count INT COMMENT 'Number of passengers (1-6 validated)',
  trip_distance_miles DECIMAL(8,2) COMMENT 'Trip distance in miles (>= 0)',
  
  -- Payment & Rate Codes (FK Validated)
  rate_code_id INT COMMENT 'Rate code (validated against dim_rate)',
  store_and_fwd_flag STRING COMMENT 'Y/N flag (validated)',
  payment_type_id INT COMMENT 'Payment method code (validated against dim_payment)',
  trip_type_id INT COMMENT 'Trip type (validated against dim_trip_type)',
  
  -- Financial Fields (Typed & Validated)
  fare_amount DECIMAL(10,2) COMMENT 'Base fare amount (>= 0)',
  extra DECIMAL(10,2) COMMENT 'Extra charges (>= 0)',
  mta_tax DECIMAL(10,2) COMMENT 'MTA tax (>= 0)',
  tip_amount DECIMAL(10,2) COMMENT 'Tip amount (>= 0, card only)',
  tolls_amount DECIMAL(10,2) COMMENT 'Total tolls paid (>= 0)',
  improvement_surcharge DECIMAL(10,2) COMMENT 'Improvement surcharge (>= 0)',
  congestion_surcharge DECIMAL(10,2) COMMENT 'Congestion surcharge (>= 0)',
  total_amount DECIMAL(10,2) NOT NULL COMMENT 'Total amount charged (>= 0)',
  
  -- Derived Business Metrics
  revenue_per_mile DECIMAL(10,2) COMMENT 'Revenue per mile (total_amount / trip_distance)',
  avg_speed_mph DECIMAL(8,2) COMMENT 'Average speed in mph',
  
  -- Data Quality Flags
  dq_status STRING DEFAULT 'VALID' COMMENT 'VALID | INVALID | QUARANTINED',
  dq_failure_reason STRING COMMENT 'Reason for DQ failure (if applicable)',
  dq_checks_passed INT COMMENT 'Number of DQ checks passed',
  dq_checks_failed INT COMMENT 'Number of DQ checks failed',
  
  -- Audit Columns
  _source_table STRING DEFAULT 'bronze.trips_raw' COMMENT 'Source table',
  _ingestion_timestamp TIMESTAMP COMMENT 'Bronze ingestion timestamp',
  _transformation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP() COMMENT 'Silver transformation timestamp',
  _dlt_pipeline_id STRING COMMENT 'DLT pipeline execution ID'
)
USING DELTA
PARTITIONED BY (pickup_date)
LOCATION 'abfss://silver@nyctaxistorage.dfs.core.windows.net/trips_cleaned'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true',
  'delta.deletedFileRetentionDuration' = 'interval 30 days',
  'quality.expectationName' = 'silver_trips_cleaned',
  'layer' = 'silver',
  'source' = 'bronze.trips_raw',
  'owner' = 'data-engineering-team',
  'dq.target_quality_score' = '99.5'
)
COMMENT 'Cleaned and validated trip data with proper types and DQ checks';

-- ========================================
-- TABLE: silver.payment_types
-- ========================================
-- Source: bronze.payment_types_raw
-- Grain: One row per payment type (deduplicated)
-- SCD Type: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS silver.payment_types (
  payment_type_id INT NOT NULL COMMENT 'Payment type code (PK)',
  payment_type_desc STRING NOT NULL COMMENT 'Payment type description',
  is_card_payment BOOLEAN COMMENT 'True if card payment (for tip analysis)',
  is_active BOOLEAN DEFAULT TRUE COMMENT 'Active status',
  
  -- Audit Columns
  _source_table STRING DEFAULT 'bronze.payment_types_raw',
  _transformation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_by STRING DEFAULT CURRENT_USER()
)
USING DELTA
LOCATION 'abfss://silver@nyctaxistorage.dfs.core.windows.net/payment_types'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'silver',
  'source' = 'bronze.payment_types_raw',
  'scd_type' = 'type_1'
)
COMMENT 'Payment type reference data (SCD Type 1)';

-- ========================================
-- TABLE: silver.rate_codes
-- ========================================
-- Source: bronze.rate_codes_raw
-- Grain: One row per rate code (deduplicated)
-- SCD Type: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS silver.rate_codes (
  rate_code_id INT NOT NULL COMMENT 'Rate code ID (PK)',
  rate_code_desc STRING NOT NULL COMMENT 'Rate code description',
  is_airport_trip BOOLEAN COMMENT 'True if airport-related rate code',
  is_active BOOLEAN DEFAULT TRUE COMMENT 'Active status',
  
  -- Audit Columns
  _source_table STRING DEFAULT 'bronze.rate_codes_raw',
  _transformation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_by STRING DEFAULT CURRENT_USER()
)
USING DELTA
LOCATION 'abfss://silver@nyctaxistorage.dfs.core.windows.net/rate_codes'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'silver',
  'source' = 'bronze.rate_codes_raw',
  'scd_type' = 'type_1'
)
COMMENT 'Rate code reference data (SCD Type 1)';

-- ========================================
-- TABLE: silver.trip_types
-- ========================================
-- Source: bronze.trip_types_raw
-- Grain: One row per trip type (deduplicated)
-- SCD Type: Type 1 (overwrite)
-- ========================================

CREATE TABLE IF NOT EXISTS silver.trip_types (
  trip_type_id INT NOT NULL COMMENT 'Trip type code (PK)',
  trip_type_desc STRING NOT NULL COMMENT 'Trip type description',
  is_dispatch BOOLEAN COMMENT 'True if dispatch trip (vs street-hail)',
  is_active BOOLEAN DEFAULT TRUE COMMENT 'Active status',
  
  -- Audit Columns
  _source_table STRING DEFAULT 'bronze.trip_types_raw',
  _transformation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  _updated_by STRING DEFAULT CURRENT_USER()
)
USING DELTA
LOCATION 'abfss://silver@nyctaxistorage.dfs.core.windows.net/trip_types'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'silver',
  'source' = 'bronze.trip_types_raw',
  'scd_type' = 'type_1'
)
COMMENT 'Trip type reference data (SCD Type 1)';

-- ========================================
-- TABLE: silver.dq_quarantine
-- ========================================
-- Purpose: Store records that failed DQ validation
-- Grain: One row per failed record per check
-- ========================================

CREATE TABLE IF NOT EXISTS silver.dq_quarantine (
  quarantine_id BIGINT GENERATED ALWAYS AS IDENTITY COMMENT 'Quarantine record ID',
  source_table STRING COMMENT 'Source table name',
  source_record_id STRING COMMENT 'Source record identifier',
  source_record_json STRING COMMENT 'Full source record as JSON',
  
  -- DQ Failure Details
  dq_rule_id STRING COMMENT 'DQ rule identifier',
  dq_rule_name STRING COMMENT 'DQ rule name',
  dq_expectation STRING COMMENT 'DLT expectation expression',
  dq_failure_reason STRING COMMENT 'Failure reason description',
  dq_failed_column STRING COMMENT 'Column that failed validation',
  dq_failed_value STRING COMMENT 'Value that failed',
  
  -- Processing Info
  can_auto_fix BOOLEAN COMMENT 'True if auto-fixable',
  fix_applied BOOLEAN DEFAULT FALSE COMMENT 'True if fix was applied',
  fix_description STRING COMMENT 'Description of fix applied',
  
  -- Audit
  quarantine_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  resolved_timestamp TIMESTAMP COMMENT 'When issue was resolved',
  resolved_by STRING COMMENT 'User who resolved',
  resolution_action STRING COMMENT 'FIXED | DELETED | IGNORED'
)
USING DELTA
LOCATION 'abfss://silver@nyctaxistorage.dfs.core.windows.net/dq_quarantine'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'silver',
  'purpose' = 'dq_quarantine'
)
COMMENT 'Quarantine table for records failing DQ validation';

-- ========================================
-- CONSTRAINTS
-- ========================================

-- Primary Keys (enforced via DLT expectations)
-- ALTER TABLE silver.trips_cleaned ADD CONSTRAINT pk_trips_cleaned PRIMARY KEY (trip_id); -- Not yet supported in Delta
-- ALTER TABLE silver.payment_types ADD CONSTRAINT pk_payment_types PRIMARY KEY (payment_type_id);
-- ALTER TABLE silver.rate_codes ADD CONSTRAINT pk_rate_codes PRIMARY KEY (rate_code_id);
-- ALTER TABLE silver.trip_types ADD CONSTRAINT pk_trip_types PRIMARY KEY (trip_type_id);

-- ========================================
-- GRANTS & PERMISSIONS
-- ========================================

GRANT SELECT ON SCHEMA silver TO `data-engineers`;
GRANT SELECT ON SCHEMA silver TO `data-analysts`;
GRANT MODIFY ON SCHEMA silver TO `data-pipeline-service-principal`;

-- ========================================
-- METADATA & TAGGING
-- ========================================

ALTER TABLE silver.trips_cleaned SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC', 'QualityChecked' = 'YES');
ALTER TABLE silver.payment_types SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE silver.rate_codes SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE silver.trip_types SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');

-- ========================================
-- VALIDATION QUERIES
-- ========================================

-- Check table creation
SHOW TABLES IN silver;

-- Sample data check
SELECT * FROM silver.trips_cleaned LIMIT 10;
SELECT * FROM silver.payment_types;
SELECT * FROM silver.rate_codes;
SELECT * FROM silver.trip_types;

-- DQ validation check
SELECT dq_status, COUNT(*) 
FROM silver.trips_cleaned 
GROUP BY dq_status;

-- ========================================
-- END OF SILVER LAYER DDL
-- ========================================
