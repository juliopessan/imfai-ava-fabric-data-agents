# Step 03 — gates

## Objetivo

Listar checks pendentes por gate (G1, G2, G3) para orientar bloqueios.

## Instruções

1) Atualize `status.md` adicionando uma seção `## Gates` com:

   - `### Gate 1 (UP→MID)`
   - `### Gate 2 (MID→DOWN)`
   - `### Gate 3 (DOWN→PROD)`

2) Para cada Gate, liste:

   - `✅` itens cumpridos (artefato existe)
   - `⏳` itens pendentes (artefato não existe)

   Sugestão mínima de checks (pode ajustar ao seu contexto):

   - Gate 1: `problem-statement.md`, `kpis.md`, `analytical-questions.md`, `sttm.md`, `dq-initial.md`
   - Gate 2: `architecture.md`, `data-model.md`, `agent-blueprint.md`, `agent-execution-contracts.md`, `dq-rules.md`, `monitoring-spec.md`
   - Gate 3: `implementation-artifacts/sql` e/ou `implementation-artifacts/pyspark`, `implementation-artifacts/tests`, `implementation-artifacts/README.md` (e `implementation-artifacts/gate-3-report.md` quando houver)

3) Pare aqui e aguarde o usuário indicar **[C] continuar** para o Step 04.

## Menu

- [C] Continuar para Step 04 (next)
- [X] Sair
