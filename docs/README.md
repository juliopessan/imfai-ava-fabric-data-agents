# 📚 Documentação

Documentação centralizada, relatórios e planos de projeto.

## Estrutura

### `reports/` — Relatórios de Execução

Relatórios da implementação da Data Migration Factory (TIER 1-3).

| Arquivo | Descrição |
|---------|-----------|
| `TIER1-COMPLETION-REPORT.md` | Relatório final de conclusão TIER 1 |
| `TIER1-FINAL-SUMMARY.md` | Sumário executivo TIER 1 |
| `TIER2-IMPLEMENTATION-SUMMARY.md` | Implementação de governança TIER 2 |
| `TIER2-PHASE2-SUMMARY.md` | Fase 2 de scripts de governança |
| `FINAL-INTEGRATION-REPORT.md` | Integração completa dos componentes |
| `CLEANUP-REPORT.md` | Limpeza e otimização de artefatos |
| `EXEC-SUMMARY.txt` | Sumário executivo geral |
| `INTEGRATION-COMPLETE.md` | Confirmação de integração |
| `WORKFLOW-INTEGRATION-STATUS.md` | Status de integração de workflows |
| `WORKFLOW-INTEGRATION-REPORT.json` | Dados estruturados de integração |
| `WORKFLOW-INTEGRATION-FINAL-STATUS.txt` | Status final de workflows |

### `project-plans/` — Planos & Documentação Estratégica

Documentação estratégica, checklists e análises de projeto.

| Arquivo | Descrição |
|---------|-----------|
| `PHASE-5-COMPLETION-SUMMARY.md` | Conclusão da Fase 5 |
| `PROJECT-COMPLETION-SUMMARY.md` | Sumário de conclusão geral do projeto |
| `REPOSITORY-STRUCTURE.md` | Mapa de estrutura do repositório |
| `INTEGRATION-CHECKLIST.md` | Checklist de integração |
| `BRADESCO-TIER1-EXECUTION-PLAN.md` | Plano de execução Bradesco TIER 1 |
| `BRADESCO-TIER1-VALIDATION-REPORT.md` | Validação Bradesco TIER 1 |
| `GAP-ANALYSIS-REPORT.md` | Análise de gaps de implementação |

### `_templates/` — Templates & Referência

Documentação de design, dashboards e padrões reutilizáveis.

## 🎯 Agentic Engineering Framework (v1.0 — 2026-06-16)

Implementação das recomendações de "The New SDLC with Vibe Coding" (Google, 2026).

| Documento | Propósito | Ação |
|-----------|----------|------|
| [IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md](./IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md) | 📋 **START HERE** — Overview de 5 recomendações + roadmap | New team member |
| [HARNESS-MANIFEST.md](./HARNESS-MANIFEST.md) | 🔧 Formaliza o harness como artefato primeira-classe | Architect review |
| [HARNESS-CHANGELOG.md](./HARNESS-CHANGELOG.md) | 📝 Append-only log de mudanças de harness com rationale | Change control |
| [OBSERVABILITY-AND-TRACES.md](./OBSERVABILITY-AND-TRACES.md) | 📊 Instrumentação com trace IDs, spans, cost attribution | SRE implementation |
| [HUMAN-AGENT-CHECKPOINTS.md](./HUMAN-AGENT-CHECKPOINTS.md) | ✅ Escalation automática (3-tier) baseada em scores | Process owner |
| `../src/shared/schemas/wave-config-extended.yaml` | 📌 Schema com skills versioning + specs executáveis | Wave architect |
| `../src/shared/schemas/spec-as-executable.md` | 🤖 Converte specs em validators (Gate 3) | QA lead |

**Roadmap:** 4 semanas (Skills Versioning → Observability → Checkpoints → Specs)

## Como Usar

1. **Agentic Engineering:** Comece em [IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md](./IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md)
2. **Relatórios:** Consulte `reports/` para histórico de execução
3. **Planejamento:** Veja `project-plans/` para decisões e análises
4. **Sumários Executivos:** Comece por `EXEC-SUMMARY.txt` para visão geral

## Estrutura de Referência

Para mais informações sobre a organização geral, veja:
- [`REPOSITORY-ORGANIZATION.md`](../REPOSITORY-ORGANIZATION.md) — Guia completo
- [`INDEX.md`](../INDEX.md) — Índice do projeto
- [`HARNESS-MANIFEST.md`](./HARNESS-MANIFEST.md) — DMF v3 foundation

---

**Última atualização:** 2026-06-09
