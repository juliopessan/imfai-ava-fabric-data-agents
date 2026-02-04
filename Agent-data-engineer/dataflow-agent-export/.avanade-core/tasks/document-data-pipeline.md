---
task: document-data-pipeline
version: 1.0
elicit: false
description: Generate comprehensive documentation for a data pipeline
---

# Document Data Pipeline

## Purpose
Create complete documentation for a data pipeline including architecture, data flow, tables, transformations, and operational procedures.

## Process

### Step 1: Load Template
LOAD the template `data-pipeline-tmpl.yaml` as the base structure.

### Step 2: Gather Information

Collect the following details:
- Pipeline name and purpose
- Data sources (files, tables, APIs)
- Table definitions (Landing, Silver, Gold)
- Transformation logic
- Data quality rules
- Execution order
- Error handling approach
- Testing strategy
- Performance metrics
- Dependencies

### Step 3: Document Architecture

CREATE an architecture diagram (text-based):

```
Data Flow Architecture:

[CSV Files]      [Parquet Files]    [JSON Files]
     ↓                  ↓                 ↓
[File Storage / S3 / Azure Blob / Local]
     ↓                  ↓                 ↓
═══════════════════════════════════════════════
     LANDING LAYER (Bronze - Raw Data)
═══════════════════════════════════════════════
     ↓                  ↓                 ↓
LND.TRIP_CSV    LND.TRIP_PARQUET   LND.REF_JSON
(All VARCHAR)    (All VARCHAR)    (All VARCHAR)
     ↓                  ↓                 ↓
═══════════════════════════════════════════════
  SILVER LAYER (Validated & Typed Data)
═══════════════════════════════════════════════
     ↓                  ↓                 ↓
SILVER.TRIP_CSV  SILVER.TRIP_PARQUET  REF.RATE_CODE
(Proper Types)   (Proper Types)       (Proper Types)
(Quality Checks) (Quality Checks)     (Reference)
     ↓                  ↓                 ↓
═══════════════════════════════════════════════
     GOLD LAYER (Business Ready Data)
═══════════════════════════════════════════════
     ↓                             ↓
GOLD.TRIP_ENRICHED           GOLD.TRIP_AGG
(Joined/Enriched)            (Aggregated)
     ↓                             ↓
[BI Tools / Reports / Analytics]
```

### Step 4: Document Tables

For each table, document:

```markdown
### SILVER.TRIP_DATA_CSV

**Purpose:** Validated trip data from CSV files with proper data types

**Source:** LND.TRIP_DATA_CSV

**Schema:**
| Column | Type | Nullable | Description | Validation Rule |
|--------|------|----------|-------------|-----------------|
| trip_id | BIGINT | NO | Unique trip identifier | Must be positive |
| vendor_id | INT | NO | Vendor identifier | 1-9 |
| pickup_datetime | TIMESTAMP | NO | Trip start time | Valid timestamp |
| fare_amount | DECIMAL(10,2) | YES | Trip fare | >= 0 |
| passenger_count | INT | YES | Number of passengers | 1-6 |
| quality_flag | VARCHAR(50) | NO | Data quality indicator | VALID/INVALID |

**Data Quality Rules:**
1. trip_id must be unique and positive
2. vendor_id must be between 1 and 9
3. pickup_datetime must be valid timestamp
4. fare_amount must be >= 0 (if not null)
5. passenger_count must be 1-6 (if not null)

**Transformation Logic:**
```sql
INSERT INTO SILVER.TRIP_DATA_CSV
SELECT 
    CAST(trip_id AS BIGINT) as trip_id,
    CAST(vendor_id AS INT) as vendor_id,
    CAST(pickup_datetime AS TIMESTAMP) as pickup_datetime,
    CAST(fare_amount AS DECIMAL(10,2)) as fare_amount,
    CAST(passenger_count AS INT) as passenger_count,
    CASE 
        WHEN trip_id ~ '^[0-9]+$' 
         AND vendor_id::INT BETWEEN 1 AND 9
         AND TRY_CAST(pickup_datetime AS TIMESTAMP) IS NOT NULL
         AND (fare_amount IS NULL OR fare_amount::NUMERIC >= 0)
        THEN 'VALID'
        ELSE 'INVALID'
    END as quality_flag,
    CURRENT_TIMESTAMP as processed_timestamp
FROM LND.TRIP_DATA_CSV;
```

**Indexes:**
- Primary Key: trip_id
- Index: pickup_datetime (for date range queries)
- Index: vendor_id (for filtering)

**Expected Volume:** 1M rows/month
**Growth Rate:** 10% annually
```

### Step 5: Document Data Flow

For each transformation:

```markdown
## Transformation: Landing → Silver (TRIP_DATA_CSV)

**Input:** LND.TRIP_DATA_CSV (VARCHAR columns)
**Output:** SILVER.TRIP_DATA_CSV (Typed columns)

**Process:**
1. Cast each column to target data type
2. Apply validation rules
3. Assign quality_flag (VALID/INVALID)
4. Capture rejects in REJECT.TRIP_DATA_CSV_REJECTS
5. Add processed_timestamp

**Execution Command:**
```bash
psql -d database -f etl/02-transform-to-silver.sql
```

**Expected Duration:** 5 minutes for 1M rows

**Success Criteria:**
- Row count matches Landing (minus rejects)
- All VALID records have proper types
- Reject rate < 1%
- No duplicate trip_ids
```

### Step 6: Document Testing

```markdown
## Unit Tests

### Test 1: Row Count Validation
**Purpose:** Ensure all records from file are loaded to Landing
**Query:** `tests/01-row-count-tests.sql`
**Expected:** File count = LND table count
**Status:** ✅ PASS (1,000,000 = 1,000,000)

### Test 2: Type Conversion
**Purpose:** Validate Silver table has correct data types
**Query:** `tests/02-schema-validation-tests.sql`
**Expected:** All columns match schema definition
**Status:** ✅ PASS

### Test 3: Aggregation Accuracy
**Purpose:** Verify Gold aggregations match source
**Query:** `tests/06-aggregation-tests.sql`
**Expected:** SUM/COUNT matches between Silver and Gold
**Status:** ✅ PASS (Variance < 0.01%)
```

### Step 7: Document Operational Procedures

```markdown
## Deployment Procedure

### Prerequisites
- Database access granted
- File storage access configured
- Dependencies deployed (reference tables)

### Deployment Steps
1. **Deploy DDL:**
   ```bash
   psql -d database -f ddl/01-landing-tables.sql
   psql -d database -f ddl/02-silver-tables.sql
   psql -d database -f ddl/03-gold-tables.sql
   ```

2. **Deploy ETL:**
   ```bash
   cp etl/*.sql /pipeline/scripts/
   ```

3. **Execute Smoke Test:**
   ```bash
   psql -d database -f tests/99-run-all-tests.sql
   ```

## Troubleshooting

### Issue: High Reject Rate
**Symptom:** More than 1% of records flagged as INVALID
**Diagnosis:** Check REJECT.{TABLE}_REJECTS for error patterns
**Resolution:** 
1. Review error_message column in rejects table
2. Identify common patterns
3. Update source data or adjust validation rules
4. Reprocess rejected records

### Issue: Performance Degradation
**Symptom:** Pipeline taking longer than expected
**Diagnosis:** Check query execution plans
**Resolution:**
1. Update statistics: `ANALYZE table_name;`
2. Rebuild indexes if needed
3. Consider partitioning large tables
4. Review and optimize JOIN operations
```

## Output

GENERATE:
- Complete pipeline documentation (Markdown)
- Architecture diagram (ASCII art or Mermaid)
- Table specifications
- Data flow descriptions
- Testing documentation
- Operational procedures
- Troubleshooting guide

## Completion

Documentation is complete when:
- ✅ All sections filled in
- ✅ Architecture clearly explained
- ✅ All tables documented
- ✅ Transformations described
- ✅ Tests documented
- ✅ Operational procedures complete
- ✅ Troubleshooting guide included
