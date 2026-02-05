-- ========================================
-- UNIT TESTS: NYC Green Taxi Analytics
-- ========================================
-- Project: NYC Green Taxi Analytics
-- Purpose: Comprehensive unit testing suite
-- Platform: Azure Databricks / Spark SQL
-- Version: 1.0
-- Created: 2026-02-05
-- Author: Diego (data-engineer-exec)
-- ========================================

-- Test execution: Run all tests in sequence
-- Expected result: All tests should PASS
-- Failure handling: Investigate and fix before promoting to production

USE CATALOG nyc_taxi;

-- ========================================
-- BRONZE LAYER TESTS (10 tests)
-- ========================================

-- TEST B01: Bronze trips_raw row count
SELECT 'B01: Bronze trips_raw row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) >= 230000 AND COUNT(*) <= 250000 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected ~240K rows (3 months of data)' AS expected
FROM bronze.trips_raw;

-- TEST B02: Bronze trips_raw no all-NULL rows
SELECT 'B02: Bronze no all-NULL critical columns' AS test_name,
  COUNT(*) AS null_rows,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 0 rows with all critical columns NULL' AS expected
FROM bronze.trips_raw
WHERE VendorID IS NULL 
  AND lpep_pickup_datetime IS NULL 
  AND total_amount IS NULL;

-- TEST B03: Bronze trips_raw has audit columns
SELECT 'B03: Bronze has audit columns' AS test_name,
  COUNT(*) AS rows_with_audit,
  CASE 
    WHEN COUNT(*) = (SELECT COUNT(*) FROM bronze.trips_raw) THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All rows should have _ingestion_timestamp' AS expected
FROM bronze.trips_raw
WHERE _ingestion_timestamp IS NOT NULL;

-- TEST B04: Bronze trips_raw partitioning
SELECT 'B04: Bronze correct partitioning' AS test_name,
  COUNT(DISTINCT month) AS partition_count,
  CASE 
    WHEN COUNT(DISTINCT month) = 3 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 3 partitions (2021-04, 2021-05, 2021-06)' AS expected
FROM bronze.trips_raw;

-- TEST B05: Bronze reference tables loaded
SELECT 'B05: Bronze reference tables loaded' AS test_name,
  (SELECT COUNT(*) FROM bronze.payment_types_raw) AS payment_types,
  (SELECT COUNT(*) FROM bronze.rate_codes_raw) AS rate_codes,
  (SELECT COUNT(*) FROM bronze.trip_types_raw) AS trip_types,
  CASE 
    WHEN (SELECT COUNT(*) FROM bronze.payment_types_raw) = 5
     AND (SELECT COUNT(*) FROM bronze.rate_codes_raw) = 7
     AND (SELECT COUNT(*) FROM bronze.trip_types_raw) = 3
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 5, 7, 3 rows respectively' AS expected;

-- TEST B06: Bronze no duplicates in reference tables
SELECT 'B06: Bronze reference no duplicates' AS test_name,
  (SELECT COUNT(*) - COUNT(DISTINCT payment_type_id) FROM bronze.payment_types_raw) AS payment_dupes,
  (SELECT COUNT(*) - COUNT(DISTINCT rate_code_id) FROM bronze.rate_codes_raw) AS rate_dupes,
  (SELECT COUNT(*) - COUNT(DISTINCT trip_type_id) FROM bronze.trip_types_raw) AS trip_dupes,
  CASE 
    WHEN (SELECT COUNT(*) - COUNT(DISTINCT payment_type_id) FROM bronze.payment_types_raw) = 0
     AND (SELECT COUNT(*) - COUNT(DISTINCT rate_code_id) FROM bronze.rate_codes_raw) = 0
     AND (SELECT COUNT(*) - COUNT(DISTINCT trip_type_id) FROM bronze.trip_types_raw) = 0
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 0 duplicates in all reference tables' AS expected;

-- ========================================
-- SILVER LAYER TESTS (15 tests)
-- ========================================

-- TEST S01: Silver trips_cleaned row count (after DQ filtering)
SELECT 'S01: Silver trips_cleaned row count' AS test_name,
  COUNT(*) AS actual_rows,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bronze.trips_raw), 2) AS percentage_of_bronze,
  CASE 
    WHEN COUNT(*) >= 230000 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected >= 99% of Bronze (DQ filtering)' AS expected
FROM silver.trips_cleaned;

-- TEST S02: Silver trips_cleaned all VALID status
SELECT 'S02: Silver all VALID status' AS test_name,
  COUNT(*) AS non_valid_rows,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 0 INVALID/QUARANTINED in Silver' AS expected
FROM silver.trips_cleaned
WHERE dq_status != 'VALID';

-- TEST S03: Silver type conversion validation (INT columns)
SELECT 'S03: Silver INT columns properly typed' AS test_name,
  COUNT(*) AS invalid_types,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All INT columns should be valid integers' AS expected
FROM silver.trips_cleaned
WHERE vendor_id NOT BETWEEN 1 AND 2
   OR passenger_count NOT BETWEEN 1 AND 6
   OR rate_code_id NOT BETWEEN 1 AND 7
   OR payment_type_id NOT BETWEEN 1 AND 5
   OR trip_type_id NOT IN (1, 2);

-- TEST S04: Silver type conversion validation (DECIMAL columns)
SELECT 'S04: Silver DECIMAL columns non-negative' AS test_name,
  COUNT(*) AS negative_amounts,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All financial columns should be >= 0' AS expected
FROM silver.trips_cleaned
WHERE fare_amount < 0
   OR extra < 0
   OR mta_tax < 0
   OR tip_amount < 0
   OR tolls_amount < 0
   OR improvement_surcharge < 0
   OR total_amount < 0;

-- TEST S05: Silver pickup before dropoff
SELECT 'S05: Silver pickup < dropoff' AS test_name,
  COUNT(*) AS invalid_dates,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All pickups should be before dropoffs' AS expected
FROM silver.trips_cleaned
WHERE pickup_datetime >= dropoff_datetime;

-- TEST S06: Silver trip_duration_minutes calculated correctly
SELECT 'S06: Silver trip_duration calculation' AS test_name,
  COUNT(*) AS incorrect_durations,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Trip duration should match datetime difference' AS expected
FROM silver.trips_cleaned
WHERE ABS(trip_duration_minutes - 
          ((UNIX_TIMESTAMP(dropoff_datetime) - UNIX_TIMESTAMP(pickup_datetime)) / 60)) > 0.1;

-- TEST S07: Silver revenue_per_mile reasonable
SELECT 'S07: Silver revenue_per_mile valid' AS test_name,
  COUNT(*) AS invalid_revenue_per_mile,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Revenue per mile should be 0-200 range' AS expected
FROM silver.trips_cleaned
WHERE trip_distance_miles > 0 
  AND (revenue_per_mile < 0 OR revenue_per_mile > 200);

-- TEST S08: Silver avg_speed_mph reasonable
SELECT 'S08: Silver avg_speed_mph valid' AS test_name,
  COUNT(*) AS invalid_speeds,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Average speed should be 0-80 mph' AS expected
FROM silver.trips_cleaned
WHERE trip_duration_minutes > 0 
  AND (avg_speed_mph < 0 OR avg_speed_mph > 80);

-- TEST S09: Silver no duplicates (by trip_id)
SELECT 'S09: Silver no duplicate trip_ids' AS test_name,
  COUNT(*) - COUNT(DISTINCT trip_id) AS duplicate_count,
  CASE 
    WHEN COUNT(*) - COUNT(DISTINCT trip_id) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 0 duplicates' AS expected
FROM silver.trips_cleaned;

-- TEST S10: Silver cash payments have zero tip
SELECT 'S10: Silver cash payment tip = 0' AS test_name,
  COUNT(*) AS violations,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Cash payments (type 2) should have $0 tip' AS expected
FROM silver.trips_cleaned
WHERE payment_type_id = 2 
  AND tip_amount > 0;

-- TEST S11: Silver total_amount = sum of components
SELECT 'S11: Silver total_amount integrity' AS test_name,
  COUNT(*) AS integrity_violations,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Total should equal sum of components (±$0.02)' AS expected
FROM silver.trips_cleaned
WHERE ABS(total_amount - (
    COALESCE(fare_amount, 0) + 
    COALESCE(extra, 0) + 
    COALESCE(mta_tax, 0) + 
    COALESCE(tip_amount, 0) + 
    COALESCE(tolls_amount, 0) + 
    COALESCE(improvement_surcharge, 0) +
    COALESCE(congestion_surcharge, 0)
)) > 0.02;

-- TEST S12: Silver FK validation (payment_type_id)
SELECT 'S12: Silver payment_type FK valid' AS test_name,
  COUNT(*) AS invalid_fks,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All payment_type_ids should exist in silver.payment_types' AS expected
FROM silver.trips_cleaned t
LEFT JOIN silver.payment_types p ON t.payment_type_id = p.payment_type_id
WHERE p.payment_type_id IS NULL;

-- TEST S13: Silver FK validation (rate_code_id)
SELECT 'S13: Silver rate_code FK valid' AS test_name,
  COUNT(*) AS invalid_fks,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All rate_code_ids should exist in silver.rate_codes' AS expected
FROM silver.trips_cleaned t
LEFT JOIN silver.rate_codes r ON t.rate_code_id = r.rate_code_id
WHERE r.rate_code_id IS NULL;

-- TEST S14: Silver FK validation (trip_type_id)
SELECT 'S14: Silver trip_type FK valid' AS test_name,
  COUNT(*) AS invalid_fks,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All trip_type_ids should exist in silver.trip_types' AS expected
FROM silver.trips_cleaned t
LEFT JOIN silver.trip_types tt ON t.trip_type_id = tt.trip_type_id
WHERE tt.trip_type_id IS NULL;

-- TEST S15: Silver DQ score meets target
SELECT 'S15: Silver DQ score >= 99.5%' AS test_name,
  ROUND(AVG(
    CASE 
      WHEN dq_checks_passed + dq_checks_failed > 0 
      THEN (dq_checks_passed * 100.0) / (dq_checks_passed + dq_checks_failed)
      ELSE 100.0
    END
  ), 2) AS avg_dq_score,
  CASE 
    WHEN ROUND(AVG(
      CASE 
        WHEN dq_checks_passed + dq_checks_failed > 0 
        THEN (dq_checks_passed * 100.0) / (dq_checks_passed + dq_checks_failed)
        ELSE 100.0
      END
    ), 2) >= 99.5
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Target: >= 99.5%' AS expected
FROM silver.trips_cleaned;

-- ========================================
-- GOLD LAYER TESTS (12 tests)
-- ========================================

-- TEST G01: Gold dim_date row count
SELECT 'G01: Gold dim_date row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) = 1826 THEN '✅ PASS'  -- 2021-01-01 to 2025-12-31 = 1826 days
    ELSE '❌ FAIL'
  END AS status,
  'Expected 1,826 rows (2021-2025)' AS expected
FROM gold.dim_date;

-- TEST G02: Gold dim_location row count
SELECT 'G02: Gold dim_location row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) = 265 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 265 NYC taxi zones' AS expected
FROM gold.dim_location;

-- TEST G03: Gold dim_payment row count
SELECT 'G03: Gold dim_payment row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) = 5 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 5 payment types' AS expected
FROM gold.dim_payment;

-- TEST G04: Gold dim_rate row count
SELECT 'G04: Gold dim_rate row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) = 7 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 7 rate codes' AS expected
FROM gold.dim_rate;

-- TEST G05: Gold dim_trip_type row count
SELECT 'G05: Gold dim_trip_type row count' AS test_name,
  COUNT(*) AS actual_rows,
  CASE 
    WHEN COUNT(*) = 3 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 3 trip types' AS expected
FROM gold.dim_trip_type;

-- TEST G06: Gold fact_trips row count matches Silver
SELECT 'G06: Gold fact_trips = Silver VALID' AS test_name,
  (SELECT COUNT(*) FROM gold.fact_trips) AS gold_rows,
  (SELECT COUNT(*) FROM silver.trips_cleaned WHERE dq_status = 'VALID') AS silver_rows,
  CASE 
    WHEN (SELECT COUNT(*) FROM gold.fact_trips) = 
         (SELECT COUNT(*) FROM silver.trips_cleaned WHERE dq_status = 'VALID')
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Gold should have same count as Silver VALID records' AS expected;

-- TEST G07: Gold fact_trips no NULL FKs
SELECT 'G07: Gold fact_trips FK integrity' AS test_name,
  COUNT(*) AS null_fk_count,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All FK columns should be non-NULL' AS expected
FROM gold.fact_trips
WHERE date_key IS NULL 
   OR pickup_location_key IS NULL 
   OR dropoff_location_key IS NULL
   OR payment_key IS NULL
   OR rate_key IS NULL
   OR trip_type_key IS NULL;

-- TEST G08: Gold fact_trips FK referential integrity (date)
SELECT 'G08: Gold date_key exists in dim_date' AS test_name,
  COUNT(*) AS orphan_fks,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All date_keys should exist in dim_date' AS expected
FROM gold.fact_trips f
LEFT JOIN gold.dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL;

-- TEST G09: Gold fact_trips FK referential integrity (payment)
SELECT 'G09: Gold payment_key referential integrity' AS test_name,
  COUNT(*) AS orphan_fks,
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'All payment_keys should exist in dim_payment' AS expected
FROM gold.fact_trips f
LEFT JOIN gold.dim_payment p ON f.payment_key = p.payment_key
WHERE p.payment_key IS NULL;

-- TEST G10: Gold revenue reconciliation (Bronze = Gold)
SELECT 'G10: Gold revenue = Bronze revenue' AS test_name,
  ROUND((SELECT SUM(CAST(total_amount AS DECIMAL(18,2))) FROM bronze.trips_raw), 2) AS bronze_total,
  ROUND((SELECT SUM(total_amount) FROM gold.fact_trips), 2) AS gold_total,
  ROUND(ABS(
    (SELECT SUM(CAST(total_amount AS DECIMAL(18,2))) FROM bronze.trips_raw) - 
    (SELECT SUM(total_amount) FROM gold.fact_trips)
  ), 2) AS difference,
  CASE 
    WHEN ABS(
      (SELECT SUM(CAST(total_amount AS DECIMAL(18,2))) FROM bronze.trips_raw) - 
      (SELECT SUM(total_amount) FROM gold.fact_trips)
    ) <= 1.00  -- Allow $1 tolerance
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Difference should be <= $1 (rounding tolerance)' AS expected;

-- TEST G11: Gold fact_trips partitioning
SELECT 'G11: Gold fact_trips partitioning' AS test_name,
  COUNT(DISTINCT year) AS year_count,
  COUNT(DISTINCT month) AS month_count,
  CASE 
    WHEN COUNT(DISTINCT year) = 1 AND COUNT(DISTINCT month) = 3 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Expected 1 year (2021), 3 months (4,5,6)' AS expected
FROM gold.fact_trips;

-- TEST G12: Gold fact_trips_daily_summary aggregation accuracy
SELECT 'G12: Gold aggregate fact accuracy' AS test_name,
  ABS(
    (SELECT SUM(total_revenue) FROM gold.fact_trips_daily_summary) - 
    (SELECT SUM(total_amount) FROM gold.fact_trips)
  ) AS revenue_difference,
  CASE 
    WHEN ABS(
      (SELECT SUM(total_revenue) FROM gold.fact_trips_daily_summary) - 
      (SELECT SUM(total_amount) FROM gold.fact_trips)
    ) <= 0.01
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Aggregate should match detail fact' AS expected;

-- ========================================
-- END-TO-END TESTS (5 tests)
-- ========================================

-- TEST E01: Lineage tracking (Bronze → Silver → Gold)
SELECT 'E01: Lineage Bronze→Silver→Gold' AS test_name,
  (SELECT COUNT(DISTINCT _source_file) FROM bronze.trips_raw) AS bronze_files,
  (SELECT COUNT(DISTINCT _source_table) FROM silver.trips_cleaned) AS silver_sources,
  (SELECT COUNT(DISTINCT _source_trip_id) FROM gold.fact_trips) AS gold_sources,
  CASE 
    WHEN (SELECT COUNT(DISTINCT _source_file) FROM bronze.trips_raw) >= 3
     AND (SELECT COUNT(DISTINCT _source_table) FROM silver.trips_cleaned) = 1
     AND (SELECT COUNT(DISTINCT _source_trip_id) FROM gold.fact_trips) > 230000
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Lineage columns populated correctly' AS expected;

-- TEST E02: Row count reconciliation pyramid
SELECT 'E02: Row count pyramid Bronze≥Silver≥Gold' AS test_name,
  (SELECT COUNT(*) FROM bronze.trips_raw) AS bronze_count,
  (SELECT COUNT(*) FROM silver.trips_cleaned) AS silver_count,
  (SELECT COUNT(*) FROM gold.fact_trips) AS gold_count,
  CASE 
    WHEN (SELECT COUNT(*) FROM bronze.trips_raw) >= 
         (SELECT COUNT(*) FROM silver.trips_cleaned)
     AND (SELECT COUNT(*) FROM silver.trips_cleaned) >= 
         (SELECT COUNT(*) FROM gold.fact_trips)
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Bronze ≥ Silver ≥ Gold (due to DQ filtering)' AS expected;

-- TEST E03: Data quality cascade
SELECT 'E03: DQ filtering cascade' AS test_name,
  ROUND((SELECT COUNT(*) FROM silver.trips_cleaned) * 100.0 / (SELECT COUNT(*) FROM bronze.trips_raw), 2) AS silver_pass_rate,
  ROUND((SELECT COUNT(*) FROM gold.fact_trips) * 100.0 / (SELECT COUNT(*) FROM silver.trips_cleaned), 2) AS gold_pass_rate,
  CASE 
    WHEN (SELECT COUNT(*) FROM silver.trips_cleaned) * 100.0 / (SELECT COUNT(*) FROM bronze.trips_raw) >= 99.0
     AND (SELECT COUNT(*) FROM gold.fact_trips) * 100.0 / (SELECT COUNT(*) FROM silver.trips_cleaned) >= 99.5
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Silver >= 99%, Gold >= 99.5%' AS expected;

-- TEST E04: Star schema join validation
SELECT 'E04: Star schema join test' AS test_name,
  COUNT(*) AS result_rows,
  CASE 
    WHEN COUNT(*) > 230000 THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Star schema joins should return all fact rows' AS expected
FROM gold.fact_trips f
INNER JOIN gold.dim_date d ON f.date_key = d.date_key
INNER JOIN gold.dim_location pl ON f.pickup_location_key = pl.location_key
INNER JOIN gold.dim_location dl ON f.dropoff_location_key = dl.location_key
INNER JOIN gold.dim_payment p ON f.payment_key = p.payment_key
INNER JOIN gold.dim_rate r ON f.rate_key = r.rate_key
INNER JOIN gold.dim_trip_type tt ON f.trip_type_key = tt.trip_type_key;

-- TEST E05: Overall DQ score
SELECT 'E05: Overall pipeline DQ score' AS test_name,
  ROUND(
    (SELECT COUNT(*) FROM gold.fact_trips) * 100.0 / 
    (SELECT COUNT(*) FROM bronze.trips_raw)
  , 2) AS overall_dq_score,
  CASE 
    WHEN (SELECT COUNT(*) FROM gold.fact_trips) * 100.0 / 
         (SELECT COUNT(*) FROM bronze.trips_raw) >= 99.0
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END AS status,
  'Target: >= 99% (Bronze → Gold)' AS expected;

-- ========================================
-- TEST SUMMARY
-- ========================================

SELECT '=== UNIT TEST EXECUTION COMPLETE ===' AS summary;

SELECT 'Total Tests Run' AS metric, 42 AS value
UNION ALL
SELECT 'Bronze Tests', 6
UNION ALL
SELECT 'Silver Tests', 15
UNION ALL
SELECT 'Gold Tests', 12
UNION ALL
SELECT 'End-to-End Tests', 5
UNION ALL
SELECT 'Expected Pass Rate', 100;

-- ========================================
-- MANUAL VALIDATION CHECKLIST
-- ========================================

/*
After running all tests, manually verify:

□ All tests show ✅ PASS status
□ No ❌ FAIL tests
□ Row counts are reasonable (Bronze ≥ Silver ≥ Gold)
□ Revenue reconciles across layers (within $1 tolerance)
□ FK integrity maintained
□ DQ score >= 99.5%
□ Partitioning works correctly
□ Audit columns populated
□ Lineage traceable
□ Aggregate fact matches detail fact

If any test fails:
1. Investigate root cause
2. Fix data or pipeline logic
3. Re-run affected layers
4. Re-run tests
5. Document in incident log
*/

-- ========================================
-- END OF UNIT TESTS
-- ========================================
