# 🔄 Workflows, Esteiras e Gates: Análise Detalhada

**Documento Complementar à Análise Comparativa**  
**Versão:** 1.0  
**Data:** 4 de Fevereiro de 2026  
**Autor:** Master Agent - Avanade Method

---

## 📑 Sumário

1. [Introdução](#1-introdução)
2. [Modelo de Esteiras BMAD-Data](#2-modelo-de-esteiras-bmad-data)
3. [Workflows por Esteira](#3-workflows-por-esteira)
4. [Sistema de Gates](#4-sistema-de-gates)
5. [Comparação: Agentes Existentes vs BMAD-Data](#5-comparação-agentes-existentes-vs-bmad-data)
6. [Contratos entre Esteiras](#6-contratos-entre-esteiras)
7. [Fluxo de Artefatos](#7-fluxo-de-artefatos)
8. [Implementação Prática](#8-implementação-prática)

---

## 1. Introdução

### 1.1 O Problema que as Esteiras Resolvem

Em projetos de dados tradicionais, o fluxo de trabalho frequentemente sofre de:

| Problema | Impacto | Solução das Esteiras |
|----------|---------|---------------------|
| Requisitos vagos pulam para código | Retrabalho 40%+ | Gate 1 obrigatório |
| Arquitetura não documentada | Débito técnico | Gate 2 com contracts |
| Código em produção sem testes | Incidentes | Gate 3 com cobertura mínima |
| Sem rastreabilidade | Auditoria impossível | Artefatos versionados |

### 1.2 Duas Filosofias de Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENTES EXISTENTES                                    │
│                    (Workflow Livre)                                      │
│                                                                          │
│    [Usuário] ──▶ [Escolhe Agente] ──▶ [*Comando] ──▶ [Artefato]        │
│         │                                    │                          │
│         │                                    │                          │
│         └────────── Loop Livre ──────────────┘                          │
│                                                                          │
│    ✅ Vantagem: Flexibilidade, velocidade                               │
│    ⚠️ Risco: Pode pular etapas importantes                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    BMAD-DATA                                             │
│                    (Workflow Controlado)                                 │
│                                                                          │
│    [UPSTREAM] ──G1──▶ [MIDSTREAM] ──G2──▶ [DOWNSTREAM] ──G3──▶ [PROD]  │
│         │                  │                   │                        │
│         │                  │                   │                        │
│    Strategist          Architect            Engineer                    │
│    Analyst             Modeler              Steward                     │
│                        Designer             BI                          │
│                                             Iterate                     │
│                                                                          │
│    ✅ Vantagem: Governança, rastreabilidade, qualidade                  │
│    ⚠️ Risco: Pode ser burocrático para tarefas simples                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Modelo de Esteiras BMAD-Data

### 2.1 Visão Geral das 3 Esteiras

O BMAD-Data organiza o SDLC de dados em **3 esteiras organizacionais**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   🟦 UPSTREAM              🟨 MIDSTREAM              🟥 DOWNSTREAM           │
│   Estratégia &             Design &                  Execução &              │
│   Requisitos               Tradução Técnica          Automação               │
│                                                                              │
│   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐         │
│   │ O QUÊ?      │          │ COMO?       │          │ FAZER!      │         │
│   │             │          │             │          │             │         │
│   │ • Problema  │          │ • Arquitet. │          │ • Código    │         │
│   │ • KPIs      │          │ • Modelo    │          │ • Testes    │         │
│   │ • Escopo    │          │ • Contracts │          │ • Deploy    │         │
│   │ • Requisitos│          │ • Trade-offs│          │ • Monitor   │         │
│   └─────────────┘          └─────────────┘          └─────────────┘         │
│                                                                              │
│        │                         │                         │                │
│        ▼                         ▼                         ▼                │
│   ┌─────────┐              ┌─────────┐              ┌─────────┐            │
│   │ GATE 1  │              │ GATE 2  │              │ GATE 3  │            │
│   │ UP→MID  │              │ MID→DOWN│              │DOWN→PROD│            │
│   └─────────┘              └─────────┘              └─────────┘            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Detalhamento por Esteira

#### 🟦 UPSTREAM — Estratégia & Requisitos

**Objetivo:** Garantir que o problema está claro antes de investir em solução técnica.

| Aspecto | Descrição |
|---------|-----------|
| **Foco** | Valor de negócio, não tecnologia |
| **Pergunta-chave** | "O QUÊ vamos resolver e COMO medir sucesso?" |
| **Accountable** | Data Product Manager / CDO |
| **Tempo típico** | 1-2 semanas |

**Agentes BMAD-Data nesta esteira:**

| Agente | Nome | Responsabilidades |
|--------|------|-------------------|
| 🎯 Data Strategist | Alex | Problem Statement, KPIs, Success Criteria |
| 📋 Business Analyst | Mary | Perguntas analíticas, STTM, DQ inicial |

**Artefatos produzidos:**

```yaml
upstream_artifacts:
  - problem-statement.md      # Definição clara do problema
  - kpis-okrs.md             # Métricas de sucesso quantificadas
  - success-criteria.md       # Critérios de aceite
  - analytical-questions.md   # Perguntas que os dados devem responder
  - sttm-initial.md          # Source-to-Target Mapping inicial
  - data-sources.md          # Fontes de dados identificadas
  - dq-initial.md            # Regras de qualidade preliminares
```

---

#### 🟨 MIDSTREAM — Design & Tradução Técnica

**Objetivo:** Traduzir requisitos em arquitetura e contratos claros antes de codificar.

| Aspecto | Descrição |
|---------|-----------|
| **Foco** | Decisões técnicas, trade-offs, governança |
| **Pergunta-chave** | "COMO vamos implementar e QUAIS são os riscos?" |
| **Accountable** | Data Solution Architect |
| **Tempo típico** | 1-3 semanas |

**Agentes BMAD-Data nesta esteira:**

| Agente | Nome | Responsabilidades |
|--------|------|-------------------|
| 🏛️ Data Solution Architect | Winston | AOD/DDS, segurança, observabilidade |
| 🧩 Data Modeler | Sofia | Modelo lógico, metadados, definições de métricas |
| 🧠 Agent Designer | Nova | Blueprint multiagente, contratos de autonomia |

**Artefatos produzidos:**

```yaml
midstream_artifacts:
  - architecture.md           # AOD (Architecture Overview Document)
  - design-decisions.md       # DDS (Design Decision Summary)
  - data-model-logical.md     # Modelo lógico de dados
  - data-contracts.yaml       # Contratos de dados formais
  - metric-contracts.yaml     # Contratos de métricas
  - security-strategy.md      # Estratégia de segurança
  - observability-spec.md     # Logs, métricas, alertas
  - agent-blueprint.md        # Design multiagente (se aplicável)
  - glossary.md               # Glossário de termos
```

---

#### 🟥 DOWNSTREAM — Execução & Automação

**Objetivo:** Executar a implementação técnica conforme contratos aprovados.

| Aspecto | Descrição |
|---------|-----------|
| **Foco** | Código executável, testado, documentado |
| **Pergunta-chave** | "O código FUNCIONA e está PRONTO para produção?" |
| **Accountable** | Data Engineering Lead |
| **Tempo típico** | 2-4 semanas |

**Agentes BMAD-Data nesta esteira:**

| Agente | Nome | Responsabilidades |
|--------|------|-------------------|
| 🛠️ Data Engineer Exec | Diego | SQL/DDL/PySpark, DQ checks, testes |
| 📊 BI Semantic | Bianca | Semantic layer, dashboards (opcional) |
| 🛡️ Data Steward | Gaia | Governança, DQ rules, monitoring |
| 🔁 Iteration Improvement | Kai | Melhoria contínua, retrospectives |

**Artefatos produzidos:**

```yaml
downstream_artifacts:
  # Código
  - sql/
      - 01-landing-tables.sql
      - 02-silver-tables.sql
      - 03-gold-tables.sql
      - 04-reference-tables.sql
  - pyspark/
      - transformations.py
      - quality_checks.py
  
  # Testes
  - tests/
      - unit-tests.sql
      - integration-tests.sql
      - data-validation.sql
  
  # Documentação
  - runbook.md
  - deployment-guide.md
  - lineage-doc.md
  
  # Governança
  - monitoring-spec.md
  - dq-rules-final.yaml
  - audit-log.md
  
  # BI (opcional)
  - semantic-model.md
  - dax-measures.dax
  - dashboards-spec.md
```

---

## 3. Workflows por Esteira

### 3.1 Catálogo de Workflows BMAD-Data

| # | Workflow | Esteira | Descrição | Agente Principal |
|---|----------|---------|-----------|------------------|
| 1 | `data-strategy` | UPSTREAM | Problem Statement + KPIs | Data Strategist |
| 2 | `business-analysis` | UPSTREAM | Requisitos + STTM | Business Analyst |
| 3 | `architecture` | MIDSTREAM | AOD/DDS + decisões | Data Solution Architect |
| 4 | `data-model` | MIDSTREAM | Modelo lógico + metadados | Data Modeler |
| 5 | `agent-blueprint` | MIDSTREAM | Design multiagente | Agent Designer |
| 6 | `agent-contracts` | MIDSTREAM | Contratos de autonomia | Agent Designer |
| 7 | `delivery` | DOWNSTREAM | DDL/SQL/PySpark | Data Engineer Exec |
| 8 | `unit-tests` | DOWNSTREAM | Testes automatizados | Data Engineer Exec |
| 9 | `governance` | DOWNSTREAM | Monitoring + DQ | Data Steward |
| 10 | `semantic-layer` | DOWNSTREAM | BI (opcional) | BI Semantic |

### 3.2 Workflows de Controle (CORE)

| # | Workflow | Tipo | Descrição |
|---|----------|------|-----------|
| 11 | `workflow-status` | Status | Estado do projeto + próximos passos |
| 12 | `gate-1-up-mid` | Gate | Validar transição UP→MID |
| 13 | `gate-2-mid-down` | Gate | Validar transição MID→DOWN |
| 14 | `gate-3-down-prod` | Gate | Validar transição DOWN→PROD |
| 15 | `routing` | Orquestração | Rotear para próximo agente |

### 3.3 Estrutura de um Workflow

Cada workflow no BMAD-Data segue uma estrutura padrão:

```
workflows/{nome-workflow}/
├── workflow.md           # Definição principal
├── {nome-workflow}.spec.md  # Especificação detalhada
└── steps-c/              # Etapas de criação
    ├── step-01-xxx.md
    ├── step-02-xxx.md
    └── ...
```

**Exemplo: `delivery/workflow.md`**

```yaml
---
name: delivery
description: Geração de DDL/SQL/PySpark para o pipeline
web_bundle: true
---

# Workflow: delivery

Workflow DOWNSTREAM para gerar estrutura de entrega (SQL/PySpark) 
e empacotar outputs em `implementation-artifacts/`.

## Saídas
- `{artifacts_root}/{project_code}/implementation-artifacts/sql/`
- `{artifacts_root}/{project_code}/implementation-artifacts/pyspark/`
- `{artifacts_root}/{project_code}/implementation-artifacts/README.md`

## Execução (create-only)
Siga as etapas em `steps-c/`.
```

### 3.4 Comparação: Workflows BMAD-Data vs Tasks Avanade Core

| Aspecto | Tasks Avanade Core | Workflows BMAD-Data |
|---------|-------------------|---------------------|
| **Ativação** | `*comando` pelo usuário | Orquestrador ou CLI |
| **Sequência** | Livre | Controlada por esteira |
| **Dependências** | Implícitas | Explícitas via gates |
| **Saídas** | `{agent}-outputs/` | `_bmad-output/{project}/` |
| **Versionamento** | Timestamp no nome | Git-native |
| **Validação** | Checklist opcional | Gate obrigatório |

---

## 4. Sistema de Gates

### 4.1 O Que São Gates?

Gates são **pontos de controle obrigatórios** entre esteiras que:

- ✅ Validam que artefatos requeridos existem
- ✅ Verificam critérios de qualidade
- ✅ Bloqueiam avanço se não atendidos
- ✅ Registram decisões de aprovação
- ✅ Permitem rollback estruturado

### 4.2 Gate 1: UPSTREAM → MIDSTREAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           GATE 1 (UP → MID)                             │
│                                                                          │
│  🎯 Propósito: Garantir que o PROBLEMA está claro antes do DESIGN       │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CRITÉRIOS DE ENTRADA                          │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ ☐ Problem Statement aprovado                                     │    │
│  │ ☐ KPIs definidos com baseline e target                          │    │
│  │ ☐ Escopo acordado com stakeholders                               │    │
│  │ ☐ Fontes de dados identificadas                                  │    │
│  │ ☐ Perguntas analíticas documentadas                              │    │
│  │ ☐ STTM inicial criado                                            │    │
│  │ ☐ Critérios de sucesso definidos                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  👤 Accountable: Data Product Manager / CDO                             │
│                                                                          │
│  📄 Artefato: gate-1-report.md                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Checklist Detalhado Gate 1:**

```markdown
## Gate 1 Checklist - UP → MID

### Problem Statement
- [ ] Problema de negócio está claramente descrito
- [ ] Impacto do problema está quantificado (quando possível)
- [ ] Público-alvo está identificado

### KPIs / Métricas de Sucesso
- [ ] KPIs têm baseline atual documentado
- [ ] KPIs têm target desejado definido
- [ ] Fórmula de cálculo está especificada
- [ ] Fonte de dados para cada KPI identificada

### Escopo
- [ ] O que está IN scope está listado
- [ ] O que está OUT of scope está listado
- [ ] Stakeholders concordaram com escopo (evidência)

### Dados
- [ ] Fontes de dados identificadas
- [ ] Formato de cada fonte documentado
- [ ] Frequência de atualização conhecida
- [ ] Acesso confirmado ou plano de acesso

### Aprovações
- [ ] Data Product Manager aprovou
- [ ] Stakeholder principal aprovou
```

---

### 4.3 Gate 2: MIDSTREAM → DOWNSTREAM (Definition of Ready)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           GATE 2 (MID → DOWN)                           │
│                                                                          │
│  🎯 Propósito: Garantir que o DESIGN está pronto para EXECUÇÃO          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CRITÉRIOS DE ENTRADA                          │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ ☐ Arquitetura (AOD/DDS) aprovada                                 │    │
│  │ ☐ Modelo lógico de dados versionado                              │    │
│  │ ☐ Data Contracts fechados e assinados                            │    │
│  │ ☐ Metric Contracts fechados e assinados                          │    │
│  │ ☐ Critérios de qualidade definidos (DQ rules)                    │    │
│  │ ☐ Estratégia de segurança aprovada                               │    │
│  │ ☐ Observabilidade spec definida                                  │    │
│  │ ☐ Estimativa de esforço validada                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  👤 Accountable: Data Solution Architect                                │
│                                                                          │
│  📄 Artefato: gate-2-report.md                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Checklist Detalhado Gate 2:**

```markdown
## Gate 2 Checklist - MID → DOWN

### Arquitetura
- [ ] AOD (Architecture Overview Document) aprovado
- [ ] Decisões técnicas documentadas com trade-offs
- [ ] Plataforma alvo definida (Databricks/Snowflake/etc)
- [ ] Padrão de arquitetura escolhido (ex: Medallion)

### Modelo de Dados
- [ ] Modelo lógico completo e versionado
- [ ] Relacionamentos e chaves definidos
- [ ] Granularidade de cada tabela documentada
- [ ] Glossário de termos criado
- [ ] Metadados documentados

### Contratos
- [ ] Data Contracts para cada tabela
  - [ ] Schema (colunas, tipos, nullable)
  - [ ] Primary/Foreign keys
  - [ ] DQ rules por coluna
  - [ ] SLA definido
- [ ] Metric Contracts para cada KPI
  - [ ] Fórmula exata
  - [ ] Dimensões aplicáveis
  - [ ] Fonte de verdade

### Segurança & Governança
- [ ] Classificação de dados (PII, sensível, público)
- [ ] Masking rules definidas se aplicável
- [ ] RBAC (Role-Based Access Control) especificado
- [ ] Compliance LGPD/GDPR validado

### Observabilidade
- [ ] Métricas de pipeline definidas
- [ ] Alertas especificados
- [ ] Log levels definidos

### Estimativa
- [ ] Esforço estimado por camada
- [ ] Recursos necessários identificados
- [ ] Timeline aprovado

### Aprovações
- [ ] Data Solution Architect aprovou
- [ ] Data Product Manager validou
```

---

### 4.4 Gate 3: DOWNSTREAM → PRODUÇÃO

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          GATE 3 (DOWN → PROD)                           │
│                                                                          │
│  🎯 Propósito: Garantir que o CÓDIGO está pronto para PRODUÇÃO          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CRITÉRIOS DE ENTRADA                          │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ ☐ Código versionado em repositório                               │    │
│  │ ☐ Testes passando (> 80% cobertura)                              │    │
│  │ ☐ Code review aprovado                                           │    │
│  │ ☐ Monitoramento ativo configurado                                │    │
│  │ ☐ Rollback definido e testado                                    │    │
│  │ ☐ Documentação técnica completa                                  │    │
│  │ ☐ Runbook criado                                                 │    │
│  │ ☐ DQ rules implementadas e validadas                             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  👤 Accountable: Data Engineering Lead                                  │
│                                                                          │
│  📄 Artefato: gate-3-report.md                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Checklist Detalhado Gate 3:**

```markdown
## Gate 3 Checklist - DOWN → PROD

### Código
- [ ] Todo código está em repositório Git
- [ ] Branch principal atualizada
- [ ] Histórico de commits limpo
- [ ] Sem secrets ou credenciais no código

### Testes
- [ ] Testes unitários passando
- [ ] Cobertura de testes > 80%
- [ ] Testes de integração passando
- [ ] Testes de qualidade de dados passando
- [ ] Comparação arquivo vs tabela validada

### Code Review
- [ ] PR criado e revisado
- [ ] Pelo menos 1 aprovação de par
- [ ] Comentários resolvidos

### Monitoramento
- [ ] Alertas configurados
- [ ] Dashboards de monitoramento criados
- [ ] Log shipping configurado
- [ ] Métricas de performance baseline

### Rollback
- [ ] Estratégia de rollback documentada
- [ ] Scripts de rollback testados
- [ ] Backup de dados críticos

### Documentação
- [ ] Runbook criado
- [ ] Deployment guide atualizado
- [ ] Data lineage documentado
- [ ] Troubleshooting guide

### Governança
- [ ] DQ rules implementadas
- [ ] Thresholds validados
- [ ] Audit logging configurado

### Aprovações
- [ ] Data Engineering Lead aprovou
- [ ] Data Steward validou governança
- [ ] Stakeholder final informado
```

---

## 5. Comparação: Agentes Existentes vs BMAD-Data

### 5.1 Modelo de Fluxo

| Aspecto | Agentes Existentes | BMAD-Data |
|---------|-------------------|-----------|
| **Tipo de fluxo** | Livre / Ad-hoc | Sequencial controlado |
| **Número de esteiras** | 0 (sem conceito) | 3 (UP/MID/DOWN) |
| **Gates** | 0 obrigatórios | 3 obrigatórios |
| **Contratos** | Nenhum | Data + Metric + Agent |
| **Orquestrador** | Master Agent (sugere) | Orion (controla) |
| **Rollback** | Manual | Estruturado por gate |

### 5.2 Mapeamento de Agentes por Esteira

```
                    BMAD-Data                    Agentes Existentes
                    ─────────                    ──────────────────

UPSTREAM           ┌───────────────┐
                   │ Data          │             
                   │ Strategist    │─────────────▶ ProductVision (parcial)
                   │ (Alex 🎯)     │             
                   └───────────────┘             
                   ┌───────────────┐             
                   │ Business      │             
                   │ Analyst       │─────────────▶ ❌ Não existe
                   │ (Mary 📋)     │             
                   └───────────────┘             

          ═══════════ GATE 1 ═══════════         ❌ Não existe

MIDSTREAM          ┌───────────────┐             
                   │ Data Solution │             
                   │ Architect     │─────────────▶ ❌ Não existe
                   │ (Winston 🏛️) │             
                   └───────────────┘             
                   ┌───────────────┐             
                   │ Data Modeler  │             
                   │ (Sofia 🧩)    │─────────────▶ ❌ Não existe
                   └───────────────┘             
                   ┌───────────────┐             
                   │ Agent         │             
                   │ Designer      │─────────────▶ ❌ Não existe
                   │ (Nova 🧠)     │             
                   └───────────────┘             

          ═══════════ GATE 2 ═══════════         ❌ Não existe

DOWNSTREAM         ┌───────────────┐             
                   │ Data Engineer │             
                   │ Exec          │─────────────▶ DataFlow 🔄 (90%)
                   │ (Diego 🛠️)   │             
                   └───────────────┘             
                   ┌───────────────┐             
                   │ BI Semantic   │             
                   │ (Bianca 📊)   │─────────────▶ InsightForge 📊 (95%)
                   └───────────────┘             
                   ┌───────────────┐             
                   │ Data Steward  │             
                   │ (Gaia 🛡️)    │─────────────▶ ❌ Não existe
                   └───────────────┘             
                   ┌───────────────┐             
                   │ Iteration     │             
                   │ Improvement   │─────────────▶ ❌ Não existe
                   │ (Kai 🔁)      │             
                   └───────────────┘             

          ═══════════ GATE 3 ═══════════         ❌ Não existe

CORE               ┌───────────────┐             
                   │ Orchestrator  │             
                   │ (Orion 🧭)    │─────────────▶ Master Agent (30%)
                   └───────────────┘             
```

### 5.3 O Que os Agentes Existentes Oferecem a Mais

Os agentes existentes têm capacidades não cobertas pelo BMAD-Data:

| Capacidade | Agente Existente | Gap no BMAD-Data |
|------------|------------------|------------------|
| **Estimativa de projeto** | DeliveryPro | ❌ Não tem |
| **Roadmap e timeline** | DeliveryPro | ❌ Não tem |
| **Análise de riscos** | DeliveryPro | Parcial (nos gates) |
| **Budget forecasting** | DeliveryPro | ❌ Não tem |
| **User Stories** | BacklogMaster | ❌ Não tem |
| **Sprint planning** | SprintPro | ❌ Não tem |
| **RLS (Row-Level Security)** | InsightForge | ❌ Não tem |
| **HTML Dashboard Preview** | InsightForge | ❌ Não tem |
| **Optimization tuning** | InsightForge | ❌ Não tem |
| **Checklists por comando** | Todos | Apenas nos gates |

---

## 6. Contratos entre Esteiras

### 6.1 Por Que Contratos São Importantes?

Contratos formais entre esteiras garantem:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SEM CONTRATOS                                     │
│                                                                      │
│  Arquiteto: "Tabela X terá 10 colunas"                              │
│  Engineer:  "Não encontrei a definição, vou assumir 8 colunas"      │
│  Resultado: RETRABALHO + BUGS + FRUSTRAÇÃO                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    COM CONTRATOS                                     │
│                                                                      │
│  Arquiteto: Assina Data Contract com schema exato                   │
│  Engineer:  Implementa exatamente conforme contrato                 │
│  Gate 2:    Valida que contrato existe e está assinado              │
│  Resultado: CLAREZA + RASTREABILIDADE + QUALIDADE                   │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Tipos de Contratos

#### 6.2.1 Data Contract

Define o schema exato de uma tabela/dataset:

```yaml
# Exemplo: data-contract-silver-trip-data.yaml

contract:
  version: "1.0"
  owner: "data-engineering-team"
  signed_by: "Data Solution Architect"
  signed_date: "2026-01-21"

table:
  name: "SILVER.TRIP_DATA_CSV"
  layer: "Silver"
  grain: "One row per trip"
  refresh: "Daily"
  sla: "99.5% availability"

schema:
  columns:
    - name: "trip_id"
      type: "BIGINT"
      nullable: false
      description: "Unique trip identifier"
      primary_key: true
      
    - name: "pickup_datetime"
      type: "DATETIME2"
      nullable: false
      description: "Trip start timestamp"
      dq_rules:
        - rule: "NOT NULL"
          severity: "ERROR"
        - rule: "pickup_datetime <= dropoff_datetime"
          severity: "ERROR"
          
    - name: "fare_amount"
      type: "DECIMAL(10,2)"
      nullable: true
      description: "Base fare in USD"
      dq_rules:
        - rule: "fare_amount >= 0"
          severity: "WARN"
        - rule: "fare_amount < 10000"
          severity: "WARN"

lineage:
  source: "LANDING.TRIP_DATA_CSV"
  transformation: "Type casting + DQ validation"
```

#### 6.2.2 Metric Contract

Define como uma métrica é calculada:

```yaml
# Exemplo: metric-contract-total-revenue.yaml

contract:
  version: "1.0"
  owner: "analytics-team"
  signed_by: "Data Modeler"
  signed_date: "2026-01-21"

metric:
  name: "Total Revenue"
  id: "metric_total_revenue"
  business_definition: "Sum of all fare amounts for completed trips"
  
  calculation:
    formula: "SUM(fare_amount) WHERE trip_status = 'completed'"
    base_table: "GOLD.TRIP_DATA_ENRICHED"
    
  granularity:
    available:
      - daily
      - weekly
      - monthly
      - yearly
    default: "daily"
    
  dimensions:
    - region
    - payment_type
    - trip_type
    - date
    
  quality:
    - rule: "Never negative"
    - rule: "YoY variance < 50% (warning)"
```

#### 6.2.3 Agent Execution Contract

Define limites de autonomia de um agente:

```yaml
# Exemplo: agent-contract-data-engineer.yaml

contract:
  version: "1.0"
  agent: "data-engineer-exec"
  signed_by: "Agent Designer"
  signed_date: "2026-01-21"

allowed_actions:
  - "Generate SQL code"
  - "Generate PySpark code"
  - "Create DDL scripts"
  - "Generate test scripts"
  - "Create documentation"
  - "Execute read-only queries for validation"

prohibited_actions:
  - "Execute DML in production"
  - "Drop tables without approval"
  - "Modify existing production code"
  - "Approve own artifacts"
  - "Skip gate validations"
  - "Access production credentials"

escalation_triggers:
  - "DQ failure rate > 10%"
  - "Test coverage < 80%"
  - "Unknown column type detected"
  - "Performance degradation > 20%"

required_inputs:
  - "Approved Data Contracts"
  - "Approved Metric Contracts"
  - "Gate 2 passed"
```

---

## 7. Fluxo de Artefatos

### 7.1 Diagrama de Fluxo Completo

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE ARTEFATOS BMAD-Data                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                          UPSTREAM                                        ││
│  │                                                                          ││
│  │  [Data Strategist]                    [Business Analyst]                 ││
│  │        │                                     │                           ││
│  │        ▼                                     ▼                           ││
│  │  ┌─────────────┐                      ┌─────────────┐                   ││
│  │  │problem-stmt │                      │analytical-  │                   ││
│  │  │kpis-okrs    │                      │questions    │                   ││
│  │  │success-crit │                      │sttm-initial │                   ││
│  │  │scope.md     │                      │dq-initial   │                   ││
│  │  └──────┬──────┘                      └──────┬──────┘                   ││
│  │         │                                    │                           ││
│  │         └────────────────┬───────────────────┘                           ││
│  │                          ▼                                               ││
│  │                   ┌─────────────┐                                        ││
│  │                   │  GATE 1     │                                        ││
│  │                   │  UP → MID   │                                        ││
│  │                   └──────┬──────┘                                        ││
│  └──────────────────────────┼──────────────────────────────────────────────┘│
│                             ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                          MIDSTREAM                                       ││
│  │                                                                          ││
│  │  [Data Solution Architect]  [Data Modeler]    [Agent Designer]          ││
│  │        │                          │                  │                   ││
│  │        ▼                          ▼                  ▼                   ││
│  │  ┌─────────────┐           ┌─────────────┐    ┌─────────────┐           ││
│  │  │architecture │           │data-model   │    │agent-       │           ││
│  │  │aod-dds.md   │           │logical.md   │    │blueprint.md │           ││
│  │  │security.md  │           │glossary.md  │    │contracts.md │           ││
│  │  │observ.md    │           │metadados.md │    │autonomy.md  │           ││
│  │  └──────┬──────┘           └──────┬──────┘    └──────┬──────┘           ││
│  │         │                         │                  │                   ││
│  │         │    ┌────────────────────┴─────────────────┐│                   ││
│  │         │    │                                      ││                   ││
│  │         ▼    ▼                                      ▼│                   ││
│  │  ┌─────────────────┐                    ┌─────────────────┐             ││
│  │  │ DATA CONTRACTS  │                    │ METRIC CONTRACTS│             ││
│  │  │ (schema, DQ)    │                    │ (fórmulas, dims)│             ││
│  │  └────────┬────────┘                    └────────┬────────┘             ││
│  │           │                                      │                       ││
│  │           └──────────────────┬───────────────────┘                       ││
│  │                              ▼                                           ││
│  │                       ┌─────────────┐                                    ││
│  │                       │  GATE 2     │                                    ││
│  │                       │ MID → DOWN  │                                    ││
│  │                       └──────┬──────┘                                    ││
│  └──────────────────────────────┼──────────────────────────────────────────┘│
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                          DOWNSTREAM                                      ││
│  │                                                                          ││
│  │  [Data Engineer Exec]    [BI Semantic]    [Data Steward]                ││
│  │        │                      │                  │                       ││
│  │        ▼                      ▼                  ▼                       ││
│  │  ┌─────────────┐       ┌─────────────┐    ┌─────────────┐               ││
│  │  │sql/         │       │semantic-    │    │monitoring-  │               ││
│  │  │  ddl/*.sql  │       │model.md     │    │spec.md      │               ││
│  │  │  etl/*.sql  │       │dax/*.dax    │    │dq-rules.yaml│               ││
│  │  │pyspark/     │       │dashboards/  │    │audit-log.md │               ││
│  │  │tests/       │       │             │    │             │               ││
│  │  │runbook.md   │       │             │    │             │               ││
│  │  └──────┬──────┘       └──────┬──────┘    └──────┬──────┘               ││
│  │         │                     │                  │                       ││
│  │         └─────────────────────┴──────────────────┘                       ││
│  │                              │                                           ││
│  │                              ▼                                           ││
│  │                       ┌─────────────┐                                    ││
│  │                       │  GATE 3     │                                    ││
│  │                       │DOWN → PROD  │                                    ││
│  │                       └──────┬──────┘                                    ││
│  └──────────────────────────────┼──────────────────────────────────────────┘│
│                                 ▼                                            │
│                          ┌─────────────┐                                     │
│                          │  PRODUÇÃO   │                                     │
│                          └─────────────┘                                     │
│                                 │                                            │
│                                 ▼                                            │
│                       [Iteration Improvement]                                │
│                              (Kai 🔁)                                        │
│                                 │                                            │
│                                 ▼                                            │
│                       ┌─────────────────┐                                    │
│                       │improvement-     │                                    │
│                       │backlog.md       │───────▶ Próximo Ciclo UPSTREAM    │
│                       │retrospective.md │                                    │
│                       └─────────────────┘                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Estrutura de Pastas de Saída

```
_bmad-output/
└── {project-code}/                    # Ex: trip-data-poc
    ├── planning-artifacts/            # UPSTREAM + MIDSTREAM
    │   ├── problem-statement.md
    │   ├── kpis-okrs.md
    │   ├── success-criteria.md
    │   ├── analytical-questions.md
    │   ├── sttm-initial.md
    │   ├── architecture.md
    │   ├── data-model-logical.md
    │   ├── glossary.md
    │   ├── data-contracts/
    │   │   ├── landing-trip-data.yaml
    │   │   ├── silver-trip-data.yaml
    │   │   └── gold-trip-data.yaml
    │   ├── metric-contracts/
    │   │   ├── total-revenue.yaml
    │   │   └── avg-trip-distance.yaml
    │   ├── gate-1-report.md
    │   ├── gate-2-report.md
    │   └── status.md
    │
    └── implementation-artifacts/       # DOWNSTREAM
        ├── sql/
        │   ├── 01-landing-tables.sql
        │   ├── 02-silver-tables.sql
        │   ├── 03-gold-tables.sql
        │   └── 04-etl-scripts.sql
        ├── pyspark/
        │   ├── transformations.py
        │   └── quality_checks.py
        ├── tests/
        │   ├── unit-tests.sql
        │   └── integration-tests.sql
        ├── docs/
        │   ├── runbook.md
        │   └── lineage.md
        ├── monitoring/
        │   ├── monitoring-spec.md
        │   └── dq-rules.yaml
        ├── gate-3-report.md
        └── README.md
```

---

## 8. Implementação Prática

### 8.1 Como Usar o BMAD-Data CLI

O BMAD-Data inclui um CLI para orquestração local:

```powershell
# Verificar status do projeto
node tools\data-agents-runner\cli.js workflow-status

# Validar Gate 1
node tools\data-agents-runner\cli.js gate-1

# Validar Gate 2
node tools\data-agents-runner\cli.js gate-2

# Sugerir próximo workflow
node tools\data-agents-runner\cli.js orchestrate

# Usar projeto diferente
node tools\data-agents-runner\cli.js orchestrate --project-code my-project
```

### 8.2 Como Adaptar Agentes Existentes para Usar Gates

Para os agentes existentes, recomendamos adicionar checklists inspirados nos gates:

```yaml
# Proposta: Adicionar ao DataFlow

commands:
  - trigger: GR
    command: "*gate-ready"
    description: "Verificar se requisitos para execução estão prontos"
    checklist:
      - "Data sources identificados?"
      - "Schema esperado documentado?"
      - "DQ rules definidos?"
      - "Plataforma alvo confirmada?"
    
  - trigger: GV
    command: "*gate-validate"
    description: "Validar artefatos antes de considerar completo"
    checklist:
      - "Código no repositório?"
      - "Testes passando?"
      - "Documentação criada?"
      - "Code review feito?"
```

### 8.3 Cenário de Uso Híbrido

Combinando o melhor dos dois mundos:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MODELO HÍBRIDO RECOMENDADO                            │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                       FASE DE DISCOVERY                          │    │
│  │  Usar: BMAD-Data (UPSTREAM + MIDSTREAM)                         │    │
│  │  Agentes: Strategist → Analyst → Architect → Modeler            │    │
│  │  Gates: G1 e G2 obrigatórios                                    │    │
│  │  Resultado: Contracts aprovados                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                       FASE DE EXECUÇÃO                           │    │
│  │  Usar: Agentes Existentes (mais maduros)                        │    │
│  │  Agentes: DataFlow, InsightForge, DeliveryPro                   │    │
│  │  Comandos: *create-ddl, *create-etl, *create-dax                │    │
│  │  Validação: Checklists + Gate 3 adaptado                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                       FASE DE GOVERNANÇA                         │    │
│  │  Usar: BMAD-Data (Data Steward + Iteration)                     │    │
│  │  Agentes: Gaia, Kai                                             │    │
│  │  Gates: G3 obrigatório                                          │    │
│  │  Resultado: Pipeline em produção + backlog de melhorias         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Anexo A: Tabela Resumo Gates

| Gate | Transição | Critérios-Chave | Accountable | Artefato |
|------|-----------|-----------------|-------------|----------|
| **G1** | UP → MID | Problema claro, KPIs, Escopo, Fontes | Data PM / CDO | gate-1-report.md |
| **G2** | MID → DOWN | Arquitetura, Modelo, Contracts, DQ | Data Solution Architect | gate-2-report.md |
| **G3** | DOWN → PROD | Código, Testes >80%, Monitoring, Runbook | Data Engineering Lead | gate-3-report.md |

---

## Anexo B: Checklist de Implementação

```markdown
## Para implementar esteiras nos Agentes Existentes

### Fase 1: Gates Opcionais
- [ ] Criar task `*gate-ready` no DataFlow
- [ ] Criar task `*gate-validate` no DataFlow
- [ ] Adicionar checklist de "Definition of Ready" 
- [ ] Adicionar checklist de "Definition of Done"

### Fase 2: Contratos
- [ ] Criar template `data-contract-tmpl.yaml`
- [ ] Criar template `metric-contract-tmpl.yaml`
- [ ] Adicionar task `*create-contract` no DataFlow

### Fase 3: Novos Agentes
- [ ] Criar agente Data Architect (Winston)
- [ ] Criar agente Data Steward (Gaia)
- [ ] Criar agente Business Analyst (Mary)

### Fase 4: Orquestração
- [ ] Expandir Master Agent com status de projeto
- [ ] Adicionar validação de gates ao Master Agent
- [ ] Implementar sugestão automática de próximo passo
```

---

**Documento gerado automaticamente pelo Master Agent**  
**Análise de Workflows, Esteiras e Gates - BMAD-Data vs Avanade Core**
