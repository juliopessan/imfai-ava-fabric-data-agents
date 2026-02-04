# Step 02 — pick-next

## Objetivo

Selecionar próximo agente/workflow.

## Instruções

1) Aplique regras determinísticas:

   - Se faltam artefatos UPSTREAM → `data-strategist` (`data-strategy`) ou `business-analyst` (`business-analysis`)
   - Se upstream ok e falta `architecture.md` → `data-solution-architect` (`architecture`)
   - Se existe `architecture.md` e falta `data-model.md` → `data-modeler` (`data-model`)
   - Se Gate 2 passou → `data-engineer-exec` (`delivery`) e em paralelo `data-steward` (`governance`)
   - Se já há implementação → `orchestrator` (gates) ou `iteration-improvement` (backlog)

2) Gere uma recomendação principal + alternativas.

3) Pare e aguarde **[C] continuar**.

## Menu

- [C] Continuar para Step 03 (explain)
- [X] Sair
