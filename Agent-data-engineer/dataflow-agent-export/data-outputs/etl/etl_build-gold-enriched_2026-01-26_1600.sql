-- =============================================================================
-- ETL Script: Build Gold Enriched
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- Purpose: Create enriched, denormalized dataset for analytics
-- Source: SILVER.GREEN_TAXI (VALID only) + Reference tables
-- Target: GOLD.TAXI_TRIPS_ENRICHED
SET NOCOUNT ON;
DECLARE @start_time DATETIME2 = GETDATE();
DECLARE @rows_inserted INT;
PRINT '=============================================================';
PRINT ' GOLD ENRICHMENT - Build Enriched Dataset';
PRINT ' Started: ' + CONVERT(VARCHAR, @start_time, 120);
PRINT '=============================================================';
-- Truncate target for full refresh
TRUNCATE TABLE GOLD.TAXI_TRIPS_ENRICHED;
-- Insert enriched data with reference lookups
INSERT INTO GOLD.TAXI_TRIPS_ENRICHED (
        trip_id,
        VendorID,
        vendor_name,
        pickup_datetime,
        dropoff_datetime,
        pickup_date,
        pickup_hour,
        pickup_day_of_week,
        pickup_day_name,
        pickup_month,
        pickup_year,
        is_weekend,
        is_rush_hour,
        PULocationID,
        DOLocationID,
        passenger_count,
        trip_distance,
        trip_duration_minutes,
        avg_speed_mph,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        congestion_surcharge,
        total_amount,
        tip_percentage,
        payment_type_id,
        payment_type_desc,
        rate_code_id,
        rate_code_desc,
        trip_type_id,
        trip_type_desc,
        store_and_fwd_flag
    )
SELECT s.trip_id,
    s.VendorID,
    v.vendor_name,
    -- Date/Time dimensions
    s.lpep_pickup_datetime,
    s.lpep_dropoff_datetime,
    CAST(s.lpep_pickup_datetime AS DATE),
    DATEPART(HOUR, s.lpep_pickup_datetime),
    DATEPART(WEEKDAY, s.lpep_pickup_datetime),
    DATENAME(WEEKDAY, s.lpep_pickup_datetime),
    MONTH(s.lpep_pickup_datetime),
    YEAR(s.lpep_pickup_datetime),
    -- Weekend flag (Saturday=7, Sunday=1)
    CASE
        WHEN DATEPART(WEEKDAY, s.lpep_pickup_datetime) IN (1, 7) THEN 1
        ELSE 0
    END,
    -- Rush hour flag (7-9 AM or 5-7 PM on weekdays)
    CASE
        WHEN DATEPART(WEEKDAY, s.lpep_pickup_datetime) NOT IN (1, 7)
        AND (
            DATEPART(HOUR, s.lpep_pickup_datetime) BETWEEN 7 AND 9
            OR DATEPART(HOUR, s.lpep_pickup_datetime) BETWEEN 17 AND 19
        ) THEN 1
        ELSE 0
    END,
    -- Location
    s.PULocationID,
    s.DOLocationID,
    -- Trip metrics
    s.passenger_count,
    s.trip_distance,
    s.trip_duration_minutes,
    -- Average speed (miles per hour)
    CASE
        WHEN s.trip_duration_minutes > 0
        AND s.trip_distance > 0 THEN CAST(
            s.trip_distance / (s.trip_duration_minutes / 60.0) AS DECIMAL(10, 2)
        )
        ELSE NULL
    END,
    -- Financial
    s.fare_amount,
    s.extra,
    s.mta_tax,
    s.tip_amount,
    s.tolls_amount,
    s.improvement_surcharge,
    s.congestion_surcharge,
    s.total_amount,
    -- Tip percentage
    CASE
        WHEN s.fare_amount > 0 THEN CAST(
            s.tip_amount * 100.0 / s.fare_amount AS DECIMAL(5, 2)
        )
        ELSE 0
    END,
    -- Enriched dimensions (with descriptions)
    s.payment_type,
    COALESCE(pt.payment_type_desc, 'Unknown'),
    s.RatecodeID,
    COALESCE(rc.rate_code_desc, 'Unknown'),
    s.trip_type,
    COALESCE(tt.trip_type_desc, 'Unknown'),
    s.store_and_fwd_flag
FROM SILVER.GREEN_TAXI s
    LEFT JOIN REF.VENDOR v ON s.VendorID = v.vendor_id
    LEFT JOIN REF.PAYMENT_TYPE pt ON s.payment_type = pt.payment_type_id
    LEFT JOIN REF.RATE_CODE rc ON s.RatecodeID = rc.rate_code_id
    LEFT JOIN REF.TRIP_TYPE tt ON s.trip_type = tt.trip_type_id
WHERE s.quality_flag = 'VALID';
SET @rows_inserted = @@ROWCOUNT;
-- Summary
PRINT '';
PRINT '=============================================================';
PRINT ' GOLD ENRICHMENT SUMMARY';
PRINT '=============================================================';
PRINT ' Records Enriched: ' + CAST(@rows_inserted AS VARCHAR);
PRINT ' Duration:         ' + CAST(
    DATEDIFF(SECOND, @start_time, GETDATE()) AS VARCHAR
) + ' seconds';
PRINT '=============================================================';
GO