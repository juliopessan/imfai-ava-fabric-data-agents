# Data Engineer Agent - Quick Start Guide

## Overview

The **Data Engineer Agent** (🔄 DataFlow) is a specialized AI assistant for building data ingestion pipelines, ETL/ELT processes, and ensuring data quality throughout the data lifecycle.

## When to Use This Agent

Use the Data Engineer agent when you need:
- Design and implement data pipelines (CSV, Parquet, JSON, TSV ingestion)
- Create DDL scripts for database tables
- Build ETL/ELT transformations (SQL or PySpark)
- Implement data quality checks and validation
- Generate unit tests for data pipelines
- Profile data sources to determine optimal data types
- Document data pipeline architecture
- Follow Medallion Architecture (Landing/Silver/Gold)

## Activating the Agent

To activate the Data Engineer agent in your workspace:

```
@workspace /agent data-engineer
```

The agent will:
1. Greet you as "DataFlow"
2. Automatically display available commands (*help)
3. Wait for your instructions

## Available Commands

Type any command with the `*` prefix:

| Command | Description |
|---------|-------------|
| `*help` | Show numbered list of available commands |
| `*create-pipeline` | Design a complete data pipeline (Landing→Silver→Gold) |
| `*create-ddl` | Generate SQL DDL scripts for tables |
| `*create-etl` | Generate ETL/ELT scripts (SQL and/or PySpark) |
| `*create-tests` | Generate unit tests for data validation |
| `*profile-data` | Analyze source files to determine data types |
| `*validate-quality` | Check data quality and identify issues |
| `*optimize-pipeline` | Improve pipeline performance |
| `*document-pipeline` | Create comprehensive pipeline documentation |
| `*execute-checklist` | Run the data engineering checklist |
| `*yolo` | Toggle Yolo Mode (autonomous operation) |
| `*exit` | Exit the Data Engineer agent |

## Example Usage

### Scenario 1: Create Complete Data Pipeline

**Your request:**
```
I need to create a pipeline to ingest monthly trip data from CSV and Parquet files, 
validate the data, and create summary tables.
```

**Agent actions:**
1. Asks for source file details (columns, formats)
2. Designs Landing→Silver→Gold architecture
3. Generates DDL scripts for all tables
4. Creates ETL scripts in SQL and/or PySpark
5. Generates data quality checks
6. Creates unit tests
7. Provides execution documentation

**Agent will use:** `*create-pipeline` task

---

### Scenario 2: Generate DDL Only

**Your request:**
```
Create DDL scripts for a landing table TRIP_DATA_CSV with all VARCHAR columns, 
and a silver table with proper data types.
```

**Agent will use:** `*create-ddl` task

**Output:**
- `01-landing-tables.sql`
- `02-silver-tables.sql`
- Indexes and constraints

---

### Scenario 3: Profile Unknown Data

**Your request:**
```
I have a CSV file with trip data but I'm not sure what data types to use. 
Can you analyze it?
```

**Agent will use:** `*profile-data` task

**Output:**
- Column analysis report
- Recommended data types with rationale
- Data quality issues identified
- Statistics and null counts

---

### Scenario 4: Create Unit Tests

**Your request:**
```
Generate unit tests to validate my TRIP_DATA pipeline - I need to compare 
file counts with table counts and verify aggregations.
```

**Agent will use:** `*create-tests` task

**Output:**
- Row count validation tests
- Schema validation tests
- Aggregation accuracy tests
- Data comparison tests
- Test runner script

---

## Typical Workflow

### End-to-End Pipeline Development

1. **Start with profiling:**
   ```
   *profile-data
   ```
   Analyze your source files to understand data types and quality

2. **Create the pipeline:**
   ```
   *create-pipeline
   ```
   Design complete architecture with all layers

3. **Generate DDL:**
   ```
   *create-ddl
   ```
   Create table definitions for all layers

4. **Generate ETL:**
   ```
   *create-etl
   ```
   Create transformation scripts

5. **Generate tests:**
   ```
   *create-tests
   ```
   Create validation tests

6. **Document:**
   ```
   *document-pipeline
   ```
   Generate comprehensive documentation

7. **Validate with checklist:**
   ```
   *execute-checklist
   ```
   Ensure all best practices followed

## Architecture Principles

The agent follows **Medallion Architecture**:

### 🥉 Landing Layer (Bronze)
- **Purpose:** Raw data ingestion
- **Strategy:** All columns as VARCHAR
- **Naming:** `LND.{SOURCE_NAME}`

### 🥈 Silver Layer
- **Purpose:** Cleaned and typed data
- **Strategy:** Proper data types, quality checks
- **Naming:** `SILVER.{SOURCE_NAME}`

### 🥇 Gold Layer
- **Purpose:** Business-ready data
- **Strategy:** Joined, enriched, aggregated
- **Naming:** `GOLD.{PURPOSE}`

## Key Features

### 1. Multi-Format Support
- CSV (comma-separated)
- Parquet (columnar)
- JSON (structured/semi-structured)
- TSV (tab-separated)
- Avro, ORC, Delta Lake

### 2. Dual Technology Support
- **SQL:** Traditional relational databases
- **PySpark:** Distributed processing at scale

### 3. Data Quality Built-In
- Type validation
- NULL checks
- Range validation
- Business rule enforcement
- Reject handling (no data loss)

### 4. Comprehensive Testing
- Row count validation
- Schema validation
- Transformation accuracy
- Aggregation verification
- File-to-table comparison

## Configuration Files

The agent uses these supporting files:

```
.avanade-core/
├── agents/
│   └── data-engineer.md          ← Agent definition
├── tasks/
│   ├── create-data-pipeline.md   ← Main pipeline creation
│   ├── create-ddl-scripts.md     ← DDL generation
│   ├── create-etl-scripts.md     ← ETL generation
│   ├── create-data-tests.md      ← Test generation
│   ├── profile-data-sources.md   ← Data profiling
│   └── document-data-pipeline.md ← Documentation
├── templates/
│   └── data-pipeline-tmpl.yaml   ← Pipeline template
├── checklists/
│   └── data-engineer-checklist.md ← Quality checklist
└── data/
    └── data-engineering-best-practices.md ← Best practices
```

## Tips for Best Results

### Be Specific with Requirements
**Good:**
```
Create a pipeline for monthly trip data CSV files with columns: 
trip_id, pickup_date, fare_amount, passenger_count. 
Load to LND.TRIP_DATA, transform to SILVER.TRIP_DATA, 
and aggregate by date in GOLD.TRIP_SUMMARY.
```

**Less Good:**
```
Make a data pipeline.
```

### Provide Sample Data
When possible, share:
- Sample rows from source files
- Expected data formats
- Business rules
- Data dictionary

### Specify Technology Preferences
Let the agent know:
- SQL vs PySpark preference
- Database platform (PostgreSQL, SQL Server, Databricks)
- Specific requirements (partitioning, indexes)

## Example: Complete Trip Data Pipeline

**Request:**
```
@workspace /agent data-engineer

I need a complete pipeline for the following requirements:

1. Monthly CSV files with trip data → LND.TRIP_DATA_CSV
2. Monthly Parquet files with trip data → LND.TRIP_DATA_PARQUET
3. TSV file with trip types → REF.TRIP_TYPE
4. JSON file with rate codes → REF.RATE_CODE
5. Transform to Silver with data quality checks
6. Create Gold table joining trip data with reference tables
7. Create Gold aggregate table by location
8. Generate unit tests to validate everything
9. Use both SQL and PySpark

Please start with *create-pipeline.
```

**Agent response:**
The agent will execute the `create-pipeline` task, which will:
1. Ask for detailed column information
2. Design the full architecture
3. Generate all DDL scripts
4. Create ETL scripts in both SQL and PySpark
5. Implement data quality checks
6. Generate comprehensive unit tests
7. Create documentation

## Troubleshooting

### Agent not responding to commands?
- Ensure you use `*` prefix (e.g., `*help`, not `help`)
- Check you've activated the agent first: `@workspace /agent data-engineer`

### Need to change agent behavior?
- Use `*exit` to leave the agent
- Activate a different agent or return to default mode

### Want more autonomous operation?
- Use `*yolo` to toggle autonomous mode
- Agent will make more decisions without asking

## Next Steps

1. **Activate the agent:**
   ```
   @workspace /agent data-engineer
   ```

2. **Start with help:**
   ```
   *help
   ```

3. **Begin your pipeline:**
   ```
   *create-pipeline
   ```

Happy data engineering! 🔄
