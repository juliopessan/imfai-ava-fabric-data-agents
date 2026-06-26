#!/usr/bin/env python3
"""
📊 Dashboard Consolidation Script

Consolida KPIs de dashboards de projeto no Executive Unified Dashboard.
Extrai métricas principais e atualiza a visão gerencial automaticamente.

Uso:
    python consolidate_dashboards.py [--projects Financeiro,reference] [--dry-run]

Exemplo:
    python consolidate_dashboards.py
    python consolidate_dashboards.py --projects Financeiro --dry-run
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

# ===== CONFIGURATION =====

PROJECTS_CONFIG = {
    "Financeiro": {
        "source": "reports/Financeiro/Financeiro-executive-dashboard.html",
        "name": "🏦 Financeiro",
        "description": "Migração Cloudera → Databricks",
        "icon": "🏢",
    },
    "reference": {
        "source": "reports/reference/reference-executive-dashboard.html",
        "name": "🏥 Reference-Sa�de",
        "description": "SQL Server → Microsoft Fabric",
        "icon": "🏥",
    },
}

EXECUTIVE_DASHBOARD = "reports/_templates/DASHBOARD-EXECUTIVE-UNIFIED.html"

# ===== EXTRACTION FUNCTIONS =====

def extract_kpi_value(html: str, label_pattern: str) -> Tuple[str, bool]:
    """
    Extrai um valor KPI procurando pelo padrão de label.
    
    Procura por:
        <div class="kpi-value">VALUE</div>
        <div class="kpi-label">LABEL</div>
    
    Args:
        html: Conteúdo HTML
        label_pattern: Padrão regex para encontrar o label
    
    Returns:
        (valor, encontrado)
    """
    pattern = rf'<div class="kpi-value">(.+?)</div>\s*<div class="kpi-label">.*?{label_pattern}'
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    
    if match and match.group(1):
        return match.group(1).strip(), True
    return "N/A", False

def extract_project_kpis(html_file: str) -> Dict[str, str]:
    """
    Extrai KPIs principais de um dashboard de projeto.
    
    Args:
        html_file: Caminho do arquivo HTML
    
    Returns:
        Dict com chaves: completeness, quality, entities, rows, artifacts, phase, status
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"   ⚠️  Arquivo não encontrado: {html_file}")
        return None
    
    kpis = {}
    
    # Completeness (procura em tabelas ou KPI cards)
    # Procura por: <td>98.7%</td> que vem após "Completeness" ou "Overall Completion"
    match = re.search(
        r'<(?:td|div)[^>]*>.*?[Cc]omple(?:teness|tion).*?</(?:td|div)>\s*<(?:td|div)[^>]*>([^<]+)</(?:td|div)>|'
        r'<(?:td|div)[^>]*>([^<]*(?:98|97|96|95|94|93|92|91|90|89|88)\.\d%[^<]*)</(?:td|div)>',
        html
    )
    if match:
        val = (match.group(1) or match.group(2) or "").strip()
        kpis['completeness'] = val if val and val != 'N/A' else "N/A"
    else:
        kpis['completeness'] = "N/A"
    
    # Quality Score (procura em tabelas ou KPI cards)
    # Procura por: <td>0.92/1.00</td> que vem após "Quality"
    match = re.search(
        r'<td><strong>[Qq]uality\s[^<]*</strong></td>\s*<td>([\d.]+(?:/[\d.]+)?)</td>',
        html
    )
    if match:
        val = match.group(1).strip() if match.group(1) else "N/A"
        kpis['quality'] = val if val and val != 'N/A' else "N/A"
    else:
        kpis['quality'] = "N/A"
    
    # Entities/Tables (procura em KPI cards)
    val, found = extract_kpi_value(html, r'[Ee]ntit|[Tt]able')
    kpis['entities'] = val if found else "N/A"
    
    # Rows/Data (procura em KPI cards)
    val, found = extract_kpi_value(html, r'[Ll]inhas|[Rr]ows')
    kpis['rows'] = val if found else "N/A"
    
    # Artifacts (procura em KPI cards ou tabelas)
    val, found = extract_kpi_value(html, r'[Aa]rtifact')
    if not found:
        # Procura em tabelas
        match = re.search(
            r'<(?:td|div)[^>]*>.*?[Aa]rtifact.*?</(?:td|div)>\s*<(?:td|div)[^>]*>([^<]+)</(?:td|div)>',
            html
        )
        val = match.group(1).strip() if match and match.group(1) else "N/A"
    kpis['artifacts'] = val
    
    # Phase (busca em subtitle ou metadata)
    phase_match = re.search(
        r'<div class="project-description">(.*?)</div>|<div class="subtitle">(.*?)</div>|<div class="kpi-sublabel">(.*?)[Pp]hase',
        html
    )
    kpis['phase'] = (phase_match.group(1) or phase_match.group(2) or phase_match.group(3) or "Unknown").strip() if phase_match else "Unknown"
    
    # Status (procura por badges ou metadata)
    if "Completo" in html or "Complete" in html or "COMPLETE" in html:
        kpis['status'] = "✓ Completo"
    elif "Em Progresso" in html or "In Progress" in html or "PROGRESS" in html:
        kpis['status'] = "⏱ Em Progresso"
    elif "Discovery" in html or "DISCOVERY" in html:
        kpis['status'] = "⏱ Discovery"
    else:
        kpis['status'] = "? Desconhecido"
    
    return kpis

def generate_project_card_html(project_key: str, project_config: Dict, kpis: Dict) -> str:
    """
    Gera HTML de card do projeto com KPIs consolidados.
    
    Args:
        project_key: ID do projeto (Financeiro, reference)
        project_config: Configuração do projeto
        kpis: KPIs extraídos
    
    Returns:
        HTML do card
    """
    if kpis is None:
        return f"<!-- Projeto {project_key}: SKIPPED (arquivo não encontrado) -->"
    
    # Determinar cor/status
    quality_val = kpis.get('quality', '0.85').split('/')[0]
    try:
        quality_num = float(quality_val)
        status_class = "active" if quality_num >= 0.90 else "inprogress" if quality_num >= 0.80 else "pending"
    except:
        status_class = "inprogress"
    
    completeness = kpis.get('completeness', 'N/A')
    
    html = f"""
                <!-- Project: {project_key} -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-name">{project_config['name']}</div>
                        <div class="project-description">{project_config['description']}</div>
                    </div>
                    <div class="project-content">
                        <div class="project-kpi">
                            <div class="project-kpi-label">Completude</div>
                            <div class="project-kpi-value">{completeness}</div>
                        </div>
                        <div class="project-kpi">
                            <div class="project-kpi-label">Qualidade</div>
                            <div class="project-kpi-value">{kpis.get('quality', 'N/A')}</div>
                        </div>
                        <div class="project-kpi">
                            <div class="project-kpi-label">Entidades/Tabelas</div>
                            <div class="project-kpi-value">{kpis.get('entities', 'N/A')}</div>
                        </div>
                        <div class="project-kpi">
                            <div class="project-kpi-label">Dados Carregados</div>
                            <div class="project-kpi-value">{kpis.get('rows', 'N/A')}</div>
                        </div>
                        <div class="project-kpi">
                            <div class="project-kpi-label">Artefatos</div>
                            <div class="project-kpi-value">{kpis.get('artifacts', 'N/A')}</div>
                        </div>
                        <div class="project-status">
                            <div class="status-badge {status_class}">→ {kpis.get('phase', 'Unknown')}</div>
                        </div>
                    </div>
                </div>
"""
    return html

def calculate_global_metrics(all_kpis: Dict[str, Dict]) -> Dict[str, str]:
    """
    Calcula métricas globais consolidadas.
    
    Args:
        all_kpis: Dict com KPIs de todos os projetos
    
    Returns:
        Dict com métricas globais
    """
    metrics = {
        'active_projects': sum(1 for kpis in all_kpis.values() if kpis is not None),
        'avg_completeness': 'N/A',
        'avg_quality': 'N/A',
    }
    
    # Calcular médias
    completeness_vals = []
    quality_vals = []
    
    for kpis in all_kpis.values():
        if kpis is None:
            continue
        
        # Parse completeness (ex: "98.7%")
        try:
            comp_str = kpis.get('completeness', '').replace('%', '').strip()
            if comp_str and comp_str != 'N/A':
                completeness_vals.append(float(comp_str))
        except:
            pass
        
        # Parse quality (ex: "0.92/1.00" ou "0.92")
        try:
            qual_str = kpis.get('quality', '').split('/')[0].strip()
            if qual_str and qual_str != 'N/A':
                quality_vals.append(float(qual_str))
        except:
            pass
    
    if completeness_vals:
        avg_comp = sum(completeness_vals) / len(completeness_vals)
        metrics['avg_completeness'] = f"{avg_comp:.1f}%"
    
    if quality_vals:
        avg_qual = sum(quality_vals) / len(quality_vals)
        metrics['avg_quality'] = f"{avg_qual:.2f}"
    
    return metrics

def update_executive_dashboard(all_kpis: Dict[str, Dict], projects_config: Dict, dry_run: bool = False):
    """
    Atualiza dashboard executivo com KPIs consolidados.
    
    Args:
        all_kpis: KPIs de todos os projetos
        projects_config: Configuração de projetos
        dry_run: Se True, não escreve arquivo
    """
    try:
        with open(EXECUTIVE_DASHBOARD, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"   ❌ Dashboard executivo não encontrado: {EXECUTIVE_DASHBOARD}")
        return False
    
    # Gerar cards dos projetos
    project_cards = ""
    for project_key, project_config in projects_config.items():
        kpis = all_kpis.get(project_key)
        card_html = generate_project_card_html(project_key, project_config, kpis)
        project_cards += card_html
    
    # Calcular métricas globais
    global_metrics = calculate_global_metrics(all_kpis)
    
    # Substituir placeholder de projetos
    # (procura por primeiro card de projeto e substitui até o último)
    pattern = r'(<!-- Project:.*?</div>\s*</div>)'
    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, project_cards.strip(), html, flags=re.DOTALL)
    
    # Atualizar timestamp
    now = datetime.now().strftime("%d de %B, %Y").replace('January', 'Janeiro').replace('February', 'Fevereiro').replace('March', 'Março').replace('April', 'Abril').replace('May', 'Maio').replace('June', 'Junho').replace('July', 'Julho').replace('August', 'Agosto').replace('September', 'Setembro').replace('October', 'Outubro').replace('November', 'Novembro').replace('December', 'Dezembro')
    html = re.sub(
        r'<span class="metadata-value">\d+ de \w+, \d+</span>',
        f'<span class="metadata-value">{now}</span>',
        html
    )
    
    # Atualizar métricas globais
    html = re.sub(
        r'<div class="kpi-value">\d+(?:\.\d+)?%?</div>\s*<div class="kpi-label">[^<]*Completude',
        f'<div class="kpi-value">{global_metrics["avg_completeness"]}</div>\n                    <div class="kpi-label">Completude Média',
        html
    )
    
    if not dry_run:
        with open(EXECUTIVE_DASHBOARD, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    else:
        print("\n[DRY-RUN] Não foi escrito arquivo")
        return True

# ===== MAIN =====

def main():
    print("=" * 70)
    print("📊 CONSOLIDATE DASHBOARDS — KPI Extraction & Aggregation")
    print("=" * 70)
    
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    projects_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith("--projects="):
            projects_filter = arg.split("=", 1)[1].split(",")
            break
    
    # Filter projects
    if projects_filter:
        projects = {k: v for k, v in PROJECTS_CONFIG.items() if k in projects_filter}
    else:
        projects = PROJECTS_CONFIG
    
    print(f"\n🔍 Extraindo KPIs de {len(projects)} projeto(s)...\n")
    
    all_kpis = {}
    
    for project_key, project_config in projects.items():
        print(f"   📁 {project_config['name']}")
        source_file = project_config['source']
        
        # Check if file exists
        if not Path(source_file).exists():
            print(f"      ⚠️  Arquivo não encontrado: {source_file}")
            all_kpis[project_key] = None
            continue
        
        # Extract KPIs
        kpis = extract_project_kpis(source_file)
        all_kpis[project_key] = kpis
        
        # Print results
        if kpis:
            print(f"      ✓ Completude: {kpis.get('completeness', 'N/A')}")
            print(f"      ✓ Qualidade: {kpis.get('quality', 'N/A')}")
            print(f"      ✓ Status: {kpis.get('status', 'N/A')}")
    
    # Calculate global metrics
    print(f"\n📊 Calculando métricas globais...")
    global_metrics = calculate_global_metrics(all_kpis)
    print(f"   ✓ Projetos Ativos: {global_metrics['active_projects']}")
    print(f"   ✓ Completude Média: {global_metrics['avg_completeness']}")
    print(f"   ✓ Qualidade Média: {global_metrics['avg_quality']}")
    
    # Update executive dashboard
    print(f"\n🎯 Atualizando Dashboard Executivo...")
    
    if dry_run:
        print("   [DRY-RUN] Nenhum arquivo será modificado\n")
    
    success = update_executive_dashboard(all_kpis, projects, dry_run=dry_run)
    
    if success:
        print(f"   ✅ Dashboard Executivo Atualizado" if not dry_run else "   ✓ [DRY-RUN] Validação OK")
        print(f"\n📊 Summary JSON:")
        print(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'projects': all_kpis,
            'global_metrics': global_metrics,
            'executive_dashboard': EXECUTIVE_DASHBOARD
        }, indent=2, ensure_ascii=False))
        return 0
    else:
        print(f"   ❌ Erro ao atualizar dashboard")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
