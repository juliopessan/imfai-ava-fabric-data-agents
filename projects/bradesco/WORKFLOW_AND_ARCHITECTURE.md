# Bradesco Data Migration — Workflow & Architecture

> Complete end-to-end autonomous pipeline for data platform migration from Cloudera to Databricks.  
> Master orchestrator: `projects/bradesco/scripts/00_MASTER_PIPELINE.py`

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  PHASE A: Configuration Validation                               │
│  └─ Validate wave-config.yaml (project metadata, owners, scope)  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  PHASE B: Upstream Discovery (Legacy Analysis)                  │
│  ├─ Phase 1: ZIP Extraction (extract legacy artifacts)          │
│  ├─ Phase 2: Inventory & Packages (scan schemas, tables)        │
│  ├─ Phase 3: Code Parsing (SQL, configs, dependencies)          │
│  ├─ Phase 4: Lineage, Configs, Dependencies, Risks             │
│  ├─ Phase 5: As-Is Architecture (source platform snapshot)      │
│  ├─ Phase 6: Upstream Summary Report                           │
│  └─ Phase 7: Gate 1 Validation (completeness, quality checks)  │
│  Output: projects/bradesco/outputs/upstream/                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  PHASE C: Midstream Design (Data Modeling)                      │
│  ├─ Phase 1: Logical Data Model (entities, attributes, types)  │
│  ├─ Phase 2: Architecture & Target Design (Medallion pattern)  │
│  └─ Phase 3: DDL & ETL Code Generation (Databricks SQL/Spark) │
│  Output: projects/bradesco/outputs/midstream/                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  PHASE D: Downstream Deployment (ETL & Validation)             │
│  ├─ Phase 1: Deployment Preparation (apply DDL, init schemas) │
│  ├─ Phase 2: ETL Execution (ingest, transform, load data)      │
│  └─ Phase 3: Validation & Reconciliation (row count, checksums)│
│  Output: projects/bradesco/outputs/downstream/                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  PHASE E: Consolidation & Dashboard Generation                 │
│  ├─ ROI Analysis (cost/benefit, payback period)                │
│  ├─ Consolidated Markdown Report (all phases + findings)       │
│  └─ Tabbed HTML Dashboard (Upstream/Midstream/Downstream tabs) │
│  Output: projects/bradesco/outputs/*.md, *.html               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  PHASE F: Template Normalization & Publication                 │
│  ├─ Normalize all HTML to Avanade master template              │
│  ├─ Archive non-HTML files to outputs/raw/                    │
│  └─ Ready for stakeholder review                               │
│  Output: projects/bradesco/outputs/*.html (only)              │
└──────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
projects/bradesco/
├── wave-config.yaml                     # Project metadata (project name, owners, scope)
├── legacy/                              # Legacy source artifacts (Cloudera exports)
├── context/                             # Additional context files
├── scripts/
│   ├── 00_MASTER_PIPELINE.py           # ⭐ ENTRY POINT — Autonomous end-to-end orchestration
│   ├── run_all_phases.py               # Upstream pipeline wrapper
│   ├── run_midstream_phases.py          # Midstream pipeline wrapper
│   ├── run_downstream_phases.py         # Downstream pipeline wrapper
│   ├── upstream_phase[1-7]_*.py        # Individual upstream phases
│   ├── midstream_phase[1-3]_*.py       # Individual midstream phases
│   ├── downstream_phase[1-3]_*.py      # Individual downstream phases
│   ├── generate_consolidated_report.py  # Consolidate all artifacts into Markdown
│   ├── generate_tabbed_report.py        # Create tabbed HTML dashboard
│   ├── generate_roi_analysis.py         # Calculate ROI metrics
│   ├── normalize_outputs_to_template.py # Apply Avanade master template
│   └── apply_html_template.py           # Utility for converting Markdown→HTML
├── outputs/                             # ✅ Final deliverables
│   ├── upstream/                        # Discovery artifacts (545+ files)
│   ├── midstream/                       # Design artifacts (DDL, architecture)
│   ├── downstream/                      # Deployment artifacts (validation, reconciliation)
│   ├── raw/                             # Non-HTML artifacts (archived)
│   ├── 00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html  # ⭐ Main dashboard (Upstream/Midstream/Downstream tabs)
│   ├── 00_CONSOLIDATED_MIGRATION_REPORT_templated.html
│   ├── 00_CONSOLIDATED_MIGRATION_REPORT.html
│   ├── EXECUTION_SUMMARY.json           # Execution metadata
│   └── README-REPORT-GENERATION.md      # Report generation instructions
```

## Quick Start

### 1. One-Command Execution (Fully Autonomous)

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install markdown pyyaml

# Run master pipeline (A→B→C→D→E→F)
python projects/bradesco/scripts/00_MASTER_PIPELINE.py
```

The master pipeline will:
- ✓ Validate configuration
- ✓ Extract legacy data
- ✓ Analyze & inventory
- ✓ Design target data model
- ✓ Generate DDL & ETL
- ✓ Deploy to Databricks
- ✓ Validate data
- ✓ Create consolidated reports
- ✓ Generate Avanade-branded dashboards
- ✓ Archive non-HTML artifacts

### 2. Serve Dashboards Locally

```powershell
python -m http.server 8000 --directory projects/bradesco/outputs
# Open: http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
```

### 3. View Execution Summary

```powershell
cat projects/bradesco/outputs/EXECUTION_SUMMARY.json
```

## Key Design Principles

### Autonomous Execution
- All phases run sequentially without human intervention.
- Each phase validates inputs before proceeding.
- Failures are logged; execution stops at critical errors.

### Artifact Organization
- Each phase produces artifacts in `outputs/{upstream,midstream,downstream}`.
- Non-HTML artifacts are automatically archived to `outputs/raw/`.
- Only clean HTML dashboards remain public in `outputs/`.

### Template Standardization
- All HTML outputs conform to `reports/_templates/DASHBOARD-TEMPLATE-MASTER.html`.
- Avanade branding (colors: #5c2d91 purple, #ff6b35 orange) applied consistently.
- Clean HTML formatting (no markdown, no raw JSON).

### Dashboard Generation
- **Tabbed UI:** Upstream / Midstream / Downstream sections in one view.
- **KPI Tables:** ROI %, payback period, entity counts, validation scores.
- **Responsive Design:** Ready for desktop, tablet, mobile.

## Artifact Outputs

### Upstream Discovery
- Legacy data inventory (schemas, tables, columns)
- Lineage analysis (dependencies, ETL flows)
- Risk assessment (orphaned data, missing metadata)
- As-Is architecture diagram
- Gate 1 validation report

### Midstream Design
- Logical data model (146+ entities for Bradesco)
- Target architecture (Medallion: Bronze/Silver/Gold)
- DDL scripts (Databricks schemas, tables)
- ETL templates (PySpark jobs, orchestration)

### Downstream Deployment
- Deployment readiness checklist
- Data load statistics (12.4M+ rows for Bradesco)
- Reconciliation reports (row counts, checksums)
- Gate 3 validation (98.7% compliance)

### Dashboards
- **Consolidated Report (Tabbed):** Entire migration in one interactive HTML.
- **ROI Analysis:** Investment justification, payback timeline.
- **Executive Summary:** One-pager for stakeholders.

## Configuration (wave-config.yaml)

```yaml
project_name: Bradesco
discovery_owner: john.doe@avanade.com
source_platform: cloudera
target_platform: databricks
scope:
  - financial_data
  - customer_segments
  - transaction_ledger
  # Add more domains as needed
```

## Logs & Debugging

- Real-time output: Check terminal during execution.
- Execution summary: `projects/bradesco/outputs/EXECUTION_SUMMARY.json`
- Phase-specific logs: `projects/bradesco/outputs/{upstream,midstream,downstream}/`
- Errors: Non-zero exit code; check last failed step for details.

## Reusability Across Projects

To apply this workflow to a new project (e.g., `einstein-hiae`):

1. Create `projects/einstein-hiae/` folder
2. Copy `projects/bradesco/scripts/` to the new project
3. Create `projects/einstein-hiae/wave-config.yaml` with project metadata
4. Place legacy artifacts in `projects/einstein-hiae/legacy/`
5. Run: `python projects/einstein-hiae/scripts/00_MASTER_PIPELINE.py`

All configurations are inferred from `wave-config.yaml` and script logic adapts automatically.

## Glossary

- **Gate:** Quality checkpoint (Gate 1 after Upstream, Gate 2 after Midstream, Gate 3 after Downstream).
- **Medallion:** Data architecture pattern (Bronze=raw, Silver=clean, Gold=analytics).
- **Lineage:** Data flow dependencies (which source tables feed which targets).
- **STTM:** Source-to-Target Mapping (row-by-row transformation rules).
- **ROI:** Return on Investment (cost savings from cloud migration).

## Support & Next Steps

For questions or customizations:
- Review log files in each phase's output folder.
- Check `EXECUTION_SUMMARY.json` for structured metadata.
- Refer to individual phase scripts for detailed business logic.
