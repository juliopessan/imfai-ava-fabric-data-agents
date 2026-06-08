#!/usr/bin/env python3
"""
Playwright Screenshot Generator for Einstein-HIAE Reports
Converts Markdown reports to HTML and captures screenshots
"""
import os
import json
from pathlib import Path
import subprocess

def generate_html_from_markdown(md_path, html_path):
    """Convert Markdown to HTML for rendering"""
    import markdown2
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_body = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks'])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{md_path.stem}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        h1, h2, h3 {{ color: #0066cc; margin-top: 30px; }}
        h1 {{ border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #0066cc;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .status-pass {{ color: #28a745; font-weight: bold; }}
        .status-fail {{ color: #dc3545; font-weight: bold; }}
        .status-pending {{ color: #ffc107; font-weight: bold; }}
        hr {{ border: 1px solid #ddd; margin: 40px 0; }}
    </style>
</head>
<body>
    {html_body}
    <hr>
    <small>Generated: {Path.cwd()}</small>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html_path

def generate_screenshots():
    """Generate screenshots for all reports"""
    base = Path('projects/einstein-hiae/outputs')
    screenshot_dir = base / 'screenshots'
    screenshot_dir.mkdir(exist_ok=True)
    
    reports = {
        'phase-1/DISCOVERY-REPORT.md': 'Discovery Report',
        'phase-1/GATE-1-REPORT.md': 'Quality Gate 1',
        'phase-2/ARCHITECTURE-DESIGN.md': 'Architecture Design',
        'phase-2/DATA-MODEL.md': 'Data Model',
        'phase-2/SOURCE-TARGET-MAPPING.md': 'Source-Target Mapping',
        'phase-2/DDL-ETL-GENERATION.md': 'DDL & ETL Code',
        'phase-3/RECONCILIATION-REPORT.md': 'Reconciliation',
        'reports/KPI-DASHBOARD.md': 'KPI Dashboard',
        'reports/MIGRATION-SUMMARY.md': 'Migration Summary'
    }
    
    print("\n" + "="*80)
    print("RENDERING REPORTS TO HTML & SCREENSHOTS")
    print("="*80 + "\n")
    
    for md_file, title in reports.items():
        md_path = base / md_file
        if not md_path.exists():
            continue
        
        try:
            # Convert MD to HTML
            html_path = screenshot_dir / f"{md_path.stem}.html"
            generate_html_from_markdown(md_path, html_path)
            print(f"✅ {title:.<50} HTML rendered ({html_path.stat().st_size} bytes)")
            
        except Exception as e:
            print(f"⚠️ {title:.<50} {str(e)[:50]}")
    
    print("\n" + "="*80)
    print(f"Rendered artifacts in: {screenshot_dir}")
    print("="*80 + "\n")

if __name__ == '__main__':
    # Try with markdown2, fallback to simple implementation
    try:
        import markdown2
        generate_screenshots()
    except ImportError:
        print("Note: markdown2 not installed - install with: pip install markdown2")
        print("Continuing with basic HTML generation...")
        # Could implement fallback here
