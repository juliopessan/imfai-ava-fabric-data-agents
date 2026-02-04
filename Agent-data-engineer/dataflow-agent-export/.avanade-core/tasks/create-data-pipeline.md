---
task: create-data-pipeline
version: 1.0
elicit: true
description: Design and implement a complete data ingestion pipeline with Landing, Silver, and Gold layers
---

# Create Data Pipeline

## Purpose
Design a complete end-to-end data pipeline including ingestion, transformation, quality checks, and aggregation following Medallion Architecture principles.

## Process

### Step 1: Gather Requirements
ASK the user for the following information:

1. **Data Sources**: What files/formats will be ingested? (CSV, Parquet, JSON, TSV, etc.)
2. **Source Schema**: What columns exist in each source?
3. **Business Rules**: Any specific transformation or validation rules?
4. **Target Tables**: Desired output table names and purposes
5. **Aggregations**: Any summary/aggregation requirements?
6. **Technology Stack**: SQL, PySpark, or both?
7. **Schedule**: Batch frequency (daily, monthly, etc.)?

### Step 2: Design Pipeline Architecture

CREATE a pipeline design covering:

**Landing Layer (Bronze)**
- Raw ingestion tables with VARCHAR columns
- Preserve source data exactly as received
- Table naming: `LND.{SOURCE_NAME}`

**Silver Layer**
- Typed and validated data
- Data quality checks applied
- Reject handling for invalid records
- Table naming: `SILVER.{SOURCE_NAME}`

**Gold Layer**
- Business-ready datasets
- Denormalized/joined data
- Aggregations and summaries
- Table naming: `GOLD.{PURPOSE}`

### Step 3: Generate Artifacts

PRODUCE the following deliverables:

1. **DDL Scripts** (SQL)
   - Landing table definitions
   - Silver table definitions (with proper types)
   - Gold table definitions
   - Reference table definitions

2. **Data Load Scripts** (SQL and/or PySpark)
   - Landing ingestion logic
   - Silver transformation logic
   - Gold business logic
   - Reference data loading

3. **Data Quality Checks**
   - Type validation
   - Null checks
   - Range validation
   - Business rule validation

4. **Unit Tests**
   - Row count validation
   - Data comparison tests
   - Aggregation verification
   - Schema validation

### Step 4: Document Pipeline

CREATE documentation including:
- Architecture diagram (text-based)
- Data flow description
- Table relationships
- Execution order
- Monitoring approach

## Output Structure

```
data-pipeline/
├── ddl/
│   ├── 01-landing-tables.sql
│   ├── 02-silver-tables.sql
│   ├── 03-gold-tables.sql
│   └── 04-reference-tables.sql
├── etl/
│   ├── sql/
│   │   ├── load-landing.sql
│   │   ├── transform-silver.sql
│   │   └── build-gold.sql
│   └── pyspark/
│       ├── load_landing.py
│       ├── transform_silver.py
│       └── build_gold.py
├── tests/
│   ├── unit-tests.sql
│   └── validation-tests.sql
└── docs/
    └── pipeline-design.md
```

## Quality Standards

- All Landing tables use VARCHAR for initial load
- Silver tables have proper data types (derived from profiling)
- Gold tables are optimized for query performance
- Every transformation has corresponding unit tests
- Error handling and logging included
- Scripts are idempotent (re-runnable)

## Completion

Pipeline is complete when:
- ✅ All DDL scripts generated and documented
- ✅ All ETL scripts created in requested language(s)
- ✅ Data quality checks implemented
- ✅ Unit tests cover all transformations
- ✅ Documentation explains design decisions
