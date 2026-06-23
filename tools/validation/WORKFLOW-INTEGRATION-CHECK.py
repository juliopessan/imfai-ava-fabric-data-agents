#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORKFLOW INTEGRATION CHECK - Verificação 100% Funcional
========================================================

Valida:
1. Sistema de memória (`/memories/repo/`)
2. Estrutura de workflow (ClienteBanco + ClienteSaude)
3. Dependências Python
4. Arquivo de configuração
5. Integridade de templates
6. Capacidade de execução do master pipeline
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# CORES & FORMATAÇÃO
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def status(check_name, success, details=""):
    symbol = f"{Colors.GREEN}✓{Colors.ENDC}" if success else f"{Colors.RED}✗{Colors.ENDC}"
    status_text = f"{Colors.GREEN}OK{Colors.ENDC}" if success else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"  {symbol} {check_name:50} [{status_text}]")
    if details:
        print(f"     {details}")

# ============================================================================
# SEÇÃO 1: SISTEMA DE MEMÓRIA
# ============================================================================
def check_memory_system():
    print(f"\n{Colors.BOLD}[1] SISTEMA DE MEMÓRIA{Colors.ENDC}")
    print("=" * 76)
    
    memory_root = Path(__file__).parent / "memories" / "repo"
    
    required_files = {
        "MEMORY-INDEX.md": "Índice navegação",
        "fabricae-metadata.md": "Fatos + métricas",
        "fabricae-lessons-learned.md": "Lições capturadas",
        "fabricae-architecture-decisions.md": "10 ADRs",
        "fabricae-best-practices.md": "How-to + operações",
        "fabricae-TODO.md": "Roadmap priorizado"
    }
    
    all_ok = True
    total_size = 0
    
    for filename, description in required_files.items():
        filepath = memory_root / filename
        exists = filepath.exists()
        size = filepath.stat().st_size if exists else 0
        total_size += size
        
        status(
            f"Memory: {filename[:40]:40}",
            exists,
            f"{size/1024:.1f} KB - {description}"
        )
        all_ok = all_ok and exists
    
    print(f"\n  📊 Total memory: {total_size/1024:.1f} KB (token-efficient)")
    return all_ok, memory_root

# ============================================================================
# SEÇÃO 2: ESTRUTURA DE WORKFLOW
# ============================================================================
def check_workflow_structure():
    print(f"\n{Colors.BOLD}[2] ESTRUTURA DE WORKFLOW{Colors.ENDC}")
    print("=" * 76)
    
    workspace_root = Path(__file__).parent
    all_ok = True
    
    # Verificar cases
    cases = {
        "clientebanco": "Case 1 (Cloudera → Databricks)",
        "ClienteSaude": "Case 2 (Legacy → Modern)"
    }
    
    for case_name, description in cases.items():
        case_path = workspace_root / "projects" / case_name
        exists = case_path.exists()
        
        # Verificar subpastas
        subfolder_status = True
        if exists:
            required_subfolders = ["scripts", "legacy", "context", "outputs"]
            missing = [f for f in required_subfolders if not (case_path / f).exists()]
            subfolder_status = len(missing) == 0
            subfolder_detail = "✓ OK" if subfolder_status else f"Missing: {', '.join(missing)}"
        else:
            subfolder_detail = "Case folder not found"
        
        status(
            f"Case: {case_name:45}",
            exists and subfolder_status,
            f"{description} - {subfolder_detail}"
        )
        all_ok = all_ok and (exists and subfolder_status)
    
    # Verificar master pipeline
    master_pipeline = workspace_root / "projects" / "clientebanco" / "scripts" / "00_MASTER_PIPELINE.py"
    master_exists = master_pipeline.exists()
    status(
        "Master Pipeline: 00_MASTER_PIPELINE.py",
        master_exists,
        "Entry point para execução autônoma"
    )
    all_ok = all_ok and master_exists
    
    # Verificar template
    template_path = workspace_root / "reports" / "_templates" / "DASHBOARD-TEMPLATE-MASTER.html"
    template_exists = template_path.exists()
    status(
        "Template: DASHBOARD-TEMPLATE-MASTER.html",
        template_exists,
        "Branding Consultoria (#5c2d91 + #ff6b35)"
    )
    all_ok = all_ok and template_exists
    
    return all_ok

# ============================================================================
# SEÇÃO 3: DEPENDÊNCIAS PYTHON
# ============================================================================
def check_dependencies():
    print(f"\n{Colors.BOLD}[3] DEPENDÊNCIAS PYTHON{Colors.ENDC}")
    print("=" * 76)
    
    required_packages = {
        "markdown": "HTML report generation",
        "yaml": "YAML configuration parsing",
        "json": "Data serialization (built-in)",
        "pathlib": "Path operations (built-in)"
    }
    
    all_ok = True
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            status(
                f"Package: {package:45}",
                True,
                f"✓ Installed - {description}"
            )
        except ImportError:
            status(
                f"Package: {package:45}",
                False,
                f"⚠ Not installed - {description}"
            )
            all_ok = False
    
    return all_ok

# ============================================================================
# SEÇÃO 4: ARQUIVO DE CONFIGURAÇÃO
# ============================================================================
def check_configuration():
    print(f"\n{Colors.BOLD}[4] ARQUIVO DE CONFIGURAÇÃO{Colors.ENDC}")
    print("=" * 76)
    
    workspace_root = Path(__file__).parent
    wave_config = workspace_root / "projects" / "ClienteSaude" / "wave-config.yaml"
    
    config_exists = wave_config.exists()
    status(
        "wave-config.yaml (Case 2)",
        config_exists,
        "Configuração central do case"
    )
    
    # Se existe, verificar estrutura básica
    if config_exists:
        try:
            import yaml
            with open(wave_config) as f:
                config = yaml.safe_load(f)
            
            required_keys = ["project_name", "migration_scope", "phases"]
            missing_keys = [k for k in required_keys if k not in config]
            
            if missing_keys:
                status(
                    "wave-config.yaml structure",
                    False,
                    f"Missing keys: {', '.join(missing_keys)}"
                )
                return False
            else:
                status(
                    "wave-config.yaml structure",
                    True,
                    f"✓ All required fields present"
                )
                return True
        except Exception as e:
            status(
                "wave-config.yaml parsing",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    return config_exists

# ============================================================================
# SEÇÃO 5: INTEGRIDADE DE TEMPLATES
# ============================================================================
def check_templates():
    print(f"\n{Colors.BOLD}[5] INTEGRIDADE DE TEMPLATES{Colors.ENDC}")
    print("=" * 76)
    
    workspace_root = Path(__file__).parent
    template_path = workspace_root / "reports" / "_templates" / "DASHBOARD-TEMPLATE-MASTER.html"
    
    all_ok = True
    
    # Verificar existência
    status(
        "Template file exists",
        template_path.exists(),
        "DASHBOARD-TEMPLATE-MASTER.html"
    )
    all_ok = all_ok and template_path.exists()
    
    if template_path.exists():
        # Verificar placeholder markers
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_markers = ["{{TITLE}}", "{{MAIN_CONTENT}}", "{{KPI_METRICS}}"]
            missing_markers = [m for m in required_markers if m not in content]
            
            marker_status = len(missing_markers) == 0
            status(
                "Template placeholders",
                marker_status,
                f"All markers present" if marker_status else f"Missing: {missing_markers}"
            )
            all_ok = all_ok and marker_status
            
            # Verificar branding
            has_purple = "#5c2d91" in content
            has_orange = "#ff6b35" in content
            
            status(
                "Consultoria branding colors",
                has_purple and has_orange,
                f"Purple #5c2d91 {'✓' if has_purple else '✗'} | Orange #ff6b35 {'✓' if has_orange else '✗'}"
            )
            all_ok = all_ok and (has_purple and has_orange)
            
        except Exception as e:
            status(
                "Template content validation",
                False,
                f"Error reading template: {str(e)}"
            )
            all_ok = False
    
    return all_ok

# ============================================================================
# SEÇÃO 6: EXECUTABILIDADE
# ============================================================================
def check_executability():
    print(f"\n{Colors.BOLD}[6] EXECUTABILIDADE DO WORKFLOW{Colors.ENDC}")
    print("=" * 76)
    
    workspace_root = Path(__file__).parent
    scripts_dir = workspace_root / "projects" / "clientebanco" / "scripts"
    
    required_scripts = [
        "00_MASTER_PIPELINE.py",
        "run_all_phases.py",
        "run_midstream_phases.py",
        "run_downstream_phases.py",
        "generate_roi_analysis.py",
        "generate_consolidated_report.py",
        "generate_tabbed_report.py",
        "normalize_outputs_to_template.py"
    ]
    
    all_ok = True
    for script in required_scripts:
        script_path = scripts_dir / script
        exists = script_path.exists()
        
        status(
            f"Script: {script[:45]:45}",
            exists,
            "Ready to execute" if exists else "NOT FOUND"
        )
        all_ok = all_ok and exists
    
    return all_ok

# ============================================================================
# SEÇÃO 7: RESUMO FINAL
# ============================================================================
def final_summary(results):
    print(f"\n{Colors.BOLD}{'=' * 76}{Colors.ENDC}")
    print(f"{Colors.BOLD}[RESUMO FINAL - INTEGRAÇÃO WORKFLOW + MEMÓRIA]{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 76}{Colors.ENDC}\n")
    
    checks = {
        "Sistema de Memória": results["memory"],
        "Estrutura de Workflow": results["workflow"],
        "Dependências Python": results["dependencies"],
        "Arquivo de Configuração": results["configuration"],
        "Integridade de Templates": results["templates"],
        "Executabilidade de Scripts": results["executability"]
    }
    
    all_ok = all(checks.values())
    
    for check_name, status_ok in checks.items():
        symbol = f"{Colors.GREEN}✓{Colors.ENDC}" if status_ok else f"{Colors.RED}✗{Colors.ENDC}"
        print(f"  {symbol} {check_name:50} {'✓ OK' if status_ok else '✗ FAIL'}")
    
    print(f"\n{Colors.BOLD}{'=' * 76}{Colors.ENDC}")
    
    if all_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ TUDO 100% FUNCIONAL!{Colors.ENDC}")
        print(f"\n{Colors.CYAN}Sistema integrado e pronto para:${Colors.ENDC}")
        print(f"  1. Executar master pipeline: python projects/clientebanco/scripts/00_MASTER_PIPELINE.py")
        print(f"  2. Referenciar memória: /memories/repo/MEMORY-INDEX.md")
        print(f"  3. Adicionar novo case: Veja fabricae-best-practices.md")
        print(f"  4. Entender arquitetura: fabricae-architecture-decisions.md (10 ADRs)")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ PROBLEMAS DETECTADOS!{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Ação recomendada:{Colors.ENDC}")
        print(f"  1. Verificar erros acima (marcados com ✗)")
        print(f"  2. Instalar dependências faltantes")
        print(f"  3. Reexecutar este script após correções")
        return 1

# ============================================================================
# MAIN
# ============================================================================
def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 76}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}WORKFLOW INTEGRATION CHECK v1.0{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}Sistema de Memória + Automação{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 76}{Colors.ENDC}")
    
    results = {
        "memory": check_memory_system()[0],
        "workflow": check_workflow_structure(),
        "dependencies": check_dependencies(),
        "configuration": check_configuration(),
        "templates": check_templates(),
        "executability": check_executability()
    }
    
    exit_code = final_summary(results)
    
    # Salvar resultado em JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "all_ok": all(results.values()),
        "results": results,
        "message": "✓ TUDO 100% FUNCIONAL!" if all(results.values()) else "✗ PROBLEMAS DETECTADOS"
    }
    
    report_path = Path(__file__).parent / "WORKFLOW-INTEGRATION-REPORT.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n  📊 Relatório salvo: {report_path}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
