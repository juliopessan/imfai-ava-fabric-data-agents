# Create Architecture Task

**Task ID:** create-architecture  
**Agent:** DataArchitect  
**Version:** 1.0

---

## Purpose

Design and document a comprehensive data architecture that supports the business requirements defined in UPSTREAM phase.

---

## Prerequisites

- Gate 1 passed
- STTM available
- Analytical questions defined
- Understanding of technology constraints

---

## Execution Steps

### Step 1: Review Upstream Artifacts

Load and review:
- STTM (source systems, target tables, transformations)
- Analytical questions (data requirements)
- Problem statement (business context)
- KPIs (success metrics)

### Step 2: Define Architecture Pattern

Select appropriate pattern:
- **Lakehouse**: Unified analytics with Delta Lake
- **Data Warehouse**: Traditional DW/DM approach
- **Hybrid**: Combination based on needs

### Step 3: Design Data Layers

Define each layer:
1. **Landing/Raw**: Ingestion strategy
2. **Bronze**: Cleansing approach
3. **Silver**: Business logic layer
4. **Gold**: Aggregation/serving layer

### Step 4: Select Technology Stack

For each component, document:
1. Technology choice
2. Justification
3. Alternatives considered

### Step 5: Design Data Flow

Document:
1. Ingestion patterns (batch, streaming, hybrid)
2. Transformation pipeline
3. Serving patterns
4. Refresh schedules

### Step 6: Address Cross-Cutting Concerns

Document:
1. Security (access, encryption)
2. Scalability (growth strategy)
3. Monitoring (observability)
4. Disaster recovery

### Step 7: Generate Architecture Document

---

## Output Template

```markdown
# Data Architecture Document

**Project:** {project_name}  
**Date:** {date}  
**Author:** DataArchitect  
**Version:** 1.0

---

## Executive Summary

{2-3 paragraph summary of the architecture approach}

**Architecture Pattern:** {Lakehouse / Data Warehouse / Hybrid}  
**Primary Technology:** {technology}  
**Target Environment:** {cloud/on-premise/hybrid}

---

## Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  SOURCES │───▶│ LANDING  │───▶│  BRONZE  │───▶│  SILVER  │───▶ GOLD │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    ORCHESTRATION & MONITORING                   │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    SECURITY & GOVERNANCE                        │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **{principle_1}**: {description}
2. **{principle_2}**: {description}
3. **{principle_3}**: {description}

---

## Data Layers

### Landing Layer (Raw)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Raw data ingestion, source fidelity |
| **Format** | {Parquet / Delta / CSV} |
| **Retention** | {30 days / configurable} |
| **Access** | ETL processes only |
| **Naming** | `lnd_{source}_{entity}` |

**Ingestion Patterns:**
- {batch / streaming / hybrid}
- {full / incremental / CDC}

### Bronze Layer (Cleansed)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Cleansed, typed, deduplicated |
| **Format** | {Delta / Parquet} |
| **Retention** | {90 days} |
| **Access** | ETL, advanced users |
| **Naming** | `brz_{domain}_{entity}` |

**Transformations Applied:**
- Data type standardization
- NULL handling
- Deduplication
- Schema enforcement

### Silver Layer (Curated)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Business logic, joined, enriched |
| **Format** | {Delta} |
| **Retention** | {1 year} |
| **Access** | Analytics, Data Science |
| **Naming** | `slv_{domain}_{entity}` |

**Transformations Applied:**
- Business rules
- Lookups and enrichment
- Aggregations
- Data quality rules

### Gold Layer (Aggregated)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Consumption-ready, aggregated |
| **Format** | {Delta / Semantic Model} |
| **Retention** | {Permanent} |
| **Access** | BI, Reporting, End Users |
| **Naming** | `gld_{domain}_{subject}` |

**Optimizations:**
- Pre-aggregated metrics
- Dimensional models
- Query-optimized schemas

---

## Technology Stack

### Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| Storage | {Azure Data Lake / S3 / GCS} | Raw and processed data |
| Processing | {Spark / Databricks / Synapse} | ETL and transformations |
| Orchestration | {ADF / Airflow / Prefect} | Pipeline scheduling |
| Serving | {Delta / SQL Endpoint / Synapse} | Query access |
| BI | {Power BI / Tableau / Looker} | Visualization |
| Governance | {Unity Catalog / Purview} | Metadata and access |

### Component Details

#### {Component 1}

| Attribute | Value |
|-----------|-------|
| **Technology** | {technology_name} |
| **Purpose** | {what it does} |
| **Justification** | {why chosen} |
| **Alternatives** | {what else was considered} |

---

## Data Flow

### Ingestion Flow

```
{Source 1} ──┐
             ├──▶ [Ingestion] ──▶ Landing
{Source 2} ──┘
```

**Ingestion Details:**

| Source | Type | Method | Frequency | SLA |
|--------|------|--------|-----------|-----|
| {source_1} | {DB/API/File} | {method} | {freq} | {sla} |
| {source_2} | {type} | {method} | {freq} | {sla} |

### Transformation Flow

```
Landing ──▶ [Clean] ──▶ Bronze ──▶ [Enrich] ──▶ Silver ──▶ [Aggregate] ──▶ Gold
```

### Serving Flow

```
Gold ──▶ [SQL Endpoint] ──▶ Power BI
     ──▶ [API]          ──▶ Applications
     ──▶ [Export]       ──▶ External Systems
```

---

## Security Architecture

### Access Control

| Layer | Access Level | Method |
|-------|--------------|--------|
| Landing | ETL Service | Service Principal |
| Bronze | ETL + Advanced Users | AAD Groups |
| Silver | Analytics Team | AAD Groups + Row Level |
| Gold | All Authorized | AAD + RLS |

### Data Protection

- **Encryption at Rest**: {method}
- **Encryption in Transit**: {method}
- **Key Management**: {approach}

### Compliance

- {compliance_requirement_1}
- {compliance_requirement_2}

---

## Scalability

### Current Sizing

| Metric | Current | Expected Growth |
|--------|---------|-----------------|
| Data Volume | {X GB} | {Y% per year} |
| Daily Records | {X records} | {Y% per year} |
| Concurrent Users | {X} | {Y} |

### Scaling Strategy

1. **Horizontal Scaling**: {approach}
2. **Partitioning Strategy**: {strategy}
3. **Caching Strategy**: {approach}

---

## Monitoring & Operations

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Pipeline Success Rate | % of successful runs | < 99% |
| Data Freshness | Time since last update | > SLA |
| Query Performance | P95 latency | > 5s |
| Storage Growth | Daily delta | > 20% |

### Monitoring Tools

- {tool_1}: {purpose}
- {tool_2}: {purpose}

---

## Disaster Recovery

| Metric | Target |
|--------|--------|
| **RTO** | {time} |
| **RPO** | {time} |
| **Backup Frequency** | {frequency} |
| **Backup Retention** | {period} |

---

## Architecture Decisions

See `decisions.md` for detailed ADRs:
- ADR-001: {decision_title}
- ADR-002: {decision_title}
- ADR-003: {decision_title}

---

## Next Steps

1. Create data model - `*create-data-model`
2. Document decisions - `*document-decisions`
3. Proceed to Gate 2 validation

---

*Document generated by DataArchitect Agent*
```

---

## Validation Checklist

Before completing, verify:

- [ ] All data layers defined
- [ ] Technology stack documented with justifications
- [ ] Data flow clearly diagrammed
- [ ] Security approach documented
- [ ] Scalability strategy defined
- [ ] Monitoring approach specified
- [ ] Aligns with STTM requirements
- [ ] Supports all analytical questions
