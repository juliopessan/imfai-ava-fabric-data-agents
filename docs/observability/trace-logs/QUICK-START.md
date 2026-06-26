# ⚡ Trace Logs — Quick Start (5 min)

**Goal:** Write your first trace in 5 minutes  
**Language:** Python  
**No setup needed** — just start writing!

---

## 🚀 Step 1: Create Helper Function (1 min)

Create a new file `src/shared/utils/trace_writer.py`:

```python
import json
from datetime import datetime
from pathlib import Path
import uuid

class TraceWriter:
    """Helper to write traces to JSONL files"""
    
    def __init__(self, base_dir: str = ".trace-logs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def write(self, trace_type: str, context: dict, operation: dict, metrics: dict = None):
        """Write a single trace event"""
        
        trace_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": f"tr_{uuid.uuid4()}",
            "trace_type": trace_type,
            "context": context,
            "operation": operation,
            "metrics": metrics or {},
            "metadata": {
                "source": __file__,
                "version": "1.0.0"
            }
        }
        
        # Determine file path
        category = context.get("category", trace_type)
        trace_dir = self.base_dir / category
        trace_dir.mkdir(parents=True, exist_ok=True)
        
        # Daily file naming
        today = datetime.utcnow().strftime("%Y-%m-%d")
        wave = context.get("wave", "general")
        trace_file = trace_dir / f"{trace_type}_{wave}_{today}_001.jsonl"
        
        # Append event (JSONL format)
        with open(trace_file, "a") as f:
            f.write(json.dumps(trace_event) + "\n")
        
        return trace_event

# Global instance
_writer = TraceWriter()

def write_trace(trace_type: str, context: dict, operation: dict, metrics: dict = None):
    """Global helper function"""
    return _writer.write(trace_type, context, operation, metrics)
```

---

## 📝 Step 2: Write Your First Trace (2 min)

In your agent/workflow/script:

```python
from src.shared.utils.trace_writer import write_trace

# After your operation completes:
write_trace(
    trace_type="agent_execution",
    context={
        "category": "agents",
        "agent_id": "my-agent",
        "wave": "Financeiro-wave2",
        "gate": 1,
        "tags": ["test", "quick-start"]
    },
    operation={
        "name": "spawn_agent",
        "duration_sec": 45.23,
        "status": "success"
    },
    metrics={
        "tokens_in": 2048,
        "tokens_out": 1024,
        "artifacts_generated": 3,
        "cost_usd": 0.15
    }
)

print("✅ Trace written!")
```

✅ This creates: `.trace-logs/agents/agent_execution_Financeiro-wave2_2026-06-18_001.jsonl`

---

## 🔍 Step 3: Read Your Traces (1 min)

```python
import json
from pathlib import Path

def read_traces(file_pattern: str):
    """Read JSONL traces"""
    traces = []
    
    for f in Path(".trace-logs").rglob(file_pattern):
        with open(f, "r") as file:
            for line in file:
                if line.strip():
                    traces.append(json.loads(line))
    
    return traces

# Query
traces = read_traces("agent_execution_*.jsonl")
for t in traces:
    print(f"{t['timestamp']} | {t['context']['agent_id']} | {t['operation']['status']}")
```

Output:
```
2026-06-18T14:32:15.123456Z | my-agent | success
```

---

## 📊 Step 4: Quick Analytics (1 min)

```python
# Total cost today
total_cost = sum(
    t.get("metrics", {}).get("cost_usd", 0)
    for t in traces
)
print(f"Cost today: ${total_cost:.2f}")

# Average duration
avg_duration = sum(
    t.get("operation", {}).get("duration_sec", 0)
    for t in traces
) / len(traces) if traces else 0
print(f"Avg duration: {avg_duration:.1f}s")

# Error rate
errors = sum(1 for t in traces if t.get("operation", {}).get("status") != "success")
error_rate = (errors / len(traces) * 100) if traces else 0
print(f"Error rate: {error_rate:.1f}%")
```

---

## 🎯 Trace Type Quickref

### **Agent Execution**
```python
write_trace(
    trace_type="agent_execution",
    context={
        "category": "agents",
        "agent_id": "migration-coordinator",
        "wave": "Financeiro-wave2",
        "gate": 1
    },
    operation={
        "name": "spawn_agent",
        "status": "success",
        "duration_sec": 45.23
    },
    metrics={"tokens_in": 2048, "tokens_out": 1024}
)
```

### **Workflow Execution**
```python
write_trace(
    trace_type="workflow_execution",
    context={
        "category": "workflows",
        "pipeline": "Financeiro-tier1",
        "wave": "Financeiro-wave2"
    },
    operation={
        "name": "execute_stage",
        "status": "success",
        "duration_sec": 120.5
    },
    metrics={"decision": "proceed_to_gate2", "artifacts": 5}
)
```

### **ETL Operation**
```python
write_trace(
    trace_type="etl_operation",
    context={
        "category": "etl",
        "pipeline": "staging-to-delta",
        "wave": "Financeiro-wave2"
    },
    operation={
        "name": "load_entities",
        "status": "success",
        "duration_sec": 30.2
    },
    metrics={
        "rows_processed": 15000,
        "rows_failed": 0,
        "throughput": 496.7
    }
)
```

### **Gate Scoring**
```python
write_trace(
    trace_type="gate_scoring",
    context={
        "category": "gates",
        "gate": 1,
        "wave": "Financeiro-wave2"
    },
    operation={
        "name": "calculate_gatescore",
        "status": "success",
        "duration_sec": 12.5
    },
    metrics={
        "base_score": 0.88,
        "adjustment": -0.05,
        "final_score": 0.83
    }
)
```

---

## 📁 File Structure Created

After running your traces:

```
.trace-logs/
├── agents/
│   └── agent_execution_Financeiro-wave2_2026-06-18_001.jsonl
├── workflows/
├── etl/
├── gates/
└── migrations/
```

Each JSONL file contains one JSON object per line (append-only).

---

## 🚫 Common Mistakes

❌ **Forgetting `.isoformat() + "Z"`** on timestamp  
❌ **Modifying existing traces** — write new file instead  
❌ **Including PII** — filter before logging  
❌ **Large objects** — reference artifact IDs instead  
❌ **Free-text in operation.name** — use consistent naming  

---

## ✅ Done!

You now have:
- ✅ Trace writing working
- ✅ Traces in JSONL format
- ✅ Basic queries running
- ✅ Analytics capability

**Next steps:**
1. Integrate into your agent/workflow
2. Read `QUERY-COOKBOOK.md` for advanced queries
3. Set up dashboard (coming soon)

**Questions?** See `README.md` (this folder)

Happy tracing! 📊
