# 📑 Índice do Repositório

Bem-vindo ao repositório da **Data Migration Factory (DMF)** — um orquestrador multi-agente para migração de plataformas de dados com governança em 3 camadas.

---

## 🎯 Comece por Aqui

### 🆕 Agentic Engineering Framework (Novo — 2026-06-16)
1. **Leia primeiro:** [`AGENTIC-ENGINEERING-V1-SUMMARY.md`](../AGENTIC-ENGINEERING-V1-SUMMARY.md) (5 min overview)
2. **Entenda harness:** [`docs/HARNESS-MANIFEST.md`](../docs/HARNESS-MANIFEST.md) (Week 1 approval)
3. **Veja roadmap:** [`docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md`](../docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md) (4 weeks)
4. **Navegue tudo:** [`NAVIGATION-INDEX.md`](../NAVIGATION-INDEX.md) (by role & task)

### Novo no Projeto (DMF)?
1. **Leia primeiro:** [`README.md`](../README.md) (root)
2. **Entenda a estrutura:** [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md) | [`REPOSITORY-QUICK-REFERENCE.md`](../REPOSITORY-QUICK-REFERENCE.md)
3. **Setup local:** [`config/README.md`](./config/README.md)
4. **Comece com um projeto:** [`projects/financeiro/README.md`](./projects/financeiro/README.md) ou [`projects/reference-saude/README.md`](./projects/reference-saude/README.md)
5. **Comece a codificar:** [`src/shared/README.md`](./src/shared/README.md)

### Já Familiarizado?
- **Ferramentas:** [`tools/README.md`](./tools/README.md)
- **Documentação:** [`docs/README.md`](./docs/README.md)
- **Projetos:** [`projects/README.md`](./projects/README.md)
- **Relatórios:** [`reports/README.md`](./reports/README.md)
- **Navegação avançada:** [`NAVIGATION-INDEX.md`](../NAVIGATION-INDEX.md) (by role, by task)

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
├── 📂 projects/                             # Projetos de Migração (Reorganizado!)
│   ├── 📂 bradesco/
│   │   ├── 📂 scripts/                      # ✅ Todos scripts centralizados
│   │   ├── 📂 outputs/                      # ✅ Todos outputs aqui
│   │   ├── 📂 state/                        # Configuração & logs
│   │   ├── 📂 legacy/                       # Dados originais
│   │   ├── README.md
│   │   └── wave-config.yaml
│   │
│   ├── 📂 reference-saude/
│   │   ├── 📂 scripts/                      # ✅ 7 scripts organizados
│   │   │   ├── orchestrator.py
│   │   │   ├── deep_legacy_analyzer.py
│   │   │   ├── generate_kpi_portal.py       # 🌐 Portal generator
│   │   │   ├── update_portal_with_legacy.py
│   │   │   ├── generate_final_report.py
│   │   │   ├── create_executive_dashboard.py
│   │   │   ├── render_screenshots.py
│   │   │   └── README.md                    # 📜 Script reference
│   │   ├── 📂 outputs/                      # ✅ 40+ generated files
│   │   │   ├── KPI_PORTAL_MASTER.html       # 🌐 LIVE PORTAL
│   │   │   ├── DEEP_LEGACY_ANALYSIS.md
│   │   │   ├── DELIVERABLES_INDEX.md
│   │   │   └── ...
│   │   ├── 📂 state/
│   │   ├── 📂 legacy/                       # 27 SQL Server scripts
│   │   ├── README.md                        # 📊 Project overview
│   │   └── wave-config.yaml
│   │
│   ├── 📂 multi-platform-migration/
│   │   ├── 📂 scripts/
│   │   ├── 📂 outputs/
│   │   ├── 📂 state/
│   │   ├── README.md
│   │   └── wave-config.yaml
│   │
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
# Esperado: 189 passed ✓

# Validar estrutura de repositório
python validate_repo_structure.py
# Esperado: 15/15 checks passed ✓
```

### 3. Executar um Projeto (30-50 segundos)

#### Opção A: Bradesco Migration
```bash
python projects/bradesco/scripts/00_MASTER_PIPELINE.py
# Outputs: projects/bradesco/outputs/
```

#### Opção B: Einstein-HIAE KPI Portal
```bash
python projects/einstein-hiae/scripts/generate_kpi_portal.py
# Portal gerado em: projects/einstein-hiae/outputs/KPI_PORTAL_MASTER.html
```

### 4. Visualizar Resultados (30 segundos)
```bash
# Serve os outputs localmente
python -m http.server 8000 --directory projects/einstein-hiae/outputs
# Abra: http://localhost:8000/KPI_PORTAL_MASTER.html
```

---

## 📊 Estrutura de Governança & Agentes (TIER 2)

### 🆕 Agentic Engineering Framework (Novo — 2026-06-16)

A DMF agora implementa **agentic engineering** com base no paper "The New SDLC with Vibe Coding" do Google:

| Componente | Documento | Propósito | Timeline |
|-----------|-----------|----------|----------|
| **Harness Formalization** | [`docs/HARNESS-MANIFEST.md`](../docs/HARNESS-MANIFEST.md) | Formalizar harness como artefato primeira-classe | Week 1 |
| **Skills Versioning** | [`src/shared/schemas/wave-config-extended.yaml`](../src/shared/schemas/wave-config-extended.yaml) | Permitir skills independentes & pinned versions | Week 2 |
| **Observability** | [`docs/OBSERVABILITY-AND-TRACES.md`](../docs/OBSERVABILITY-AND-TRACES.md) | Traces distribuídas, cost attribution, drift detection | Week 3 |
| **Escalation Rules** | [`docs/HUMAN-AGENT-CHECKPOINTS.md`](../docs/HUMAN-AGENT-CHECKPOINTS.md) | 3-tier checkpoint system (auto-approve, human review, critical) | Week 4 |
| **Specs-as-Executable** | [`src/shared/schemas/spec-as-executable.md`](../src/shared/schemas/spec-as-executable.md) | Converter specs estáticas em validators (DataContractValidator) | Week 4 |

**📖 Comece em:** [`AGENTIC-ENGINEERING-V1-SUMMARY.md`](../AGENTIC-ENGINEERING-V1-SUMMARY.md) (5 min)

---

### Multi-Agent Orchestration Architecture

A Data Migration Factory implementa **orquestração de múltiplos agentes** com governança em 3 camadas:

### Agentes (21 Total)
- **upstream-discovery:** 4 agentes
- **midstream-design:** 6 agentes
- **midstream-quality:** 3 agentes
- **downstream-execution:** 5 agentes
- **core-coordination:** 3 agentes

Cada agente valida suas saídas através de **quality gates** com scores >= 0.85

### Governança Estratégica (23 scripts)
```
UPSTREAM (4 phases)  →  MIDSTREAM (3 phases)  →  DOWNSTREAM (1 phase)
Gate 0: Config       →  Gate 1: Architecture   →  Gate 2: Reconciliation
Gate Score >= 0.85 required for promotion
```

---

## 📚 Documentação por Tópico

### Para Entender o Projeto
| Recurso | Localização | Tempo |
|---------|-------------|-------|
| Missão & Visão | [`README.md`](../README.md) | 5 min |
| Estrutura Atual | [`REPOSITORY-ORGANIZATION.md`](./REPOSITORY-ORGANIZATION.md) | 10 min |
| Agentes DMF | [`docs/project-plans/`](./docs/project-plans/) | 15 min |
| Governança TIER 2 | [`src/shared/scripts/README.md`](./src/shared/scripts/README.md) | 20 min |

### Para Começar com um Projeto
| Recurso | Localização | Tempo |
|---------|-------------|-------|
| Bradesco Setup | [`projects/bradesco/README.md`](./projects/bradesco/README.md) | 5 min |
| Einstein-HIAE Portal | [`projects/einstein-hiae/README.md`](./projects/einstein-hiae/README.md) | 5 min |
| Scripts Reference | [`projects/einstein-hiae/scripts/README.md`](./projects/einstein-hiae/scripts/README.md) | 10 min |
| Multi-Platform Wave | [`projects/multi-platform-migration/README.md`](./projects/multi-platform-migration/README.md) | 10 min |

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
