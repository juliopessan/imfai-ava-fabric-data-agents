-- ============================================================================
-- 02-SILVER-TABLES.SQL - NYC Green Taxi Silver Layer
-- ============================================================================
-- Purpose: Silver tables with PROPER DATA TYPES derived from data profiling
-- Data Quality: Validation rules and quality flags included
-- Author: DataFlow Agent
-- Date: November 14, 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

PRINT '============================================================================';
PRINT 'CREATING SILVER TABLES - NYC GREEN TAXI DATA';
PRINT '============================================================================';
PRINT '';

-- ============================================================================
-- SCHEMAS CREATION
-- ============================================================================
PRINT '--- Creating Silver Schema ---';

-- Create schema if doesn't exist
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'SILVER')
    EXEC('CREATE SCHEMA SILVER');
    PRINT '✅ Schema SILVER created';

PRINT '';

-- ============================================================================
-- REQUIREMENT 1b: SILVER.TRIP_DATA_CSV (proper data types from profiling)
-- ============================================================================
PRINT '--- REQUIREMENT 1b: Creating SILVER.TRIP_DATA_CSV ---';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('SILVER.TRIP_DATA_CSV', 'U') IS NOT NULL
    DROP TABLE SILVER.TRIP_DATA_CSV;
    PRINT '🗑️  Dropped existing SILVER.TRIP_DATA_CSV';

CREATE TABLE SILVER.TRIP_DATA_CSV (
    -- Business primary key
    trip_id                   BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Core trip data with proper data types (derived from profiling)
    VendorID                  INT NOT NULL 
        CHECK (VendorID IN (1,2)),  -- CMT or VTS
    
    lpep_pickup_datetime      DATETIME2 NOT NULL,
    lpep_dropoff_datetime     DATETIME2 NOT NULL,
    
    store_and_fwd_flag        CHAR(1) 
        CHECK (store_and_fwd_flag IN ('Y','N')) DEFAULT 'N',
    
    RatecodeID                INT 
        CHECK (RatecodeID BETWEEN 1 AND 6),  -- FK to REF.RATE_CODE
    
    PULocationID              INT 
        CHECK (PULocationID > 0),  -- Pickup location
    
    DOLocationID              INT 
        CHECK (DOLocationID > 0),  -- Dropoff location
    
    passenger_count           INT 
        CHECK (passenger_count BETWEEN 0 AND 10),
    
    trip_distance             DECIMAL(8,2) 
        CHECK (trip_distance >= 0 AND trip_distance <= 500),  -- Max 500 miles
    
    -- Financial data with precision for currency
    fare_amount               DECIMAL(10,2) 
        CHECK (fare_amount >= 0),
    
    extra                     DECIMAL(6,2) DEFAULT 0
        CHECK (extra >= 0),  -- Surcharges
    
    mta_tax                   DECIMAL(4,2) DEFAULT 0
        CHECK (mta_tax >= 0),  -- MTA tax
    
    tip_amount                DECIMAL(10,2) DEFAULT 0
        CHECK (tip_amount >= 0),
    
    tolls_amount              DECIMAL(10,2) DEFAULT 0
        CHECK (tolls_amount >= 0),
    
    -- ehail_fee column DROPPED (always empty in source data)
    
    improvement_surcharge     DECIMAL(4,2) DEFAULT 0
        CHECK (improvement_surcharge >= 0),
    
    total_amount              DECIMAL(12,2) 
        CHECK (total_amount >= 0),
    
    payment_type              INT 
        CHECK (payment_type BETWEEN 1 AND 6),  -- FK to REF.PAYMENT_TYPE
    
    trip_type                 INT 
        CHECK (trip_type IN (1,2)),  -- FK to REF.TRIP_TYPE
    
    congestion_surcharge      DECIMAL(6,2) DEFAULT 0
        CHECK (congestion_surcharge >= 0),
    
    -- Derived columns
    trip_duration_minutes     AS DATEDIFF(MINUTE, lpep_pickup_datetime, lpep_dropoff_datetime),
    trip_month                AS MONTH(lpep_pickup_datetime),
    trip_year                 AS YEAR(lpep_pickup_datetime),
    
    -- Data Quality Framework
    quality_flag              VARCHAR(10) DEFAULT 'VALID' 
        CHECK (quality_flag IN ('VALID', 'INVALID', 'WARNING')),
    
    quality_errors            VARCHAR(MAX),  -- JSON array of validation errors
    quality_score             AS (
        CASE 
            WHEN quality_flag = 'VALID' THEN 100
            WHEN quality_flag = 'WARNING' THEN 75
            ELSE 0
        END
    ),
    
    -- Audit columns
    processed_timestamp       DATETIME2 DEFAULT GETDATE(),
    source_landing_id         BIGINT,  -- FK to LANDING table
    source_file               VARCHAR(500),
    etl_batch_id              VARCHAR(50),
    
    -- Table-level constraint for datetime validation
    CONSTRAINT CHK_TRIP_DATA_CSV_DATETIME 
        CHECK (lpep_dropoff_datetime > lpep_pickup_datetime)
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Silver layer for NYC Green Taxi trip data from CSV files. Contains validated data with proper types and quality flags.',
    @level0type = N'SCHEMA', @level0name = N'SILVER',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_CSV';

PRINT '✅ SILVER.TRIP_DATA_CSV created successfully';
PRINT '   • Proper data types from profiling analysis';
PRINT '   • Data quality constraints and validations';
PRINT '   • Computed columns for analytics';
PRINT '   • Quality framework integrated';
PRINT '';

-- ============================================================================
-- REQUIREMENT 2b: SILVER.TRIP_DATA_PARQUET (same structure as CSV)
-- ============================================================================
PRINT '--- REQUIREMENT 2b: Creating SILVER.TRIP_DATA_PARQUET ---';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('SILVER.TRIP_DATA_PARQUET', 'U') IS NOT NULL
    DROP TABLE SILVER.TRIP_DATA_PARQUET;
    PRINT '🗑️  Dropped existing SILVER.TRIP_DATA_PARQUET';

CREATE TABLE SILVER.TRIP_DATA_PARQUET (
    -- Business primary key
    trip_id                   BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Core trip data with proper data types (same as CSV structure)
    VendorID                  INT NOT NULL 
        CHECK (VendorID IN (1,2)),
    
    lpep_pickup_datetime      DATETIME2 NOT NULL,
    lpep_dropoff_datetime     DATETIME2 NOT NULL,
    
    store_and_fwd_flag        CHAR(1) 
        CHECK (store_and_fwd_flag IN ('Y','N')) DEFAULT 'N',
    
    RatecodeID                INT 
        CHECK (RatecodeID BETWEEN 1 AND 6),
    
    PULocationID              INT 
        CHECK (PULocationID > 0),
    
    DOLocationID              INT 
        CHECK (DOLocationID > 0),
    
    passenger_count           INT 
        CHECK (passenger_count BETWEEN 0 AND 10),
    
    trip_distance             DECIMAL(8,2) 
        CHECK (trip_distance >= 0 AND trip_distance <= 500),
    
    -- Financial data
    fare_amount               DECIMAL(10,2) 
        CHECK (fare_amount >= 0),
    
    extra                     DECIMAL(6,2) DEFAULT 0
        CHECK (extra >= 0),
    
    mta_tax                   DECIMAL(4,2) DEFAULT 0
        CHECK (mta_tax >= 0),
    
    tip_amount                DECIMAL(10,2) DEFAULT 0
        CHECK (tip_amount >= 0),
    
    tolls_amount              DECIMAL(10,2) DEFAULT 0
        CHECK (tolls_amount >= 0),
    
    improvement_surcharge     DECIMAL(4,2) DEFAULT 0
        CHECK (improvement_surcharge >= 0),
    
    total_amount              DECIMAL(12,2) 
        CHECK (total_amount >= 0),
    
    payment_type              INT 
        CHECK (payment_type BETWEEN 1 AND 6),
    
    trip_type                 INT 
        CHECK (trip_type IN (1,2)),
    
    congestion_surcharge      DECIMAL(6,2) DEFAULT 0
        CHECK (congestion_surcharge >= 0),
    
    -- Derived columns
    trip_duration_minutes     AS DATEDIFF(MINUTE, lpep_pickup_datetime, lpep_dropoff_datetime),
    trip_month                AS MONTH(lpep_pickup_datetime),
    trip_year                 AS YEAR(lpep_pickup_datetime),
    
    -- Data Quality Framework
    quality_flag              VARCHAR(10) DEFAULT 'VALID' 
        CHECK (quality_flag IN ('VALID', 'INVALID', 'WARNING')),
    
    quality_errors            VARCHAR(MAX),
    quality_score             AS (
        CASE 
            WHEN quality_flag = 'VALID' THEN 100
            WHEN quality_flag = 'WARNING' THEN 75
            ELSE 0
        END
    ),
    
    -- Audit columns
    processed_timestamp       DATETIME2 DEFAULT GETDATE(),
    source_landing_id         BIGINT,
    source_file               VARCHAR(500),
    partition_key             VARCHAR(50),  -- month=04, month=05, etc.
    etl_batch_id              VARCHAR(50),
    
    -- Table-level constraint for datetime validation
    CONSTRAINT CHK_TRIP_DATA_PARQUET_DATETIME 
        CHECK (lpep_dropoff_datetime > lpep_pickup_datetime)
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Silver layer for NYC Green Taxi trip data from Parquet files. Contains validated data with proper types and quality flags.',
    @level0type = N'SCHEMA', @level0name = N'SILVER',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_PARQUET';

PRINT '✅ SILVER.TRIP_DATA_PARQUET created successfully';
PRINT '   • Same structure as TRIP_DATA_CSV';
PRINT '   • Optimized for Parquet source format';
PRINT '   • Partition-aware processing';
PRINT '';

-- ============================================================================
-- REJECT TABLES FOR DATA QUALITY
-- ============================================================================
PRINT '--- Creating Reject Tables ---';
PRINT '';

-- Reject table for CSV data
IF OBJECT_ID('SILVER.TRIP_DATA_CSV_REJECTS', 'U') IS NOT NULL
    DROP TABLE SILVER.TRIP_DATA_CSV_REJECTS;

CREATE TABLE SILVER.TRIP_DATA_CSV_REJECTS (
    reject_id                 BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Original data (all VARCHAR to capture any invalid values)
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
    ehail_fee                 VARCHAR(50),
    improvement_surcharge     VARCHAR(50),
    total_amount              VARCHAR(50),
    payment_type              VARCHAR(50),
    trip_type                 VARCHAR(50),
    congestion_surcharge      VARCHAR(50),
    
    -- Rejection details
    reject_reason             VARCHAR(MAX),  -- Detailed error messages
    reject_timestamp          DATETIME2 DEFAULT GETDATE(),
    source_landing_id         BIGINT,
    source_file               VARCHAR(500)
);

-- Reject table for Parquet data
IF OBJECT_ID('SILVER.TRIP_DATA_PARQUET_REJECTS', 'U') IS NOT NULL
    DROP TABLE SILVER.TRIP_DATA_PARQUET_REJECTS;

CREATE TABLE SILVER.TRIP_DATA_PARQUET_REJECTS (
    reject_id                 BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Original data (same structure as CSV rejects)
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
    ehail_fee                 VARCHAR(50),
    improvement_surcharge     VARCHAR(50),
    total_amount              VARCHAR(50),
    payment_type              VARCHAR(50),
    trip_type                 VARCHAR(50),
    congestion_surcharge      VARCHAR(50),
    
    -- Rejection details
    reject_reason             VARCHAR(MAX),
    reject_timestamp          DATETIME2 DEFAULT GETDATE(),
    source_landing_id         BIGINT,
    source_file               VARCHAR(500),
    partition_key             VARCHAR(50)
);

PRINT '✅ Reject tables created for data quality tracking';
PRINT '';

-- ============================================================================
-- SILVER LAYER INDEXES (Optimized for Analytics and Gold Layer ETL)
-- ============================================================================
PRINT '--- Creating Silver Layer Indexes ---';
PRINT '';

-- Primary analytics indexes
CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_CSV_pickup_location 
ON SILVER.TRIP_DATA_CSV (PULocationID, lpep_pickup_datetime);

CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_CSV_payment_rate_trip 
ON SILVER.TRIP_DATA_CSV (payment_type, RatecodeID, trip_type);

CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_CSV_quality 
ON SILVER.TRIP_DATA_CSV (quality_flag, processed_timestamp);

-- Same indexes for Parquet table
CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_PARQUET_pickup_location 
ON SILVER.TRIP_DATA_PARQUET (PULocationID, lpep_pickup_datetime);

CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_PARQUET_payment_rate_trip 
ON SILVER.TRIP_DATA_PARQUET (payment_type, RatecodeID, trip_type);

CREATE NONCLUSTERED INDEX IX_SILVER_TRIP_DATA_PARQUET_quality 
ON SILVER.TRIP_DATA_PARQUET (quality_flag, processed_timestamp);

PRINT '✅ Silver layer indexes created for optimal performance';
PRINT '';

-- ============================================================================
-- COMPLETION SUMMARY
-- ============================================================================
PRINT '============================================================================';
PRINT 'SILVER LAYER DEPLOYMENT COMPLETE';
PRINT '============================================================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  ✅ SILVER.TRIP_DATA_CSV (Requirements 1b)';
PRINT '  ✅ SILVER.TRIP_DATA_PARQUET (Requirements 2b)';
PRINT '  ✅ SILVER.TRIP_DATA_CSV_REJECTS (Quality tracking)';
PRINT '  ✅ SILVER.TRIP_DATA_PARQUET_REJECTS (Quality tracking)';
PRINT '';
PRINT 'Features Implemented:';
PRINT '  • Proper data types from profiling analysis';
PRINT '  • Comprehensive data quality constraints';
PRINT '  • Check constraints for data validation';
PRINT '  • Quality flag framework (VALID/INVALID/WARNING)';
PRINT '  • Computed columns for analytics';
PRINT '  • Reject tables for invalid records';
PRINT '  • Optimized indexes for performance';
PRINT '';
PRINT 'Quality Framework:';
PRINT '  • 20+ validation rules implemented';
PRINT '  • Automatic quality scoring';
PRINT '  • Detailed error tracking';
PRINT '  • Referential integrity preparation';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Run 03-GOLD-TABLES.SQL (Gold layer for business consumption)';
PRINT '  2. Run 04-REFERENCE-TABLES.SQL (Reference data)';
PRINT '  3. Run ETL scripts to populate from LANDING';
PRINT '============================================================================';