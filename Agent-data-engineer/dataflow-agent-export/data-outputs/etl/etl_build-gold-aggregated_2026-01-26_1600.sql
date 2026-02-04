-- =============================================================================
-- ETL Script: Build Gold Aggregated
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- Purpose: Create aggregated metrics for analytics dashboards
-- Source: GOLD.TAXI_TRIPS_ENRICHED
-- Targets: GOLD.TAXI_TRIPS_AGG_LOCATION, GOLD.TAXI_TRIPS_AGG_DAILY
SET NOCOUNT ON;
DECLARE @start_time DATETIME2 = GETDATE();
DECLARE @rows_location INT,
    @rows_daily INT;
PRINT '=============================================================';
PRINT ' GOLD AGGREGATION - Build Summary Tables';
PRINT ' Started: ' + CONVERT(VARCHAR, @start_time, 120);
PRINT '=============================================================';
-- -----------------------------------------------------------------------------
-- Aggregation 1: By Pickup Location + Month
-- -----------------------------------------------------------------------------
PRINT '';
PRINT 'Building GOLD.TAXI_TRIPS_AGG_LOCATION...';
TRUNCATE TABLE GOLD.TAXI_TRIPS_AGG_LOCATION;
INSERT INTO GOLD.TAXI_TRIPS_AGG_LOCATION (
        PULocationID,
        trip_month,
        trip_year,
        total_trips,
        total_passengers,
        avg_passengers_per_trip,
        total_distance,
        avg_distance,
        min_distance,
        max_distance,
        total_duration_minutes,
        avg_duration_minutes,
        total_fare,
        total_tips,
        total_revenue,
        avg_fare,
        avg_tip,
        avg_total,
        tip_rate,
        credit_card_trips,
        cash_trips,
        credit_card_pct
    )
SELECT PULocationID,
    pickup_month,
    pickup_year,
    -- Trip counts
    COUNT(*) AS total_trips,
    SUM(COALESCE(passenger_count, 1)) AS total_passengers,
    CAST(
        AVG(
            CAST(COALESCE(passenger_count, 1) AS DECIMAL(5, 2))
        ) AS DECIMAL(5, 2)
    ),
    -- Distance metrics
    SUM(trip_distance),
    CAST(AVG(trip_distance) AS DECIMAL(10, 2)),
    MIN(trip_distance),
    MAX(trip_distance),
    -- Duration metrics
    SUM(trip_duration_minutes),
    CAST(
        AVG(CAST(trip_duration_minutes AS DECIMAL(10, 2))) AS DECIMAL(10, 2)
    ),
    -- Financial metrics
    SUM(fare_amount),
    SUM(tip_amount),
    SUM(total_amount),
    CAST(AVG(fare_amount) AS DECIMAL(10, 2)),
    CAST(AVG(tip_amount) AS DECIMAL(10, 2)),
    CAST(AVG(total_amount) AS DECIMAL(10, 2)),
    -- Tip rate (tips / fare)
    CASE
        WHEN SUM(fare_amount) > 0 THEN CAST(
            SUM(tip_amount) * 100.0 / SUM(fare_amount) AS DECIMAL(5, 2)
        )
        ELSE 0
    END,
    -- Payment breakdown
    SUM(
        CASE
            WHEN payment_type_id = 1 THEN 1
            ELSE 0
        END
    ),
    SUM(
        CASE
            WHEN payment_type_id = 2 THEN 1
            ELSE 0
        END
    ),
    CAST(
        SUM(
            CASE
                WHEN payment_type_id = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*) AS DECIMAL(5, 2)
    )
FROM GOLD.TAXI_TRIPS_ENRICHED
GROUP BY PULocationID,
    pickup_month,
    pickup_year;
SET @rows_location = @@ROWCOUNT;
PRINT 'Location aggregation rows: ' + CAST(@rows_location AS VARCHAR);
-- -----------------------------------------------------------------------------
-- Aggregation 2: Daily Summary
-- -----------------------------------------------------------------------------
PRINT '';
PRINT 'Building GOLD.TAXI_TRIPS_AGG_DAILY...';
TRUNCATE TABLE GOLD.TAXI_TRIPS_AGG_DAILY;
INSERT INTO GOLD.TAXI_TRIPS_AGG_DAILY (
        trip_date,
        day_of_week,
        day_name,
        is_weekend,
        trip_month,
        trip_year,
        total_trips,
        total_passengers,
        total_distance,
        avg_distance,
        total_fare,
        total_tips,
        total_revenue,
        avg_fare,
        avg_total,
        morning_rush_trips,
        evening_rush_trips
    )
SELECT pickup_date,
    DATEPART(WEEKDAY, pickup_date),
    DATENAME(WEEKDAY, pickup_date),
    CASE
        WHEN DATEPART(WEEKDAY, pickup_date) IN (1, 7) THEN 1
        ELSE 0
    END,
    MONTH(pickup_date),
    YEAR(pickup_date),
    -- Volume
    COUNT(*),
    SUM(COALESCE(passenger_count, 1)),
    -- Distance
    SUM(trip_distance),
    CAST(AVG(trip_distance) AS DECIMAL(10, 2)),
    -- Financial
    SUM(fare_amount),
    SUM(tip_amount),
    SUM(total_amount),
    CAST(AVG(fare_amount) AS DECIMAL(10, 2)),
    CAST(AVG(total_amount) AS DECIMAL(10, 2)),
    -- Rush hour breakdown
    SUM(
        CASE
            WHEN pickup_hour BETWEEN 7 AND 9 THEN 1
            ELSE 0
        END
    ),
    SUM(
        CASE
            WHEN pickup_hour BETWEEN 17 AND 19 THEN 1
            ELSE 0
        END
    )
FROM GOLD.TAXI_TRIPS_ENRICHED
GROUP BY pickup_date;
SET @rows_daily = @@ROWCOUNT;
PRINT 'Daily aggregation rows: ' + CAST(@rows_daily AS VARCHAR);
-- -----------------------------------------------------------------------------
-- Summary
-- -----------------------------------------------------------------------------
PRINT '';
PRINT '=============================================================';
PRINT ' GOLD AGGREGATION SUMMARY';
PRINT '=============================================================';
PRINT ' Location Aggregates: ' + CAST(@rows_location AS VARCHAR) + ' rows';
PRINT ' Daily Aggregates:    ' + CAST(@rows_daily AS VARCHAR) + ' rows';
PRINT ' Duration:            ' + CAST(
    DATEDIFF(SECOND, @start_time, GETDATE()) AS VARCHAR
) + ' seconds';
PRINT '=============================================================';
GO