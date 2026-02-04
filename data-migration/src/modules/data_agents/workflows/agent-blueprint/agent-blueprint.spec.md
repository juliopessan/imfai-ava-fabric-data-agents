# Workflow Specification: agent-blueprint

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/agent-blueprint/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Consolidar blueprint multiagente (papéis, sequência, handoffs e artefatos) alinhado ao modelo UP→MID→DOWN.

**Description:** Workflow MIDSTREAM para transformar o PRD (agentes por esteira) em blueprint operacional com contratos e pontos de autonomia.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: agent-blueprint
description: Blueprint multiagente e orquestração por artefatos
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/agent-blueprint'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | roster | Confirmar roster de agentes e responsabilidades |
| 02 | contracts-io | Definir contratos de I/O e artefatos por etapa |
| 03 | autonomy | Definir limites de autonomia e escalação |
| 04 | orchestration | Definir regras de orquestração e gatilhos por artefato |
| 05 | export | Gerar blueprint versionável |

---

## Workflow Inputs

### Required Inputs
- PRD (seção de agentes e gates)
- Arquitetura (decisões de observabilidade/auditoria)

### Optional Inputs
- Convenções internas de projeto

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/agent-blueprint.md`

---

## Agent Integration

### Primary Agent
- `agent-designer`

### Other Agents
- `orchestrator`
- `data-solution-architect`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
