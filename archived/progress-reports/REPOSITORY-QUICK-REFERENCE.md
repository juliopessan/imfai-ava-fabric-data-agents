# 🗺️ Repository Quick Reference Map

**Purpose:** Fast lookup for files, scripts, and resources  
**Updated:** 2026-06-16

---

## 📍 Script Locations

### Einstein-HIAE Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `orchestrator.py` | `projects/einstein-hiae/scripts/` | Master orchestration |
| `deep_legacy_analyzer.py` | `projects/einstein-hiae/scripts/` | Legacy DDL extraction |
| `generate_kpi_portal.py` | `projects/einstein-hiae/scripts/` | Portal generation |
| `generate_final_report.py` | `projects/einstein-hiae/scripts/` | Report generation |
| `create_executive_dashboard.py` | `projects/einstein-hiae/scripts/` | Dashboard creation |
| `render_screenshots.py` | `projects/einstein-hiae/scripts/` | Screenshot automation |
| `update_portal_with_legacy.py` | `projects/einstein-hiae/scripts/` | Portal content merge |

### Bradesco Scripts
- Located in: `projects/bradesco/scripts/`

### Utility Scripts
- Located in: `tools/validation/`, `tools/utilities/`

---

## 📊 Output Locations

### Einstein-HIAE Outputs

| File | Location | Type |
|------|----------|------|
| `KPI_PORTAL_MASTER.html` | `projects/einstein-hiae/outputs/` | Portal (LIVE) |
| `AVANADE_DESIGN_TOKENS.css` | `projects/einstein-hiae/outputs/` | Design system |
| `AVANADE_COMPONENTS.css` | `projects/einstein-hiae/outputs/` | UI components |
| `PORTAL_INTERACTIONS.js` | `projects/einstein-hiae/outputs/` | Interactivity |
| `EINSTEIN_KPI_PORTAL_CONTENT.json` | `projects/einstein-hiae/outputs/` | Portal content |
| `DEEP_LEGACY_ANALYSIS_SUMMARY.txt` | `projects/einstein-hiae/outputs/` | Summary |
| `EXECUTION_SUMMARY.txt` | `projects/einstein-hiae/outputs/` | Execution log |
| `DELIVERABLES_INDEX.md` | `projects/einstein-hiae/outputs/` | File index |

### Phase Outputs
- **Phase 1 (Discovery):** `projects/einstein-hiae/outputs/phase-1/`
- **Phase 2 (Architecture):** `projects/einstein-hiae/outputs/phase-2/`
- **Phase 3 (Deployment):** `projects/einstein-hiae/outputs/phase-3/`

### Bradesco Outputs
- Located in: `projects/bradesco/outputs/`
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
| `projects/` | Case study projects (bradesco, einstein-hiae) |
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

### Run Einstein-HIAE Portal Generation
```bash
cd projects/einstein-hiae/scripts
python generate_kpi_portal.py
```

### Run Einstein-HIAE Deep Legacy Analysis
```bash
cd projects/einstein-hiae/scripts
python deep_legacy_analyzer.py
```

### Access Einstein Portal
```
Browser: http://localhost:8000/KPI_PORTAL_MASTER.html
File: projects/einstein-hiae/outputs/KPI_PORTAL_MASTER.html
```

### Run Bradesco Tests
```bash
cd projects/bradesco/scripts
# [Test commands]
```

### View Project Status
- **Einstein:** `projects/einstein-hiae/README.md`
- **Bradesco:** `projects/bradesco/README.md`

---

## 📈 File Organization Statistics

### Einstein-HIAE
- **Total files:** ~80
- **Scripts:** 7 (in `scripts/`)
- **Outputs:** 40+ (in `outputs/`)
- **Phases:** 3 (in `outputs/phase-{1,2,3}/`)
- **Portal files:** 5 (HTML, CSS×2, JS, JSON)

### Bradesco
- **Total files:** ~60
- **Scripts:** Multiple (in `scripts/`)
- **Outputs:** 10+ (in `outputs/`)
- **State files:** 2 (in `state/`)

---

## ✅ Verification Checklist

- [x] Einstein scripts in `scripts/` folder
- [x] Einstein outputs in `outputs/` folder
- [x] Bradesco docs in `outputs/` folder
- [x] Bradesco state in `state/` folder
- [x] No orphaned .py files in project roots
- [x] No orphaned .md files in project roots (except README)
- [x] Portal files accessible
- [x] Templates copied to `docs/_templates/`

---

**Reference Generated:** 2026-06-16  
**By:** Repository Audit & Reorganization  
**Status:** ✅ COMPLETE
