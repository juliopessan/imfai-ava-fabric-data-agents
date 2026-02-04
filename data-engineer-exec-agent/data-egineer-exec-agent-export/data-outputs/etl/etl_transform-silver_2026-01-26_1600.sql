-- =============================================================================
-- ETL Script: Transform Landing to Silver (CSV Source)
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- Purpose: Transform raw CSV data from Landing to typed Silver layer
-- Implements: Type conversion, validation, quality flagging, reject capture
SET NOCOUNT ON;
DECLARE @start_time DATETIME2 = GETDATE();
DECLARE @rows_processed INT = 0;
DECLARE @rows_valid INT = 0;
DECLARE @rows_invalid INT = 0;
PRINT '=============================================================';
PRINT ' SILVER TRANSFORMATION - CSV SOURCE';
PRINT ' Started: ' + CONVERT(VARCHAR, @start_time, 120);
PRINT '=============================================================';
-- -----------------------------------------------------------------------------
-- Step 1: Insert VALID records to Silver
-- Validation rules applied:
--   R001: fare_amount >= 0
--   R002: total_amount >= 0
--   R003: trip_distance >= 0
--   R004: passenger_count BETWEEN 0 AND 10
--   R005: pickup_datetime <= dropoff_datetime
--   R006: payment_type IN (1,2,3,4,5,6)
--   R007: RatecodeID IN (1,2,3,4,5,6,99)
-- -----------------------------------------------------------------------------
INSERT INTO SILVER.GREEN_TAXI (
        VendorID,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        RatecodeID,
        PULocationID,
        DOLocationID,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        trip_type,
        congestion_surcharge,
        trip_duration_minutes,
        trip_month,
        trip_year,
        quality_flag,
        quality_issues,
        source_system,
        source_file,
        landing_timestamp
    )
SELECT -- Type conversions
    TRY_CAST(VendorID AS TINYINT),
    TRY_CAST(lpep_pickup_datetime AS DATETIME2),
    TRY_CAST(lpep_dropoff_datetime AS DATETIME2),
    LEFT(store_and_fwd_flag, 1),
    TRY_CAST(RatecodeID AS TINYINT),
    TRY_CAST(PULocationID AS SMALLINT),
    TRY_CAST(DOLocationID AS SMALLINT),
    TRY_CAST(passenger_count AS TINYINT),
    TRY_CAST(trip_distance AS DECIMAL(10, 2)),
    TRY_CAST(fare_amount AS DECIMAL(10, 2)),
    TRY_CAST(extra AS DECIMAL(10, 2)),
    TRY_CAST(mta_tax AS DECIMAL(10, 2)),
    TRY_CAST(tip_amount AS DECIMAL(10, 2)),
    TRY_CAST(tolls_amount AS DECIMAL(10, 2)),
    TRY_CAST(ehail_fee AS DECIMAL(10, 2)),
    TRY_CAST(improvement_surcharge AS DECIMAL(10, 2)),
    TRY_CAST(total_amount AS DECIMAL(10, 2)),
    TRY_CAST(payment_type AS TINYINT),
    TRY_CAST(trip_type AS TINYINT),
    TRY_CAST(congestion_surcharge AS DECIMAL(10, 2)),
    -- Derived: trip duration in minutes
    DATEDIFF(
        MINUTE,
        TRY_CAST(lpep_pickup_datetime AS DATETIME2),
        TRY_CAST(lpep_dropoff_datetime AS DATETIME2)
    ),
    -- Derived: month and year
    MONTH(TRY_CAST(lpep_pickup_datetime AS DATETIME2)),
    YEAR(TRY_CAST(lpep_pickup_datetime AS DATETIME2)),
    -- Quality flag: VALID if all rules pass
    'VALID',
    NULL,
    -- Source metadata
    'CSV',
    source_file,
    load_timestamp
FROM LND.GREEN_TAXI_CSV
WHERE -- All validation rules must pass for VALID
    TRY_CAST(fare_amount AS DECIMAL(10, 2)) >= 0
    AND TRY_CAST(total_amount AS DECIMAL(10, 2)) >= 0
    AND TRY_CAST(trip_distance AS DECIMAL(10, 2)) >= 0
    AND COALESCE(TRY_CAST(passenger_count AS TINYINT), 1) BETWEEN 0 AND 10
    AND TRY_CAST(lpep_pickup_datetime AS DATETIME2) <= TRY_CAST(lpep_dropoff_datetime AS DATETIME2)
    AND COALESCE(TRY_CAST(payment_type AS TINYINT), 0) IN (0, 1, 2, 3, 4, 5, 6)
    AND COALESCE(TRY_CAST(RatecodeID AS TINYINT), 1) IN (1, 2, 3, 4, 5, 6, 99) -- Required fields not null
    AND TRY_CAST(PULocationID AS SMALLINT) IS NOT NULL
    AND TRY_CAST(DOLocationID AS SMALLINT) IS NOT NULL
    AND TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NOT NULL;
SET @rows_valid = @@ROWCOUNT;
PRINT 'Valid records inserted: ' + CAST(@rows_valid AS VARCHAR);
-- -----------------------------------------------------------------------------
-- Step 2: Capture INVALID records to Reject table
-- -----------------------------------------------------------------------------
INSERT INTO SILVER.GREEN_TAXI_REJECT (
        VendorID,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        RatecodeID,
        PULocationID,
        DOLocationID,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        trip_type,
        congestion_surcharge,
        reject_reason,
        reject_rule_code,
        source_system,
        source_file
    )
SELECT VendorID,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    store_and_fwd_flag,
    RatecodeID,
    PULocationID,
    DOLocationID,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
    trip_type,
    congestion_surcharge,
    -- Build reject reason
    CONCAT_WS(
        '; ',
        CASE
            WHEN TRY_CAST(fare_amount AS DECIMAL(10, 2)) < 0 THEN 'R001: Negative fare_amount'
        END,
        CASE
            WHEN TRY_CAST(total_amount AS DECIMAL(10, 2)) < 0 THEN 'R002: Negative total_amount'
        END,
        CASE
            WHEN TRY_CAST(trip_distance AS DECIMAL(10, 2)) < 0 THEN 'R003: Negative trip_distance'
        END,
        CASE
            WHEN COALESCE(TRY_CAST(passenger_count AS TINYINT), 1) NOT BETWEEN 0 AND 10 THEN 'R004: Invalid passenger_count'
        END,
        CASE
            WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) > TRY_CAST(lpep_dropoff_datetime AS DATETIME2) THEN 'R005: Pickup after dropoff'
        END,
        CASE
            WHEN COALESCE(TRY_CAST(payment_type AS TINYINT), 0) NOT IN (0, 1, 2, 3, 4, 5, 6) THEN 'R006: Invalid payment_type'
        END,
        CASE
            WHEN TRY_CAST(PULocationID AS SMALLINT) IS NULL THEN 'R008: NULL PULocationID'
        END,
        CASE
            WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL THEN 'R009: Invalid pickup datetime'
        END
    ),
    'MULTI',
    'CSV',
    source_file
FROM LND.GREEN_TAXI_CSV
WHERE -- Any validation rule fails
    TRY_CAST(fare_amount AS DECIMAL(10, 2)) < 0
    OR TRY_CAST(total_amount AS DECIMAL(10, 2)) < 0
    OR TRY_CAST(trip_distance AS DECIMAL(10, 2)) < 0
    OR COALESCE(TRY_CAST(passenger_count AS TINYINT), 1) NOT BETWEEN 0 AND 10
    OR TRY_CAST(lpep_pickup_datetime AS DATETIME2) > TRY_CAST(lpep_dropoff_datetime AS DATETIME2)
    OR COALESCE(TRY_CAST(payment_type AS TINYINT), 0) NOT IN (0, 1, 2, 3, 4, 5, 6)
    OR TRY_CAST(PULocationID AS SMALLINT) IS NULL
    OR TRY_CAST(DOLocationID AS SMALLINT) IS NULL
    OR TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL;
SET @rows_invalid = @@ROWCOUNT;
PRINT 'Invalid records rejected: ' + CAST(@rows_invalid AS VARCHAR);
-- -----------------------------------------------------------------------------
-- Summary
-- -----------------------------------------------------------------------------
SET @rows_processed = @rows_valid + @rows_invalid;
PRINT '';
PRINT '=============================================================';
PRINT ' TRANSFORMATION SUMMARY';
PRINT '=============================================================';
PRINT ' Total Processed: ' + CAST(@rows_processed AS VARCHAR);
PRINT ' Valid Records:   ' + CAST(@rows_valid AS VARCHAR) + ' (' + CAST(
    CAST(
        @rows_valid * 100.0 / NULLIF(@rows_processed, 0) AS DECIMAL(5, 2)
    ) AS VARCHAR
) + '%)';
PRINT ' Invalid Records: ' + CAST(@rows_invalid AS VARCHAR) + ' (' + CAST(
    CAST(
        @rows_invalid * 100.0 / NULLIF(@rows_processed, 0) AS DECIMAL(5, 2)
    ) AS VARCHAR
) + '%)';
PRINT ' Duration:        ' + CAST(
    DATEDIFF(SECOND, @start_time, GETDATE()) AS VARCHAR
) + ' seconds';
PRINT '=============================================================';
GO