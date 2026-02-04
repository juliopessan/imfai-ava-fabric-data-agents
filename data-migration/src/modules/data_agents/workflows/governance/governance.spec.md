# Workflow Specification: governance

**Module:** data_agents
**Status:** Generated — workflow file present (`workflows/governance/workflow.md`)
**Created:** 2026-01-21

---

## Workflow Overview

**Goal:** Definir Monitoring Spec, DQ rules, logs de governança e critérios para bloquear/alertar.

**Description:** Workflow DOWNSTREAM de governança e observabilidade para garantir auditabilidade (RNF01) e suporte aos gates.

**Workflow Type:** Document-producing

---

## Workflow Structure

### Entry Point

```yaml
---
name: governance
description: Governança, DQ e observabilidade
web_bundle: true
installed_path: '{project-root}/_bmad/data_agents/workflows/governance'
---
```

### Mode

- [x] Create-only (steps-c/)
- [ ] Tri-modal (steps-c/, steps-e/, steps-v/)

---

## Planned Steps

| Step | Name | Goal |
|------|------|------|
| 01 | dq-rules | Consolidar regras de DQ (thresholds + action) |
| 02 | observability | Definir logs, métricas e alertas |
| 03 | compliance | Checklist LGPD/GDPR e rastreabilidade |
| 04 | export | Gerar Monitoring Spec versionável |

---

## Workflow Inputs

### Required Inputs
- Regras de DQ iniciais (do `business-analysis`)
- Requisitos não-funcionais (RNF01-05)

### Optional Inputs
- Ferramentas de monitoramento alvo

---

## Workflow Outputs

### Output Format
- [x] Document-producing
- [ ] Non-document

### Output Files
- `{artifacts_root}/{project_code}/planning-artifacts/monitoring-spec.md`
- `{artifacts_root}/{project_code}/planning-artifacts/dq-rules.md`

---

## Agent Integration

### Primary Agent
- `data-steward`

### Other Agents
- `data-engineer-exec`
- `orchestrator`

---

## Implementation Notes

Use o workflow **create-workflow** (workflow-builder) para criar o workflow definitivo.

_Spec criada em 2026-01-21 via BMAD Module workflow_
