# Token Metrics & Dashboard Server

**Comprehensive token usage tracking and live dashboard server for Data Migration Factory.**

---

## 📊 Components

### **1. Token Metrics Collector** (`token_metrics_collector.py`)
Extracts token usage data from migration artifacts.

```bash
# Generate sample metrics
python token_metrics_collector.py --sample --output metrics.json

# Collect from wave directory
python token_metrics_collector.py --wave-dir projects/WAVE-001/outputs/

# View summary
python token_metrics_collector.py --sample
```

**Output: `metrics.json`**
```json
{
  "by_agent": {
    "discovery-scout": {"tokens": 45_000, "calls": 8, "phase": "upstream"},
    ...
  },
  "by_phase": {
    "upstream": 77_000,
    "midstream": 204_000,
    "downstream": 63_000
  },
  "total": 344_000,
  "timestamp": "2026-06-05T..."
}
```

---

### **2. Dashboard Server** (`dashboard_server.py`)
Flask app that serves the executive dashboard with live token metrics.

#### **Installation**
```bash
# Install Flask (if not already installed)
pip install flask

# Or for dev
pip install -e ".[dev]"
```

#### **Usage**

**Simple Start (local, sample metrics):**
```bash
python dashboard_server.py --port 8000
# Open: http://127.0.0.1:8000
```

**With Custom Metrics:**
```bash
# First, collect token metrics
python token_metrics_collector.py --sample --output metrics.json

# Start server with metrics
python dashboard_server.py --metrics metrics.json --port 8000
```

**Production Setup:**
```bash
# Listen on all interfaces (requires firewall config)
python dashboard_server.py --host 0.0.0.0 --port 5000

# Enable debug mode for development
python dashboard_server.py --debug
```

#### **Server Routes**

| Route | Response | Purpose |
|-------|----------|---------|
| `/` | HTML | Main dashboard |
| `/api/metrics` | JSON | Token metrics API |
| `/health` | JSON | Health check |

---

### **3. Updated Dashboard Generator** (`generate-dashboard.py`)
Now integrates token metrics into static HTML.

#### **Usage**

**With Token Metrics:**
```bash
python generate-dashboard.py \
  --wave-config projects/WAVE-001/wave-config.json \
  --gate-scores projects/WAVE-001/gate-scores.json \
  --token-metrics projects/WAVE-001/metrics.json \
  --output reports/WAVE-001-dashboard.html
```

**Sample Dashboard (auto-includes metrics):**
```bash
python generate-dashboard.py --sample --output reports/sample-dashboard.html
```

---

## 🚀 Quick Start

### **Scenario 1: View Dashboard in Browser**
```bash
# Option A: Static HTML (offline)
open reports/executive-dashboard.html

# Option B: Live server with metrics
python dashboard_server.py
# Open: http://127.0.0.1:8000
```

### **Scenario 2: Generate Report with Wave Data**
```bash
# Step 1: Collect token metrics from wave
python token_metrics_collector.py \
  --wave-dir projects/my-wave/outputs/ \
  --output projects/my-wave/metrics.json

# Step 2: Generate dashboard with all data
python generate-dashboard.py \
  --wave-config projects/my-wave/wave-config.json \
  --gate-scores projects/my-wave/gate-scores.json \
  --token-metrics projects/my-wave/metrics.json \
  --output projects/my-wave/executive-dashboard-final.html

# Step 3: Open report
open projects/my-wave/executive-dashboard-final.html
```

### **Scenario 3: Weekly Dashboard Email**
```bash
#!/bin/bash
# weekly-dashboard.sh

WAVE_DIR="projects/active-wave"
METRICS_FILE="$WAVE_DIR/metrics.json"
OUTPUT="$WAVE_DIR/dashboard-$(date +%Y%m%d).html"

# Collect metrics
python token_metrics_collector.py --wave-dir "$WAVE_DIR/outputs/" --output "$METRICS_FILE"

# Generate dashboard
python generate-dashboard.py \
  --wave-config "$WAVE_DIR/wave-config.json" \
  --gate-scores "$WAVE_DIR/gate-scores.json" \
  --token-metrics "$METRICS_FILE" \
  --output "$OUTPUT"

# Convert to PDF and email
wkhtmltopdf "$OUTPUT" "${OUTPUT%.html}.pdf"
echo "Dashboard attached" | mail -a "$OUTPUT" -s "Weekly DMF Report" stakeholders@company.com
```

---

## 📊 Dashboard Sections

### **Token Usage Analytics** (NEW)

#### **Phase Distribution**
- Visual breakdown of tokens used per phase (Upstream/Midstream/Downstream)
- Percentage and absolute token count per phase
- Progress bars with gradient theme

#### **Cost Analysis**
- Estimated cost in USD (based on GPT-4 pricing: $0.0015/MTok)
- Total token count
- Tokens in millions (MTok)
- Pricing rate used

#### **Top Agents by Token Consumption**
- Table showing top 5 agents
- Agent name, phase, token count, number of calls
- Sorted by highest token usage

---

## 🔧 Integration Examples

### **Azure DevOps Pipeline**
```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'

  - script: |
      pip install -r requirements-dev.txt
      python reports/token_metrics_collector.py --wave-dir $(Build.SourcesDirectory)/projects/active-wave/outputs --output metrics.json
      python reports/generate-dashboard.py --sample --token-metrics metrics.json --output dashboard.html
    displayName: 'Generate Dashboard with Metrics'

  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: 'dashboard.html'
      artifactName: 'executive-dashboard'
```

### **Cron Job (Weekly Report)**
```bash
# /etc/cron.d/dmf-dashboard
0 9 * * 1 cd /app && python reports/dashboard_server.py --port 8000 &
0 10 * * 1 /app/scripts/generate-weekly-dashboard.sh
```

### **Python Script Integration**
```python
from reports.token_metrics_collector import TokenMetricsCollector
from reports.generate_dashboard import DashboardGenerator

# Collect metrics
collector = TokenMetricsCollector()
metrics = collector.collect_from_artifacts("projects/WAVE-001/outputs/")

# Generate dashboard
gen = DashboardGenerator("projects/WAVE-001/wave-config.json")
gen.token_metrics = metrics
gen.generate("dashboard-final.html")

print(f"✅ Generated dashboard with {metrics['total']:,} tokens")
```

---

## 📈 Metrics Structure

```
Token Metrics JSON Schema:

{
  "by_agent": {
    "<agent_name>": {
      "tokens": <int>,
      "calls": <int>,
      "phase": "upstream|midstream|downstream"
    }
  },
  "by_phase": {
    "<phase>": <total_tokens>
  },
  "by_wave": {
    "<wave_name>": <total_tokens>
  },
  "by_section": {
    "<section_name>": {
      "tokens": <int>,
      "phase": "<phase>"
    }
  },
  "total": <total_tokens>,
  "timestamp": "ISO8601"
}
```

---

## 💡 Token Cost Reference

| Model | Cost/MTok | Example |
|-------|-----------|---------|
| GPT-4 Turbo | $0.0150 | 1M tokens = $15 |
| GPT-4 32K | $0.0150 | 1M tokens = $15 |
| GPT-3.5 Turbo | $0.0005 | 1M tokens = $0.50 |
| Claude 3 Opus | $0.0150 | 1M tokens = $15 |

*Rates are approximate and subject to change. See provider pricing.*

---

## 🔐 Server Security Notes

- **Local Development:** `--host 127.0.0.1` (default, safe)
- **Internal Network:** `--host 0.0.0.0` + firewall rules
- **Production:** Use reverse proxy (nginx/Apache) + HTTPS
- **No Authentication:** Server assumes trusted network (add authentication layer if needed)

---

## 📋 API Examples

### **Get Metrics via API**
```bash
curl http://127.0.0.1:8000/api/metrics | jq .

# Response:
{
  "by_agent": {...},
  "by_phase": {...},
  "total": 344000,
  "timestamp": "2026-06-05T..."
}
```

### **Health Check**
```bash
curl http://127.0.0.1:8000/health
# {"status": "ok", "timestamp": "..."}
```

---

## 🆘 Troubleshooting

### **Flask not installed**
```bash
pip install flask
```

### **Port already in use**
```bash
# Use different port
python dashboard_server.py --port 8001

# Or kill existing process
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### **Token metrics not showing**
```bash
# Check if metrics file exists
ls -la projects/my-wave/metrics.json

# Generate sample metrics to test
python token_metrics_collector.py --sample --output test-metrics.json

# Start server with sample metrics
python dashboard_server.py --metrics test-metrics.json
```

### **Metrics file format error**
```bash
# Validate JSON
python -m json.tool projects/my-wave/metrics.json

# Fix formatting if needed
python -c "import json; print(json.dumps(json.load(open('metrics.json')), indent=2))" > metrics-fixed.json
```

---

## 📚 References

- **Token Metrics:** [token_metrics_collector.py](token_metrics_collector.py)
- **Dashboard Generator:** [generate-dashboard.py](generate-dashboard.py)
- **Server:** [dashboard_server.py](dashboard_server.py)
- **Main Dashboard:** [executive-dashboard.html](executive-dashboard.html)
- **Guide:** [EXECUTIVE-DASHBOARD-GUIDE.md](EXECUTIVE-DASHBOARD-GUIDE.md)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2026-06-05
