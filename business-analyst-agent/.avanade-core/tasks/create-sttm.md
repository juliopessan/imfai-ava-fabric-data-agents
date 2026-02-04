# Create STTM Task

**Task ID:** create-sttm  
**Agent:** BusinessAnalyst  
**Version:** 1.0

---

## Purpose

Create a comprehensive Source-to-Target Mapping (STTM) document that defines how data flows from source systems to target tables across all data layers.

---

## Prerequisites

- Problem statement available (from DataStrategist)
- Understanding of data sources
- Access to source system documentation or samples

---

## Execution Steps

### Step 1: Identify Source Systems

For each source, document:
1. System name
2. System type (Database, API, File, Stream)
3. Connection method
4. Refresh frequency
5. Owner/Contact

**Questions to ask:**
- "What systems contain the data you need?"
- "How is data currently extracted from these systems?"
- "How often is the data updated?"

### Step 2: Document Source Tables/Entities

For each source system, list:
1. Table/Entity name
2. Description
3. Primary key(s)
4. Approximate row count
5. Key columns relevant to project

### Step 3: Define Target Architecture

Define target layers:
1. **Landing/Raw** - Raw data as-is from source
2. **Bronze** - Cleaned, typed data
3. **Silver** - Transformed, business logic applied
4. **Gold** - Aggregated, ready for consumption

### Step 4: Create Field-Level Mapping

For each target field, document:
1. Source system, table, column
2. Target layer, table, column
3. Data type transformation
4. Transformation logic
5. PK/FK designation

### Step 5: Document Transformation Rules

For complex transformations:
1. Rule description
2. SQL or pseudo-code
3. Business justification
4. Example input → output

### Step 6: Generate STTM Document

---

## Output Template

```markdown
# Source-to-Target Mapping (STTM)

**Project:** {project_name}  
**Date:** {date}  
**Author:** BusinessAnalyst  
**Version:** 1.0

---

## Executive Summary

This document defines the mapping from source systems to target data layers for the {project_name} data pipeline.

**Sources:** {n} systems  
**Target Tables:** {n} tables across {n} layers

---

## Source Systems Overview

### Source 1: {system_name}

| Attribute | Value |
|-----------|-------|
| **Type** | {Database / API / File / Stream} |
| **Connection** | {connection_string_pattern} |
| **Refresh** | {Real-time / Daily / Weekly} |
| **Owner** | {owner_name} |
| **Contact** | {contact_info} |

#### Source Tables

| Table Name | Description | Primary Key | Est. Rows |
|------------|-------------|-------------|-----------|
| {table_1} | {description} | {pk} | {rows} |
| {table_2} | {description} | {pk} | {rows} |

---

### Source 2: {system_name}

{same format}

---

## Target Architecture

### Layer Overview

| Layer | Purpose | Retention | Access |
|-------|---------|-----------|--------|
| Landing | Raw data ingestion | 30 days | ETL only |
| Bronze | Cleaned, typed | 90 days | ETL only |
| Silver | Business logic | 1 year | Analytics |
| Gold | Aggregated | Permanent | BI/Reports |

### Target Tables Summary

| Layer | Table Name | Source(s) | Description |
|-------|------------|-----------|-------------|
| Landing | lnd_{table} | {source} | {desc} |
| Bronze | brz_{table} | lnd_{table} | {desc} |
| Silver | slv_{table} | brz_{table} | {desc} |
| Gold | gld_{table} | slv_{table} | {desc} |

---

## Field-Level Mapping

### {Target_Table_Name}

**Layer:** {Bronze/Silver/Gold}  
**Source:** {source_table}  
**Description:** {table_description}

| # | Source Column | Source Type | Target Column | Target Type | Transformation | PK/FK |
|---|---------------|-------------|---------------|-------------|----------------|-------|
| 1 | {src_col} | {type} | {tgt_col} | {type} | {rule} | {PK/FK/-} |
| 2 | {src_col} | {type} | {tgt_col} | {type} | {rule} | {-} |
| 3 | - | - | {tgt_col} | {type} | {derived} | {-} |

---

## Transformation Rules

### TR-001: {rule_name}

**Applies to:** {target_table.column}  
**Type:** {Lookup / Calculation / Derivation / Cleansing}

**Description:**
{what the transformation does}

**Logic:**
```sql
{SQL or pseudo-code}
```

**Example:**
| Input | Output |
|-------|--------|
| {input_value} | {output_value} |

**Business Justification:**
{why this transformation is needed}

---

### TR-002: {rule_name}

{same format}

---

## Reference Data

### Reference Tables Required

| Table | Description | Source | Update Frequency |
|-------|-------------|--------|------------------|
| {ref_table} | {desc} | {source} | {freq} |

---

## Data Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   SOURCE    │────▶│   LANDING   │────▶│   BRONZE    │────▶│   SILVER    │────▶│   GOLD   │
│  {source}   │     │  Raw Copy   │     │   Cleaned   │     │  Business   │     │  Aggregated│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └───────────┘
```

---

## Key Mapping Decisions

| Decision | Rationale |
|----------|-----------|
| {decision_1} | {rationale} |
| {decision_2} | {rationale} |

---

## Open Questions

| # | Question | Owner | Due Date |
|---|----------|-------|----------|
| 1 | {question} | {owner} | {date} |

---

## Next Steps

1. Review STTM with stakeholders
2. Define analytical questions - `*analytical-questions`
3. Define initial DQ requirements - `*dq-initial`

---

*Document generated by BusinessAnalyst Agent*
```

---

## Validation Checklist

Before completing, verify:

- [ ] All source systems documented
- [ ] All source tables listed with PKs
- [ ] Target layers defined (Landing, Bronze, Silver, Gold)
- [ ] All target tables documented
- [ ] Field mapping is complete (no gaps)
- [ ] Transformation rules documented
- [ ] Data types specified for source and target
- [ ] PK/FK relationships identified
- [ ] Reference data identified
- [ ] Open questions captured

---

## Common Transformation Types

| Type | Description | Example |
|------|-------------|---------|
| Direct Copy | No transformation | source.field → target.field |
| Type Cast | Data type change | VARCHAR → DATE |
| Lookup | Reference table join | code → description |
| Derivation | Calculate new value | price × quantity |
| Aggregation | Sum, count, avg | SUM(amount) |
| Cleansing | Trim, upper, null handling | TRIM(UPPER(field)) |
| Concatenation | Combine fields | first + ' ' + last |
| Split | Separate field | address → city, state, zip |
