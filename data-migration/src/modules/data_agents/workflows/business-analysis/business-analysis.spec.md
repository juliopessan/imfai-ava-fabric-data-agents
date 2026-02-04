# Workflow Specification: business-analysis

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/business-analysis/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Produzir perguntas analíticas, requisitos, regras técnicas, critérios de qualidade e STTM inicial.

**Description:** Workflow UPSTREAM para traduzir o problema em requisitos técnicos rastreáveis e prontos para arquitetura (Gate 1).

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: business-analysis
description: Perguntas analíticas, requisitos e STTM
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/business-analysis'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | scope | Confirmar escopo e fontes de dados |
| 02 | analytical-questions | Estruturar perguntas e decisões |
| 03 | rules | Converter regras de negócio em regras técnicas |
| 04 | sttm | Gerar STTM (fonte→destino) |
| 05 | dq | Propor critérios iniciais de DQ |
| 06 | export | Gerar artefatos versionáveis |

---

## Workflow Inputs

### Required Inputs
- Problem Statement + KPIs (do `data-strategy`)
- Descrição do pipeline piloto (Trip Data)

### Optional Inputs
- Amostras de dados / dicionários
- Regras adicionais do cliente

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/analytical-questions.md`
- `{artifacts_root}/{project_code}/planning-artifacts/sttm.md`
- `{artifacts_root}/{project_code}/planning-artifacts/dq-initial.md`

---

## Agent Integration

### Primary Agent
- `business-analyst`

### Other Agents
- `data-solution-architect`
- `data-modeler`
- `orchestrator`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
