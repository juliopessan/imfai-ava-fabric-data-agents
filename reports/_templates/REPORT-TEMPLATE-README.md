# Avanade Professional Report Template

Standard template for generating professional data migration reports with Avanade branding.

## Quick Start (30 seconds)

### 1. Create your report configuration JSON

```json
{
  "title": "Your Report Title",
  "subtitle": "Your Subtitle Here",
  "version": "1.0",
  "kpis": [
    {
      "value": "463",
      "label": "Tests",
      "color": "orange",
      "sub_text": "100% pass"
    }
  ],
  "content_sections": [
    {
      "title": "Section Title",
      "content": "Section description text...",
      "table_data": [
        {
          "Column1": "Value1",
          "Column2": "Value2"
        }
      ]
    }
  ],
  "next_steps": [
    "Step 1",
    "Step 2",
    "Step 3"
  ]
}
```

### 2. Generate report

**Python (Programmatic):**
```python
from generate_report import ReportGenerator

generator = ReportGenerator()
report = generator.generate(
    title="My Report",
    subtitle="Analysis Results",
    kpis=[{"value": "100", "label": "Tests", "color": "orange"}],
    content_sections=[{"title": "Findings", "content": "..."}],
    next_steps=["Action 1", "Action 2"],
    output_path="my_report.html"
)
```

**Command Line:**
```bash
python generate_report.py report-config.json output_report.html
```

### 3. Open in browser

```powershell
start my_report.html
```

---

## Template Structure

| Section | Purpose | Customizable |
|---------|---------|--------------|
| **Header** | Avanade branding, title, date, version badge | Title, subtitle, version |
| **KPI Cards** | 6 key metrics in responsive grid | Values, labels, colors |
| **Content Blocks** | Flexible sections with tables | Title, text, table data |
| **Next Steps** | Action items | Array of steps |
| **Footer** | Copyright, generation info | Auto-generated |

---

## Customization

### KPI Card Colors
Available: `orange`, `magenta`, `red`, `gold`, `green`, `blue`

```json
{
  "value": "150x",
  "label": "Speed",
  "color": "green",
  "sub_text": "vs baseline"
}
```

### Content Tables
Automatic from array of dicts:

```json
{
  "title": "Metrics",
  "content": "Performance data",
  "table_data": [
    {"Metric": "Throughput", "Value": "10K/s"},
    {"Metric": "Latency", "Value": "28ms"}
  ]
}
```

---

## Examples

### Example 1: Financeiro Wave Report
```bash
# Copy example config
cp report-config.example.json financeiro-wave-1.json

# Customize values in financeiro-wave-1.json

# Generate
python generate_report.py financeiro-wave-1.json projects/financeiro/reports/WAVE-1-REPORT.html
```

### Example 2: Executive Summary
```python
from generate_report import ReportGenerator

gen = ReportGenerator()
report = gen.generate(
    title="Executive Summary — Q2 2026",
    subtitle="Multi-Wave Migration Results",
    kpis=[
        {"value": "4", "label": "Waves Complete", "color": "green"},
        {"value": "12M", "label": "Rows Migrated", "color": "orange"},
        {"value": "98.7%", "label": "Data Accuracy", "color": "blue"},
    ],
    content_sections=[...],
    next_steps=["Plan Q3", "Optimize costs"],
    output_path="executive_summary.html"
)
```

---

## File Reference

| File | Purpose |
|------|---------|
| `REPORT-TEMPLATE-AVANADE-STANDARD.html` | Base HTML template with Avanade styling |
| `generate_report.py` | Python report generator class + CLI |
| `report-config.example.json` | Template configuration example |
| `REPORT-TEMPLATE-README.md` | This file |

---

## Integration with Factory

Place generated reports in project output directories:

```
projects/
  ├── financeiro/
  │   └── reports/
  │       ├── WAVE-1-REPORT.html (generated)
  │       ├── WAVE-2-REPORT.html (generated)
  │       └── wave-config.json
  ├── supply-chain/
  │   └── reports/
  │       ├── DISCOVERY-REPORT.html (generated)
  │       └── wave-config.json
```

Serve with:
```bash
python -m http.server 8000 --directory projects/financeiro/reports
# Open: http://localhost:8000/WAVE-1-REPORT.html
```

---

## Standards

- **Branding:** Avanade official colors + Segoe UI typography
- **Responsive:** Works on desktop, tablet, mobile
- **Accessibility:** Semantic HTML, proper color contrast
- **Performance:** Pure HTML/CSS, no external frameworks
- **Compatibility:** Modern browsers (Chrome, Edge, Safari, Firefox)

---

## Support

For custom templates or styling, modify `REPORT-TEMPLATE-AVANADE-STANDARD.html` or create a new template variant (e.g., `REPORT-TEMPLATE-EXECUTIVE.html`).

All reports follow Avanade Data Migration Factory v3 standards.
