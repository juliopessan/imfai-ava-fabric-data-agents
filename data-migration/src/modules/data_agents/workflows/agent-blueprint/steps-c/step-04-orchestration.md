# Step 04 — orchestration

## Objetivo

Definir regras de orquestração e gatilhos por artefato (roteamento determinístico).

## Instruções

1) Em `agent-blueprint.md`, adicione `## Regras de orquestração (artefato → próximo passo)`.

2) Defina regras simples em forma de lista/if-then, por exemplo:

   - Se não existe `problem-statement.md` → próximo: `data-strategist` / `data-strategy`
   - Se existe `problem-statement.md` e não existe `sttm.md` → próximo: `business-analyst` / `business-analysis`
   - Se Gate 1 PASS e não existe `architecture.md` → `data-solution-architect` / `architecture`
   - Se existe `architecture.md` e não existe `data-model.md` → `data-modeler` / `data-model`
   - Se Gate 2 PASS → `data-engineer-exec` / `delivery`

3) Pare e aguarde **[C] continuar**.

## Menu

- [C] Continuar para Step 05 (export)
- [X] Sair
