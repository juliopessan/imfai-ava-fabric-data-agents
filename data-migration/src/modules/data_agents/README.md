# Data & Agentic AI — BMAD-Data

Agentes e workflows para acelerar projetos de dados (UP→MID→DOWN) com gates e contratos.

Framework BMAD-Data para pipelines, migração e modernização com auditabilidade e outputs versionáveis.

---

## Overview

Este módulo implementa um time de agentes + workflows que seguem o modelo de 3 esteiras:

- **UPSTREAM** — Estratégia & Requisitos
- **MIDSTREAM** — Design & Tradução Técnica
- **DOWNSTREAM** — Execução & Automação

O controle acontece via **gates obrigatórios** (Gate 1, 2 e 3) e por **artefatos versionáveis** (Markdown + código), integrando naturalmente com Git.

---

## Installation

Este repositório já contém o módulo em `src/modules/data_agents/`. Em um ambiente BMAD com CLI, a instalação normalmente é feita via comando de install do BMAD.

> Nota: a forma exata de instalação depende do CLI/runner BMAD disponível no seu ambiente.

---

## Quick Start

1. Comece pelo workflow **data-strategy** para gerar Problem Statement, KPIs e Success Criteria.
2. Execute **business-analysis** para perguntas analíticas, STTM e DQ inicial.
3. Siga para **architecture** e **data-model** (MIDSTREAM).
4. Valide **gate-2-mid-down** antes de gerar código com **delivery**.
5. Gere testes com **unit-tests** e valide **gate-3-down-prod**.

Para documentação detalhada, veja **[docs/](docs/)**.

---

## Components

### Agents (specs)

- `data-strategist` — Estratégia/KPIs (UPSTREAM)
- `business-analyst` — Requisitos/STTM/DQ inicial (UPSTREAM)
- `data-solution-architect` — AOD/DDS/decisões (MIDSTREAM)
- `data-modeler` — Modelo lógico/metadados/métricas (MIDSTREAM)
- `agent-designer` — Blueprint multiagente/contratos (MIDSTREAM)
- `data-engineer-exec` — Execução unificada (DOWNSTREAM)
- `bi-semantic` — BI/Semantic (opcional)
- `data-steward` — Governança/DQ/monitoramento (DOWNSTREAM)
- `iteration-improvement` — Melhoria contínua (DOWNSTREAM)
- `orchestrator` — Gates & routing (CORE)

> Observação: nesta etapa, os agentes estão definidos como **specs** (`.spec.md`). Use o workflow de **create-agent** para gerar os agentes finais.

### Workflows (specs)

- `data-strategy`
- `business-analysis`
- `architecture`
- `data-model`
- `agent-blueprint`
- `agent-contracts`
- `delivery`
- `unit-tests`
- `governance`
- `workflow-status`
- `gate-1-up-mid`
- `gate-2-mid-down`
- `gate-3-down-prod`
- `routing`

---

## Configuration

As opções de configuração do módulo ficam em `module.yaml`:

- `platform_target` (databricks/snowflake)
- `project_code` (ex.: `trip-data-poc`)
- `artifacts_root` (onde salvar artefatos)
- `enable_bi_agent` (habilita o agente opcional de BI)

---

## Module Structure

```
data_agents/
├── module.yaml
├── README.md
├── TODO.md
├── docs/
│   ├── getting-started.md
│   ├── agents.md
│   ├── workflows.md
│   └── examples.md
├── agents/
├── workflows/
└── _module-installer/
```

---

## Author

Criado via BMAD Module workflow.
