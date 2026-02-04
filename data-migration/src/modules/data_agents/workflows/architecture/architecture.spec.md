# Workflow Specification: architecture

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/architecture/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Definir e versionar a arquitetura de dados e decisões (AOD/DDS), incluindo segurança, observabilidade e trade-offs.

**Description:** Workflow MIDSTREAM para consolidar arquitetura governável e pronta para Gate 2.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: architecture
description: Arquitetura (AOD/DDS) e decisões técnicas
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/architecture'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | inputs | Consolidar inputs (STTM, DQ, constraints) |
| 02 | architecture-options | Explorar opções e trade-offs |
| 03 | decisions | Registrar decisões e rationale |
| 04 | security-observability | Definir segurança e observabilidade |
| 05 | export | Gerar artefato AOD/DDS |

---

## Workflow Inputs

### Required Inputs
- STTM + requisitos (do `business-analysis`)
- Plataforma alvo (`platform_target`)

### Optional Inputs
- Restrições do cliente/ambiente
- Padrões corporativos

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/architecture.md`

---

## Agent Integration

### Primary Agent
- `data-solution-architect`

### Other Agents
- `agent-designer`
- `data-modeler`
- `orchestrator`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
