-- =============================================================================
-- Unit Tests: NYC Green Taxi Pipeline
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
SET NOCOUNT ON;
DECLARE @test_count INT = 0;
DECLARE @pass_count INT = 0;
DECLARE @fail_count INT = 0;
PRINT '╔═══════════════════════════════════════════════════════════════════╗';
PRINT '║           NYC GREEN TAXI PIPELINE - UNIT TESTS                    ║';
PRINT '╚═══════════════════════════════════════════════════════════════════╝';
PRINT '';
-- =============================================================================
-- TEST CATEGORY 1: ROW COUNT VALIDATION
-- =============================================================================
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
PRINT ' CATEGORY 1: ROW COUNT VALIDATION';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
-- TEST 1.1: Landing has data
SET @test_count + = 1;
DECLARE @landing_count INT;
SELECT @landing_count = COUNT(*)
FROM LND.GREEN_TAXI_CSV;
IF @landing_count > 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 1.1 PASS: Landing table has ' + FORMAT(@landing_count, 'N0') + ' rows';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 1.1 FAIL: Landing table is empty';
END -- TEST 1.2: Silver completeness (VALID + REJECT = LANDING)
SET @test_count + = 1;
DECLARE @silver_valid INT,
    @silver_reject INT,
    @silver_total INT;
SELECT @silver_valid = COUNT(*)
FROM SILVER.GREEN_TAXI;
SELECT @silver_reject = COUNT(*)
FROM SILVER.GREEN_TAXI_REJECT;
SET @silver_total = @silver_valid + @silver_reject;
IF @silver_total = @landing_count BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 1.2 PASS: No data loss (Landing=' + FORMAT(@landing_count, 'N0') + ', Silver=' + FORMAT(@silver_valid, 'N0') + ', Reject=' + FORMAT(@silver_reject, 'N0') + ')';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 1.2 FAIL: Data loss detected (Landing=' + FORMAT(@landing_count, 'N0') + ', Total Silver=' + FORMAT(@silver_total, 'N0') + ')';
END -- TEST 1.3: Gold uses only VALID records
SET @test_count + = 1;
DECLARE @gold_count INT;
SELECT @gold_count = COUNT(*)
FROM GOLD.TAXI_TRIPS_ENRICHED;
IF @gold_count = @silver_valid BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 1.3 PASS: Gold matches Silver VALID (' + FORMAT(@gold_count, 'N0') + ' rows)';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 1.3 FAIL: Gold/Silver mismatch (Gold=' + FORMAT(@gold_count, 'N0') + ', Silver VALID=' + FORMAT(@silver_valid, 'N0') + ')';
END -- =============================================================================
-- TEST CATEGORY 2: DATA QUALITY CHECKS
-- =============================================================================
PRINT '';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
PRINT ' CATEGORY 2: DATA QUALITY CHECKS';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
-- TEST 2.1: No negative fares in Silver VALID
SET @test_count + = 1;
DECLARE @neg_fare INT;
SELECT @neg_fare = COUNT(*)
FROM SILVER.GREEN_TAXI
WHERE fare_amount < 0
    AND quality_flag = 'VALID';
IF @neg_fare = 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 2.1 PASS: No negative fares in VALID records';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 2.1 FAIL: ' + CAST(@neg_fare AS VARCHAR) + ' negative fares in VALID';
END -- TEST 2.2: No NULL PULocationID in Silver
SET @test_count + = 1;
DECLARE @null_pu INT;
SELECT @null_pu = COUNT(*)
FROM SILVER.GREEN_TAXI
WHERE PULocationID IS NULL;
IF @null_pu = 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 2.2 PASS: No NULL PULocationID in Silver';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 2.2 FAIL: ' + CAST(@null_pu AS VARCHAR) + ' NULL PULocationID found';
END -- TEST 2.3: Valid payment types only
SET @test_count + = 1;
DECLARE @invalid_payment INT;
SELECT @invalid_payment = COUNT(*)
FROM SILVER.GREEN_TAXI
WHERE payment_type NOT IN (1, 2, 3, 4, 5, 6)
    AND payment_type IS NOT NULL;
IF @invalid_payment = 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 2.3 PASS: All payment types are valid (1-6)';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 2.3 FAIL: ' + CAST(@invalid_payment AS VARCHAR) + ' invalid payment types';
END -- =============================================================================
-- TEST CATEGORY 3: REFERENTIAL INTEGRITY
-- =============================================================================
PRINT '';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
PRINT ' CATEGORY 3: REFERENTIAL INTEGRITY';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
-- TEST 3.1: Payment type reference exists
SET @test_count + = 1;
DECLARE @orphan_payment INT;
SELECT @orphan_payment = COUNT(*)
FROM SILVER.GREEN_TAXI s
    LEFT JOIN REF.PAYMENT_TYPE p ON s.payment_type = p.payment_type_id
WHERE p.payment_type_id IS NULL
    AND s.payment_type IS NOT NULL;
IF @orphan_payment = 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 3.1 PASS: All payment types have reference data';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 3.1 FAIL: ' + CAST(@orphan_payment AS VARCHAR) + ' orphan payment types';
END -- TEST 3.2: Rate code reference exists
SET @test_count + = 1;
DECLARE @orphan_rate INT;
SELECT @orphan_rate = COUNT(*)
FROM SILVER.GREEN_TAXI s
    LEFT JOIN REF.RATE_CODE r ON s.RatecodeID = r.rate_code_id
WHERE r.rate_code_id IS NULL
    AND s.RatecodeID IS NOT NULL
    AND s.RatecodeID <> 99;
IF @orphan_rate = 0 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 3.2 PASS: All rate codes have reference data';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 3.2 FAIL: ' + CAST(@orphan_rate AS VARCHAR) + ' orphan rate codes';
END -- =============================================================================
-- TEST CATEGORY 4: AGGREGATION VALIDATION
-- =============================================================================
PRINT '';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
PRINT ' CATEGORY 4: AGGREGATION VALIDATION';
PRINT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
-- TEST 4.1: Location aggregation total matches detail
SET @test_count + = 1;
DECLARE @agg_total_trips BIGINT,
    @detail_total_trips INT;
SELECT @agg_total_trips = SUM(total_trips)
FROM GOLD.TAXI_TRIPS_AGG_LOCATION;
SELECT @detail_total_trips = COUNT(*)
FROM GOLD.TAXI_TRIPS_ENRICHED;
IF @agg_total_trips = @detail_total_trips BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 4.1 PASS: Aggregation trip count matches detail (' + FORMAT(@agg_total_trips, 'N0') + ')';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 4.1 FAIL: Trip count mismatch (Agg=' + FORMAT(@agg_total_trips, 'N0') + ', Detail=' + FORMAT(@detail_total_trips, 'N0') + ')';
END -- TEST 4.2: Revenue aggregation matches
SET @test_count + = 1;
DECLARE @agg_revenue DECIMAL(18, 2),
    @detail_revenue DECIMAL(18, 2);
SELECT @agg_revenue = SUM(total_revenue)
FROM GOLD.TAXI_TRIPS_AGG_LOCATION;
SELECT @detail_revenue = SUM(total_amount)
FROM GOLD.TAXI_TRIPS_ENRICHED;
IF ABS(@agg_revenue - @detail_revenue) < 1.00 BEGIN
SET @pass_count + = 1;
PRINT '✅ TEST 4.2 PASS: Revenue aggregation matches ($' + FORMAT(@agg_revenue, 'N2') + ')';
END
ELSE BEGIN
SET @fail_count + = 1;
PRINT '❌ TEST 4.2 FAIL: Revenue mismatch (Agg=$' + FORMAT(@agg_revenue, 'N2') + ', Detail=$' + FORMAT(@detail_revenue, 'N2') + ')';
END -- =============================================================================
-- TEST SUMMARY
-- =============================================================================
PRINT '';
PRINT '╔═══════════════════════════════════════════════════════════════════╗';
PRINT '║                      TEST EXECUTION SUMMARY                       ║';
PRINT '╠═══════════════════════════════════════════════════════════════════╣';
PRINT '║  Total Tests:  ' + CAST(@test_count AS VARCHAR(5)) + '                                               ║';
PRINT '║  Passed:       ' + CAST(@pass_count AS VARCHAR(5)) + '  (' + CAST(
    CAST(
        @pass_count * 100.0 / @test_count AS DECIMAL(5, 1)
    ) AS VARCHAR
) + '%)                                       ║';
PRINT '║  Failed:       ' + CAST(@fail_count AS VARCHAR(5)) + '                                               ║';
PRINT '╠═══════════════════════════════════════════════════════════════════╣';
IF @fail_count = 0 PRINT '║  STATUS:       ✅ ALL TESTS PASSED                               ║';
ELSE PRINT '║  STATUS:       ❌ SOME TESTS FAILED                              ║';
PRINT '╚═══════════════════════════════════════════════════════════════════╝';
GO