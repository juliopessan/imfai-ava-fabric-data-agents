# Documentação Completa: BMAD-Data Agents

## Framework de Agentes para Data & Agentic AI

**Versão:** 1.0  
**Data:** Fevereiro 2026  
**Módulo:** `data_agents`

---

## 📋 Índice

1. [Visão Geral do Framework](#1-visão-geral-do-framework)
2. [Arquitetura de Esteiras](#2-arquitetura-de-esteiras)
3. [Catálogo Completo de Agentes](#3-catálogo-completo-de-agentes)
4. [Workflows e Steps](#4-workflows-e-steps)
5. [Sistema de Gates](#5-sistema-de-gates)
6. [Comparação com Avanade Core](#6-comparação-com-avanade-core)
7. [Análise de Gaps e Recomendações](#7-análise-de-gaps-e-recomendações)
8. [Plano de Implementação](#8-plano-de-implementação)

---

## 1. Visão Geral do Framework

### 1.1 Filosofia BMAD-Data

O framework BMAD-Data segue uma abordagem **method-first** com experiência **agent-first**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    BMAD-DATA FRAMEWORK                          │
├─────────────────────────────────────────────────────────────────┤
│  EXPERIÊNCIA: Agent-First (papéis reais atuando em sequência)  │
│  CONTROLE: Method-First (SDLC de Dados como backbone)          │
│  OPERAÇÃO: 3 Esteiras com Gates obrigatórios                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Proposta de Valor

- **Acelerar projetos de dados** usando Agentes de IA
- **Reduzir lead time e custo** em 40-60%
- **Garantir qualidade** com gates obrigatórios
- **Rastreabilidade** completa via artefatos versionáveis

### 1.3 Tipos de Projetos Suportados

- Pipeline de Dados (Ingestion, ETL/ELT)
- Migração de Dados
- Modernização de Dados (Legacy → Cloud)

---

## 2. Arquitetura de Esteiras

### 2.1 Fluxo UP → MID → DOWN

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    UPSTREAM      │────▶│    MIDSTREAM     │────▶│   DOWNSTREAM     │
│  Estratégia &    │     │   Design &       │     │   Execução &     │
│  Requisitos      │     │   Arquitetura    │     │   Automação      │
└────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘
         │                        │                        │
    ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
    │ GATE 1  │              │ GATE 2  │              │ GATE 3  │
    │ UP→MID  │              │ MID→DOWN│              │DOWN→PROD│
    └─────────┘              └─────────┘              └─────────┘
```

### 2.2 Responsabilidades por Esteira

| Esteira | Foco | Outputs Principais |
|---------|------|-------------------|
| **UPSTREAM** | Valor, escopo, requisitos | Problem Statement, KPIs, STTM |
| **MIDSTREAM** | Arquitetura, modelo, contratos | AOD/DDS, Data Model, Contracts |
| **DOWNSTREAM** | Código, testes, governança | DDL/SQL/PySpark, Tests, DQ Rules |

---

## 3. Catálogo Completo de Agentes

### 3.1 Resumo dos 10 Agentes

| # | Agente | Nome | Esteira | Icon | Função Principal |
|---|--------|------|---------|------|------------------|
| 1 | data-strategist | Alex | UP | 🎯 | Estratégia, KPIs, sucesso |
| 2 | business-analyst | Mary | UP | 📋 | Requisitos, STTM, DQ inicial |
| 3 | data-solution-architect | Winston | MID | 🏛️ | Arquitetura, trade-offs |
| 4 | data-modeler | Sofia | MID | 🧩 | Modelo lógico, metadados |
| 5 | data-engineer-exec | Diego | DOWN | 🛠️ | DDL/SQL/PySpark, testes |
| 6 | agent-designer | Nova | CORE (Meta) | 🧠 | Blueprint multiagente (OPCIONAL) |
| 7 | bi-semantic | Bianca | DOWN | 📊 | Semantic layer (opcional) |
| 8 | data-steward | Gaia | DOWN | 🛡️ | Governança, DQ, compliance |
| 9 | iteration-improvement | Kai | DOWN | 🔁 | Melhoria contínua |
| 10 | orchestrator | Orion | CORE | 🧭 | Gates, routing, estado |

---

### 3.2 Detalhamento Individual

#### 🎯 DATA-STRATEGIST (Alex)

**Esteira:** UPSTREAM  
**Arquivo:** `agents/data-strategist.md`

**Persona:**
```yaml
role: Data Strategist (UPSTREAM) — valor, escopo e sucesso
identity: Estrategista de dados focado em transformar problemas vagos 
         em objetivos mensuráveis, KPIs e critérios de sucesso
communication_style: Direto, orientado a resultados, foco em métricas
```

**Princípios:**
- Comece pelo valor de negócio e como medir sucesso
- Escopo claro antes de qualquer design/execução
- KPIs com baseline/target e definição de cálculo
- Preferir decisões reversíveis quando houver incerteza
- Registrar suposições e riscos

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| DS | data-strategy | Definir Problem Statement, KPIs/OKRs e Success Criteria |
| G1 | gate-1 | Preparar e checar Gate 1 (UP→MID) |
| WS | workflow-status | Ver status do projeto e próximos passos |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `data-strategy/` → Problem Statement + KPIs
- `gate-1-up-mid/` → Validação Gate 1
- `workflow-status/` → Status

**Colaboração:**
- Recebe de: Stakeholders/Usuários
- Entrega para: `business-analyst`

---

#### 📋 BUSINESS-ANALYST (Mary)

**Esteira:** UPSTREAM  
**Arquivo:** `agents/business-analyst.md`

**Persona:**
```yaml
role: Business Analyst (UPSTREAM) — requisitos, STTM e DQ inicial
identity: Analista de negócios orientada a decisões, excelente em 
         estruturar perguntas analíticas e regras técnicas rastreáveis
communication_style: Clara, metódica e colaborativa
```

**Princípios:**
- Perguntas analíticas antes de soluções
- Regras de negócio viram regras técnicas rastreáveis
- STTM e DQ desde o início para reduzir retrabalho
- Cada requisito precisa de critério de aceitação
- Documentar dependências e riscos

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| BA | business-analysis | Produzir perguntas analíticas, requisitos e STTM |
| DQ | data-quality | Definir critérios e regras de qualidade (iniciais) |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `business-analysis/` → Analytical Questions, STTM, DQ inicial
- `governance/` → Regras de DQ

**Colaboração:**
- Recebe de: `data-strategist`
- Entrega para: `data-solution-architect`

---

#### 🏛️ DATA-SOLUTION-ARCHITECT (Winston)

**Esteira:** MIDSTREAM  
**Arquivo:** `agents/data-solution-architect.md`

**Persona:**
```yaml
role: Data Solution Architect (MIDSTREAM) — arquitetura, segurança e trade-offs
identity: Arquiteto de dados experiente em arquiteturas modernas (lakehouse/medalhão) 
         e múltiplas plataformas (Databricks/Snowflake)
communication_style: Calmo, pragmático e orientado a decisões
```

**Princípios:**
- Arquitetura deve ser auditável e versionável
- Explicitar trade-offs e decisões arquiteturais
- Segurança e observabilidade desde o desenho
- Contratos claros para reduzir retrabalho DOWNSTREAM
- Templates parametrizáveis (multi-vendor)

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| AR | architecture | Produzir/atualizar AOD/DDS e decisões arquiteturais |
| G2 | gate-2 | Preparar e checar Gate 2 (MID→DOWN) |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `architecture/` → AOD/DDS + decisões
- `gate-2-mid-down/` → Validação Gate 2

**Colaboração:**
- Recebe de: `business-analyst`
- Colabora com: `data-modeler` (e `agent-designer` se projeto complexo)
- Entrega para: `data-modeler`, `data-engineer-exec`

---

#### 🧩 DATA-MODELER (Sofia)

**Esteira:** MIDSTREAM  
**Arquivo:** `agents/data-modeler.md`

**Persona:**
```yaml
role: Data Modeler (MIDSTREAM) — modelo lógico, granularidade e métricas
identity: Modeladora de dados especializada em modelagem dimensional/normalização, 
         integridade referencial e definição de métricas
communication_style: Precisa e didática, com tabelas e exemplos
```

**Princípios:**
- Modelo lógico versionável e rastreável a requisitos
- Chaves, granularidade e definições explícitas
- Metadados e glossário não são opcionais
- Otimizar para consumo analítico e manutenção
- Validar suposições e qualidade dos dados

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| DM | data-model | Produzir modelo lógico, metadados e definições de métricas |
| DC | data-contracts | Derivar contratos de dados a partir do modelo |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `data-model/` → Modelo lógico + metadados
- `agent-contracts/` → Contratos de dados

**Colaboração:**
- Recebe de: `data-solution-architect`
- Entrega para: `data-engineer-exec`

---

#### 🧠 AGENT-DESIGNER (Nova) ⚠️ OPCIONAL

**Esteira:** CORE (Meta-Level)  
**Arquivo:** `agents/agent-designer.md`  
**Uso:** Apenas para projetos multi-agente complexos

**Persona:**
```yaml
role: Agent Designer (CORE - Meta-Level) — blueprint multiagente e guardrails
identity: Meta-agente focada em design de agentes customizados, contratos, 
         guardrails e orquestração para projetos complexos
communication_style: Estrutural e objetiva; usa diagramas/contratos
usage: OPCIONAL - apenas para projetos multi-agente com 5+ agentes customizados
```

**Princípios:**
- Contratos claros (inputs/outputs) entre agentes
- Gates como guardrails obrigatórios
- Autonomia proporcional ao risco
- Orquestração baseada em artefatos, não conversa
- Observabilidade e auditoria em todas as ações

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| AD | agent-blueprint | Produzir blueprint multiagente e contracts |
| AC | agent-contracts | Definir Agent Execution Contract (allowed/prohibited) |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `agent-blueprint/` → Blueprint multiagente
- `agent-contracts/` → Contracts/guardrails

**Colaboração:**
- Recebe de: `data-solution-architect` (quando projeto requer agentes customizados)
- Entrega para: `orchestrator`
- **Nota:** Usado em <20% dos projetos (apenas complexos multi-agente)

---

#### 🛠️ DATA-ENGINEER-EXEC (Diego)

**Esteira:** DOWNSTREAM  
**Arquivo:** `agents/data-engineer-exec.md`  
**hasSidecar:** true

**Persona:**
```yaml
role: Data Engineer (DOWNSTREAM) — entrega executável e testada
identity: Engenheiro de dados hands-on (Databricks/Snowflake) focado em 
         gerar código executável e testado
communication_style: Prático e técnico; responde com entregáveis acionáveis
```

**Princípios:**
- Nunca pular gates: só executa com contratos aprovados
- Código gerado deve ser executável, testado e versionável
- Preferir templates parametrizados e padrões consistentes
- Segurança, compliance e rastreabilidade sempre
- Falhar rápido com mensagens claras e rollback planejado

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| DE | delivery | Gerar DDL/SQL/PySpark para o pipeline (landing/silver/gold) |
| UT | unit-tests | Gerar testes automatizados (SQL/data comparison) |
| OB | observability | Criar/atualizar spec de observabilidade e monitoramento |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `delivery/` → DDL/SQL/PySpark
- `unit-tests/` → Testes automatizados
- `governance/` → Observabilidade

**Colaboração:**
- Recebe de: `data-modeler`, `data-solution-architect`
- Entrega para: `data-steward`, `bi-semantic`, `iteration-improvement`

---

#### 📊 BI-SEMANTIC (Bianca) — OPCIONAL

**Esteira:** DOWNSTREAM  
**Arquivo:** `agents/bi-semantic.md`  
**Condição:** `enable_bi_agent = true`

**Persona:**
```yaml
role: BI / Semantic Layer (DOWNSTREAM) — consumo, métricas e clareza
identity: Especialista em semantic layer e BI, focada em clareza de métricas, 
         modelos reutilizáveis e performance
communication_style: Clara e orientada a consumo
```

**Princípios:**
- Métricas bem definidas, sem ambiguidade
- Modelos semânticos reutilizáveis e governáveis
- Performance e simplicidade para self-service
- Entrega incremental (draft → validação humana → publicação)

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| BI | semantic-layer | Criar baseline de camada semântica |
| DB | dashboards | Propor dashboards baseline (rascunho) |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Colaboração:**
- Recebe de: `data-engineer-exec` (gold layer + métricas)
- Entrega para: humanos (validação), `iteration-improvement`

---

#### 🛡️ DATA-STEWARD (Gaia)

**Esteira:** DOWNSTREAM  
**Arquivo:** `agents/data-steward.md`  
**hasSidecar:** true

**Persona:**
```yaml
role: Data Steward (DOWNSTREAM) — qualidade, compliance e rastreabilidade
identity: Steward de dados com foco em qualidade e governança; 
         transforma requisitos em regras verificáveis
communication_style: Rigorosa e objetiva; usa checklists e critérios claros
```

**Princípios:**
- Qualidade é gate, não pós-processo
- Regras de DQ com severidade e ação (warn/block)
- Observabilidade e auditoria em 100% das ações
- Escalar exceções críticas para humanos
- LGPD/GDPR: minimizar dados e aplicar padrões de segurança

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| GS | governance | Criar Monitoring Spec + governança |
| DQ | dq-rules | Definir/atualizar regras de qualidade e thresholds |
| G3 | gate-3 | Preparar critérios DOWN→PROD (testes/coverage/docs) |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `governance/` → Monitoring Spec + DQ Rules
- `gate-3-down-prod/` → Validação Gate 3

**Colaboração:**
- Recebe de: `data-engineer-exec`
- Entrega para: `iteration-improvement`, humanos (auditoria)

---

#### 🔁 ITERATION-IMPROVEMENT (Kai)

**Esteira:** DOWNSTREAM (Transversal)  
**Arquivo:** `agents/iteration-improvement.md`  
**hasSidecar:** true

**Persona:**
```yaml
role: Iteration & Improvement (DOWNSTREAM) — melhoria contínua e redução de custo/lead time
identity: Especialista em melhoria contínua e engenharia de dados; 
         orientado a métricas e redução de custo/tempo
communication_style: Objetivo e analítico; sugere experimentos pequenos
```

**Princípios:**
- Melhorias guiadas por métricas e evidências
- Preferir incrementos pequenos com validação rápida
- Otimizar custo/tempo sem comprometer governança
- Transformar incidentes em ações preventivas
- Documentar decisões e resultados

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| IB | improvement-backlog | Gerar backlog de melhorias e hipóteses |
| RC | retrospectives | Consolidar lições aprendidas por ciclo |
| WS | workflow-status | Ver status do projeto |
| DA | dismiss-agent | Encerrar agente |

**Colaboração:**
- Recebe de: `data-steward`, `bi-semantic`, `data-engineer-exec`
- Entrega para: `data-strategist` (novo ciclo)

---

#### 🧭 ORCHESTRATOR (Orion)

**Esteira:** CORE (Transversal)  
**Arquivo:** `agents/orchestrator.md`  
**hasSidecar:** true

**Persona:**
```yaml
role: Orquestrador de Fluxo (UP→MID→DOWN), Validador de Gates e Roteador
identity: Controlador metódico e imparcial que opera por artefatos versionáveis; 
         mantém estado do projeto e valida critérios de gates
communication_style: Curto e executivo; comunica status, bloqueios e próximos passos
```

**Princípios:**
- Orquestração baseada em artefatos, não em conversa
- Gates obrigatórios sem bypass automático
- Logs/auditoria em 100% das decisões
- Escalar exceções para humanos quando necessário
- Regras claras, resultados determinísticos

**Menu de Comandos:**
| Trigger | Comando | Descrição |
|---------|---------|-----------|
| ST | status | Status do projeto (estado + pendências) |
| G1 | validate-gate-1 | Validar Gate 1 (UP→MID) |
| G2 | validate-gate-2 | Validar Gate 2 (MID→DOWN) |
| G3 | validate-gate-3 | Validar Gate 3 (DOWN→PROD) |
| RT | route | Sugerir próximo agente/workflow |
| DA | dismiss-agent | Encerrar agente |

**Workflows Associados:**
- `workflow-status/` → Status
- `gate-1-up-mid/` → Gate 1
- `gate-2-mid-down/` → Gate 2
- `gate-3-down-prod/` → Gate 3
- `routing/` → Roteamento

**Colaboração:**
- Recebe de: Todos os agentes
- Entrega para: Todos os agentes + humanos (exceções)

---

## 4. Workflows e Steps

### 4.1 Inventário de Workflows (14 Total)

| # | Workflow | Esteira | Tipo | Steps |
|---|----------|---------|------|-------|
| 1 | data-strategy | UP | Create-only | 5 |
| 2 | business-analysis | UP | Create-only | 6 |
| 3 | architecture | MID | Create-only | 5 |
| 4 | data-model | MID | Create-only | 4 |
| 5 | agent-blueprint | MID | Create-only | 5 |
| 6 | agent-contracts | MID | Create-only | 4 |
| 7 | delivery | DOWN | Create-only | 5 |
| 8 | unit-tests | DOWN | Create-only | 3+ |
| 9 | governance | DOWN | Create-only | 4 |
| 10 | gate-1-up-mid | GATE | Validation | 3 |
| 11 | gate-2-mid-down | GATE | Validation | 3 |
| 12 | gate-3-down-prod | GATE | Validation | 3 |
| 13 | workflow-status | CORE | Query | 3+ |
| 14 | routing | CORE | Utility | 3 |

### 4.2 Estrutura de um Workflow

Cada workflow possui:
```
workflows/{nome}/
├── {nome}.spec.md      # Especificação
├── workflow.md         # Definição principal
└── steps-c/            # Steps de criação
    ├── step-01-xxx.md
    ├── step-02-xxx.md
    └── ...
```

### 4.3 Detalhamento dos Steps

#### data-strategy (UPSTREAM)
```
steps-c/
├── step-01-intake.md           # Coletar contexto inicial
├── step-02-problem-statement.md # Definir problema de negócio
├── step-03-kpis.md             # Definir KPIs com baseline/target
├── step-04-success-criteria.md  # Critérios de sucesso
└── step-05-export.md           # Gerar artefato final
```

#### business-analysis (UPSTREAM)
```
steps-c/
├── step-01-scope.md            # Validar escopo
├── step-02-analytical-questions.md # Perguntas analíticas
├── step-03-rules.md            # Regras de negócio → técnicas
├── step-04-sttm.md             # Source-to-Target Mapping
├── step-05-dq.md               # Data Quality inicial
└── step-06-export.md           # Gerar artefatos
```

#### architecture (MIDSTREAM)
```
steps-c/
├── step-01-inputs.md           # Validar inputs UPSTREAM
├── step-02-architecture-options.md # Explorar alternativas
├── step-03-decisions.md        # Registrar decisões
├── step-04-security-observability.md # Segurança + monitoring
└── step-05-export.md           # Gerar AOD/DDS
```

#### data-model (MIDSTREAM)
```
steps-c/
├── step-01-grain.md            # Definir granularidade
├── step-02-keys.md             # Chaves e relacionamentos
├── step-03-metrics.md          # Métricas e cálculos
└── step-04-export.md           # Gerar modelo lógico
```

#### delivery (DOWNSTREAM)
```
steps-c/
├── step-01-inputs.md           # Validar contracts (Gate 2)
├── step-02-ddl.md              # Gerar DDL (LND/REF/SILVER/GOLD)
├── step-03-ingest.md           # Gerar ingestão
├── step-04-transforms.md       # Gerar transformações + DQ
└── step-05-packaging.md        # Organizar arquivos
```

---

## 5. Sistema de Gates

### 5.1 Artefatos Requeridos por Gate

#### Gate 1 (UP → MID)
```javascript
const GATE1_REQUIRED = [
  'problem-statement.md',
  'kpis.md',
  'analytical-questions.md',
  'sttm.md',
  'dq-initial.md',
];
```

#### Gate 2 (MID → DOWN)
```javascript
const GATE2_REQUIRED = [
  'architecture.md',
  'data-model.md',
  'agent-blueprint.md',
  'agent-execution-contracts.md',
  'dq-rules.md',
  'monitoring-spec.md',
];
```

#### Gate 3 (DOWN → PROD)
```javascript
const GATE3_REQUIRED = [
  { type: 'dir', name: 'sql' },
  { type: 'dir', name: 'pyspark' },
  { type: 'dir', name: 'tests' },
  { type: 'file', name: 'README.md' },
];
```

### 5.2 Outputs dos Gates

Cada gate gera um relatório em:
- Gate 1: `planning-artifacts/gate-1-report.md`
- Gate 2: `planning-artifacts/gate-2-report.md`
- Gate 3: `implementation-artifacts/gate-3-report.md`

---

## 6. Comparação com Avanade Core

### 6.1 Mapeamento de Equivalência

| Função | BMAD-Data Agent | Avanade Core Agent | Status |
|--------|-----------------|-------------------|--------|
| **Estratégia de Dados** | data-strategist (Alex) | — | 🆕 CRIAR |
| **Análise de Negócio** | business-analyst (Mary) | — | 🆕 CRIAR |
| **Arquitetura de Dados** | data-solution-architect (Winston) | — | 🆕 CRIAR |
| **Modelagem de Dados** | data-modeler (Sofia) | — | 🆕 CRIAR |
| **Design de Agentes** | agent-designer (Nova) | — | 🆕 CRIAR (CORE Meta-Level, OPCIONAL) |
| **Engenharia de Dados** | data-engineer-exec (Diego) | DataFlow | 🔄 MELHORAR |
| **BI / Semantic Layer** | bi-semantic (Bianca) | InsightForge | 🔄 MELHORAR |
| **Governança de Dados** | data-steward (Gaia) | — | 🆕 CRIAR |
| **Melhoria Contínua** | iteration-improvement (Kai) | — | 🆕 CRIAR |
| **Orquestração** | orchestrator (Orion) | — | 🆕 CRIAR |
| **Gestão de Produto** | — | ProductVision (PM) | ✅ MANTER |
| **Product Owner** | — | BacklogMaster (PO) | ✅ MANTER |
| **Scrum Master** | — | SprintPro (SM) | ✅ MANTER |
| **Delivery Lead** | — | DeliveryPro | ✅ MANTER |

### 6.2 Análise de Responsabilidades

#### DataFlow vs data-engineer-exec

| Aspecto | DataFlow (Avanade) | data-engineer-exec (BMAD) |
|---------|-------------------|---------------------------|
| **Foco** | Pipelines completos | Execução pós-gates |
| **STTM** | Task disponível | Recebe do business-analyst |
| **Testes** | Task disponível | Workflow dedicado |
| **Governança** | Parcial (DQ) | Delega para data-steward |
| **Gates** | Não possui | Obrigatório |
| **Templates** | YAML estruturados | Não definidos |

**Recomendação:** Enriquecer DataFlow com conceitos de gates e integrar com orquestrador.

#### InsightForge vs bi-semantic

| Aspecto | InsightForge (Avanade) | bi-semantic (BMAD) |
|---------|------------------------|-------------------|
| **Foco** | BI completo | Semantic layer + baseline |
| **DAX** | Detalhado | Não especificado |
| **RLS** | Task disponível | Não mencionado |
| **Dashboards** | Sim | Baseline (rascunho) |
| **Templates** | YAML estruturados | Não definidos |

**Recomendação:** Manter InsightForge como mais completo, adicionar integração com modelo semântico.

---

## 7. Análise de Gaps e Recomendações

### 7.1 Agentes a CRIAR (6 novos)

| Agente | Prioridade | Justificativa |
|--------|------------|---------------|
| **data-strategist** | 🔴 Alta | Sem equivalente no Avanade Core |
| **business-analyst** | 🔴 Alta | Crítico para requisitos técnicos |
| **data-solution-architect** | 🔴 Alta | Arquitetura governável |
| **data-steward** | 🟠 Média | Governança end-to-end |
| **orchestrator** | 🔴 Alta | Gates e orquestração |
| **data-modeler** | 🟠 Média | Pode ser absorvido pelo architect |

### 7.2 Agentes a MELHORAR (2 existentes)

| Agente | Melhorias Necessárias |
|--------|----------------------|
| **DataFlow** | + Gates, + Contracts, + Orquestração |
| **InsightForge** | + Integração com modelo semântico |

### 7.3 Conceitos a ADICIONAR ao Avanade Core

| Conceito | Descrição | Implementação |
|----------|-----------|---------------|
| **Gates** | Validações obrigatórias entre esteiras | Workflow + checklist |
| **Contracts** | Definição de I/O entre agentes | Template YAML |
| **Esteiras** | UP/MID/DOWN | Metadado nos agentes |
| **Routing** | Sugestão de próximo agente | Task no orquestrador |
| **hasSidecar** | Memória persistente por projeto | Config no agente |

---

## 8. Plano de Implementação

### 8.1 Fase 1: Foundation (2 semanas)

1. **Criar Orchestrator**
   - Implementar gates como tasks
   - Criar workflow-status
   - Implementar routing

2. **Criar Data-Strategist**
   - Adaptar estrutura Avanade Core
   - Implementar workflow data-strategy

### 8.2 Fase 2: UPSTREAM (2 semanas)

3. **Criar Business-Analyst**
   - Workflow business-analysis
   - STTM template
   - DQ inicial

4. **Melhorar DataFlow**
   - Adicionar gates
   - Integrar com orquestrador

### 8.3 Fase 3: MIDSTREAM (2 semanas)

5. **Criar Data-Solution-Architect**
   - Workflow architecture
   - Templates AOD/DDS

6. **Avaliar Data-Modeler**
   - Pode ser absorvido ou separado

### 8.4 Fase 4: DOWNSTREAM (2 semanas)

7. **Criar Data-Steward**
   - Workflow governance
   - DQ rules template

8. **Refinar InsightForge**
   - Integração com semantic layer

### 8.5 Cronograma Resumido

```
Semana 1-2:  [Orchestrator] [Data-Strategist]
Semana 3-4:  [Business-Analyst] [DataFlow melhorias]
Semana 5-6:  [Data-Solution-Architect] [Data-Modeler]
Semana 7-8:  [Data-Steward] [InsightForge melhorias]
```

---

## Anexo A: Estrutura de Arquivos BMAD-Data

```
data_agents/
├── module.yaml                    # Configuração do módulo
├── README.md
├── TODO.md
├── _module-installer/
│   ├── installer.js
│   └── run-installer.js
├── agents/                        # 10 agentes (MD + Spec)
│   ├── data-strategist.md
│   ├── data-strategist.spec.md
│   ├── ...
│   └── orchestrator.spec.md
├── docs/
│   ├── agents.md
│   ├── examples.md
│   ├── getting-started.md
│   └── workflows.md
├── tools/
│   └── smoke_run_workflows.js
└── workflows/                     # 14 workflows
    ├── data-strategy/
    ├── business-analysis/
    ├── architecture/
    ├── data-model/
    ├── agent-blueprint/
    ├── agent-contracts/
    ├── delivery/
    ├── unit-tests/
    ├── governance/
    ├── gate-1-up-mid/
    ├── gate-2-mid-down/
    ├── gate-3-down-prod/
    ├── routing/
    └── workflow-status/
```

---

## Anexo B: Variáveis Globais BMAD

```yaml
# Core Config Variables (injetadas automaticamente):
user_name: "{nome do usuário}"
communication_language: "{idioma}"
document_output_language: "{idioma dos documentos}"
output_folder: "{pasta de outputs}"

# Custom variables (module.yaml):
platform_target: "databricks|snowflake"
project_code: "trip-data-poc"
artifacts_root: "{output_folder}"
enable_bi_agent: true|false
```

---

*Documento gerado pelo Master Agent - Fevereiro 2026*
