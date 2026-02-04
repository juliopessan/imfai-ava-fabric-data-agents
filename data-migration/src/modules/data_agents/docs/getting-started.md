# Getting Started — Data & Agentic AI (BMAD-Data)

Este guia te ajuda a começar com o módulo `data_agents` e o piloto **Trip Data Pipeline**.

---

## O que este módulo faz

Fornece um conjunto de **agentes** e **workflows** para executar projetos de dados com:

- **Esteiras UP/MID/DOWN**
- **Gates obrigatórios** entre esteiras
- **Artefatos versionáveis** (Markdown + código) para auditoria e rastreabilidade

---

## Antes de começar

Tenha estes arquivos como referência:

- `PRD_Data_Agentic_AI_v2.md`
- `_bmad-output/planning-artifacts/architecture.md`

---

## Primeiros passos (sequência recomendada)

1. **UPSTREAM**
   - `data-strategy` → Problem Statement + KPIs
   - `business-analysis` → perguntas analíticas + STTM + DQ inicial
2. **Gate 1**
   - `gate-1-up-mid` → validar DoD do Gate 1
3. **MIDSTREAM**
   - `architecture` → AOD/DDS + decisões
   - `data-model` → modelo lógico + metadados + métricas
   - `agent-blueprint` + `agent-contracts` → contratos/guardrails
4. **Gate 2**
   - `gate-2-mid-down` → validar DoR do Gate 2
5. **DOWNSTREAM**
   - `delivery` → gerar DDL/SQL/PySpark
   - `unit-tests` → gerar testes
   - `governance` → monitoring spec + DQ rules
6. **Gate 3**
   - `gate-3-down-prod` → validar critérios finais

---

## Onde os outputs são gerados

O módulo pede (via `module.yaml`):

- `artifacts_root`
- `project_code`

O installer cria pastas como:

- `{artifacts_root}/{project_code}/planning-artifacts/`
- `{artifacts_root}/{project_code}/implementation-artifacts/`
- `{artifacts_root}/{project_code}/logs/`

---

## Próximo passo

Veja:
- [Agents Reference](agents.md)
- [Workflows Reference](workflows.md)
- [Examples](examples.md)
