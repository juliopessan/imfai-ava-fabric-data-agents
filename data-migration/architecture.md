---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - PRD_Data_Agentic_AI_v2.md
workflowType: 'architecture'
project_name: 'Data_Agents'
user_name: 'F.a.almeida'
date: '2026-01-21'
---

# Architecture Decision Document
## Data & Agentic AI — Modelo Híbrido BMAD-Data

_Este documento é construído colaborativamente através de descoberta passo-a-passo. Seções são adicionadas conforme trabalhamos juntos em cada decisão arquitetural._

---

## Documento de Entrada

**PRD Utilizado:** PRD_Data_Agentic_AI_v2.md (v2.0 - 2026-01-21)

### Resumo do PRD

- **Proposta:** Framework de aceleração para projetos de dados usando Agentes de IA
- **Modelo:** Híbrido BMAD-Data com 3 esteiras (UPSTREAM, MIDSTREAM, DOWNSTREAM)
- **Agentes:** 9 agentes definidos por papel
- **Caso Piloto:** Trip Data Pipeline (Arquitetura Medalhão)
- **Prioridades:** Redução de Lead Time e Custo

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

| ID | Requisito | Implicação Arquitetural |
|----|-----------|------------------------|
| RF01 | Fluxo sequencial por agente | Orquestrador com state machine |
| RF02 | Gates obrigatórios | Sistema de validação de critérios |
| RF03 | Artefatos versionáveis | Integração Git nativa |
| RF04 | Trilha de auditoria | Sistema de logging estruturado |
| RF05 | Geração SQL/PySpark | Engine de code generation |
| RF06 | Geração DDL | Templates de schema parametrizados |
| RF07 | Testes automatizados | Framework de testes integrado |
| RF08 | Profiling automático | Análise estatística de dados |
| RF09 | DQ checks configuráveis | Motor de regras de qualidade |

**Non-Functional Requirements:**

| ID | Requisito | Constraint Arquitetural |
|----|-----------|------------------------|
| RNF01 | Auditabilidade 100% | Logging em todas as camadas |
| RNF02 | 10 projetos paralelos | Design stateless + queue-based |
| RNF03 | LGPD/GDPR | Data masking, consent, retention |
| RNF04 | <30s por interação | Async processing, caching |
| RNF05 | >99% uptime | Redundância, health checks |

**Scale & Complexity:**

- Primary domain: Backend + Data Engineering + AI/LLM
- Complexity level: Enterprise
- Estimated architectural components: 15-20

### Technical Constraints & Dependencies

| Dependência | Constraint |
|-------------|------------|
| LLM Provider | Latência de API, custos por token, rate limits |
| Git | Versionamento de todos artefatos |
| Plataformas de Dados | Multi-tenant, multi-vendor |
| Ambiente de Execução | Decisão pendente (Cloud/Local/Híbrido) |

### Cross-Cutting Concerns Identified

1. **Auditabilidade** — Logging estruturado em todos componentes
2. **Versionamento** — Git-based para artefatos, prompts, código
3. **Segurança** — LGPD/GDPR compliance, data masking
4. **Observabilidade** — Métricas, traces, alertas
5. **Adaptabilidade** — Templates parametrizáveis por plataforma

---

## Technical Stack Decisions

### Target Platforms (Multi-vendor)

| Plataforma | Outputs Suportados |
|------------|-------------------|
| **Databricks** | Spark SQL, PySpark |
| **Snowflake** | SQL (dialect-specific) |
| **Extensível** | Templates parametrizáveis |

### LLM Provider Strategy

- **Primary:** Azure OpenAI (GPT-5)
- **Fallback:** Múltiplos providers
- **Abstração:** Interface comum para troca de provider

### Agent Implementation

| Aspecto | Decisão |
|---------|---------|
| **Formato** | `agents.MD` — Declarativo, Plataforma Avanade |
| **Linguagem** | Python (scripts de geração) |
| **Versionamento** | Git-based |

### Execution Environment

- **Plataforma:** Azure (Avanade — pré-definida)
- **Foco:** Design de agentes, não infraestrutura
- **Deployment:** Importação via `agents.MD`

### Code Generation Outputs

- **SQL:** ANSI + dialetos (Snowflake, Databricks)
- **PySpark:** Templates nativos
- **Strategy:** Dual-output parametrizado

---

## Agents Architecture

### Architectural Scope

| Escopo | Descrição |
|--------|-----------|
| **In Scope** | Design detalhado de todos os 10 agentes |
| **Entregável** | Especificação `agents.MD` para cada agente |

### Agents Overview

| # | Esteira | Agente | Status |
|---|---------|--------|--------|
| 1 | UPSTREAM | Data Strategist / Product Agent | ✅ Documentado |
| 2 | UPSTREAM | Business Analyst Agent | ✅ Documentado |
| 3 | MIDSTREAM | Data Solution Architect Agent | ✅ Documentado |
| 4 | MIDSTREAM | Data Modeler Agent | ✅ Documentado |
| 5 | MIDSTREAM | Agent Design / AI Design Agent | ✅ Documentado |
| 6 | DOWNSTREAM | Data Engineer Execution Agent | ✅ Documentado |
| 7 | DOWNSTREAM | BI / Semantic Layer Agent | ✅ Documentado |
| 8 | DOWNSTREAM | Data Steward / Governance Agent | ✅ Documentado |
| 9 | DOWNSTREAM | Iteration & Improvement Agent | ✅ Documentado |
| 10 | CORE | **Orchestrator Agent** | ✅ Documentado |

---

## Agent Design Template

Cada agente será detalhado com a seguinte estrutura:

```markdown
### Agent: [Nome do Agente]

**Esteira:** [UP/MID/DOWN/CORE]
**Papel:** [Descrição do papel]

#### Inputs
- [Lista de inputs esperados]

#### Outputs
- [Lista de outputs gerados]

#### Contratos
- **Recebe de:** [Agentes anteriores]
- **Entrega para:** [Agentes seguintes]

#### Regras de Autonomia
- [O que pode fazer sozinho]
- [O que precisa de aprovação humana]

#### Prompts Base
- [Instruções principais]

#### Exemplo de `agents.MD`
[Estrutura do arquivo]
```

---

## 10. Orchestrator Agent

### Orchestrator Role

O Orquestrador é o componente central que:
- Observa artefatos (não conversas)
- Valida gates entre esteiras
- Controla transições UP → MID → DOWN
- Escala exceções para humanos
- Registra trilha de auditoria

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   WATCHER   │  │    GATE     │  │  TRANSITION │         │
│  │  (Artefatos)│  │  VALIDATOR  │  │  CONTROLLER │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         ▼                ▼                ▼                 │
│  ┌─────────────────────────────────────────────────┐       │
│  │              STATE MACHINE                       │       │
│  │  UP ──[Gate1]──▶ MID ──[Gate2]──▶ DOWN ──[G3]──▶│       │
│  └─────────────────────────────────────────────────┘       │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   AUDIT     │  │  EXCEPTION  │  │   ROUTING   │         │
│  │   LOGGER    │  │   HANDLER   │  │   ENGINE    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Orchestrator Components

| Componente | Responsabilidade |
|------------|------------------|
| **Watcher** | Monitora criação/atualização de artefatos |
| **Gate Validator** | Avalia critérios de cada gate (checklist) |
| **Transition Controller** | Autoriza ou bloqueia mudança de esteira |
| **State Machine** | Mantém estado atual do projeto (UP/MID/DOWN) |
| **Audit Logger** | Registra todas ações para rastreabilidade |
| **Exception Handler** | Escala para humano quando necessário |
| **Routing Engine** | Direciona para o próximo agente correto |

### Orchestrator Inputs
- Eventos de criação/atualização de artefatos
- Requisições de transição de gate
- Status reports dos agentes de execução

### Orchestrator Outputs
- Aprovação/rejeição de transição de gate
- Roteamento para próximo agente
- Logs de auditoria
- Alertas de exceção para humanos

### Orchestrator Contracts
- **Recebe de:** Todos os 9 agentes de execução
- **Entrega para:** Todos os 9 agentes de execução + Humanos (exceções)

### Orchestrator Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Validar critérios de gate | ✅ Autônomo |
| Aprovar transição (critérios OK) | ✅ Autônomo |
| Rejeitar transição (critérios NOK) | ✅ Autônomo |
| Rotear para próximo agente | ✅ Autônomo |
| Registrar logs | ✅ Autônomo |
| Rollback de estado | ⚠️ Requer aprovação humana |
| Bypass de gate | ⚠️ Requer aprovação humana |
| Mudança de regras de gate | ❌ Proibido |

---

## 1. Data Strategist / Product Agent

**Esteira:** UPSTREAM
**Papel:** Definir valor, escopo e sucesso do projeto de dados

### Inputs
- Problema de negócio (texto livre ou documento)
- Contexto organizacional
- Restrições conhecidas

### Outputs
- Problem Statement
- KPIs / OKRs
- Success Criteria
- Escopo inicial

### Contracts
- **Recebe de:** Humano (início do projeto)
- **Entrega para:** Business Analyst Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Fazer perguntas de clarificação | ✅ Autônomo |
| Sugerir KPIs | ✅ Autônomo |
| Definir KPIs finais | ⚠️ Requer validação humana |
| Definir escopo | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um Data Strategist especializado em definir valor de negócio para projetos de dados.
Seu objetivo é transformar problemas vagos em Problem Statements claros e mensuráveis.
Sempre pergunte sobre: impacto de negócio, stakeholders, métricas de sucesso, timeline.
```

---

## 2. Business Analyst Agent

**Esteira:** UPSTREAM
**Papel:** Traduzir negócio em requisitos analíticos e técnicos

### Inputs
- Problem Statement (do Data Strategist)
- KPIs definidos
- Contexto de dados disponíveis

### Outputs
- Analytical Questions
- Decision Requirements
- Regras Técnicas
- STTM (Source-to-Target Mapping)

### Contracts
- **Recebe de:** Data Strategist Agent
- **Entrega para:** Data Solution Architect Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Estruturar perguntas analíticas | ✅ Autônomo |
| Realizar profiling conceitual | ✅ Autônomo |
| Converter regras de negócio | ✅ Autônomo |
| Aprovar STTM final | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um Business Analyst especializado em traduzir necessidades de negócio em requisitos técnicos de dados.
Foque em: perguntas analíticas, regras de negócio, qualidade de dados, mapeamento fonte-destino.
Sempre documente premissas e dependências.
```

---

## 3. Data Solution Architect Agent

**Esteira:** MIDSTREAM
**Papel:** Definir a solução técnica ótima e governável

### Inputs
- STTM do Business Analyst
- Requisitos técnicos
- Restrições de plataforma

### Outputs
- Arquitetura de Dados
- AOD (Architecture Overview Document)
- DDS (Detailed Design Specification)
- Estratégia de Segurança e Observabilidade

### Contracts
- **Recebe de:** Business Analyst Agent
- **Entrega para:** Data Modeler Agent, Agent Design Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Explorar opções de arquitetura | ✅ Autônomo |
| Recomendar trade-offs | ✅ Autônomo |
| Definir arquitetura final | ⚠️ Requer validação humana |
| Escolher plataforma | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um Data Solution Architect com expertise em Databricks, Snowflake e arquiteturas modernas de dados.
Sempre considere: escalabilidade, custo, governança, segurança, observabilidade.
Documente trade-offs explicitamente.
```

---

## 4. Data Modeler Agent

**Esteira:** MIDSTREAM
**Papel:** Garantir coerência e qualidade do modelo de dados

### Inputs
- Arquitetura aprovada
- STTM
- Regras de negócio

### Outputs
- Modelo Lógico
- Definições de Métricas
- Metadados
- Glossário de dados

### Contracts
- **Recebe de:** Data Solution Architect Agent
- **Entrega para:** Data Engineer Execution Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Definir modelo lógico | ✅ Autônomo |
| Estabelecer relacionamentos | ✅ Autônomo |
| Detectar problemas de normalização | ✅ Autônomo |
| Aprovar modelo final | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um Data Modeler especializado em modelagem dimensional e normalização.
Foque em: integridade referencial, performance de queries, lineage, metadados.
Sempre documente decisões de modelagem.
```

---

## 5. Agent Design / AI Design Agent

**Esteira:** MIDSTREAM
**Papel:** Definir arquitetura multiagente e limites de autonomia

### Inputs
- Arquitetura de dados
- Requisitos de automação
- Regras de governança

### Outputs
- Blueprint Multiagente
- Agent Contracts
- Regras de Autonomia

### Contracts
- **Recebe de:** Data Solution Architect Agent
- **Entrega para:** Orchestrator Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Definir contratos I/O | ✅ Autônomo |
| Propor limites de autonomia | ✅ Autônomo |
| Aprovar regras finais | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um AI Design Architect especializado em sistemas multiagente.
Foque em: contratos claros, limites de autonomia, pontos de escalação humana.
Garanta que agentes não tenham poder excessivo.
```

---

## 6. Data Engineer Execution Agent

**Esteira:** DOWNSTREAM
**Papel:** Executar tecnicamente a solução conforme contratos aprovados

### Inputs
- Data Contracts
- Metric Contracts
- Arquitetura aprovada
- Modelo lógico

### Outputs
- SQL / DDL versionados
- Pipelines executáveis (PySpark)
- Testes automatizados
- Documentação técnica

### Contracts
- **Recebe de:** Data Modeler Agent, Data Solution Architect Agent
- **Entrega para:** BI Agent, Data Steward Agent

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Gerar SQL/PySpark | ✅ Autônomo |
| Gerar DDL | ✅ Autônomo |
| Gerar testes | ✅ Autônomo |
| Executar em produção | ❌ Requer aprovação humana |
| Modificar dados existentes | ❌ Requer aprovação humana |

### Prompts Base
```
Você é um Data Engineer especializado em Databricks e Snowflake.
Gere código SQL e PySpark seguindo best practices.
Sempre inclua: tratamento de erros, logging, testes unitários, documentação.
NUNCA execute código destrutivo sem aprovação.
```

---

## 7. BI / Semantic Layer Agent

**Esteira:** DOWNSTREAM (Opcional)
**Papel:** Disponibilizar camada analítica para consumo de negócio

### Inputs
- Modelo de dados Gold
- Definições de métricas
- Requisitos de visualização

### Outputs
- Modelo Semântico
- Dashboards baseline
- Medidas (DAX/etc)

### Contracts
- **Recebe de:** Data Engineer Execution Agent
- **Entrega para:** Humanos (usuários finais)

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Criar modelo semântico | ✅ Autônomo |
| Gerar medidas | ✅ Autônomo |
| Criar dashboards draft | ✅ Autônomo |
| Publicar para usuários | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um BI Developer especializado em camadas semânticas.
Crie modelos otimizados para self-service analytics.
Foque em: nomenclatura clara, hierarquias, medidas reutilizáveis.
```

---

## 8. Data Steward / Governance Agent

**Esteira:** DOWNSTREAM
**Papel:** Garantir qualidade, conformidade e rastreabilidade

### Inputs
- Pipelines executados
- Regras de DQ
- Requisitos de compliance

### Outputs
- Monitoring Spec
- Regras de Qualidade aplicadas
- Logs de Governança
- Relatórios de compliance

### Contracts
- **Recebe de:** Data Engineer Execution Agent
- **Entrega para:** Iteration Agent, Humanos (auditoria)

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Monitorar qualidade | ✅ Autônomo |
| Gerar alertas | ✅ Autônomo |
| Bloquear pipeline com DQ crítico | ✅ Autônomo |
| Aprovar exceções de DQ | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um Data Steward focado em qualidade e governança de dados.
Monitore: completude, consistência, conformidade, freshness.
Escale anomalias críticas imediatamente.
```

---

## 9. Iteration & Improvement Agent

**Esteira:** DOWNSTREAM
**Papel:** Evoluir continuamente a solução

### Inputs
- Métricas de performance
- Feedback de usuários
- Logs de erros
- Relatórios de governança

### Outputs
- Improvement Backlog
- Hipóteses Revisadas
- Recomendações de otimização

### Contracts
- **Recebe de:** Data Steward Agent, BI Agent
- **Entrega para:** Data Strategist Agent (novo ciclo)

### Autonomy Rules
| Ação | Autonomia |
|------|-----------|
| Analisar métricas | ✅ Autônomo |
| Identificar melhorias | ✅ Autônomo |
| Priorizar backlog | ⚠️ Requer validação humana |
| Iniciar novo ciclo | ⚠️ Requer validação humana |

### Prompts Base
```
Você é um especialista em melhoria contínua de soluções de dados.
Analise: performance, custos, feedback, erros.
Proponha melhorias incrementais e transformacionais.
```

---

## Core Architectural Decisions

### Decision Summary

| Categoria | Decisão | Rationale |
|-----------|---------|-----------|
| **Estrutura do Framework** | Por Esteira (UP/MID/DOWN) | Alinhado com modelo de 3 esteiras do PRD |
| **Formato de Contratos** | Markdown + Frontmatter | Consistente com `agents.MD` |
| **Templates de Código** | Jinja2 parametrizados | Padrão Python, multi-plataforma |
| **Engine de Templates** | Jinja2 | Nativo Python, flexível |

---

### Estrutura de Pastas do Framework

```
/data-agents-framework/
├── /agents/
│   ├── /upstream/
│   │   ├── data-strategist.agent.md
│   │   └── business-analyst.agent.md
│   ├── /midstream/
│   │   ├── data-architect.agent.md
│   │   ├── data-modeler.agent.md
│   │   └── agent-designer.agent.md
│   ├── /downstream/
│   │   ├── data-engineer.agent.md
│   │   ├── bi-semantic.agent.md
│   │   ├── data-steward.agent.md
│   │   └── iteration.agent.md
│   └── /core/
│       └── orchestrator.agent.md
├── /templates/
│   ├── /sql/
│   │   ├── /databricks/
│   │   └── /snowflake/
│   ├── /pyspark/
│   └── /tests/
├── /contracts/
│   ├── /data/
│   └── /metric/
├── /gates/
│   ├── gate-1-up-mid.md
│   ├── gate-2-mid-down.md
│   └── gate-3-down-prod.md
└── /outputs/
    └── /{project-name}/
```

---

### Formato de Contratos

**Data Contract Template:**

```markdown
---
contract_type: data
name: {{table_name}}
version: 1.0
status: draft | approved
owner: {{team}}
sla: {{frequency}}
platform: databricks | snowflake
---

# Data Contract: {{table_name}}

## Schema

| Column | Type | Nullable | PK | Description |
|--------|------|----------|-----|-------------|
| {{col}} | {{type}} | {{null}} | {{pk}} | {{desc}} |

## Data Quality Rules

| Rule | Threshold | Action |
|------|-----------|--------|
| Completeness | > 99% | Warn |
| Freshness | < 24h | Block |

## Lineage

- **Source:** {{source_table}}
- **Transformations:** {{transform_list}}
```

---

### Critérios dos Gates

#### Gate 1: UPSTREAM → MIDSTREAM

| Critério | Obrigatório | Validação |
|----------|-------------|-----------|
| Problem Statement documentado | ✅ | Arquivo existe |
| KPIs definidos (mín. 3) | ✅ | Contagem no doc |
| Escopo aprovado | ✅ | Flag de aprovação humana |
| Fontes de dados identificadas | ✅ | Lista não vazia |
| STTM inicial criado | ⚠️ | Opcional |

#### Gate 2: MIDSTREAM → DOWNSTREAM

| Critério | Obrigatório | Validação |
|----------|-------------|-----------|
| Arquitetura aprovada | ✅ | Flag de aprovação |
| Modelo lógico versionado | ✅ | Arquivo em Git |
| Data Contracts assinados | ✅ | Status = "approved" |
| DQ rules documentadas | ✅ | Arquivo existe |
| Plataforma definida | ✅ | Campo preenchido |

#### Gate 3: DOWNSTREAM → PRODUCTION

| Critério | Obrigatório | Validação |
|----------|-------------|-----------|
| Código em Git | ✅ | Branch/PR existe |
| Testes passando | ✅ | CI status = green |
| Cobertura > 80% | ✅ | Métrica de coverage |
| Documentação completa | ✅ | Arquivos existem |
| Aprovação humana | ✅ | Flag manual |

---

### Templates de Geração de Código

**Engine:** Jinja2 (Python)

**Estrutura:**

```
/templates/
├── /sql/
│   ├── /databricks/
│   │   ├── ddl_create_table.sql.j2
│   │   ├── dml_insert.sql.j2
│   │   └── dq_check.sql.j2
│   └── /snowflake/
│       ├── ddl_create_table.sql.j2
│       ├── dml_insert.sql.j2
│       └── dq_check.sql.j2
├── /pyspark/
│   ├── ingest_csv.py.j2
│   ├── ingest_parquet.py.j2
│   ├── transform_silver.py.j2
│   └── transform_gold.py.j2
└── /tests/
    ├── unit_test.sql.j2
    └── data_comparison.sql.j2
```

**Parâmetros Comuns:**

| Parâmetro | Descrição |
|-----------|-----------|
| `{{table_name}}` | Nome da tabela |
| `{{schema}}` | Schema/database |
| `{{columns}}` | Lista de colunas |
| `{{platform}}` | databricks / snowflake |
| `{{dq_rules}}` | Regras de qualidade |
| `{{sla}}` | SLA de freshness |

---

### Observabilidade e Auditoria

#### Logs

| Evento | Nível | Campos |
|--------|-------|--------|
| Agent started | INFO | agent_id, project_id, timestamp |
| Gate validation | INFO | gate_id, criteria, result |
| Gate transition | INFO | from_stage, to_stage, approved_by |
| Code generated | INFO | agent_id, artifact_type, lines |
| Human escalation | WARN | reason, agent_id, context |
| Error | ERROR | agent_id, error_type, stack |

#### Métricas

| Métrica | Tipo | Granularidade |
|---------|------|---------------|
| `lead_time_total` | Histogram | Por projeto |
| `gate_pass_rate` | Gauge | Por gate |
| `agent_execution_time` | Histogram | Por agente |
| `code_generation_count` | Counter | Por tipo |
| `human_escalation_rate` | Gauge | Por agente |

#### Alertas

| Condição | Severidade | Ação |
|----------|------------|------|
| Gate rejeitado 3x consecutivas | WARN | Notificar humano |
| Agent timeout > 30s | WARN | Retry + notificar |
| Erro em código gerado | ERROR | Bloquear + notificar |
| DQ crítico | ERROR | Bloquear pipeline |

---

