# Playbook de Onboarding — Novo Projeto

> **Tipo:** Tutorial — do zero ao primeiro wave executável  
> **Público:** Novos membros do time (analistas, engenheiros, coordenadores)  
> **Tempo estimado:** Onboarding completo em ~2 horas de leitura + setup

---

## O Que Você Vai Aprender

Ao final deste guia você saberá:

1. Como funciona o modelo de operação (fases, gates, agentes)
2. Como configurar o ambiente local
3. Como ativar e usar os agentes no VS Code
4. Como executar sua primeira wave simulada
5. Onde encontrar ajuda quando travar

---

## Seção 1 — Entenda o Método Antes de Configurar Qualquer Coisa

### 1.1 — A ideia central

Este projeto é uma **fábrica de migração agentica**: em vez de scripts avulsos e processo manual, todo o lifecycle de uma migração de dados é orquestrado por agentes de IA especializados, validados por gates obrigatórios com critérios mensuráveis.

```

UPSTREAM          MIDSTREAM         DOWNSTREAM
(Discovery)       (Design)          (Execution)
    │                 │                  │
  Gate 1           Gate 2             Gate 3
    │                 │                  │
 Catalogar         Arquitetar         Executar
 Mapear            Modelar            Reconciliar
 Estratégiar       Validar            Documentar

```

**Regra que você precisa internalizar:** nada avança de fase sem score de gate calculado e decisão registrada. Gate não é checklist de honra — é bloqueador técnico.

### 1.2 — Os três papéis que você provavelmente vai exercer

| Papel | O que faz | Agentes mais usados |
| --- | --- | --- |

| **Migration Coordinator** | Orquestra waves, valida gates, decide aprovação | `master-agent`, `migration-coordinator` |
| **Data Engineer / Architect** | Projeta, modela, gera código, valida qualidade | `data-architect`, `data-modeler`, `code-generator`, `quality-gate` |
| **Downstream Executor** | Executa waves, reconcilia, documenta | `downstream-executor`, `reconciliation`, `documentation` |

Em projetos menores uma pessoa pode exercer todos os papéis. Em projetos enterprise cada papel tem um owner.

### 1.3 — Os agentes do projeto

Temos 19 agentes organizados por fase. A regra é sempre começar pelo `master-agent` se você não sabe por onde ir:

| Fase | Agentes Core |
| --- | --- |

| Pre-wave | `master-agent`, `migration-coordinator` |
| UPSTREAM (Gate 1) | `discovery-scout`, `data-strategist`, `business-analyst`, `logic-extractor` |
| MIDSTREAM (Gate 2) | `data-architect`, `data-modeler`, `data-steward`, `quality-gate`, `security-compliance` |
| DOWNSTREAM (Gate 3) | `downstream-executor`, `reconciliation`, `self-healing`, `documentation` |
| Pós-wave | `iteration-improvement` |

Agentes opcionais: `bi-semantic`, `code-generator`, `inventory-scout`, `agent-designer`

### 1.4 — Leitura recomendada antes de colocar a mão na massa

Execute esta leitura na ordem:

1. [README.md](../README.md) — visão geral do projeto (5 min)
2. Este playbook até o fim (você está aqui)
3. [COPILOT-AGENTS-GUIDE.md](COPILOT-AGENTS-GUIDE.md) — referência de comandos (leia as seções das fases em que você vai atuar)
4. [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) — quando for executar sua primeira wave real

Documentos avançados (leia quando necessário):

- [PRD-Agentic-Data-Migration-Factory.md](PRD-Agentic-Data-Migration-Factory.md) — requisitos e critérios de aceite

- [OPERATING-MODEL-CANVAS-v2.md](OPERATING-MODEL-CANVAS-v2.md) — modelo operacional e permissões por agente

- [SKILLS-BLUEPRINT-BY-GATE.md](SKILLS-BLUEPRINT-BY-GATE.md) — skills disponíveis por gate

---

## Seção 2 — Configure o Ambiente Local

### Pré-requisitos

Antes de começar, verifique que você tem instalado:

| Ferramenta | Versão mínima | Como verificar |
| --- | --- | --- |

| Python | 3.13+ | `python --version` |
| Git | qualquer | `git --version` |
| VS Code | qualquer | abrir o app |
| GitHub Copilot | extensão ativa | ícone no VS Code |

### Passo 2.1 — Clone e abra o workspace

```powershell
# Clone o repositório (substitua pela URL real)
git clone <URL-DO-REPOSITÓRIO>

# Entre na pasta do projeto
cd "Data-Migration v3"

# Abra no VS Code
code .

```

> Se o projeto já está clonado, simplesmente abra a pasta no VS Code: `File → Open Folder`.

### Passo 2.2 — Crie e ative o ambiente virtual

```powershell
# Crie o venv
python -m venv .venv

# Ative no Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Ative no Linux/Mac
source .venv/bin/activate

```

Você verá `(.venv)` no início do prompt — isso confirma que o venv está ativo.

> **Importante:** sempre ative o venv antes de rodar qualquer script Python. Se o terminal foi fechado e reaberto, execute o Activate novamente.

### Passo 2.3 — Instale as dependências

```powershell
pip install pytest pyyaml

```

Não há `requirements.txt` no momento — estas duas são as únicas dependências do framework de governança.

### Passo 2.4 — Valide a instalação

```powershell
python -m pytest tests/ -q

```

Resultado esperado:

```

189 passed in X.XXs

```

Se você ver `189 passed`, o ambiente está funcionando corretamente. Qualquer falha indica problema de configuração — veja a Seção 6 (Troubleshooting).

---

## Seção 3 — Ative os Agentes no VS Code

### Passo 3.1 — Confirme que o GitHub Copilot está ativo

1. Abra o VS Code
2. Pressione `Ctrl+Alt+I` para abrir o GitHub Copilot Chat
3. O painel de chat deve aparecer à esquerda ou à direita

Se não aparecer, instale a extensão **GitHub Copilot Chat** pelo Marketplace do VS Code.

### Passo 3.2 — Selecione um agente

1. No painel do Copilot Chat, clique no seletor de modo no canto superior esquerdo:
   ```

   [ Ask ▼ ]  ← clique aqui
   ```

2. Você verá a lista de agentes disponíveis (os `.chatmode.md` da pasta `.github/agents/`)
3. Selecione o agente desejado

### Passo 3.3 — Teste com o master-agent

```

[Selecione: master-agent]
> olá

```

O agente deve se apresentar com seu menu de comandos. Se não aparecer a apresentação, tente:

```

> *help

```

### Passo 3.4 — Explore os comandos disponíveis

Cada agente tem comandos com o prefixo `*`. Para ver todos:

```

> *help

```

Para navegar pelo projeto sem saber qual agente usar:

```

[Selecione: master-agent]
> *route
Contexto: [descreva o que você quer fazer]

```

O `master-agent` vai recomendar o agente correto.

---

## Seção 4 — Entenda a Estrutura do Projeto

```

Data-Migration v3/
├── .github/
│   ├── agents/          ← 19 agentes (arquivos .chatmode.md)
│   └── skills/          ← 26 skills instaladas
├── scripts/             ← 23 módulos Python de governança
├── tests/               ← 189 testes automatizados
├── docs/                ← Documentação do projeto
│   ├── PRD-...          ← Requisitos do produto
│   ├── OPERATING-MODEL  ← Modelo operacional
│   ├── COPILOT-AGENTS-GUIDE ← Referência de comandos
│   ├── SKILLS-BLUEPRINT ← Skills por gate
│   ├── PLAYBOOK-MIGRATION-OPERATIONS.md ← Operação de waves
│   └── PLAYBOOK-ONBOARDING.md ← Este arquivo
├── <nome>-agent/        ← Pasta de cada agente com seus outputs
│   ├── <agent>-outputs/ ← Artefatos gerados pelo agente
│   └── README.md
└── README.md            ← Ponto de entrada do projeto

```

### Scripts de governança (pasta `scripts/`)

Os scripts Python implementam as validações que os agentes usam internamente. Como novo membro, você provavelmente vai interagir com:

| Script | O que faz |
| --- | --- |
| `validate_wave_config.py` | Valida o YAML de configuração de uma wave |
| `gate_score_report.py` | Calcula o GateScore de um gate |
| `validate_gate1_artifacts.py` | Verifica artefatos obrigatórios do Gate 1 |
| `validate_gate2_artifacts.py` | Verifica artefatos obrigatórios do Gate 2 |
| `validate_gate3_artifacts.py` | Verifica artefatos obrigatórios do Gate 3 |
| `kpi_dashboard_report.py` | Calcula e reporta KPIs do projeto |
| `wave_status_tracker.py` | Status consolidado da wave nos 3 gates |
| `governance_policy.py` | Motor de política de tool use por agente |
| `data_contract_validator.py` | Validação declarativa de contratos de dados |

Consulte [scripts/README.md](../scripts/README.md) para a lista completa dos 23 módulos.

---

## Seção 5 — Execute Sua Primeira Wave Simulada

Esta seção guia você em uma simulação de wave para aprender o fluxo sem risco. Use dados fictícios.

### Passo 5.1 — Crie um wave-config de exemplo

```powershell
# Crie uma pasta para a wave de teste
mkdir wave-test-onboarding

```

Crie o arquivo `wave-test-onboarding/wave-config.yaml`:

```yaml
wave_id: WAVE-ONBOARDING
wave_name: "Onboarding Test Wave"
scope:
  entities:
    - Customers
    - Orders

source:
  type: sql_server
  database: NORTHWIND_DEV
target:
  platform: "destino a definir"
discovery_owner: discovery-scout
status: in_progress

```

### Passo 5.2 — Valide o config

```powershell
python scripts/validate_wave_config.py

```

### Passo 5.3 — Simule o Gate 1 com o discovery-scout

```text
[Selecione: discovery-scout]
> *scan-repo
Fonte: SQL Server 2019, banco: NORTHWIND_DEV
Escopo: tabelas Customers e Orders (simulação de onboarding)

> *classify
Classifique por complexidade

```

Observe o formato das saídas — `inventory-report.md` com complexidade Low/Medium/High.

### Passo 5.4 — Simule o problema de negócio

```text
[Selecione: data-strategist]
> *define-problem
Projeto: WAVE-ONBOARDING — migração de teste
Objetivo: aprender o fluxo da factory

```

### Passo 5.5 — Calcule um GateScore simulado

```text
[Selecione: migration-coordinator]
> *gate1-validate
Wave: WAVE-ONBOARDING

```

Se algum artefato obrigatório estiver faltando, o agente vai apontar o que falta. Isso é o comportamento esperado — aprenda o que cada gate exige observando os bloqueadores.

### Passo 5.6 — Leia o Playbook de Operações

Com o fluxo simulado em mente, leia [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) de ponta a ponta. Agora você vai entender cada passo com contexto prático.

---

## Seção 6 — Troubleshooting

### Problema: `189 passed` não aparece

**Causa mais comum:** pyyaml não instalado.

```powershell
pip install pyyaml
python -m pytest tests/ -q

```

### Problema: agentes não aparecem no VS Code

**Verifique:**

1. A extensão GitHub Copilot Chat está instalada e ativa
2. O workspace aberto é a pasta raiz do projeto (onde fica `.github/`)
3. Os arquivos `.chatmode.md` existem em `.github/agents/`

```powershell
# Verifique se os arquivos existem
Get-ChildItem .github\agents\ -Filter "*.chatmode.md" | Measure-Object
# Esperado: 21 arquivos (19 ativos + 1 deprecated + 1 opcional)

```

### Problema: venv não ativa (PowerShell)

```powershell
# Se houver erro de execução de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois tente ativar novamente:
.\.venv\Scripts\Activate.ps1

```

### Problema: não sei qual agente usar

```text
[Selecione: master-agent]
> *route
[descreva o que você quer fazer]

```

O `master-agent` sempre recomenda o agente correto para o contexto.

### Problema: agente não entende meu contexto

- Forneça sempre: nome da wave, entidades em escopo, plataforma fonte e destino

- Use os comandos com `*` em vez de linguagem livre quando disponíveis

- Se o agente se perder, abra um novo chat e selecione o agente novamente

---

## Seção 7 — Referência Rápida de Comandos de Setup

```powershell
# Setup completo de um novo ambiente
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest pyyaml
python -m pytest tests/ -q    # deve retornar 189 passed

# Comandos do dia a dia
python -m pytest tests/ -q                                             # todos os testes
python -m pytest tests/test_gate_score_report.py -v                   # teste específico
python -m scripts.validate_wave_config WAVE-001.yaml                  # validar wave-config
python -m scripts.validate_agent_contracts --root .                   # contratos dos agentes
python -m scripts.validate_gate3_artifacts downstream-executor-agent/downstream-outputs

```

---

## Seção 8 — Próximos Passos

Depois de concluir as seções 1 a 5, você está pronto para:

| Objetivo | O que fazer |
| --- | --- |

| Executar uma wave real | Siga [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) |
| Aprofundar em um agente específico | Leia a seção correspondente em [COPILOT-AGENTS-GUIDE.md](COPILOT-AGENTS-GUIDE.md) |
| Entender permissões e governança | Leia [OPERATING-MODEL-CANVAS-v2.md](OPERATING-MODEL-CANVAS-v2.md) |
| Ver o modelo de qualidade (GateScore) | Leia [PRD-Agentic-Data-Migration-Factory.md](PRD-Agentic-Data-Migration-Factory.md) seção 4 |
| Explorar skills disponíveis | Leia [SKILLS-BLUEPRINT-BY-GATE.md](SKILLS-BLUEPRINT-BY-GATE.md) |

---

## Checklist de Conclusão do Onboarding

- [ ] Li as seções 1 a 5 deste playbook

- [ ] Ambiente Python configurado com venv ativo

- [ ] `pip install pytest pyyaml` executado

- [ ] `189 passed` confirmado no `pytest`

- [ ] GitHub Copilot Chat aberto no VS Code

- [ ] `master-agent` ativado e `*help` respondido

- [ ] Wave simulada criada e Gate 1 tentado

- [ ] [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) lido

- [ ] Sabia qual agente chamar para cada fase
