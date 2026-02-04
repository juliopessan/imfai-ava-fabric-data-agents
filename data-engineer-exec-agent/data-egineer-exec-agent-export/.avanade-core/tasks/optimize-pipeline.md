---
task: optimize-pipeline
version: 1.0
elicit: true
description: Analyze and optimize data pipeline performance
---

# Optimize Data Pipeline

## Purpose
Analyze pipeline performance bottlenecks and implement optimizations to improve speed, reduce costs, and enhance scalability.

## Process

### Step 1: Gather Performance Baseline
ASK the user:

1. **Current Performance**: How long does the pipeline take?
2. **Data Volumes**: How much data is processed?
3. **Pain Points**: Where are the slowdowns?
4. **Target Goals**: What are the performance targets?
5. **Infrastructure**: SQL Server, PostgreSQL, Databricks, etc.?

### Step 2: Analyze Query Performance

**SQL Query Analysis:**
```sql
-- Get query execution plans
EXPLAIN ANALYZE
SELECT ... FROM SILVER.TRIP_DATA
JOIN REF.RATE_CODE ON ...;

-- Check slow queries (PostgreSQL)
SELECT 
    query,
    calls,
    total_exec_time / 1000 as total_seconds,
    mean_exec_time / 1000 as avg_seconds,
    max_exec_time / 1000 as max_seconds
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Unused indexes
ORDER BY schemaname, tablename;
```

**PySpark Performance:**
```python
# Enable query execution time tracking
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Explain physical plan
df.explain(mode="formatted")

# Check partition information
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Identify skewed data
df.groupBy("partition_key").count().orderBy(F.desc("count")).show()
```

### Step 3: Indexing Optimization

**Identify Missing Indexes:**
```sql
-- Find tables without indexes on foreign keys
SELECT 
    t.table_name,
    c.column_name,
    'Missing index on FK' as recommendation
FROM information_schema.table_constraints t
JOIN information_schema.constraint_column_usage c 
    ON t.constraint_name = c.constraint_name
WHERE t.constraint_type = 'FOREIGN KEY'
  AND NOT EXISTS (
    SELECT 1 FROM pg_indexes i
    WHERE i.tablename = t.table_name
      AND i.indexdef LIKE '%' || c.column_name || '%'
  );
```

**Create Strategic Indexes:**
```sql
-- Index for JOIN operations
CREATE INDEX idx_trip_rate_code 
ON SILVER.TRIP_DATA(rate_code_id);

-- Composite index for common queries
CREATE INDEX idx_trip_date_vendor 
ON SILVER.TRIP_DATA(trip_date, vendor_id);

-- Partial index for filtered queries
CREATE INDEX idx_valid_trips 
ON SILVER.TRIP_DATA(trip_id) 
WHERE quality_flag = 'VALID';

-- Include columns for covering index
CREATE INDEX idx_trip_covering 
ON SILVER.TRIP_DATA(pickup_location_id) 
INCLUDE (fare_amount, trip_distance);
```

### Step 4: Partitioning Strategy

**Implement Table Partitioning:**
```sql
-- Range partitioning by date (PostgreSQL)
CREATE TABLE SILVER.TRIP_DATA (
    trip_id BIGINT,
    trip_date DATE,
    ...
) PARTITION BY RANGE (trip_date);

CREATE TABLE SILVER.TRIP_DATA_2023 
    PARTITION OF SILVER.TRIP_DATA
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE SILVER.TRIP_DATA_2024
    PARTITION OF SILVER.TRIP_DATA
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

**PySpark Partitioning:**
```python
# Repartition for better parallelism
df_optimized = df.repartition(200, "partition_key")

# Partition by column when writing
df.write \
    .partitionBy("year", "month") \
    .parquet("path/to/output")

# Coalesce for fewer output files
df.coalesce(10).write.parquet("path/to/output")
```

### Step 5: Query Optimization

**Rewrite Inefficient Queries:**

**Before (Inefficient):**
```sql
-- Slow: Multiple subqueries
SELECT 
    t.*,
    (SELECT rate_desc FROM REF.RATE_CODE WHERE id = t.rate_code_id) as rate,
    (SELECT payment_desc FROM REF.PAYMENT_TYPE WHERE id = t.payment_type) as payment
FROM SILVER.TRIP_DATA t;
```

**After (Optimized):**
```sql
-- Fast: Single JOIN
SELECT 
    t.*,
    r.rate_desc,
    p.payment_desc
FROM SILVER.TRIP_DATA t
LEFT JOIN REF.RATE_CODE r ON t.rate_code_id = r.rate_code_id
LEFT JOIN REF.PAYMENT_TYPE p ON t.payment_type = p.payment_type_id;
```

**Push Predicates Down:**
```sql
-- Inefficient: Filter after JOIN
SELECT * FROM (
    SELECT t.*, r.rate_desc
    FROM SILVER.TRIP_DATA t
    JOIN REF.RATE_CODE r ON t.rate_code_id = r.rate_code_id
) sub
WHERE trip_date >= '2024-01-01';

-- Efficient: Filter before JOIN
SELECT t.*, r.rate_desc
FROM SILVER.TRIP_DATA t
JOIN REF.RATE_CODE r ON t.rate_code_id = r.rate_code_id
WHERE t.trip_date >= '2024-01-01';
```

### Step 6: Reduce Data Movement

**Minimize Shuffles (PySpark):**
```python
# Broadcast small tables
from pyspark.sql.functions import broadcast

df_result = df_large.join(
    broadcast(df_small),
    "key"
)

# Use bucketing for repeated joins
df.write \
    .bucketBy(50, "join_key") \
    .sortBy("join_key") \
    .saveAsTable("bucketed_table")
```

**Column Pruning:**
```sql
-- Bad: Select all columns
SELECT * FROM SILVER.TRIP_DATA;

-- Good: Select only needed columns
SELECT trip_id, fare_amount, trip_date 
FROM SILVER.TRIP_DATA;
```

### Step 7: Caching and Materialization

**Materialized Views:**
```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW GOLD.TRIP_SUMMARY_MV AS
SELECT 
    pickup_location_id,
    DATE_TRUNC('day', trip_date) as trip_day,
    COUNT(*) as trip_count,
    SUM(fare_amount) as total_fare,
    AVG(fare_amount) as avg_fare
FROM SILVER.TRIP_DATA
WHERE quality_flag = 'VALID'
GROUP BY pickup_location_id, DATE_TRUNC('day', trip_date);

-- Refresh periodically
REFRESH MATERIALIZED VIEW GOLD.TRIP_SUMMARY_MV;
```

**PySpark Caching:**
```python
# Cache frequently accessed DataFrames
df_filtered = df.filter(F.col("quality_flag") == "VALID")
df_filtered.cache()

# Persist with storage level
df.persist(StorageLevel.MEMORY_AND_DISK)

# Don't forget to unpersist
df_filtered.unpersist()
```

### Step 8: Batch vs Incremental Processing

**Implement Incremental Loads:**
```sql
-- Instead of full table reload
INSERT INTO SILVER.TRIP_DATA
SELECT ...
FROM LND.TRIP_DATA;

-- Use incremental processing
INSERT INTO SILVER.TRIP_DATA
SELECT ...
FROM LND.TRIP_DATA
WHERE load_timestamp > (
    SELECT COALESCE(MAX(processed_timestamp), '1900-01-01')
    FROM SILVER.TRIP_DATA
);
```

### Step 9: Statistics and Vacuum

**Maintain Table Statistics:**
```sql
-- PostgreSQL
ANALYZE SILVER.TRIP_DATA;
VACUUM ANALYZE SILVER.TRIP_DATA;

-- SQL Server
UPDATE STATISTICS SILVER.TRIP_DATA WITH FULLSCAN;

-- Databricks
ANALYZE TABLE SILVER.TRIP_DATA COMPUTE STATISTICS;
OPTIMIZE SILVER.TRIP_DATA;
```

### Step 10: File Format Optimization

**Use Columnar Formats:**
```python
# Convert CSV to Parquet
df = spark.read.csv("input.csv", header=True)
df.write.parquet("output.parquet", compression="snappy")

# Use Delta Lake for ACID transactions
df.write.format("delta").save("path/to/delta-table")
```

## Optimization Report

Generate a report:

```markdown
# Pipeline Optimization Report

## Performance Baseline
- **Before Optimization**: 45 minutes
- **After Optimization**: 12 minutes
- **Improvement**: 73% faster

## Optimizations Applied

### 1. Indexing (Impact: -15 minutes)
- ✅ Created index on `rate_code_id` (JOIN column)
- ✅ Created composite index on `trip_date, vendor_id`
- ✅ Created covering index for aggregation query

### 2. Partitioning (Impact: -10 minutes)
- ✅ Partitioned SILVER.TRIP_DATA by trip_date (monthly)
- ✅ Enabled partition pruning on date range queries

### 3. Query Rewrite (Impact: -5 minutes)
- ✅ Replaced correlated subqueries with JOINs
- ✅ Added predicate pushdown for early filtering
- ✅ Eliminated SELECT * patterns

### 4. Materialized Views (Impact: -3 minutes)
- ✅ Created MV for GOLD.TRIP_SUMMARY
- ✅ Scheduled hourly refresh

### 5. Statistics Update (Impact: -2 minutes)
- ✅ Updated table statistics
- ✅ Vacuumed bloated tables

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Runtime | 45 min | 12 min | 73% ↓ |
| Landing Load | 5 min | 3 min | 40% ↓ |
| Silver Transform | 25 min | 6 min | 76% ↓ |
| Gold Creation | 15 min | 3 min | 80% ↓ |
| CPU Usage | 85% | 45% | 47% ↓ |
| Memory Usage | 12 GB | 6 GB | 50% ↓ |
| Cost per Run | $5.00 | $1.50 | 70% ↓ |

## Recommendations

### Immediate
- ✅ All applied

### Short-term
- [ ] Implement incremental processing for large tables
- [ ] Add more partitions as data grows
- [ ] Consider data archival for old data

### Long-term
- [ ] Evaluate migration to columnar storage (Parquet)
- [ ] Consider Delta Lake for ACID guarantees
- [ ] Implement auto-scaling for variable workloads
```

## Output

DELIVER:
1. **Optimization Report** (Markdown)
2. **Optimized SQL Scripts**
3. **Index Creation Scripts**
4. **Performance Benchmarks** (Before/After)
5. **Monitoring Queries** (to track ongoing performance)

## Completion

Optimization is complete when:
- ✅ Performance baseline established
- ✅ Bottlenecks identified
- ✅ Optimizations implemented
- ✅ Performance improvements measured
- ✅ Cost reduction calculated
- ✅ Documentation updated
- ✅ Monitoring in place
