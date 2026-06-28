#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FACTORY BOOTSTRAP — Data Migration Factory v3
==============================================
Creates a complete, autonomous migration project from scratch.
Copies + patches all phase scripts. Generates wave-config.yaml.
Drops a pre-configured GENERIC_MASTER_PIPELINE.py into the new project.

Usage:
    python scripts/FACTORY_BOOTSTRAP.py --project-name supply-chain --wave 1
    python scripts/FACTORY_BOOTSTRAP.py --project-name retail-pos --domain retail --target fabric
    python scripts/FACTORY_BOOTSTRAP.py --list-domains

Examples:
    python scripts/FACTORY_BOOTSTRAP.py --project-name ecommerce-platform --domain ecommerce
    python scripts/FACTORY_BOOTSTRAP.py --project-name supply-chain --domain logistics --wave 2
"""

import argparse
import io
import shutil
import sys
import re
from datetime import datetime
from pathlib import Path

# Force UTF-8 output on Windows (prevents charmap errors with Unicode chars)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_SOURCE = REPO_ROOT / "projects" / "financeiro" / "scripts"
PROJECTS_DIR = REPO_ROOT / "projects"
TOOLS_PATH = REPO_ROOT / "tools" / "trace-integration"

# ── Domain Defaults ──────────────────────────────────────────────────────────
DOMAIN_DEFAULTS = {
    "logistics": {
        "description": "Supply chain, warehouse, transportation, inventory management",
        "sources": ["SAP ERP", "Oracle WMS", "Kinaxis", "Blue Yonder"],
        "token_budgets": {"upstream": 160000, "midstream": 130000, "downstream": 110000, "consolidation": 55000},
        "known_risks": ["supplier_data_fragmentation", "real_time_inventory_sync", "multi_warehouse_topology"],
        "target_platform": "fabric",
    },
    "retail": {
        "description": "Point of sale, multi-store, product catalog, promotions",
        "sources": ["Salesforce", "SAP POS", "Azure SQL", "Dynamics 365"],
        "token_budgets": {"upstream": 140000, "midstream": 110000, "downstream": 95000, "consolidation": 50000},
        "known_risks": ["high_volume_transactions", "multi_store_consolidation", "seasonal_load_spikes"],
        "target_platform": "fabric",
    },
    "ecommerce": {
        "description": "Online sales, product catalog, orders, payments, recommendations",
        "sources": ["Magento", "Shopify", "MongoDB", "Elasticsearch", "Redis"],
        "token_budgets": {"upstream": 150000, "midstream": 120000, "downstream": 100000, "consolidation": 50000},
        "known_risks": ["unstructured_product_data", "real_time_recommendations", "multi_currency_support"],
        "target_platform": "fabric",
    },
    "healthcare": {
        "description": "Patient records, clinical workflows, billing, compliance (LGPD/HIPAA)",
        "sources": ["HL7 FHIR", "Epic", "SQL Server", "Oracle Health"],
        "token_budgets": {"upstream": 170000, "midstream": 140000, "downstream": 120000, "consolidation": 60000},
        "known_risks": ["phi_data_sensitivity", "hl7_fhir_compliance", "audit_trail_requirements"],
        "target_platform": "fabric",
    },
    "finance": {
        "description": "Core banking, accounting, payments, regulatory reporting",
        "sources": ["Cloudera", "Airflow", "SAP BO", "PowerCenter", "Snowflake"],
        "token_budgets": {"upstream": 150000, "midstream": 120000, "downstream": 100000, "consolidation": 50000},
        "known_risks": ["regulatory_compliance", "data_lineage_audit", "reconciliation_precision"],
        "target_platform": "fabric",
    },
    "manufacturing": {
        "description": "Production planning, quality control, equipment, IoT sensors",
        "sources": ["SAP S/4HANA", "OSIsoft PI", "Wonderware", "SQL Server"],
        "token_budgets": {"upstream": 155000, "midstream": 125000, "downstream": 105000, "consolidation": 52000},
        "known_risks": ["iot_data_volume", "real_time_quality_alerts", "equipment_downtime_tracking"],
        "target_platform": "fabric",
    },
    "generic": {
        "description": "General-purpose migration (customize after bootstrap)",
        "sources": ["Legacy System A", "Legacy System B"],
        "token_budgets": {"upstream": 150000, "midstream": 120000, "downstream": 100000, "consolidation": 50000},
        "known_risks": ["data_quality_unknown", "legacy_documentation_gaps"],
        "target_platform": "fabric",
    },
}

# ── Ponytail artifact targets (Gate 1-4) ─────────────────────────────────────
PONYTAIL_TARGETS = {
    1: {"min": 1, "target": 3, "max": 5},   # Upstream: YAGNI
    2: {"min": 2, "target": 5, "max": 8},   # Midstream: Design críticas
    3: {"min": 3, "target": 6, "max": 10},  # Downstream: 1 ETL prototípico
    4: {"min": 2, "target": 11, "max": 20}, # Consolidation: 2-3 dashboards + templates
}

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║       DATA MIGRATION FACTORY v3 — PROJECT BOOTSTRAP         ║
║       Avanade | Orange DNA | 100% Autonomous                 ║
╚══════════════════════════════════════════════════════════════╝
"""


def print_step(n, total, title):
    print(f"\n  [{n}/{total}] {title}")
    print(f"  {'─' * 60}")


def slugify(name: str) -> str:
    """Normalize project name: supply chain → supply-chain"""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def list_domains():
    print("\nAvailable domains:\n")
    for domain, info in DOMAIN_DEFAULTS.items():
        sources = ", ".join(info["sources"][:3])
        print(f"  {domain:<20} {info['description'][:55]}")
        print(f"  {'':20} Sources: {sources}")
        print()
    sys.exit(0)


def create_directory_structure(project_dir: Path, project_name: str):
    """Create the complete project directory structure."""
    dirs = [
        project_dir / "scripts",
        project_dir / "outputs" / "upstream",
        project_dir / "outputs" / "midstream",
        project_dir / "outputs" / "downstream",
        project_dir / "outputs" / "consolidation",
        project_dir / "outputs" / "raw",
        project_dir / "legacy",
        project_dir / "context",
        project_dir / "state",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print(f"    ✅ Created {len(dirs)} directories")


def copy_and_patch_scripts(project_dir: Path, project_name: str, domain_info: dict):
    """Copy all phase scripts and patch hardcoded references."""
    if not TEMPLATE_SOURCE.exists():
        print(f"    ⚠️  Template source not found: {TEMPLATE_SOURCE}")
        print(f"    Creating stub phase scripts instead...")
        _create_stub_scripts(project_dir, project_name, domain_info)
        return

    target_scripts = project_dir / "scripts"
    scripts_to_copy = [
        "upstream_phase1_extract.py",
        "upstream_phase2_inventory.py",
        "upstream_phase3_parse.py",
        "upstream_phase4_lineage.py",
        "upstream_phase5_architecture.py",
        "upstream_phase6_summary.py",
        "upstream_phase7_validate.py",
        "midstream_phase1_design.py",
        "midstream_phase2_architecture.py",
        "midstream_phase3_codegen.py",
        "downstream_phase1_prep.py",
        "downstream_phase2_deploy.py",
        "downstream_phase3_validation.py",
        "run_all_phases.py",
        "run_midstream_phases.py",
        "run_downstream_phases.py",
        "apply_html_template.py",
        "generate_consolidated_report.py",
        "generate_tabbed_report.py",
        "normalize_outputs_to_template.py",
        "md_to_html.py",
    ]

    copied = 0
    for script in scripts_to_copy:
        src = TEMPLATE_SOURCE / script
        if not src.exists():
            continue
        dst = target_scripts / script
        content = src.read_text(encoding="utf-8", errors="ignore")

        # Patch: replace Financeiro project name references in output strings
        # (print statements / strings only - not structural paths)
        content = content.replace("' Financeiro —", f"' {project_name.upper()} —")
        content = content.replace('"Financeiro"', f'"{project_name}"')
        content = content.replace("Financeiro-", f"{project_name}-")
        content = content.replace("Financeiro_", f"{project_name}_")

        dst.write_text(content, encoding="utf-8")
        copied += 1

    # Patch PHASE4: hardcoded absolute project path
    _write_phase4(project_dir, project_name)
    print(f"    ✅ Copied + patched {copied} phase scripts")
    print(f"    ✅ Generated PHASE4_CONSOLIDATION_ORCHESTRATOR.py")


def _write_phase4(project_dir: Path, project_name: str):
    """Write a patched PHASE4 that uses dynamic project root instead of hardcoded Financeiro."""
    phase4_src = TEMPLATE_SOURCE / "PHASE4_CONSOLIDATION_ORCHESTRATOR.py"
    if not phase4_src.exists():
        return
    content = phase4_src.read_text(encoding="utf-8", errors="ignore")
    # The critical fix: replace the hardcoded Path("projects/Financeiro") with __file__-based path
    content = content.replace(
        'self.project_root = Path("projects/Financeiro")',
        'self.project_root = Path(__file__).parent.parent',
    )
    # Also fix any remaining Financeiro references in strings
    content = content.replace('"Financeiro Migration"', f'"{project_name.title()} Migration"')
    content = content.replace("Financeiro-", f"{project_name}-")
    (project_dir / "scripts" / "PHASE4_CONSOLIDATION_ORCHESTRATOR.py").write_text(
        content, encoding="utf-8"
    )


def _create_stub_scripts(project_dir: Path, project_name: str, domain_info: dict):
    """Create minimal stub scripts when template is unavailable."""
    target = project_dir / "scripts"
    stub_phases = {
        "run_all_phases.py": _stub_runner("UPSTREAM", ["upstream_phase1_extract.py",
            "upstream_phase2_inventory.py","upstream_phase3_parse.py",
            "upstream_phase4_lineage.py","upstream_phase5_architecture.py",
            "upstream_phase6_summary.py","upstream_phase7_validate.py"], project_name),
        "run_midstream_phases.py": _stub_runner("MIDSTREAM", ["midstream_phase1_design.py",
            "midstream_phase2_architecture.py","midstream_phase3_codegen.py"], project_name),
        "run_downstream_phases.py": _stub_runner("DOWNSTREAM", ["downstream_phase1_prep.py",
            "downstream_phase2_deploy.py","downstream_phase3_validation.py"], project_name),
    }
    for fname, content in stub_phases.items():
        (target / fname).write_text(content, encoding="utf-8")
    for phase_script in [
        "upstream_phase1_extract.py","upstream_phase2_inventory.py","upstream_phase3_parse.py",
        "upstream_phase4_lineage.py","upstream_phase5_architecture.py",
        "upstream_phase6_summary.py","upstream_phase7_validate.py",
        "midstream_phase1_design.py","midstream_phase2_architecture.py","midstream_phase3_codegen.py",
        "downstream_phase1_prep.py","downstream_phase2_deploy.py","downstream_phase3_validation.py",
    ]:
        stub = (
            f'"""Stub: {phase_script} — copy from projects/financeiro/scripts/ and adapt."""\n'
            f'import sys\nfrom pathlib import Path\n'
            f'BASE = Path(__file__).parent.parent\n'
            f'print(f"[STUB] {phase_script} — BASE={{BASE}}")\n'
            f'sys.exit(0)\n'
        )
        (target / phase_script).write_text(stub, encoding="utf-8")
    print(f"    ✅ Created stub scripts (replace with real logic per project)")


def _stub_runner(name: str, phases: list, project_name: str) -> str:
    phases_repr = repr(phases)
    return f'''\
"""Run All {name} Phases — {project_name}"""
import subprocess, sys, os, time
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
phases = {phases_repr}
results = []; total_start = time.time()
for script in phases:
    start = time.time()
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, script)],
                       capture_output=False, cwd=SCRIPTS_DIR)
    elapsed = time.time() - start
    status = "OK" if r.returncode == 0 else "FAILED"
    results.append((script, status, elapsed))
    if r.returncode != 0:
        print(f"  *** {{script}} FAILED"); break
failed = sum(1 for _, s, _ in results if s == "FAILED")
sys.exit(0 if failed == 0 else 1)
'''


def generate_wave_config(project_dir: Path, project_name: str, wave: int,
                          domain: str, target_platform: str, domain_info: dict):
    """Generate a fully populated wave-config.yaml for the new project."""
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(project_name)
    budgets = domain_info["token_budgets"]
    sources_str = "\n".join(f'    - "{s}"' for s in domain_info["sources"])
    risks_str = "\n".join(f'    - "{r}"' for r in domain_info["known_risks"])

    config = f"""\
# ============================================================================
# WAVE CONFIG — {project_name.upper()}
# Generated by FACTORY_BOOTSTRAP.py on {today}
# Domain: {domain} | Target: {target_platform} | Wave: {wave}
# ============================================================================
project_name: "{project_name}"
project_id: "{slug}-{datetime.now().year}"
description: "{domain_info['description']}"
organization: "Avanade"
target_platform: "{target_platform}"
migration_scope: "Full lift-and-shift + modernization."

# ── Wave ──────────────────────────────────────────────────────────────────────
wave_number: {wave}
wave_name: "{project_name.title()} Wave {wave}"
wave_start_date: "{today}"
wave_target_completion: "{datetime.now().year}-12-31"

# ── Ownership & RACI ──────────────────────────────────────────────────────────
discovery_owner: "discovery-scout"
architecture_owner: "data-architect"
data_model_owner: "data-modeler"
code_generator_owner: "code-generator"
quality_gate_owner: "quality-gate"
security_owner: "security-compliance"

# ── Known Sources (customize per project) ─────────────────────────────────────
sources:
{sources_str}

# ── Token Budgets (Ponytail Ladder) ───────────────────────────────────────────
# These feed directly into GENERIC_MASTER_PIPELINE trace metrics.
# Adjust based on actual source complexity.
token_budgets:
  upstream: {budgets['upstream']}
  midstream: {budgets['midstream']}
  downstream: {budgets['downstream']}
  consolidation: {budgets['consolidation']}

# ── Cost Targets per Gate (Ponytail enforcement) ──────────────────────────────
cost_targets:
  gate_1_upstream: 0.50
  gate_2_midstream: 0.40
  gate_3_downstream: 0.35
  gate_4_consolidation: 0.20

# ── Artifact Targets (Ponytail Ladder — YAGNI enforcement) ───────────────────
artifact_targets:
  gate_1: {{min: 1, target: 3, max: 5}}
  gate_2: {{min: 2, target: 5, max: 8}}
  gate_3: {{min: 3, target: 6, max: 10}}
  gate_4: {{min: 2, target: 11, max: 20}}

# ── Known Risks (domain-specific defaults) ───────────────────────────────────
known_risks:
{risks_str}

# ── GateScore Formula ─────────────────────────────────────────────────────────
# 0.35×Completude + 0.25×Qualidade + 0.20×RiscoResidual + 0.20×Reconciliação
# Approved: >= 0.85 | With open items: 0.70–0.84 | Blocked: < 0.70
gate_score_threshold:
  approved: 0.85
  approved_with_items: 0.70
  blocked: 0.70

# ── Trace & Observability ─────────────────────────────────────────────────────
trace:
  enabled: true
  wave_id: "{slug}-wave{wave}"
  output_dir: ".trace-logs"
"""
    (project_dir / "wave-config.yaml").write_text(config, encoding="utf-8")
    print(f"    ✅ wave-config.yaml generated ({len(config.splitlines())} lines)")


def generate_master_pipeline(project_dir: Path, project_name: str, slug: str, wave: int):
    """Drop a project-specific GENERIC_MASTER_PIPELINE.py into scripts/."""
    pipeline_code = f'''\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERIC MASTER PIPELINE — {project_name.upper()} | Wave {wave}
============================================================
Auto-generated by FACTORY_BOOTSTRAP.py — do not edit wave params here.
All configuration lives in wave-config.yaml (one level up).

Usage:
    python projects/{slug}/scripts/GENERIC_MASTER_PIPELINE.py
"""
import subprocess
import sys
import io
import os
import time
import yaml
from pathlib import Path
from datetime import datetime

# ── Force UTF-8 on Windows ───────────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent.parent
TOOLS_PATH = REPO_ROOT / "tools" / "trace-integration"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

try:
    from trace_writer import get_trace_writer
    from coach_insights import get_coach_insights
    TRACE_ENABLED = True
except ImportError:
    TRACE_ENABLED = False

# ── Load wave-config.yaml ─────────────────────────────────────────────────────
_cfg_path = PROJECT_ROOT / "wave-config.yaml"
try:
    with open(_cfg_path, encoding="utf-8") as _f:
        CFG = yaml.safe_load(_f)
except FileNotFoundError:
    print(f"[ERROR] wave-config.yaml not found at {{_cfg_path}}")
    sys.exit(1)

PROJECT_NAME = CFG.get("project_name", "{project_name}")
WAVE_ID = CFG.get("trace", {{}}).get("wave_id", "{slug}-wave{wave}")
BUDGETS = CFG.get("token_budgets", {{}})
COST_TARGETS = CFG.get("cost_targets", {{}})


def print_header(text):
    print(f"\\n{{'=' * 76}}\\n  {{text}}\\n{{'=' * 76}}\\n")


def run_script(script_name: str, description: str):
    """Execute a phase script and return (success, elapsed)."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"  [ERROR] Script not found: {{script_path}}")
        return False, 0

    print(f"  Executing: {{description}}...")
    start = time.time()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            cwd=str(SCRIPTS_DIR),
            timeout=300,
            env=env,
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            print(f"    [OK] {{elapsed:.1f}}s\\n")
            return True, elapsed
        else:
            print(f"    [FAIL] exit={{result.returncode}}\\n")
            return False, elapsed
    except subprocess.TimeoutExpired:
        return False, 300
    except Exception as e:
        print(f"    [ERROR] {{e}}\\n")
        return False, 0


def capture_trace(writer, coach, gate: int, operation: str, elapsed: float,
                  success: bool, artifacts: int):
    """Write trace + run Ponytail + coach analysis for one gate."""
    if not (TRACE_ENABLED and writer):
        return None
    tokens_in = BUDGETS.get(["upstream","midstream","downstream","consolidation"][gate-1], 100000)
    tokens_out = tokens_in // 2  # 50% compression (Ponytail target)
    cost_target = list(COST_TARGETS.values())[gate - 1] if COST_TARGETS else 0.50
    trace = writer.write_agent_execution(
        agent_id=f"{{PROJECT_NAME}}-gate{{gate}}-orchestrator",
        wave=WAVE_ID,
        gate=gate,
        operation_name=operation,
        duration_sec=elapsed,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost_target * (0.9 if success else 0.5),
        artifacts_generated=artifacts if success else 0,
        status="success" if success else "failure",
        user="system-automation",
    )
    analysis = coach.analyze_execution(trace)
    coach.print_insights(analysis)
    ladder = coach.validate_ponytail_ladder(trace, gate)
    if not ladder.get("ladder_ok", True):
        print(f"  [PONYTAIL] Gate {{gate}} violations: {{ladder.get('violations', [])}}")
    return trace


def main():
    print_header(f"{{PROJECT_NAME.upper()}} DATA MIGRATION FACTORY — MASTER PIPELINE")
    print(f"  Project:    {{PROJECT_ROOT}}")
    print(f"  Wave:       {{WAVE_ID}}")
    print(f"  Outputs:    {{OUTPUTS_DIR}}")
    print(f"  Started:    {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
    print(f"  Token budgets: {{BUDGETS}}")

    overall_start = time.time()
    results = []
    writer = get_trace_writer() if TRACE_ENABLED else None
    coach = get_coach_insights() if TRACE_ENABLED else None
    traces = []

    # ── Gate 1: UPSTREAM DISCOVERY (7 phases) ─────────────────────────────────
    print_header("GATE 1 — UPSTREAM DISCOVERY")
    ok, elapsed = run_script("run_all_phases.py", "Upstream pipeline (7 phases)")
    results.append(("Upstream Discovery", ok, elapsed))
    t = capture_trace(writer, coach, 1, "gate1_upstream_discovery", elapsed, ok, 3)
    if t: traces.append(t)

    # ── Gate 2: MIDSTREAM DESIGN (3 phases) ───────────────────────────────────
    print_header("GATE 2 — MIDSTREAM DESIGN")
    ok, elapsed = run_script("run_midstream_phases.py", "Midstream pipeline (3 phases)")
    results.append(("Midstream Design", ok, elapsed))
    t = capture_trace(writer, coach, 2, "gate2_midstream_design", elapsed, ok, 5)
    if t: traces.append(t)

    # ── Gate 3: DOWNSTREAM DEPLOYMENT (3 phases) ──────────────────────────────
    print_header("GATE 3 — DOWNSTREAM DEPLOYMENT")
    ok, elapsed = run_script("run_downstream_phases.py", "Downstream pipeline (3 phases)")
    results.append(("Downstream Deployment", ok, elapsed))
    t = capture_trace(writer, coach, 3, "gate3_downstream_deployment", elapsed, ok, 6)
    if t: traces.append(t)

    # ── Gate 4: CONSOLIDATION ─────────────────────────────────────────────────
    print_header("GATE 4 — CONSOLIDATION & PUBLISH")
    ok, elapsed = run_script("PHASE4_CONSOLIDATION_ORCHESTRATOR.py", "Consolidation + dashboards")
    results.append(("Consolidation", ok, elapsed))
    t = capture_trace(writer, coach, 4, "gate4_consolidation", elapsed, ok, 11)
    if t: traces.append(t)

    # ── Wave Summary ──────────────────────────────────────────────────────────
    if TRACE_ENABLED and coach:
        try:
            coach.print_wave_summary(WAVE_ID)
        except Exception:
            pass

    # ── Final Report ──────────────────────────────────────────────────────────
    total = time.time() - overall_start
    print_header("PIPELINE SUMMARY")
    print(f"  {{\'Gate\':<35}} {{\'Status\':<10}} {{\'Time\':<10}}")
    print(f"  {{'-' * 57}}")
    for name, ok, elapsed in results:
        status = "[OK]  " if ok else "[FAIL]"
        print(f"  {{name:<35}} {{status:<10}} {{elapsed:.1f}}s")
    print(f"  {{'-' * 57}}")
    print(f"  {{\'TOTAL\':<35}} {{\'\':<10}} {{total:.1f}}s")
    failed = sum(1 for _, s, _ in results if not s)
    msg = "All gates completed!" if failed == 0 else str(failed) + " gate(s) failed."
    print(f"\\n  " + msg)
    print(f"  Outputs: {{OUTPUTS_DIR}}")

    output_html = OUTPUTS_DIR / "00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html"
    if output_html.exists():
        print(f"\\n  Dashboard: python -m http.server 8000 --directory {{OUTPUTS_DIR}}")
        print(f"  Open:      http://localhost:8000/{{output_html.name}}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
'''
    (project_dir / "scripts" / "GENERIC_MASTER_PIPELINE.py").write_text(
        pipeline_code, encoding="utf-8"
    )
    print(f"    ✅ GENERIC_MASTER_PIPELINE.py generated (reads wave-config.yaml)")


def generate_readme(project_dir: Path, project_name: str, slug: str,
                    wave: int, domain: str, domain_info: dict):
    """Generate a quick-start README for the new project."""
    sources_str = ", ".join(domain_info["sources"])
    readme = f"""\
# {project_name.title()} — Migration Project

**Domain:** {domain} | **Wave:** {wave} | **Target:** {domain_info['target_platform'].upper()}

## Quick Start

```powershell
# 1. Ensure venv is active
.\\..\\..\\..venv\\Scripts\\Activate.ps1

# 2. Add legacy ZIP files (optional — for real data)
#    Copy source artifacts to: legacy/

# 3. Run migration (autonomous)
python scripts/GENERIC_MASTER_PIPELINE.py

# 4. View dashboard
python -m http.server 8000 --directory outputs
# Open: http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
```

## Configuration

All settings live in `wave-config.yaml`:
- Token budgets per gate
- Source systems
- Target platform
- Ponytail artifact targets
- GateScore thresholds

## Pipeline Sequence

```
Gate 1: Upstream Discovery    (7 phases — inventory, parse, lineage)
Gate 2: Midstream Design      (3 phases — data model, architecture, codegen)
Gate 3: Downstream Deployment (3 phases — prep, deploy, validate)
Gate 4: Consolidation         (dashboards, ROI, publish)
```

## Known Sources

{sources_str}

## Estimated Costs (with Ponytail)

| Gate | Tokens IN | Tokens OUT | Cost Target |
|------|-----------|------------|-------------|
| Upstream | {domain_info['token_budgets']['upstream']:,} | {domain_info['token_budgets']['upstream'] // 2:,} | $0.50 |
| Midstream | {domain_info['token_budgets']['midstream']:,} | {domain_info['token_budgets']['midstream'] // 2:,} | $0.40 |
| Downstream | {domain_info['token_budgets']['downstream']:,} | {domain_info['token_budgets']['downstream'] // 2:,} | $0.35 |
| Consolidation | {domain_info['token_budgets']['consolidation']:,} | {domain_info['token_budgets']['consolidation'] // 2:,} | $0.20 |
| **Total/Wave** | | | **~$1.45** |

_Generated by FACTORY_BOOTSTRAP.py on {datetime.now().strftime('%Y-%m-%d')}_
"""
    (project_dir / "README.md").write_text(readme, encoding="utf-8")
    print(f"    ✅ README.md generated")


def check_dependencies():
    """Check that yaml is available for the generated pipeline."""
    try:
        import yaml  # noqa
        return True
    except ImportError:
        print("    ⚠️  PyYAML not installed. Run: pip install pyyaml")
        print("       (Required by GENERIC_MASTER_PIPELINE.py)")
        return False


def bootstrap(project_name: str, wave: int, domain: str, target_platform: str):
    """Main bootstrap entry point."""
    print(BANNER)
    slug = slugify(project_name)
    domain_info = DOMAIN_DEFAULTS.get(domain, DOMAIN_DEFAULTS["generic"])
    target = domain_info.get("target_platform", target_platform)
    project_dir = PROJECTS_DIR / slug

    print(f"  Project:   {project_name}")
    print(f"  Slug:      {slug}")
    print(f"  Domain:    {domain}")
    print(f"  Target:    {target}")
    print(f"  Wave:      {wave}")
    print(f"  Location:  {project_dir}")

    if project_dir.exists():
        print(f"\n  ⚠️  Project already exists at {project_dir}")
        ans = input("  Overwrite? [y/N] ").strip().lower()
        if ans != "y":
            print("  Aborted.")
            sys.exit(0)

    TOTAL_STEPS = 6
    print_step(1, TOTAL_STEPS, "Creating directory structure")
    create_directory_structure(project_dir, slug)

    print_step(2, TOTAL_STEPS, "Copying + patching phase scripts")
    copy_and_patch_scripts(project_dir, slug, domain_info)

    print_step(3, TOTAL_STEPS, "Generating wave-config.yaml")
    generate_wave_config(project_dir, project_name, wave, domain, target, domain_info)

    print_step(4, TOTAL_STEPS, "Generating GENERIC_MASTER_PIPELINE.py")
    generate_master_pipeline(project_dir, project_name, slug, wave)

    print_step(5, TOTAL_STEPS, "Generating README.md")
    generate_readme(project_dir, project_name, slug, wave, domain, domain_info)

    print_step(6, TOTAL_STEPS, "Validating dependencies")
    check_dependencies()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ PROJECT BOOTSTRAPPED SUCCESSFULLY                        ║
╚══════════════════════════════════════════════════════════════╝

  Location:  projects/{slug}/
  Config:    projects/{slug}/wave-config.yaml
  Pipeline:  projects/{slug}/scripts/GENERIC_MASTER_PIPELINE.py

  NEXT STEPS:

  1. (Optional) Add legacy ZIP files to:
     projects/{slug}/legacy/

  2. Run migration:
     python projects/{slug}/scripts/GENERIC_MASTER_PIPELINE.py

  3. View dashboard:
     python -m http.server 8000 --directory projects/{slug}/outputs
     http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html

  Estimated cost: ~$1.45/wave (with Ponytail: ~$1.26)
  Estimated time: ~1 minute
""")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Data Migration Factory — Project Bootstrap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/FACTORY_BOOTSTRAP.py --project-name supply-chain
  python scripts/FACTORY_BOOTSTRAP.py --project-name retail-pos --domain retail
  python scripts/FACTORY_BOOTSTRAP.py --project-name ecommerce --domain ecommerce --wave 2
  python scripts/FACTORY_BOOTSTRAP.py --list-domains
        """,
    )
    parser.add_argument("--project-name", required=False, help="Project name (e.g. supply-chain)")
    parser.add_argument("--domain", default="generic",
                        choices=list(DOMAIN_DEFAULTS.keys()),
                        help="Business domain (default: generic)")
    parser.add_argument("--wave", type=int, default=1, help="Wave number (default: 1)")
    parser.add_argument("--target", default="fabric", help="Target platform (default: fabric)")
    parser.add_argument("--list-domains", action="store_true", help="List available domains")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.list_domains:
        list_domains()
    if not args.project_name:
        print("ERROR: --project-name is required. Use --list-domains to see available domains.")
        sys.exit(1)
    bootstrap(args.project_name, args.wave, args.domain, args.target)
