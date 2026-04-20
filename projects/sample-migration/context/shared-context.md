---
context_version: "1.0"
updated_at: "{{TIMESTAMP}}"
trace_id: "{{TRACE_ID}}"
---

# Shared Context — {{PROJECT_NAME}}

> Lido por todos os agentes no início de cada tarefa.
> Atualizado automaticamente pelo migration-coordinator após cada gate.

## Projeto
- **Nome**: {{PROJECT_NAME}}
- **Cliente**: {{CLIENT_NAME}}
- **Plataforma Origem**: {{SOURCE_PLATFORM}}
- **Plataforma Destino**: {{TARGET_PLATFORM}}
- **Tecnologia Legada**: {{LEGACY_TECHNOLOGY}}

## Status dos Gates
| Gate | Status | Score | Agente | Data |
|------|--------|-------|--------|------|
| Gate 1 | {{STATUS}} | {{SCORE}} | migration-coordinator | {{DATE}} |
| Gate 2 | {{STATUS}} | {{SCORE}} | migration-coordinator | {{DATE}} |
| Gate 3 | {{STATUS}} | {{SCORE}} | migration-coordinator | {{DATE}} |

## Outputs Disponíveis
```
projects/{{PROJECT_NAME}}/outputs/
├── upstream/            ← Gate 1 artifacts
├── midstream/           ← Gate 2 artifacts
├── downstream/          ← Gate 3 artifacts
└── summary/
```
