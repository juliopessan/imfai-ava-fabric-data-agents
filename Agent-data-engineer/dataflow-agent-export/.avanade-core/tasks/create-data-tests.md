---
task: create-data-tests
version: 1.0
elicit: true
description: Generate comprehensive unit tests for data pipelines
---

# Create Data Tests

## Purpose
Create SQL-based unit tests to validate data integrity, transformations, and quality throughout the pipeline.

## Process

### Step 1: Define Test Scope
ASK the user:

1. **Tables to Test**: Which tables need validation?
2. **Test Types**: Row counts, schema, data quality, aggregations?
3. **Test Framework**: Plain SQL or specific testing framework?
4. **Acceptance Criteria**: What defines test success?

### Step 2: Generate Row Count Tests

```sql
-- Test 1: Validate row counts between file and table
CREATE OR REPLACE VIEW TEST.row_count_validation AS
SELECT 
    'LND.TRIP_DATA_CSV' as table_name,
    COUNT(*) as table_count,
    (SELECT COUNT(*) FROM external_source) as file_count,
    CASE 
        WHEN COUNT(*) = (SELECT COUNT(*) FROM external_source) 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM LND.TRIP_DATA_CSV;
```

### Step 3: Generate Schema Validation Tests

```sql
-- Test 2: Validate table schema matches expected
CREATE OR REPLACE VIEW TEST.schema_validation AS
SELECT 
    table_name,
    column_name,
    data_type,
    CASE 
        WHEN data_type = expected_type THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM information_schema.columns
WHERE table_schema = 'SILVER' AND table_name = '{TABLE_NAME}';
```

### Step 4: Generate Data Quality Tests

```sql
-- Test 3: Validate no null values in required columns
CREATE OR REPLACE VIEW TEST.null_check_{TABLE_NAME} AS
SELECT 
    '{COLUMN_NAME}' as column_name,
    COUNT(*) as null_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM SILVER.{TABLE_NAME}
WHERE {COLUMN_NAME} IS NULL;

-- Test 4: Validate data ranges
CREATE OR REPLACE VIEW TEST.range_check_{TABLE_NAME} AS
SELECT 
    '{COLUMN_NAME}' as column_name,
    MIN({COLUMN_NAME}) as min_value,
    MAX({COLUMN_NAME}) as max_value,
    CASE 
        WHEN MIN({COLUMN_NAME}) >= {MIN_EXPECTED} 
         AND MAX({COLUMN_NAME}) <= {MAX_EXPECTED}
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM SILVER.{TABLE_NAME};
```

### Step 5: Generate Transformation Tests

```sql
-- Test 5: Validate join integrity
CREATE OR REPLACE VIEW TEST.join_validation AS
SELECT 
    'GOLD.{TABLE_NAME}' as target_table,
    COUNT(DISTINCT g.id) as gold_count,
    COUNT(DISTINCT s.id) as silver_count,
    CASE 
        WHEN COUNT(DISTINCT g.id) = COUNT(DISTINCT s.id) 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM GOLD.{TABLE_NAME} g
FULL OUTER JOIN SILVER.{TABLE_NAME} s ON g.id = s.id;

-- Test 6: Validate aggregation logic
CREATE OR REPLACE VIEW TEST.aggregation_validation AS
SELECT 
    group_key,
    SUM(amount) as expected_sum,
    (SELECT SUM(amount) FROM GOLD.{AGG_TABLE} WHERE group_key = s.group_key) as actual_sum,
    CASE 
        WHEN ABS(SUM(amount) - actual_sum) < 0.01 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM SILVER.{TABLE_NAME} s
GROUP BY group_key;
```

### Step 6: Generate Data Comparison Tests

```sql
-- Test 7: Compare file data vs table data
CREATE OR REPLACE VIEW TEST.data_comparison_{TABLE_NAME} AS
WITH file_data AS (
    SELECT * FROM read_csv('{FILE_PATH}')
),
table_data AS (
    SELECT * FROM LND.{TABLE_NAME}
)
SELECT 
    COUNT(DISTINCT f.*) as file_unique_rows,
    COUNT(DISTINCT t.*) as table_unique_rows,
    CASE 
        WHEN COUNT(DISTINCT f.*) = COUNT(DISTINCT t.*) 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM file_data f
FULL OUTER JOIN table_data t ON f.id = t.id;
```

### Step 7: Create Test Runner

```sql
-- Master test runner
CREATE OR REPLACE VIEW TEST.all_tests_summary AS
SELECT * FROM TEST.row_count_validation
UNION ALL
SELECT * FROM TEST.schema_validation
UNION ALL
SELECT * FROM TEST.null_check_{TABLE_NAME}
UNION ALL
SELECT * FROM TEST.range_check_{TABLE_NAME}
UNION ALL
SELECT * FROM TEST.join_validation
UNION ALL
SELECT * FROM TEST.aggregation_validation
UNION ALL
SELECT * FROM TEST.data_comparison_{TABLE_NAME};

-- Execute all tests
SELECT 
    test_name,
    test_result,
    CURRENT_TIMESTAMP as test_execution_time
FROM TEST.all_tests_summary
ORDER BY test_result DESC, test_name;
```

## PySpark Testing Approach

```python
from pyspark.sql import functions as F

def test_row_count(spark, table_name, expected_count):
    actual_count = spark.table(table_name).count()
    assert actual_count == expected_count, f"Row count mismatch: {actual_count} != {expected_count}"
    print(f"✅ PASS: {table_name} row count = {actual_count}")

def test_no_nulls(spark, table_name, column_name):
    null_count = spark.table(table_name).filter(F.col(column_name).isNull()).count()
    assert null_count == 0, f"Found {null_count} nulls in {column_name}"
    print(f"✅ PASS: {table_name}.{column_name} has no nulls")

def test_aggregation(spark, source_table, agg_table, group_col, sum_col):
    expected = spark.table(source_table).groupBy(group_col).agg(F.sum(sum_col).alias("expected_sum"))
    actual = spark.table(agg_table).select(group_col, F.col(sum_col).alias("actual_sum"))
    
    comparison = expected.join(actual, group_col).filter(
        F.abs(F.col("expected_sum") - F.col("actual_sum")) > 0.01
    )
    
    assert comparison.count() == 0, "Aggregation mismatch found"
    print(f"✅ PASS: Aggregation on {group_col} matches")

# Run all tests
test_row_count(spark, "LND.TRIP_DATA_CSV", 10000)
test_no_nulls(spark, "SILVER.TRIP_DATA_CSV", "trip_id")
test_aggregation(spark, "SILVER.TRIP_DATA", "GOLD.TRIP_AGG", "location_id", "fare_amount")
```

## Output Structure

```
tests/
├── 01-row-count-tests.sql
├── 02-schema-validation-tests.sql
├── 03-null-check-tests.sql
├── 04-range-validation-tests.sql
├── 05-join-integrity-tests.sql
├── 06-aggregation-tests.sql
├── 07-data-comparison-tests.sql
├── 99-run-all-tests.sql
└── pyspark-tests.py
```

## Quality Standards

- ✅ Test every transformation step
- ✅ Compare files to tables
- ✅ Validate row counts match
- ✅ Check schema compliance
- ✅ Verify no unexpected nulls
- ✅ Validate data ranges
- ✅ Test join integrity
- ✅ Verify aggregation accuracy
- ✅ Clear PASS/FAIL reporting

## Completion

Tests are complete when:
- All tables have row count validation
- Schema matches expectations
- Data quality rules verified
- Transformations validated
- Test runner created
- Documentation provided
