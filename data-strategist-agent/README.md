# 🎯 DataStrategist Agent

**Avanade™ Core Agent for Data Strategy and Business Problem Definition**

---

## Overview

The DataStrategist Agent is the starting point for data pipeline projects. It specializes in translating business needs into clear data strategy by defining problems, identifying KPIs, and establishing success criteria.

---

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **Problem Definition** | Create clear, quantified business problem statements |
| **KPI Identification** | Define measurable Key Performance Indicators |
| **Success Criteria** | Establish criteria for project success |
| **Stakeholder Mapping** | Identify and analyze stakeholders |
| **Value Proposition** | Document data value proposition |

---

## Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*define-problem` | Guide through problem statement creation |
| `*create-kpis` | Create KPIs based on business objectives |
| `*success-criteria` | Define measurable success criteria |
| `*stakeholders` | Identify and document stakeholders |
| `*value-prop` | Create data value proposition |
| `*strategy-summary` | Generate strategy summary document |

---

## Project Phase

```
┌─────────────────────────────────────────────────────────────┐
│ UPSTREAM (Discovery)                                        │
│ ┌─────────────────┐    ┌─────────────────┐                 │
│ │ DataStrategist  │───▶│ BusinessAnalyst │                 │
│ │ 🎯              │    │                 │                 │
│ │ Problem, KPIs,  │    │ STTM, Questions │                 │
│ │ Success Criteria│    │ DQ Initial      │                 │
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
| `problem-statement.md` | Business problem definition | ✅ Yes |
| `kpis.md` | Key Performance Indicators | ✅ Yes |
| `success-criteria.md` | Success criteria | ⚠️ Recommended |
| `stakeholders.md` | Stakeholder map | Optional |
| `value-proposition.md` | Data value proposition | Optional |

---

## File Structure

```
data-strategist-agent/
├── .avanade-core/
│   ├── agents/
│   │   └── data-strategist.md
│   ├── tasks/
│   │   ├── define-problem-statement.md
│   │   ├── create-kpis.md
│   │   └── define-success-criteria.md
│   ├── checklists/
│   │   └── data-strategist-checklist.md
│   ├── templates/
│   │   ├── problem-statement-tmpl.yaml
│   │   └── kpis-tmpl.yaml
│   ├── data/
│   │   └── strategy-best-practices.md
│   └── core-config.yaml
└── README.md
```

---

## Quick Start

### 1. Define the Problem
```
@data-strategist *define-problem
```

### 2. Create KPIs
```
@data-strategist *create-kpis
```

### 3. Define Success Criteria
```
@data-strategist *success-criteria
```

---

## Workflow

1. **Start with the Problem**
   - Use `*define-problem` to create problem statement
   - Ensure business context is clear
   - Quantify the impact

2. **Define Measurable KPIs**
   - Use `*create-kpis` after problem is defined
   - Set baselines and targets
   - Document calculation methods

3. **Establish Success Criteria**
   - Use `*success-criteria` to define what success looks like
   - Prioritize criteria (Must/Should/Nice to Have)
   - Get stakeholder agreement

4. **Hand Off to BusinessAnalyst**
   - Share problem statement and KPIs
   - BusinessAnalyst will create STTM and analytical questions

---

## Best Practices

1. **Start with "Why"** - Understand the business driver first
2. **Be specific** - Avoid vague problem statements
3. **Quantify everything** - Use numbers to describe impact
4. **Think stakeholders** - Consider who benefits and who decides
5. **Connect to value** - Link every deliverable to business value

---

## Integration with Other Agents

**Sends artifacts to:**
- **BusinessAnalyst**: Problem context for requirements
- **Orchestrator**: Strategic artifacts for Gate 1 validation

**Receives guidance from:**
- **Orchestrator**: Routing and phase management

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-21 | Initial release |

---

*DataStrategist Agent - Part of Avanade™ Core*
