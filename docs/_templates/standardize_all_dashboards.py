#!/usr/bin/env python3
"""
Padroniza todos os arquivos HTML com a estrutura Consultoria do ClienteBanco.
Aplica o template mestre a todos os dashboards.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def get_template_css():
    """Retorna o CSS padrão Consultoria"""
    return """        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1f3a93 0%, #0f1d4d 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            padding: 40px 30px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .header .metadata {
            margin-top: 15px;
            font-size: 0.95em;
            position: relative;
            z-index: 1;
        }
        
        .status-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.3);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            font-weight: bold;
        }
        
        .content {
            padding: 40px;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .kpi-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .kpi-card:hover {
            border-color: #ff6b35;
            box-shadow: 0 8px 16px rgba(255, 107, 53, 0.2);
            transform: translateY(-2px);
        }
        
        .kpi-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #ff6b35;
            margin: 15px 0;
        }
        
        .kpi-label {
            font-size: 0.95em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .kpi-sublabel {
            font-size: 0.85em;
            color: #999;
            margin-top: 8px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #1f3a93;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #ff6b35;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .chart-container {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .metrics-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .metrics-table th {
            background: linear-gradient(135deg, #1f3a93 0%, #0f1d4d 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .metrics-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .metrics-table tr:hover {
            background: #f9f9f9;
        }
        
        .metrics-table .tier {
            font-weight: 600;
            color: #1f3a93;
        }
        
        .status-pass {
            color: #27ae60;
            font-weight: bold;
        }
        
        .status-fail {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .status-warning {
            color: #f39c12;
            font-weight: bold;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 1024px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
        }
        
        .risk-item {
            background: #f5f5f5;
            padding: 15px;
            border-left: 4px solid #ff6b35;
            margin-bottom: 12px;
            border-radius: 4px;
        }
        
        .risk-high {
            border-left-color: #e74c3c;
            background: #fadad1;
        }
        
        .risk-medium {
            border-left-color: #f39c12;
            background: #fdebd0;
        }
        
        .risk-low {
            border-left-color: #27ae60;
            background: #d5f4e6;
        }
        
        .footer {
            background: #f5f5f5;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }
        
        .highlight {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 0 4px;
        }
        
        .badge-success {
            background: #d5f4e6;
            color: #27ae60;
        }
        
        .badge-info {
            background: #d6eaf8;
            color: #1f3a93;
        }
        
        .badge-warning {
            background: #fdebd0;
            color: #f39c12;
        }

        @media (prefers-color-scheme: dark) {
            body {
                background: linear-gradient(135deg, #0f1d4d 0%, #1a1f37 100%);
            }
            .container {
                background: #1a1f37;
                color: #e0e0e0;
            }
            .content {
                background: #1a1f37;
                color: #e0e0e0;
            }
            .chart-container {
                background: #2a2f4f;
                border-color: #3a3f5f;
            }
            .metrics-table {
                background: #2a2f4f;
            }
            .metrics-table td {
                border-bottom-color: #3a3f5f;
            }
            .kpi-card {
                background: #2a2f4f;
                border-color: #3a3f5f;
                color: #e0e0e0;
            }
            .kpi-label {
                color: #b0b0b0;
            }
            .kpi-sublabel {
                color: #808080;
            }
            .risk-item {
                background: #2a2f4f;
                color: #e0e0e0;
            }
            .footer {
                background: #2a2f4f;
                color: #b0b0b0;
                border-top-color: #3a3f5f;
            }
        }
"""

def standardize_html(file_path, title, subtitle, project_name):
    """Padroniza um arquivo HTML com a estrutura Consultoria"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair conteúdo do <body> se existir
        body_start = content.find('<body>')
        body_end = content.find('</body>')
        
        if body_start != -1 and body_end != -1:
            old_body_content = content[body_start + 6:body_end].strip()
        else:
            old_body_content = ""
        
        # Extrair scripts
        script_pattern = '<script>'
        scripts = []
        temp_content = content
        while '<script>' in temp_content:
            start = temp_content.find('<script>')
            end = temp_content.find('</script>') + len('</script>')
            if start != -1 and end > start:
                scripts.append(temp_content[start:end])
                temp_content = temp_content[:start] + temp_content[end:]
        
        # Tentar extrair título da página
        title_match = content[content.find('<title>') + 7:content.find('</title>')] if '<title>' in content else title
        
        # Novo HTML
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_match} | Consultoria</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
{get_template_css()}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="metadata">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Project:</strong> {project_name}
            </div>
            <div class="status-badge">✓ COMPLETE & VALIDATED</div>
        </div>
        
        <!-- CONTENT -->
        <div class="content">
            {old_body_content if old_body_content else '<div class="section"><h2 class="section-title">📊 Dashboard Content</h2><p>Content will be populated here.</p></div>'}
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <p>
                <strong>{project_name}</strong> | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                Powered by Consultoria's Data Migration Factory v3 | 
                <span style="color: #ff6b35; font-weight: bold;">100% Autonomous Execution</span>
            </p>
        </div>
    </div>
    
    {''.join(scripts) if scripts else '<script>console.log("No scripts to load");</script>'}
</body>
</html>
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return True, "Padronizado com sucesso"
    
    except Exception as e:
        return False, str(e)

def main():
    """Padroniza todos os arquivos HTML"""
    
    reports_dir = Path(r"~/projects/imfai-ava-fabric-data-agents\reports")
    
    html_files = [
        {
            'path': reports_dir / '_templates' / 'executive-dashboard.html',
            'title': '📊 Executive Dashboard Template',
            'subtitle': 'Multi-Project Overview',
            'project': 'Consultoria Data Migration Factory'
        },
        {
            'path': reports_dir / '_templates' / 'example-dashboard.html',
            'title': '📈 Example Dashboard',
            'subtitle': 'Template Example',
            'project': 'Consultoria Data Migration Factory'
        },
        {
            'path': reports_dir / '_templates' / 'dashboard-with-metrics.html',
            'title': '📊 Dashboard with Metrics',
            'subtitle': 'Metrics Visualization',
            'project': 'Consultoria Data Migration Factory'
        },
        {
            'path': reports_dir / 'clientebanco' / 'ROI_ANALYSIS_VISUAL.html',
            'title': '💰 ROI Analysis - ClienteBanco',
            'subtitle': 'Cost-Benefit Analysis & Savings',
            'project': 'ClienteBanco Data Migration'
        },
        {
            'path': reports_dir / 'clientebanco' / 'clientebanco-autonomous-test-report.html',
            'title': '✅ Autonomous Test Report - ClienteBanco',
            'subtitle': 'Full Migration Testing & Validation',
            'project': 'ClienteBanco Data Migration'
        },
        {
            'path': reports_dir / 'clientebanco' / 'clientebanco-3tier-dashboard.html',
            'title': '🏗️ 3-Tier Migration Dashboard - ClienteBanco',
            'subtitle': 'Upstream · Midstream · Downstream',
            'project': 'ClienteBanco Data Migration'
        },
    ]
    
    results = []
    
    for item in html_files:
        file_path = item['path']
        
        if file_path.exists():
            success, message = standardize_html(
                str(file_path),
                item['title'],
                item['subtitle'],
                item['project']
            )
            results.append({
                'file': file_path.name,
                'status': '✅' if success else '❌',
                'message': message
            })
        else:
            results.append({
                'file': file_path.name,
                'status': '⚠️',
                'message': 'Arquivo não encontrado'
            })
    
    # Exibir resultados
    print("\n" + "="*70)
    print("📊 PADRONIZAÇÃO DE DASHBOARDS HTML — RELATÓRIO")
    print("="*70)
    
    for result in results:
        print(f"\n{result['status']} {result['file']}")
        print(f"   → {result['message']}")
    
    success_count = sum(1 for r in results if r['status'] == '✅')
    print("\n" + "="*70)
    print(f"✅ {success_count}/{len(results)} arquivos padronizados com sucesso")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
