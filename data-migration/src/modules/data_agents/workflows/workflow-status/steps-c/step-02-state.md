# Step 02 — state

## Objetivo

Determinar o estado macro do projeto (UPSTREAM / MIDSTREAM / DOWNSTREAM) com base nos artefatos encontrados.

## Instruções

1) Leia o conteúdo atual de:

   - `{artifacts_root}/{project_code}/planning-artifacts/status.md`

2) Defina o estado baseada em sinais:

   - **UPSTREAM** se ainda faltam `problem-statement.md`/`kpis.md`/`analytical-questions.md`/`sttm.md`
   - **MIDSTREAM** se upstream está completo mas ainda faltam `architecture.md`/`data-model` outputs
   - **DOWNSTREAM** se `architecture.md` existe e contratos/modelos estão definidos **e** há evidência de execução, por exemplo:
     - existe `implementation-artifacts/` (qualquer conteúdo) **ou**
     - existe `gate-2-report.md` (PASS) **ou**
     - existe `delivery`/`unit-tests` outputs (ex.: `implementation-artifacts/sql|pyspark|tests`)

3) Atualize `status.md` adicionando:

   - `## Estado atual`
   - `- Stream: ...`
   - `- Evidências:` lista de arquivos que suportam a decisão

4) Pare aqui e aguarde o usuário indicar **[C] continuar** para o Step 03.

## Menu

- [C] Continuar para Step 03 (gates)
- [X] Sair
