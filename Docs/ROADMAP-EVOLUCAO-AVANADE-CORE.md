# Roadmap de Evolução: Avanade Core Agents

## Plano de Expansão do Ecossistema de Agentes

**Data:** Fevereiro 2026  
**Versão:** 1.0  
**Status:** Aprovação Pendente

---

## 📋 Sumário Executivo

### Situação Atual

| Categoria | Agentes | Status |
|-----------|---------|--------|
| **Data Engineering** | 1 (DataFlow) | ✅ Operacional |
| **BI Development** | 1 (InsightForge) | ✅ Operacional |
| **Agile/Product** | 3 (PM, PO, SM) | ✅ Operacional |
| **Delivery** | 1 (DeliveryPro) | ✅ Operacional |
| **Estratégia & Governança** | 0 | ❌ Gap identificado |

### Objetivo

Expandir o ecossistema Avanade Core para cobrir o ciclo completo de projetos de dados:
- **Novos agentes** para estratégia, arquitetura e governança
- **Gates de qualidade** para transições entre fases
- **Orquestração** centralizada do fluxo de trabalho
- **Integração VS Code** via chatmodes para todos os agentes

---

## 🎯 Decisões Estratégicas

### Decisão 1: Quais agentes criar?

| Agente | Decisão | Justificativa |
|--------|---------|---------------|
| DataStrategist | 🆕 **CRIAR** | Definição de valor e KPIs |
| BusinessAnalyst | 🆕 **CRIAR** | STTM e requisitos técnicos |
| DataArchitect | 🆕 **CRIAR** | Arquitetura e modelagem |
| DataSteward | 🆕 **CRIAR** | Governança e qualidade |
| Orchestrator | 🆕 **CRIAR** | Gates e coordenação |
| DataFlow | 🔄 **ENRIQUECER** | Adicionar validações de gate |
| InsightForge | 🔄 **ENRIQUECER** | Integrar com modelo semântico |

### Decisão 2: Como estruturar?

**Arquitetura em Esteiras:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    AVANADE CORE AGENTS                          │
├─────────────────────────────────────────────────────────────────┤
│  Estrutura: .avanade-core/                                      │
│  Formato: Markdown + YAML                                       │
│  Ativação: VS Code Chatmodes                                    │
│  Execução: Task-first com *commands                             │
│  Governança: Gates obrigatórios entre esteiras                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  UPSTREAM    │────▶│  MIDSTREAM   │────▶│  DOWNSTREAM  │
│  Estratégia  │     │  Arquitetura │     │  Execução    │
└──────────────┘     └──────────────┘     └──────────────┘
      │ Gate 1            │ Gate 2            │ Gate 3
```

---

## 📊 Matriz de Responsabilidades Final

### Ecossistema Completo (11 Agentes)

| # | Agente | Esteira | Status | Responsabilidades |
|---|--------|---------|--------|-------------------|
| 1 | **DataStrategist** | UP | 🆕 Criar | KPIs, Problem Statement, Success Criteria |
| 2 | **BusinessAnalyst** | UP | 🆕 Criar | STTM, Analytical Questions, DQ inicial |
| 3 | **DataArchitect** | MID | 🆕 Criar | AOD/DDS, Modelo Lógico, Decisões |
| 4 | **DataFlow** | MID/DOWN | 🔄 Melhorar | Pipelines, DDL, ETL, Testes |
| 5 | **InsightForge** | DOWN | 🔄 Melhorar | Semantic Layer, DAX, Dashboards |
| 6 | **DataSteward** | DOWN | 🆕 Criar | Governança, DQ Rules, Compliance |
| 7 | **Orchestrator** | CORE | 🆕 Criar | Gates, Routing, Estado |
| 8 | **ProductVision** | AGILE | ✅ Manter | PRD, Features, Epics |
| 9 | **BacklogMaster** | AGILE | ✅ Manter | User Stories, AC, Backlog |
| 10 | **SprintPro** | AGILE | ✅ Manter | Sprints, Velocity, Ceremonies |
| 11 | **DeliveryPro** | PM | ✅ Manter | Estimativas, Roadmap, Riscos |

---

## 🗓️ Roadmap de Implementação

### Fase 1: Fundação (Semanas 1-3)

#### 1.1 Criar Orchestrator
**Prioridade:** 🔴 CRÍTICA

```yaml
agent:
  name: Orchestrator
  id: orchestrator
  title: Pipeline Orchestrator & Gate Validator
  icon: 🧭

commands:
  - status: Ver status atual do projeto e próximos passos
  - gate-1: Validar Gate 1 (UP→MID)
  - gate-2: Validar Gate 2 (MID→DOWN)
  - gate-3: Validar Gate 3 (DOWN→PROD)
  - route: Sugerir próximo agente/workflow
  - audit: Ver histórico de gates e decisões
```

**Tarefas:**
- [ ] Criar `orchestrator/.avanade-core/agents/orchestrator.md`
- [ ] Criar task `validate-gate.md` (parametrizável)
- [ ] Criar task `project-status.md`
- [ ] Criar task `route-next.md`
- [ ] Criar checklist `gate-checklist.md`
- [ ] Criar template `gate-report-tmpl.yaml`
- [ ] Criar chatmode `orchestrator.chatmode.md`

#### 1.2 Criar DataStrategist
**Prioridade:** 🔴 CRÍTICA

```yaml
agent:
  name: DataStrategist
  id: data-strategist
  title: Data Strategy & Value Definition Specialist
  icon: 🎯

commands:
  - define-problem: Definir Problem Statement
  - define-kpis: Estabelecer KPIs com baseline/target
  - success-criteria: Documentar critérios de sucesso
  - prepare-gate1: Preparar artefatos para Gate 1
```

**Tarefas:**
- [ ] Criar estrutura `.avanade-core/`
- [ ] Criar agent definition
- [ ] Criar tasks (4)
- [ ] Criar templates (2)
- [ ] Criar checklist
- [ ] Criar chatmode

---

### Fase 2: UPSTREAM (Semanas 4-5)

#### 2.1 Criar BusinessAnalyst
**Prioridade:** 🔴 CRÍTICA

```yaml
agent:
  name: BusinessAnalyst
  id: business-analyst
  title: Business Requirements & Data Mapping Specialist
  icon: 📋

commands:
  - analytical-questions: Estruturar perguntas analíticas
  - create-sttm: Criar Source-to-Target Mapping
  - define-dq: Definir critérios de qualidade iniciais
  - business-rules: Traduzir regras de negócio
```

**Tarefas:**
- [ ] Criar estrutura `.avanade-core/`
- [ ] Criar tasks para STTM, DQ, regras
- [ ] Criar template STTM (YAML)
- [ ] Integrar com DataStrategist

---

### Fase 3: MIDSTREAM (Semanas 6-8)

#### 3.1 Criar DataArchitect
**Prioridade:** 🟠 ALTA

```yaml
agent:
  name: DataArchitect
  id: data-architect
  title: Data Solution Architect & Modeler
  icon: 🏛️

commands:
  - create-architecture: Criar AOD/DDS
  - create-data-model: Criar modelo lógico
  - document-decisions: Registrar decisões arquiteturais
  - prepare-gate2: Preparar artefatos para Gate 2
  - review-architecture: Revisar arquitetura existente
```

**Responsabilidades:** Arquitetura técnica + Modelagem de dados

#### 3.2 Melhorar DataFlow
**Prioridade:** 🟠 ALTA

**Adições ao DataFlow existente:**

```yaml
# Adicionar ao commands existente:
commands:
  # ... comandos existentes ...
  - check-contracts: Validar contracts antes de executar
  - register-lineage: Registrar lineage no catálogo
  - prepare-gate3: Preparar artefatos para Gate 3

# Adicionar metadata:
metadata:
  esteira: DOWNSTREAM
  requires_gate: 2
  outputs_to: data-steward, orchestrator
```

---

### Fase 4: DOWNSTREAM (Semanas 9-11)

#### 4.1 Criar DataSteward
**Prioridade:** 🟠 ALTA

```yaml
agent:
  name: DataSteward
  id: data-steward
  title: Data Governance & Quality Specialist
  icon: 🛡️

commands:
  - create-dq-rules: Definir regras de qualidade
  - create-monitoring: Criar spec de observabilidade
  - compliance-check: Verificar LGPD/GDPR
  - create-catalog: Criar/atualizar catálogo de dados
  - audit-report: Gerar relatório de auditoria
```

#### 4.2 Melhorar InsightForge
**Prioridade:** 🟡 MÉDIA

**Adições:**
- Integração com modelo semântico do DataArchitect
- Validação de métricas contra DQ rules
- Registro de medidas no catálogo

---

### Fase 5: Integração (Semanas 12-13)

#### 5.1 Criar Chatmodes para todos os novos agentes
#### 5.2 Atualizar documentação
#### 5.3 Criar demos de fluxo completo
#### 5.4 Testes de integração

---

## 📁 Estrutura de Pastas Final

```
Agents-Data-Enginer/
├── orchestrator/                    # 🆕 CRIAR
│   ├── .avanade-core/
│   │   ├── agents/
│   │   │   └── orchestrator.md
│   │   ├── tasks/
│   │   │   ├── validate-gate.md
│   │   │   ├── project-status.md
│   │   │   └── route-next.md
│   │   ├── templates/
│   │   │   └── gate-report-tmpl.yaml
│   │   ├── checklists/
│   │   │   ├── gate-1-checklist.md
│   │   │   ├── gate-2-checklist.md
│   │   │   └── gate-3-checklist.md
│   │   └── core-config.yaml
│   ├── orchestrator.chatmode.md
│   └── README.md
│
├── data-strategist/                 # 🆕 CRIAR
│   ├── .avanade-core/
│   │   ├── agents/
│   │   │   └── data-strategist.md
│   │   ├── tasks/
│   │   │   ├── define-problem-statement.md
│   │   │   ├── define-kpis.md
│   │   │   ├── define-success-criteria.md
│   │   │   └── prepare-gate1.md
│   │   ├── templates/
│   │   │   ├── problem-statement-tmpl.yaml
│   │   │   └── kpis-tmpl.yaml
│   │   ├── checklists/
│   │   │   └── strategist-checklist.md
│   │   └── core-config.yaml
│   ├── data-strategist.chatmode.md
│   └── README.md
│
├── business-analyst/                # 🆕 CRIAR
│   ├── .avanade-core/
│   │   ├── agents/
│   │   │   └── business-analyst.md
│   │   ├── tasks/
│   │   │   ├── create-sttm.md
│   │   │   ├── analytical-questions.md
│   │   │   ├── define-dq-initial.md
│   │   │   └── translate-business-rules.md
│   │   ├── templates/
│   │   │   ├── sttm-tmpl.yaml
│   │   │   └── analytical-questions-tmpl.yaml
│   │   ├── checklists/
│   │   │   └── analyst-checklist.md
│   │   └── core-config.yaml
│   ├── business-analyst.chatmode.md
│   └── README.md
│
├── data-architect/                  # 🆕 CRIAR
│   ├── .avanade-core/
│   │   ├── agents/
│   │   │   └── data-architect.md
│   │   ├── tasks/
│   │   │   ├── create-architecture.md
│   │   │   ├── create-data-model.md
│   │   │   ├── document-decisions.md
│   │   │   └── prepare-gate2.md
│   │   ├── templates/
│   │   │   ├── architecture-tmpl.yaml
│   │   │   └── data-model-tmpl.yaml
│   │   ├── checklists/
│   │   │   └── architect-checklist.md
│   │   └── core-config.yaml
│   ├── data-architect.chatmode.md
│   └── README.md
│
├── data-steward/                    # 🆕 CRIAR
│   ├── .avanade-core/
│   │   ├── agents/
│   │   │   └── data-steward.md
│   │   ├── tasks/
│   │   │   ├── create-dq-rules.md
│   │   │   ├── create-monitoring.md
│   │   │   ├── compliance-check.md
│   │   │   └── audit-report.md
│   │   ├── templates/
│   │   │   ├── dq-rules-tmpl.yaml
│   │   │   └── monitoring-tmpl.yaml
│   │   ├── checklists/
│   │   │   └── steward-checklist.md
│   │   └── core-config.yaml
│   ├── data-steward.chatmode.md
│   └── README.md
│
├── Agent-data-engineer/             # 🔄 MELHORAR
│   └── dataflow-agent-export/
│       └── .avanade-core/
│           └── (adicionar tasks de gates)
│
├── bi-developer-agent/              # 🔄 MELHORAR
│   └── .avanade-core/
│       └── (adicionar integração semântica)
│
├── delivery-lead-agent/             # ✅ MANTER
├── po-pm-sm/                        # ✅ MANTER
│
└── Docs/
    ├── ANALISE-COMPARATIVA-AGENTES.md
    ├── WORKFLOWS-ESTEIRAS-GATES.md
    └── ROADMAP-EVOLUCAO.md          # 🆕 ESTE DOCUMENTO
```

---

## ✅ Checklist de Implementação

### Fase 1: Fundação
- [ ] Orchestrator criado e testado
- [ ] DataStrategist criado e testado
- [ ] Gate 1 funcional
- [ ] Documentação atualizada

### Fase 2: UPSTREAM
- [ ] BusinessAnalyst criado e testado
- [ ] STTM template funcional
- [ ] Fluxo UP completo validado

### Fase 3: MIDSTREAM
- [ ] DataArchitect criado e testado
- [ ] DataFlow melhorado
- [ ] Gate 2 funcional
- [ ] Fluxo MID completo validado

### Fase 4: DOWNSTREAM
- [ ] DataSteward criado e testado
- [ ] InsightForge melhorado
- [ ] Gate 3 funcional
- [ ] Fluxo DOWN completo validado

### Fase 5: Integração
- [ ] Todos os chatmodes criados
- [ ] Demos funcionando
- [ ] Documentação completa
- [ ] Treinamento preparado

---

## 📈 Métricas de Sucesso

| Métrica | Baseline | Target | Como Medir |
|---------|----------|--------|------------|
| **Agentes Operacionais** | 7 | 11 | Contagem |
| **Cobertura de Gates** | 0% | 100% | Gates implementados / 3 |
| **Lead Time Redução** | — | 40% | Tempo médio de projeto |
| **Retrabalho Redução** | — | 60% | Tickets de correção |
| **Satisfação do Time** | — | 85% | Survey |

---

## 🔗 Próximos Passos Imediatos

1. **Revisar este documento** com stakeholders
2. **Priorizar** agentes da Fase 1
3. **Criar primeira versão** do Orchestrator
4. **Testar** com projeto piloto
5. **Iterar** baseado em feedback

---

*Documento Avanade Core Agents - Fevereiro 2026*
