-- =============================================================================
-- DDL Script: Landing Tables (Bronze Layer)
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- -----------------------------------------------------------------------------
-- LND.GREEN_TAXI_CSV
-- Purpose: Raw CSV trip data ingestion (VARCHAR preservation)
-- Source: green_tripdata_2021-*.csv
-- -----------------------------------------------------------------------------
IF OBJECT_ID('LND.GREEN_TAXI_CSV', 'U') IS NOT NULL DROP TABLE LND.GREEN_TAXI_CSV;
GO CREATE TABLE LND.GREEN_TAXI_CSV (
        -- Source columns (all VARCHAR for raw preservation)
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
        -- Audit columns
        load_timestamp DATETIME2 DEFAULT GETDATE(),
        source_file VARCHAR(500),
        source_month VARCHAR(10)
    );
GO -- Add table comment
    EXEC sp_addextendedproperty @name = N'MS_Description',
    @value = N 'Landing table for NYC Green Taxi CSV data - raw VARCHAR preservation',
    @level0type = N'SCHEMA',
    @level0name = 'LND',
    @level1type = N'TABLE',
    @level1name = 'GREEN_TAXI_CSV';
GO -- -----------------------------------------------------------------------------
    -- LND.GREEN_TAXI_PARQUET
    -- Purpose: Raw Parquet trip data ingestion (VARCHAR preservation)
    -- Source: month=04/, month=05/, month=06/ partitions
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('LND.GREEN_TAXI_PARQUET', 'U') IS NOT NULL DROP TABLE LND.GREEN_TAXI_PARQUET;
GO CREATE TABLE LND.GREEN_TAXI_PARQUET (
        -- Source columns (all VARCHAR for raw preservation)
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
        -- Audit columns
        load_timestamp DATETIME2 DEFAULT GETDATE(),
        source_partition VARCHAR(100),
        source_file VARCHAR(500)
    );
GO -- =============================================================================
    -- Verification Query
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
WHERE TABLE_SCHEMA = 'LND'
ORDER BY TABLE_NAME;
GO PRINT '✅ Landing tables created successfully';
GO