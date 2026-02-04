# DataModeler Agent (Sofia)

**Avanade™ Core Data Agent**

---

## Overview

The DataModeler agent (Sofia 🧩) is responsible for designing logical data models, defining granularity, metrics, and ensuring metadata quality during the MIDSTREAM phase of data projects.

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Name** | Sofia |
| **Icon** | 🧩 |
| **Phase** | MIDSTREAM |
| **Gate** | Gate 2 |
| **Dependencies** | DataStrategist, BusinessAnalyst, DataArchitect (Gate 1 passed) |
| **Artifacts** | data-model.md, data-contracts.md, metrics-catalog.md |

---

## Activation

### VS Code Chatmode

Use the DataModeler chatmode:
```
@data-modeler
```

### Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` | Current progress on Gate 2 artifacts |
| `*data-model` / `*DM` | Create logical data model |
| `*data-contracts` / `*DC` | Define data contracts |
| `*granularity` | Define table granularity |
| `*metrics` | Document metrics and KPIs |
| `*metadata` | Create metadata catalog |
| `*validate` | Validate model against requirements |

---

## Gate 2 Deliverables

### Required Artifacts

1. **data-model.md**
   - Logical dimensional model
   - Entity definitions (Facts and Dims)
   - Relationships and cardinality
   - Granularity per table
   - SCD types for dimensions

2. **data-contracts.md**
   - Input contracts (sources)
   - Output contracts (consumers)
   - Schema evolution rules
   - Versioning strategy
   - Breaking vs non-breaking changes

3. **metrics-catalog.md**
   - Business metrics definitions
   - Formulas and calculation rules
   - Allowed aggregations
   - Filters and contexts
   - Owner and SLA per metric

---

## Core Principles

1. **Versionable logical model** — Model must evolve with business
2. **Explicit keys and granularity** — Always define PK, FK and grain
3. **Mandatory metadata** — Description, owner, SLA, lineage
4. **Consistent naming** — Naming standards across all layers
5. **Contracts as guarantee** — Well-defined inputs/outputs
6. **Documented derived metrics** — Clear formulas and business rules

---

## Data Modeling Standards

### Granularity Definition

| Layer | Grain | Example |
|-------|-------|---------|
| Landing | 1:1 source | One record per CSV line |
| Silver | Clean entity | One record per transaction |
| Gold Fact | Business event | One row per sale |
| Gold Dim | Master entity | One row per customer (SCD2) |

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Fact Table | `fact_{subject}` | `fact_sales`, `fact_trips` |
| Dimension | `dim_{entity}` | `dim_customer`, `dim_date` |
| Bridge | `bridge_{relationship}` | `bridge_customer_segment` |
| Metric | `mtrc_{name}` | `mtrc_revenue_ytd` |

---

## Workflow

1. **Receive upstream requirements**
   - Load STTM from Mary
   - Review KPIs from Alex
   - Understand architecture from Winston

2. **Define logical model**
   - Identify entities (Facts vs Dims)
   - Define granularity per table
   - Map relationships

3. **Create data contracts**
   - Document expected schemas
   - Define evolution rules
   - Establish SLAs

4. **Document metrics**
   - Catalog business metrics
   - Define formulas and rules
   - Map to model columns

5. **Validate and deliver**
   - Verify alignment with requirements
   - Ensure model completeness
   - Prepare handoff for Gate 2

---

## Handoff

After completing:
- **To DataArchitect (Winston)** → Technical validation of model
- **To DataEngineerExec (Diego)** → DDL/ETL implementation
- **To DataSteward (Gaia)** → Governance and DQ rules

---

## Folder Structure

```
data-modeler-agent/
├── README.md
└── .avanade-core/
    ├── core-config.yaml
    ├── agents/
    │   └── data-modeler.md
    ├── checklists/
    │   └── data-modeler-checklist.md
    ├── data/
    │   └── modeling-best-practices.md
    ├── tasks/
    │   ├── create-data-model.md
    │   ├── create-data-contracts.md
    │   ├── define-granularity.md
    │   └── create-metrics-catalog.md
    └── templates/
        ├── data-model-tmpl.md
        ├── data-contract-tmpl.yaml
        └── metrics-catalog-tmpl.md
```

---

*Sofia works in the MIDSTREAM phase, after Mary (Business Analyst) and alongside Winston (Architect), before Diego (Data Engineer).*
