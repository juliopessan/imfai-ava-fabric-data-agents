# 📊 Trace Logs Repository

**Purpose:** Centralized storage for execution traces, telemetry, and analytics data  
**Format:** JSONL (JSON Lines) — append-only, queryable, timestamped  
**Scope:** Agents, workflows, ETL pipelines, quality gates, data migrations

---

## 📁 Directory Structure

```
.trace-logs/
├── README.md                          (this file)
├── trace-schema.json                  (validation schema)
├── agents/                            (agent execution traces)
├── workflows/                         (workflow orchestration traces)
├── etl/                              (ETL pipeline traces)
├── gates/                            (quality gate scoring traces)
├── migrations/                        (data migration traces)
├── analytics/                         (pre-aggregated metrics)
└── archive/                          (older traces, compressed)
```

---

## 📝 File Naming Convention

**Pattern:** `{trace_type}_{context}_{date}_{sequence}.jsonl`

**Examples:**
```
agents_migration-coordinator_2026-06-18_001.jsonl
workflows_clientebanco-wave2_2026-06-18_001.jsonl
etl_staging-to-delta_2026-06-18_001.jsonl
gates_gate1_2026-06-18_001.jsonl
migrations_clientebanco-wave2-entities_2026-06-18_001.jsonl
```

---

## 🔍 Trace Event Structure

Each line in a JSONL file is a complete trace event:

```json
{
  "timestamp": "2026-06-18T14:32:15.123456Z",
  "trace_id": "tr_bdf3e2c1-8f9a-42eb-b012-1a2b3c4d5e6f",
  "trace_type": "agent_execution",
  "context": {
    "agent_id": "migration-coordinator",
    "wave": "clientebanco-wave2",
    "gate": 1,
    "user": "data-engineer@company.com"
  },
  "operation": {
    "name": "spawn_agent",
    "duration_sec": 45.23,
    "status": "success",
    "error": null
  },
  "metrics": {
    "tokens_in": 2048,
    "tokens_out": 1024,
    "artifacts_generated": 3,
    "artifact_size_kb": 245
  },
  "tags": ["critical", "gate-1-validation"],
  "metadata": {
    "source": "migration-coordinator.py:1245",
    "version": "1.0.0"
  }
}
```

---

## 📊 Trace Types

| Type | File Path | Purpose | Typical Fields |
|------|-----------|---------|-----------------|
| **agent_execution** | `agents/` | Agent runs, task completion, token usage | agent_id, duration, tokens, status |
| **workflow_execution** | `workflows/` | Orchestrator decisions, hand-offs | workflow_id, stage, decision, path |
| **etl_operation** | `etl/` | Data pipeline runs, record counts | source, target, rows_processed, errors |
| **gate_scoring** | `gates/` | Quality gate results, scores | gate_num, artifacts, score, anti_patterns |
| **migration_event** | `migrations/` | Entity counts, STTM stability, wave progress | wave, entity_count, coverage, status |
| **performance_metric** | `analytics/` | Pre-aggregated hourly/daily stats | period, avg_duration, error_rate, throughput |

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
        "tags": context.get("tags", []),
        "metadata": {
            "source": __file__,
            "version": "1.0.0"
        }
    }
    
    # Determine file path based on trace type
    trace_dir = Path(".trace-logs") / context.get("category", trace_type)
    trace_dir.mkdir(parents=True, exist_ok=True)
    
    # Find or create today's file
    today = datetime.utcnow().strftime("%Y-%m-%d")
    trace_file = trace_dir / f"{trace_type}_{context.get('subcontext', 'general')}_{today}_001.jsonl"
    
    # Append trace event
    with open(trace_file, "a") as f:
        f.write(json.dumps(trace_event) + "\n")
    
    return trace_event

# Usage
write_trace(
    trace_type="agent_execution",
    context={
        "agent_id": "migration-coordinator",
        "wave": "clientebanco-wave2",
        "gate": 1,
        "category": "agents",
        "subcontext": "migration-coordinator",
        "tags": ["critical", "gate-1"]
    },
    operation={
        "name": "spawn_agent",
        "duration_sec": 45.23,
        "status": "success"
    },
    metrics={
        "tokens_in": 2048,
        "tokens_out": 1024,
        "artifacts_generated": 3
    }
)
```

### **Read & Query Traces (Python)**

```python
import json
from pathlib import Path
from datetime import datetime

def read_traces(trace_file: str, trace_type_filter: str = None):
    """Read JSONL trace file and optionally filter"""
    
    traces = []
    trace_path = Path(".trace-logs") / trace_file
    
    if not trace_path.exists():
        print(f"File not found: {trace_path}")
        return traces
    
    with open(trace_path, "r") as f:
        for line in f:
            if line.strip():
                event = json.loads(line)
                if trace_type_filter is None or event.get("trace_type") == trace_type_filter:
                    traces.append(event)
    
    return traces

# Usage
traces = read_traces("agents/agent_execution_migration-coordinator_2026-06-18_001.jsonl")
for trace in traces:
    print(f"{trace['timestamp']} | {trace['context']['agent_id']} | {trace['operation']['status']}")
```

---

## 📈 Analytics & Dashboards

Traces are designed for:

| Use Case | Query Example |
|----------|---|
| **Agent Performance** | Filter by agent_id, aggregate duration, tokens |
| **Error Tracking** | Filter by status != "success", extract error |
| **Cost Analysis** | Sum tokens × pricing_rate |
| **SLA Monitoring** | Track duration vs threshold |
| **Dependency Chains** | Follow trace_id across traces |

---

## 🔒 Data Retention & Cleanup

**Retention Policy:**
- **Hot:** Last 7 days (`.trace-logs/agents/`, `.trace-logs/workflows/`) — live analytics
- **Warm:** 7–30 days → compress + move to `archive/`
- **Cold:** >30 days → archive zip file with timestamp

**Cleanup Script:**
```bash
# Archive traces older than 7 days
find .trace-logs -name "*.jsonl" -mtime +7 -exec gzip {} \;
mv .trace-logs/*/*.gz .trace-logs/archive/
```

---

## 🎯 Best Practices

✅ **Always include timestamp** — ISO 8601 UTC format  
✅ **Unique trace_id** — UUID v4 for correlation  
✅ **Consistent context** — Include wave, gate, agent_id  
✅ **Minimal but complete** — Include what's needed for analysis  
✅ **Append-only** — Never modify existing traces  
✅ **Daily rotation** — One JSONL file per day per context  
✅ **Tag for queries** — Add tags for quick filtering  

---

## 🚫 Anti-Patterns

❌ **Don't store PII** — Filter sensitive data before logging  
❌ **Don't append to old files** — Create new file per day  
❌ **Don't modify traces** — Write once, read many (WORM)  
❌ **Don't store large objects** — Reference artifact IDs, not content  
❌ **Don't mix trace types** — Keep agent traces separate from ETL traces  

---

## 📚 Related Documentation

- **Observability Guide:** `docs/observability/README.md`
- **Coach Telemetry:** `.coach/README.md`
- **Analytics Setup:** `docs/observability/trace-logs/ANALYTICS-SETUP.md` (coming soon)
- **Query Cookbook:** `docs/observability/trace-logs/QUERY-COOKBOOK.md` (coming soon)

---

## 🔧 Integration Points

Traces should be written from:

| Source | Trace Type | Location |
|--------|-----------|----------|
| migration-coordinator | workflow_execution | workflows/ |
| quality-gate | gate_scoring | gates/ |
| ETL scripts | etl_operation | etl/ |
| Coach telemetry_collector | agent_execution | agents/ |
| Analytics aggregator | performance_metric | analytics/ |

---

**Status:** ✅ Ready to Use  
**Last Updated:** 2026-06-18  
**Schema Version:** 1.0.0
