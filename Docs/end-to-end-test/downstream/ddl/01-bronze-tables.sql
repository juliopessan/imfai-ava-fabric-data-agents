-- ========================================
-- DDL Script: BRONZE LAYER TABLES
-- ========================================
-- Project: NYC Green Taxi Analytics
-- Platform: Azure Databricks (Unity Catalog)
-- Layer: Bronze (Raw Data Ingestion)
-- Version: 1.0
-- Created: 2026-02-05
-- Author: Diego (DataEngineerExec)
-- ========================================

-- Bronze layer contains raw data exactly as received from sources
-- All columns as STRING for schema flexibility
-- Includes audit columns for lineage tracking

USE CATALOG nyc_taxi;
CREATE SCHEMA IF NOT EXISTS bronze
  COMMENT 'Bronze layer - Raw data ingestion with no transformations';

-- ========================================
-- TABLE: bronze.trips_raw
-- ========================================
-- Source: green_tripdata_*.csv files
-- Grain: One row per trip (raw, may contain duplicates)
-- Load: Streaming (Delta Live Tables)
-- Partitioning: BY month (STRING format YYYY-MM)
-- ========================================

CREATE TABLE IF NOT EXISTS bronze.trips_raw (
  -- Natural Keys
  VendorID STRING COMMENT 'Vendor identifier (1=Creative Mobile, 2=VeriFone)',
  
  -- Temporal Fields
  lpep_pickup_datetime STRING COMMENT 'Pickup datetime (raw string from CSV)',
  lpep_dropoff_datetime STRING COMMENT 'Dropoff datetime (raw string from CSV)',
  
  -- Location Fields
  PULocationID STRING COMMENT 'Pickup location ID (TLC Taxi Zone)',
  DOLocationID STRING COMMENT 'Dropoff location ID (TLC Taxi Zone)',
  
  -- Trip Details
  passenger_count STRING COMMENT 'Number of passengers',
  trip_distance STRING COMMENT 'Trip distance in miles',
  
  -- Payment Fields
  RatecodeID STRING COMMENT 'Rate code at end of trip',
  store_and_fwd_flag STRING COMMENT 'Y=trip held in memory, N=sent immediately',
  payment_type STRING COMMENT 'Payment method code',
  
  -- Financial Fields
  fare_amount STRING COMMENT 'Base fare amount',
  extra STRING COMMENT 'Extra charges (rush hour, overnight)',
  mta_tax STRING COMMENT 'MTA tax',
  tip_amount STRING COMMENT 'Tip amount (card only)',
  tolls_amount STRING COMMENT 'Total tolls paid',
  improvement_surcharge STRING COMMENT 'Improvement surcharge',
  total_amount STRING COMMENT 'Total amount charged',
  
  -- Trip Type
  trip_type STRING COMMENT '1=Street-hail, 2=Dispatch',
  
  -- Congestion Surcharge
  congestion_surcharge STRING COMMENT 'Congestion surcharge amount',
  
  -- Audit Columns
  _ingestion_timestamp TIMESTAMP COMMENT 'Databricks ingestion timestamp',
  _source_file STRING COMMENT 'Source CSV file path',
  _load_date DATE COMMENT 'Date of data load',
  
  -- Partitioning Column
  month STRING COMMENT 'Partition column (YYYY-MM format)'
)
USING DELTA
PARTITIONED BY (month)
LOCATION 'abfss://bronze@nycta

xistorage.dfs.core.windows.net/trips_raw'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true',
  'quality.expectationName' = 'bronze_trips_raw',
  'layer' = 'bronze',
  'source' = 'green_tripdata_*.csv',
  'owner' = 'data-engineering-team'
)
COMMENT 'Raw green taxi trip data - no transformations, all VARCHAR';

-- ========================================
-- TABLE: bronze.payment_types_raw
-- ========================================
-- Source: payment_type_array.json
-- Grain: One row per payment type code
-- Load: Batch (Manual or scripted)
-- ========================================

CREATE TABLE IF NOT EXISTS bronze.payment_types_raw (
  payment_type_id STRING COMMENT 'Payment type code (raw from JSON)',
  payment_type_desc STRING COMMENT 'Payment type description',
  
  -- Audit Columns
  _ingestion_timestamp TIMESTAMP COMMENT 'Databricks ingestion timestamp',
  _source_file STRING COMMENT 'Source JSON file path',
  _load_date DATE COMMENT 'Date of data load'
)
USING DELTA
LOCATION 'abfss://bronze@nyctaxistorage.dfs.core.windows.net/payment_types_raw'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'bronze',
  'source' = 'payment_type_array.json',
  'owner' = 'data-engineering-team'
)
COMMENT 'Raw payment type reference data from JSON';

-- ========================================
-- TABLE: bronze.rate_codes_raw
-- ========================================
-- Source: rate_code.json
-- Grain: One row per rate code
-- Load: Batch (Manual or scripted)
-- ========================================

CREATE TABLE IF NOT EXISTS bronze.rate_codes_raw (
  rate_code_id STRING COMMENT 'Rate code ID (raw from JSON)',
  rate_code_desc STRING COMMENT 'Rate code description',
  
  -- Audit Columns
  _ingestion_timestamp TIMESTAMP COMMENT 'Databricks ingestion timestamp',
  _source_file STRING COMMENT 'Source JSON file path',
  _load_date DATE COMMENT 'Date of data load'
)
USING DELTA
LOCATION 'abfss://bronze@nyctaxistorage.dfs.core.windows.net/rate_codes_raw'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'bronze',
  'source' = 'rate_code.json',
  'owner' = 'data-engineering-team'
)
COMMENT 'Raw rate code reference data from JSON';

-- ========================================
-- TABLE: bronze.trip_types_raw
-- ========================================
-- Source: trip_type.tsv
-- Grain: One row per trip type
-- Load: Batch (Manual or scripted)
-- ========================================

CREATE TABLE IF NOT EXISTS bronze.trip_types_raw (
  trip_type_id STRING COMMENT 'Trip type code (raw from TSV)',
  trip_type_desc STRING COMMENT 'Trip type description',
  
  -- Audit Columns
  _ingestion_timestamp TIMESTAMP COMMENT 'Databricks ingestion timestamp',
  _source_file STRING COMMENT 'Source TSV file path',
  _load_date DATE COMMENT 'Date of data load'
)
USING DELTA
LOCATION 'abfss://bronze@nyctaxistorage.dfs.core.windows.net/trip_types_raw'
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'layer' = 'bronze',
  'source' = 'trip_type.tsv',
  'owner' = 'data-engineering-team'
)
COMMENT 'Raw trip type reference data from TSV';

-- ========================================
-- GRANTS & PERMISSIONS
-- ========================================

-- Bronze layer: Read access for Silver transformations
GRANT SELECT ON SCHEMA bronze TO `data-engineers`;
GRANT MODIFY ON SCHEMA bronze TO `data-pipeline-service-principal`;

-- ========================================
-- METADATA & TAGGING
-- ========================================

ALTER TABLE bronze.trips_raw SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE bronze.payment_types_raw SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE bronze.rate_codes_raw SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');
ALTER TABLE bronze.trip_types_raw SET TAGS ('PII' = 'NO', 'Sensitivity' = 'PUBLIC');

-- ========================================
-- VALIDATION QUERIES
-- ========================================

-- Check table creation
SHOW TABLES IN bronze;

-- Sample data check
SELECT * FROM bronze.trips_raw LIMIT 10;
SELECT * FROM bronze.payment_types_raw;
SELECT * FROM bronze.rate_codes_raw;
SELECT * FROM bronze.trip_types_raw;

-- ========================================
-- END OF BRONZE LAYER DDL
-- ========================================
