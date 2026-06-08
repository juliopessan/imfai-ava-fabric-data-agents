# Bradesco Data Platform Migration — Complete Project

> **Autonomous end-to-end migration orchestration from Cloudera to Databricks**
> 
> Single entry point: `python projects/bradesco/scripts/00_MASTER_PIPELINE.py`
>
> **🧠 Memory System**: Project knowledge captured in `/memories/repo/MEMORY-INDEX.md`  
> Reference this for architecture, lessons learned, best practices, and roadmap.

## 🎯 Project Overview

This project implements a **complete data migration pipeline** for the Bradesco financial institution:
- **Source:** Cloudera (legacy on-premises data platform)
- **Target:** Databricks (cloud-native data lakehouse on Azure)
- **Scope:** Financial data, customer segments, transaction ledgers
- **Outcome:** Production-ready Databricks environment with full data validation

### Key Metrics
- **Legacy extraction:** 545+ artifacts
- **Logical entities:** 146 data models
- **Data loaded:** 12.4M+ rows
- **Validation score:** 98.7% (Production Ready)
- **ROI:** Quantified in consolidated dashboard

---

## 📋 Quick Start

### Prerequisites
```powershell
# Ensure you have:
# - Python 3.13+
# - Virtual environment (.venv) created
# - Dependencies: markdown, pyyaml
```

### One-Command Execution (Recommended)
```powershell
# Navigate to project root
cd c:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install markdown pyyaml

# Run the master pipeline (autonomous A→F)
python projects/bradesco/scripts/00_MASTER_PIPELINE.py
```

**Runtime:** ~10–20 minutes (depends on legacy data volume)

**Output:**
- ✓ Phase A: Configuration validated
- ✓ Phase B: Legacy data extracted & analyzed
- ✓ Phase C: Target data model designed
- ✓ Phase D: Data deployed & validated
- ✓ Phase E: Reports & dashboards generated
- ✓ Phase F: Outputs normalized & published

### View Results
```powershell
# Serve dashboards locally
python -m http.server 8000 --directory projects/bradesco/outputs

# Open browser to:
# http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
```

---

## 📂 Project Structure

```
projects/bradesco/
├── wave-config.yaml                              # Project metadata
├── legacy/                                        # Cloudera exports (input)
├── WORKFLOW_AND_ARCHITECTURE.md                 # ⭐ Detailed workflow explanation
├── README-REPORT-GENERATION.md                   # Dashboard generation guide
├── scripts/
│   ├── 00_MASTER_PIPELINE.py                    # ⭐ MAIN ENTRY POINT
│   ├── run_all_phases.py                        # Upstream wrapper
│   ├── run_midstream_phases.py                  # Midstream wrapper
│   ├── run_downstream_phases.py                 # Downstream wrapper
│   ├── upstream_phase[1-7]_*.py                 # Individual phases
│   ├── midstream_phase[1-3]_*.py
│   ├── downstream_phase[1-3]_*.py
│   ├── generate_consolidated_report.py          # Report aggregator
│   ├── generate_tabbed_report.py                # Dashboard builder
│   ├── generate_roi_analysis.py                 # ROI calculator
│   └── normalize_outputs_to_template.py         # Template applier
└── outputs/
    ├── upstream/                                 # Discovery artifacts
    ├── midstream/                                # Design artifacts
    ├── downstream/                               # Deployment artifacts
    ├── raw/                                      # Non-HTML archives
    ├── 00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html  # ⭐ MAIN DASHBOARD
    ├── EXECUTION_SUMMARY.json                   # Metadata
    └── README-REPORT-GENERATION.md               # Output instructions
```

---

## 🔄 Workflow Phases

### Phase A: Configuration Validation
- Verify `wave-config.yaml` has all required fields
- Check project metadata (name, owners, scope)

### Phase B: Upstream Discovery (Legacy Analysis)
1. Extract legacy data archives
2. Inventory schemas, tables, columns
3. Parse code (SQL, configs)
4. Analyze lineage & dependencies
5. Map data flows & risks
6. Summarize findings
7. Validate completeness (Gate 1)

### Phase C: Midstream Design (Data Modeling)
1. Design logical data model
2. Define target architecture (Medallion pattern)
3. Generate DDL & ETL code

### Phase D: Downstream Deployment (ETL & Validation)
1. Prepare deployment environment
2. Execute ETL pipelines
3. Validate data integrity (Gate 3)

### Phase E: Consolidation & Dashboards
1. Calculate ROI metrics
2. Aggregate findings into Markdown report
3. Build tabbed HTML dashboard

### Phase F: Template Normalization & Publication
1. Apply Avanade master template to all HTML
2. Archive non-HTML files to `raw/`
3. Prepare for stakeholder review

---

## 📊 Dashboard Features

The **main output** is `00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html`:

✨ **Interactive Tabbed UI:**
- **Upstream Tab:** Legacy analysis, inventory, risks
- **Midstream Tab:** Data model, architecture, design decisions
- **Downstream Tab:** Deployment checklist, load stats, validation results

📈 **KPI Metrics (per tab):**
- ROI % & payback period
- Entity/artifact counts
- Validation scores & gate status

🎨 **Avanade Branding:**
- Purple (#5c2d91) + Orange (#ff6b35) gradient header
- Clean, professional layout
- Mobile-responsive design

---

## 🛠️ Manual Execution (Advanced)

For step-by-step control, see `README-REPORT-GENERATION.md`:

```powershell
# Run individual phases
python projects/bradesco/scripts/run_all_phases.py           # Upstream
python projects/bradesco/scripts/run_midstream_phases.py     # Midstream
python projects/bradesco/scripts/run_downstream_phases.py    # Downstream

# Generate reports
python projects/bradesco/scripts/generate_consolidated_report.py
python projects/bradesco/scripts/generate_roi_analysis.py
python projects/bradesco/scripts/generate_tabbed_report.py

# Normalize & archive
python projects/bradesco/scripts/normalize_outputs_to_template.py
```

---

## 📝 Configuration (wave-config.yaml)

Required fields:
```yaml
project_name: Bradesco
discovery_owner: john.doe@avanade.com
source_platform: cloudera
target_platform: databricks
scope:
  - financial_data
  - customer_segments
  - transaction_ledger
```

---

## 📖 Full Documentation

- **Workflow & Architecture:** [WORKFLOW_AND_ARCHITECTURE.md](WORKFLOW_AND_ARCHITECTURE.md)
- **Report Generation Guide:** [README-REPORT-GENERATION.md](README-REPORT-GENERATION.md)
- **Data Migration Factory v3 Docs:** [../../docs/](../../docs/)

---

## 🚀 Reusability

To migrate another project (e.g., Einstein-HIAE):

1. Create `projects/einstein-hiae/`
2. Copy `projects/bradesco/scripts/` to new project
3. Create `projects/einstein-hiae/wave-config.yaml`
4. Place legacy data in `projects/einstein-hiae/legacy/`
5. Run: `python projects/einstein-hiae/scripts/00_MASTER_PIPELINE.py`

All logic adapts automatically based on configuration.

---

## ✅ Verification Checklist

After running the master pipeline:

- [ ] `EXECUTION_SUMMARY.json` shows all phases with ✓ SUCCESS
- [ ] `upstream/`, `midstream/`, `downstream/` folders have artifacts
- [ ] `outputs/*.html` contains 3+ normalized dashboards
- [ ] `raw/` folder contains archived Markdown/JSON files
- [ ] Dashboard loads at `http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html`
- [ ] Dashboard tabs (Upstream/Midstream/Downstream) are clickable
- [ ] KPI metrics display correctly
- [ ] Avanade branding visible (purple header, orange accents)

---

## 📞 Support

For questions or issues:
1. Check `EXECUTION_SUMMARY.json` for structured error logs
2. Review phase-specific outputs in `upstream/`, `midstream/`, `downstream/`
3. Refer to individual phase scripts for business logic
4. See `WORKFLOW_AND_ARCHITECTURE.md` for conceptual guidance

---

**Status:** 🟢 Production Ready  
**Last Updated:** 2026-06-08  
**Maintained By:** Data Migration Factory v3 Team
