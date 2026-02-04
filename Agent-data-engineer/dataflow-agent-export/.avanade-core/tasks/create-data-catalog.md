---
task: create-data-catalog
version: 1.0
elicit: true
description: Create comprehensive data catalog and business glossary for data assets
---

# Create Data Catalog & Data Glossary

## Purpose
Generate a comprehensive data catalog documenting all data assets, their metadata, ownership, and a business glossary defining key terms and metrics used across the organization.

## Process

### Step 1: Gather Catalog Requirements
ASK the user:

1. **Scope**: Which databases/schemas to catalog?
2. **Data Sources**: Tables, views, files, APIs?
3. **Business Domain**: What business areas are covered?
4. **Stakeholders**: Who are the data owners and stewards?
5. **Existing Documentation**: Any existing data dictionaries?

### Step 2: Extract Technical Metadata

**SQL - Extract Table Metadata:**
```sql
-- Get all tables with row counts and sizes
SELECT 
    t.table_schema,
    t.table_name,
    t.table_type,
    (SELECT COUNT(*) FROM information_schema.columns c 
     WHERE c.table_name = t.table_name 
     AND c.table_schema = t.table_schema) as column_count,
    pg_total_relation_size(quote_ident(t.table_schema) || '.' || quote_ident(t.table_name)) as size_bytes,
    obj_description((quote_ident(t.table_schema) || '.' || quote_ident(t.table_name))::regclass) as table_description
FROM information_schema.tables t
WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY t.table_schema, t.table_name;
```

**SQL - Extract Column Metadata:**
```sql
-- Get all columns with detailed metadata
SELECT 
    c.table_schema,
    c.table_name,
    c.column_name,
    c.ordinal_position,
    c.data_type,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale,
    c.is_nullable,
    c.column_default,
    col_description((quote_ident(c.table_schema) || '.' || quote_ident(c.table_name))::regclass, c.ordinal_position) as column_description,
    -- Check if part of primary key
    CASE WHEN pk.column_name IS NOT NULL THEN 'YES' ELSE 'NO' END as is_primary_key,
    -- Check if part of foreign key
    CASE WHEN fk.column_name IS NOT NULL THEN fk.referenced_table ELSE NULL END as references_table
FROM information_schema.columns c
LEFT JOIN (
    SELECT ku.table_schema, ku.table_name, ku.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
    WHERE tc.constraint_type = 'PRIMARY KEY'
) pk ON c.table_schema = pk.table_schema AND c.table_name = pk.table_name AND c.column_name = pk.column_name
LEFT JOIN (
    SELECT 
        ku.table_schema, ku.table_name, ku.column_name,
        ccu.table_name as referenced_table
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
    JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
) fk ON c.table_schema = fk.table_schema AND c.table_name = fk.table_name AND c.column_name = fk.column_name
WHERE c.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY c.table_schema, c.table_name, c.ordinal_position;
```

**PySpark - Extract Metadata:**
```python
from pyspark.sql import SparkSession

def extract_catalog_metadata(spark, database_name):
    """Extract metadata for all tables in a database"""
    catalog_entries = []
    
    # Get all tables
    tables = spark.catalog.listTables(database_name)
    
    for table in tables:
        # Get table details
        table_info = {
            'database': table.database,
            'table_name': table.name,
            'table_type': table.tableType,
            'is_temporary': table.isTemporary
        }
        
        # Get schema details
        df = spark.table(f"{table.database}.{table.name}")
        columns = []
        for field in df.schema.fields:
            columns.append({
                'column_name': field.name,
                'data_type': str(field.dataType),
                'nullable': field.nullable,
                'metadata': field.metadata
            })
        
        table_info['columns'] = columns
        table_info['row_count'] = df.count()
        catalog_entries.append(table_info)
    
    return catalog_entries
```

### Step 3: Create Data Catalog Structure

**Catalog Entry Template:**
```markdown
## {SCHEMA}.{TABLE_NAME}

### Overview
| Attribute | Value |
|-----------|-------|
| **Full Name** | {schema}.{table_name} |
| **Type** | Table / View / External Table |
| **Layer** | Landing / Silver / Gold / Reference |
| **Owner** | {data_owner} |
| **Steward** | {data_steward} |
| **Created** | {creation_date} |
| **Last Updated** | {last_update} |
| **Row Count** | {approximate_rows} |
| **Size** | {size_mb} MB |

### Description
{Business description of what this table represents and its purpose}

### Source Information
| Attribute | Value |
|-----------|-------|
| **Source System** | {source_system_name} |
| **Source Table/File** | {source_identifier} |
| **Load Frequency** | Daily / Hourly / Real-time |
| **SLA** | {sla_hours} hours |

### Schema Definition

| # | Column | Type | Nullable | PK | FK | Description | Business Term |
|---|--------|------|----------|----|----|-------------|---------------|
| 1 | {col1} | {type} | YES/NO | ✓ | → REF.table | {description} | {glossary_term} |
| 2 | {col2} | {type} | YES/NO | | | {description} | {glossary_term} |

### Data Quality Rules
| Rule ID | Column | Rule Type | Rule Description | Threshold |
|---------|--------|-----------|------------------|-----------|
| DQ001 | {col} | NOT NULL | Column must not be null | 100% |
| DQ002 | {col} | RANGE | Value must be between X and Y | 99.9% |

### Relationships
```
{TABLE_NAME}
    ├── FK: column_a → REF.lookup_table.id
    └── FK: column_b → DIM.dimension_table.key
```

### Usage Notes
- **Common Queries**: {typical query patterns}
- **Performance Tips**: {indexing and query recommendations}
- **Known Issues**: {any known data quality issues or limitations}

### Change History
| Date | Change | Author |
|------|--------|--------|
| {date} | Initial creation | {author} |
```

### Step 4: Create Business Glossary

**Glossary Entry Template:**
```markdown
## Business Glossary

### A

#### Active Customer
- **Definition**: A customer who has made at least one purchase in the last 12 months
- **Business Owner**: Marketing Department
- **Calculation**: COUNT(DISTINCT customer_id) WHERE last_purchase_date >= DATEADD(month, -12, CURRENT_DATE)
- **Related Terms**: Customer, Churned Customer, New Customer
- **Used In Tables**: GOLD.customer_summary, GOLD.sales_metrics

#### Average Order Value (AOV)
- **Definition**: The average monetary value of all orders
- **Business Owner**: Finance Department
- **Calculation**: SUM(order_total) / COUNT(DISTINCT order_id)
- **Unit**: Currency (USD)
- **Related Terms**: Order, Revenue, Gross Sales
- **Used In Tables**: GOLD.daily_sales_agg, GOLD.monthly_metrics

### B

#### Business Day
- **Definition**: Any day that is not a Saturday, Sunday, or company holiday
- **Business Owner**: Operations
- **Calculation**: Excludes weekends and dates in REF.holidays table
- **Related Terms**: Calendar Day, Working Day
- **Used In Tables**: REF.calendar, GOLD.operational_metrics
```

### Step 5: Generate Catalog Documentation

**Output Structure:**
```
data-catalog/
├── README.md                    # Catalog overview and navigation
├── catalog/
│   ├── landing/
│   │   ├── LND.TRIP_DATA_CSV.md
│   │   └── LND.TRIP_DATA_PARQUET.md
│   ├── silver/
│   │   ├── SILVER.TRIP_DATA.md
│   │   └── SILVER.CUSTOMER.md
│   ├── gold/
│   │   ├── GOLD.TRIP_ENRICHED.md
│   │   └── GOLD.DAILY_METRICS.md
│   └── reference/
│       ├── REF.RATE_CODE.md
│       └── REF.PAYMENT_TYPE.md
├── glossary/
│   ├── business-glossary.md     # Business terms A-Z
│   └── technical-glossary.md    # Technical terms
├── domains/
│   ├── sales-domain.md          # Sales data domain
│   └── operations-domain.md     # Operations data domain
└── metadata/
    ├── table-inventory.csv      # Machine-readable catalog
    └── column-inventory.csv     # All columns across all tables
```

### Step 6: Create Machine-Readable Exports

**CSV Export - Table Inventory:**
```csv
schema,table_name,table_type,layer,owner,steward,row_count,size_mb,description,source_system,load_frequency
LND,TRIP_DATA_CSV,TABLE,Landing,DataOps,John Doe,785000,150,Raw trip data from CSV files,NYC TLC,Daily
SILVER,TRIP_DATA,TABLE,Silver,DataOps,John Doe,780000,120,Validated trip data with proper types,LND.TRIP_DATA_CSV,Daily
```

**JSON Export - Full Metadata:**
```json
{
  "catalog_version": "1.0",
  "generated_date": "2026-01-26",
  "tables": [
    {
      "schema": "SILVER",
      "name": "TRIP_DATA",
      "type": "TABLE",
      "layer": "Silver",
      "owner": "DataOps",
      "columns": [
        {
          "name": "trip_id",
          "type": "BIGINT",
          "nullable": false,
          "is_pk": true,
          "description": "Unique trip identifier",
          "business_term": "Trip ID"
        }
      ]
    }
  ]
}
```

## Output

Generate the following artifacts:

1. **Data Catalog** (Markdown)
   - Individual table documentation
   - Schema overview pages
   - Relationship diagrams

2. **Business Glossary** (Markdown)
   - Alphabetical term definitions
   - Cross-references to tables

3. **Machine-Readable Exports**
   - table-inventory.csv
   - column-inventory.csv
   - catalog-metadata.json

4. **Catalog Index** (README.md)
   - Navigation structure
   - Quick reference links

## Completion Criteria

Catalog is complete when:
- ✅ All tables documented with full metadata
- ✅ All columns have descriptions
- ✅ Business glossary covers key terms
- ✅ Relationships documented
- ✅ Data owners identified
- ✅ Machine-readable exports generated
