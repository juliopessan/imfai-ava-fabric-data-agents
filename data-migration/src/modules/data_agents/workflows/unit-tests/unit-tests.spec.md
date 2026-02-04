# Workflow Specification: unit-tests

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/unit-tests/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Gerar testes automatizados (SQL e/ou PySpark) para validar ingestão, transformações e integridade de dados.

**Description:** Workflow DOWNSTREAM para gerar suíte mínima de testes visando Gate 3 (cobertura > 80% quando aplicável).

**Workflow Type:** Non-document (tests)

---

## Workflow Structure

### Entry Point

```yaml
---
name: unit-tests
description: Geração de testes automatizados para o pipeline
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/unit-tests'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | strategy | Definir abordagem de teste (SQL vs PySpark) |
| 02 | data-fixtures | Definir/gerar dados de exemplo (se necessário) |
| 03 | tests | Gerar testes (comparação arquivo×tabela, constraints, DQ) |
| 04 | ci-notes | Notas para execução local/CI |

---

## Workflow Inputs

### Required Inputs
- Tabelas e transforms gerados (`delivery`)
- Regras de DQ e constraints

### Optional Inputs
- Ferramenta de teste alvo (dbt, pytest, etc.)

---

## Workflow Outputs

### Output Format
- [ ] Document-producing
- [x] Non-document

### Output Files
- `{artifacts_root}/{project_code}/implementation-artifacts/tests/`

---

## Agent Integration

### Primary Agent
- `data-engineer-exec`

### Other Agents
- `data-steward`
- `orchestrator`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
