#!/usr/bin/env python3
"""
Playwright Screenshot & Visual Documentation Generator
Captura screenshots de estágios da migração e gera relatório Before/After

Instalação:
  pip install playwright
  playwright install chromium
  
Uso:
  python screenshots_generator.py --project clientebanco --stage upstream
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright, Page
import argparse


class PlaywrightScreenshotGenerator:
    """Gerador de screenshots e documentação visual"""
    
    def __init__(self, project_name: str = "clientebanco", output_dir: str = "reports/screenshots"):
        self.project_name = project_name
        self.output_dir = Path(output_dir) / project_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots: List[Dict] = []
        self.metadata = {
            "project": project_name,
            "generated": datetime.now().isoformat(),
            "screenshots": []
        }
    
    async def capture_dashboard(self, dashboard_url: str, stage_name: str, label: str):
        """Captura screenshot de um dashboard"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            
            try:
                print(f"📸 Capturando {stage_name}: {label}...")
                await page.goto(dashboard_url, wait_until="networkidle")
                
                # Aguardar renderização completa
                await page.wait_for_timeout(2000)
                
                # Screenshot completo
                screenshot_path = self.output_dir / f"{stage_name}_{label.replace(' ', '_').lower()}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                
                # Metadados
                screenshot_info = {
                    "stage": stage_name,
                    "label": label,
                    "file": str(screenshot_path.name),
                    "timestamp": datetime.now().isoformat(),
                    "url": dashboard_url,
                    "viewport": "1920x1080"
                }
                self.screenshots.append(screenshot_info)
                self.metadata["screenshots"].append(screenshot_info)
                
                print(f"✅ Salvo: {screenshot_path.name}")
                
            except Exception as e:
                print(f"❌ Erro ao capturar {stage_name}: {str(e)}")
            
            finally:
                await browser.close()
    
    async def capture_multiple_dashboards(self, dashboards: List[Dict]):
        """Captura múltiplos dashboards em paralelo"""
        tasks = []
        
        for dashboard in dashboards:
            task = self.capture_dashboard(
                dashboard["url"],
                dashboard["stage"],
                dashboard["label"]
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    def save_metadata(self):
        """Salva metadados em JSON"""
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"💾 Metadados salvos: {metadata_path}")
    
    def generate_comparison_html(self):
        """Gera HTML com comparação Before/After"""
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Before & After - {self.project_name} | Consultoria</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f9f9f9;
            color: #333;
            padding: 24px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .header {{
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            padding: 48px 24px;
            color: white;
            border-radius: 12px;
            margin-bottom: 48px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.95;
            margin-bottom: 24px;
        }}
        
        .header .metadata {{
            font-size: 0.95em;
            opacity: 0.85;
        }}
        
        .section {{
            margin-bottom: 48px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #1f3a93;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 3px solid #ff6b35;
            font-weight: 700;
        }}
        
        .comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        
        .comparison-item {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            transition: all 0.3s ease;
        }}
        
        .comparison-item:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
            transform: translateY(-2px);
        }}
        
        .comparison-label {{
            background: linear-gradient(135deg, #1f3a93 0%, #0f1d4d 100%);
            color: white;
            padding: 16px 24px;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .comparison-label.before {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }}
        
        .comparison-label.after {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        }}
        
        .screenshot-container {{
            padding: 16px;
            background: #f9f9f9;
            position: relative;
        }}
        
        .screenshot-container img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
            display: block;
            max-height: 600px;
            object-fit: cover;
        }}
        
        .stage-info {{
            padding: 16px 24px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.9em;
            color: #666;
        }}
        
        .stage-label {{
            display: inline-block;
            background: #ff6b35;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 48px;
        }}
        
        .metric-card {{
            background: white;
            padding: 24px;
            border-radius: 8px;
            border-left: 4px solid #ff6b35;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}
        
        .metric-value {{
            font-size: 2.4em;
            font-weight: 700;
            color: #ff6b35;
            margin: 12px 0;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        .footer {{
            background: #f9f9f9;
            padding: 24px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 48px;
        }}
        
        .footer strong {{
            color: #666;
            font-weight: 600;
        }}
        
        @media (max-width: 1024px) {{
            .comparison {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>📊 Before & After — Visual Migration Documentation</h1>
            <div class="subtitle">Progresso Técnico da Migração</div>
            <div class="metadata">
                <strong>Projeto:</strong> {self.project_name.upper()}<br>
                <strong>Gerado:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Total de Screenshots:</strong> {len(self.screenshots)}
            </div>
        </div>
        
        <!-- METRICS -->
        <div class="section">
            <h2 class="section-title">📈 Resumo de Documentação</h2>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Total de Etapas</div>
                    <div class="metric-value">{len(set(s['stage'] for s in self.screenshots))}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Screenshots Capturados</div>
                    <div class="metric-value">{len(self.screenshots)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Data de Geração</div>
                    <div class="metric-value" style="font-size: 1.2em;">{datetime.now().strftime('%d/%m')}</div>
                </div>
            </div>
        </div>
        
        <!-- COMPARISONS -->
        <div class="section">
            <h2 class="section-title">🔄 Comparação: Antes × Depois</h2>
"""
        
        # Agrupar screenshots por estágio
        stages = {}
        for ss in self.screenshots:
            stage = ss['stage']
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(ss)
        
        # Gerar comparações
        for stage, screenshots in stages.items():
            html_content += f"""
            <div style="margin-bottom: 48px;">
                <h3 style="font-size: 1.4em; color: #1f3a93; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35;">
                    🔹 Etapa: {stage.upper()}
                </h3>
"""
            
            # Mostrar screenshots em pares ou individuais
            for i, ss in enumerate(screenshots):
                html_content += f"""
                <div class="comparison-item" style="margin-bottom: 20px;">
                    <div class="comparison-label after">
                        📸 {ss['label']}
                    </div>
                    <div class="screenshot-container">
                        <img src="{ss['file']}" alt="{ss['label']}" />
                    </div>
                    <div class="stage-info">
                        <div class="stage-label">{ss['stage']}</div>
                        <div style="margin-top: 8px;">
                            <strong>Capturado:</strong> {ss['timestamp']}<br>
                            <strong>Viewport:</strong> {ss['viewport']}
                        </div>
                    </div>
                </div>
"""
            
            html_content += "</div>"
        
        html_content += """
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <strong>Consultoria Data Migration Factory v3</strong> — Visual Documentation Engine<br>
            Esta documentação foi gerada automaticamente utilizando Playwright + Orchestration Agents
        </div>
    </div>
</body>
</html>
"""
        
        # Salvar HTML
        html_path = self.output_dir / "before_after_comparison.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Relatório gerado: {html_path}")
        return str(html_path)


def run_screenshot_capture(project: str = "clientebanco", stage: str = "upstream"):
    """Executa captura de screenshots"""
    
    # URLs de dashboards para capturar
    dashboards_to_capture = {
        "clientebanco": {
            "upstream": [
                {
                    "url": "file:///path/to/imfai-ava-fabric-data-agents/reports/clientebanco/clientebanco-executive-dashboard.html",
                    "stage": "upstream",
                    "label": "Executive Dashboard - Estado Inicial"
                },
                {
                    "url": "file:///path/to/imfai-ava-fabric-data-agents/reports/clientebanco/ROI_ANALYSIS_VISUAL.html",
                    "stage": "upstream",
                    "label": "ROI Analysis - Antes da Migração"
                }
            ],
            "midstream": [
                {
                    "url": "file:///path/to/imfai-ava-fabric-data-agents/reports/clientebanco/clientebanco-autonomous-test-report.html",
                    "stage": "midstream",
                    "label": "Test Report - Validações em Progresso"
                }
            ],
            "downstream": [
                {
                    "url": "file:///path/to/imfai-ava-fabric-data-agents/reports/clientebanco/clientebanco-3tier-dashboard.html",
                    "stage": "downstream",
                    "label": "3-Tier Dashboard - Estado Final"
                }
            ]
        }
    }
    
    # Validar projeto
    if project not in dashboards_to_capture:
        print(f"❌ Projeto '{project}' não encontrado. Disponíveis: {list(dashboards_to_capture.keys())}")
        return
    
    # Validar estágio
    if stage not in dashboards_to_capture[project]:
        print(f"❌ Etapa '{stage}' não encontrada. Disponíveis: {list(dashboards_to_capture[project].keys())}")
        return
    
    # Capturar
    generator = PlaywrightScreenshotGenerator(project)
    
    dashboards = dashboards_to_capture[project][stage]
    print(f"\n🎬 Iniciando captura de {len(dashboards)} screenshots...")
    print(f"📁 Projeto: {project} | Etapa: {stage}\n")
    
    asyncio.run(generator.capture_multiple_dashboards(dashboards))
    
    # Salvar metadados
    generator.save_metadata()
    
    # Gerar HTML
    html_path = generator.generate_comparison_html()
    
    print(f"\n✅ Captura concluída!")
    print(f"📸 Screenshots salvos em: {generator.output_dir}")
    print(f"🌐 Abra no navegador: {html_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Capturar screenshots de dashboards para documentação visual"
    )
    parser.add_argument("--project", default="clientebanco", help="Nome do projeto")
    parser.add_argument("--stage", default="upstream", help="Etapa: upstream, midstream, downstream")
    
    args = parser.parse_args()
    
    run_screenshot_capture(args.project, args.stage)
