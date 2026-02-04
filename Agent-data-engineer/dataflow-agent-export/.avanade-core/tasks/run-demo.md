---
task: run-demo
version: 1.0
elicit: true
description: Execute interactive demo workflow showcasing all DataFlow agent capabilities
---

# Run Demo Workflow

## Purpose

Execute an interactive demonstration of the DataFlow agent's capabilities using sample NYC Green Taxi data. This demo showcases the complete data engineering workflow from raw data to business-ready analytics.

### Indicative Impact
- **Traditional Approach**: 152 hours (~19 working days) for complete pipeline
- **AI-Assisted Approach**: 21 hours (~2.6 working days)
- **Improvement**: 86% reduction in effort, 7.2x faster delivery

## Demo Scenarios

Present numbered options to user:

```
╔══════════════════════════════════════════════════════════════════╗
║           🔄 DataFlow Agent - Demo Workflow                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Select a demo scenario to execute:                              ║
║                                                                  ║
║  1. 📊 Data Profiling - Analyze NYC Taxi CSV files              ║
║  2. 🏗️  Complete Pipeline - End-to-end data pipeline creation   ║
║  3. 📝 DDL Generation - Create table definitions                ║
║  4. 🔄 ETL Development - Build transformation logic             ║
║  5. ✅ Data Quality - Implement validation framework            ║
║  6. 🧪 Test Creation - Generate unit tests                      ║
║  7. ⚡ Optimization - Performance analysis & tuning             ║
║  8. 📚 Documentation - Generate pipeline documentation          ║
║  9. 📋 Checklist Audit - Production readiness review            ║
║  A. 🚀 FULL DEMO - Run all scenarios sequentially               ║
║                                                                  ║
║  Type a number (1-9) or 'A' for full demo:                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Demo Data Context

**NYC Green Taxi Dataset (April-June 2021)**
- ~785,000 trip records
- Multiple file formats: CSV, Parquet, JSON, TSV
- Reference data: Payment Types, Rate Codes, Trip Types

**Sample Files Available:**
```
Files/
├── green_tripdata_2021-04.csv    # April trips (~262K records)
├── green_tripdata_2021-05.csv    # May trips (~261K records)
├── green_tripdata_2021-06.csv    # June trips (~262K records)
├── payment_type_array.json       # Payment type lookup
├── rate_code.json                # Rate code lookup
├── trip_type.tsv                 # Trip type lookup
└── month=04/, 05/, 06/           # Parquet partitions
```

## Scenario Execution

### Scenario 1: Data Profiling
**Command:** `*profile-data`

Generate comprehensive profile report including:
- Row counts and file sizes
- Column schema detection
- Data type inference
- Null value analysis
- Value distribution statistics
- Data quality observations

**Output:** `data-outputs/profiles/profile_nyc-taxi_YYYY-MM-DD_HHmm.md`

---

### Scenario 2: Complete Pipeline
**Command:** `*create-pipeline`

Create end-to-end Medallion architecture pipeline:
- Landing tables (raw VARCHAR)
- Silver tables (typed, validated)
- Gold tables (enriched, aggregated)
- Reference tables
- ETL scripts for all layers
- Unit tests
- Documentation

**Output:** Full project in `data-outputs/`

---

### Scenario 3: DDL Generation
**Command:** `*create-ddl`

Generate table definitions for:
- `LND.GREEN_TAXI` - Landing layer
- `SILVER.GREEN_TAXI` - Silver layer with types
- `SILVER.GREEN_TAXI_REJECT` - Reject table
- `GOLD.TAXI_TRIPS_ENRICHED` - Enriched data
- `GOLD.TAXI_TRIPS_AGG` - Aggregated metrics
- `REF.PAYMENT_TYPE`, `REF.RATE_CODE`, `REF.TRIP_TYPE`

**Output:** `data-outputs/ddl/`

---

### Scenario 4: ETL Development
**Command:** `*create-etl`

Generate transformation scripts:
- Landing ingestion (CSV, Parquet)
- Silver transformation with validation
- Gold enrichment with JOINs
- Gold aggregation
- Reference data loading

**Output:** `data-outputs/etl/`

---

### Scenario 5: Data Quality
**Command:** `*validate-quality`

Implement quality framework:
- Type validation rules
- NULL checks
- Range validation (fares, distances)
- Referential integrity
- Quality flag assignment
- Reject capture

**Output:** `data-outputs/quality/`

---

### Scenario 6: Test Creation
**Command:** `*create-tests`

Generate test suite:
- Row count validation
- Schema validation
- Data type verification
- Aggregation validation
- Business rule tests

**Output:** `data-outputs/tests/`

---

### Scenario 7: Optimization
**Command:** `*optimize-pipeline`

Performance analysis:
- Index recommendations
- Query optimization
- Partitioning strategy
- Statistics maintenance
- Resource utilization

**Output:** `data-outputs/optimization/`

---

### Scenario 8: Documentation
**Command:** `*document-pipeline`

Generate documentation:
- Architecture overview
- Data flow diagrams
- Table schemas
- ETL logic description
- Execution guide

**Output:** `data-outputs/documentation/`

---

### Scenario 9: Checklist Audit
**Command:** `*execute-checklist`

Production readiness review:
- Pre-development checklist
- DDL verification
- ETL verification
- Quality framework check
- Testing coverage
- Documentation completeness

**Output:** `data-outputs/audits/`

---

### Scenario A: Full Demo
Execute all scenarios in sequence with progress tracking.

## Output Structure Verification

Before generating outputs, verify structure exists:

```
data-outputs/
├── ddl/            # Table definitions
├── etl/            # Transformation scripts
├── tests/          # Unit tests
├── profiles/       # Data profiling reports
├── quality/        # Quality validation
├── documentation/  # Pipeline documentation
├── optimization/   # Performance analysis
└── audits/         # Checklist results
```

## Demo Completion

After demo execution, generate summary report showing:
- Scenarios executed
- Artifacts generated
- AI impact metrics
- Time saved calculations
