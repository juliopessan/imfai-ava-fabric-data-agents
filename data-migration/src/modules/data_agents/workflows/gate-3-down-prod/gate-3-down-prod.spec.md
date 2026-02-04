# Workflow Specification: gate-3-down-prod

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/gate-3-down-prod/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Validar critérios do Gate 3 (DOWN→PROD): código versionado, testes passando, cobertura, docs e aprovação humana.

**Description:** Workflow de validação (CORE) para autorizar entrega final / pronta para produção.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: gate-3-down-prod
description: Validação do Gate 3 (DOWN→PROD)
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/gate-3-down-prod'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | locate | Localizar outputs de execução e evidências |
| 02 | validate | Checar checklist Gate 3 |
| 03 | report | Gerar relatório PASS/FAIL + gaps |

---

## Workflow Inputs

### Required Inputs
- Evidência de código em Git
- Evidência de testes passando
- Evidência de cobertura
- Documentação/runbook

### Optional Inputs
- Aprovação humana (flag/registro)

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/implementation-artifacts/gate-3-report.md`

---

## Agent Integration

### Primary Agent
- `orchestrator`

### Other Agents
- `data-engineer-exec`
- `data-steward`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
