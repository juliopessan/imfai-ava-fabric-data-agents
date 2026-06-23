#!/usr/bin/env python3
"""
Dashboard Standardizer — Applies Consultoria Golden Standard design to all dashboards
Mantém conteúdo único, aplica design padrão CSS + HTML structure
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Padrão Ouro CSS
GOLDEN_STYLE = """
:root {
    --ava-orange: #FF5800;
    --ava-magenta: #CE0569;
    --ava-red: #C80000;
    --ava-gold: #FFB314;
    --ava-purple: #890078;
    --ava-green: #47800A;
    --ava-dark: #2D2D2D;
    --ava-gray: #595959;
    --ava-light: #E7E6E6;
    --bg-body: #FAFAFA;
    --text-primary: #1A1A1A;
    --text-secondary: #5A5A5A;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: var(--bg-body);
    color: var(--text-primary);
    line-height: 1.6;
}

/* ===== HEADER ===== */
.header {
    background: linear-gradient(135deg, #1a0a00 0%, #3d1700 30%, var(--ava-orange) 100%);
    padding: 48px 56px;
    color: white;
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: -80px;
    right: -40px;
    width: 550px;
    height: 550px;
    background: radial-gradient(circle, rgba(255, 88, 0, 0.25) 0%, transparent 55%);
    border-radius: 50%;
}

.header h1 {
    font-family: 'Segoe UI Black', 'Segoe UI', sans-serif;
    font-size: 36px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 10px;
    position: relative;
    z-index: 1;
}

.header .subtitle {
    font-size: 15px;
    opacity: 0.7;
    position: relative;
    z-index: 1;
    max-width: 640px;
}

.header .metadata {
    margin-top: 15px;
    font-size: 0.95em;
    position: relative;
    z-index: 1;
}

.status-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 8px 16px;
    border-radius: 20px;
    margin-top: 10px;
    font-weight: bold;
    font-size: 12px;
}

/* ===== MAIN ===== */
.main {
    max-width: 1520px;
    margin: 0 auto;
    padding: 44px;
}

.content {
    padding: 44px;
    max-width: 1520px;
    margin: 0 auto;
}

.section-title {
    font-family: 'Segoe UI Black', 'Segoe UI', sans-serif;
    font-size: 20px;
    font-weight: 900;
    color: var(--ava-dark);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(to right, var(--ava-orange), transparent);
}

/* ===== KPI GRID ===== */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
    gap: 18px;
    margin-bottom: 48px;
}

.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05);
    border-top: 4px solid var(--ava-light);
    transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 28px rgba(0, 0, 0, 0.09);
}

.kpi-card.c-orange { border-top-color: var(--ava-orange); }
.kpi-card.c-magenta { border-top-color: var(--ava-magenta); }
.kpi-card.c-red { border-top-color: var(--ava-red); }
.kpi-card.c-gold { border-top-color: var(--ava-gold); }
.kpi-card.c-purple { border-top-color: var(--ava-purple); }
.kpi-card.c-green { border-top-color: var(--ava-green); }
.kpi-card.c-blue { border-top-color: #0057B8; }
.kpi-card.c-dark { border-top-color: var(--ava-dark); }
.kpi-card.c-teal { border-top-color: #05A870; }

.kpi-value {
    font-family: 'Segoe UI Black', 'Segoe UI', sans-serif;
    font-size: 42px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 5px;
}

.kpi-card.c-orange .kpi-value { color: var(--ava-orange); }
.kpi-card.c-magenta .kpi-value { color: var(--ava-magenta); }
.kpi-card.c-red .kpi-value { color: var(--ava-red); }
.kpi-card.c-purple .kpi-value { color: var(--ava-purple); }
.kpi-card.c-green .kpi-value { color: var(--ava-green); }
.kpi-card.c-blue .kpi-value { color: #0057B8; }

.kpi-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 700;
}

.kpi-sub {
    font-size: 10px;
    color: #999;
    margin-top: 3px;
}

/* ===== MERMAID ===== */
.mermaid-section {
    margin-bottom: 48px;
    background: white;
    border-radius: 18px;
    padding: 36px 28px;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05);
    overflow-x: auto;
}

.mermaid-section .mermaid {
    display: flex;
    justify-content: center;
}

/* ===== PHASE BLOCKS ===== */
.phase-block {
    background: white;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.phase-block-header {
    padding: 18px 26px;
    color: white;
    display: flex;
    align-items: center;
    gap: 14px;
    cursor: pointer;
    user-select: none;
}

.phase-content {
    padding: 0 26px 26px;
}

/* ===== TABLES ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

table thead {
    background: linear-gradient(135deg, var(--ava-purple), var(--ava-magenta));
    color: white;
}

table th {
    padding: 16px;
    text-align: left;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

table td {
    padding: 14px 16px;
    border-bottom: 1px solid #EEE;
}

table tbody tr:hover {
    background: #F8F8F8;
}

/* ===== CHART CONTAINER ===== */
.chart-container {
    background: white;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05);
}

/* ===== FOOTER ===== */
.footer {
    background: linear-gradient(135deg, #1a0a00, #3d1700, var(--ava-orange));
    color: white;
    text-align: center;
    padding: 32px;
    font-size: 12px;
}

.footer .brand-color {
    color: var(--ava-gold);
}

.footer .sub {
    opacity: 0.5;
    font-size: 10px;
    margin-top: 6px;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .header {
        padding: 32px 24px;
    }

    .header h1 {
        font-size: 28px;
    }

    .main, .content {
        padding: 24px;
    }

    .kpi-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
    }

    table {
        font-size: 12px;
    }

    table th, table td {
        padding: 10px 12px;
    }
}
"""

def extract_body_content(html_content):
    """Extrai conteúdo do body, removendo tags head"""
    # Encontra o conteúdo entre <body> e </body>
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_title(html_content):
    """Extrai title do documento"""
    match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Dashboard"

def create_golden_html(title, body_content):
    """Cria HTML com padrão ouro"""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Consultoria DMF</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
{GOLDEN_STYLE}
    </style>
</head>
<body>
    <!-- ========== HEADER ========== -->
    <div class="header">
        <div class="header-content">
            <h1>📊 {title}</h1>
            <p>Consultoria Data Migration Factory — {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>

    <!-- ========== MAIN CONTENT ========== -->
    <div class="main">
        {body_content}
    </div>

    <!-- ========== FOOTER ========== -->
    <div class="footer">
        <strong class="brand-color">DMF</strong> &mdash; Data Migration Factory<br>
        <span class="sub">Powered by DMF Fabric Agents &middot; Consultoria</span>
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '#FFF5EE',
                primaryBorderColor: '#FF5800',
                primaryTextColor: '#2D2D2D',
                lineColor: '#FFB314',
                secondaryColor: '#F5E6FF',
                tertiaryColor: '#E8F5E0'
            }},
            flowchart: {{
                curve: 'basis',
                nodeSpacing: 25,
                rankSpacing: 40
            }}
        }});

        function togglePhase(el) {{
            el.parentElement.classList.toggle('collapsed');
        }}
    </script>
</body>
</html>"""

def process_dashboard(file_path):
    """Processa um dashboard e aplica padrão ouro"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_html = f.read()
        
        title = extract_title(original_html)
        body_content = extract_body_content(original_html)
        
        # Se não achou body_content, usa o arquivo inteiro como conteúdo
        if not body_content:
            body_content = original_html
        
        golden_html = create_golden_html(title, body_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(golden_html)
        
        return True, f"✅ {file_path} — Padrão aplicado"
    except Exception as e:
        return False, f"❌ {file_path} — Erro: {str(e)}"

def main():
    """Aplica padrão ouro a todos os dashboards"""
    base_path = Path("reports")
    
    dashboards = [
        "clientebanco/clientebanco-autonomous-test-report.html",
        "clientebanco/clientebanco-3tier-dashboard.html",
        "clientebanco/clientebanco-executive-dashboard.html",
        "clientebanco/ROI_ANALYSIS_VISUAL.html",
        "_templates/DASHBOARD-TEMPLATE-ORANGE-DNA.html",
        "_templates/DASHBOARD-ENTERPRISE-STANDARD.html",
        "_templates/dashboard-with-metrics.html",
        "_templates/example-dashboard.html",
        "_templates/executive-dashboard.html",
    ]
    
    print("🎨 Consultoria Golden Standard Dashboard Standardizer")
    print("=" * 60)
    
    results = []
    for dash in dashboards:
        full_path = base_path / dash
        if full_path.exists():
            success, msg = process_dashboard(str(full_path))
            results.append(msg)
            print(msg)
        else:
            print(f"⚠️  {full_path} — Não encontrado")
    
    print("=" * 60)
    print(f"✅ Processamento concluído: {sum(1 for r in results if r.startswith('✅'))} sucesso(s)")

if __name__ == "__main__":
    main()
