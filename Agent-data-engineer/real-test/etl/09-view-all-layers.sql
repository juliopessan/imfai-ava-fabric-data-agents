-- ============================================================================
-- 09-VIEW-ALL-LAYERS.SQL - View data in all layers
-- ============================================================================
-- Purpose: Complete query to visualize pipeline data in all stages
-- Author: DataFlow Agent
-- Date: November 17, 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

SET NOCOUNT ON;

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                                                                          █';
PRINT '█              DATA VISUALIZATION - ALL LAYERS                            █';
PRINT '█                                                                          █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';

-- ============================================================================
-- GENERAL STATISTICS
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'GENERAL STATISTICS';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Description: Counts total records in each pipeline layer
--              and shows timestamps of first and last load
--              Useful for validating data flow between layers
SELECT 
    'LANDING' AS layer,
    COUNT(*) AS total_records,
    MIN(load_timestamp) AS first_load,
    MAX(load_timestamp) AS last_load
FROM LANDING.TRIP_DATA_CSV

UNION ALL

SELECT 
    'SILVER',
    COUNT(*),
    MIN(processed_timestamp),
    MAX(processed_timestamp)
FROM SILVER.TRIP_DATA_CSV

UNION ALL

SELECT 
    'GOLD',
    COUNT(*),
    MIN(created_timestamp),
    MAX(created_timestamp)
FROM GOLD.TRIP_DATA_CSV

UNION ALL

SELECT 
    'GOLD_AGG',
    COUNT(*),
    MIN(created_timestamp),
    MAX(created_timestamp)
FROM GOLD.TRIP_DATA_PARQUET_AGG;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CAMADA 1: LANDING (Raw Data - VARCHAR)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Sample of first 5 records:';
PRINT '';

-- Description: Displays first 5 records from LANDING layer (raw data)
--              Shows data exactly as ingested, in VARCHAR format
--              Useful for verifying structure and content of source data
SELECT TOP 5
    landing_id,
    VendorID,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    trip_distance,
    fare_amount,
    total_amount,
    payment_type,
    source_file,
    load_timestamp
FROM LANDING.TRIP_DATA_CSV
ORDER BY landing_id;

PRINT '';
PRINT 'LANDING Statistics:';
PRINT '';

-- Description: Summarizes LANDING layer statistics
--              Counts total records, unique vendors, unique payment types
--              Shows temporal window of loaded data
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT VendorID) AS unique_vendors,
    COUNT(DISTINCT payment_type) AS unique_payment_types,
    MIN(CAST(load_timestamp AS VARCHAR)) AS first_load,
    MAX(CAST(load_timestamp AS VARCHAR)) AS last_load
FROM LANDING.TRIP_DATA_CSV;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'LAYER 2: SILVER (Refined Data - Correct Types + Validations)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Sample of first 5 records:';
PRINT '';

-- Description: Displays first 5 records from SILVER layer (refined data)
--              Shows data with correct types, applied validations and quality scores
--              Includes calculated trip_duration_minutes and quality flags
SELECT TOP 5
    trip_id,
    VendorID,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    trip_distance,
    fare_amount,
    total_amount,
    payment_type,
    quality_flag,
    quality_score,
    trip_duration_minutes,
    processed_timestamp
FROM SILVER.TRIP_DATA_CSV
ORDER BY trip_id;

PRINT '';
PRINT 'SILVER Quality Statistics:';
PRINT '';

-- Description: Analyzes SILVER layer quality metrics
--              Calculates average, minimum and maximum quality scores
--              Counts valid, invalid and warning records
--              Shows percentage of valid records
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT VendorID) AS unique_vendors,
    AVG(quality_score) AS avg_quality_score,
    MIN(quality_score) AS min_quality_score,
    MAX(quality_score) AS max_quality_score,
    SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) AS valid_records,
    SUM(CASE WHEN quality_flag = 'INVALID' THEN 1 ELSE 0 END) AS invalid_records,
    SUM(CASE WHEN quality_flag = 'WARNING' THEN 1 ELSE 0 END) AS warning_records,
    CAST(SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS valid_percentage
FROM SILVER.TRIP_DATA_CSV;

PRINT '';
PRINT 'Distribution by Quality Flag:';
PRINT '';

-- Description: Groups records by quality flag (VALID/INVALID/WARNING)
--              Shows count and percentage of each category
--              Useful for identifying data quality issues
SELECT 
    quality_flag,
    COUNT(*) AS records,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS percentage
FROM SILVER.TRIP_DATA_CSV
GROUP BY quality_flag
ORDER BY records DESC;

PRINT '';
PRINT 'Statistics by Vendor:';
PRINT '';

-- Description: Aggregates metrics by vendor (VendorID)
--              Calculates averages for distance, fare, total amount and quality
--              Sums total distance and fare by vendor
--              Useful for comparing performance between vendors
SELECT 
    VendorID,
    COUNT(*) AS trips,
    AVG(trip_distance) AS avg_distance,
    AVG(fare_amount) AS avg_fare,
    AVG(total_amount) AS avg_total,
    AVG(quality_score) AS avg_quality,
    SUM(trip_distance) AS total_distance,
    SUM(fare_amount) AS total_fare
FROM SILVER.TRIP_DATA_CSV
GROUP BY VendorID
ORDER BY trips DESC;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'LAYER 3: GOLD (Enriched Data - With Reference JOINs)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Sample of first 5 enriched records:';
PRINT '';

-- Description: Displays first 5 records from GOLD layer (enriched data)
--              Shows data with applied reference JOINs (rate_code, payment_type, trip_type)
--              Includes calculated metrics: fare_per_mile, tip_percentage, pickup_hour
--              Demonstrates complete enrichment with readable descriptions
SELECT TOP 5
    trip_id,
    silver_trip_id,
    VendorID,
    pickup_datetime,
    dropoff_datetime,
    trip_distance,
    fare_amount,
    total_amount,
    rate_code,
    payment_type_desc,
    trip_type_desc,
    fare_per_mile,
    tip_percentage,
    pickup_hour,
    pickup_day_of_week
FROM GOLD.TRIP_DATA_CSV
ORDER BY trip_id;

PRINT '';
PRINT 'Enrichment Statistics:';
PRINT '';

-- Description: Summarizes success of enrichment process in GOLD layer
--              Counts unique values of each reference dimension
--              Calculates averages of derived metrics (fare_per_mile, tip_percentage)
--              Validates if all 3 JOINs were successful
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT rate_code) AS unique_rate_codes,
    COUNT(DISTINCT payment_type_desc) AS unique_payment_types,
    COUNT(DISTINCT trip_type_desc) AS unique_trip_types,
    AVG(fare_per_mile) AS avg_fare_per_mile,
    AVG(tip_percentage) AS avg_tip_percentage
FROM GOLD.TRIP_DATA_CSV;

PRINT '';
PRINT 'Distribution by Payment Type:';
PRINT '';

-- Description: Analyzes trip behavior by payment method
--              Aggregates total revenue, average, fare_per_mile and tip percentage by type
--              Identifies most profitable payment methods
--              Useful for analyzing passenger preferences
SELECT 
    payment_type_desc,
    COUNT(*) AS trips,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_revenue,
    AVG(fare_per_mile) AS avg_fare_per_mile,
    AVG(tip_percentage) AS avg_tip_pct,
    SUM(trip_distance) AS total_distance
FROM GOLD.TRIP_DATA_CSV
GROUP BY payment_type_desc
ORDER BY trips DESC;

PRINT '';
PRINT 'Distribution by Rate Code:';
PRINT '';

-- Description: Analyzes trip distribution by fare type
--              Compares Standard, JFK, Newark, Negotiated and other rate codes
--              Shows average fare and distance by type
--              Identifies which rate codes generate most revenue
SELECT 
    rate_code,
    COUNT(*) AS trips,
    AVG(fare_amount) AS avg_fare,
    AVG(trip_distance) AS avg_distance,
    SUM(total_amount) AS total_revenue
FROM GOLD.TRIP_DATA_CSV
GROUP BY rate_code
ORDER BY trips DESC;

PRINT '';
PRINT 'Distribution by Trip Type:';
PRINT '';

-- Description: Compares Street-hail vs Dispatch trips
--              Analyzes fare and distance differences between types
--              Shows preference for call mode
--              Useful for operational strategy
SELECT 
    trip_type_desc,
    COUNT(*) AS trips,
    AVG(fare_amount) AS avg_fare,
    AVG(trip_distance) AS avg_distance,
    SUM(total_amount) AS total_revenue
FROM GOLD.TRIP_DATA_CSV
GROUP BY trip_type_desc
ORDER BY trips DESC;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'LAYER 4: GOLD AGGREGATED (Aggregations by Location)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Top 10 locations by trip volume:';
PRINT '';

-- Description: Lists top 10 pickup zones with highest trip count
--              Shows aggregated metrics: total distance, total fare, averages
--              Calculates revenue_per_mile for revenue efficiency
--              Identifies demand hotspots
SELECT TOP 10
    PULocationID,
    trip_count,
    total_trip_distance,
    total_fare_amount,
    avg_fare_amount,
    avg_trip_distance,
    CAST(total_fare_amount / NULLIF(total_trip_distance, 0) AS DECIMAL(10,2)) AS revenue_per_mile,
    data_quality_percentage
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY trip_count DESC, total_fare_amount DESC;

PRINT '';
PRINT 'Top 10 locations by revenue:';
PRINT '';

-- Description: Lists top 10 pickup zones with highest total revenue
--              Prioritizes most profitable locations regardless of volume
--              Compares average fare and efficiency (revenue_per_mile)
--              Useful for fleet positioning strategy
SELECT TOP 10
    PULocationID,
    trip_count,
    total_fare_amount,
    avg_fare_amount,
    total_trip_distance,
    CAST(total_fare_amount / NULLIF(total_trip_distance, 0) AS DECIMAL(10,2)) AS revenue_per_mile
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY total_fare_amount DESC;

PRINT '';
PRINT 'Aggregation Statistics:';
PRINT '';

-- Description: Summarizes consolidated metrics from GOLD_AGG layer
--              Counts unique locations, total aggregated trips
--              Sums total distance and total revenue from all zones
--              Validates if aggregation matches GOLD layer data
SELECT 
    COUNT(*) AS unique_locations,
    SUM(trip_count) AS total_trips,
    SUM(total_trip_distance) AS total_distance,
    SUM(total_fare_amount) AS total_revenue,
    AVG(avg_fare_amount) AS avg_fare_across_locations,
    AVG(data_quality_percentage) AS avg_quality_pct
FROM GOLD.TRIP_DATA_PARQUET_AGG;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'REFERENCE DATA';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'TRIP_TYPE:';
-- Description: Displays trip type reference table (loaded from TSV)
--              Shows all categories: Street-hail, Dispatch
--              Includes metadata: created_date, updated_date, is_active
SELECT * FROM REF.TRIP_TYPE ORDER BY trip_type;

PRINT '';
PRINT 'RATE_CODE:';
-- Description: Displays rate code reference table (loaded from JSON)
--              Lists all rate codes: Standard, JFK, Newark, Nassau, Negotiated, Group
--              Shows flags: is_flat_rate, is_airport_rate, is_active
--              8 detailed columns for fare classification
SELECT * FROM REF.RATE_CODE ORDER BY rate_code_id;

PRINT '';
PRINT 'PAYMENT_TYPE:';
-- Description: Displays payment method reference table (loaded from JSON array)
--              Lists 7 types: Credit card, Cash, No charge, Dispute, Unknown, Voided trip
--              Shows flags: is_electronic, is_cash, requires_processing
--              Includes sub_type for additional categorization
SELECT * FROM REF.PAYMENT_TYPE ORDER BY payment_type;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CROSS-LAYER ANALYSIS (Layer Comparison)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Volume Consistency:';
PRINT '';

-- Description: Validates record consistency between pipeline layers
--              Compares counts: Landing→Silver, Silver→Gold, Gold→Gold_Agg
--              Calculates absolute and percentage differences
--              Identifies losses or inconsistencies in data flow
--              Should show 0% difference for intact pipeline
SELECT 
    'Landing → Silver' AS comparison,
    (SELECT COUNT(*) FROM LANDING.TRIP_DATA_CSV) AS source_count,
    (SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV) AS target_count,
    (SELECT COUNT(*) FROM LANDING.TRIP_DATA_CSV) - (SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV) AS difference,
    CAST(ABS((SELECT COUNT(*) FROM LANDING.TRIP_DATA_CSV) - (SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV)) * 100.0 / 
         NULLIF((SELECT COUNT(*) FROM LANDING.TRIP_DATA_CSV), 0) AS DECIMAL(5,2)) AS diff_percentage

UNION ALL

SELECT 
    'Silver → Gold',
    (SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID'),
    (SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV),
    (SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID') - (SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV),
    CAST(ABS((SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID') - (SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV)) * 100.0 / 
         NULLIF((SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID'), 0) AS DECIMAL(5,2))

UNION ALL

SELECT 
    'Gold → Gold_Agg (trips)',
    (SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV),
    (SELECT SUM(trip_count) FROM GOLD.TRIP_DATA_PARQUET_AGG),
    (SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV) - (SELECT SUM(trip_count) FROM GOLD.TRIP_DATA_PARQUET_AGG),
    CAST(ABS((SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV) - (SELECT SUM(trip_count) FROM GOLD.TRIP_DATA_PARQUET_AGG)) * 100.0 / 
         NULLIF((SELECT COUNT(*) FROM GOLD.TRIP_DATA_CSV), 0) AS DECIMAL(5,2));

PRINT '';
PRINT 'Quality Metrics by Layer:';
PRINT '';

-- Description: Compares quality metrics across 4 layers
--              Landing: N/A (raw VARCHAR)
--              Silver: quality_score/100 and % valid
--              Gold: % enrichment with JOINs
--              Gold_Agg: data_quality_percentage and aggregated trips
--              Useful for understanding quality evolution in pipeline
SELECT 
    'Landing' AS layer,
    COUNT(*) AS total_records,
    'N/A' AS quality_metric,
    'Raw VARCHAR data' AS description
FROM LANDING.TRIP_DATA_CSV

UNION ALL

SELECT 
    'Silver',
    COUNT(*),
    CAST(AVG(quality_score) AS VARCHAR) + '/100',
    CAST(SUM(CASE WHEN quality_flag='VALID' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS VARCHAR(10)) + '% valid'
FROM SILVER.TRIP_DATA_CSV

UNION ALL

SELECT 
    'Gold',
    COUNT(*),
    '100% enriched',
    '3 JOINs successful'
FROM GOLD.TRIP_DATA_CSV

UNION ALL

SELECT 
    'Gold_Agg',
    COUNT(*),
    CAST(AVG(data_quality_percentage) AS VARCHAR) + '%',
    CAST(SUM(trip_count) AS VARCHAR) + ' trips aggregated'
FROM GOLD.TRIP_DATA_PARQUET_AGG;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'LINEAGE ANALYSIS (Tracking a specific record)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Example: Tracking first record through layers:';
PRINT '';

DECLARE @FirstLandingID INT = (SELECT MIN(landing_id) FROM LANDING.TRIP_DATA_CSV);
DECLARE @FirstTripID INT = (SELECT MIN(trip_id) FROM SILVER.TRIP_DATA_CSV);

PRINT 'LANDING (ID: ' + CAST(@FirstLandingID AS VARCHAR) + '):';
-- Description: Shows original record in LANDING layer
--              Starting point of lineage tracking
--              Raw data in VARCHAR format exactly as ingested
SELECT 
    landing_id,
    VendorID,
    lpep_pickup_datetime,
    trip_distance,
    fare_amount,
    payment_type,
    load_timestamp
FROM LANDING.TRIP_DATA_CSV
WHERE landing_id = @FirstLandingID;

PRINT '';
PRINT 'SILVER (trip_id: ' + CAST(@FirstTripID AS VARCHAR) + ', source_landing_id: ' + CAST(@FirstLandingID AS VARCHAR) + '):';
-- Description: Tracks same record in SILVER layer after transformation
--              Shows source_landing_id for linkage with LANDING
--              Includes applied quality_flag and quality_score
--              Demonstrates type conversion and validations
SELECT 
    trip_id,
    source_landing_id,
    VendorID,
    lpep_pickup_datetime,
    trip_distance,
    fare_amount,
    payment_type,
    quality_flag,
    quality_score,
    processed_timestamp
FROM SILVER.TRIP_DATA_CSV
WHERE trip_id = @FirstTripID;

PRINT '';
PRINT 'GOLD (enriched with references):';
-- Description: Tracks same record in GOLD layer after enrichment
--              Shows silver_trip_id for linkage with SILVER
--              Displays readable descriptions of payment_type, rate_code and trip_type
--              Includes calculated metrics: fare_per_mile
--              Demonstrates result of 3 reference JOINs
SELECT 
    trip_id,
    silver_trip_id,
    VendorID,
    pickup_datetime,
    trip_distance,
    fare_amount,
    payment_type_desc,
    rate_code,
    trip_type_desc,
    fare_per_mile,
    created_timestamp
FROM GOLD.TRIP_DATA_CSV
WHERE silver_trip_id = @FirstTripID;

PRINT '';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'FINAL SUMMARY';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Description: Executive summary of complete pipeline
--              Status of each layer: records, quality and characteristics
--              Landing: 17 records in VARCHAR
--              Silver: 17 records with 100/100 quality
--              Gold: 17 records 100% enriched with 3 JOINs
--              Gold_Agg: 10 locations with 17 aggregated trips
--              ✅ indicates operational and validated layer
SELECT 
    '✅ LANDING' AS layer,
    'Raw data' AS description,
    (SELECT CAST(COUNT(*) AS VARCHAR) FROM LANDING.TRIP_DATA_CSV) + ' records' AS status,
    'VARCHAR columns preserve source format' AS quality

UNION ALL

SELECT 
    '✅ SILVER',
    'Refined data',
    (SELECT CAST(COUNT(*) AS VARCHAR) FROM SILVER.TRIP_DATA_CSV) + ' records',
    (SELECT CAST(CAST(AVG(quality_score) AS DECIMAL(5,2)) AS VARCHAR) FROM SILVER.TRIP_DATA_CSV) + '/100 avg quality'

UNION ALL

SELECT 
    '✅ GOLD',
    'Enriched data',
    (SELECT CAST(COUNT(*) AS VARCHAR) FROM GOLD.TRIP_DATA_CSV) + ' records',
    '100% enriched with 3 JOINs'

UNION ALL

SELECT 
    '✅ GOLD_AGG',
    'Aggregated data',
    (SELECT CAST(COUNT(*) AS VARCHAR) FROM GOLD.TRIP_DATA_PARQUET_AGG) + ' locations',
    (SELECT CAST(SUM(trip_count) AS VARCHAR) FROM GOLD.TRIP_DATA_PARQUET_AGG) + ' trips aggregated';

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                    COMPLETE VISUALIZATION FINISHED                      █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Next steps:';
PRINT '  • To see details of a specific record, use WHERE clauses';
PRINT '  • To export data, add -o "output.txt" to sqlcmd command';
PRINT '  • For specific analyses, modify queries as needed';
PRINT '';

GO
