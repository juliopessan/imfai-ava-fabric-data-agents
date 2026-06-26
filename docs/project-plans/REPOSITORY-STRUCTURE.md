# Repository Structure — Data Migration Factory v3

## 📦 Organização do Repositório

```
imfai-ava-fabric-data-agents/
│
├── 🚀 ENTRADA PRINCIPAL
│   └── projects/
│       ├── Financeiro/                      ← CASE 1: Cloudera → Databricks (ATIVO)
│       │   ├── wave-config.yaml           # Configuração do projeto
│       │   ├── context/                   # Contexto & requisitos
│       │   ├── legacy/                    # Dados de origem (ZIPs)
│       │   ├── outputs/                   # Artefatos finais
│       │   │   ├── upstream/              # Descoberta
│       │   │   ├── midstream/             # Design
│       │   │   ├── downstream/            # Deployment
│       │   │   ├── raw/                   # Artefatos não-HTML
│       │   │   ├── 00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html ⭐
│       │   │   ├── 00_CONSOLIDATED_MIGRATION_REPORT_templated.html
│       │   │   └── 00_CONSOLIDATED_MIGRATION_REPORT.html
│       │   ├── scripts/                   # 🔥 WORKFLOW COMPLETO
│       │   │   ├── 00_MASTER_PIPELINE.py  # Orquestrador principal
│       │   │   ├── run_all_phases.py      # Wrapper upstream
│       │   │   ├── run_midstream_phases.py # Wrapper midstream
│       │   │   ├── run_downstream_phases.py # Wrapper downstream
│       │   │   ├── upstream_phase*.py     # 7 fases descoberta
│       │   │   ├── generate_roi_analysis.py
│       │   │   ├── generate_consolidated_report.py
│       │   │   ├── generate_tabbed_report.py
│       │   │   └── normalize_outputs_to_template.py
│       │   ├── README.md                  # Quick start
│       │   ├── WORKFLOW_AND_ARCHITECTURE.md
│       │   └── README-REPORT-GENERATION.md
│       │
│       └── Reference-Sa�de/                 ← CASE 2: Referência (SUS/saude)
│           ├── wave-config.yaml
│           ├── orchestrator.py
│           ├── outputs/
│           └── [similar structure to Financeiro]
│
├── 📊 TEMPLATES & DASHBOARD
│   └── reports/
│       ├── _templates/
│       │   ├── DASHBOARD-TEMPLATE-MASTER.html  # Avanade branding
│       │   └── [other templates]
│       ├── Financeiro/                     # Outputs públicos (Financeiro)
│       │   ├── 00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
│       │   └── [other HTML dashboards]
│       ├── simple_server.py              # HTTP server local
│       ├── README.md                     # Instruções
│       └── QUICK-START.md
│
├── 🛠️ SETUP & SCRIPTS
│   ├── scripts/
│   │   ├── install-windows-quick.ps1    # Instalação (Windows)
│   │   └── install-windows-quick.cmd
│   └── requirements-dev.txt              # Dependências Python
│
├── 🔧 CONFIGURATION
│   ├── .github/                          # GitHub config
│   ├── .vscode/                          # VS Code settings
│   ├── .venv/                            # Python environment
│   ├── azure-pipelines.yml               # CI/CD (futuro)
│   └── .gitignore
│
└── 📖 DOCS (deprecated — manter para referência)
    └── [docs antigos removidos]
```

---

## ✅ O Que Foi Mantido (Essencial)

| Item | Motivo |
|------|--------|
| `projects/Financeiro/` | Case principal ativo — workflow completo em `scripts/` |
| `projects/Reference-Sa�de/` | Case referência (SUS/saude) — serve como modelo |
| `reports/_templates/` | Template Avanade obrigatório para branding |
| `reports/Financeiro/` | Outputs públicos do case Financeiro |
| `scripts/install-*.ps1/cmd` | Replicabilidade para novos cases |
| `.venv/` | Environment Python necessário |
| `requirements-dev.txt` | Dependências Python |
| `azure-pipelines.yml` | Preparação para CI/CD futuro |

---

## 🗑️ O Que Foi Removido (Não-Essencial)

| Item | Motivo |
|---|---|
| `docs/` | Documentação sobre agentes/orchestrator antigos |
| `src/` | Código antigo de agentes/módulos |
| `infra/` | Infraestrutura não usada (Databricks, MCP server) |
| `graphify-out/` | Análise de código (não usado) |
| `projects/graphify/` | Subprojeto externo (Graphify tool) |
| `reports/screenshots/` | Screenshots antigas |
| `reports/generate-executive-dashboard.py` | Script antigo |
| `reports/simple-server.py` (duplicado) | Versão duplicada (mantive `simple_server.py`) |
| `BACKLOG-48H.md`, `TIMELINE-48H.md` | Histórico antigo |
| `PROJECT-SUMMARY.md` | Histórico de reference |
| `PLAYWRIGHT-*.md` | Integração não usada |
| `Makefile`, `module.yaml`, `list_screenshots.py` | Não usados |

---

## 🚀 Como Usar Para Novos Cases

Quando um novo case chegar (ex: Case 3):

1. **Criar pasta do case em `projects/`**
   ```
   projects/novo-case/
   ├── wave-config.yaml
   ├── legacy/
   ├── context/
   ├── outputs/
   └── scripts/  ← Copiar de projects/Financeiro/scripts
   ```

2. **Usar o master pipeline**
   ```powershell
   cd projects/novo-case/scripts
   .venv\Scripts\python.exe 00_MASTER_PIPELINE.py
   ```

3. **Outputs são automaticamente salvos em:**
   ```
   projects/novo-case/outputs/
   ├── upstream/
   ├── midstream/
   ├── downstream/
   └── *.html  (Avanade-branded)
   ```

---

## 🔄 Workflow Autônomo (Testado ✅)

```
.venv\Scripts\python.exe projects/Financeiro/scripts/00_MASTER_PIPELINE.py
    ↓
Phase B: Upstream Discovery (12.9s)     → 545 files, 27/27 PASS
Phase C: Midstream Design (4.9s)         → 146 entities, Medallion arch
Phase D: Downstream Deployment (5.1s)    → 12.45M rows, 98.7% valid
Phase E: Consolidation (3.8s)            → ROI analysis + reports
Phase F: Normalization (1.3s)            → Avanade templates applied
    ↓
Resultado: 3 HTML dashboards + documentação completa
Total: 28.1 segundos
```

---

## 📊 Dashboards Gerados

**Após executar o master pipeline, os seguintes HTML são gerados:**

1. `00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html` ⭐ **PRINCIPAL**
   - Tabs: Upstream | Midstream | Downstream
   - KPIs: ROI, payback period, entity counts, validation scores
   - Branding: Avanade (purple #5c2d91 + orange #ff6b35)

2. `00_CONSOLIDATED_MIGRATION_REPORT_templated.html`
   - Versão template-only com branding

3. `00_CONSOLIDATED_MIGRATION_REPORT.html`
   - HTML simples sem template

**Todos os 3 são salvos em:**
- `projects/{case}/outputs/` (local)
- `reports/{case}/` (público)

---

## 🎯 Replicabilidade Garantida

✅ Todo novo case segue o mesmo padrão:
- Mesma estrutura de pastas
- Mesmo workflow (00_MASTER_PIPELINE.py)
- Mesmos templates (reports/_templates/)
- Mesmas métricas e KPIs

**Estimativa para próximos cases:**
- Setup: 5 minutos (copiar estrutura)
- Execution: ~30 segundos (automatizado)
- Total: <40 minutos até dashboard pronto

---

## 📝 Documentação Essencial

| Arquivo | Propósito |
|---------|-----------|
| `projects/Financeiro/README.md` | Quick start Financeiro |
| `projects/Financeiro/WORKFLOW_AND_ARCHITECTURE.md` | Explicação completa do workflow |
| `projects/Financeiro/README-REPORT-GENERATION.md` | Instruções de execução |
| `reports/README.md` | Como servir dashboards |
| `REPOSITORY-STRUCTURE.md` | Este arquivo |

---

**Gerado**: 2026-06-08
**Status**: ✅ Repositório pronto para novos cases
