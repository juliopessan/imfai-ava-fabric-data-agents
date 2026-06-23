# 🗺️ Repository Quick Reference Map

**Purpose:** Fast lookup for files, scripts, and resources  
**Updated:** 2026-06-16

---

## 📍 Script Locations

### ClienteSaude Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `orchestrator.py` | `projects/ClienteSaude/scripts/` | Master orchestration |
| `deep_legacy_analyzer.py` | `projects/ClienteSaude/scripts/` | Legacy DDL extraction |
| `generate_kpi_portal.py` | `projects/ClienteSaude/scripts/` | Portal generation |
| `generate_final_report.py` | `projects/ClienteSaude/scripts/` | Report generation |
| `create_executive_dashboard.py` | `projects/ClienteSaude/scripts/` | Dashboard creation |
| `render_screenshots.py` | `projects/ClienteSaude/scripts/` | Screenshot automation |
| `update_portal_with_legacy.py` | `projects/ClienteSaude/scripts/` | Portal content merge |

### ClienteBanco Scripts
- Located in: `projects/clientebanco/scripts/`

### Utility Scripts
- Located in: `tools/validation/`, `tools/utilities/`

---

## 📊 Output Locations

### ClienteSaude Outputs

| File | Location | Type |
|------|----------|------|
| `KPI_PORTAL_MASTER.html` | `projects/ClienteSaude/outputs/` | Portal (LIVE) |
| `CONSULTORIA_DESIGN_TOKENS.css` | `projects/ClienteSaude/outputs/` | Design system |
| `CONSULTORIA_COMPONENTS.css` | `projects/ClienteSaude/outputs/` | UI components |
| `PORTAL_INTERACTIONS.js` | `projects/ClienteSaude/outputs/` | Interactivity |
| `CLIENTESAUDE_KPI_PORTAL_CONTENT.json` | `projects/ClienteSaude/outputs/` | Portal content |
| `DEEP_LEGACY_ANALYSIS_SUMMARY.txt` | `projects/ClienteSaude/outputs/` | Summary |
| `EXECUTION_SUMMARY.txt` | `projects/ClienteSaude/outputs/` | Execution log |
| `DELIVERABLES_INDEX.md` | `projects/ClienteSaude/outputs/` | File index |

### Phase Outputs
- **Phase 1 (Discovery):** `projects/ClienteSaude/outputs/phase-1/`
- **Phase 2 (Architecture):** `projects/ClienteSaude/outputs/phase-2/`
- **Phase 3 (Deployment):** `projects/ClienteSaude/outputs/phase-3/`

### ClienteBanco Outputs
- Located in: `projects/clientebanco/outputs/`
- Includes: Test reports, execution guides, documentation

---

## 📁 Project Structure Template

```
projects/{project}/
│
├── README.md                    # Project overview
├── wave-config.yaml            # Configuration
│
├── 📂 scripts/                  # Analysis & generation scripts
│   ├── orchestrator.py
│   ├── *.py
│   └── README.md
│
├── 📂 outputs/                  # Generated artifacts
│   ├── phase-1/                 # Discovery outputs
│   ├── phase-2/                 # Architecture outputs
│   ├── phase-3/                 # Deployment outputs
│   ├── dashboards/              # HTML/CSS/JS
│   ├── artifacts/               # JSON configs
│   ├── reports/                 # Analysis reports
│   ├── *.html, *.css, *.js      # Portal files
│   └── SUMMARY_*.txt
│
├── 📂 state/                    # Admin & execution state
│   ├── EXECUTION_CONFIG.json
│   ├── LAST_EXECUTION.log
│   └── [status files]
│
├── 📂 legacy/                   # Original source data
│   ├── dw-scripts-extracted/
│   ├── *.sql
│   └── [legacy artifacts]
│
├── 📂 context/                  # Analysis context
│   ├── *.md
│   └── [context docs]
│
└── 📂 docs/                     # Project documentation
    ├── *.md
    └── [internal docs]
```

---

## 🔗 Key Directories

| Path | Purpose |
|------|---------|
| `projects/` | Case study projects (clientebanco, ClienteSaude) |
| `projects/*/scripts/` | Executable Python scripts |
| `projects/*/outputs/` | Generated artifacts & reports |
| `projects/*/state/` | Execution state & config |
| `projects/*/legacy/` | Original source data |
| `docs/` | Main documentation |
| `docs/reports/` | Analysis reports |
| `docs/project-plans/` | Planning documents |
| `docs/_templates/` | Report/dashboard templates |
| `tools/` | Utility scripts & validation |
| `src/` | Framework code |
| `config/` | Global configuration |
| `reports/` | [DEPRECATED - being consolidated] |

---

## 🎯 Common Tasks

### Run ClienteSaude Portal Generation
```bash
cd projects/ClienteSaude/scripts
python generate_kpi_portal.py
```

### Run ClienteSaude Deep Legacy Analysis
```bash
cd projects/ClienteSaude/scripts
python deep_legacy_analyzer.py
```

### Access ClienteSaude Portal
```
Browser: http://localhost:8000/KPI_PORTAL_MASTER.html
File: projects/ClienteSaude/outputs/KPI_PORTAL_MASTER.html
```

### Run ClienteBanco Tests
```bash
cd projects/clientebanco/scripts
# [Test commands]
```

### View Project Status
- **ClienteSaude:** `projects/ClienteSaude/README.md`
- **ClienteBanco:** `projects/clientebanco/README.md`

---

## 📈 File Organization Statistics

### ClienteSaude
- **Total files:** ~80
- **Scripts:** 7 (in `scripts/`)
- **Outputs:** 40+ (in `outputs/`)
- **Phases:** 3 (in `outputs/phase-{1,2,3}/`)
- **Portal files:** 5 (HTML, CSS×2, JS, JSON)

### ClienteBanco
- **Total files:** ~60
- **Scripts:** Multiple (in `scripts/`)
- **Outputs:** 10+ (in `outputs/`)
- **State files:** 2 (in `state/`)

---

## ✅ Verification Checklist

- [x] ClienteSaude scripts in `scripts/` folder
- [x] ClienteSaude outputs in `outputs/` folder
- [x] ClienteBanco docs in `outputs/` folder
- [x] ClienteBanco state in `state/` folder
- [x] No orphaned .py files in project roots
- [x] No orphaned .md files in project roots (except README)
- [x] Portal files accessible
- [x] Templates copied to `docs/_templates/`

---

**Reference Generated:** 2026-06-16  
**By:** Repository Audit & Reorganization  
**Status:** ✅ COMPLETE
