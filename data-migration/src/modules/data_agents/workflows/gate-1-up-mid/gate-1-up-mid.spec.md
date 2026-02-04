# Workflow Specification: gate-1-up-mid

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/gate-1-up-mid/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Validar critérios do Gate 1 (UP→MID) com base em artefatos existentes.

**Description:** Workflow de validação (CORE) para bloquear/autorizar transição para MIDSTREAM.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: gate-1-up-mid
description: Validação do Gate 1 (UP→MID)
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/gate-1-up-mid'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | locate | Localizar artefatos UPSTREAM |
| 02 | validate | Checar checklist Gate 1 |
| 03 | report | Gerar relatório PASS/FAIL + gaps |

---

## Workflow Inputs

### Required Inputs
- Artefatos: problem statement, KPIs, escopo, fontes, STTM (opcional)

### Optional Inputs
- Aprovação humana (flag/registro)

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/gate-1-report.md`

---

## Agent Integration

### Primary Agent
- `orchestrator`

### Other Agents
- `data-strategist`
- `business-analyst`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
