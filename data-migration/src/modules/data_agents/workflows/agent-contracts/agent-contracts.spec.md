# Workflow Specification: agent-contracts

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/agent-contracts/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Definir contratos de execução dos agentes (ações permitidas/proibidas, inputs obrigatórios, outputs esperados).

**Description:** Workflow MIDSTREAM para padronizar guardrails de execução e habilitar validações automatizadas pelo Orchestrator.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: agent-contracts
description: Agent Execution Contracts (guardrails)
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/agent-contracts'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | scope | Definir escopo e categorias de ação |
| 02 | contracts | Criar contratos por agente (allow/deny) |
| 03 | approvals | Definir ações que exigem validação humana |
| 04 | export | Gerar contratos versionáveis |

---

## Workflow Inputs

### Required Inputs
- Blueprint multiagente
- Gates e critérios do PRD

### Optional Inputs
- Padrões corporativos de segurança

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/agent-execution-contracts.md`

---

## Agent Integration

### Primary Agent
- `agent-designer`

### Other Agents
- `orchestrator`
- `data-steward`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
