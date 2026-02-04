# Workflow Specification: workflow-status

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/workflow-status/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Exibir status do projeto (esteira atual, artefatos existentes, gates pendentes) e orientar o próximo passo.

**Description:** Workflow utilitário para o Orchestrator e demais agentes lerem artefatos e reportarem progresso.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: workflow-status
description: Status do projeto e próximos passos
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/workflow-status'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | scan | Identificar artefatos existentes (planning/implementation) |
| 02 | state | Determinar estado UP/MID/DOWN |
| 03 | gates | Listar checks pendentes por gate |
| 04 | next | Sugerir próximo agente/workflow |

---

## Workflow Inputs

### Required Inputs
- `artifacts_root` e `project_code`

### Optional Inputs
- Branch/PR info (se disponível)

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/status.md`

---

## Agent Integration

### Primary Agent
- `orchestrator`

### Other Agents
- Todos (workflow compartilhado)

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
