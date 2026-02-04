-- ============================================================================
-- 01-LANDING-TABLES.SQL - NYC Green Taxi Landing Layer
-- ============================================================================
-- Purpose: Landing tables with ALL VARCHAR columns (as specified in requirements)
-- Data Sources: CSV files, Parquet files
-- Author: DataFlow Agent
-- Date: November 14, 2025
-- ============================================================================

USE [TEST_PIPELINE];
GO

PRINT '============================================================================';
PRINT 'CREATING LANDING TABLES - NYC GREEN TAXI DATA';
PRINT '============================================================================';
PRINT '';

-- ============================================================================
-- SCHEMAS CREATION
-- ============================================================================
PRINT '--- Creating Schemas ---';

-- Create schemas if they don't exist
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'LND')
    EXEC('CREATE SCHEMA LND');
    PRINT '✅ Schema LND created';

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'LANDING')
    EXEC('CREATE SCHEMA LANDING');
    PRINT '✅ Schema LANDING created';

PRINT '';

-- ============================================================================
-- REQUIREMENT 1a: LANDING.TRIP_DATA_CSV (from CSV files)
-- ============================================================================
PRINT '--- REQUIREMENT 1a: Creating LANDING.TRIP_DATA_CSV ---';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('LANDING.TRIP_DATA_CSV', 'U') IS NOT NULL
    DROP TABLE LANDING.TRIP_DATA_CSV;
    PRINT '🗑️  Dropped existing LANDING.TRIP_DATA_CSV';

CREATE TABLE LANDING.TRIP_DATA_CSV (
    -- All columns as VARCHAR as per requirement 1a
    VendorID                  VARCHAR(50),
    lpep_pickup_datetime      VARCHAR(50),
    lpep_dropoff_datetime     VARCHAR(50),
    store_and_fwd_flag        VARCHAR(50),
    RatecodeID                VARCHAR(50),
    PULocationID              VARCHAR(50),
    DOLocationID              VARCHAR(50),
    passenger_count           VARCHAR(50),
    trip_distance             VARCHAR(50),
    fare_amount               VARCHAR(50),
    extra                     VARCHAR(50),
    mta_tax                   VARCHAR(50),
    tip_amount                VARCHAR(50),
    tolls_amount              VARCHAR(50),
    ehail_fee                 VARCHAR(50),  -- Always empty but keeping per source structure
    improvement_surcharge     VARCHAR(50),
    total_amount              VARCHAR(50),
    payment_type              VARCHAR(50),
    trip_type                 VARCHAR(50),
    congestion_surcharge      VARCHAR(50),
    
    -- Audit and tracking columns
    load_timestamp            DATETIME2 DEFAULT GETDATE(),
    source_file               VARCHAR(500),
    load_batch_id             VARCHAR(50),
    
    -- Primary key for tracking
    landing_id                BIGINT IDENTITY(1,1) PRIMARY KEY
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Landing table for NYC Green Taxi trip data from CSV files. All columns stored as VARCHAR for initial ingestion.',
    @level0type = N'SCHEMA', @level0name = N'LANDING',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_CSV';

PRINT '✅ LANDING.TRIP_DATA_CSV created successfully';
PRINT '   • 20 data columns (all VARCHAR)';
PRINT '   • 3 audit columns';
PRINT '   • Primary key: landing_id';
PRINT '';

-- ============================================================================
-- REQUIREMENT 2a: LANDING.TRIP_DATA_PARQUET (from Parquet files)
-- ============================================================================
PRINT '--- REQUIREMENT 2a: Creating LANDING.TRIP_DATA_PARQUET ---';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('LANDING.TRIP_DATA_PARQUET', 'U') IS NOT NULL
    DROP TABLE LANDING.TRIP_DATA_PARQUET;
    PRINT '🗑️  Dropped existing LANDING.TRIP_DATA_PARQUET';

CREATE TABLE LANDING.TRIP_DATA_PARQUET (
    -- All columns as VARCHAR as per requirement 2a
    VendorID                  VARCHAR(50),
    lpep_pickup_datetime      VARCHAR(50),
    lpep_dropoff_datetime     VARCHAR(50),
    store_and_fwd_flag        VARCHAR(50),
    RatecodeID                VARCHAR(50),
    PULocationID              VARCHAR(50),
    DOLocationID              VARCHAR(50),
    passenger_count           VARCHAR(50),
    trip_distance             VARCHAR(50),
    fare_amount               VARCHAR(50),
    extra                     VARCHAR(50),
    mta_tax                   VARCHAR(50),
    tip_amount                VARCHAR(50),
    tolls_amount              VARCHAR(50),
    ehail_fee                 VARCHAR(50),  -- Always empty but keeping per source structure
    improvement_surcharge     VARCHAR(50),
    total_amount              VARCHAR(50),
    payment_type              VARCHAR(50),
    trip_type                 VARCHAR(50),
    congestion_surcharge      VARCHAR(50),
    
    -- Audit and tracking columns
    load_timestamp            DATETIME2 DEFAULT GETDATE(),
    source_file               VARCHAR(500),
    partition_key             VARCHAR(50),  -- month=04, month=05, etc.
    
    -- Primary key for tracking
    landing_id                BIGINT IDENTITY(1,1) PRIMARY KEY
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Landing table for NYC Green Taxi trip data from Parquet files. All columns stored as VARCHAR for initial ingestion.',
    @level0type = N'SCHEMA', @level0name = N'LANDING',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_PARQUET';

PRINT '✅ LANDING.TRIP_DATA_PARQUET created successfully';
PRINT '   • 20 data columns (all VARCHAR)';
PRINT '   • 3 audit columns';
PRINT '   • Primary key: landing_id';
PRINT '';

-- ============================================================================
-- INDEXES FOR LANDING TABLES (Optimized for ETL Performance)
-- ============================================================================
PRINT '--- Creating Indexes for Landing Tables ---';
PRINT '';

-- Index on load_timestamp for data processing efficiency
CREATE NONCLUSTERED INDEX IX_TRIP_DATA_CSV_load_timestamp 
ON LANDING.TRIP_DATA_CSV (load_timestamp);

CREATE NONCLUSTERED INDEX IX_TRIP_DATA_PARQUET_load_timestamp 
ON LANDING.TRIP_DATA_PARQUET (load_timestamp);

-- Index on source_file for batch tracking
CREATE NONCLUSTERED INDEX IX_TRIP_DATA_CSV_source_file 
ON LANDING.TRIP_DATA_CSV (source_file);

CREATE NONCLUSTERED INDEX IX_TRIP_DATA_PARQUET_source_file 
ON LANDING.TRIP_DATA_PARQUET (source_file);

PRINT '✅ Indexes created for optimized ETL performance';
PRINT '';

-- ============================================================================
-- DATA LINEAGE AND TRACKING
-- ============================================================================
PRINT '--- Creating Data Lineage Table ---';
PRINT '';

-- Drop table if exists
IF OBJECT_ID('LANDING.DATA_LINEAGE', 'U') IS NOT NULL
    DROP TABLE LANDING.DATA_LINEAGE;

CREATE TABLE LANDING.DATA_LINEAGE (
    lineage_id          BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_file         VARCHAR(500) NOT NULL,
    target_table        VARCHAR(100) NOT NULL,
    records_loaded      INT,
    load_timestamp      DATETIME2 DEFAULT GETDATE(),
    load_status         VARCHAR(20) DEFAULT 'SUCCESS',
    error_message       VARCHAR(MAX)
);

PRINT '✅ Data lineage tracking table created';
PRINT '';

-- ============================================================================
-- COMPLETION SUMMARY
-- ============================================================================
PRINT '============================================================================';
PRINT 'LANDING LAYER DEPLOYMENT COMPLETE';
PRINT '============================================================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  ✅ LANDING.TRIP_DATA_CSV (Requirements 1a)';
PRINT '  ✅ LANDING.TRIP_DATA_PARQUET (Requirements 2a)';
PRINT '  ✅ LANDING.DATA_LINEAGE (Tracking)';
PRINT '';
PRINT 'Schema Structure:';
PRINT '  • All data columns stored as VARCHAR (as required)';
PRINT '  • Audit columns for load tracking';
PRINT '  • Indexes for ETL performance';
PRINT '  • Data lineage for monitoring';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Run 02-SILVER-TABLES.SQL (Silver layer with proper data types)';
PRINT '  2. Run 03-GOLD-TABLES.SQL (Gold layer for business consumption)';
PRINT '  3. Run 04-REFERENCE-TABLES.SQL (Reference data)';
PRINT '';
PRINT 'Ready for data ingestion from:';
PRINT '  📁 green_tripdata_2021-04.csv (86,941 records)';
PRINT '  📁 green_tripdata_2021-05.csv (88,180 records)';
PRINT '  📁 green_tripdata_2021-06.csv (86,737 records)';
PRINT '  📁 month=04/*.parquet (TBD records)';
PRINT '  📁 month=05/*.parquet (TBD records)';
PRINT '  📁 month=06/*.parquet (TBD records)';
PRINT '============================================================================';