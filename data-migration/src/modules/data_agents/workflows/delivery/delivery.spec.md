# Workflow Specification: delivery

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/delivery/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Gerar entregáveis técnicos executáveis (DDL/SQL/PySpark) para o pipeline medalhão do caso piloto (Trip Data).

**Description:** Workflow DOWNSTREAM para gerar código e estrutura de execução com base em contracts aprovados (Gate 2).

**Workflow Type:** Non-document (code + docs)

---

## Workflow Structure

### Entry Point

```yaml
---
name: delivery
description: Geração de DDL/SQL/PySpark para o pipeline
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/delivery'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | inputs | Validar inputs (contracts, plataforma, layouts) |
| 02 | ddl | Gerar DDL das tabelas (LND/REF/SILVER/GOLD) |
| 03 | ingest | Gerar ingestão (CSV/Parquet/TSV/JSON) |
| 04 | transforms | Gerar transformações Silver/Gold + DQ checks |
| 05 | packaging | Organizar arquivos em pastas versionáveis |

---

## Workflow Inputs

### Required Inputs
- Plataforma (`platform_target`)
- Data contracts + modelo lógico aprovados (Gate 2)
- Definição do piloto Trip Data (tabelas e frequências)

### Optional Inputs
- Convenções de naming por cliente
- Implementação de observabilidade padrão

---

## Workflow Outputs

### Output Format
- [ ] Document-producing
- [x] Non-document

### Output Files
- `{artifacts_root}/{project_code}/implementation-artifacts/sql/`
- `{artifacts_root}/{project_code}/implementation-artifacts/pyspark/`
- `{artifacts_root}/{project_code}/implementation-artifacts/README.md`

---

## Agent Integration

### Primary Agent
- `data-engineer-exec`

### Other Agents
- `data-steward` (DQ/governance)
- `orchestrator` (Gate 2 compliance)

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
