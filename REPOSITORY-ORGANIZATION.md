# 📁 Estrutura de Organização do Repositório

> Reorganização de artefatos soltos em uma estrutura modular e profissional.

---

## Árvore de Diretórios (Nova Estrutura)

```
imfai-ava-fabric-data-agents/
│
├── 📂 docs/                                    # Documentação e Relatórios
│   ├── 📂 reports/
│   │   ├── TIER1-COMPLETION-REPORT.md
│   │   ├── TIER1-FINAL-SUMMARY.md
│   │   ├── TIER2-IMPLEMENTATION-SUMMARY.md
│   │   ├── TIER2-PHASE2-SUMMARY.md
│   │   ├── FINAL-INTEGRATION-REPORT.md
│   │   ├── CLEANUP-REPORT.md
│   │   ├── EXEC-SUMMARY.txt
│   │   ├── INTEGRATION-COMPLETE.md
│   │   ├── WORKFLOW-INTEGRATION-STATUS.md
│   │   ├── WORKFLOW-INTEGRATION-REPORT.json
│   │   └── WORKFLOW-INTEGRATION-FINAL-STATUS.txt
│   │
│   ├── 📂 project-plans/
│   │   ├── PHASE-5-COMPLETION-SUMMARY.md
│   │   ├── PROJECT-COMPLETION-SUMMARY.md
│   │   ├── REPOSITORY-STRUCTURE.md
│   │   ├── INTEGRATION-CHECKLIST.md
│   │   ├── BRADESCO-TIER1-EXECUTION-PLAN.md
│   │   ├── BRADESCO-TIER1-VALIDATION-REPORT.md
│   │   └── GAP-ANALYSIS-REPORT.md
│   │
│   └── 📄 README.md                           # Índice de documentação
│
├── 📂 tools/                                   # Scripts de Utilidade
│   ├── 📂 validation/
│   │   ├── WORKFLOW-INTEGRATION-CHECK.py
│   │   ├── WORKFLOW-INTEGRATION-CHECK-v2.py
│   │   ├── run_bradesco_tier1_validation.py
│   │   └── README.md
│   │
│   ├── 📂 utilities/
│   │   ├── test_telemetry_system.py
│   │   └── README.md
│   │
│   └── 📄 README.md                           # Índice de ferramentas
│
├── 📂 config/                                  # Configurações
│   ├── requirements-dev.txt
│   ├── azure-pipelines.yml
│   └── README.md
│
├── 📂 projects/                                # Projetos de Migração
│   ├── 📂 bradesco/
│   ├── 📂 einstein-hiae/
│   └── README.md
│
├── 📂 reports/                                 # Relatórios de Execução
│   ├── 📂 _templates/
│   ├── 📂 bradesco/
│   ├── INDEX.md
│   ├── QUICK-START.md
│   └── README.md
│
├── 📂 scripts/                                 # Scripts Legados
│   ├── install-windows-quick.cmd
│   ├── install-windows-quick.ps1
│   └── README.md
│
├── 📂 src/                                     # Código-Fonte Principal
│   └── 📂 shared/
│       ├── 📂 scripts/                         # Módulos de Governança TIER 2
│       ├── 📂 tests/
│       └── README.md
│
├── 📂 .github/                                 # GitHub Actions & Configurações
│   ├── 📂 agents/
│   ├── 📂 skills/
│   ├── 📂 instructions/
│   └── workflows/
│
├── 📂 .venv/                                   # Python Virtual Environment
│
├── 📂 .vscode/                                 # Configurações VS Code
│
├── 📄 REPOSITORY-ORGANIZATION.md               # Este arquivo
│
├── 📄 INDEX.md                                 # Índice Principal
│
├── 📄 .gitignore
│
├── 📄 .git/
│
└── 📄 azure-pipelines.yml                      # (Será movido para /config)
```

---

## Mapeamento de Arquivos: Antes → Depois

### Relatórios (→ `/docs/reports/`)
| Arquivo Atual | Novo Local |
|---|---|
| `TIER1-COMPLETION-REPORT.md` | `docs/reports/TIER1-COMPLETION-REPORT.md` |
| `TIER1-FINAL-SUMMARY.md` | `docs/reports/TIER1-FINAL-SUMMARY.md` |
| `TIER2-IMPLEMENTATION-SUMMARY.md` | `docs/reports/TIER2-IMPLEMENTATION-SUMMARY.md` |
| `TIER2-PHASE2-SUMMARY.md` | `docs/reports/TIER2-PHASE2-SUMMARY.md` |
| `FINAL-INTEGRATION-REPORT.md` | `docs/reports/FINAL-INTEGRATION-REPORT.md` |
| `CLEANUP-REPORT.md` | `docs/reports/CLEANUP-REPORT.md` |
| `EXEC-SUMMARY.txt` | `docs/reports/EXEC-SUMMARY.txt` |
| `INTEGRATION-COMPLETE.md` | `docs/reports/INTEGRATION-COMPLETE.md` |
| `WORKFLOW-INTEGRATION-STATUS.md` | `docs/reports/WORKFLOW-INTEGRATION-STATUS.md` |
| `WORKFLOW-INTEGRATION-REPORT.json` | `docs/reports/WORKFLOW-INTEGRATION-REPORT.json` |
| `WORKFLOW-INTEGRATION-FINAL-STATUS.txt` | `docs/reports/WORKFLOW-INTEGRATION-FINAL-STATUS.txt` |

### Planos & Checklists (→ `/docs/project-plans/`)
| Arquivo Atual | Novo Local |
|---|---|
| `PHASE-5-COMPLETION-SUMMARY.md` | `docs/project-plans/PHASE-5-COMPLETION-SUMMARY.md` |
| `PROJECT-COMPLETION-SUMMARY.md` | `docs/project-plans/PROJECT-COMPLETION-SUMMARY.md` |
| `REPOSITORY-STRUCTURE.md` | `docs/project-plans/REPOSITORY-STRUCTURE.md` |
| `INTEGRATION-CHECKLIST.md` | `docs/project-plans/INTEGRATION-CHECKLIST.md` |
| `BRADESCO-TIER1-EXECUTION-PLAN.md` | `docs/project-plans/BRADESCO-TIER1-EXECUTION-PLAN.md` |
| `BRADESCO-TIER1-VALIDATION-REPORT.md` | `docs/project-plans/BRADESCO-TIER1-VALIDATION-REPORT.md` |
| `GAP-ANALYSIS-REPORT.md` | `docs/project-plans/GAP-ANALYSIS-REPORT.md` |

### Scripts de Validação (→ `/tools/validation/`)
| Arquivo Atual | Novo Local |
|---|---|
| `WORKFLOW-INTEGRATION-CHECK.py` | `tools/validation/WORKFLOW-INTEGRATION-CHECK.py` |
| `WORKFLOW-INTEGRATION-CHECK-v2.py` | `tools/validation/WORKFLOW-INTEGRATION-CHECK-v2.py` |
| `run_bradesco_tier1_validation.py` | `tools/validation/run_bradesco_tier1_validation.py` |

### Scripts de Utilidade (→ `/tools/utilities/`)
| Arquivo Atual | Novo Local |
|---|---|
| `test_telemetry_system.py` | `tools/utilities/test_telemetry_system.py` |

### Configuração (→ `/config/`)
| Arquivo Atual | Novo Local |
|---|---|
| `requirements-dev.txt` | `config/requirements-dev.txt` |
| `azure-pipelines.yml` | `config/azure-pipelines.yml` |

---

## Instruções de Reorganização

### Opção 1: Manual (via PowerShell)

```powershell
# Navegar para o repositório
cd c:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents

# 1. Mover relatórios
mv TIER1-COMPLETION-REPORT.md docs/reports/
mv TIER1-FINAL-SUMMARY.md docs/reports/
mv TIER2-IMPLEMENTATION-SUMMARY.md docs/reports/
mv TIER2-PHASE2-SUMMARY.md docs/reports/
mv FINAL-INTEGRATION-REPORT.md docs/reports/
mv CLEANUP-REPORT.md docs/reports/
mv EXEC-SUMMARY.txt docs/reports/
mv INTEGRATION-COMPLETE.md docs/reports/
mv WORKFLOW-INTEGRATION-STATUS.md docs/reports/
mv WORKFLOW-INTEGRATION-REPORT.json docs/reports/
mv WORKFLOW-INTEGRATION-FINAL-STATUS.txt docs/reports/

# 2. Mover planos e checklists
mv PHASE-5-COMPLETION-SUMMARY.md docs/project-plans/
mv PROJECT-COMPLETION-SUMMARY.md docs/project-plans/
mv REPOSITORY-STRUCTURE.md docs/project-plans/
mv INTEGRATION-CHECKLIST.md docs/project-plans/
mv BRADESCO-TIER1-EXECUTION-PLAN.md docs/project-plans/
mv BRADESCO-TIER1-VALIDATION-REPORT.md docs/project-plans/
mv GAP-ANALYSIS-REPORT.md docs/project-plans/

# 3. Mover scripts de validação
mv WORKFLOW-INTEGRATION-CHECK.py tools/validation/
mv WORKFLOW-INTEGRATION-CHECK-v2.py tools/validation/
mv run_bradesco_tier1_validation.py tools/validation/

# 4. Mover scripts de utilidade
mv test_telemetry_system.py tools/utilities/

# 5. Mover configurações
mv requirements-dev.txt config/
mv azure-pipelines.yml config/
```

### Opção 2: Script Python Automatizado

```python
# reorganize_repository.py
import os
import shutil
from pathlib import Path

def move_files(source_root):
    moves = [
        # (source, destination_folder)
        ('TIER1-COMPLETION-REPORT.md', 'docs/reports'),
        ('TIER1-FINAL-SUMMARY.md', 'docs/reports'),
        # ... adicionar mais mappings
    ]
    
    for source, dest_folder in moves:
        src_path = Path(source_root) / source
        dst_dir = Path(source_root) / dest_folder
        dst_dir.mkdir(parents=True, exist_ok=True)
        
        if src_path.exists():
            shutil.move(str(src_path), str(dst_dir / source))
            print(f"✓ {source} → {dest_folder}/")

if __name__ == '__main__':
    move_files('.')
```

---

## Benefícios da Nova Estrutura

### ✅ Organização Lógica
- **Relatórios** agrupados em um só lugar (`/docs/reports/`)
- **Ferramentas** separadas em validação vs utilidades
- **Configurações** centralizadas
- **Código-fonte** mantido em `/src/` separado de artefatos

### ✅ Navegabilidade Melhorada
- Menos poluição na raiz do repositório
- Estrutura previsível para novos membros do time
- READMEs em cada pasta explicando conteúdo

### ✅ Manutenção Facilitada
- Fácil localizar documentação por tipo
- Scripts de teste isolados de scripts de utilidade
- Configurações centralizadas e versionáveis

### ✅ Conformidade Profissional
- Padrão Avanade/Enterprise
- Estrutura escalável para novos projetos
- Git ignores mais eficientes

---

## Próximos Passos

1. ✅ **Criar estrutura de pastas** (CONCLUÍDO)
2. ⏳ **Mover arquivos** para novos locais (Opção 1 ou 2)
3. ⏳ **Criar READMEs** em cada pasta (`docs/README.md`, `tools/README.md`, etc.)
4. ⏳ **Atualizar referências** em `.github/workflows/` se houver
5. ⏳ **Atualizar `.gitignore`** se necessário
6. ⏳ **Commit & Push** para versionar a nova estrutura

---

## Exemplo de Conteúdo para READMEs

### `/docs/README.md`
```markdown
# 📚 Documentação

Relatórios, planos e documentação de projeto.

- **`reports/`** — Relatórios de execução (TIER 1-2, integração, limpeza)
- **`project-plans/`** — Planos, checklists e análises
```

### `/tools/README.md`
```markdown
# 🔧 Ferramentas

Scripts de validação, testes e utilidades.

- **`validation/`** — Scripts de verificação de integração e validação
- **`utilities/`** — Scripts auxiliares (telemetria, etc.)
```

---

## Estrutura Pós-Reorganização (Raiz Limpa)

```
imfai-ava-fabric-data-agents/
├── .github/
├── .gitignore
├── .venv/
├── .vscode/
├── config/                              # ← Novo
├── docs/                                # ← Novo
├── projects/
├── reports/
├── scripts/
├── src/
├── tools/                               # ← Novo
├── INDEX.md
└── REPOSITORY-ORGANIZATION.md           # Este arquivo
```

**Raiz:**  apenas 9 itens (antes: ~30 arquivos soltos) ✅

---

## Perguntas Frequentes

**P: E os arquivos que estão movendo — e o Git?**  
R: Use `git mv` em vez de apenas `mv` para preservar o histórico:
```bash
git mv TIER1-COMPLETION-REPORT.md docs/reports/
```

**P: Preciso atualizar importações?**  
R: Se houver imports em Python referenciando esses arquivos, sim. Busque por esses nomes em `src/` e `.github/`.

**P: Quando fazer essa reorganização?**  
R: Idealmente em um commit separado com mensagem clara: `refactor: organize repository structure`

**P: Posso fazer parcialmente?**  
R: Sim! Comece com `/docs/` e `/tools/`, depois `/config` em um commit separado.

---

**Data de Criação:** 2026-06-09  
**Responsável:** GitHub Copilot  
**Status:** 📋 Pronto para Execução
