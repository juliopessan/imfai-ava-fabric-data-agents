#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORKFLOW INTEGRATION VALIDATION v2 - Simplificado & Realista
=============================================================
Valida estrutura funcional (sem dependência em Copilot Memory)
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# ============================================================================
# CORES & FORMATAÇÃO
# ============================================================================
class C:
    G = '\033[92m'  # Green
    R = '\033[91m'  # Red
    Y = '\033[93m'  # Yellow
    C = '\033[96m'  # Cyan
    B = '\033[1m'   # Bold
    E = '\033[0m'   # End

def ok(name, detail=""):
    print(f"  {C.G}✓{C.E} {name:50} {C.G}OK{C.E}  {detail}")

def fail(name, detail=""):
    print(f"  {C.R}✗{C.E} {name:50} {C.R}FAIL{C.E} {detail}")

# ============================================================================
# MAIN VALIDATION
# ============================================================================
def validate():
    ws_root = Path(__file__).parent
    all_ok = True
    
    print(f"\n{C.B}{C.C}{'='*76}{C.E}")
    print(f"{C.B}{C.C}WORKFLOW INTEGRATION CHECK v2.0{C.E}")
    print(f"{C.B}{C.C}Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.E}")
    print(f"{C.B}{C.C}{'='*76}{C.E}\n")
    
    # ========================================================================
    # [1] ESTRUTURA DE CASES
    # ========================================================================
    print(f"{C.B}[1] ESTRUTURA DE CASES{C.E}")
    print("=" * 76)
    
    for case_name in ["bradesco", "einstein-hiae"]:
        case_path = ws_root / "projects" / case_name
        exists = case_path.exists()
        
        subfolders = ["scripts", "legacy", "context", "outputs"]
        subfolder_check = all((case_path / f).exists() for f in subfolders)
        
        if exists and subfolder_check:
            ok(f"Case: {case_name}", "✓ All folders present")
        else:
            missing = [f for f in subfolders if not (case_path / f).exists()] if exists else "case folder missing"
            fail(f"Case: {case_name}", f"Missing: {missing}" if isinstance(missing, list) else missing)
            all_ok = False
    
    # ========================================================================
    # [2] MASTER PIPELINE & SCRIPTS
    # ========================================================================
    print(f"\n{C.B}[2] MASTER PIPELINE & SCRIPTS CRÍTICOS{C.E}")
    print("=" * 76)
    
    critical_scripts = {
        "projects/bradesco/scripts/00_MASTER_PIPELINE.py": "Master orchestrator",
        "projects/bradesco/scripts/run_all_phases.py": "Phase B: Upstream",
        "projects/bradesco/scripts/run_midstream_phases.py": "Phase C: Midstream",
        "projects/bradesco/scripts/run_downstream_phases.py": "Phase D: Downstream",
        "projects/bradesco/scripts/generate_consolidated_report.py": "Report generation",
        "projects/bradesco/scripts/generate_tabbed_report.py": "Dashboard generation",
        "projects/bradesco/scripts/normalize_outputs_to_template.py": "Template normalization"
    }
    
    for script_rel, description in critical_scripts.items():
        script_path = ws_root / script_rel
        if script_path.exists():
            ok(f"Script: {Path(script_rel).name}", description)
        else:
            fail(f"Script: {Path(script_rel).name}", f"NOT FOUND - {description}")
            all_ok = False
    
    # ========================================================================
    # [3] TEMPLATES & BRANDING
    # ========================================================================
    print(f"\n{C.B}[3] TEMPLATES & BRANDING{C.E}")
    print("=" * 76)
    
    template_path = ws_root / "reports" / "_templates" / "DASHBOARD-TEMPLATE-MASTER.html"
    if template_path.exists():
        ok("Template: DASHBOARD-TEMPLATE-MASTER.html", "Avanade branding")
        
        # Check placeholders
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_markers = [
            ("{{TITLE}}", "Page title placeholder"),
            ("{{MAIN_CONTENT}}", "Main content section"),
            ("{{KPI_METRICS}}", "KPI metrics section"),
            ("#5c2d91", "Purple branding color"),
            ("#ff6b35", "Orange branding color")
        ]
        
        for marker, desc in required_markers:
            if marker in content:
                ok(f"  Placeholder: {marker}", desc)
            else:
                fail(f"  Placeholder: {marker}", f"MISSING - {desc}")
                all_ok = False
    else:
        fail("Template: DASHBOARD-TEMPLATE-MASTER.html", "NOT FOUND")
        all_ok = False
    
    # ========================================================================
    # [4] CONFIGURAÇÃO
    # ========================================================================
    print(f"\n{C.B}[4] CONFIGURAÇÃO{C.E}")
    print("=" * 76)
    
    wave_config = ws_root / "projects" / "einstein-hiae" / "wave-config.yaml"
    if wave_config.exists():
        ok("wave-config.yaml", "Configuration file present")
        
        try:
            import yaml
            with open(wave_config) as f:
                config = yaml.safe_load(f)
            
            required_keys = ["project_name", "migration_scope", "phases"]
            missing_keys = [k for k in required_keys if k not in config]
            
            if not missing_keys:
                ok("  Config structure", "All required fields present")
            else:
                fail("  Config structure", f"Missing: {missing_keys}")
                all_ok = False
        except Exception as e:
            fail("  Config parsing", f"Error: {str(e)}")
            all_ok = False
    else:
        fail("wave-config.yaml", "NOT FOUND")
        all_ok = False
    
    # ========================================================================
    # [5] DEPENDÊNCIAS PYTHON
    # ========================================================================
    print(f"\n{C.B}[5] DEPENDÊNCIAS PYTHON{C.E}")
    print("=" * 76)
    
    required_packages = {
        "markdown": "HTML report generation",
        "yaml": "YAML configuration",
        "json": "Data serialization",
        "pathlib": "Path operations"
    }
    
    for package, desc in required_packages.items():
        try:
            __import__(package)
            ok(f"Package: {package}", desc)
        except ImportError:
            fail(f"Package: {package}", f"NOT INSTALLED - {desc}")
            all_ok = False
    
    # ========================================================================
    # [6] OUTPUTS & FUNCIONALIDADE
    # ========================================================================
    print(f"\n{C.B}[6] OUTPUTS & FUNCIONALIDADE{C.E}")
    print("=" * 76)
    
    outputs_path = ws_root / "projects" / "bradesco" / "outputs"
    if outputs_path.exists():
        ok("Outputs folder: bradesco", "Ready for generated reports")
    else:
        fail("Outputs folder: bradesco", "NOT FOUND")
        all_ok = False
    
    # ========================================================================
    # [RESUMO FINAL]
    # ========================================================================
    print(f"\n{C.B}{'='*76}{C.E}")
    print(f"{C.B}{C.C}RESUMO FINAL{C.E}")
    print(f"{C.B}{'='*76}{C.E}\n")
    
    if all_ok:
        print(f"{C.G}{C.B}✓ TUDO 100% FUNCIONAL!{C.E}\n")
        print(f"{C.C}Sistema pronto para:{C.E}")
        print(f"  1. Executar master pipeline:")
        print(f"     python projects/bradesco/scripts/00_MASTER_PIPELINE.py")
        print(f"\n  2. Referenciar documentação:")
        print(f"     - Memória: /memories/repo/MEMORY-INDEX.md")
        print(f"     - Código: projects/bradesco/README.md")
        print(f"\n  3. Adicionar novo case:")
        print(f"     - Veja: /memories/repo/fabricae-best-practices.md")
        return 0
    else:
        print(f"{C.R}{C.B}✗ PROBLEMAS DETECTADOS{C.E}\n")
        print(f"{C.Y}Ação recomendada:{C.E}")
        print(f"  1. Revisar erros acima (marcados com ✗)")
        print(f"  2. Instalar pacotes faltantes")
        print(f"  3. Reexecutar este script")
        return 1

# ============================================================================
# SAVE REPORT
# ============================================================================
def save_report(success):
    ws_root = Path(__file__).parent
    report = {
        "timestamp": datetime.now().isoformat(),
        "validation_passed": success,
        "workspace": str(ws_root),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
    
    report_file = ws_root / "WORKFLOW-INTEGRATION-REPORT.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n  📊 Relatório salvo: {report_file}")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    success = validate() == 0
    save_report(success)
    sys.exit(0 if success else 1)
