#!/usr/bin/env python3
"""
Report Generator from Avanade Template
Generates professional reports based on REPORT-TEMPLATE-AVANADE-STANDARD.html
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def generate_kpi_card(value: str, label: str, color: str = "orange", sub_text: Optional[str] = None) -> str:
    """Generate a single KPI card HTML"""
    sub_html = f'<div class="kpi-sub">{sub_text}</div>' if sub_text else ''
    return f'''    <div class="kpi-card c-{color}">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
      {sub_html}
    </div>'''

def generate_content_block(title: str, content: str, table_data: Optional[List[Dict]] = None) -> str:
    """Generate a content block with optional table"""
    table_html = ""
    if table_data and len(table_data) > 0:
        # Extract headers from first item
        headers = list(table_data[0].keys())
        table_html = f"""
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            {''.join(f'<th>{h}</th>' for h in headers)}
          </tr>
        </thead>
        <tbody>
          {''.join(f'<tr>{"".join(f"<td>{row.get(h, "")}</td>" for h in headers)}</tr>' for row in table_data)}
        </tbody>
      </table>
    </div>"""
    
    return f'''  <div class="content-block">
    <h3>{title}</h3>
    <p>{content}</p>{table_html}
  </div>'''

def generate_next_steps(steps: List[str]) -> str:
    """Generate next steps section"""
    steps_html = ''.join(f'<p>✓ {step}</p>' for step in steps)
    return f'''    {steps_html}'''

class ReportGenerator:
    """Generate professional Avanade-branded reports"""
    
    def __init__(self, template_path: Optional[str] = None):
        """Initialize with template path"""
        if template_path is None:
            # Use default template in _templates directory
            base_dir = Path(__file__).parent
            template_path = base_dir / "REPORT-TEMPLATE-AVANADE-STANDARD.html"
        
        self.template_path = Path(template_path)
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
    
    def generate(
        self,
        title: str,
        subtitle: str,
        kpis: List[Dict],
        content_sections: List[Dict],
        next_steps: List[str],
        version: str = "1.0",
        output_path: Optional[str] = None
    ) -> str:
        """Generate report from template"""
        
        # Generate KPI cards
        kpi_cards_html = '\n'.join([
            generate_kpi_card(
                kpi['value'],
                kpi['label'],
                kpi.get('color', 'orange'),
                kpi.get('sub_text')
            )
            for kpi in kpis
        ])
        
        # Generate content sections
        content_html = '\n'.join([
            generate_content_block(
                section['title'],
                section['content'],
                section.get('table_data')
            )
            for section in content_sections
        ])
        
        # Generate next steps
        next_steps_html = generate_next_steps(next_steps)
        
        # Get current date
        report_date = datetime.now().strftime("%B %d, %Y")
        
        # Replace template variables
        report = self.template
        report = report.replace("{{REPORT_TITLE}}", title)
        report = report.replace("{{REPORT_SUBTITLE}}", subtitle)
        report = report.replace("{{REPORT_DATE}}", report_date)
        report = report.replace("{{REPORT_VERSION}}", version)
        report = report.replace("{{KPI_CARDS}}", kpi_cards_html)
        report = report.replace("{{CONTENT_SECTIONS}}", content_html)
        report = report.replace("{{NEXT_STEPS}}", next_steps_html)
        
        # Save if output path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ Report generated: {output_file}")
        
        return report

def generate_from_json(json_config_path: str, output_path: Optional[str] = None):
    """Generate report from JSON config file"""
    
    with open(json_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    generator = ReportGenerator()
    report = generator.generate(
        title=config['title'],
        subtitle=config['subtitle'],
        kpis=config['kpis'],
        content_sections=config['content_sections'],
        next_steps=config['next_steps'],
        version=config.get('version', '1.0'),
        output_path=output_path or config.get('output_path')
    )
    
    return report

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_config = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        generate_from_json(json_config, output_file)
    else:
        # Demo
        generator = ReportGenerator()
        
        kpis = [
            {"value": "100", "label": "Tests", "color": "orange"},
            {"value": "5", "label": "Modules", "color": "magenta"},
            {"value": "95%", "label": "Success", "color": "green"},
        ]
        
        content = [
            {
                "title": "Overview",
                "content": "This is a sample report generated from the Avanade template."
            }
        ]
        
        steps = ["Review findings", "Implement recommendations", "Schedule follow-up"]
        
        report = generator.generate(
            title="Sample Report",
            subtitle="Generated from Avanade Template",
            kpis=kpis,
            content_sections=content,
            next_steps=steps,
            version="1.0",
            output_path="sample_report.html"
        )
        
        print("✓ Demo report created: sample_report.html")
