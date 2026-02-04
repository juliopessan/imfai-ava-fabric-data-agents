# Product Requirements Document (PRD)
## Data & Agentic AI — Modelo Híbrido BMAD-Data
### Versão 2.0

---

## 1. Visão Geral

Este PRD descreve um sistema de **Data & Agentic AI** baseado no **modelo híbrido BMAD-Data**, no qual:

- A experiência é **agent-first** (papéis reais atuando em sequência)
- O controle é **method-first** (SDLC de Dados como backbone invisível)
- A operação segue **3 esteiras organizacionais**:
  - **UPSTREAM** — Estratégia e Problema
  - **MIDSTREAM** — Design e Tradução Técnica
  - **DOWNSTREAM** — Execução e Automação

### 1.1 Proposta de Valor

**Framework de aceleração para projetos de dados** que utiliza Agentes de IA para aumentar a capacidade humana em projetos de:
- Pipeline de Dados
- Migração de Dados
- Modernização de Dados

### 1.2 Público-Alvo

- Consultores de Dados Avanade
- Arquitetos de Solução Avanade
- Equipes de Projetos de Dados Avanade

---

## 2. Objetivos do Produto

- Entregar valor de negócio mensurável por meio de dados e Agentic AI
- Reduzir fricção entre negócio, dados, AI e governança
- Garantir rastreabilidade, auditabilidade e escalabilidade
- Permitir inovação com controle (agent-first com guardrails metodológicos)
- **Reduzir lead time e custo de projetos de dados** (prioridade principal)

---

## 3. Métricas de Sucesso

### 3.1 Métricas Primárias (Prioridade Alta)

| Métrica | Baseline Manual | Target com Agentes | Redução Esperada | Como Medir |
|---------|-----------------|-------------------|------------------|------------|
| **Lead Time Total** | `[A PREENCHER]` dias | `[CALCULAR]` dias | 40-60% | Tempo início → entrega final |
| **Custo por Pipeline** | R$ `[A PREENCHER]` | R$ `[CALCULAR]` | 30-50% | (Horas totais × custo/hora) |

### 3.2 Métricas Secundárias

| Métrica | Baseline Manual | Target com Agentes | Redução Esperada | Como Medir |
|---------|-----------------|-------------------|------------------|------------|
| **Tempo de Design (MID)** | `[A PREENCHER]` horas | `[CALCULAR]` horas | 50% | Horas em arquitetura e modelagem |
| **Tempo de Coding (DOWN)** | `[A PREENCHER]` horas | `[CALCULAR]` horas | 60-70% | Horas gerando SQL/PySpark/DDL |
| **Taxa de Retrabalho** | `[A PREENCHER]` % | < 10% | Significativa | Revisões necessárias pós-gate |
| **Cobertura de Testes** | `[A PREENCHER]` % | > 80% | Aumento | % de testes gerados automaticamente |
| **Aderência a Padrões** | `[A PREENCHER]` % | > 95% | Aumento | Checklist de governança aprovado |

### 3.3 Instruções para Preenchimento do Baseline

> **AÇÃO REQUERIDA:** Antes de iniciar a Fase 0 (POC), a equipe deve:
> 1. Selecionar 3-5 projetos similares já executados manualmente
> 2. Coletar dados de tempo e custo reais
> 3. Calcular médias para cada métrica
> 4. Preencher a coluna "Baseline Manual"
> 5. Calcular targets baseados nas reduções esperadas

---

## 4. Escopo

### 4.1 Dentro do Escopo

- Ciclo completo do SDLC de Dados & Agentic AI
- Modelo de agentes por papel
- Orquestração por gates metodológicos
- Contratos MID → DOWN
- Governança e auditoria
- **Cenário piloto: Pipeline de Dados com Arquitetura Medalhão**

### 4.2 Fora do Escopo

- Implementação de código de produção do cliente
- Prompts finais de agentes (serão desenvolvidos iterativamente)
- Ferramentas específicas de cloud/vendor (framework agnóstico)

---

## 5. Caso de Uso Piloto — Trip Data Pipeline

### 5.1 Descrição do Cenário

Pipeline de dados fictício para validação do framework, utilizando dados de viagens (Trip Data) com arquitetura medalhão (Landing → Silver → Gold).

### 5.2 Componentes do Pipeline

| Camada | Tabela | Fonte | Formato | Frequência |
|--------|--------|-------|---------|------------|
| **Landing** | LND.TRIP_DATA_CSV | Arquivo CSV | VARCHAR (todas) | Mensal |
| **Landing** | LND.TRIP_DATA_PARQUET | Arquivo Parquet | VARCHAR (todas) | Mensal |
| **Reference** | REF.TRIP_TYPE | trip_type.tsv | TSV | Estático |
| **Reference** | REF.RATE_CODE | rate_code.json | JSON | Estático |
| **Reference** | REF.PAYMENT_TYPE | payment_type_array.json | JSON Array | Estático |
| **Silver** | SILVER.TRIP_DATA_CSV | LND.TRIP_DATA_CSV | Tipado + DQ | Mensal |
| **Silver** | SILVER.TRIP_DATA_PARQUET | LND.TRIP_DATA_PARQUET | Tipado + DQ | Mensal |
| **Gold** | GOLD.TRIP_DATA_CSV | Silver + Refs | Enriquecido | Mensal |
| **Gold** | GOLD.TRIP_DATA_PARQUET_AGG | Silver | Agregado | Mensal |

### 5.3 Requisitos Técnicos do Piloto

1. **Ingestão CSV/Parquet**
   - Landing com todas colunas VARCHAR
   - Profiling automático para derivar tipos
   - Data Quality checks em colunas não-VARCHAR
   - Scripts SQL ou PySpark

2. **Tabelas de Referência**
   - Parsing de TSV, JSON e JSON Array
   - DDL scripts em SQL

3. **Camada Gold**
   - Joins enriquecidos (TRIP_DATA_CSV + refs)
   - Agregações (TRIP_DATA_PARQUET por PULocationID)
   - Sum de trip_distance e fare_amount
   - Count de trips

4. **Testes**
   - Unit tests SQL comparando arquivos × tabelas
   - Validação de integridade de dados

---

## 6. Estrutura de Esteiras

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    UPSTREAM     │────▶│    MIDSTREAM    │────▶│   DOWNSTREAM    │
│  Estratégia &   │     │    Design &     │     │   Execução &    │
│   Requisitos    │     │Tradução Técnica │     │   Automação     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
     Gate 1                  Gate 2                  Gate 3
   (UP → MID)              (MID → DOWN)           (DOWN → PROD)
```

Cada transição é controlada por **gates obrigatórios**.

---

## 7. Agentes por Esteira (Agent-First)

### 🟦 UPSTREAM — Estratégia & Requisitos

#### 7.1 Data Strategist / Product Agent
**Objetivo:** Definir valor, escopo e sucesso.

**Responsabilidades**
- Definir problema de negócio
- Estabelecer KPIs e critérios de sucesso
- Priorizar casos de uso

**Outputs**
- Problem Statement
- KPIs / OKRs
- Success Criteria

---

#### 7.2 Business Analyst Agent (Enhanced)
**Objetivo:** Traduzir negócio em requisitos analíticos e técnicos.

**Responsabilidades**
- Estruturar perguntas analíticas
- Realizar profiling conceitual inicial
- Converter regras de negócio em regras técnicas
- Definir critérios de qualidade
- Produzir STTM / requisitos técnicos iniciais

**Outputs**
- Analytical Questions
- Decision Requirements
- Regras Técnicas
- STTM

---

### 🟨 MIDSTREAM — Design & Tradução Técnica

#### 7.3 Data Solution Architect Agent
**Objetivo:** Definir a solução técnica ótima e governável.

**Responsabilidades**
- Explorar múltiplas arquiteturas e trade-offs
- Criar AOD / DDS
- Definir segurança, governança, auditoria e observabilidade
- Recomendar otimizações de custo e performance
- Sugerir configurações de plataforma
- Definir padrões e controle de acesso

**Outputs**
- Arquitetura de Dados
- AOD / DDS
- Estratégia de Segurança e Observabilidade

---

#### 7.4 Data Modeler Agent (Design)
**Objetivo:** Garantir coerência e qualidade do modelo de dados.

**Responsabilidades**
- Definir modelo lógico
- Estabelecer relacionamentos, chaves e índices
- Detectar problemas de normalização
- Definir lineage lógico
- Criar glossário e metadados

**Outputs**
- Modelo Lógico
- Definições de Métricas
- Metadados

---

#### 7.5 Agent Design / AI Design Agent
**Objetivo:** Definir arquitetura multiagente e limites de autonomia.

**Responsabilidades**
- Definir contratos de I/O entre agentes
- Definir limites de decisão e autonomia
- Preparar regras de orquestração

**Outputs**
- Blueprint Multiagente
- Agent Contracts
- Regras de Autonomia

---

### 🟥 DOWNSTREAM — Execução & Automação

#### 7.6 Data Engineer Execution Agent (Unificado)
**Objetivo:** Executar tecnicamente a solução conforme contratos aprovados.

**Responsabilidades (consolidadas)**
- Geração de SQL e PySpark
- Criação física de tabelas e schemas (DDL)
- Ingestão de dados (raw / landing / curated)
- Parsing de dados complexos (JSON, logs, regex)
- Implementação de regras de qualidade e validação
- Performance tuning
- Error handling e recovery
- Observabilidade (logs, métricas, alertas)
- Unit tests e sample data
- Documentação técnica (runbooks, lineage)
- Peer review automatizado

**Inputs**
- Data Contracts
- Metric Contracts
- Arquitetura aprovada

**Outputs**
- SQL / DDL versionados
- Pipelines executáveis
- Testes automatizados
- Documentação técnica

> **Nota:** Não existem agentes downstream fragmentados (ex.: SQL Agent).
> Todas essas capacidades pertencem a este agente unificado.

---

#### 7.7 BI / Semantic Layer Agent (Opcional)
**Objetivo:** Disponibilizar camada analítica para consumo de negócio.

**Responsabilidades**
- Criar modelos semânticos
- Gerar medidas (ex.: DAX)
- Criar dashboards baseline
- Otimizar performance de datasets BI

**Outputs**
- Modelo Semântico
- Dashboards
- Medidas

---

#### 7.8 Data Steward / Governance Agent
**Objetivo:** Garantir qualidade, conformidade e rastreabilidade.

**Outputs**
- Monitoring Spec
- Regras de Qualidade
- Logs de Governança

---

#### 7.9 Iteration & Improvement Agent
**Objetivo:** Evoluir continuamente a solução.

**Outputs**
- Improvement Backlog
- Hipóteses Revisadas

---

## 8. Backbone Metodológico (Invisível)

### Fases do SDLC
1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment
7. Monitoring & Governance
8. Iteration & Improvement

---

## 9. Gates entre Esteiras

### Gate 1 — UP → MID
**Critérios**
- Problema claro e documentado
- KPIs definidos com valores-alvo
- Escopo acordado com stakeholders
- Dados de entrada identificados

**Accountable:** Data Product Manager / CDO

**Definition of Done:**
- [ ] Problem Statement aprovado
- [ ] KPIs documentados
- [ ] Escopo assinado
- [ ] Fontes de dados mapeadas

---

### Gate 2 — MID → DOWN (Definition of Ready)
**Critérios**
- Arquitetura definida e aprovada
- Modelo lógico aprovado
- Data & Metric Contracts fechados
- Critérios de qualidade definidos
- Estimativas de esforço validadas

**Accountable:** Data Solution Architect

**Definition of Done:**
- [ ] AOD/DDS aprovado
- [ ] Modelo lógico versionado
- [ ] Contracts assinados
- [ ] DQ rules documentadas
- [ ] Estimativa aprovada

---

### Gate 3 — DOWN → PROD
**Critérios**
- Código versionado em repositório
- Testes passando (> 80% cobertura)
- Monitoramento ativo configurado
- Rollback definido e testado
- Documentação técnica completa

**Accountable:** Data Engineering Lead

**Definition of Done:**
- [ ] PR aprovado e merged
- [ ] Testes automatizados passando
- [ ] Alertas configurados
- [ ] Runbook documentado
- [ ] Rollback testado

---

## 10. Contratos MID → DOWN

### 10.1 Data Contract
- Schema (colunas, tipos, nullable)
- Chaves primárias e estrangeiras
- Regras de qualidade (DQ rules)
- Owner e SLA
- Formato de entrega

### 10.2 Metric Contract
- Nome da métrica
- Fórmula de cálculo
- Granularidade
- Dimensões aplicáveis
- Fonte de verdade (tabela base)

### 10.3 Agent Execution Contract
- Ações permitidas
- Ações proibidas
- Inputs obrigatórios
- Outputs esperados
- Limites de autonomia

---

## 11. Orquestração

O **Orquestrador**:
- Observa artefatos (não conversas)
- Valida gates automaticamente
- Controla transições entre esteiras
- Escala exceções para humanos
- Registra trilha de auditoria

---

## 12. Stakeholders

| Stakeholder | Papel | Interesse Principal | Envolvimento |
|-------------|-------|---------------------|--------------|
| **Consultores de Dados Avanade** | Usuários primários | Produtividade, qualidade de entrega | Alto - Operacional |
| **Arquitetos de Solução Avanade** | Usuários primários | Padronização, governança técnica | Alto - Design |
| **Equipe de Projetos de Dados** | Usuários primários | Velocidade, redução de custo | Alto - Execução |
| **Liderança Avanade** | Sponsor | ROI, diferenciação competitiva | Médio - Estratégico |
| **Clientes Finais** | Beneficiários | Entrega rápida, qualidade | Baixo - Indireto |

---

## 13. Análise de Riscos

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|---------------|---------|-----------|
| R1 | **Agentes geram código incorreto** | Média | Alto | Gates de validação obrigatórios + revisão humana em DOWN→PROD |
| R2 | **Resistência da equipe à adoção** | Média | Médio | Programa de treinamento + demonstração de quick wins |
| R3 | **Dependência de LLM externo** | Baixa | Alto | Fallback para execução manual + prompts versionados |
| R4 | **Variabilidade entre contextos de clientes** | Alta | Médio | Templates adaptáveis por tipo de projeto e plataforma |
| R5 | **Qualidade de dados de entrada ruim** | Alta | Alto | DQ checks obrigatórios no Gate 1 + profiling automático |
| R6 | **Custos de API/tokens elevados** | Média | Médio | Monitoramento de uso + limites por projeto + caching |
| R7 | **Prompts desatualizados** | Média | Médio | Versionamento Git + revisão trimestral |

---

## 14. Roadmap de Implementação

| Fase | Objetivo | Entregáveis | Critério de Sucesso | Dependências |
|------|----------|-------------|---------------------|--------------|
| **Fase 0 - POC** | Validar framework com cenário fictício | Pipeline Trip Data completo via agentes | Pipeline funciona end-to-end | Ambiente de dev, LLM access |
| **Fase 1 - MVP** | Primeiro projeto real com cliente | Framework básico operacional | Lead time < baseline manual | POC aprovada, cliente piloto |
| **Fase 2 - Escala** | Expansão para múltiplos projetos | Templates por tipo de projeto | Adoção por 3+ equipes | MVP validado |
| **Fase 3 - Produto** | Oferta padronizada Avanade | Playbook + programa de treinamento | ROI documentado e replicável | Escala comprovada |

---

## 15. Dependências Técnicas

| Dependência | Tipo | Status | Responsável | Ação Necessária |
|-------------|------|--------|-------------|-----------------|
| **LLM (Claude/GPT)** | Infraestrutura | Disponível | TI Avanade | Definir modelo padrão e contratos |
| **Ambiente de Execução** | Infraestrutura | A definir | Arquitetura | Decidir: Cloud vs Local vs Híbrido |
| **Repositório de Prompts** | Tooling | A criar | Equipe Framework | Setup Git + estrutura de pastas |
| **Dados de Exemplo** | Dados | Disponível | Equipe Framework | Usar cenário Trip Data |
| **Plataforma de Dados** | Variável | Por projeto | Cliente | Templates multi-plataforma (Databricks, Synapse, etc.) |

---

## 16. Requisitos

### 16.1 Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceitação |
|----|-----------|------------|----------------------|
| RF01 | Fluxo sequencial por agente | Alta | Agentes executam na ordem UP→MID→DOWN |
| RF02 | Gates obrigatórios entre esteiras | Alta | Transição bloqueada se critérios não atendidos |
| RF03 | Artefatos versionáveis | Alta | Todos outputs em Git com histórico |
| RF04 | Trilha de auditoria completa | Alta | Log de todas ações de agentes |
| RF05 | Geração de código SQL/PySpark | Alta | Código executável e testado |
| RF06 | Geração de DDL | Alta | Scripts de criação de tabelas |
| RF07 | Geração de testes automatizados | Média | Cobertura > 80% |
| RF08 | Profiling automático de dados | Média | Tipos derivados automaticamente |
| RF09 | DQ checks configuráveis | Alta | Regras de qualidade aplicadas |

### 16.2 Requisitos Não Funcionais

| ID | Requisito | Especificação | Métrica |
|----|-----------|---------------|---------|
| RNF01 | **Auditabilidade** | Toda ação rastreável | 100% de cobertura de logs |
| RNF02 | **Escalabilidade** | Suportar múltiplos projetos simultâneos | Até 10 projetos paralelos |
| RNF03 | **Segurança** | Conformidade LGPD/GDPR | Zero vazamentos de dados |
| RNF04 | **Performance** | Tempo de resposta do agente | < 30s por interação |
| RNF05 | **Disponibilidade** | Uptime do framework | > 99% em horário comercial |

---

## 17. RACI

| Atividade | Liderança | Arquitetos | Consultores | Clientes |
|-----------|-----------|------------|-------------|----------|
| Definição de requisitos | A | C | R | I |
| Design de arquitetura | I | A/R | C | I |
| Execução de pipeline | I | C | A/R | I |
| Validação de gates | A | R | R | C |
| Aprovação final | A | C | I | R |

**Legenda:** R=Responsible, A=Accountable, C=Consulted, I=Informed

---

## 18. Glossário

| Termo | Definição |
|-------|-----------|
| **BMAD** | Business/Method/Agent/Data - Framework híbrido de desenvolvimento |
| **AOD** | Architecture Overview Document |
| **DDS** | Detailed Design Specification |
| **STTM** | Source-to-Target Mapping |
| **DQ** | Data Quality |
| **DDL** | Data Definition Language |
| **Gate** | Ponto de controle obrigatório entre fases |
| **Esteira** | Grupo de atividades relacionadas (UP/MID/DOWN) |

---

## 19. Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | - | - | Versão inicial - modelo operacional |
| 2.0 | 2026-01-21 | Mary (BA Agent) + F.a.almeida | Adição de: métricas quantificáveis, caso de uso piloto, stakeholders, riscos, roadmap, dependências, critérios de aceitação |

---

## 20. Próximos Passos

1. [ ] **Preencher baselines** - Coletar dados de projetos anteriores para métricas
2. [ ] **Configurar ambiente POC** - Setup de LLM e repositório
3. [ ] **Executar Fase 0** - Validar framework com Trip Data Pipeline
4. [ ] **Documentar lições aprendidas** - Retrospec pós-POC
5. [ ] **Identificar cliente piloto** - Para Fase 1 (MVP)

---

*Documento gerado com apoio do BMAD Framework - Business Analyst Agent (Mary)*
