# Comparação Completa de Documentos dos Agentes

## Avanade Method (Core) vs BMAD-Data Agents

**Data:** Janeiro 2026  
**Autor:** Master Agent  
**Versão:** 1.0

---

## 📊 Resumo Executivo

| Métrica | Avanade Core | BMAD-Data |
|---------|--------------|-----------|
| **Total de Agentes** | 7 | 10 |
| **Arquivos por Agente** | ~25-30 | 2-3 |
| **Workflows** | Embutidos em Tasks | 14 separados |
| **Templates** | YAML estruturados | Não definidos |
| **Checklists** | MD dedicados | Embutidos em Gates |
| **Gates/Validações** | Opcional | Obrigatório (3 gates) |

---

## 🔵 AVANADE CORE AGENTS - Inventário Completo

### 1. DataFlow (Data Engineer)

**Localização:** `Agent-data-engineer/dataflow-agent-export/.avanade-core/`

| Categoria | Arquivos | Descrição |
|-----------|----------|-----------|
| **Agents** | 1 | `data-engineer.md` (135 linhas) |
| **Tasks** | 16 | Workflows executáveis |
| **Templates** | 4 | YAML estruturados |
| **Checklists** | 1 | Validação de qualidade |
| **Data** | 1 | Referência de boas práticas |
| **Config** | 1 | `core-config.yaml` |

**Tasks Detalhadas:**
```
├── analyze-data-gaps.md
├── analyze-existing-pipeline.md
├── create-data-tests.md
├── create-ddl-scripts.md
├── create-documentation.md
├── create-etl-scripts.md
├── create-pipeline.md
├── execute-checklist.md
├── explain-pipeline.md
├── generate-outputs.md
├── help.md
├── optimize-queries.md
├── profile-data-sources.md
├── recommend-tools.md
├── review-code.md
└── validate-data-quality.md
```

**Templates:**
```
├── data-pipeline-tmpl.yaml
├── data-tests-tmpl.yaml
├── ddl-scripts-tmpl.yaml
└── etl-scripts-tmpl.yaml
```

**Checklist:** `data-engineer-checklist.md`  
**Data:** `data-engineering-best-practices.md`

---

### 2. InsightForge (BI Developer)

**Localização:** `bi-developer-agent/.avanade-core/`

| Categoria | Arquivos | Descrição |
|-----------|----------|-----------|
| **Agents** | 0* | Não possui pasta agents |
| **Tasks** | 13 | Workflows BI |
| **Templates** | 4 | YAML para BI |
| **Checklists** | 3 | Validações BI |
| **Data** | 2 | Referências técnicas |
| **Config** | 1 | `core-config.yaml` |

**Tasks Detalhadas:**
```
├── analyze-existing-model.md
├── create-dashboard.md
├── create-dax-measures.md
├── create-documentation.md
├── create-semantic-model.md
├── execute-checklist.md
├── generate-outputs.md
├── help.md
├── implement-rls.md
├── optimize-performance.md
├── recommend-visualizations.md
├── review-model.md
└── validate-measures.md
```

**Templates:**
```
├── bi-requirements-tmpl.yaml
├── dashboard-spec-tmpl.yaml
├── dax-library-tmpl.yaml
└── semantic-model-tmpl.yaml
```

**Checklists:**
```
├── bi-developer-checklist.md
├── dashboard-review-checklist.md
└── performance-checklist.md
```

**Data:**
```
├── bi-best-practices.md
└── dax-patterns-reference.md
```

---

### 3. DeliveryPro (Delivery Lead)

**Localização:** `delivery-lead-agent/.avanade-core/`

| Categoria | Arquivos | Descrição |
|-----------|----------|-----------|
| **Agents** | 1 | `delivery-lead.md` (150 linhas) |
| **Tasks** | 12 | Workflows de gestão |
| **Templates** | 5 | YAML para delivery |
| **Checklists** | 3 | Validações de projeto |
| **Data** | 2 | Referências |
| **Config** | 1 | `core-config.yaml` |

**Tasks Detalhadas:**
```
├── assess-risks.md
├── create-documentation.md
├── create-roadmap.md
├── create-status-report.md
├── estimate-project.md
├── execute-checklist.md
├── generate-outputs.md
├── help.md
├── manage-changes.md
├── plan-delivery.md
├── review-delivery.md
└── track-progress.md
```

**Templates:**
```
├── delivery-plan-tmpl.yaml
├── exec-summary-tmpl.yaml
├── project-estimation-tmpl.yaml
├── risk-register-tmpl.yaml
└── roadmap-tmpl.yaml
```

**Checklists:**
```
├── change-checklist.md
├── delivery-lead-checklist.md
└── project-kickoff-checklist.md
```

**Data:**
```
├── cost-benchmarks.md
└── delivery-best-practices.md
```

---

### 4. PO-PM-SM (Product Owner, Product Manager, Scrum Master)

**Localização:** `po-pm-sm/.avanade-core/`

| Categoria | Arquivos | Descrição |
|-----------|----------|-----------|
| **Agents** | 3 | PO, PM, SM separados |
| **Tasks** | 10 | Workflows Agile |
| **Templates** | 4 | YAML para Agile |
| **Checklists** | 4 | Validações de role |
| **Data** | 2 | Referências |
| **Config** | 1 | `core-config.yaml` |

**Agents:**
```
├── product-manager.md
├── product-owner.md
└── scrum-master.md
```

**Tasks:**
```
├── create-epic.md
├── create-user-story.md
├── execute-checklist.md
├── help.md
├── identify-dependencies.md
├── next-story.md
├── organize-sprints.md
├── prepare-planning.md
├── refine-backlog.md
└── retrospective.md
```

**Templates:**
```
├── backlog-tmpl.yaml
├── epic-tmpl.yaml
├── sprint-plan-tmpl.yaml
└── user-story-tmpl.yaml
```

**Checklists:**
```
├── product-manager-checklist.md
├── product-owner-checklist.md
├── scrum-master-checklist.md
└── story-quality-checklist.md
```

**Data:**
```
├── agile-best-practices.md
└── estimation-reference.md
```

---

## 🟠 BMAD-DATA AGENTS - Inventário Completo

### Estrutura do Agente BMAD

Cada agente possui **2-3 arquivos**:
- `{nome}.md` - Definição do agente (ativação, persona, menu)
- `{nome}.spec.md` - Especificação técnica (metadata, integração)
- Workflows associados (externos)

**Localização:** `data-migration/src/modules/data_agents/agents/`

---

### Lista Completa de Agentes BMAD

| # | Agente | Esteira | Função Principal |
|---|--------|---------|------------------|
| 1 | **data-strategist** (Samuel) | UPSTREAM | Estratégia de dados, PRD |
| 2 | **business-analyst** (Beatriz) | UPSTREAM | Análise de negócio, requisitos |
| 3 | **data-solution-architect** (André) | MIDSTREAM | Arquitetura técnica, decisões |
| 4 | **data-modeler** (Marina) | MIDSTREAM | Modelagem lógica/física |
| 5 | **agent-designer** (Nova) | CORE (Meta) | Design de agentes (OPCIONAL) |
| 6 | **data-engineer-exec** (Diego) | DOWNSTREAM | Geração de DDL/SQL/PySpark |
| 7 | **bi-semantic** (Isabela) | DOWNSTREAM | Modelo semântico, DAX |
| 8 | **data-steward** (Gabriel) | DOWNSTREAM | Governança, qualidade |
| 9 | **iteration-improvement** (Luana) | TRANSVERSAL | Melhoria contínua |
| 10 | **orchestrator** (Orion) | TRANSVERSAL | Gates, roteamento |

---

### Detalhamento por Agente BMAD

#### 1. data-strategist (Samuel)
```
├── data-strategist.md (~75 linhas)
└── data-strategist.spec.md (~80 linhas)

Workflows associados:
├── data-strategy/
└── agent-contracts/
```

#### 2. business-analyst (Beatriz)
```
├── business-analyst.md (~75 linhas)
└── business-analyst.spec.md (~80 linhas)

Workflows associados:
├── business-analysis/
└── agent-contracts/
```

#### 3. data-solution-architect (André)
```
├── data-solution-architect.md (~85 linhas)
└── data-solution-architect.spec.md (~90 linhas)

Workflows associados:
├── architecture/
└── agent-contracts/
```

#### 4. data-modeler (Marina)
```
├── data-modeler.md (~80 linhas)
└── data-modeler.spec.md (~85 linhas)

Workflows associados:
├── data-model/
└── agent-contracts/
```

#### 5. agent-designer (Theo)
```
├── agent-designer.md (~70 linhas)
└── agent-designer.spec.md (~75 linhas)

Workflows associados:
└── agent-blueprint/
```

#### 6. data-engineer-exec (Diego)
```
├── data-engineer-exec.md (~75 linhas)
└── data-engineer-exec.spec.md (~93 linhas)

Workflows associados:
├── delivery/
├── unit-tests/
└── governance/
```

#### 7. bi-semantic (Isabela)
```
├── bi-semantic.md (~75 linhas)
└── bi-semantic.spec.md (~80 linhas)

Workflows associados:
├── delivery/
└── governance/
```

#### 8. data-steward (Gabriel)
```
├── data-steward.md (~80 linhas)
└── data-steward.spec.md (~85 linhas)

Workflows associados:
└── governance/
```

#### 9. iteration-improvement (Luana)
```
├── iteration-improvement.md (~70 linhas)
└── iteration-improvement.spec.md (~75 linhas)

Workflows associados:
└── workflow-status/
```

#### 10. orchestrator (Orion)
```
├── orchestrator.md (~80 linhas)
└── orchestrator.spec.md (~85 linhas)

Workflows associados:
├── workflow-status/
├── gate-1-up-mid/
├── gate-2-mid-down/
├── gate-3-down-prod/
└── routing/
```

---

### Workflows BMAD (14 Total)

| Workflow | Tipo | Esteira | Descrição |
|----------|------|---------|-----------|
| `agent-blueprint/` | Create-only | META | Criar novos agentes |
| `agent-contracts/` | Tri-modal | UP/MID | Definir contratos |
| `architecture/` | Create-only | MID | Arquitetura técnica |
| `business-analysis/` | Tri-modal | UP | Análise de negócio |
| `data-model/` | Create-only | MID | Modelagem de dados |
| `data-strategy/` | Create-only | UP | Estratégia de dados |
| `delivery/` | Create-only | DOWN | DDL/SQL/PySpark |
| `gate-1-up-mid/` | Validation | Gate | UP → MID |
| `gate-2-mid-down/` | Validation | Gate | MID → DOWN |
| `gate-3-down-prod/` | Validation | Gate | DOWN → PROD |
| `governance/` | Create-only | DOWN | Governança |
| `routing/` | Utility | META | Roteamento |
| `unit-tests/` | Create-only | DOWN | Testes |
| `workflow-status/` | Query | META | Status |

---

## 📐 Comparação Estrutural Detalhada

### Estrutura de Arquivo do Agente

| Aspecto | Avanade Core | BMAD-Data |
|---------|--------------|-----------|
| **Formato Principal** | Markdown + YAML embedded | XML embedded em Markdown |
| **Tamanho Médio** | 100-150 linhas | 70-90 linhas |
| **Persona** | YAML block | XML `<persona>` |
| **Menu/Commands** | YAML dependencies | XML `<menu>` items |
| **Ativação** | `activation-instructions` (YAML) | `<activation>` (XML) |
| **Workflows** | Tasks individuais | Referências externas |

### Exemplo de Persona (Comparação)

**Avanade Core:**
```yaml
persona:
  role: Senior Data Engineer & Pipeline Architect
  style: Precise, methodical, quality-focused
  identity: Master of data pipelines...
  focus: Data ingestion, transformation...
  core_principles:
    - Data Quality First
    - Layered Architecture
    - ...
```

**BMAD-Data:**
```xml
<persona>
  <role>Data Engineer (DOWNSTREAM)</role>
  <identity>Engenheiro de dados hands-on...</identity>
  <communication_style>Prático e técnico...</communication_style>
  <principles>
    - Nunca pular gates
    - Código executável e testado
    - ...
  </principles>
</persona>
```

---

## 🎯 Tabela de Equivalência Funcional

| Função | Avanade Core Agent | BMAD-Data Agent |
|--------|-------------------|-----------------|
| **Data Engineering** | DataFlow | data-engineer-exec |
| **BI/Analytics** | InsightForge | bi-semantic |
| **Delivery/PM** | DeliveryPro | — |
| **Product Owner** | BacklogMaster | — |
| **Product Manager** | VisionCraft | — |
| **Scrum Master** | AgilityGuide | — |
| **Estratégia de Dados** | — | data-strategist |
| **Análise de Negócio** | — | business-analyst |
| **Arquitetura** | — | data-solution-architect |
| **Modelagem de Dados** | — | data-modeler |
| **Design de Agentes** | — | agent-designer |
| **Governança** | — | data-steward |
| **Melhoria Contínua** | — | iteration-improvement |
| **Orquestração/Gates** | — | orchestrator |

---

## 📂 Contagem Total de Arquivos

### Avanade Core

| Pasta | DataFlow | InsightForge | DeliveryPro | PO-PM-SM | **Total** |
|-------|----------|--------------|-------------|----------|-----------|
| agents/ | 1 | 0 | 1 | 3 | **5** |
| tasks/ | 16 | 13 | 12 | 10 | **51** |
| templates/ | 4 | 4 | 5 | 4 | **17** |
| checklists/ | 1 | 3 | 3 | 4 | **11** |
| data/ | 1 | 2 | 2 | 2 | **7** |
| config | 1 | 1 | 1 | 1 | **4** |
| **Total** | **24** | **23** | **24** | **24** | **95** |

### BMAD-Data

| Categoria | Arquivos |
|-----------|----------|
| Agents (MD + Spec) | 20 |
| Workflows (pastas) | 14 |
| **Total** | **34+** |

*Nota: Cada workflow pode conter múltiplos arquivos internos (steps)*

---

## 🔄 Mapeamento de Conceitos

| Conceito | Avanade Core | BMAD-Data |
|----------|--------------|-----------|
| **Definição do Agente** | `.avanade-core/agents/*.md` | `agents/*.md` |
| **Especificação** | Embutida no agente | `agents/*.spec.md` |
| **Workflows** | `tasks/*.md` | `workflows/*/` |
| **Templates** | `templates/*.yaml` | Não definido |
| **Validações** | `checklists/*.md` | Gates + Workflows |
| **Referências** | `data/*.md` | PRD + Architecture |
| **Config** | `core-config.yaml` | BMAD globals |
| **Ativação VS Code** | `.chatmode.md` | Não implementado |

---

## 🏗️ Arquitetura de Documentação

### Avanade Core (Flat Structure)
```
.avanade-core/
├── agents/           # Definições de agentes
├── tasks/            # Workflows executáveis
├── templates/        # Estruturas YAML
├── checklists/       # Validações manuais
├── data/             # Referências técnicas
└── core-config.yaml  # Configuração global
```

### BMAD-Data (Modular Structure)
```
data_agents/
├── agents/           # Agentes + Specs
│   ├── *.md          # Definição
│   └── *.spec.md     # Especificação
└── workflows/        # Workflows separados
    ├── */            # Um por workflow
    │   ├── workflow.md
    │   ├── *.spec.md
    │   └── steps-c/  # Steps do workflow
```

---

## ✅ Conclusão

### Forças do Avanade Core
- ✅ Maior quantidade de conteúdo pronto
- ✅ Templates YAML estruturados
- ✅ Checklists dedicados
- ✅ Integração VS Code via chatmodes
- ✅ Execução imediata (task-first)

### Forças do BMAD-Data
- ✅ Arquitetura mais modular
- ✅ Gates obrigatórios (qualidade)
- ✅ Separação clara de esteiras
- ✅ Specs separadas (manutenibilidade)
- ✅ Orquestração centralizada

### Recomendação de Convergência
1. **Adotar** estrutura modular do BMAD para workflows complexos
2. **Manter** templates YAML do Avanade Core
3. **Implementar** gates do BMAD no Avanade Core
4. **Preservar** chatmodes para ativação VS Code
5. **Unificar** referências em pasta `data/` comum

---

## Anexo: Mapa Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                    AVANADE CORE AGENTS                          │
├─────────────────────────────────────────────────────────────────┤
│  DataFlow (24 docs)  │  InsightForge (23 docs)                  │
│  DeliveryPro (24 docs) │ PO-PM-SM (24 docs)                     │
│  ─────────────────────────────────────────────────────────────  │
│  Estrutura: Flat, task-first, VS Code integrated                │
│  Total: ~95 arquivos                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BMAD-DATA AGENTS                           │
├─────────────────────────────────────────────────────────────────┤
│  UPSTREAM: data-strategist, business-analyst                    │
│  MIDSTREAM: data-solution-architect, data-modeler, agent-design │
│  DOWNSTREAM: data-engineer-exec, bi-semantic, data-steward      │
│  TRANSVERSAL: orchestrator, iteration-improvement               │
│  ─────────────────────────────────────────────────────────────  │
│  Estrutura: Modular, gate-driven, workflow-separated            │
│  Total: 10 agentes + 14 workflows                               │
└─────────────────────────────────────────────────────────────────┘
```

---

*Documento gerado automaticamente pelo Master Agent*
