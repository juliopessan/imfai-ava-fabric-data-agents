# Guia de Padronização Estrutural — fabric-data-agents

> **Objetivo:** Alinhar a estrutura de pastas do `imfai-ava-fabric-data-agents` ao padrão
> estabelecido pelo `imfai-ava-fabric-apps-agents`, preservando integralmente o escopo
> e o conteúdo específico da fábrica de migração de dados.
>
> **Premissa importante:** Os dois repositórios têm escopos distintos —
> `fabric-apps` migra stacks de aplicação (Delphi → .NET/Angular) e
> `fabric-data` migra dados e pipelines (legado → Databricks/Azure).
> A padronização é **estrutural**, nunca de conteúdo.

---

## Sumário

1. [Visão geral das mudanças](#1-visão-geral-das-mudanças)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Fase 1 — Limpeza imediata](#3-fase-1--limpeza-imediata)
4. [Fase 2 — Renomeações e movimentações simples](#4-fase-2--renomeações-e-movimentações-simples)
5. [Fase 3 — Reestruturação das Skills](#5-fase-3--reestruturação-das-skills)
6. [Fase 4 — Reestruturação dos Agentes](#6-fase-4--reestruturação-dos-agentes)
7. [Fase 5 — Reestruturação dos Módulos src/](#7-fase-5--reestruturação-dos-módulos-src)
8. [Fase 6 — Ajustes finais e validação](#8-fase-6--ajustes-finais-e-validação)
9. [Estrutura alvo completa](#9-estrutura-alvo-completa)
10. [Checklist de execução](#10-checklist-de-execução)

---

## 1. Visão geral das mudanças

| Categoria | Ação | Impacto |
|---|---|---|
| `.venv/`, `.pytest_cache/`, `.vscode/` | Remover do versionamento + gitignore | Baixo |
| `azure-databricks-integration/`, `azure-mcp-server/` | Avaliar e mover para branch/repo próprio | Médio |
| `.avanade-core/` na raiz | Dissolver — conteúdo migra para `src/modules/` | Alto |
| `Docs/` | Renomear para `docs/` e revisar conteúdo | Baixo |
| `.github/agents/` (arquivos soltos) | Reorganizar com subpasta por agente em `src/modules/` | Alto |
| `.github/skills/` | Eliminar duplicatas, padronizar prefixo `ava-dmf-*` | Médio |
| `.github/ISSUE_TEMPLATE/`, `workflows/` | Remover ou mover para pipeline de CI separado | Baixo |
| `*-agent/` na raiz | Dissolver — conteúdo migra para `src/modules/` | Alto |
| `scripts/` e `tests/` | Mover para dentro de `src/modules/` | Médio |
| `src/modules/` | Reorganizar sob `dmf-fabric-agents/` com subpastas por agente | Alto |
| `AGENTS.md`, `wave-config-sample.yaml` | Mover para `docs/` ou `src/shared/` | Baixo |

---

## 2. Pré-requisitos

```bash
# Criar branch de trabalho antes de qualquer alteração
git checkout -b feat/standardize-folder-structure

# Confirmar que não há mudanças pendentes
git status
```

> **Nunca execute as fases diretamente na branch `main`.**
> Cada fase deve ser commitada separadamente para facilitar revisão e rollback.

---

## 3. Fase 1 — Limpeza imediata

Itens que não devem estar versionados e não têm equivalente no padrão do fabric-apps.

### 3.1 Atualizar `.gitignore`

Adicionar ao `.gitignore` as entradas abaixo caso ainda não existam:

```gitignore
# Ambiente virtual Python
.venv/
venv/
env/

# Cache pytest
.pytest_cache/

# VS Code
.vscode/

# Compilados Python
__pycache__/
*.pyc
*.pyo
```

```bash
# Remover do índice git (sem deletar os arquivos locais)
git rm -r --cached .venv/
git rm -r --cached .pytest_cache/
git rm -r --cached .vscode/
git rm -r --cached "**/__pycache__/"

git commit -m "chore: remove venv, cache e vscode do versionamento"
```

### 3.2 Avaliar `azure-databricks-integration/` e `azure-mcp-server/`

Essas pastas representam integrações específicas de infraestrutura que **não têm equivalente no fabric-apps** pois são exclusivas do escopo de dados. Há duas opções:

**Opção A — Manter como submódulo de infraestrutura (recomendada)**
Mover para um diretório próprio que sinalize claramente que se trata de integrações de plataforma, não de agentes:

```bash
mkdir -p infra/
git mv azure-databricks-integration/ infra/azure-databricks/
git mv azure-mcp-server/ infra/azure-mcp-server/
```

**Opção B — Extrair para repositório separado**
Se o time considerar que essas integrações crescerão de forma independente, o ideal é um repo próprio (`imfai-ava-fabric-data-infra`).

```bash
git commit -m "chore: move integrações de infraestrutura para infra/"
```

### 3.3 Remover arquivos soltos da raiz sem equivalente no padrão

```bash
# AGENTS.md → mover para docs/
mkdir -p docs/
git mv AGENTS.md docs/agents-catalog.md

# wave-config-sample.yaml → mover para src/shared/
mkdir -p src/shared/samples/
git mv wave-config-sample.yaml src/shared/samples/wave-config-sample.yaml

# Remover ISSUE_TEMPLATE (substituído pelo fluxo padrão de projetos)
git rm -r .github/ISSUE_TEMPLATE/

# Remover workflow de CI interno (será recriado no padrão correto se necessário)
git rm .github/workflows/ci-governance.yml

git commit -m "chore: reorganiza arquivos soltos da raiz para paths padronizados"
```

---

## 4. Fase 2 — Renomeações e movimentações simples

### 4.1 Renomear `Docs/` para `docs/`

```bash
git mv Docs/ docs/
```

O conteúdo de `docs/` no padrão fabric-apps contém dois arquivos principais:
- `agents-catalog.md` — catálogo de todos os agentes disponíveis
- `guia-execucao-fluxo-agentes.md` — passo a passo de como usar os agentes

Manter os arquivos existentes do fabric-data e criar o `guia-execucao-fluxo-agentes.md` equivalente para o contexto de migração de dados:

```bash
# O agents-catalog.md já foi movido de AGENTS.md no passo 3.3
# Criar o guia de execução específico para dados
touch docs/guia-execucao-fluxo-agentes.md

git commit -m "chore: padroniza docs/ (lowercase) e adiciona guia de execução"
```

### 4.2 Ajustar `project/context/`

No fabric-apps, a pasta `project/context/` contém **apenas**:
- `agent-task-config.yaml`
- `shared-context.md`

O arquivo `project-config.yaml` existe em `projects/_template/context/` (para novos projetos) mas **não** em `project/` (instância de trabalho ativa).

```bash
# Remover project-config.yaml de project/context/ se existir
git rm project/context/project-config.yaml

git commit -m "chore: alinha project/context/ ao padrão (remove project-config.yaml)"
```

### 4.3 Adicionar estrutura de outputs no `project/`

O fabric-apps mantém outputs de exemplo em `project/outputs/`. Criar a estrutura base:

```bash
mkdir -p project/outputs/upstream/inventory/
mkdir -p project/outputs/midstream/
mkdir -p project/outputs/downstream/ddl/
mkdir -p project/outputs/downstream/etl/
mkdir -p project/outputs/downstream/documentation/
mkdir -p project/outputs/downstream/tests/

# Criar .gitkeep para versionar pastas vazias
touch project/outputs/upstream/inventory/.gitkeep
touch project/outputs/midstream/.gitkeep
touch project/outputs/downstream/ddl/.gitkeep

git commit -m "feat: adiciona estrutura de outputs em project/ conforme padrão"
```

---

## 5. Fase 3 — Reestruturação das Skills

### 5.1 Situação atual

O fabric-data tem **duas cópias de cada skill**: uma sem prefixo e outra com prefixo `dmf-`. Isso é redundância que precisa ser eliminada.

```
# Exemplo do problema:
.github/skills/agent-orchestrator/SKILL.md      ← sem prefixo
.github/skills/dmf-agent-orchestrator/SKILL.md  ← com prefixo dmf-
```

### 5.2 Convenção de nomenclatura adotada

O fabric-apps usa o prefixo `ava-` seguido do **domínio** e do **nome funcional**.
Para o fabric-data, o padrão equivalente será `ava-dmf-` para sinalizar que é uma skill
específica da fábrica de dados dentro do ecossistema `ava-`.

| Antes (fabric-data) | Depois (padronizado) |
|---|---|
| `agent-orchestrator/` | `ava-dmf-agent-orchestrator/` |
| `dmf-agent-orchestrator/` | *(deletar — duplicata)* |
| `data-engineering-data-pipeline/` | `ava-dmf-data-pipeline/` |
| `dmf-data-engineering-data-pipeline/` | *(deletar — duplicata)* |
| `sql-optimization-patterns/` | `ava-dmf-sql-optimization/` |
| `data-quality-frameworks/` | `ava-dmf-data-quality/` |
| `autonomous-agents/` | `ava-dmf-autonomous-agents/` |

### 5.3 Script de renomeação das skills

```bash
cd .github/skills/

# ── PASSO 1: Deletar todas as versões sem prefixo (manter apenas dmf-*)
# (são duplicatas das versões dmf-)
for dir in agent-evaluation agent-governance agent-manager-skill \
            agent-memory-mcp agent-memory-systems \
            agent-orchestration agent-orchestration-improve-agent \
            agent-orchestration-multi-agent-optimize agent-orchestrator \
            agentic-development-principles agentic-eval agents-md \
            ai-agent-development ai-agents-architect autonomous-agent-patterns \
            autonomous-agents avanade-brand-guidelines \
            data-engineering-data-pipeline data-quality-frameworks \
            framework-migration-legacy-modernize multi-agent-brainstorming \
            multi-agent-patterns observability-monitoring-slo-implement \
            production-code-audit sql-optimization-patterns tdd-orchestrator; do
  git rm -r "$dir/" 2>/dev/null || true
done

# ── PASSO 2: Renomear as versões dmf-* para o novo padrão ava-dmf-*
declare -A renames=(
  ["dmf-agent-evaluation"]="ava-dmf-agent-evaluation"
  ["dmf-agent-governance"]="ava-dmf-agent-governance"
  ["dmf-agent-manager-skill"]="ava-dmf-agent-manager"
  ["dmf-agent-memory-mcp"]="ava-dmf-agent-memory-mcp"
  ["dmf-agent-memory-systems"]="ava-dmf-agent-memory-systems"
  ["dmf-agent-orchestration"]="ava-dmf-agent-orchestration"
  ["dmf-agent-orchestration-improve-agent"]="ava-dmf-orchestration-improve-agent"
  ["dmf-agent-orchestration-multi-agent-optimize"]="ava-dmf-multi-agent-optimize"
  ["dmf-agent-orchestrator"]="ava-dmf-agent-orchestrator"
  ["dmf-agentic-development-principles"]="ava-dmf-agentic-principles"
  ["dmf-agentic-eval"]="ava-dmf-agentic-eval"
  ["dmf-agents-md"]="ava-dmf-agents-md"
  ["dmf-ai-agent-development"]="ava-dmf-ai-agent-development"
  ["dmf-ai-agents-architect"]="ava-dmf-ai-agents-architect"
  ["dmf-autonomous-agent-patterns"]="ava-dmf-autonomous-agent-patterns"
  ["dmf-autonomous-agents"]="ava-dmf-autonomous-agents"
  ["dmf-avanade-brand-guidelines"]="ava-dmf-brand-guidelines"
  ["dmf-data-engineering-data-pipeline"]="ava-dmf-data-pipeline"
  ["dmf-data-quality-frameworks"]="ava-dmf-data-quality"
  ["dmf-framework-migration-legacy-modernize"]="ava-dmf-legacy-modernize"
  ["dmf-multi-agent-brainstorming"]="ava-dmf-multi-agent-brainstorming"
  ["dmf-multi-agent-patterns"]="ava-dmf-multi-agent-patterns"
  ["dmf-observability-monitoring-slo-implement"]="ava-dmf-observability-slo"
  ["dmf-production-code-audit"]="ava-dmf-production-audit"
  ["dmf-sql-optimization-patterns"]="ava-dmf-sql-optimization"
  ["dmf-tdd-orchestrator"]="ava-dmf-tdd-orchestrator"
  ["dmf-agent-orchestration-improve-agent"]="ava-dmf-orchestration-improve"
)

for old in "${!renames[@]}"; do
  new="${renames[$old]}"
  if [ -d "$old" ]; then
    git mv "$old" "$new"
    echo "Renomeado: $old → $new"
  fi
done

cd ../..
git commit -m "chore: padroniza prefixo de skills para ava-dmf-* e remove duplicatas"
```

### 5.4 Atualizar referências internas

Após renomear as skills, atualizar qualquer referência a elas no `copilot-instructions.md` e nos agentes:

```bash
# Encontrar todas as referências às skills antigas
grep -r "dmf-agent-" .github/copilot-instructions.md
grep -r "dmf-agent-" src/

# Substituir conforme o mapeamento da tabela 5.2
# (executar manualmente ou com sed para cada renomeação)
```

---

## 6. Fase 4 — Reestruturação dos Agentes

Esta é a fase de maior impacto. O problema central:

**Situação atual:** 21 arquivos `.chatmode.md` soltos em `.github/agents/` sem organização por módulo ou subpasta individual.

**Padrão alvo:** Cada agente em sua própria subpasta dentro do módulo ao qual pertence em `src/modules/dmf-fabric-agents/`, espelhando exatamente o que o fabric-apps faz com `src/modules/ava-fabric-agents/`.

### 6.1 Mapeamento de agentes por módulo

| Agente (arquivo atual) | Módulo destino | Subpasta do agente |
|---|---|---|
| `discovery-scout.chatmode.md` | `upstream-discovery` | `agents/discovery-scout/` |
| `inventory-scout.chatmode.md` | `upstream-discovery` | `agents/inventory-scout/` |
| `business-analyst.chatmode.md` | `upstream-discovery` | `agents/business-analyst/` |
| `data-strategist.chatmode.md` | `upstream-discovery` | `agents/data-strategist/` |
| `logic-extractor.chatmode.md` | `upstream-discovery` | `agents/logic-extractor/` |
| `data-architect.chatmode.md` | `midstream-design` | `agents/data-architect/` |
| `data-modeler.chatmode.md` | `midstream-design` | `agents/data-modeler/` |
| `data-steward.chatmode.md` | `midstream-design` | `agents/data-steward/` |
| `code-generator.chatmode.md` | `midstream-design` | `agents/code-generator/` |
| `agent-designer.chatmode.md` | `midstream-design` | `agents/agent-designer/` |
| `quality-gate.chatmode.md` | `midstream-quality` | `agents/quality-gate/` |
| `security-compliance.chatmode.md` | `midstream-quality` | `agents/security-compliance/` |
| `downstream-executor.chatmode.md` | `downstream-execution` | `agents/downstream-executor/` |
| `documentation.chatmode.md` | `downstream-execution` | `agents/documentation/` |
| `reconciliation.chatmode.md` | `downstream-execution` | `agents/reconciliation/` |
| `self-healing.chatmode.md` | `downstream-execution` | `agents/self-healing/` |
| `bi-semantic.chatmode.md` | `downstream-execution` | `agents/bi-semantic/` |
| `migration-coordinator.chatmode.md` | `core-coordination` | `agents/migration-coordinator/` |
| `orchestrator.chatmode.md` | `core-coordination` | `agents/orchestrator/` |
| `master-agent.chatmode.md` | `core-coordination` | `agents/master-agent/` |
| `iteration-improvement.chatmode.md` | `core-coordination` | `agents/iteration-improvement/` |

### 6.2 Script de migração dos agentes

```bash
# Criar estrutura base de cada módulo
for module in upstream-discovery midstream-design midstream-quality \
              downstream-execution core-coordination; do
  mkdir -p src/modules/dmf-fabric-agents/$module/agents/
  mkdir -p src/modules/dmf-fabric-agents/$module/workflows/
  mkdir -p src/modules/dmf-fabric-agents/$module/checklists/
  mkdir -p src/modules/dmf-fabric-agents/$module/templates/
  touch src/modules/dmf-fabric-agents/$module/module.yaml
done

# ── upstream-discovery
for agent in discovery-scout inventory-scout business-analyst \
             data-strategist logic-extractor; do
  mkdir -p src/modules/dmf-fabric-agents/upstream-discovery/agents/$agent/
  git mv .github/agents/$agent.chatmode.md \
         src/modules/dmf-fabric-agents/upstream-discovery/agents/$agent/$agent.md
done

# ── midstream-design
for agent in data-architect data-modeler data-steward \
             code-generator agent-designer; do
  mkdir -p src/modules/dmf-fabric-agents/midstream-design/agents/$agent/
  git mv .github/agents/$agent.chatmode.md \
         src/modules/dmf-fabric-agents/midstream-design/agents/$agent/$agent.md
done

# ── midstream-quality
for agent in quality-gate security-compliance; do
  mkdir -p src/modules/dmf-fabric-agents/midstream-quality/agents/$agent/
  git mv .github/agents/$agent.chatmode.md \
         src/modules/dmf-fabric-agents/midstream-quality/agents/$agent/$agent.md
done

# ── downstream-execution
for agent in downstream-executor documentation reconciliation \
             self-healing bi-semantic; do
  mkdir -p src/modules/dmf-fabric-agents/downstream-execution/agents/$agent/
  git mv .github/agents/$agent.chatmode.md \
         src/modules/dmf-fabric-agents/downstream-execution/agents/$agent/$agent.md
done

# ── core-coordination
for agent in migration-coordinator orchestrator master-agent \
             iteration-improvement; do
  mkdir -p src/modules/dmf-fabric-agents/core-coordination/agents/$agent/
  git mv .github/agents/$agent.chatmode.md \
         src/modules/dmf-fabric-agents/core-coordination/agents/$agent/$agent.md
done

# Remover o diretório vazio .github/agents/
git rm -r .github/agents/

git commit -m "feat: reorganiza agentes em subpastas por módulo em src/modules/dmf-fabric-agents/"
```

> **Nota sobre a extensão `.chatmode.md`:** O fabric-apps usa simplesmente `.md` para os
> arquivos de agente dentro de `src/modules/`. A extensão `.chatmode.md` é específica para
> registro no GitHub Copilot como chat mode. Ao mover para `src/modules/`, o arquivo perde
> essa função automática — o registro passa a ser feito pelo `copilot-instructions.md`
> apontando para o caminho do módulo.

---

## 7. Fase 5 — Reestruturação dos Módulos `src/`

### 7.1 Situação atual vs. alvo

**Atual (fabric-data):**
```
src/modules/
├── core-coordination/      ← módulo flat (agents + tasks + templates misturados)
├── downstream-execution/
├── midstream-design/
├── midstream-quality/
└── upstream-discovery/
```

**Alvo (padrão fabric-apps adaptado):**
```
src/modules/
└── dmf-fabric-agents/      ← namespace único da fábrica
    ├── upstream-discovery/
    ├── midstream-design/
    ├── midstream-quality/
    ├── downstream-execution/
    └── core-coordination/
```

### 7.2 Estrutura interna de cada módulo

Cada módulo deve seguir exatamente esta anatomia, conforme o fabric-apps:

```
<módulo>/
├── module.yaml               ← metadados do módulo (nome, versão, agentes registrados)
├── agents/
│   └── <nome-do-agente>/
│       └── <nome-do-agente>.md   ← definição do agente (migrado da fase 4)
├── checklists/
│   └── <agente>-checklist.md
├── data/
│   └── <agente>-core-config.yaml
│       └── <domínio>-best-practices.md
├── tasks/
│   └── <verbo-objeto>.md         ← tarefas individuais que os agentes executam
├── templates/
│   └── <artefato>-tmpl.<ext>
└── workflows/
    └── <nome-do-pipeline>/
        ├── workflow.md
        └── steps/
            ├── step-01-<nome>.md
            ├── step-02-<nome>.md
            └── ...
```

### 7.3 Migrar conteúdo existente dos módulos antigos

O conteúdo que hoje está em `src/modules/<módulo>/` deve ser movido para
`src/modules/dmf-fabric-agents/<módulo>/` mantendo a estrutura interna:

```bash
# Criar o namespace dmf-fabric-agents
mkdir -p src/modules/dmf-fabric-agents/

# Mover cada módulo para dentro do namespace
for module in core-coordination downstream-execution midstream-design \
              midstream-quality upstream-discovery; do
  git mv src/modules/$module/ src/modules/dmf-fabric-agents/$module/
done

git commit -m "feat: encapsula módulos sob namespace dmf-fabric-agents/"
```

### 7.4 Migrar conteúdo das pastas `*-agent/` da raiz

As pastas soltas na raiz (`code-generator-agent/`, `discovery-scout-agent/`, etc.)
contêm conteúdo que já tem equivalente em `src/modules/`. O processo é:

1. Verificar se o conteúdo em `*-agent/.avanade-core/` é diferente do que está em `src/modules/`
2. Mesclar o que for exclusivo
3. Remover as pastas da raiz

```bash
# Exemplo para code-generator-agent
# Verificar diferenças antes de deletar
diff -r code-generator-agent/.avanade-core/tasks/ \
        src/modules/dmf-fabric-agents/midstream-design/tasks/

# Se não houver diferenças relevantes, remover:
git rm -r code-generator-agent/
git rm -r discovery-scout-agent/
git rm -r documentation-agent/
git rm -r downstream-executor-agent/
git rm -r inventory-scout-agent/
git rm -r logic-extractor-agent/
git rm -r migration-coordinator-agent/
git rm -r quality-gate-agent/
git rm -r reconciliation-agent/
git rm -r security-compliance-agent/
git rm -r self-healing-agent/

git commit -m "chore: remove pastas *-agent/ da raiz (conteúdo já em src/modules/)"
```

### 7.5 Migrar `.avanade-core/` da raiz

O `.avanade-core/` na raiz contém `data/`, `policies/`, `tasks/` e `templates/` que são
referências globais. Esse conteúdo pertence a `src/shared/`:

```bash
# Mover data/ para src/shared/data/
cp -r .avanade-core/data/* src/shared/data/
git add src/shared/data/

# Mover policies/ para src/shared/
mkdir -p src/shared/policies/
cp -r .avanade-core/policies/* src/shared/policies/
git add src/shared/policies/

# Mover templates/ para src/shared/templates/
cp -r .avanade-core/templates/* src/shared/templates/
git add src/shared/templates/

# Mover tasks/ — revisar se não há equivalente nos módulos
# Tasks globais (usadas por múltiplos agentes) vão para src/shared/tasks/
mkdir -p src/shared/tasks/
cp -r .avanade-core/tasks/* src/shared/tasks/
git add src/shared/tasks/

# Após confirmar que tudo foi migrado:
git rm -r .avanade-core/

git commit -m "chore: dissolve .avanade-core/ raiz — conteúdo migrado para src/shared/"
```

### 7.6 Migrar `scripts/` e `tests/`

No fabric-apps não há `scripts/` ou `tests/` na raiz. Essas pastas pertencem
dentro do módulo que as utiliza ou em `src/shared/`:

```bash
# Scripts de governança/validação → src/shared/scripts/
mkdir -p src/shared/scripts/
git mv scripts/* src/shared/scripts/

# Tests correspondentes → src/shared/tests/
mkdir -p src/shared/tests/
git mv tests/* src/shared/tests/

git rm -r scripts/ tests/

git commit -m "chore: move scripts/ e tests/ para src/shared/"
```

---

## 8. Fase 6 — Ajustes finais e validação

### 8.1 Criar `module.yaml` nos novos módulos

Cada módulo em `src/modules/dmf-fabric-agents/` precisa de um `module.yaml`.
Usar como modelo o padrão do fabric-apps:

```yaml
# src/modules/dmf-fabric-agents/upstream-discovery/module.yaml
name: upstream-discovery
version: "1.0.0"
description: "Agentes responsáveis pela fase de descoberta e inventário da migração de dados"
agents:
  - discovery-scout
  - inventory-scout
  - business-analyst
  - data-strategist
  - logic-extractor
skills:
  - ava-dmf-data-pipeline
  - ava-dmf-data-quality
  - ava-dmf-agent-orchestrator
```

### 8.2 Atualizar `copilot-instructions.md`

O arquivo `.github/copilot-instructions.md` provavelmente referencia caminhos antigos.
Atualizar todas as referências:

```bash
# Verificar referências desatualizadas
grep -n "\.github/agents/" .github/copilot-instructions.md
grep -n "src/modules/core-coordination" .github/copilot-instructions.md
grep -n "src/modules/upstream-discovery" .github/copilot-instructions.md

# Substituir conforme os novos caminhos
# Exemplos de substituição:
# .github/agents/orchestrator.chatmode.md
#   → src/modules/dmf-fabric-agents/core-coordination/agents/orchestrator/orchestrator.md
#
# src/modules/upstream-discovery/
#   → src/modules/dmf-fabric-agents/upstream-discovery/
```

### 8.3 Adicionar `docs/guia-execucao-fluxo-agentes.md`

O fabric-apps tem este arquivo como referência de uso. Criar o equivalente
para o contexto de migração de dados com a estrutura mínima:

```markdown
# Guia de Execução — Fábrica de Migração de Dados

## Fluxo de Agentes

### Fase 1 — Upstream (Descoberta)
...

### Fase 2 — Midstream (Design e Qualidade)
...

### Fase 3 — Downstream (Execução)
...
```

### 8.4 Validação final da estrutura

```bash
# Verificar se não há mais arquivos .chatmode.md em .github/agents/
ls .github/agents/ 2>/dev/null && echo "PROBLEMA: ainda há arquivos em .github/agents/" \
  || echo "OK: .github/agents/ removido"

# Verificar se não há mais pastas *-agent/ na raiz
ls -d *-agent/ 2>/dev/null && echo "PROBLEMA: ainda há pastas *-agent/ na raiz" \
  || echo "OK: sem pastas *-agent/ na raiz"

# Verificar se namespace dmf-fabric-agents existe
ls src/modules/dmf-fabric-agents/ && echo "OK: namespace dmf-fabric-agents criado"

# Verificar se todos os agentes foram migrados
find src/modules/dmf-fabric-agents/ -name "*.md" -path "*/agents/*" | sort

# Verificar se .avanade-core/ raiz foi removido
ls .avanade-core/ 2>/dev/null && echo "PROBLEMA: .avanade-core/ ainda na raiz" \
  || echo "OK: .avanade-core/ removido da raiz"
```

---

## 9. Estrutura alvo completa

```
imfai-ava-fabric-data-agents/
│
├── .github/
│   ├── copilot-instructions.md
│   └── skills/
│       ├── ava-dmf-agent-evaluation/SKILL.md
│       ├── ava-dmf-agent-governance/SKILL.md
│       ├── ava-dmf-agent-manager/SKILL.md
│       ├── ava-dmf-agent-memory-mcp/SKILL.md
│       ├── ava-dmf-agent-memory-systems/SKILL.md
│       ├── ava-dmf-agent-orchestration/SKILL.md
│       ├── ava-dmf-agent-orchestrator/SKILL.md
│       ├── ava-dmf-agentic-eval/SKILL.md
│       ├── ava-dmf-agentic-principles/SKILL.md
│       ├── ava-dmf-agents-md/SKILL.md
│       ├── ava-dmf-ai-agent-development/SKILL.md
│       ├── ava-dmf-ai-agents-architect/SKILL.md
│       ├── ava-dmf-autonomous-agent-patterns/SKILL.md
│       ├── ava-dmf-autonomous-agents/SKILL.md
│       ├── ava-dmf-brand-guidelines/SKILL.md
│       ├── ava-dmf-data-pipeline/SKILL.md
│       ├── ava-dmf-data-quality/SKILL.md
│       ├── ava-dmf-legacy-modernize/SKILL.md
│       ├── ava-dmf-multi-agent-brainstorming/SKILL.md
│       ├── ava-dmf-multi-agent-optimize/SKILL.md
│       ├── ava-dmf-multi-agent-patterns/SKILL.md
│       ├── ava-dmf-observability-slo/SKILL.md
│       ├── ava-dmf-orchestration-improve/SKILL.md
│       ├── ava-dmf-production-audit/SKILL.md
│       ├── ava-dmf-sql-optimization/SKILL.md
│       └── ava-dmf-tdd-orchestrator/SKILL.md
│
├── docs/
│   ├── agents-catalog.md
│   └── guia-execucao-fluxo-agentes.md
│
├── infra/                           ← escopo exclusivo fabric-data
│   ├── azure-databricks/
│   └── azure-mcp-server/
│
├── project/
│   ├── context/
│   │   ├── agent-task-config.yaml
│   │   └── shared-context.md
│   └── outputs/
│       ├── upstream/inventory/
│       ├── midstream/
│       └── downstream/
│
├── projects/
│   ├── _template/
│   │   └── context/
│   │       ├── agent-task-config.yaml
│   │       ├── project-config.yaml
│   │       └── shared-context.md
│   └── <nome-do-projeto>/
│       ├── context/
│       └── outputs/
│           ├── upstream/
│           ├── midstream/
│           └── downstream/
│
├── src/
│   ├── modules/
│   │   └── dmf-fabric-agents/       ← namespace único da fábrica de dados
│   │       ├── upstream-discovery/
│   │       │   ├── module.yaml
│   │       │   ├── agents/
│   │       │   │   ├── discovery-scout/
│   │       │   │   │   └── discovery-scout.md
│   │       │   │   ├── inventory-scout/
│   │       │   │   │   └── inventory-scout.md
│   │       │   │   ├── business-analyst/
│   │       │   │   │   └── business-analyst.md
│   │       │   │   ├── data-strategist/
│   │       │   │   │   └── data-strategist.md
│   │       │   │   └── logic-extractor/
│   │       │   │       └── logic-extractor.md
│   │       │   ├── checklists/
│   │       │   ├── data/
│   │       │   ├── tasks/
│   │       │   ├── templates/
│   │       │   └── workflows/
│   │       │       └── upstream-pipeline/
│   │       │           ├── workflow.md
│   │       │           └── steps/
│   │       │
│   │       ├── midstream-design/
│   │       │   ├── module.yaml
│   │       │   ├── agents/
│   │       │   │   ├── data-architect/
│   │       │   │   ├── data-modeler/
│   │       │   │   ├── data-steward/
│   │       │   │   ├── code-generator/
│   │       │   │   └── agent-designer/
│   │       │   ├── checklists/
│   │       │   ├── data/
│   │       │   ├── tasks/
│   │       │   ├── templates/
│   │       │   └── workflows/
│   │       │
│   │       ├── midstream-quality/
│   │       │   ├── module.yaml
│   │       │   ├── agents/
│   │       │   │   ├── quality-gate/
│   │       │   │   └── security-compliance/
│   │       │   ├── checklists/
│   │       │   ├── data/
│   │       │   ├── tasks/
│   │       │   ├── templates/
│   │       │   └── workflows/
│   │       │
│   │       ├── downstream-execution/
│   │       │   ├── module.yaml
│   │       │   ├── agents/
│   │       │   │   ├── downstream-executor/
│   │       │   │   ├── documentation/
│   │       │   │   ├── reconciliation/
│   │       │   │   ├── self-healing/
│   │       │   │   └── bi-semantic/
│   │       │   ├── checklists/
│   │       │   ├── data/
│   │       │   ├── tasks/
│   │       │   ├── templates/
│   │       │   └── workflows/
│   │       │
│   │       └── core-coordination/
│   │           ├── module.yaml
│   │           ├── agents/
│   │           │   ├── migration-coordinator/
│   │           │   ├── orchestrator/
│   │           │   ├── master-agent/
│   │           │   └── iteration-improvement/
│   │           ├── checklists/
│   │           ├── data/
│   │           ├── tasks/
│   │           ├── templates/
│   │           └── workflows/
│   │
│   └── shared/
│       ├── checklists/
│       ├── data/
│       │   └── patterns/
│       │       └── data-migration/      ← escopo exclusivo fabric-data
│       │           ├── cost-benchmarks.md
│       │           └── delivery-best-practices.md
│       ├── policies/                    ← migrado de .avanade-core/policies/
│       ├── samples/
│       │   └── wave-config-sample.yaml
│       ├── schemas/
│       │   ├── agent-result.schema.json
│       │   ├── agent-task.schema.json
│       │   └── gate-decision.schema.json
│       ├── scripts/                     ← migrado de scripts/
│       ├── tasks/                       ← migrado de .avanade-core/tasks/
│       ├── templates/
│       │   ├── exec-summary-tmpl.yaml
│       │   ├── gates/
│       │   ├── project-estimation-tmpl.yaml
│       │   ├── risk-register-tmpl.yaml
│       │   └── roadmap-tmpl.yaml
│       └── tests/                       ← migrado de tests/
│
├── .gitignore
├── files
├── module.yaml
└── README.md
```

---

## 10. Checklist de execução

Usar este checklist para acompanhar o progresso, fase a fase.

### Fase 1 — Limpeza
- [ ] `.gitignore` atualizado com `.venv/`, `.pytest_cache/`, `.vscode/`, `__pycache__/`
- [ ] `.venv/`, `.pytest_cache/`, `.vscode/` removidos do índice git
- [ ] `azure-databricks-integration/` movido para `infra/` ou repo separado
- [ ] `azure-mcp-server/` movido para `infra/` ou repo separado
- [ ] `AGENTS.md` movido para `docs/agents-catalog.md`
- [ ] `wave-config-sample.yaml` movido para `src/shared/samples/`
- [ ] `.github/ISSUE_TEMPLATE/` removido
- [ ] `.github/workflows/ci-governance.yml` removido

### Fase 2 — Renomeações simples
- [ ] `Docs/` renomeado para `docs/`
- [ ] `docs/guia-execucao-fluxo-agentes.md` criado
- [ ] `project/context/project-config.yaml` removido
- [ ] `project/outputs/` criado com subpastas `upstream/`, `midstream/`, `downstream/`

### Fase 3 — Skills
- [ ] Skills sem prefixo deletadas (duplicatas)
- [ ] Skills `dmf-*` renomeadas para `ava-dmf-*`
- [ ] Referências atualizadas em `copilot-instructions.md`

### Fase 4 — Agentes
- [ ] `src/modules/dmf-fabric-agents/` criado com subpastas por módulo
- [ ] Subpasta criada para cada agente individualmente
- [ ] Todos os 21 arquivos `.chatmode.md` migrados para subpastas corretas
- [ ] `.github/agents/` removido

### Fase 5 — Módulos `src/`
- [ ] Módulos movidos para dentro de `dmf-fabric-agents/`
- [ ] `module.yaml` criado em cada módulo
- [ ] Pastas `*-agent/` da raiz comparadas e removidas
- [ ] `.avanade-core/` dissolvido — conteúdo em `src/shared/`
- [ ] `scripts/` movido para `src/shared/scripts/`
- [ ] `tests/` movido para `src/shared/tests/`

### Fase 6 — Validação
- [ ] Nenhum arquivo em `.github/agents/`
- [ ] Nenhuma pasta `*-agent/` na raiz
- [ ] Nenhum `.avanade-core/` na raiz
- [ ] `copilot-instructions.md` sem referências a caminhos antigos
- [ ] Todos os agentes localizáveis em `src/modules/dmf-fabric-agents/*/agents/<nome>/<nome>.md`
- [ ] PR aberta para revisão da equipe

---

> **Importante:** A pasta `infra/` (com `azure-databricks/` e `azure-mcp-server/`) é um
> diferencial legítimo do fabric-data e não precisa ter equivalente no fabric-apps.
> A padronização de estrutura não implica eliminar o que é específico de cada fábrica —
> implica organizar esse conteúdo de forma previsível e consistente.
