-- =============================================================================
-- DDL Script: Silver Tables
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- -----------------------------------------------------------------------------
-- SILVER.GREEN_TAXI
-- Purpose: Typed, validated trip data with quality flags
-- Source: LND.GREEN_TAXI_CSV, LND.GREEN_TAXI_PARQUET
-- -----------------------------------------------------------------------------
IF OBJECT_ID('SILVER.GREEN_TAXI', 'U') IS NOT NULL DROP TABLE SILVER.GREEN_TAXI;
GO CREATE TABLE SILVER.GREEN_TAXI (
        -- Primary Key
        trip_id BIGINT IDENTITY(1, 1) PRIMARY KEY,
        -- Typed source columns
        VendorID TINYINT,
        lpep_pickup_datetime DATETIME2,
        lpep_dropoff_datetime DATETIME2,
        store_and_fwd_flag CHAR(1),
        RatecodeID TINYINT,
        PULocationID SMALLINT NOT NULL,
        DOLocationID SMALLINT NOT NULL,
        passenger_count TINYINT,
        trip_distance DECIMAL(10, 2),
        fare_amount DECIMAL(10, 2),
        extra DECIMAL(10, 2),
        mta_tax DECIMAL(10, 2),
        tip_amount DECIMAL(10, 2),
        tolls_amount DECIMAL(10, 2),
        ehail_fee DECIMAL(10, 2),
        improvement_surcharge DECIMAL(10, 2),
        total_amount DECIMAL(10, 2),
        payment_type TINYINT,
        trip_type TINYINT,
        congestion_surcharge DECIMAL(10, 2),
        -- Derived columns
        trip_duration_minutes INT,
        trip_month TINYINT,
        trip_year SMALLINT,
        -- Quality columns
        quality_flag VARCHAR(20) NOT NULL DEFAULT 'VALID',
        quality_issues VARCHAR(500),
        -- Audit columns
        source_system VARCHAR(20),
        -- 'CSV' or 'PARQUET'
        source_file VARCHAR(500),
        landing_timestamp DATETIME2,
        processed_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- Indexes for query performance
    CREATE NONCLUSTERED INDEX IX_GREEN_TAXI_PickupDate ON SILVER.GREEN_TAXI (lpep_pickup_datetime);
CREATE NONCLUSTERED INDEX IX_GREEN_TAXI_PULocation ON SILVER.GREEN_TAXI (PULocationID);
CREATE NONCLUSTERED INDEX IX_GREEN_TAXI_QualityFlag ON SILVER.GREEN_TAXI (quality_flag);
CREATE NONCLUSTERED INDEX IX_GREEN_TAXI_PaymentType ON SILVER.GREEN_TAXI (payment_type);
GO -- -----------------------------------------------------------------------------
    -- SILVER.GREEN_TAXI_REJECT
    -- Purpose: Rejected records from validation
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('SILVER.GREEN_TAXI_REJECT', 'U') IS NOT NULL DROP TABLE SILVER.GREEN_TAXI_REJECT;
GO CREATE TABLE SILVER.GREEN_TAXI_REJECT (
        reject_id BIGINT IDENTITY(1, 1) PRIMARY KEY,
        -- Original values (VARCHAR to preserve raw data)
        VendorID VARCHAR(50),
        lpep_pickup_datetime VARCHAR(50),
        lpep_dropoff_datetime VARCHAR(50),
        store_and_fwd_flag VARCHAR(10),
        RatecodeID VARCHAR(50),
        PULocationID VARCHAR(50),
        DOLocationID VARCHAR(50),
        passenger_count VARCHAR(50),
        trip_distance VARCHAR(50),
        fare_amount VARCHAR(50),
        extra VARCHAR(50),
        mta_tax VARCHAR(50),
        tip_amount VARCHAR(50),
        tolls_amount VARCHAR(50),
        ehail_fee VARCHAR(50),
        improvement_surcharge VARCHAR(50),
        total_amount VARCHAR(50),
        payment_type VARCHAR(50),
        trip_type VARCHAR(50),
        congestion_surcharge VARCHAR(50),
        -- Reject metadata
        reject_reason VARCHAR(500) NOT NULL,
        reject_rule_code VARCHAR(20),
        source_system VARCHAR(20),
        source_file VARCHAR(500),
        reject_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- =============================================================================
    -- Verification
    -- =============================================================================
SELECT TABLE_SCHEMA,
    TABLE_NAME,
    (
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS c
        WHERE c.TABLE_SCHEMA = t.TABLE_SCHEMA
            AND c.TABLE_NAME = t.TABLE_NAME
    ) AS column_count
FROM INFORMATION_SCHEMA.TABLES t
WHERE TABLE_SCHEMA = 'SILVER'
ORDER BY TABLE_NAME;
GO PRINT '✅ Silver tables created successfully';
GO