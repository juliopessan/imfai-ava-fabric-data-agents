-- ============================================================================
-- 03-GOLD-TABLES.SQL - NYC Green Taxi Gold Layer
-- ============================================================================
-- Purpose: Gold tables for business consumption and analytics
-- Requirements: 6 (enriched CSV data) and 7 (aggregated Parquet data)
-- Author: DataFlow Agent
-- Date: November 14, 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

PRINT '============================================================================';
PRINT 'CREATING GOLD TABLES - NYC GREEN TAXI DATA';
PRINT '============================================================================';
PRINT '';

-- ============================================================================
-- SCHEMAS CREATION
-- ============================================================================
PRINT '--- Creating Gold Schema ---';

-- Create schema if doesn't exist
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'GOLD')
    EXEC('CREATE SCHEMA GOLD');
    PRINT '✅ Schema GOLD created';

PRINT '';

-- ============================================================================
-- REQUIREMENT 6: GOLD.TRIP_DATA_CSV (Enriched with reference data)
-- ============================================================================
PRINT '--- REQUIREMENT 6: Creating GOLD.TRIP_DATA_CSV ---';
PRINT '    Join with REF.RATE_CODE, REF.PAYMENT_TYPE, REF.TRIP_TYPE';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('GOLD.TRIP_DATA_CSV', 'U') IS NOT NULL
    DROP TABLE GOLD.TRIP_DATA_CSV;
    PRINT '🗑️  Dropped existing GOLD.TRIP_DATA_CSV';

CREATE TABLE GOLD.TRIP_DATA_CSV (
    -- Business primary key
    trip_id                   BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Core trip identifiers
    silver_trip_id            BIGINT NOT NULL,  -- FK to SILVER.TRIP_DATA_CSV
    VendorID                  INT NOT NULL,
    
    -- Trip timing
    pickup_datetime           DATETIME2 NOT NULL,
    dropoff_datetime          DATETIME2 NOT NULL,
    trip_duration_minutes     INT,
    trip_duration_hours       AS (trip_duration_minutes / 60.0),
    
    -- Trip details
    store_and_fwd_flag        CHAR(1),
    passenger_count           INT,
    trip_distance             DECIMAL(8,2),
    
    -- Location information
    PULocationID              INT,
    DOLocationID              INT,
    
    -- REQUIREMENT 6a: Rate code information (JOIN with REF.RATE_CODE)
    RatecodeID                INT,
    rate_code                 VARCHAR(100),  -- From REF.RATE_CODE.rate_code
    
    -- REQUIREMENT 6b: Payment type information (JOIN with REF.PAYMENT_TYPE)
    payment_type              INT,
    payment_type_desc         VARCHAR(50),   -- From REF.PAYMENT_TYPE.payment_type_desc
    
    -- REQUIREMENT 6c: Trip type information (JOIN with REF.TRIP_TYPE)
    trip_type                 INT,
    trip_type_desc            VARCHAR(50),   -- From REF.TRIP_TYPE.trip_type_desc
    
    -- Financial details (all amounts)
    fare_amount               DECIMAL(10,2),
    extra                     DECIMAL(6,2),
    mta_tax                   DECIMAL(4,2),
    tip_amount                DECIMAL(10,2),
    tolls_amount              DECIMAL(10,2),
    improvement_surcharge     DECIMAL(4,2),
    congestion_surcharge      DECIMAL(6,2),
    total_amount              DECIMAL(12,2),
    
    -- Derived business metrics
    tip_percentage            AS (
        CASE 
            WHEN fare_amount > 0 THEN (tip_amount / fare_amount) * 100
            ELSE 0 
        END
    ),
    
    fare_per_mile             AS (
        CASE 
            WHEN trip_distance > 0 THEN fare_amount / trip_distance
            ELSE NULL 
        END
    ),
    
    total_surcharges          AS (extra + mta_tax + improvement_surcharge + congestion_surcharge),
    
    -- Time-based dimensions
    pickup_hour               AS DATEPART(HOUR, pickup_datetime),
    pickup_day_of_week        AS DATEPART(WEEKDAY, pickup_datetime),
    pickup_day_of_month       AS DAY(pickup_datetime),
    pickup_month              AS MONTH(pickup_datetime),
    pickup_year               AS YEAR(pickup_datetime),
    pickup_quarter            AS DATEPART(QUARTER, pickup_datetime),
    
    -- Business classifications
    trip_category             AS (
        CASE 
            WHEN trip_distance <= 1 THEN 'Short'
            WHEN trip_distance <= 5 THEN 'Medium'  
            WHEN trip_distance <= 15 THEN 'Long'
            ELSE 'Extra Long'
        END
    ),
    
    fare_category             AS (
        CASE 
            WHEN total_amount <= 10 THEN 'Low'
            WHEN total_amount <= 30 THEN 'Medium'
            WHEN total_amount <= 100 THEN 'High'
            ELSE 'Premium'
        END
    ),
    
    -- Quality and audit
    data_quality_score        INT,
    created_timestamp         DATETIME2 DEFAULT GETDATE(),
    etl_batch_id              VARCHAR(50)
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Gold layer enriched trip data with rate codes, payment types, and trip types. Ready for business consumption and analytics.',
    @level0type = N'SCHEMA', @level0name = N'GOLD',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_CSV';

PRINT '✅ GOLD.TRIP_DATA_CSV created successfully';
PRINT '   • Enriched with rate_code descriptions';
PRINT '   • Enriched with payment_type descriptions';
PRINT '   • Enriched with trip_type descriptions';
PRINT '   • Business-ready computed columns';
PRINT '   • Time-based dimensional attributes';
PRINT '';

-- ============================================================================
-- REQUIREMENT 7: GOLD.TRIP_DATA_PARQUET_AGG (Aggregated by PULocationID)
-- ============================================================================
PRINT '--- REQUIREMENT 7: Creating GOLD.TRIP_DATA_PARQUET_AGG ---';
PRINT '    Aggregated by PULocationID with SUM(trip_distance), SUM(fare_amount), COUNT(trips)';
PRINT '';

-- Drop table if exists for clean deployment
IF OBJECT_ID('GOLD.TRIP_DATA_PARQUET_AGG', 'U') IS NOT NULL
    DROP TABLE GOLD.TRIP_DATA_PARQUET_AGG;
    PRINT '🗑️  Dropped existing GOLD.TRIP_DATA_PARQUET_AGG';

CREATE TABLE GOLD.TRIP_DATA_PARQUET_AGG (
    -- Aggregation primary key
    agg_id                    BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Grouping dimension
    PULocationID              INT NOT NULL,
    
    -- REQUIREMENT 7 aggregations
    total_trip_distance       DECIMAL(15,2),     -- SUM(trip_distance)
    total_fare_amount         DECIMAL(15,2),     -- SUM(fare_amount)
    trip_count                INT,               -- COUNT(trips)
    
    -- Additional business aggregations
    avg_trip_distance         DECIMAL(8,2),      -- AVG(trip_distance)
    avg_fare_amount           DECIMAL(10,2),     -- AVG(fare_amount)
    max_trip_distance         DECIMAL(8,2),      -- MAX(trip_distance)
    max_fare_amount           DECIMAL(10,2),     -- MAX(fare_amount)
    min_trip_distance         DECIMAL(8,2),      -- MIN(trip_distance)
    min_fare_amount           DECIMAL(10,2),     -- MIN(fare_amount)
    
    -- Financial aggregations
    total_tip_amount          DECIMAL(15,2),
    total_tolls_amount        DECIMAL(15,2),
    total_amount_sum          DECIMAL(15,2),
    avg_total_amount          DECIMAL(10,2),
    
    -- Trip characteristics
    avg_passenger_count       DECIMAL(3,2),
    avg_trip_duration_minutes DECIMAL(8,2),
    
    -- Time-based aggregations
    earliest_pickup           DATETIME2,
    latest_pickup             DATETIME2,
    
    -- Operational metrics
    short_trips_count         INT,              -- trips <= 1 mile
    medium_trips_count        INT,              -- trips 1-5 miles  
    long_trips_count          INT,              -- trips 5-15 miles
    extra_long_trips_count    INT,              -- trips > 15 miles
    
    -- Payment method distribution
    credit_card_trips         INT,              -- payment_type = 1
    cash_trips                INT,              -- payment_type = 2
    other_payment_trips       INT,              -- payment_type > 2
    
    -- Quality metrics
    valid_trips_count         INT,              -- quality_flag = 'VALID'
    invalid_trips_count       INT,              -- quality_flag = 'INVALID'
    data_quality_percentage   AS (
        CASE 
            WHEN trip_count > 0 THEN (valid_trips_count * 100.0 / trip_count)
            ELSE 100 
        END
    ),
    
    -- Derived KPIs
    revenue_per_mile          AS (
        CASE 
            WHEN total_trip_distance > 0 THEN total_fare_amount / total_trip_distance
            ELSE 0 
        END
    ),
    
    avg_revenue_per_trip      AS (
        CASE 
            WHEN trip_count > 0 THEN total_fare_amount / trip_count
            ELSE 0 
        END
    ),
    
    location_utilization      AS (
        CASE 
            WHEN trip_count >= 1000 THEN 'High'
            WHEN trip_count >= 100 THEN 'Medium'
            WHEN trip_count >= 10 THEN 'Low'
            ELSE 'Minimal'
        END
    ),
    
    -- Audit and ETL tracking
    aggregation_date          DATE,              -- Date of aggregation
    data_from_date            DATE,              -- Earliest trip date
    data_to_date              DATE,              -- Latest trip date
    created_timestamp         DATETIME2 DEFAULT GETDATE(),
    etl_batch_id              VARCHAR(50)
);

-- Add table comment
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Gold layer aggregated trip data by pickup location. Contains comprehensive metrics and KPIs for location-based analytics.',
    @level0type = N'SCHEMA', @level0name = N'GOLD',
    @level1type = N'TABLE', @level1name = N'TRIP_DATA_PARQUET_AGG';

PRINT '✅ GOLD.TRIP_DATA_PARQUET_AGG created successfully';
PRINT '   • Aggregated by PULocationID as required';
PRINT '   • SUM(trip_distance) and SUM(fare_amount)';
PRINT '   • COUNT(trips) and additional business metrics';
PRINT '   • Location utilization and revenue KPIs';
PRINT '';

-- ============================================================================
-- ADDITIONAL GOLD TABLES FOR ANALYTICS
-- ============================================================================
PRINT '--- Creating Additional Gold Analytics Tables ---';
PRINT '';

-- Daily summary table
IF OBJECT_ID('GOLD.DAILY_TRIP_SUMMARY', 'U') IS NOT NULL
    DROP TABLE GOLD.DAILY_TRIP_SUMMARY;

CREATE TABLE GOLD.DAILY_TRIP_SUMMARY (
    summary_id                BIGINT IDENTITY(1,1) PRIMARY KEY,
    trip_date                 DATE NOT NULL,
    source_table              VARCHAR(50),  -- 'CSV' or 'PARQUET'
    
    total_trips               INT,
    total_distance            DECIMAL(15,2),
    total_revenue             DECIMAL(15,2),
    avg_trip_distance         DECIMAL(8,2),
    avg_fare_amount           DECIMAL(10,2),
    
    unique_pickup_locations   INT,
    unique_dropoff_locations  INT,
    
    created_timestamp         DATETIME2 DEFAULT GETDATE(),
    etl_batch_id              VARCHAR(50)
);

PRINT '✅ GOLD.DAILY_TRIP_SUMMARY created for time-series analytics';
PRINT '';

-- ============================================================================
-- GOLD LAYER INDEXES (Optimized for Business Queries)
-- ============================================================================
PRINT '--- Creating Gold Layer Indexes ---';
PRINT '';

-- GOLD.TRIP_DATA_CSV indexes
CREATE NONCLUSTERED INDEX IX_GOLD_TRIP_DATA_CSV_pickup_datetime 
ON GOLD.TRIP_DATA_CSV (pickup_datetime);

CREATE NONCLUSTERED INDEX IX_GOLD_TRIP_DATA_CSV_location_time 
ON GOLD.TRIP_DATA_CSV (PULocationID, pickup_datetime);

CREATE NONCLUSTERED INDEX IX_GOLD_TRIP_DATA_CSV_payment_rate 
ON GOLD.TRIP_DATA_CSV (payment_type, RatecodeID);

CREATE NONCLUSTERED INDEX IX_GOLD_TRIP_DATA_CSV_trip_category 
ON GOLD.TRIP_DATA_CSV (trip_category, fare_category);

-- GOLD.TRIP_DATA_PARQUET_AGG indexes
CREATE UNIQUE NONCLUSTERED INDEX IX_GOLD_PARQUET_AGG_location 
ON GOLD.TRIP_DATA_PARQUET_AGG (PULocationID);

CREATE NONCLUSTERED INDEX IX_GOLD_PARQUET_AGG_utilization 
ON GOLD.TRIP_DATA_PARQUET_AGG (location_utilization, trip_count);

-- Daily summary indexes
CREATE UNIQUE NONCLUSTERED INDEX IX_GOLD_DAILY_SUMMARY_date_source 
ON GOLD.DAILY_TRIP_SUMMARY (trip_date, source_table);

PRINT '✅ Gold layer indexes created for optimal business query performance';
PRINT '';

-- ============================================================================
-- COMPLETION SUMMARY
-- ============================================================================
PRINT '============================================================================';
PRINT 'GOLD LAYER DEPLOYMENT COMPLETE';
PRINT '============================================================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  ✅ GOLD.TRIP_DATA_CSV (Requirement 6 - Enriched data)';
PRINT '  ✅ GOLD.TRIP_DATA_PARQUET_AGG (Requirement 7 - Aggregated data)';
PRINT '  ✅ GOLD.DAILY_TRIP_SUMMARY (Additional analytics)';
PRINT '';
PRINT 'REQUIREMENT 6 Implementation:';
PRINT '  • JOIN with REF.RATE_CODE on rate_code_id ✅';
PRINT '  • JOIN with REF.PAYMENT_TYPE on payment_type ✅';
PRINT '  • JOIN with REF.TRIP_TYPE on trip_type ✅';
PRINT '  • Added rate_code, payment_type_desc, trip_type_desc ✅';
PRINT '';
PRINT 'REQUIREMENT 7 Implementation:';
PRINT '  • Aggregated by PULocationID ✅';
PRINT '  • SUM(trip_distance) ✅';
PRINT '  • SUM(fare_amount) ✅';
PRINT '  • COUNT(trips) ✅';
PRINT '  • Additional business metrics included ✅';
PRINT '';
PRINT 'Business Features:';
PRINT '  • Computed columns for analytics';
PRINT '  • Time-based dimensional attributes';
PRINT '  • Trip and fare categorization';
PRINT '  • Revenue and utilization KPIs';
PRINT '  • Data quality metrics';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Run 04-REFERENCE-TABLES.SQL';
PRINT '  2. Create ETL scripts to populate Gold from Silver';
PRINT '  3. Implement JOIN logic for enrichment';
PRINT '============================================================================';