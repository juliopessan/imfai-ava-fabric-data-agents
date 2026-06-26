# 🔍 Trace Logs Query Cookbook

**Purpose:** Common analytical queries for trace logs  
**Format:** Python code snippets  
**Status:** Ready to copy & adapt

---

## 📊 Cost Analysis

### Total Cost Today
```python
import json
from pathlib import Path
from datetime import datetime

def total_cost_today():
    total = 0
    today = datetime.utcnow().strftime("%Y-%m-%d")
    
    for f in Path(".trace-logs").rglob(f"*_{today}_*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                total += event.get("metrics", {}).get("cost_usd", 0)
    
    return total

cost = total_cost_today()
print(f"💰 Cost today: ${cost:.2f}")
```

### Cost by Agent
```python
import json
from pathlib import Path
from collections import defaultdict

def cost_by_agent():
    costs = defaultdict(float)
    
    for f in Path(".trace-logs/agents").glob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                agent = event["context"].get("agent_id", "unknown")
                costs[agent] += event.get("metrics", {}).get("cost_usd", 0)
    
    return dict(sorted(costs.items(), key=lambda x: x[1], reverse=True))

costs = cost_by_agent()
for agent, cost in costs.items():
    print(f"{agent}: ${cost:.2f}")
```

### Cost by Wave
```python
import json
from pathlib import Path
from collections import defaultdict

def cost_by_wave():
    costs = defaultdict(float)
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                wave = event["context"].get("wave", "unknown")
                costs[wave] += event.get("metrics", {}).get("cost_usd", 0)
    
    return dict(sorted(costs.items(), key=lambda x: x[1], reverse=True))

costs = cost_by_wave()
for wave, cost in costs.items():
    print(f"{wave}: ${cost:.2f}")
```

---

## ⏱️ Performance Analysis

### Average Duration by Agent
```python
import json
from pathlib import Path
from collections import defaultdict

def avg_duration_by_agent():
    stats = defaultdict(list)
    
    for f in Path(".trace-logs/agents").glob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                agent = event["context"].get("agent_id")
                duration = event["operation"].get("duration_sec")
                if duration is not None:
                    stats[agent].append(duration)
    
    results = {}
    for agent, durations in stats.items():
        results[agent] = {
            "avg": sum(durations) / len(durations),
            "min": min(durations),
            "max": max(durations),
            "count": len(durations)
        }
    
    return results

stats = avg_duration_by_agent()
for agent, data in stats.items():
    print(f"{agent}: {data['avg']:.1f}s avg (min: {data['min']:.1f}s, max: {data['max']:.1f}s, n={data['count']})")
```

### Slowest Operations
```python
import json
from pathlib import Path

def slowest_operations(top_n: int = 10):
    operations = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                operations.append({
                    "timestamp": event.get("timestamp"),
                    "name": event["operation"].get("name"),
                    "duration": event["operation"].get("duration_sec", 0),
                    "agent": event["context"].get("agent_id", "n/a"),
                    "wave": event["context"].get("wave", "n/a")
                })
    
    # Sort by duration descending
    operations.sort(key=lambda x: x["duration"], reverse=True)
    return operations[:top_n]

slowest = slowest_operations(5)
print("🐢 Slowest 5 operations:")
for op in slowest:
    print(f"  {op['duration']:.1f}s | {op['name']} ({op['agent']} in {op['wave']})")
```

---

## ❌ Error Analysis

### Error Rate by Gate
```python
import json
from pathlib import Path
from collections import defaultdict

def error_rate_by_gate():
    gate_stats = defaultdict(lambda: {"total": 0, "failed": 0})
    
    for f in Path(".trace-logs/gates").glob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                gate = event["context"].get("gate")
                gate_stats[gate]["total"] += 1
                
                if event["operation"].get("status") != "success":
                    gate_stats[gate]["failed"] += 1
    
    return gate_stats

stats = error_rate_by_gate()
for gate, data in sorted(stats.items()):
    if data["total"] > 0:
        rate = (data["failed"] / data["total"]) * 100
        print(f"Gate {gate}: {rate:.1f}% error rate ({data['failed']}/{data['total']})")
```

### Failed Operations with Errors
```python
import json
from pathlib import Path

def failed_operations():
    failures = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                
                if event["operation"].get("status") != "success":
                    failures.append({
                        "timestamp": event.get("timestamp"),
                        "type": event.get("trace_type"),
                        "operation": event["operation"].get("name"),
                        "status": event["operation"].get("status"),
                        "error": event["operation"].get("error"),
                        "wave": event["context"].get("wave")
                    })
    
    return failures

failures = failed_operations()
print(f"❌ {len(failures)} failed operations:")
for f in failures:
    print(f"  {f['timestamp']} | {f['operation']} ({f['type']}) | {f['wave']}")
    if f['error']:
        print(f"    Error: {f['error'][:80]}...")
```

---

## 📈 Token Usage

### Total Tokens by Wave
```python
import json
from pathlib import Path
from collections import defaultdict

def tokens_by_wave():
    stats = defaultdict(lambda: {"in": 0, "out": 0})
    
    for f in Path(".trace-logs/agents").glob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                wave = event["context"].get("wave", "unknown")
                metrics = event.get("metrics", {})
                
                stats[wave]["in"] += metrics.get("tokens_in", 0)
                stats[wave]["out"] += metrics.get("tokens_out", 0)
    
    return stats

stats = tokens_by_wave()
for wave, data in sorted(stats.items()):
    total = data["in"] + data["out"]
    print(f"{wave}: {total:,} tokens ({data['in']:,} in, {data['out']:,} out)")
```

### Token Efficiency (output/input ratio)
```python
import json
from pathlib import Path

def token_efficiency():
    ratios = []
    
    for f in Path(".trace-logs/agents").glob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                metrics = event.get("metrics", {})
                
                tokens_in = metrics.get("tokens_in", 0)
                tokens_out = metrics.get("tokens_out", 0)
                
                if tokens_in > 0:
                    ratio = tokens_out / tokens_in
                    ratios.append({
                        "agent": event["context"].get("agent_id"),
                        "ratio": ratio,
                        "in": tokens_in,
                        "out": tokens_out
                    })
    
    # Sort by ratio descending (higher = more efficient)
    ratios.sort(key=lambda x: x["ratio"], reverse=True)
    
    print("Token efficiency (output/input):")
    for r in ratios[:10]:
        print(f"  {r['agent']}: {r['ratio']:.2f} ({r['out']:,}/{r['in']:,})")
```

---

## 📊 Aggregation & Summaries

### Daily Summary Report
```python
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def daily_summary(date: str = None):
    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    
    summary = {
        "date": date,
        "total_traces": 0,
        "total_cost": 0,
        "operations": defaultdict(int),
        "statuses": defaultdict(int),
        "agents": set(),
        "waves": set()
    }
    
    for f in Path(".trace-logs").rglob(f"*_{date}_*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                
                summary["total_traces"] += 1
                summary["total_cost"] += event.get("metrics", {}).get("cost_usd", 0)
                summary["operations"][event.get("trace_type")] += 1
                summary["statuses"][event["operation"].get("status")] += 1
                summary["agents"].add(event["context"].get("agent_id"))
                summary["waves"].add(event["context"].get("wave"))
    
    # Convert sets to lists for printing
    summary["agents"] = list(summary["agents"])
    summary["waves"] = list(summary["waves"])
    
    return summary

report = daily_summary()
print(f"📊 Summary for {report['date']}:")
print(f"  Total traces: {report['total_traces']}")
print(f"  Total cost: ${report['total_cost']:.2f}")
print(f"  Operations: {dict(report['operations'])}")
print(f"  Statuses: {dict(report['statuses'])}")
print(f"  Agents: {', '.join(report['agents'])}")
print(f"  Waves: {', '.join(report['waves'])}")
```

### Wave Completion Report
```python
import json
from pathlib import Path
from collections import defaultdict

def wave_report(wave: str):
    report = {
        "wave": wave,
        "traces_count": 0,
        "total_duration": 0,
        "total_cost": 0,
        "total_tokens": 0,
        "gates": defaultdict(int),
        "status_breakdown": defaultdict(int),
        "agents_involved": set()
    }
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                
                if event["context"].get("wave") == wave:
                    report["traces_count"] += 1
                    report["total_duration"] += event["operation"].get("duration_sec", 0)
                    
                    metrics = event.get("metrics", {})
                    report["total_cost"] += metrics.get("cost_usd", 0)
                    report["total_tokens"] += metrics.get("tokens_in", 0) + metrics.get("tokens_out", 0)
                    
                    gate = event["context"].get("gate")
                    if gate:
                        report["gates"][gate] += 1
                    
                    report["status_breakdown"][event["operation"].get("status")] += 1
                    report["agents_involved"].add(event["context"].get("agent_id"))
    
    report["agents_involved"] = list(report["agents_involved"])
    return report

report = wave_report("Financeiro-wave2")
print(f"📋 Wave Report: {report['wave']}")
print(f"  Traces: {report['traces_count']}")
print(f"  Duration: {report['total_duration']:.1f}s")
print(f"  Cost: ${report['total_cost']:.2f}")
print(f"  Tokens: {report['total_tokens']:,}")
print(f"  Agents: {', '.join(report['agents_involved'])}")
print(f"  Status: {dict(report['status_breakdown'])}")
print(f"  Gates: {dict(report['gates'])}")
```

---

## 🔗 Correlation Analysis

### Trace ID Correlation (track hand-offs)
```python
import json
from pathlib import Path

def find_correlated_traces(trace_id: str):
    """Find all traces with the same trace_id"""
    correlated = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                if event.get("trace_id") == trace_id:
                    correlated.append(event)
    
    return correlated

# Example: find chain of operations
traces = find_correlated_traces("tr_bdf3e2c1-8f9a-42eb-b012-1a2b3c4d5e6f")
for t in traces:
    print(f"{t['timestamp']} | {t['trace_type']} | {t['operation']['name']}")
```

### Find Cascading Failures
```python
import json
from pathlib import Path

def cascading_failures(window_sec: int = 60):
    """Find failures that happened within time window"""
    failures = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                if event["operation"].get("status") == "failure":
                    failures.append(event)
    
    # Group by time window
    cascades = []
    for i, failure in enumerate(failures):
        related = [f for f in failures if abs((failure["timestamp"] > f["timestamp"]) and (failure["timestamp"] < (f["timestamp"] + window_sec)))]
        if len(related) > 1:
            cascades.append(related)
    
    return cascades
```

---

## 💡 Tips & Tricks

### Filter by Tag
```python
import json
from pathlib import Path

def traces_with_tag(tag: str):
    """Get all traces with a specific tag"""
    results = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                if tag in event.get("tags", []):
                    results.append(event)
    
    return results

critical = traces_with_tag("critical")
print(f"Critical traces: {len(critical)}")
```

### Recent Traces Only
```python
import json
from pathlib import Path
from datetime import datetime, timedelta

def recent_traces(hours: int = 1):
    """Get traces from last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    results = []
    
    for f in Path(".trace-logs").rglob("*.jsonl"):
        with open(f) as file:
            for line in file:
                event = json.loads(line)
                ts = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
                if ts > cutoff:
                    results.append(event)
    
    return results

recent = recent_traces(hours=2)
print(f"Traces from last 2 hours: {len(recent)}")
```

---

**Ready to query?** Copy any snippet above and adapt for your use case!

**More help?** See `.trace-logs/README.md` or `QUICK-START.md`
