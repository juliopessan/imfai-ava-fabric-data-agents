# Step 01 — scan

## Objetivo

Identificar artefatos existentes (planning/implementation) e capturar um inventário com timestamps (se disponíveis).

## Entradas necessárias

- `{artifacts_root}`
- `{project_code}`

## Instruções

1) Resolva o caminho raiz do projeto (pasta do repositório) e **localize** a pasta de artefatos:

   - `ARTIFACTS_ROOT = {artifacts_root}`
   - `PROJECT = {project_code}`
   - `PROJECT_ROOT = ARTIFACTS_ROOT/PROJECT`
   - `PLANNING = PROJECT_ROOT/planning-artifacts`
   - `IMPLEMENTATION = PROJECT_ROOT/implementation-artifacts`
   - `LOGS = PROJECT_ROOT/logs`

2) Faça um scan dos diretórios acima (crie uma lista) e categorize:

   - Planning artifacts existentes (nomes de arquivo)
   - Implementation artifacts existentes (nomes de arquivo)
   - Logs existentes (nomes de arquivo)

3) Crie/atualize o arquivo:

   - `{artifacts_root}/{project_code}/planning-artifacts/status.md`

   Com:

   - Cabeçalho com data/hora (ISO)
   - Seção “Artefatos encontrados” (planning/implementation/logs)
   - Seção “Observações” com gaps óbvios (ex.: sem `problem-statement.md`, etc.)

   Checklist mínimo recomendado (para orientar os gaps):

   - UPSTREAM: `problem-statement.md`, `kpis.md`, `analytical-questions.md`, `sttm.md`, `dq-initial.md`
   - MIDSTREAM: `architecture.md`, `data-model.md`, `agent-blueprint.md`, `agent-execution-contracts.md`
   - GOVERNANCE: `dq-rules.md`, `monitoring-spec.md`
   - GATES: `gate-1-report.md`, `gate-2-report.md` (e `implementation-artifacts/gate-3-report.md` quando aplicável)

4) Pare aqui e aguarde o usuário indicar **[C] continuar** para o Step 02.

## Menu

- [C] Continuar para Step 02 (state)
- [X] Sair
