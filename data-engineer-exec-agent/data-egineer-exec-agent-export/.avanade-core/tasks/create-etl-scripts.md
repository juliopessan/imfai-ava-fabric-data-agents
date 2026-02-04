---
task: create-etl-scripts
version: 1.0
elicit: true
description: Generate ETL/ELT scripts in SQL or PySpark for data transformation
---

# Create ETL Scripts

## Purpose
Generate data transformation scripts to move data through Landing → Silver → Gold layers with proper validation and quality checks.

## Process

### Step 1: Define Requirements
ASK the user:

1. **Language Preference**: SQL, PySpark, or both?
2. **Source Tables**: Which tables to transform?
3. **Transformation Logic**: Business rules, joins, aggregations
4. **Data Quality Rules**: Validation requirements
5. **Error Handling**: How to handle rejects?

### Step 2: Landing → Silver ETL

**SQL Approach:**
```sql
-- Transform landing to silver with type conversion
INSERT INTO SILVER.{TABLE_NAME}
SELECT 
    CAST(col1 AS INT) as col1,
    CAST(col2 AS DECIMAL(10,2)) as col2,
    CAST(col3 AS DATE) as col3,
    CASE 
        WHEN {validation_check} THEN 'VALID'
        ELSE 'INVALID'
    END as quality_flag,
    CURRENT_TIMESTAMP as processed_timestamp
FROM LND.{TABLE_NAME}
WHERE {optional_filter};
```

**PySpark Approach:**
```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Read landing data
df_landing = spark.table("LND.{TABLE_NAME}")

# Apply transformations and quality checks
df_silver = df_landing \
    .withColumn("col1", F.col("col1").cast(IntegerType())) \
    .withColumn("col2", F.col("col2").cast(DecimalType(10,2))) \
    .withColumn("col3", F.to_date("col3", "yyyy-MM-dd")) \
    .withColumn("quality_flag", 
                F.when(F.col("col1").isNotNull(), "VALID")
                .otherwise("INVALID")) \
    .withColumn("processed_timestamp", F.current_timestamp())

# Write to silver
df_silver.write.mode("overwrite").saveAsTable("SILVER.{TABLE_NAME}")
```

### Step 3: Silver → Gold ETL

**For Joins and Enrichment:**
```sql
-- Build gold table with joins
INSERT INTO GOLD.{TABLE_NAME}
SELECT 
    s.col1,
    s.col2,
    r1.description as col1_desc,
    r2.category as col2_category,
    CURRENT_TIMESTAMP as created_timestamp
FROM SILVER.{TABLE_NAME} s
LEFT JOIN REF.{REF_TABLE_1} r1 ON s.col1 = r1.id
LEFT JOIN REF.{REF_TABLE_2} r2 ON s.col2 = r2.id
WHERE s.quality_flag = 'VALID';
```

**For Aggregations:**
```sql
-- Build aggregated gold table
INSERT INTO GOLD.{AGG_TABLE_NAME}
SELECT 
    group_col,
    COUNT(*) as record_count,
    SUM(amount_col) as total_amount,
    AVG(metric_col) as avg_metric,
    MIN(date_col) as first_date,
    MAX(date_col) as last_date
FROM SILVER.{TABLE_NAME}
WHERE quality_flag = 'VALID'
GROUP BY group_col;
```

### Step 4: Add Error Handling

**Create Reject Table:**
```sql
CREATE TABLE REJECT.{TABLE_NAME}_REJECTS (
    original_data TEXT,
    error_message VARCHAR(1000),
    error_timestamp TIMESTAMP,
    source_file VARCHAR(500)
);
```

**Capture Rejects:**
```sql
INSERT INTO REJECT.{TABLE_NAME}_REJECTS
SELECT 
    ROW_TO_JSON(lnd.*) as original_data,
    'Type conversion failed' as error_message,
    CURRENT_TIMESTAMP as error_timestamp,
    lnd.source_file
FROM LND.{TABLE_NAME} lnd
WHERE NOT {validation_condition};
```

### Step 5: Add Logging and Monitoring

```sql
-- Create audit log table
CREATE TABLE AUDIT.PIPELINE_LOG (
    log_id BIGINT IDENTITY,
    pipeline_name VARCHAR(100),
    stage VARCHAR(50),
    status VARCHAR(20),
    records_processed INT,
    records_rejected INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    error_message TEXT
);

-- Log execution
INSERT INTO AUDIT.PIPELINE_LOG 
VALUES ('TRIP_DATA_ETL', 'SILVER', 'SUCCESS', 1000, 5, ...);
```

## Output Structure

```
etl/
├── sql/
│   ├── 01-load-landing.sql
│   ├── 02-transform-to-silver.sql
│   ├── 03-build-gold-enriched.sql
│   ├── 04-build-gold-aggregated.sql
│   └── 99-handle-rejects.sql
└── pyspark/
    ├── load_landing.py
    ├── transform_to_silver.py
    ├── build_gold_enriched.py
    └── build_gold_aggregated.py
```

## Quality Standards

- ✅ All type conversions handled safely
- ✅ NULL handling explicit
- ✅ Quality flags assigned
- ✅ Rejects captured, not lost
- ✅ Idempotent (re-runnable)
- ✅ Logging and audit trail
- ✅ Performance optimized (partition pruning, broadcast joins)
- ✅ Clear comments explaining logic

## Completion

ETL is complete when:
- Scripts move data Landing → Silver → Gold
- Data quality checks implemented
- Error handling captures rejects
- Logging tracks execution
- Scripts tested and validated
