# DQ Rules Document Template

# Data Quality Rules Specification

**Project:** {project_name}  
**Date:** {date}  
**Author:** DataSteward  
**Version:** 1.0

---

## Overview

This document defines comprehensive data quality rules for all data layers.

### Rule Statistics

| Layer | Rules | Critical | High | Medium | Low |
|-------|-------|----------|------|--------|-----|
| Bronze | {n} | {n} | {n} | {n} | {n} |
| Silver | {n} | {n} | {n} | {n} | {n} |
| Gold | {n} | {n} | {n} | {n} | {n} |
| **Total** | {n} | {n} | {n} | {n} | {n} |

### Severity Definitions

| Severity | Action | Description |
|----------|--------|-------------|
| CRITICAL | REJECT | Record rejected, pipeline may fail |
| HIGH | QUARANTINE | Record sent to quarantine for review |
| MEDIUM | FLAG | Record flagged but processed |
| LOW | LOG | Issue logged only |

---

## Bronze Layer Rules

### Entity: brz_{entity_name}

#### Completeness Rules

| Rule ID | Column | Check | Severity | Action | Message |
|---------|--------|-------|----------|--------|---------|
| BRZ_{ENT}_001 | {column} | NOT NULL | CRITICAL | REJECT | {column} is required |

#### Validity Rules

| Rule ID | Column | Check | Parameters | Severity | Action | Message |
|---------|--------|-------|------------|----------|--------|---------|
| BRZ_{ENT}_010 | {column} | DATA_TYPE | {type} | CRITICAL | REJECT | Invalid data type |

#### Uniqueness Rules

| Rule ID | Columns | Check | Severity | Action | Message |
|---------|---------|-------|----------|--------|---------|
| BRZ_{ENT}_020 | {key} | UNIQUE | CRITICAL | REJECT | Duplicate key |

---

## Silver Layer Rules

### Entity: slv_{domain}_{entity_name}

#### Referential Integrity Rules

| Rule ID | Source Column | Target Table | Target Column | Severity | Action | Default |
|---------|---------------|--------------|---------------|----------|--------|---------|
| SLV_{ENT}_030 | {fk_column} | {dim_table} | {pk_column} | HIGH | DEFAULT | -1 |

#### Consistency Rules

| Rule ID | Expression | Description | Severity | Action | Message |
|---------|------------|-------------|----------|--------|---------|
| SLV_{ENT}_040 | `{expression}` | {description} | HIGH | QUARANTINE | {message} |

---

## Gold Layer Rules

### Entity: gld_fact_{name}

#### Aggregation Validation Rules

| Rule ID | Check | Expected | Tolerance | Severity | Action |
|---------|-------|----------|-----------|----------|--------|
| GLD_FACT_{NAME}_060 | ROW_COUNT | > previous | 0% | HIGH | ALERT |

---

## Quarantine Strategy

### Quarantine Table Schema

```sql
CREATE TABLE quarantine.{layer}_{entity}_quarantine (
    quarantine_id BIGINT GENERATED ALWAYS AS IDENTITY,
    original_record STRING,
    rule_id STRING,
    rule_message STRING,
    severity STRING,
    quarantine_timestamp TIMESTAMP,
    reviewed_by STRING,
    resolution STRING
);
```

### Threshold Alerts

| Severity | Threshold | Action |
|----------|-----------|--------|
| CRITICAL | > 0 records | Fail pipeline |
| HIGH | > 1% of batch | Fail pipeline |
| MEDIUM | > 5% of batch | Alert only |

---

*Template provided by DataSteward Agent*
