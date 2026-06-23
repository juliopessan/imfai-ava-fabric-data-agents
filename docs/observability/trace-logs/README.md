# 📊 Trace Logs — Observability & Analytics

**Purpose:** Centralized trace logging system for tracking execution, performance, and quality metrics across all systems  
**Format:** JSONL (append-only, queryable, timestamped)  
**Location:** `.trace-logs/` (hidden directory at project root)  
**Quick Start:** `docs/observability/trace-logs/QUICK-START.md`

---

## 🎯 What Are Trace Logs?

Trace logs are **detailed, timestamped records** of every significant operation:

```
Agent runs       →  How long? Did it succeed? How many tokens?
Workflows        →  Which path was taken? Any hand-offs?
ETL pipelines    →  How many rows? Any errors?
Quality gates    →  What's the score? Any patterns detected?
Data migrations  →  How many entities? What's the coverage?
```

**Key Difference from Traditional Logs:**
- Traditional logs: ❌ File-based, hard to search
- Trace logs: ✅ **JSONL format** (one JSON object per line)
  - Easy to parse and query
  - Structured data (no free-text parsing needed)
  - Fast aggregation for analytics

---

## 📁 Directory Structure

```
.trace-logs/                          Hidden directory at project root
├── README.md                         This guide
├── trace-schema.json                 Validation schema (enforces data integrity)
│
├── agents/                           Agent execution traces
│   └── agent_execution_*.jsonl
│
├── workflows/                        Orchestrator traces
│   └── workflow_execution_*.jsonl
│
├── etl/                             ETL pipeline traces
│   └── etl_operation_*.jsonl
│
├── gates/                           Quality gate traces
│   └── gate_scoring_*.jsonl
│
├── migrations/                      Migration event traces
│   └── migration_event_*.jsonl
│
├── analytics/                       Pre-aggregated metrics
│   └── performance_metric_*.jsonl
│
└── archive/                         Older traces (compressed)
    └── 2026-05-*.tar.gz
```

---

## 📝 Trace Event Example

Each line in a JSONL file is a complete event:

```json
{
  "timestamp": "2026-06-18T14:32:15.123456Z",
  "trace_id": "tr_bdf3e2c1-8f9a-42eb-b012-1a2b3c4d5e6f",
  "trace_type": "agent_execution",
  "context": {
    "agent_id": "migration-coordinator",
    "wave": "clientebanco-wave2",
    "gate": 1,
    "user": "data-engineer@company.com",
    "tags": ["critical", "gate-1-validation"]
  },
  "operation": {
    "name": "spawn_agent",
    "duration_sec": 45.23,
    "status": "success"
  },
  "metrics": {
    "tokens_in": 2048,
    "tokens_out": 1024,
    "artifacts_generated": 3
  }
}
```

---

## 📊 Trace Types

| Type | Purpose | File Path | Example Metrics |
|------|---------|-----------|-----------------|
| **agent_execution** | Agent task completion | `agents/` | duration, tokens, artifacts |
| **workflow_execution** | Orchestrator decisions | `workflows/` | decision, path, hand-off |
| **etl_operation** | Data pipeline runs | `etl/` | rows_processed, error_rate |
| **gate_scoring** | Quality gate results | `gates/` | score, anti_patterns, artifacts |
| **migration_event** | Wave progress | `migrations/` | entity_count, coverage |
| **performance_metric** | Pre-aggregated stats | `analytics/` | avg_duration, throughput |

---

## 🚀 Quick Start

### **Write a Trace (Python)**

```python
import json
from datetime import datetime
from pathlib import Path
import uuid

def write_trace(trace_type: str, context: dict, operation: dict, metrics: dict = None):
    """Write a trace event to JSONL file"""
    
    trace_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": f"tr_{uuid.uuid4()}",
        "trace_type": trace_type,
        "context": context,
        "operation": operation,
        "metrics": metrics or {},
        "metadata": {"source": __file__, "version": "1.0.0"}
    }
    
    # Create category directory
    category = context.get("category", trace_type)
    trace_dir = Path(".trace-logs") / category
    trace_dir.mkdir(parents=True, exist_ok=True)
    
    # Append to today's file
    today = datetime.utcnow().strftime("%Y-%m-%d")
    trace_file = trace_dir / f"{trace_type}_{context.get('wave', 'general')}_{today}_001.jsonl"
    
    with open(trace_file, "a") as f:
        f.write(json.dumps(trace_event) + "\n")

# Usage
write_trace(
    trace_type="agent_execution",
    context={
        "category": "agents",
        "agent_id": "migration-coordinator",
        "wave": "clientebanco-wave2",
        "gate": 1,
        "tags": ["critical"]
    },
    operation={
        "name": "spawn_agent",
        "duration_sec": 45.23,
        "status": "success"
    },
    metrics={"tokens_in": 2048, "tokens_out": 1024}
)
```

### **Read & Query Traces (Python)**

```python
import json
from pathlib import Path

def read_traces(trace_file: str):
    """Read JSONL file"""
    traces = []
    path = Path(".trace-logs") / trace_file
    
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    return traces

# Usage
traces = read_traces("agents/agent_execution_clientebanco-wave2_2026-06-18_001.jsonl")
for trace in traces:
    print(f"{trace['timestamp']} | {trace['operation']['name']} | {trace['operation']['status']}")
```

---

## 🔍 Common Queries

### **Total Cost Today**
```python
import json
from pathlib import Path

total_cost = 0
for f in Path(".trace-logs/agents").glob("*_2026-06-18_*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            total_cost += event.get("metrics", {}).get("cost_usd", 0)

print(f"Cost today: ${total_cost:.2f}")
```

### **Agent Performance by Wave**
```python
import json
from pathlib import Path
from collections import defaultdict

durations = defaultdict(list)
for f in Path(".trace-logs/agents").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            wave = event["context"].get("wave")
            durations[wave].append(event["operation"].get("duration_sec", 0))

for wave, times in durations.items():
    print(f"{wave}: {sum(times)/len(times):.1f}s avg")
```

### **Error Rate by Gate**
```python
import json
from pathlib import Path
from collections import defaultdict

gate_stats = defaultdict(lambda: {"total": 0, "failed": 0})
for f in Path(".trace-logs/gates").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            gate = event["context"].get("gate")
            gate_stats[gate]["total"] += 1
            if event["operation"].get("status") != "success":
                gate_stats[gate]["failed"] += 1

for gate, stats in sorted(gate_stats.items()):
    rate = stats["failed"] / stats["total"] if stats["total"] > 0 else 0
    print(f"Gate {gate}: {rate*100:.1f}% error rate")
```

---

## 🎯 Integration Points

**Who writes traces:**

| System | What | How |
|--------|------|-----|
| migration-coordinator | workflow_execution | Call write_trace() after spawn_agent() |
| quality-gate | gate_scoring | Call write_trace() in calculate_gatescore() |
| ETL scripts | etl_operation | Call write_trace() after each batch |
| Coach telemetry | agent_execution | TelemetryCollector.log_execution() |
| Analytics | performance_metric | Aggregator script (nightly) |

---

## 📈 Analytics Use Cases

✅ **Performance Dashboard**
- Avg duration by agent
- Tokens/cost trends
- Success rates by wave

✅ **Cost Analysis**
- Total cost by agent/wave
- Cost per artifact
- Trending cost increase/decrease

✅ **SLA Monitoring**
- Duration vs threshold
- Error rate tracking
- Alerts on regression

✅ **Dependency Chains**
- Trace hand-offs between agents
- Identify bottlenecks
- Critical path analysis

---

## 🔒 Data Retention

**Policy:**
- **Last 7 days:** Live in `.trace-logs/`
- **7–30 days:** Moved to `archive/` (compressed)
- **>30 days:** Delete or external storage

**Cleanup Script:**
```bash
# Compress traces older than 7 days
find .trace-logs -name "*.jsonl" -mtime +7 -exec gzip {} \;
tar czf archive/traces-$(date +%Y-%m-%d).tar.gz .trace-logs/*/*.gz
rm .trace-logs/*/*.gz
```

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| [QUICK-START.md](QUICK-START.md) | Get writing traces in 5 minutes |
| [QUERY-COOKBOOK.md](QUERY-COOKBOOK.md) | Common analytical queries |
| [DASHBOARDING.md](DASHBOARDING.md) | Connect traces to dashboards |
| `.trace-logs/trace-schema.json` | Full data validation schema |
| `.trace-logs/README.md` | Low-level implementation guide |

---

## ✅ Best Practices

✅ **Always include timestamp** — ISO 8601 UTC  
✅ **Unique trace_id** — UUID v4 for correlation  
✅ **Consistent context** — wave, gate, agent_id  
✅ **Minimal complete** — Include what's needed, no bloat  
✅ **Append-only** — Never modify existing traces  
✅ **Daily rotation** — New file per day per context  
✅ **Tag for filtering** — Add tags for quick queries  

---

## 🚫 Anti-Patterns

❌ **No PII** — Filter sensitive data before logging  
❌ **No free-text** — Use structured fields only  
❌ **No large objects** — Reference artifact IDs  
❌ **No mixing types** — Keep agent traces ≠ ETL traces  
❌ **No manual edits** — Write once, read many  

---

## 🔧 Related Documentation

- **Observability Overview:** `docs/observability/README.md`
- **Coach Telemetry:** `.coach/README.md`
- **Monitoring & Alerts:** `docs/observability/OBSERVABILITY-AND-TRACES.md`

---

**Status:** ✅ Ready to Use  
**Last Updated:** 2026-06-18  
**Schema Version:** 1.0.0

---

## 📍 Start Here

1. **Read:** `QUICK-START.md` (5 minutes)
2. **Write:** Your first trace (10 minutes)
3. **Query:** Using cookbook examples (15 minutes)
4. **Integrate:** Into your system (30 minutes)

Happy tracing! 📊
