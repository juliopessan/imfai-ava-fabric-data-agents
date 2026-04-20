# 🧭 Migration Coordinator Agent

**AI-Agent Migration Factory™ — Pipeline Orchestration & Gate Validation**

---

## Overview

O Migration Coordinator Agent (Orion) é o coordenador central da Migration Factory. Gerencia o fluxo end-to-end da migração, coordena todos os agentes especializados, valida gates entre fases, e garante que a migração siga o plano estabelecido.

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Persona** | Orion |
| **Icon** | 🧭 |
| **Phase** | CORE |
| **Gate** | All (1, 2, 3) |
| **Autonomy** | Level 1 (Assisted) |
| **Engine** | LangChain + LangGraph State Machine |

---

## Activation

```
@migration-coordinator
```

---

## Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` | Generate migration status report |
| `*start-wave` | Initialize and start a migration wave |
| `*gate-1` | Validate Gate 1 (UPSTREAM → MIDSTREAM) |
| `*gate-2` | Validate Gate 2 (MIDSTREAM → DOWNSTREAM) |
| `*gate-3` | Validate Gate 3 (DOWNSTREAM → PRODUCTION) |
| `*rollback` | Initiate wave rollback procedure |
| `*escalate` | Escalate issue to human team |
| `*audit` | Show audit trail of all decisions |
| `*route` | Route to the best agent for a task |

---

## Migration Phases

```
┌─────────────┐     Gate 1      ┌─────────────┐     Gate 2      ┌─────────────┐     Gate 3      ┌─────────┐
│  UPSTREAM   │────────────────▶│  MIDSTREAM   │────────────────▶│ DOWNSTREAM  │────────────────▶│PRODUÇÃO │
│  Discovery  │  ✅ Inventário  │  Transform   │  ✅ Código OK   │  Validation │  ✅ Dados OK    │         │
│             │  ✅ Lógica OK   │              │  ✅ Quality OK   │             │  ✅ Reconciled  │         │
│  Scout 🔍   │  ✅ Blueprint   │  Coda ⚙️     │  ✅ Security OK  │ Phoenix 🔧  │  ✅ Documented  │         │
│  Logan 🧠   │                 │  Vera ✅     │                 │ Balance ⚖️   │                 │         │
│             │                 │  Shield 🔒   │                 │ Scribe 📚   │                 │         │
└─────────────┘                 └─────────────┘                 └─────────────┘                 └─────────┘
```

---

## UPSTREAM Deliverables (Gate 1)

### Required Artifacts
1. **inventory.json** — Complete inventory of legacy pipelines, tables, jobs
2. **dependency-graph.json** — DAG of all dependencies between objects
3. **dead-code-report.md** — Orphan objects identified
4. **pseudocode/*.json** — Platform-agnostic logic for each pipeline
5. **digital-twin.json** — Semantic blueprint of the legacy environment

---

## Integration Points

### Upstream
None (entry point — receives migration plan from PM)

### Downstream
All agents: Scout 🔍, Logan 🧠, Coda ⚙️, Vera ✅, Shield 🔒, Phoenix 🔧, Balance ⚖️, Scribe 📚

---

## File Structure

```
migration-coordinator-agent/
├── README.md
└── .avanade-core/
    ├── core-config.yaml
    ├── agents/
    │   └── migration-coordinator.md
    ├── checklists/
    │   ├── migration-coordinator-checklist.md
    │   ├── gate-1-checklist.md
    │   ├── gate-2-checklist.md
    │   └── gate-3-checklist.md
    ├── data/
    │   ├── migration-orchestration-best-practices.md
    │   └── gate-criteria-reference.md
    ├── tasks/
    │   ├── start-wave.md
    │   ├── project-status.md
    │   ├── validate-gate-1.md
    │   ├── validate-gate-2.md
    │   ├── validate-gate-3.md
    │   ├── rollback-wave.md
    │   ├── escalate.md
    │   ├── audit-trail.md
    │   └── route-next.md
    └── templates/
        ├── wave-status-report-tmpl.md
        ├── gate-report-tmpl.md
        └── rollback-plan-tmpl.md
```

---

## Related Agents

| Agent | Relationship |
|-------|--------------|
| **Scout 🔍** | Triggers UPSTREAM discovery |
| **Logan 🧠** | Receives logic extraction results |
| **Coda ⚙️** | Triggers MIDSTREAM code generation |
| **Vera ✅** | Receives quality validation results |
| **Shield 🔒** | Receives compliance results |
| **Phoenix 🔧** | Receives self-healing results |
| **Balance ⚖️** | Triggers DOWNSTREAM reconciliation |
| **Scribe 📚** | Triggers documentation generation |

---

*AI-Agent Migration Factory™ — Migration Coordinator Agent v4.0*
