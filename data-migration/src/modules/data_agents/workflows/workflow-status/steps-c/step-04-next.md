# Step 04 — next

## Objetivo

Sugerir o próximo agente/workflow, determinístico e baseado no estado e gates.

## Instruções

1) Leia a seção `## Estado atual` e `## Gates` do `status.md`.

2) Adicione uma seção `## Próximo passo sugerido` com:

   - Sugestão principal (1)
   - Alternativas (2–3)
   - Exatamente qual agente deve rodar (ex.: `data-strategist`, `business-analyst`, `data-solution-architect`, `orchestrator`) e qual workflow (ex.: `data-strategy`, `business-analysis`, etc.)

   Regras simples:

   - Se Gate 1 pendente → sugerir `data-strategist`/`business-analyst`
   - Se Gate 1 ok e Gate 2 pendente → sugerir `data-solution-architect`
   - Se Gate 2 ok e entrega pendente → sugerir `data-engineer-exec` + `delivery` / `unit-tests`

3) Finalize com `## Histórico` (append-only) registrando a execução do workflow-status (data + stream + sugestão).

4) Pare.
