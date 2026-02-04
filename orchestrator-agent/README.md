# 🧭 Orchestrator Agent

**Avanade™ Core Agent for Pipeline Orchestration and Gate Validation**

---

## Overview

The Orchestrator Agent is the central coordinator for data pipeline projects. It manages phase transitions through gate validations, routes work to specialized agents, maintains audit trails, and provides project status visibility.

---

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **Gate Validation** | Validate completion of UPSTREAM, MIDSTREAM, and DOWNSTREAM phases |
| **Agent Routing** | Intelligently route to the best agent for each task |
| **Status Reporting** | Generate comprehensive project status reports |
| **Audit Trail** | Maintain complete history of project activities |
| **Artifact Inventory** | Track all project artifacts across phases |

---

## Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` | Generate project status report |
| `*gate-1` | Validate Gate 1 (UPSTREAM → MIDSTREAM) |
| `*gate-2` | Validate Gate 2 (MIDSTREAM → DOWNSTREAM) |
| `*gate-3` | Validate Gate 3 (DOWNSTREAM → PRODUCTION) |
| `*route` | Get recommendation for best agent |
| `*artifacts` | List all project artifacts |
| `*audit` | Show audit trail |

---

## Project Phases

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  UPSTREAM   │────▶│  MIDSTREAM  │────▶│ DOWNSTREAM  │────▶│ PRODUCTION  │
│  Discovery  │     │   Design    │     │Implementation│     │   Deploy    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
    ┌───────┐          ┌───────┐          ┌───────┐
    │Gate 1 │          │Gate 2 │          │Gate 3 │
    └───────┘          └───────┘          └───────┘
```

---

## Gate Criteria Summary

### Gate 1: UPSTREAM → MIDSTREAM

**Required Artifacts:**
- Problem Statement
- KPIs
- Analytical Questions
- STTM (Source-to-Target Mapping)
- DQ Initial (Initial Data Quality)

### Gate 2: MIDSTREAM → DOWNSTREAM

**Required Artifacts:**
- Architecture Document
- Data Model
- Tech Decisions (ADRs)
- DQ Rules

### Gate 3: DOWNSTREAM → PRODUCTION

**Required Artifacts:**
- DDL Scripts
- ETL Code
- Unit Tests
- Integration Tests
- Documentation
- DQ Validation Results

---

## Agent Network

The Orchestrator routes to these specialized agents:

| Agent | Phase | Expertise |
|-------|-------|-----------|
| **DataStrategist** | UPSTREAM | Problem definition, KPIs, strategy |
| **BusinessAnalyst** | UPSTREAM | STTM, analytical questions, requirements |
| **DataArchitect** | MIDSTREAM | Architecture, data model, decisions |
| **DataSteward** | MIDSTREAM | Governance, DQ rules, compliance |
| **DataFlow** | DOWNSTREAM | DDL, ETL, testing, profiling |
| **InsightForge** | DOWNSTREAM | BI, dashboards, DAX, semantic model |
| **DeliveryPro** | Cross-Phase | Delivery, risks, dependencies |

---

## File Structure

```
orchestrator-agent/
├── .avanade-core/
│   ├── agents/
│   │   └── orchestrator.md
│   ├── tasks/
│   │   ├── project-status.md
│   │   ├── validate-gate-1.md
│   │   ├── validate-gate-2.md
│   │   ├── validate-gate-3.md
│   │   ├── route-next.md
│   │   ├── audit-trail.md
│   │   └── list-artifacts.md
│   ├── checklists/
│   │   ├── orchestrator-checklist.md
│   │   ├── gate-1-checklist.md
│   │   ├── gate-2-checklist.md
│   │   └── gate-3-checklist.md
│   ├── templates/
│   │   ├── gate-report-tmpl.yaml
│   │   └── status-report-tmpl.yaml
│   ├── data/
│   │   ├── orchestration-best-practices.md
│   │   └── gate-criteria-reference.md
│   └── core-config.yaml
└── README.md
```

---

## Quick Start

### 1. Check Project Status
```
@orchestrator *status
```

### 2. Validate a Gate
```
@orchestrator *gate-1
```

### 3. Get Routing Recommendation
```
@orchestrator *route "I need to create data quality rules"
```

### 4. List All Artifacts
```
@orchestrator *artifacts
```

---

## Integration with Other Agents

The Orchestrator works as the central hub:

1. **Receives** project context and state
2. **Validates** phase completion through gates
3. **Routes** to specialized agents with context
4. **Records** all activities in audit trail
5. **Reports** status to stakeholders

---

## Best Practices

1. **Start with status** - Always run `*status` at the beginning of a session
2. **Validate before transitioning** - Don't skip gate validations
3. **Follow routing recommendations** - Use the suggested agent for each task
4. **Review audit regularly** - Check the trail for insights and patterns
5. **Complete phases fully** - Partial completion creates technical debt

---

## Configuration

The agent is configured via `core-config.yaml`:

```yaml
gates:
  gate-1:
    required_artifacts: [...]
  gate-2:
    required_artifacts: [...]
  gate-3:
    required_artifacts: [...]

routing:
  agents: [...]

settings:
  language: "pt-BR"
  auto_audit: true
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-21 | Initial release |

---

*Orchestrator Agent - Part of Avanade™ Core*
