# 📊 BusinessAnalyst Agent

**Avanade™ Core Agent for Requirements Analysis and Data Mapping**

---

## Overview

The BusinessAnalyst Agent bridges business strategy and technical implementation. It specializes in creating Source-to-Target Mappings (STTM), formulating analytical questions, and defining initial data quality requirements.

---

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **STTM Creation** | Document source-to-target data mappings |
| **Analytical Questions** | Define business questions the data must answer |
| **DQ Initial** | Establish initial data quality requirements |
| **Business Rules** | Document transformation and business rules |
| **Source Analysis** | Analyze and document data sources |

---

## Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*create-sttm` | Create Source-to-Target Mapping document |
| `*analytical-questions` | Define analytical questions |
| `*dq-initial` | Define initial data quality requirements |
| `*business-rules` | Document business rules |
| `*source-analysis` | Analyze data sources |

---

## Project Phase

```
┌─────────────────────────────────────────────────────────────┐
│ UPSTREAM (Discovery)                                        │
│ ┌─────────────────┐    ┌─────────────────┐                 │
│ │ DataStrategist  │───▶│ BusinessAnalyst │                 │
│ │                 │    │ 📊              │                 │
│ │ Problem, KPIs   │    │ STTM, Questions │                 │
│ │                 │    │ DQ Initial      │                 │
│ └─────────────────┘    └─────────────────┘                 │
│                              │                              │
│                              ▼                              │
│                         ┌─────────┐                         │
│                         │ Gate 1  │                         │
│                         └─────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Output Artifacts

| Artifact | Description | Gate 1 Required |
|----------|-------------|-----------------|
| `sttm.md` | Source-to-Target Mapping | ✅ Yes |
| `analytical-questions.md` | Business questions | ✅ Yes |
| `dq-initial.md` | Initial DQ requirements | ✅ Yes |
| `business-rules.md` | Transformation rules | Optional |
| `source-analysis.md` | Source documentation | Optional |

---

## File Structure

```
business-analyst-agent/
├── .avanade-core/
│   ├── agents/
│   │   └── business-analyst.md
│   ├── tasks/
│   │   ├── create-sttm.md
│   │   ├── define-analytical-questions.md
│   │   └── define-dq-initial.md
│   ├── checklists/
│   │   └── business-analyst-checklist.md
│   ├── templates/
│   │   ├── sttm-tmpl.yaml
│   │   └── analytical-questions-tmpl.yaml
│   ├── data/
│   │   └── requirements-best-practices.md
│   └── core-config.yaml
└── README.md
```

---

## Quick Start

### 1. Create STTM
```
@business-analyst *create-sttm
```

### 2. Define Analytical Questions
```
@business-analyst *analytical-questions
```

### 3. Define Initial DQ Requirements
```
@business-analyst *dq-initial
```

---

## Workflow

1. **Review Upstream Artifacts**
   - Problem statement from DataStrategist
   - KPIs and success criteria
   - Stakeholder requirements

2. **Create STTM**
   - Document all source systems
   - Map fields to target tables
   - Define transformation rules

3. **Define Analytical Questions**
   - Translate KPIs to specific questions
   - Identify data requirements per question
   - Prioritize by business value

4. **Define DQ Initial**
   - Identify critical fields
   - Set quality thresholds
   - Define initial validation rules

5. **Hand Off for Gate 1**
   - Pass to Orchestrator for validation

---

## STTM Structure

### Data Layers

| Layer | Purpose | Naming |
|-------|---------|--------|
| Landing | Raw data copy | `lnd_*` |
| Bronze | Cleaned, typed | `brz_*` |
| Silver | Business logic | `slv_*` |
| Gold | Aggregated | `gld_*` |

### Mapping Table Format

| Source | Target | Transform |
|--------|--------|-----------|
| system.table.column | layer_table.column | rule |

---

## Integration with Other Agents

**Receives from:**
- **DataStrategist**: Problem statement, KPIs

**Sends to:**
- **DataArchitect**: STTM for architecture design
- **Orchestrator**: Artifacts for Gate 1 validation

---

## Best Practices

1. **Review upstream first** - Always check problem statement and KPIs
2. **Be comprehensive** - Don't miss source fields
3. **Think questions** - What will the data need to answer?
4. **Quality early** - Define DQ requirements from the start
5. **Document transformations** - Leave no ambiguity

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-21 | Initial release |

---

*BusinessAnalyst Agent - Part of Avanade™ Core*
