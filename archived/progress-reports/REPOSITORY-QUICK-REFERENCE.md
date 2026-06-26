# 🗺️ Repository Quick Reference Map

**Purpose:** Fast lookup for files, scripts, and resources  
**Updated:** 2026-06-16

---

## 📍 Script Locations

### Reference-Sa�de Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `orchestrator.py` | `projects/Reference-Sa�de/scripts/` | Master orchestration |
| `deep_legacy_analyzer.py` | `projects/Reference-Sa�de/scripts/` | Legacy DDL extraction |
| `generate_kpi_portal.py` | `projects/Reference-Sa�de/scripts/` | Portal generation |
| `generate_final_report.py` | `projects/Reference-Sa�de/scripts/` | Report generation |
| `create_executive_dashboard.py` | `projects/Reference-Sa�de/scripts/` | Dashboard creation |
| `render_screenshots.py` | `projects/Reference-Sa�de/scripts/` | Screenshot automation |
| `update_portal_with_legacy.py` | `projects/Reference-Sa�de/scripts/` | Portal content merge |

### Financeiro Scripts
- Located in: `projects/Financeiro/scripts/`

### Utility Scripts
- Located in: `tools/validation/`, `tools/utilities/`

---

## 📊 Output Locations

### Reference-Sa�de Outputs

| File | Location | Type |
|------|----------|------|
| `KPI_PORTAL_MASTER.html` | `projects/Reference-Sa�de/outputs/` | Portal (LIVE) |
| `AVANADE_DESIGN_TOKENS.css` | `projects/Reference-Sa�de/outputs/` | Design system |
| `AVANADE_COMPONENTS.css` | `projects/Reference-Sa�de/outputs/` | UI components |
| `PORTAL_INTERACTIONS.js` | `projects/Reference-Sa�de/outputs/` | Interactivity |
| `reference_KPI_PORTAL_CONTENT.json` | `projects/Reference-Sa�de/outputs/` | Portal content |
| `DEEP_LEGACY_ANALYSIS_SUMMARY.txt` | `projects/Reference-Sa�de/outputs/` | Summary |
| `EXECUTION_SUMMARY.txt` | `projects/Reference-Sa�de/outputs/` | Execution log |
| `DELIVERABLES_INDEX.md` | `projects/Reference-Sa�de/outputs/` | File index |

### Phase Outputs
- **Phase 1 (Discovery):** `projects/Reference-Sa�de/outputs/phase-1/`
- **Phase 2 (Architecture):** `projects/Reference-Sa�de/outputs/phase-2/`
- **Phase 3 (Deployment):** `projects/Reference-Sa�de/outputs/phase-3/`

### Financeiro Outputs
- Located in: `projects/Financeiro/outputs/`
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
| `projects/` | Case study projects (Financeiro, Reference-Sa�de) |
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

### Run Reference-Sa�de Portal Generation
```bash
cd projects/Reference-Sa�de/scripts
python generate_kpi_portal.py
```

### Run Reference-Sa�de Deep Legacy Analysis
```bash
cd projects/Reference-Sa�de/scripts
python deep_legacy_analyzer.py
```

### Access reference Portal
```
Browser: http://localhost:8000/KPI_PORTAL_MASTER.html
File: projects/Reference-Sa�de/outputs/KPI_PORTAL_MASTER.html
```

### Run Financeiro Tests
```bash
cd projects/Financeiro/scripts
# [Test commands]
```

### View Project Status
- **reference:** `projects/Reference-Sa�de/README.md`
- **Financeiro:** `projects/Financeiro/README.md`

---

## 📈 File Organization Statistics

### Reference-Sa�de
- **Total files:** ~80
- **Scripts:** 7 (in `scripts/`)
- **Outputs:** 40+ (in `outputs/`)
- **Phases:** 3 (in `outputs/phase-{1,2,3}/`)
- **Portal files:** 5 (HTML, CSS×2, JS, JSON)

### Financeiro
- **Total files:** ~60
- **Scripts:** Multiple (in `scripts/`)
- **Outputs:** 10+ (in `outputs/`)
- **State files:** 2 (in `state/`)

---

## ✅ Verification Checklist

- [x] reference scripts in `scripts/` folder
- [x] reference outputs in `outputs/` folder
- [x] Financeiro docs in `outputs/` folder
- [x] Financeiro state in `state/` folder
- [x] No orphaned .py files in project roots
- [x] No orphaned .md files in project roots (except README)
- [x] Portal files accessible
- [x] Templates copied to `docs/_templates/`

---

**Reference Generated:** 2026-06-16  
**By:** Repository Audit & Reorganization  
**Status:** ✅ COMPLETE
