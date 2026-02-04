---
task: profile-data-sources
version: 1.0
elicit: true
description: Analyze source data files to determine proper data types and quality characteristics
---

# Profile Data Sources

## Purpose
Analyze source data files to understand their structure, data types, quality issues, and characteristics before designing the pipeline.

## Process

### Step 1: Gather File Information
ASK the user:

1. **File Location:** Where are the source files?
2. **File Format:** CSV, Parquet, JSON, TSV, etc.?
3. **Sample Available:** Can we access a sample of the data?
4. **Expected Schema:** Do you have a data dictionary?

### Step 2: Load Sample Data

**For CSV/TSV:**
```sql
-- Load sample into temp table
CREATE TEMP TABLE temp_sample AS
SELECT * FROM read_csv('{file_path}', auto_detect=true)
LIMIT 10000;
```

**For Parquet:**
```python
import pandas as pd
df_sample = pd.read_parquet('{file_path}', nrows=10000)
```

**For JSON:**
```python
import json
with open('{file_path}') as f:
    data = [json.loads(line) for line in f.readlines()[:10000]]
```

### Step 3: Analyze Column Characteristics

For each column, determine:

**Data Type Detection:**
```sql
SELECT 
    column_name,
    -- Check if numeric
    SUM(CASE WHEN column ~ '^[0-9]+$' THEN 1 ELSE 0 END) as numeric_count,
    -- Check if decimal
    SUM(CASE WHEN column ~ '^[0-9]+\.[0-9]+$' THEN 1 ELSE 0 END) as decimal_count,
    -- Check if date
    SUM(CASE WHEN TRY_CAST(column AS DATE) IS NOT NULL THEN 1 ELSE 0 END) as date_count,
    -- Check if boolean
    SUM(CASE WHEN column IN ('true', 'false', '0', '1') THEN 1 ELSE 0 END) as bool_count,
    COUNT(*) as total_count,
    COUNT(DISTINCT column) as distinct_count,
    SUM(CASE WHEN column IS NULL OR column = '' THEN 1 ELSE 0 END) as null_count,
    MIN(LENGTH(column)) as min_length,
    MAX(LENGTH(column)) as max_length,
    AVG(LENGTH(column))::INT as avg_length
FROM temp_sample;
```

**PySpark Profiling:**
```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

def profile_column(df, col_name):
    return df.agg(
        F.count(col_name).alias('count'),
        F.countDistinct(col_name).alias('distinct'),
        F.sum(F.when(F.col(col_name).isNull(), 1).otherwise(0)).alias('nulls'),
        F.min(F.length(col_name)).alias('min_len'),
        F.max(F.length(col_name)).alias('max_len'),
        F.avg(F.length(col_name)).alias('avg_len')
    ).collect()[0]

# Profile all columns
for col in df.columns:
    stats = profile_column(df, col)
    print(f"{col}: {stats}")
```

### Step 4: Determine Recommended Data Types

**Decision Logic:**

| Characteristic | Recommended Type |
|----------------|------------------|
| All numeric, no decimals, < 2B | INT |
| All numeric, no decimals, > 2B | BIGINT |
| Numeric with decimals | DECIMAL(p,s) |
| Floating point needed | FLOAT/DOUBLE |
| Valid dates (>90% parseable) | DATE |
| Valid timestamps | TIMESTAMP |
| True/False/0/1 | BOOLEAN |
| Low cardinality (<50 values) | VARCHAR(n) with CHECK constraint |
| High cardinality text | VARCHAR(max_length * 1.2) |
| Very long text | TEXT |

### Step 5: Identify Data Quality Issues

**Check for:**
```sql
-- Nulls
SELECT 
    '{column}' as column_name,
    COUNT(*) as null_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM temp_sample), 2) as null_pct
FROM temp_sample
WHERE {column} IS NULL OR {column} = '';

-- Outliers (numeric columns)
SELECT 
    '{column}' as column_name,
    MIN({column}::NUMERIC) as min_val,
    MAX({column}::NUMERIC) as max_val,
    AVG({column}::NUMERIC) as avg_val,
    STDDEV({column}::NUMERIC) as stddev
FROM temp_sample
WHERE {column} ~ '^[0-9.]+$';

-- Invalid formats
SELECT 
    '{column}' as column_name,
    {column} as invalid_value,
    COUNT(*) as occurrence_count
FROM temp_sample
WHERE NOT ({validation_condition})
GROUP BY {column}
ORDER BY occurrence_count DESC
LIMIT 10;
```

### Step 6: Generate Profile Report

CREATE a markdown report:

```markdown
# Data Profile: {SOURCE_NAME}

## File Information
- **Format:** CSV
- **Size:** 100 MB
- **Row Count:** 1,000,000
- **Column Count:** 15

## Column Analysis

### Column: trip_id
- **Current Type:** VARCHAR
- **Recommended Type:** BIGINT
- **Rationale:** All values numeric, no nulls
- **Statistics:**
  - Distinct Count: 1,000,000 (100% unique)
  - Null Count: 0 (0%)
  - Min Value: 1
  - Max Value: 1000000
- **Quality Issues:** None

### Column: fare_amount
- **Current Type:** VARCHAR
- **Recommended Type:** DECIMAL(10,2)
- **Rationale:** Numeric with 2 decimal places
- **Statistics:**
  - Min: 0.00
  - Max: 999.99
  - Avg: 15.47
  - Null Count: 50 (0.005%)
- **Quality Issues:** 
  - 50 null values
  - 3 negative values found
  - 2 values > 500 (potential outliers)

### Column: trip_date
- **Current Type:** VARCHAR
- **Recommended Type:** DATE
- **Rationale:** 99.8% parseable as date
- **Statistics:**
  - Format: YYYY-MM-DD
  - Min Date: 2020-01-01
  - Max Date: 2023-12-31
  - Null Count: 100 (0.01%)
- **Quality Issues:**
  - 2000 invalid date formats (0.2%)
  - Need to handle: "2023-13-45", "NA", "Unknown"

## Data Quality Summary

| Issue Type | Count | Percentage |
|------------|-------|------------|
| Null Values | 1,250 | 0.08% |
| Invalid Formats | 2,003 | 0.13% |
| Outliers | 15 | 0.001% |
| Duplicates | 0 | 0% |

## Recommendations

1. **Landing Table:** Use VARCHAR for all columns
2. **Silver Table:** Apply recommended types with quality checks
3. **Quality Rules:**
   - Reject records with null trip_id
   - Flag fare_amount < 0 or > 500
   - Parse trip_date with error handling
4. **Expected Reject Rate:** ~0.2% (2,000 records)
```

## Output

PRODUCE:
1. **Data Profile Report** (Markdown)
2. **Recommended Schema** (DDL)
3. **Quality Check Queries** (SQL)
4. **Statistics Summary** (CSV/Table)

## Completion

Profiling is complete when:
- ✅ All columns analyzed
- ✅ Data types recommended with rationale
- ✅ Quality issues identified
- ✅ Sample statistics captured
- ✅ Profile report generated
- ✅ Recommendations documented
