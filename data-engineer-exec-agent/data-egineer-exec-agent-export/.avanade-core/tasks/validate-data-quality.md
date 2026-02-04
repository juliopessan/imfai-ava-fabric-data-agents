---
task: validate-data-quality
version: 1.0
elicit: true
description: Perform comprehensive data quality validation checks on pipeline data
---

# Validate Data Quality

## Purpose
Execute comprehensive data quality checks across Landing, Silver, and Gold layers to identify issues, anomalies, and ensure data meets quality standards.

## Process

### Step 1: Identify Validation Scope
ASK the user:

1. **Tables to Validate**: Which tables need quality checks?
2. **Quality Dimensions**: Completeness, Accuracy, Consistency, Timeliness, Validity?
3. **Critical Fields**: Which columns are most important?
4. **Thresholds**: What are acceptable error rates?

### Step 2: Completeness Checks

**Null/Missing Value Analysis:**
```sql
-- Check for nulls in critical columns
SELECT 
    'SILVER.TRIP_DATA' as table_name,
    'trip_id' as column_name,
    COUNT(*) as total_rows,
    SUM(CASE WHEN trip_id IS NULL THEN 1 ELSE 0 END) as null_count,
    ROUND(100.0 * SUM(CASE WHEN trip_id IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as null_pct,
    CASE 
        WHEN SUM(CASE WHEN trip_id IS NULL THEN 1 ELSE 0 END) = 0 THEN '✅ PASS'
        ELSE '❌ FAIL'
    END as quality_status
FROM SILVER.TRIP_DATA;

-- Check for empty strings
SELECT 
    column_name,
    COUNT(*) as empty_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM table_name), 2) as empty_pct
FROM table_name
WHERE column_name = '' OR TRIM(column_name) = ''
GROUP BY column_name;
```

**PySpark Completeness:**
```python
from pyspark.sql import functions as F

def check_completeness(df, table_name):
    total_rows = df.count()
    results = []
    
    for col_name in df.columns:
        null_count = df.filter(F.col(col_name).isNull()).count()
        null_pct = (null_count / total_rows) * 100
        
        results.append({
            'table': table_name,
            'column': col_name,
            'total_rows': total_rows,
            'null_count': null_count,
            'null_pct': round(null_pct, 2),
            'status': '✅ PASS' if null_count == 0 else '⚠️ WARNING'
        })
    
    return results
```

### Step 3: Validity Checks

**Data Type Validation:**
```sql
-- Verify numeric fields are valid numbers
SELECT 
    'fare_amount' as field_name,
    COUNT(*) as invalid_count,
    STRING_AGG(DISTINCT fare_amount, ', ') as sample_invalid_values
FROM SILVER.TRIP_DATA
WHERE TRY_CAST(fare_amount AS DECIMAL) IS NULL
  AND fare_amount IS NOT NULL;

-- Verify date fields are valid dates
SELECT 
    'trip_date' as field_name,
    COUNT(*) as invalid_count,
    STRING_AGG(DISTINCT trip_date, ', ') as sample_invalid_values
FROM SILVER.TRIP_DATA
WHERE TRY_CAST(trip_date AS DATE) IS NULL
  AND trip_date IS NOT NULL;
```

**Range Validation:**
```sql
-- Check numeric ranges
SELECT 
    'fare_amount' as field_name,
    MIN(fare_amount) as min_value,
    MAX(fare_amount) as max_value,
    AVG(fare_amount) as avg_value,
    CASE 
        WHEN MIN(fare_amount) < 0 THEN '❌ FAIL: Negative values'
        WHEN MAX(fare_amount) > 10000 THEN '⚠️ WARNING: Outliers detected'
        ELSE '✅ PASS'
    END as quality_status
FROM SILVER.TRIP_DATA
WHERE TRY_CAST(fare_amount AS DECIMAL) IS NOT NULL;

-- Check date ranges
SELECT 
    'trip_date' as field_name,
    MIN(trip_date) as earliest_date,
    MAX(trip_date) as latest_date,
    CASE 
        WHEN MIN(trip_date) < '2000-01-01' THEN '❌ FAIL: Date too old'
        WHEN MAX(trip_date) > CURRENT_DATE THEN '❌ FAIL: Future dates'
        ELSE '✅ PASS'
    END as quality_status
FROM SILVER.TRIP_DATA;
```

**Format Validation:**
```sql
-- Email format
SELECT COUNT(*) as invalid_email_count
FROM SILVER.CUSTOMERS
WHERE email NOT LIKE '%_@_%.__%'
  AND email IS NOT NULL;

-- Phone format
SELECT COUNT(*) as invalid_phone_count
FROM SILVER.CUSTOMERS
WHERE phone !~ '^\+?[0-9]{10,15}$'
  AND phone IS NOT NULL;
```

### Step 4: Consistency Checks

**Cross-Table Consistency:**
```sql
-- Check referential integrity
SELECT 
    'SILVER.TRIP_DATA' as child_table,
    'REF.RATE_CODE' as parent_table,
    COUNT(*) as orphan_count,
    STRING_AGG(DISTINCT CAST(t.rate_code_id AS VARCHAR), ', ') as orphan_values
FROM SILVER.TRIP_DATA t
LEFT JOIN REF.RATE_CODE r ON t.rate_code_id = r.rate_code_id
WHERE r.rate_code_id IS NULL
  AND t.rate_code_id IS NOT NULL;
```

**Internal Consistency:**
```sql
-- Logical consistency (e.g., end_date >= start_date)
SELECT 
    COUNT(*) as inconsistent_records,
    'end_date < start_date' as inconsistency_type
FROM SILVER.TRIP_DATA
WHERE dropoff_datetime < pickup_datetime;

-- Sum consistency (e.g., total = subtotal + tax)
SELECT 
    COUNT(*) as inconsistent_records,
    'total != subtotal + tax' as inconsistency_type
FROM SILVER.TRIP_DATA
WHERE ABS((fare_amount + tip_amount + tolls_amount) - total_amount) > 0.01;
```

### Step 5: Uniqueness Checks

**Duplicate Detection:**
```sql
-- Check for duplicate primary keys
SELECT 
    trip_id,
    COUNT(*) as duplicate_count
FROM SILVER.TRIP_DATA
GROUP BY trip_id
HAVING COUNT(*) > 1;

-- Check for duplicate records (all columns)
SELECT 
    *,
    COUNT(*) OVER (PARTITION BY trip_id, pickup_datetime, fare_amount) as dup_count
FROM SILVER.TRIP_DATA
WHERE COUNT(*) OVER (PARTITION BY trip_id, pickup_datetime, fare_amount) > 1;
```

**PySpark Duplicates:**
```python
# Find duplicates
df_with_dup_count = df.groupBy(df.columns).count()
duplicates = df_with_dup_count.filter(F.col('count') > 1)

print(f"Duplicate records: {duplicates.count()}")
duplicates.show()
```

### Step 6: Accuracy Checks

**Statistical Outliers:**
```sql
-- Z-score outlier detection
WITH stats AS (
    SELECT 
        AVG(fare_amount) as mean_fare,
        STDDEV(fare_amount) as stddev_fare
    FROM SILVER.TRIP_DATA
)
SELECT 
    trip_id,
    fare_amount,
    (fare_amount - mean_fare) / stddev_fare as z_score,
    CASE 
        WHEN ABS((fare_amount - mean_fare) / stddev_fare) > 3 THEN '⚠️ OUTLIER'
        ELSE '✅ NORMAL'
    END as outlier_status
FROM SILVER.TRIP_DATA
CROSS JOIN stats
WHERE ABS((fare_amount - mean_fare) / stddev_fare) > 3;
```

**Business Rule Validation:**
```sql
-- Check business rules
SELECT 
    'passenger_count > 0 AND <= 6' as rule,
    COUNT(*) as violation_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM SILVER.TRIP_DATA), 2) as violation_pct
FROM SILVER.TRIP_DATA
WHERE passenger_count <= 0 OR passenger_count > 6;
```

### Step 7: Timeliness Checks

**Data Freshness:**
```sql
-- Check data recency
SELECT 
    table_name,
    MAX(load_timestamp) as last_load_time,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(load_timestamp))) / 3600 as hours_since_load,
    CASE 
        WHEN MAX(load_timestamp) > CURRENT_TIMESTAMP - INTERVAL '24 hours' THEN '✅ FRESH'
        WHEN MAX(load_timestamp) > CURRENT_TIMESTAMP - INTERVAL '48 hours' THEN '⚠️ STALE'
        ELSE '❌ VERY STALE'
    END as freshness_status
FROM (
    SELECT 'LND.TRIP_DATA_CSV' as table_name, MAX(load_timestamp) as load_timestamp
    FROM LND.TRIP_DATA_CSV
    UNION ALL
    SELECT 'SILVER.TRIP_DATA_CSV', MAX(processed_timestamp)
    FROM SILVER.TRIP_DATA_CSV
) t
GROUP BY table_name;
```

### Step 8: Generate Quality Report

CREATE a comprehensive quality report:

```markdown
# Data Quality Report: {TABLE_NAME}
**Generated:** {timestamp}
**Table:** {schema.table}
**Total Records:** {count}

## Quality Summary

| Dimension | Status | Pass Rate | Issues Found |
|-----------|--------|-----------|--------------|
| Completeness | ✅ PASS | 99.8% | 20 nulls in optional fields |
| Validity | ⚠️ WARNING | 99.2% | 80 invalid dates |
| Consistency | ✅ PASS | 100% | 0 orphan records |
| Uniqueness | ✅ PASS | 100% | 0 duplicates |
| Accuracy | ⚠️ WARNING | 98.5% | 150 outliers detected |
| Timeliness | ✅ PASS | - | Last loaded 2 hours ago |

## Detailed Findings

### Completeness Issues
- **trip_id**: 0 nulls (100% complete) ✅
- **fare_amount**: 20 nulls (99.998% complete) ✅
- **pickup_datetime**: 0 nulls (100% complete) ✅

### Validity Issues
- **fare_amount**: 5 negative values found ❌
  - Sample: -10.50, -5.00
- **trip_date**: 80 invalid date formats ❌
  - Sample: "2023-13-45", "NA", "Unknown"

### Accuracy Issues
- **fare_amount outliers**: 150 records with z-score > 3
  - Sample values: $15,000, $12,500, $10,800

## Recommendations

1. **Immediate Action:**
   - Reject or correct 5 negative fare amounts
   - Fix 80 invalid date formats

2. **Investigation:**
   - Review 150 outlier fare amounts (may be valid luxury trips)
   - Verify data source quality

3. **Prevention:**
   - Add validation in Silver transformation
   - Implement range checks at ingestion

## Quality Metrics

- **Overall Quality Score**: 98.9%
- **Critical Issues**: 85
- **Warnings**: 150
- **Pass Rate**: Acceptable (> 95% threshold)
```

## Output

GENERATE:
1. **Quality Report** (Markdown)
2. **SQL Validation Scripts**
3. **Issue Details** (CSV with all violations)
4. **Quality Metrics Dashboard** (Summary stats)

## Quality Checklist

- ✅ Completeness validated (nulls, missing values)
- ✅ Validity checked (types, formats, ranges)
- ✅ Consistency verified (cross-table, internal logic)
- ✅ Uniqueness confirmed (no duplicates)
- ✅ Accuracy assessed (outliers, business rules)
- ✅ Timeliness evaluated (data freshness)
- ✅ Issues documented with examples
- ✅ Recommendations provided
- ✅ Thresholds compared against standards

## Completion

Validation is complete when:
- All quality dimensions checked
- Issues identified and documented
- Quality score calculated
- Actionable recommendations provided
- Report generated and reviewed
