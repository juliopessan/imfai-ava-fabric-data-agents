# AgentDesigner Agent (Nova)

**Avanade™ Core Data Agent**

---

## Overview

The AgentDesigner agent (Nova 🧠) is a **meta-level agent** responsible for designing multi-agent blueprints, defining guardrails, and establishing agent contracts. It operates in the **CORE layer** and is **OPTIONAL** - used only for complex multi-agent projects (5+ custom agents).

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Name** | Nova |
| **Icon** | 🧠 |
| **Phase** | MIDSTREAM |
| **Gate** | Gate 2 |
| **Dependencies** | DataStrategist, BusinessAnalyst, DataArchitect |
| **Artifacts** | agent-blueprint.md, agent-contracts.md, orchestration-flow.md |

---

## Activation

### VS Code Chatmode

Use the AgentDesigner chatmode:
```
@agent-designer
```

### Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` / `*WS` | Show progress on artifacts |
| `*agent-blueprint` / `*AD` | Create agent blueprint |
| `*agent-contracts` / `*AC` | Define contracts between agents |
| `*guardrails` | Design guardrails and gates |
| `*orchestration` | Design orchestration flow |
| `*autonomy-matrix` | Define autonomy levels |
| `*dismiss` / `*DA` | End session |

---

## Gate 2 Deliverables

### Required Artifacts

1. **agent-blueprint.md**
   - Agent definitions
   - Responsibilities and scope
   - Tools and capabilities
   - Persona and behavior
   - Activation instructions

2. **agent-contracts.md**
   - Input/output contracts
   - Dependencies between agents
   - Handoff protocols
   - Error handling
   - Retry policies

3. **orchestration-flow.md**
   - Execution flow
   - Gates and checkpoints
   - Decision points
   - Escalation paths
   - Human-in-the-loop triggers

---

## Core Principles

1. **Clear I/O contracts** — Each agent must have well-defined inputs/outputs
2. **Gates as guardrails** — Mandatory validation points between phases
3. **Autonomy proportional to risk** — More risk = more human oversight
4. **Specialization over generalization** — Focused agents are more reliable
5. **Composition over monolith** — Small agents that collaborate
6. **Built-in observability** — Logs, traces and metrics from design

---

## Autonomy Levels

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 1 | **Assisted** | Suggests, human decides | PRD review |
| 2 | **Supervised** | Executes, human approves | Code generation |
| 3 | **Monitored** | Executes, human audits | Data validation |
| 4 | **Autonomous** | Executes independently | Logging, metrics |

---

## Workflow

1. **Analyze Context**
   - Understand project and stakeholders
   - Map automation requirements
   - Identify risk points

2. **Design Agents**
   - Define responsibilities
   - Establish boundaries
   - Specify capabilities

3. **Create Contracts**
   - Define I/O for each agent
   - Map dependencies
   - Establish handoffs

4. **Design Guardrails**
   - Create validation gates
   - Define autonomy levels
   - Plan escalations

5. **Validate and Iterate**
   - Review with stakeholders
   - Simulate flows
   - Adjust design

---

## Handoff

After completing:
- **To DataArchitect (Winston)** → Technical validation of design
- **To Orchestrator (Orion)** → Flow implementation
- **To DataEngineerExec (Diego)** → Pipeline execution

---

## Folder Structure

```
agent-designer-agent/
├── README.md
└── .avanade-core/
    ├── core-config.yaml
    ├── agents/
    │   └── agent-designer.md
    ├── checklists/
    │   └── agent-designer-checklist.md
    ├── data/
    │   └── agent-design-best-practices.md
    ├── tasks/
    │   ├── create-agent-blueprint.md
    │   ├── create-agent-contracts.md
    │   ├── design-guardrails.md
    │   └── create-orchestration-flow.md
    └── templates/
        ├── agent-blueprint-tmpl.md
        ├── agent-contract-tmpl.yaml
        └── orchestration-flow-tmpl.md
```

---

*Nova works in the CORE (Meta-Level) layer, designing the agent architecture for complex multi-agent projects. For standard data pipeline projects (80% of cases), this agent is NOT needed.*
