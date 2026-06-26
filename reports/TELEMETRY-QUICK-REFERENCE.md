# 📊 Telemetry System — Quick Reference Card

**Status:** ✅ Production Ready | **Created:** 2026-06-25

---

## 📁 Where Everything Is

### Main Files
| Component | Location | Type | Size | Purpose |
|-----------|----------|------|------|---------|
| **Trace Logs System** | `.trace-logs/` | JSON Lines | JSONL | Centralized trace storage (6 categories) |
| **Telemetry Engine** | `src/shared/scripts/execution_telemetry.py` | Python | 271 LOC | Real-time metrics tracking |
| **Dashboard Gen** | `src/shared/scripts/generate_telemetry_dashboard.py` | Python | 447 LOC | HTML dashboard (15-30 KB) |
| **Coach Telemetry** | `.coach/telemetry-schema.json` | JSON | Schema | Agent instrumentation |
| **Documentation** | `docs/observability/OBSERVABILITY-AND-TRACES.md` | Markdown | 15 KB | Full technical guide |
| **Quick Start** | `docs/observability/trace-logs/QUICK-START.md` | Markdown | 5 KB | 5-minute setup |
| **Inventory** | **`reports/TELEMETRY-SYSTEM-INVENTORY.md`** | Markdown | 50 KB | **Complete reference** ⭐ |

---

## 🚀 30-Second Setup

```python
from execution_telemetry import ExecutionTelemetry

# Step 1: Initialize
telemetry = ExecutionTelemetry("My Workflow", "agent-name")

# Step 2: Track phases
with telemetry.track_phase("Phase Name", "Phase ID"):
    telemetry.add_tool_call("Tool", status="success", cost=0.005)

# Step 3: Generate report
report = telemetry.generate_report()
telemetry.to_json("telemetry.json")

# Step 4: Create dashboard
from generate_telemetry_dashboard import generate_full_telemetry_dashboard
html = generate_full_telemetry_dashboard(report)
```

---

## 📊 What Gets Tracked

| Category | Metrics | Example |
|----------|---------|---------|
| **Time** | Wall clock execution | 45.2 seconds |
| **Tokens** | Input + output breakdown | 2,048 in / 1,024 out |
| **Cost** | USD @ Claude Haiku pricing | $0.0039 |
| **Tools** | Name, status, duration, cost | Azure API: 0.5ms, $0.001 |
| **RAG** | Docs retrieved, tokens used | 10 docs, 250 tokens |
| **Cache** | Hit/miss ratio | 100% cache hit rate |
| **Business** | Custom outcomes, impact | Data Quality: 95%, High impact |

---

## 📍 Trace Categories

```
.trace-logs/
├── agents/           → Agent executions (spawn, complete, fail)
├── workflows/        → Orchestrator decisions (routes, hand-offs)
├── etl/             → Data pipeline operations (rows processed)
├── gates/           → Quality gate scoring (scores, artifacts)
├── migrations/      → Wave progress (entity count, coverage)
└── analytics/       → Pre-aggregated metrics (avg duration, throughput)
```

---

## 🔍 Quick Queries

### Cost by Agent (Last 24h)
```python
from collections import defaultdict
from pathlib import Path
import json

agent_costs = defaultdict(float)
for f in Path(".trace-logs/agents").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            agent = event["context"]["agent_id"]
            cost = event["metrics"].get("cost_usd", 0)
            agent_costs[agent] += cost

for agent, cost in sorted(agent_costs.items(), key=lambda x: x[1], reverse=True):
    print(f"{agent}: ${cost:.4f}")
```

### Success Rate by Wave
```python
from collections import defaultdict
import json
from pathlib import Path

stats = defaultdict(lambda: {"total": 0, "success": 0})
for f in Path(".trace-logs/agents").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            wave = event["context"]["wave"]
            if event["operation"]["status"] == "success":
                stats[wave]["success"] += 1
            stats[wave]["total"] += 1

for wave, data in stats.items():
    rate = data["success"] / data["total"] * 100
    print(f"{wave}: {rate:.1f}% ({data['success']}/{data['total']})")
```

---

## 📈 Dashboard Features

| Feature | Details |
|---------|---------|
| **Sidebar** | Sticky metrics panel (320px) |
| **Metrics** | Time, tokens, cost, status, cache hit %, breakdown |
| **Timeline** | Expandable phases & spans (icon-labeled) |
| **Business Layer** | Outcomes by category (color-coded) |
| **Size** | 15-30 KB HTML (embedded CSS/JS, no dependencies) |
| **Format** | Pure HTML (works offline, shareable) |

---

## ✅ Best Practices

1. ✅ Always include **ISO 8601 UTC timestamp**
2. ✅ Use **UUID v4** for trace_id
3. ✅ Include **wave, gate, agent_id** in context
4. ✅ **Append-only** — never modify existing traces
5. ✅ **Rotate daily** — one file per day per context
6. ✅ **Tag for filtering** — add tags for quick queries
7. ✅ **No PII** — filter sensitive data before logging

---

## 🚫 Don't Do This

❌ Store PII in traces  
❌ Append to old files  
❌ Modify existing traces  
❌ Store large objects (reference IDs instead)  
❌ Mix trace types in same file  

---

## 📚 Read These (In Order)

1. **Quick Start** (5 min) — `docs/observability/trace-logs/QUICK-START.md`
2. **Trace Logs** (15 min) — `docs/observability/trace-logs/README.md`
3. **Full Guide** (45 min) — `docs/observability/OBSERVABILITY-AND-TRACES.md`
4. **Inventory** (reference) — **`reports/TELEMETRY-SYSTEM-INVENTORY.md`** ⭐

---

## 🎯 Use Cases

**Performance Dashboard**
- Average duration per agent
- Token/cost trends
- Success rates by wave

**Cost Analysis**
- Total cost by agent/wave
- Cost per artifact
- Cost increase/decrease trends

**SLA Monitoring**
- Duration vs threshold
- Error rate tracking
- Regression alerts

**Dependency Analysis**
- Trace hand-offs between agents
- Identify bottlenecks
- Critical path analysis

---

## 📊 Test Results

```
Execution Time: 1 second
Total Tokens: 1,690 (100 input, 1,590 output)
Cost: $0.0039 USD
Cache Hit Rate: 100%
Timeline Events: 8
Business Outcomes: 7 categories, 10+ metrics
Output Size: Demo dashboard 22.9 KB, JSON 6.2 KB
Status: ✅ All tests passed
```

---

## 🔌 Integration Points

| Source | Writes To | Status |
|--------|-----------|--------|
| migration-coordinator | `workflows/` | ✅ Ready |
| quality-gate script | `gates/` | ✅ Ready |
| ETL pipelines | `etl/` | ✅ Ready |
| Coach system | `agents/` | ✅ Ready |
| Analytics engine | `analytics/` | ✅ Ready |

---

## 💰 Pricing Model

**Claude Haiku (Default)**
- Input: $0.80 per million tokens
- Output: $2.40 per million tokens
- Customizable via `price_per_input_mtok` and `price_per_output_mtok`

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Init overhead | < 1ms |
| Per-call tracking | < 0.5ms |
| Dashboard generation | ~500ms |
| Total workflow overhead | < 2% |
| Memory footprint | ~100 KB |

---

## 🎓 Implementation Steps

```
Step 1: Read Quick Start (5 min)
Step 2: Initialize ExecutionTelemetry class
Step 3: Wrap code in track_phase()
Step 4: Add tool_call/rag/memory/outcome records
Step 5: Generate report & export JSON
Step 6: Create dashboard HTML
Step 7: Write to .trace-logs/ via write_trace()
Step 8: Query JSONL files for analytics
Step 9: Monitor & refine metrics
```

---

## 📞 Support

| Question | Answer |
|----------|--------|
| How do I write a trace? | See QUICK-START.md |
| What trace types exist? | See trace-logs/README.md |
| How do I query costs? | See query examples above |
| Full architecture? | See OBSERVABILITY-AND-TRACES.md |
| Complete reference? | See **TELEMETRY-SYSTEM-INVENTORY.md** ⭐ |

---

## 📦 Files to Share

**For Architects/Decision-Makers:**
- `reports/TELEMETRY-SYSTEM-INVENTORY.md` (complete reference)
- This quick card (overview)

**For Developers:**
- `docs/observability/trace-logs/QUICK-START.md` (setup)
- `src/shared/scripts/execution_telemetry.py` (examples)
- `tools/utilities/test_telemetry_system.py` (working demo)

**For DevOps:**
- `docs/observability/OBSERVABILITY-AND-TRACES.md` (full guide)
- `projects/bradesco/scripts/00_MASTER_PIPELINE_WITH_TELEMETRY.py` (integration)
- `.trace-logs/trace-schema.json` (schema)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2026-06-25  
**Version:** 1.0.0  
**Author:** System Telemetry Team
