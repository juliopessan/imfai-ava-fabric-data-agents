# Step 02 — contracts-io

## Objetivo

Definir contratos de I/O e artefatos por etapa (handoffs por arquivo).

## Instruções

1) Em `agent-blueprint.md`, adicione `## Contratos de I/O por etapa`.

2) Para cada etapa (UP→MID→DOWN), descreva:

   - Entrada (artefatos esperados)
   - Saída (artefatos gerados)
   - Dono (agente primário)
   - Consumidores (agentes seguintes)

   Sugestão mínima:

   - data-strategy → `problem-statement.md`, `kpis.md`
   - business-analysis → `analytical-questions.md`, `sttm.md`, `dq-initial.md`
   - architecture → `architecture.md`
   - data-model → `data-model.md`
   - governance → `dq-rules.md`, `monitoring-spec.md`
   - gate-2 → `gate-2-report.md`
   - delivery → `implementation-artifacts/sql|pyspark`, `README.md`
   - unit-tests → `implementation-artifacts/tests`
   - gate-3 → `gate-3-report.md`

3) Pare e aguarde **[C] continuar**.

## Menu

- [C] Continuar para Step 03 (autonomy)
- [X] Sair
