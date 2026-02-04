# Workflow Specification: routing

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/routing/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Recomendar (e opcionalmente acionar) o próximo agente/workflow com base no estado do projeto e artefatos disponíveis.

**Description:** Workflow CORE que implementa a lógica de roteamento do Orchestrator (artefatos → próximo passo).

**Workflow Type:** Non-document

---

## Workflow Structure

### Entry Point

```yaml
---
name: routing
description: Roteamento para próximo agente/workflow
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/routing'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | detect-state | Determinar estado UP/MID/DOWN |
| 02 | pick-next | Selecionar próximo agente e workflow |
| 03 | explain | Justificar decisão e listar pré-requisitos |

---

## Workflow Inputs

### Required Inputs
- Status do projeto (scan de artefatos)

### Optional Inputs
- Preferências do usuário (ex.: pular BI)

---

## Workflow Outputs

### Output Format
- [ ] Document-producing
- [x] Non-document

### Output Files
- (opcional) `{artifacts_root}/{project_code}/planning-artifacts/next-step.md`

---

## Agent Integration

### Primary Agent
- `orchestrator`

### Other Agents
- Todos (alvo do roteamento)

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
