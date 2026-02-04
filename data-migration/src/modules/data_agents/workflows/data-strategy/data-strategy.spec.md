# Workflow Specification: data-strategy

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/data-strategy/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Definir Problem Statement, KPIs/OKRs e Success Criteria do projeto/piloto.

**Description:** Workflow UPSTREAM para transformar o contexto do PRD em objetivos mensuráveis e critérios de sucesso aprováveis no Gate 1.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: data-strategy
description: Definir Problem Statement, KPIs e Success Criteria
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/data-strategy'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | intake | Capturar contexto e restrições do projeto |
| 02 | problem-statement | Redigir problem statement claro e testável |
| 03 | kpis | Definir KPIs (baseline/target + fórmula + owner) |
| 04 | success-criteria | Consolidar DoD do Gate 1 |
| 05 | export | Gerar artefato versionável |

---

## Workflow Inputs

### Required Inputs
- Contexto do projeto (PRD)
- Stakeholders/owners
- Caso de uso piloto (Trip Data Pipeline)

### Optional Inputs
- Baselines históricos (quando disponíveis)
- Restrições de plataforma/ambiente

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/problem-statement.md`
- `{artifacts_root}/{project_code}/planning-artifacts/kpis.md`

---

## Agent Integration

### Primary Agent
- `data-strategist`

### Other Agents
- `business-analyst` (consumo dos outputs)
- `orchestrator` (validação Gate 1)

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
