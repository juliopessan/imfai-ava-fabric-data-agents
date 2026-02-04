# Workflow Specification: gate-2-mid-down

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/gate-2-mid-down/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Validar critérios do Gate 2 (MID→DOWN) com base em artefatos versionados (arquitetura, modelo, contracts).

**Description:** Workflow de validação (CORE) para autorizar execução técnica e geração de código.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: gate-2-mid-down
description: Validação do Gate 2 (MID→DOWN)
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/gate-2-mid-down'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | locate | Localizar artefatos MIDSTREAM |
| 02 | validate | Checar checklist Gate 2 |
| 03 | report | Gerar relatório PASS/FAIL + gaps |

---

## Workflow Inputs

### Required Inputs
- Arquitetura aprovada
- Modelo lógico versionado
- Data/Metrics/Agent execution contracts
- DQ rules documentadas
- Plataforma definida

### Optional Inputs
- Aprovação humana (flag/registro)

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/gate-2-report.md`

---

## Agent Integration

### Primary Agent
- `orchestrator`

### Other Agents
- `data-solution-architect`
- `data-modeler`
- `agent-designer`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
