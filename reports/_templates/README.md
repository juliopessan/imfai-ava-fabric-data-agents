# Executive Dashboard — Data Migration Factory v3

> **Consultoria-branded executive dashboard** for enterprise data platform migration oversight. Designed for C-suite, PMO, and stakeholder communication. **Now with real-time token usage tracking and cost analytics.**

---

## 📊 What's Inside

### **Core Dashboard Files**

| File | Purpose |
|------|---------|
| `executive-dashboard.html` | 🎨 Main dashboard — Consultoria Style Guide 100% compliant |
| `generate-dashboard.py` | 🔧 Python script to generate live dashboard from wave data |
| `EXECUTIVE-DASHBOARD-GUIDE.md` | 📖 User guide + customization instructions |
| `validate-compliance.py` | ✅ Style guide compliance checker |

### **Token Metrics Files (NEW)**

| File | Purpose |
|------|---------|
| `token_metrics_collector.py` | 📊 Collects and aggregates token usage by agent/phase |
| `dashboard_server.py` | 🌐 Flask web server for URL-based dashboard access |
| `TOKEN-METRICS-GUIDE.md` | 📈 Complete API and integration guide |
| `example-workflow.py` | 🚀 End-to-end workflow demonstration |
| `sample-token-metrics.json` | 📋 Example metrics file format |

---

## 🚀 Quick Start

### **View Dashboard (Offline)**
```bash
# Open in browser
open executive-dashboard.html                    # macOS
start executive-dashboard.html                   # Windows
xdg-open executive-dashboard.html                # Linux
```

### **Generate Dashboard with Token Metrics**
```bash
# Sample data (for testing)
python generate-dashboard.py --sample --output dashboard-with-metrics.html

# Real wave data with metrics
python generate-dashboard.py \
  --wave-config ../projects/your-wave/wave-config.json \
  --gate-scores ../projects/your-wave/gate-scores.json \
  --token-metrics ../projects/your-wave/metrics.json \
  --output executive-dashboard-WAVE-001.html
```

### **Start Web Server (URL Access)**
```bash
# Simple (sample metrics)
python dashboard_server.py --port 8000

# With custom metrics
python token_metrics_collector.py --sample --output metrics.json
python dashboard_server.py --metrics metrics.json --port 8000

# Then open: http://127.0.0.1:8000
```

### **Run Complete Workflow**
```bash
python example-workflow.py
```

---

## 📊 Token Metrics — NEW Feature

### **Collect Token Usage**
```bash
# View sample metrics
python token_metrics_collector.py --sample

# Collect from wave directory
python token_metrics_collector.py --wave-dir ../projects/WAVE-001/outputs/

# Output includes:
# - Tokens by agent (discovery-scout, code-generator, etc.)
# - Phase breakdown (Upstream/Midstream/Downstream)
# - Cost estimation (USD based on GPT-4 pricing)
# - Top 5 agents by consumption
```

### **Sample Output**
```
📊 Token Usage Metrics
==================================================
Total Tokens: 344,000

By Phase:
  upstream            :     77,000 ( 22.4%)
  midstream           :    204,000 ( 59.3%)
  downstream          :     63,000 ( 18.3%)

Top Agents:
  code-generator                :     72,000 tokens
  data-architect                :     56,000 tokens
  data-modeler                  :     48,000 tokens

Cost (GPT-4): $0.52 USD
```

### **Dashboard Integration**
The dashboard now includes:
- **Phase Distribution Chart** — Visual breakdown with progress bars
- **Cost Analysis Table** — Estimated USD cost and M-token breakdown
- **Top Agents Rankings** — Table of highest token consumers
- **API Endpoint** — JSON metrics at `/api/metrics`

---

## 🎨 Design System

**Consultoria Brand Compliance:** ✅ 100%

- **Colors:** Orange #FF5800 (primary), Greys (80–10), master gradient (135° Orange→Aurora)
- **Typography:** Segoe UI (Light for H1/H2, Semibold for H3/H5), 42pt–20pt hierarchy
- **Cards:** Border-top 4px orange, hover effects, Consultoria shadow system
- **Spacing:** 8px base unit (all margins/padding in multiples)
- **Tagline:** "Do what matters" (Orange hero section, white footer)
- **Responsive:** Mobile-first, tested on all breakpoints + print

---

## 📋 Dashboard Content

### **Sections**

1. **Executive Summary** — 21 agents, 26 skills, 3 gates, 23 governance scripts
2. **Three-Gate Framework** — Flow diagram with status indicators (🟢/🟡/🔴)
3. **Token Usage Analytics (NEW)** — Phase breakdown, cost, top agents
4. **Agent Portfolio** — 21 specialists organized by phase (Upstream → Midstream → Downstream)
5. **Skill Library** — 26 domain knowledge modules (Discovery, Architecture, Execution)
6. **Governance & Compliance** — 100% Microsoft stack, policy-as-code
7. **CI/CD Pipeline** — 7 automated jobs (trigger → lint → test → deploy)
8. **Migration Playbooks** — Recommended sequences (EDW, OLTP, hybrid)
9. **Performance Metrics** — 189 tests, 100% compliance, GateScore thresholds
10. **Team Conventions** — wave-config.yaml, discovery owner, artifact structure
11. **Next Steps** — 5 concrete actions to begin migrations

---

## 🔄 Integration

### **Connect to Wave Tracker**
The `generate-dashboard.py` script reads:
- `wave-config.json` — entities, discovery owner, timeline
- `gate-scores.json` — GateScore per gate (0.0–1.0)
- `metrics.json` — Token usage by agent and phase (NEW)

Update these JSON files, re-run the generator, and get a fresh dashboard with updated metrics.

### **Web Server Integration**
```bash
# Start dashboard server on port 8000
python dashboard_server.py --port 8000

# Access dashboard: http://127.0.0.1:8000/
# Access metrics API: http://127.0.0.1:8000/api/metrics
# Health check: http://127.0.0.1:8000/health
```

### **Automation Example**
```bash
# Generate dashboard weekly with token metrics
0 9 * * 1 python /path/to/reports/token_metrics_collector.py \
  --wave-dir /path/to/projects/active-wave/outputs/ \
  --output /path/to/projects/active-wave/metrics.json

0 9 * * 1 python /path/to/reports/generate-dashboard.py \
  --output reports/weekly-executive-summary.html
```

### **Distribution**
- **Email:** Attach HTML or PDF to weekly stakeholder report
- **Teams:** Pin in Teams channel (link to HTML file)
- **Portal:** Host on intranet with Apache/IIS
- **Archive:** Commit snapshot to Git per gate approval

---

## 🎯 Use Cases

### **Executive Steering Committee**
- Weekly status dashboard (gate progress, KPIs, risk register)
- Slide deck export (print or PPTX)

### **PMO Reporting**
- Wave progress tracking (Upstream → Downstream)
- Resource planning (agent allocation per phase)

### **Stakeholder Communication**
- Client-facing deck (executive summary + next steps)
- Investment justification (ROI, timeline, team size)

### **Internal Handoff**
- Discovery → Architecture → Execution transition checklist
- Quality gate documentation (scores, open items, approver)

---

## 🛠️ Customization

### **A. Update Gate Status**
```html
<!-- Before -->
<div class="ava-status ava-status--green">✅ Approved</div>

<!-- After (Amber = In Review) -->
<div class="ava-status ava-status--amber">⚠️ In Review (0.78/1.0)</div>
```

### **B. Add Custom Metrics**
```html
<div class="ava-card ava-card--compact ava-text-center">
    <div class="ava-metric__value">3.2</div>
    <div class="ava-metric__label">Week Velocity (avg)</div>
</div>
```

### **C. Python Customization**
```python
from generate_dashboard import DashboardGenerator

gen = DashboardGenerator()
html = gen.generate()
# Custom post-processing
html = html.replace("{{ wave_name }}", "WAVE-002")
print(html)
```

---

## ✅ Quality Checklist

Before sharing with executives:

- [ ] Metrics are current (agent count, test pass rate, GateScore)
- [ ] Gate statuses match wave-config.json state
- [ ] No broken links or typos
- [ ] Logo + tagline properly positioned
- [ ] Tested on mobile + tablet + print
- [ ] PDF export renders correctly
- [ ] All tables fit on slide (if exporting to deck)

---

## 🔐 Accessibility & Compliance

- **WCAG 2.1 AA:** Color contrast verified, semantic HTML, responsive
- **Print-friendly:** Header/footer hidden, cards forced white bg
- **Microsoft Stack:** 100% — no external CDNs or non-Microsoft tooling
- **Brand:** Consultoria Style Guide 100% applied

---

## � API Reference

### Token Metrics Endpoints

```bash
# Get dashboard with metrics (HTML)
GET http://127.0.0.1:8000/
# Returns: HTML dashboard with embedded token usage visualization

# Get raw metrics (JSON)
GET http://127.0.0.1:8000/api/metrics
# Returns: {
#   "by_agent": {...},
#   "by_phase": {"upstream": 77000, "midstream": 204000, ...},
#   "total": 344000,
#   "timestamp": "2026-06-05T..."
# }

# Health check
GET http://127.0.0.1:8000/health
# Returns: {"status": "ok", "timestamp": "..."}
```

---

## 🧪 Verification

### Compliance Check
```bash
python validate-compliance.py
# ✅ PASSED: 100% Consultoria Style Guide Compliant
```

### Token Metrics Validation
```bash
python token_metrics_collector.py --sample
# Shows: Total tokens by phase, top agents, cost estimate
```

### Workflow Test
```bash
python example-workflow.py
# Runs end-to-end: collect → generate → report → analyze
```

---

## 📞 Support

### **Token Metrics Issues**
See: `TOKEN-METRICS-GUIDE.md` → **Troubleshooting**

### **Dashboard Generation**
See: `EXECUTIVE-DASHBOARD-GUIDE.md` → **Troubleshooting**

### **Server Setup**
See: `TOKEN-METRICS-GUIDE.md` → **Server Setup & Deployment**

### **Migration Guidance**
See: `docs/OPERATING-MODEL-CANVAS-v2.md` or `docs/COPILOT-AGENTS-GUIDE.md`

---

## 📅 Maintenance

| Task | Frequency | Owner |
|------|-----------|-------|
| Collect token metrics | Per wave | Tech Lead |
| Update dashboard | Per sprint | PMO |
| Update agent inventory | Annually | Migration Coordinator |
| Brand audit (colors, fonts) | Quarterly | Design Lead |
| Server uptime monitoring | Continuous | DevOps |

---

## 📚 Documentation

- **Executive Dashboard Guide** → `EXECUTIVE-DASHBOARD-GUIDE.md`
- **Token Metrics API** → `TOKEN-METRICS-GUIDE.md`
- **Implementation Checklist** → `IMPLEMENTATION-CHECKLIST.md`
- **Data Migration Factory** → `docs/OPERATING-MODEL-CANVAS-v2.md`
- **Agent Reference** → `docs/COPILOT-AGENTS-GUIDE.md`

---

**Last Updated:** 2026-06-05  
**Version:** 2.0 (with Token Metrics)  
**Status:** ✅ Production Ready  
**Compliance:** Consultoria Style Guide 100% | WCAG 2.1 AA ✅  
**Token Metrics:** ✅ Complete & Tested
