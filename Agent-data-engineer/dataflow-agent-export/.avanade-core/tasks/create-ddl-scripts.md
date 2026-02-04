---
task: create-ddl-scripts
version: 1.0
elicit: true
description: Generate SQL DDL scripts for Landing, Silver, and Gold tables
---

# Create DDL Scripts

## Purpose
Generate comprehensive DDL (Data Definition Language) scripts for creating database tables across all pipeline layers.

## Process

### Step 1: Gather Schema Information
ASK the user:

1. **Source Files**: What files will be ingested?
2. **Column Details**: Column names and sample data
3. **Database Platform**: SQL Server, PostgreSQL, Databricks SQL, etc.?
4. **Schema Names**: Landing, Silver, Gold schema names

### Step 2: Analyze Data Types

For each source file:
- **Landing**: All columns as VARCHAR (max length)
- **Silver**: Derive proper types from data profiling
  - Numeric: INT, BIGINT, DECIMAL, FLOAT
  - Date/Time: DATE, TIMESTAMP, DATETIME
  - Text: VARCHAR(n), TEXT
  - Boolean: BOOLEAN, BIT

### Step 3: Generate DDL Scripts

CREATE separate SQL files:

**01-landing-tables.sql**
```sql
-- Landing tables with VARCHAR columns
CREATE TABLE IF NOT EXISTS LND.{TABLE_NAME} (
    {columns with VARCHAR types},
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(500)
);
```

**02-silver-tables.sql**
```sql
-- Silver tables with proper data types
CREATE TABLE IF NOT EXISTS SILVER.{TABLE_NAME} (
    {columns with correct types},
    quality_flag VARCHAR(50),
    processed_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**03-gold-tables.sql**
```sql
-- Gold tables optimized for queries
CREATE TABLE IF NOT EXISTS GOLD.{TABLE_NAME} (
    {business-ready columns},
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**04-reference-tables.sql**
```sql
-- Reference/dimension tables
CREATE TABLE IF NOT EXISTS REF.{TABLE_NAME} (
    {reference columns}
);
```

### Step 4: Add Indexes and Constraints

For each table:
- Primary keys
- Foreign keys (where applicable)
- Indexes on frequently queried columns
- Unique constraints
- Check constraints

### Step 5: Add Comments

Document each table and column:
```sql
COMMENT ON TABLE schema.table_name IS 'Purpose description';
COMMENT ON COLUMN schema.table_name.column_name IS 'Column description';
```

## Output

Generate DDL scripts with:
- DROP statements (optional, with IF EXISTS)
- CREATE TABLE statements
- Index creation
- Constraint definitions
- Column comments
- Execution notes

## Quality Checklist

- ✅ All tables follow naming conventions
- ✅ Landing uses VARCHAR for all business columns
- ✅ Silver has appropriate data types
- ✅ Gold is denormalized and query-optimized
- ✅ Audit columns included (timestamps, flags)
- ✅ Indexes on join/filter columns
- ✅ Scripts are idempotent
- ✅ Clear comments on each object
