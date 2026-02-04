# Data Engineering Best Practices

## Medallion Architecture

### Bronze/Landing Layer
**Purpose:** Raw data ingestion, exactly as received from source

**Principles:**
- All columns as VARCHAR to prevent type conversion failures
- Preserve original data without any transformations
- Include metadata: load_timestamp, source_file
- Never delete or modify raw data
- Idempotent loads (can be rerun safely)

**Example:**
```sql
CREATE TABLE LND.TRIP_DATA (
    col1 VARCHAR(500),
    col2 VARCHAR(500),
    col3 VARCHAR(500),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(500)
);
```

### Silver Layer
**Purpose:** Cleaned, validated, and typed data

**Principles:**
- Proper data types derived from profiling
- Data quality checks applied
- Rejects captured, not discarded
- Quality flags assigned (VALID/INVALID)
- Add processing metadata

**Example:**
```sql
CREATE TABLE SILVER.TRIP_DATA (
    trip_id INT NOT NULL,
    fare_amount DECIMAL(10,2),
    trip_date DATE NOT NULL,
    quality_flag VARCHAR(50) NOT NULL,
    processed_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Gold Layer
**Purpose:** Business-ready, denormalized, aggregated data

**Principles:**
- Optimized for specific use cases
- Denormalized for query performance
- Only includes validated data
- Enriched with reference data
- Aggregated where needed

**Example:**
```sql
CREATE TABLE GOLD.TRIP_SUMMARY (
    location_id INT,
    location_name VARCHAR(200),
    total_trips BIGINT,
    total_fare DECIMAL(18,2),
    avg_fare DECIMAL(10,2),
    created_timestamp TIMESTAMP
);
```

## Data Quality

### Validation Strategy
1. **Type Validation:** Ensure data can be cast to target type
2. **Range Validation:** Check numeric/date ranges
3. **NULL Validation:** Enforce NOT NULL constraints
4. **Referential Integrity:** Validate foreign keys
5. **Business Rules:** Apply domain-specific rules

### Reject Handling
```sql
-- Capture rejects with context
INSERT INTO REJECT.TRIP_DATA_REJECTS
SELECT 
    ROW_TO_JSON(lnd.*) as original_data,
    'Invalid fare amount: ' || lnd.fare_amount as error_message,
    CURRENT_TIMESTAMP as error_timestamp,
    lnd.source_file
FROM LND.TRIP_DATA lnd
WHERE TRY_CAST(lnd.fare_amount AS DECIMAL) IS NULL;
```

## Performance Optimization

### Indexing Strategy
- Index foreign key columns
- Index columns in JOIN conditions
- Index columns in WHERE clauses
- Avoid over-indexing (slows inserts)

### Partitioning
```sql
-- Partition by date for time-series data
CREATE TABLE SILVER.TRIP_DATA (
    trip_date DATE,
    ...
) PARTITION BY RANGE (trip_date);
```

### Query Optimization
- Use column pruning (select only needed columns)
- Predicate pushdown (filter early)
- Broadcast small tables in joins
- Use EXPLAIN to analyze plans

## Testing Standards

### Row Count Tests
```sql
-- Compare source file to table
SELECT 
    (SELECT COUNT(*) FROM external_file) as file_count,
    (SELECT COUNT(*) FROM LND.table) as table_count,
    CASE WHEN file_count = table_count THEN 'PASS' ELSE 'FAIL' END;
```

### Aggregation Tests
```sql
-- Validate SUM calculations
SELECT 
    GROUP_COL,
    SUM(amount) as expected,
    (SELECT SUM(amount) FROM GOLD.table WHERE group_col = s.group_col) as actual,
    CASE WHEN ABS(expected - actual) < 0.01 THEN 'PASS' ELSE 'FAIL' END
FROM SILVER.table s
GROUP BY GROUP_COL;
```

## Idempotency

### Truncate and Load
```sql
-- Safe for small tables
TRUNCATE TABLE SILVER.table;
INSERT INTO SILVER.table SELECT ...;
```

### Merge/Upsert
```sql
-- Safe for incremental loads
MERGE INTO SILVER.table t
USING staging s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

## Error Handling

### Try-Catch in SQL
```sql
BEGIN TRY
    INSERT INTO SILVER.table ...
END TRY
BEGIN CATCH
    INSERT INTO AUDIT.error_log 
    VALUES (ERROR_MESSAGE(), CURRENT_TIMESTAMP);
END CATCH;
```

### PySpark Error Handling
```python
try:
    df.write.mode("overwrite").saveAsTable("SILVER.table")
except Exception as e:
    log_error(f"Pipeline failed: {str(e)}")
    raise
```

## Logging and Monitoring

### Audit Logging
```sql
CREATE TABLE AUDIT.pipeline_log (
    pipeline_name VARCHAR(100),
    stage VARCHAR(50),
    status VARCHAR(20),
    rows_processed INT,
    rows_rejected INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    error_message TEXT
);

-- Log execution
INSERT INTO AUDIT.pipeline_log
VALUES ('TRIP_ETL', 'SILVER', 'SUCCESS', 10000, 5, ...);
```

## File Format Best Practices

### CSV
- Always use header row
- Handle special characters (commas, quotes)
- Specify encoding (UTF-8)
- Use consistent delimiter

### Parquet
- Best for large datasets
- Columnar storage = fast aggregations
- Built-in compression
- Schema embedded

### JSON
- Good for semi-structured data
- Handle nested structures
- Flatten when possible for relational storage

## Naming Conventions

### Tables
- `LND.{SOURCE}_{FORMAT}` - Landing tables
- `SILVER.{SOURCE}_{FORMAT}` - Silver tables
- `GOLD.{PURPOSE}` - Gold tables
- `REF.{ENTITY}` - Reference tables
- `REJECT.{SOURCE}_REJECTS` - Reject tables

### Columns
- lowercase_with_underscores
- Descriptive names (avoid abbreviations)
- Suffix with `_id` for keys
- Suffix with `_date` for dates
- Suffix with `_amt` for amounts

## Version Control

### Script Organization
```
data-pipeline/
├── ddl/
│   ├── 01-create-schemas.sql
│   ├── 02-landing-tables.sql
│   ├── 03-silver-tables.sql
│   └── 04-gold-tables.sql
├── etl/
│   ├── 01-load-landing.sql
│   ├── 02-transform-silver.sql
│   └── 03-build-gold.sql
└── tests/
    └── validate-pipeline.sql
```

### Versioning Strategy
- Use semantic versioning (v1.0.0)
- Tag releases in Git
- Document breaking changes
- Maintain backward compatibility when possible
