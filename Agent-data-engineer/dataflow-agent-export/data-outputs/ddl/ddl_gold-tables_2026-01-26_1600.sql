-- =============================================================================
-- DDL Script: Gold Tables
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- -----------------------------------------------------------------------------
-- GOLD.TAXI_TRIPS_ENRICHED
-- Purpose: Denormalized, business-ready trip data with lookups
-- Source: SILVER.GREEN_TAXI + REF tables
-- -----------------------------------------------------------------------------
IF OBJECT_ID('GOLD.TAXI_TRIPS_ENRICHED', 'U') IS NOT NULL DROP TABLE GOLD.TAXI_TRIPS_ENRICHED;
GO CREATE TABLE GOLD.TAXI_TRIPS_ENRICHED (
        -- Primary Key
        trip_id BIGINT PRIMARY KEY,
        -- Trip identifiers
        VendorID TINYINT,
        vendor_name VARCHAR(50),
        -- Date/Time dimensions
        pickup_datetime DATETIME2 NOT NULL,
        dropoff_datetime DATETIME2 NOT NULL,
        pickup_date DATE NOT NULL,
        pickup_hour TINYINT,
        pickup_day_of_week TINYINT,
        pickup_day_name VARCHAR(10),
        pickup_month TINYINT,
        pickup_year SMALLINT,
        is_weekend BIT,
        is_rush_hour BIT,
        -- Location dimensions
        PULocationID SMALLINT NOT NULL,
        DOLocationID SMALLINT NOT NULL,
        -- Trip metrics
        passenger_count TINYINT,
        trip_distance DECIMAL(10, 2),
        trip_duration_minutes INT,
        avg_speed_mph DECIMAL(10, 2),
        -- Financial metrics
        fare_amount DECIMAL(10, 2),
        extra DECIMAL(10, 2),
        mta_tax DECIMAL(10, 2),
        tip_amount DECIMAL(10, 2),
        tolls_amount DECIMAL(10, 2),
        improvement_surcharge DECIMAL(10, 2),
        congestion_surcharge DECIMAL(10, 2),
        total_amount DECIMAL(10, 2),
        tip_percentage DECIMAL(5, 2),
        -- Enriched dimensions (from reference tables)
        payment_type_id TINYINT,
        payment_type_desc VARCHAR(50),
        rate_code_id TINYINT,
        rate_code_desc VARCHAR(50),
        trip_type_id TINYINT,
        trip_type_desc VARCHAR(50),
        store_and_fwd_flag CHAR(1),
        -- Audit
        processed_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- Indexes for analytics queries
    CREATE NONCLUSTERED INDEX IX_ENRICHED_PickupDate ON GOLD.TAXI_TRIPS_ENRICHED (pickup_date);
CREATE NONCLUSTERED INDEX IX_ENRICHED_PULocation ON GOLD.TAXI_TRIPS_ENRICHED (PULocationID);
CREATE NONCLUSTERED INDEX IX_ENRICHED_PaymentType ON GOLD.TAXI_TRIPS_ENRICHED (payment_type_id);
CREATE NONCLUSTERED INDEX IX_ENRICHED_Month ON GOLD.TAXI_TRIPS_ENRICHED (pickup_month, pickup_year);
GO -- -----------------------------------------------------------------------------
    -- GOLD.TAXI_TRIPS_AGG_LOCATION
    -- Purpose: Aggregated trip metrics by pickup location
    -- Grain: PULocationID + Month
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('GOLD.TAXI_TRIPS_AGG_LOCATION', 'U') IS NOT NULL DROP TABLE GOLD.TAXI_TRIPS_AGG_LOCATION;
GO CREATE TABLE GOLD.TAXI_TRIPS_AGG_LOCATION (
        -- Dimensions
        PULocationID SMALLINT NOT NULL,
        trip_month TINYINT NOT NULL,
        trip_year SMALLINT NOT NULL,
        -- Trip metrics
        total_trips INT,
        total_passengers INT,
        avg_passengers_per_trip DECIMAL(5, 2),
        -- Distance metrics
        total_distance DECIMAL(18, 2),
        avg_distance DECIMAL(10, 2),
        min_distance DECIMAL(10, 2),
        max_distance DECIMAL(10, 2),
        -- Duration metrics
        total_duration_minutes INT,
        avg_duration_minutes DECIMAL(10, 2),
        -- Financial metrics
        total_fare DECIMAL(18, 2),
        total_tips DECIMAL(18, 2),
        total_revenue DECIMAL(18, 2),
        avg_fare DECIMAL(10, 2),
        avg_tip DECIMAL(10, 2),
        avg_total DECIMAL(10, 2),
        tip_rate DECIMAL(5, 2),
        -- Payment breakdown
        credit_card_trips INT,
        cash_trips INT,
        credit_card_pct DECIMAL(5, 2),
        -- Audit
        processed_timestamp DATETIME2 DEFAULT GETDATE(),
        CONSTRAINT PK_AGG_LOCATION PRIMARY KEY (PULocationID, trip_month, trip_year)
    );
GO -- -----------------------------------------------------------------------------
    -- GOLD.TAXI_TRIPS_AGG_DAILY
    -- Purpose: Daily aggregated metrics for trend analysis
    -- Grain: Date
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('GOLD.TAXI_TRIPS_AGG_DAILY', 'U') IS NOT NULL DROP TABLE GOLD.TAXI_TRIPS_AGG_DAILY;
GO CREATE TABLE GOLD.TAXI_TRIPS_AGG_DAILY (
        -- Dimensions
        trip_date DATE PRIMARY KEY,
        day_of_week TINYINT,
        day_name VARCHAR(10),
        is_weekend BIT,
        trip_month TINYINT,
        trip_year SMALLINT,
        -- Volume metrics
        total_trips INT,
        total_passengers INT,
        -- Distance metrics
        total_distance DECIMAL(18, 2),
        avg_distance DECIMAL(10, 2),
        -- Financial metrics
        total_fare DECIMAL(18, 2),
        total_tips DECIMAL(18, 2),
        total_revenue DECIMAL(18, 2),
        avg_fare DECIMAL(10, 2),
        avg_total DECIMAL(10, 2),
        -- Hour distribution (peak hours)
        morning_rush_trips INT,
        -- 7-9 AM
        evening_rush_trips INT,
        -- 5-7 PM
        -- Audit
        processed_timestamp DATETIME2 DEFAULT GETDATE()
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
WHERE TABLE_SCHEMA = 'GOLD'
ORDER BY TABLE_NAME;
GO PRINT '✅ Gold tables created successfully';
GO