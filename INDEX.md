# 📑 Índice do Repositório

Bem-vindo ao repositório da **Data Migration Factory (DMF)** — um orquestrador multi-agente para migração de plataformas de dados com governança em 3 camadas.

---

## 🎯 Comece por Aqui

### Novo no Projeto?
1. **Leia primeiro:** [`README.md`](../README.md) (root)
2. **Entenda a estrutura:** [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md)
3. **Setup local:** [`config/README.md`](./config/README.md)
4. **Comece a codificar:** [`src/shared/README.md`](./src/shared/README.md)

### Já Familiarizado?
- **Ferramentas:** [`tools/README.md`](./tools/README.md)
- **Documentação:** [`docs/README.md`](./docs/README.md)
- **Projetos:** [`projects/README.md`](./projects/README.md)
- **Relatórios:** [`reports/README.md`](./reports/README.md)

---

## 📂 Estrutura de Pastas

```
imfai-ava-fabric-data-agents/
│
├── 📂 config/                               # Configurações
│   ├── requirements-dev.txt
│   ├── azure-pipelines.yml
│   └── README.md
│
├── 📂 docs/                                 # Documentação Centralizada
│   ├── 📂 reports/                          # Relatórios de Execução
│   ├── 📂 project-plans/                    # Planos & Estratégia
│   └── README.md
│
├── 📂 tools/                                # Ferramentas de Desenvolvimento
│   ├── 📂 validation/                       # Scripts de Validação
│   ├── 📂 utilities/                        # Utilitários Auxiliares
│   ├── reorganize-repository.ps1
│   └── README.md
│
├── 📂 projects/                             # Projetos de Migração
│   ├── 📂 bradesco/
│   ├── 📂 einstein-hiae/
│   └── README.md
│
├── 📂 reports/                              # Relatórios Dinâmicos
│   ├── 📂 _templates/
│   ├── 📂 bradesco/
│   └── README.md
│
├── 📂 scripts/                              # Scripts Legados
│   ├── install-windows-quick.cmd
│   ├── install-windows-quick.ps1
│   └── README.md
│
├── 📂 src/                                  # Código-Fonte Principal
│   └── 📂 shared/
│       ├── 📂 scripts/                      # 17 Módulos de Governança
│       ├── 📂 tests/                        # 315 Testes Unitários
│       └── README.md
│
├── 📂 .github/                              # GitHub Actions & Config
│   ├── 📂 agents/                           # Definições de Agentes
│   ├── 📂 skills/                           # Skills de Domínio
│   ├── 📂 instructions/                     # Instruções de Orquestração
│   └── 📂 workflows/
│
├── 📄 REPOSITORY-ORGANIZATION.md             # Guia de Organização (novo!)
├── 📄 INDEX.md                               # Este arquivo
├── 📄 README.md
├── 📄 azure-pipelines.yml
└── ...
```

---

## 🚀 Quick Start

### 1. Setup Inicial (5 min)
```bash
# Clone e navegue
git clone <repo-url>
cd imfai-ava-fabric-data-agents

# Ativar venv e instalar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r config/requirements-dev.txt
```

### 2. Verificar Setup (1 min)
```bash
# Executar testes
python -m pytest src/shared/tests/ -q
# Esperado: 315 passed ✓
```

### 3. Reorganizar Repositório (2 min)
```bash
# Opcional: Mover arquivos soltos para estrutura organizada
.\tools\reorganize-repository.ps1 -DryRun  # Visualizar mudanças
.\tools\reorganize-repository.ps1          # Executar
```

### 4. Explorar Projeto
```bash
# Entender a governança
cat src/shared/scripts/README.md

# Listar ferramentas disponíveis
ls tools/validation/

# Ver relatórios
ls docs/reports/
```

---

## 📊 Estrutura de Governança (TIER 2)

A Data Migration Factory implementa **3 camadas de governança**:

### TIER 1: Validadores Base (Raiz)
- ✅ 6 validadores estruturais
- ✅ Validação de configurações
- ✅ Checagem de integridade

### TIER 2: Governança Estratégica (17 scripts)
```
Phase 1 (6 scripts)  →  Phase 2 (4 scripts)  →  Phase 3 (7 scripts)
93 tests ✓           →  64 tests ✓           →  158 tests ✓
                     
                     TOTAL: 315 testes (100% passing)
```

**Phase 1:** Wave tracking, quality, policy, data contracts  
**Phase 2:** KPI dashboards, artifact mgmt, risk aggregation  
**Phase 3:** Reconciliation, cost, audit, classification, dependencies

### TIER 3: Execução (Planejado)
- Orchestração de execução
- Recuperação de erros
- Monitoramento de performance
- State machine

---

## 📚 Documentação por Tópico

### Para Entender o Projeto
| Recurso | Localização | Tempo |
|---------|-------------|-------|
| Missão & Visão | [`README.md`](../README.md) | 5 min |
| Estrutura Atual | [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md) | 10 min |
| Agentes DMF | [`docs/project-plans/`](./docs/project-plans/) | 15 min |
| Governança TIER 2 | [`src/shared/scripts/README.md`](./src/shared/scripts/README.md) | 20 min |

### Para Começar a Codificar
| Recurso | Localização | Tempo |
|---------|-------------|-------|
| Setup Local | [`config/README.md`](./config/README.md) | 5 min |
| Estructura de Código | [`src/shared/README.md`](./src/shared/README.md) | 10 min |
| Executar Testes | [`src/shared/tests/`](./src/shared/tests/) | 1 min |

### Para Usar Ferramentas
| Recurso | Localização | Tempo |
|---------|-------------|-------|
| Ferramentas Disponíveis | [`tools/README.md`](./tools/README.md) | 5 min |
| Scripts de Validação | [`tools/validation/README.md`](./tools/validation/README.md) | 10 min |
| Reorganizar Repo | [`tools/reorganize-repository.ps1`](./tools/reorganize-repository.ps1) | 2 min |

### Para Ver Relatórios
| Recurso | Localização | Conteúdo |
|---------|-------------|---------|
| Execução TIER 1 | [`docs/reports/TIER1-*`](./docs/reports/) | Conclusão, validação |
| Implementação TIER 2 | [`docs/reports/TIER2-*`](./docs/reports/) | Fases 1-2-3 |
| Integração | [`docs/reports/FINAL-INTEGRATION-*`](./docs/reports/) | Status final |

---

## 🛠️ Tarefas Comuns

### Mover Arquivos Soltos
```bash
# Ver o que será movido (dry-run)
.\tools\reorganize-repository.ps1 -DryRun

# Executar (com git mv)
.\tools\reorganize-repository.ps1

# Commit
git commit -m 'refactor: organize repository structure'
```

### Executar Testes
```bash
# Todos os testes (315)
python -m pytest src/shared/tests/ -q

# Testes específicos (ex: Phase 3)
python -m pytest src/shared/tests/test_reconciliation_harness.py -v

# Com cobertura
python -m pytest src/shared/tests/ --cov=src/shared/scripts
```

### Verificar Integridade
```bash
# Validação rápida
python tools/validation/WORKFLOW-INTEGRATION-CHECK.py

# Validação completa (v2)
python tools/validation/WORKFLOW-INTEGRATION-CHECK-v2.py

# Validação específica (Bradesco)
python tools/validation/run_bradesco_tier1_validation.py
```

### Explorar Governança
```bash
# Ver scripts disponíveis
ls src/shared/scripts/

# Ver um script específico
cat src/shared/scripts/reconciliation_harness.py

# Ver testes
ls src/shared/tests/test_*.py
```

---

## 📈 Próximos Passos

### ✅ Completo
- TIER 1: Validadores estruturais (6 scripts)
- TIER 2: Governança de Migração (17 scripts, 315 testes)
- Repositório: Organização de artefatos (docs, tools, config)

### ⏳ Em Progresso
- TIER 3: Camada de Execução (orchestração, recuperação, monitoramento)
- Documentação: READMEs em cada pasta

### 📋 Planejado
- Integração com Microsoft Foundry
- Machine Learning para previsão de risco
- Dashboard de telemetria em tempo real
- Exportação de métricas para Azure Monitor

---

## 🆘 Precisa de Ajuda?

### Troubleshooting Comum

| Problema | Solução |
|----------|---------|
| "ModuleNotFoundError" | `pip install -r config/requirements-dev.txt` |
| "pytest not found" | `.\.venv\Scripts\Activate.ps1` + reinstalar deps |
| Permissão negada | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` |
| Arquivo não encontrado | Verificar se já foi movido (ver [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md)) |

### Referências Rápidas

- **Config:** [`config/README.md`](./config/README.md)
- **Ferramentas:** [`tools/README.md`](./tools/README.md)
- **Documentação:** [`docs/README.md`](./docs/README.md)
- **Governança:** [`src/shared/scripts/README.md`](./src/shared/scripts/README.md)
- **Projetos:** [`projects/README.md`](./projects/README.md)

---

## 📞 Contato & Contribuição

Para questões ou contribuições:
1. Abra uma issue em GitHub
2. Consulte [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md)
3. Siga as convenções do projeto (ver `.github/instructions/`)

---

## 📋 Metadados

| Campo | Valor |
|-------|-------|
| **Versão** | 2.0 (com organização de artefatos) |
| **Última Atualização** | 2026-06-09 |
| **Status** | ✅ Produção-Ready (TIER 1-2) |
| **Testes** | 315 passing (100%) |
| **Documentação** | Completa (TIER 1-2) |
| **Responsável** | GitHub Copilot + Avanade DMF Team |

---

**Boa sorte com a Data Migration Factory! 🚀**

Para começar agora: [`config/README.md`](./config/README.md)
