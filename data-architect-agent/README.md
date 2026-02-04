# DataArchitect Agent

**Avanade™ Core Data Agent**

---

## Overview

The DataArchitect agent is responsible for designing comprehensive data architectures, creating data models, and documenting key technical decisions during the MIDSTREAM phase of data projects.

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Icon** | 🏗️ |
| **Phase** | MIDSTREAM |
| **Gate** | Gate 2 |
| **Dependencies** | DataStrategist, BusinessAnalyst (Gate 1 passed) |
| **Artifacts** | architecture.md, data-model.md, decisions.md |

---

## Activation

### VS Code Chatmode

Use the DataArchitect chatmode:
```
@data-architect
```

### Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` | Current progress on Gate 2 artifacts |
| `*create-architecture` | Design data architecture |
| `*create-data-model` | Create dimensional/entity model |
| `*document-decisions` | Create Architecture Decision Records |
| `*tech-stack` | Document technology selections |
| `*security-design` | Design security architecture |

---

## Gate 2 Deliverables

### Required Artifacts

1. **architecture.md**
   - High-level architecture diagram
   - Data layer definitions (Landing → Bronze → Silver → Gold)
   - Technology stack with justifications
   - Data flow documentation
   - Security and scalability approach

2. **data-model.md**
   - Entity Relationship Diagrams
   - Table definitions per layer
   - Column specifications
   - Naming conventions
   - SCD type definitions

3. **decisions.md**
   - Architecture Decision Records (ADRs)
   - Technology selection rationale
   - Modeling approach decisions
   - Security model decisions

---

## Workflow

### Typical Session

```
User: @data-architect let's design the architecture

Agent: I'll help design the data architecture. Let me review the 
       Gate 1 artifacts first...
       
       Based on the STTM and analytical questions, I recommend:
       
       **Architecture Pattern:** Lakehouse
       **Technology:** Azure Databricks + Delta Lake
       
       Should I create the full architecture document?
```

### Sequential Tasks

1. **Start**: `*create-architecture`
   - Review upstream artifacts
   - Select architecture pattern
   - Define technology stack
   - Document data flow

2. **Then**: `*create-data-model`
   - Design dimensional model
   - Define fact and dimension tables
   - Document relationships
   - Specify column details

3. **Finally**: `*document-decisions`
   - Create ADRs for key decisions
   - Document alternatives considered
   - Record consequences

---

## Integration Points

### Upstream (Gate 1)

Receives from:
- **DataStrategist**: Problem statement, KPIs
- **BusinessAnalyst**: STTM, analytical questions, DQ initial

### Downstream (Gate 2 → Gate 3)

Provides to:
- **DataSteward**: Architecture for governance rules
- **DataFlow**: Data model for DDL/ETL generation
- **InsightForge**: Model for semantic layer

---

## File Structure

```
data-architect-agent/
├── .avanade-core/
│   ├── agents/
│   │   └── data-architect.md
│   ├── core-config.yaml
│   ├── tasks/
│   │   ├── create-architecture.md
│   │   ├── create-data-model.md
│   │   └── document-decisions.md
│   ├── checklists/
│   │   └── data-architect-checklist.md
│   ├── templates/
│   │   ├── architecture-tmpl.yaml
│   │   ├── data-model-tmpl.yaml
│   │   └── adr-tmpl.yaml
│   └── data/
│       └── architecture-best-practices.md
└── README.md
```

---

## Best Practices

### Architecture Design

1. Start with business requirements (from STTM)
2. Choose appropriate pattern (Lakehouse, DW, Hybrid)
3. Define all layers clearly
4. Document technology justifications
5. Address security early
6. Plan for scalability

### Data Modeling

1. Align with analytical questions
2. Use consistent naming conventions
3. Define clear grain for facts
4. Apply appropriate SCD types
5. Document all relationships
6. Include standard dimensions (date, time)

### Decision Records

1. Document all significant decisions
2. List alternatives considered
3. State consequences clearly
4. Link related decisions
5. Review periodically

---

## Example Output

### Architecture Summary

```
Architecture Pattern: Lakehouse
Storage: Azure Data Lake Gen2
Processing: Azure Databricks
Orchestration: Azure Data Factory
Serving: Databricks SQL
BI: Power BI Premium

Data Layers:
- Landing: Raw ingestion (Parquet)
- Bronze: Cleansed (Delta)
- Silver: Curated (Delta)
- Gold: Aggregated (Delta + Semantic)
```

### Model Summary

```
Dimensional Model:
- 3 Fact Tables
- 8 Dimension Tables
- 1 Bridge Table

Key Entities:
- gld_fact_trips (grain: trip_id)
- gld_dim_vendor
- gld_dim_location
- gld_dim_date
```

---

## Related Agents

| Agent | Relationship |
|-------|--------------|
| **Orchestrator** | Validates Gate 2 readiness |
| **DataStrategist** | Provides problem statement |
| **BusinessAnalyst** | Provides STTM |
| **DataSteward** | Receives for governance |
| **DataFlow** | Receives for implementation |

---

*Avanade™ Core - DataArchitect Agent*
