# Workflow Specification: data-model

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/data-model/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Produzir modelo lógico, metadados, glossário e definições de métricas para o pipeline (medalhão).

**Description:** Workflow MIDSTREAM para definir o modelo consumível pela execução (Gate 2), com foco no caso piloto Trip Data.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: data-model
description: Modelo lógico, metadados e métricas
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/data-model'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | entities | Listar entidades/tabelas por camada (LND/SILVER/GOLD/REF) |
| 02 | keys-grain | Definir chaves, granularidade e relacionamentos |
| 03 | metrics | Definir métricas e fórmulas |
| 04 | metadata | Criar glossário e metadados |
| 05 | export | Gerar artefatos versionáveis |

---

## Workflow Inputs

### Required Inputs
- Arquitetura aprovada
- STTM

### Optional Inputs
- Dicionário de dados do cliente
- Regras adicionais de DQ

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/logical-model.md`
- `{artifacts_root}/{project_code}/planning-artifacts/metrics.md`
- `{artifacts_root}/{project_code}/planning-artifacts/metadata-glossary.md`

---

## Agent Integration

### Primary Agent
- `data-modeler`

### Other Agents
- `data-engineer-exec`
- `orchestrator`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
