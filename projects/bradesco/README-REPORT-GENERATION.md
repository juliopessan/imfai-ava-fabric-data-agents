# Bradesco Report Generation & Dashboard Instructions

> **QUICK START:** Use the Master Pipeline for fully autonomous execution.  
> See `WORKFLOW_AND_ARCHITECTURE.md` for complete workflow documentation.

## Standard Workflow (Recommended)

### ⭐ Automated End-to-End (MASTER PIPELINE)

This is the **primary method** — executes all phases A–F autonomously:

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install markdown pyyaml

# Run master orchestrator (complete pipeline: validation → discovery → design → deployment → dashboards → normalization)
python projects/bradesco/scripts/00_MASTER_PIPELINE.py
```

**Outputs:**
- `projects/bradesco/outputs/upstream/` — discovery artifacts
- `projects/bradesco/outputs/midstream/` — design artifacts
- `projects/bradesco/outputs/downstream/` — deployment artifacts
- `projects/bradesco/outputs/*.html` — Avanade-branded dashboards (only)
- `projects/bradesco/outputs/raw/` — archived non-HTML files
- `projects/bradesco/outputs/EXECUTION_SUMMARY.json` — execution metadata

---

## Manual/Step-by-Step Workflow

Use this only if you need to run **individual phases** for debugging or customization.

### Step 1: Validate Configuration

```powershell
python src/shared/scripts/validate_wave_config.py projects/bradesco/wave-config.yaml
```

### Step 2: Run Upstream Discovery

```powershell
python projects/bradesco/scripts/run_all_phases.py
```

### Step 3: Run Midstream Design

```powershell
python projects/bradesco/scripts/run_midstream_phases.py
```

### Step 4: Run Downstream Deployment

```powershell
python projects/bradesco/scripts/run_downstream_phases.py
```

### Step 5: Generate Consolidated Report

```powershell
python projects/bradesco/scripts/generate_consolidated_report.py
```

### Step 6: Generate ROI Analysis

```powershell
python projects/bradesco/scripts/generate_roi_analysis.py
```

### Step 7: Generate Tabbed Dashboard

```powershell
python projects/bradesco/scripts/generate_tabbed_report.py
```

### Step 8: Normalize to Avanade Template

```powershell
python projects/bradesco/scripts/normalize_outputs_to_template.py
```

### Step 9: Archive Non-HTML Outputs

```powershell
Get-ChildItem -Path projects/bradesco/outputs -File | Where-Object { $_.Extension -ne '.html' } | Move-Item -Destination projects/bradesco/outputs/raw -Force
```

---

## Serve Dashboards Locally

```powershell
python -m http.server 8000 --directory projects/bradesco/outputs
# Open: http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
```

---

## Standard Output Policy

✅ **Allowed in `projects/bradesco/outputs/`:**
- `.html` files (dashboards, reports)
- Subdirectories: `upstream/`, `midstream/`, `downstream/`, `raw/`

❌ **NOT allowed in root of `outputs/`:**
- `.md` files → move to `raw/`
- `.json` files → move to `raw/`
- Other formats → move to `raw/`

**Reasoning:** Only clean HTML dashboards should be publicly visible; raw artifacts are archived for traceability.

---

## Dashboard Features

- **Tabbed Navigation:** Switch between Upstream / Midstream / Downstream
- **KPI Metrics:** ROI, payback period, entity counts, validation scores
- **Avanade Branding:** Purple (#5c2d91) + Orange (#ff6b35) color scheme
- **Responsive Layout:** Desktop, tablet, mobile-friendly
- **Clean HTML:** No markdown syntax; production-ready formatting

---

## Reusability

To apply this workflow to a new project:

1. Create `projects/{new-project}/`
2. Copy `scripts/` to the new project folder
3. Create `wave-config.yaml` with project metadata
4. Place legacy artifacts in `legacy/`
5. Run: `python scripts/00_MASTER_PIPELINE.py` 
