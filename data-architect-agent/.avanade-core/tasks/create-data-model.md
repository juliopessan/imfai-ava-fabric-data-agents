# Create Data Model Task

**Task ID:** create-data-model  
**Agent:** DataArchitect  
**Version:** 1.0

---

## Purpose

Design a comprehensive data model that implements the architecture and supports business requirements with proper dimensional modeling.

---

## Prerequisites

- Architecture document created
- STTM available
- Analytical questions defined
- Technology decisions made

---

## Execution Steps

### Step 1: Review Source Analysis

Analyze:
- Source entities from STTM
- Relationships between sources
- Data types and constraints
- Update patterns

### Step 2: Identify Model Type

Choose appropriate modeling approach:
- **Dimensional Model**: Star/Snowflake for BI
- **Data Vault**: Hub/Link/Satellite for historical tracking
- **One Big Table (OBT)**: Denormalized for simple analytics
- **Hybrid**: Combination based on use cases

### Step 3: Define Entities per Layer

#### Bronze Layer
- Raw entities with source fidelity
- Technical metadata columns
- Audit columns

#### Silver Layer
- Business entities
- Conformed dimensions
- History tracking

#### Gold Layer
- Fact tables
- Dimension tables
- Aggregated tables

### Step 4: Define Relationships

Document:
- Primary keys (natural and surrogate)
- Foreign key relationships
- Cardinality (1:1, 1:N, M:N)
- SCD types for dimensions

### Step 5: Define Columns

For each table document:
- Column name (naming convention)
- Data type
- Nullability
- Description
- Business rules
- Source mapping

### Step 6: Generate Data Model Document

---

## Output Template

```markdown
# Data Model Document

**Project:** {project_name}  
**Date:** {date}  
**Author:** DataArchitect  
**Version:** 1.0

---

## Model Overview

### Modeling Approach

**Primary Model Type:** {Dimensional / Data Vault / Hybrid}  
**Design Rationale:** {why this approach was chosen}

### Model Statistics

| Layer | Tables | Relationships |
|-------|--------|---------------|
| Bronze | {count} | {count} |
| Silver | {count} | {count} |
| Gold | {count} | {count} |

---

## Entity Relationship Diagram

### High-Level ERD

```
                        ┌─────────────────┐
                        │   dim_date      │
                        └────────┬────────┘
                                 │
┌─────────────┐    ┌────────────┴────────────┐    ┌─────────────┐
│ dim_entity_1│───▶│       fact_main          │◀───│ dim_entity_2│
└─────────────┘    └─────────────────────────┘    └─────────────┘
```

---

## Bronze Layer Models

### Entity: brz_{entity_name}

**Description:** {purpose of this bronze table}  
**Source:** {source_system}  
**Update Pattern:** {full / incremental / CDC}

| Column | Type | Nullable | Description | Source |
|--------|------|----------|-------------|--------|
| _key | STRING | No | Business key | {source_col} |
| {column_1} | {type} | {Yes/No} | {description} | {source_col} |
| {column_2} | {type} | {Yes/No} | {description} | {source_col} |
| _source_file | STRING | No | Ingestion source | System |
| _ingested_at | TIMESTAMP | No | Ingestion time | System |
| _batch_id | STRING | No | Batch identifier | System |

**Primary Key:** `_key`  
**Partition Key:** `_ingested_at`

---

## Silver Layer Models

### Entity: slv_{domain}_{entity_name}

**Description:** {purpose of this silver table}  
**SCD Type:** {Type 1 / Type 2 / Hybrid}  
**Business Owner:** {team/person}

| Column | Type | Nullable | Description | Transformation |
|--------|------|----------|-------------|----------------|
| {entity}_sk | BIGINT | No | Surrogate key | Generated |
| {entity}_bk | STRING | No | Business key | {transformation} |
| {column_1} | {type} | {Yes/No} | {description} | {transformation} |
| {column_2} | {type} | {Yes/No} | {description} | {transformation} |
| is_current | BOOLEAN | No | Current record flag | SCD logic |
| valid_from | TIMESTAMP | No | Validity start | SCD logic |
| valid_to | TIMESTAMP | Yes | Validity end | SCD logic |
| _created_at | TIMESTAMP | No | Record creation | System |
| _updated_at | TIMESTAMP | No | Last update | System |

**Primary Key:** `{entity}_sk`  
**Business Key:** `{entity}_bk`  
**Partition Key:** `{partition_column}`

**Business Rules:**
1. {rule_1}
2. {rule_2}

---

## Gold Layer Models

### Fact Table: gld_fact_{name}

**Description:** {what this fact measures}  
**Grain:** {one row = what}  
**Update Frequency:** {frequency}

| Column | Type | Nullable | Description | Source |
|--------|------|----------|-------------|--------|
| fact_sk | BIGINT | No | Surrogate key | Generated |
| date_sk | INT | No | Date dimension key | dim_date |
| {dim_1}_sk | BIGINT | No | Dimension 1 key | slv_{dim_1} |
| {dim_2}_sk | BIGINT | No | Dimension 2 key | slv_{dim_2} |
| {measure_1} | DECIMAL(18,2) | No | {description} | {calculation} |
| {measure_2} | DECIMAL(18,2) | Yes | {description} | {calculation} |
| {measure_3} | INT | No | {description} | {calculation} |
| _created_at | TIMESTAMP | No | Record creation | System |

**Primary Key:** `fact_sk`  
**Foreign Keys:**
- `date_sk` → `dim_date.date_sk`
- `{dim_1}_sk` → `dim_{dim_1}.{dim_1}_sk`

**Measures:**
| Measure | Type | Aggregation | Description |
|---------|------|-------------|-------------|
| {measure_1} | Additive | SUM | {description} |
| {measure_2} | Semi-additive | AVG | {description} |
| {measure_3} | Non-additive | DISTINCT COUNT | {description} |

### Dimension Table: gld_dim_{name}

**Description:** {what this dimension represents}  
**SCD Type:** {Type 1 / Type 2}  
**Record Count (Est.):** {estimate}

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| {dim}_sk | BIGINT | No | Surrogate key |
| {dim}_bk | STRING | No | Business key |
| {attr_1} | {type} | {Yes/No} | {description} |
| {attr_2} | {type} | {Yes/No} | {description} |
| {hierarchy_1}_name | STRING | Yes | Hierarchy level 1 |
| {hierarchy_2}_name | STRING | Yes | Hierarchy level 2 |
| is_current | BOOLEAN | No | Current record flag |
| valid_from | DATE | No | Validity start |
| valid_to | DATE | Yes | Validity end |

**Primary Key:** `{dim}_sk`  
**Business Key:** `{dim}_bk`

**Hierarchies:**
```
{hierarchy_name}
└── {level_1}
    └── {level_2}
        └── {level_3}
```

---

## Standard Dimensions

### dim_date

**Description:** Standard date dimension  
**Grain:** One row per calendar day  
**Range:** {start_date} to {end_date}

| Column | Type | Description |
|--------|------|-------------|
| date_sk | INT | YYYYMMDD format |
| full_date | DATE | Calendar date |
| year | INT | Year |
| quarter | INT | Quarter (1-4) |
| month | INT | Month (1-12) |
| week | INT | Week of year |
| day_of_week | INT | Day (1=Monday) |
| is_weekend | BOOLEAN | Weekend flag |
| is_holiday | BOOLEAN | Holiday flag |
| fiscal_year | INT | Fiscal year |
| fiscal_quarter | INT | Fiscal quarter |

### dim_time (if needed)

**Description:** Time dimension for intraday analysis  
**Grain:** One row per second/minute

---

## Relationships

### Relationship Diagram

| Parent Table | Child Table | Cardinality | FK Column |
|--------------|-------------|-------------|-----------|
| dim_date | fact_{main} | 1:N | date_sk |
| dim_{entity_1} | fact_{main} | 1:N | {entity_1}_sk |
| dim_{entity_2} | fact_{main} | 1:N | {entity_2}_sk |

### Referential Integrity Rules

- All fact table FKs must exist in dimension
- Unknown values use surrogate key `-1`
- Late arriving dimensions handled via placeholder

---

## Naming Conventions

### Tables

| Layer | Pattern | Example |
|-------|---------|---------|
| Landing | `lnd_{source}_{entity}` | lnd_sap_orders |
| Bronze | `brz_{domain}_{entity}` | brz_sales_orders |
| Silver | `slv_{domain}_{entity}` | slv_sales_orders |
| Gold Fact | `gld_fact_{subject}` | gld_fact_sales |
| Gold Dim | `gld_dim_{entity}` | gld_dim_customer |

### Columns

| Type | Pattern | Example |
|------|---------|---------|
| Surrogate Key | `{entity}_sk` | customer_sk |
| Business Key | `{entity}_bk` | customer_bk |
| Foreign Key | `{entity}_sk` | customer_sk (in fact) |
| Date FK | `{context}_date_sk` | order_date_sk |
| Flag | `is_{condition}` | is_active |
| Count | `{noun}_count` | item_count |
| Amount | `{noun}_amount` | sale_amount |
| Audit | `_{action}_at` | _created_at |

---

## Data Types Standard

| Logical Type | Physical Type | Notes |
|--------------|---------------|-------|
| Surrogate Key | BIGINT | Auto-generated |
| Business Key | STRING | Natural key |
| Text | STRING | Variable length |
| Integer | INT / BIGINT | Based on range |
| Decimal | DECIMAL(18,4) | Monetary values |
| Percentage | DECIMAL(5,4) | 0.0000 to 1.0000 |
| Boolean | BOOLEAN | true/false |
| Date | DATE | YYYY-MM-DD |
| Timestamp | TIMESTAMP | UTC timezone |

---

## Next Steps

1. Document architecture decisions - `*document-decisions`
2. Create DDL scripts based on this model
3. Proceed to Gate 2 validation

---

*Document generated by DataArchitect Agent*
```

---

## Validation Checklist

Before completing, verify:

- [ ] All required entities defined
- [ ] Relationships clearly documented
- [ ] Keys (PK, FK, BK) specified
- [ ] Data types appropriate
- [ ] Naming conventions consistent
- [ ] Supports all analytical questions
- [ ] Aligns with architecture document
- [ ] SCD types defined for dimensions
