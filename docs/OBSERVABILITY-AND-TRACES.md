# Observability & Distributed Traces — DMF v3

**Version:** 1.0  
**Date:** 2026-06-16  
**Owner:** SRE / Observability Lead  

---

## Purpose

Instrumentar **toda a cadeia agentic** (agent invoke → tool calls → sub-agents → validators) com traces distribuídos, permitindo:
- 🔍 **Root cause analysis:** Qual agente/tool causou o problema?
- 💰 **Cost attribution:** Quanto custa cada wave/gate/agente?
- 📊 **Drift detection:** Agent se comportando diferente de histórico?
- ⚡ **Performance optimization:** Onde estamos gastando tempo/tokens?

---

## Trace ID Propagation

### Architecture: Trace Context Flow

```
┌─ Entry Point: master-agent (*route command)
│  trace_id = uuid.uuid4()  → "a7f3-92c1-4e8b-11d7-5fk2m9p0"
│  
├─ Skill loaded: ava-dmf-data-quality@v2.1.3
│  span_id = uuid.uuid4()  → "skill-discovery-001"
│  parent_span_id = trace_id
│  
├─ Agent invoked: data-modeler
│  span_id = uuid.uuid4()  → "agent-modeler-001"
│  parent_span_id = trace_id
│
│  ├─ Perceive (LLM call)
│  │  span_id = "perceive-001"
│  │  parent_span_id = "agent-modeler-001"
│  │  events: {model, tokens_in, tokens_out, cost_usd, latency_ms}
│  │
│  ├─ Plan (internal reasoning)
│  │  span_id = "plan-001"
│  │  parent_span_id = "agent-modeler-001"
│  │
│  ├─ Tool Call: validate_data_contracts
│  │  span_id = "tool-001"
│  │  parent_span_id = "agent-modeler-001"
│  │  events: {tool_name, args, result, duration_ms, cost_usd}
│  │
│  ├─ Sub-Agent Invocation: quality-gate
│  │  span_id = "sub-agent-001"
│  │  parent_span_id = "agent-modeler-001"
│  │  → Passes trace_id (correlation!)
│  │
│  └─ Iterate/Escalate
│     span_id = "decision-001"
│     parent_span_id = "agent-modeler-001"
│     events: {success/escalate, reason, next_action}
│
└─ Return to caller
   Final metrics aggregated from all spans
```

### Trace Context Object (Python)

```python
from dataclasses import dataclass
from typing import Optional, Dict, List
import uuid
import time

@dataclass
class TraceContext:
    """Propagated across all agent calls."""
    trace_id: str = None  # Unique per top-level invocation
    parent_span_id: str = None  # Link to caller
    span_id: str = None  # This span's ID
    agent_id: str = None  # data-modeler, quality-gate, etc.
    wave_id: str = None  # clientebanco-g1
    gate: int = None  # 1, 2, 3
    session_id: str = None  # User session (if applicable)
    timestamp: str = None  # ISO 8601
    
    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())
        if not self.span_id:
            self.span_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
    
    def new_child_span(self, agent_id: str, span_name: str = None) -> "TraceContext":
        """Create child span, inherit trace_id."""
        return TraceContext(
            trace_id=self.trace_id,  # INHERIT
            parent_span_id=self.span_id,  # Link to me
            span_id=str(uuid.uuid4()),  # New span
            agent_id=agent_id or self.agent_id,
            wave_id=self.wave_id,
            gate=self.gate,
            session_id=self.session_id
        )

    def to_headers(self) -> Dict[str, str]:
        """For HTTP propagation (traceparent format)."""
        return {
            "traceparent": f"00-{self.trace_id}-{self.span_id}-01",
            "x-wave-id": self.wave_id or "",
            "x-gate": str(self.gate) or ""
        }

    @staticmethod
    def from_headers(headers: Dict[str, str]) -> "TraceContext":
        """Extract from HTTP headers."""
        traceparent = headers.get("traceparent", "")
        if traceparent:
            parts = traceparent.split("-")
            trace_id = parts[1] if len(parts) > 1 else str(uuid.uuid4())
            span_id = parts[2] if len(parts) > 2 else str(uuid.uuid4())
        else:
            trace_id = str(uuid.uuid4())
            span_id = str(uuid.uuid4())
        
        return TraceContext(
            trace_id=trace_id,
            span_id=span_id,
            wave_id=headers.get("x-wave-id"),
            gate=int(headers.get("x-gate", 0)) or None
        )
```

---

## Span Event Schema

### Standard Span Types

#### 1. **Agent Invocation Span**
```json
{
  "span_type": "agent",
  "span_id": "agent-modeler-001",
  "parent_span_id": "trace-root",
  "agent_id": "data-modeler",
  "wave_id": "clientebanco-g1",
  "gate": 2,
  "timestamp_start": "2026-06-16T14:30:42.100Z",
  "timestamp_end": "2026-06-16T14:31:00.600Z",
  "duration_ms": 18500,
  "status": "success|escalated|failed",
  "escalation_reason": "trajectory_quality < 0.75",
  "children": [
    "perceive-001", "plan-001", "tool-001", "decision-001"
  ]
}
```

#### 2. **LLM Call Span** (Perceive)
```json
{
  "span_type": "llm_call",
  "span_id": "perceive-001",
  "parent_span_id": "agent-modeler-001",
  "model": "claude-opus-4",
  "timestamp_start": "2026-06-16T14:30:42.200Z",
  "timestamp_end": "2026-06-16T14:30:50.300Z",
  "duration_ms": 8100,
  "tokens_input": 12450,
  "tokens_output": 3200,
  "cost_usd": 0.18,
  "temperature": 0.7,
  "max_tokens": 4096,
  "stop_reason": "end_turn",
  "cache_hits": 0,
  "cache_creation": 2,
  "cache_cost_usd": 0.02
}
```

#### 3. **Tool Execution Span**
```json
{
  "span_type": "tool_call",
  "span_id": "tool-001",
  "parent_span_id": "agent-modeler-001",
  "tool_name": "validate_data_contracts",
  "tool_category": "governance",
  "timestamp_start": "2026-06-16T14:30:51.400Z",
  "timestamp_end": "2026-06-16T14:30:53.700Z",
  "duration_ms": 2300,
  "inputs": {
    "file_path": "projects/clientebanco/outputs/gate2/data-contracts.yaml",
    "strict_mode": true
  },
  "outputs": {
    "passed": false,
    "errors": 3,
    "warnings": 45,
    "validation_score": 0.68
  },
  "execution_environment": "sandbox-ci-pipeline",
  "cost_usd": 0.05,
  "status": "success"
}
```

#### 4. **Sub-Agent Invocation Span**
```json
{
  "span_type": "sub_agent",
  "span_id": "sub-agent-001",
  "parent_span_id": "agent-modeler-001",
  "sub_agent_id": "quality-gate",
  "delegation_reason": "Evaluate trajectory compliance",
  "timestamp_start": "2026-06-16T14:30:54.000Z",
  "timestamp_end": "2026-06-16T14:30:58.500Z",
  "duration_ms": 4500,
  "cost_usd": 0.12,
  "status": "success",
  "result": {
    "trajectory_quality": 0.82,
    "compliance": 0.91
  },
  "trace_id_passed": "a7f3-92c1-4e8b-11d7-5fk2m9p0"
}
```

#### 5. **Decision Span** (Iterate or Escalate)
```json
{
  "span_type": "decision",
  "span_id": "decision-001",
  "parent_span_id": "agent-modeler-001",
  "timestamp": "2026-06-16T14:30:59.000Z",
  "decision": "escalate_to_human",
  "reason": "warnings > 10 && trajectory_quality < 0.75",
  "checkpoint_applied": "gate_2_escalation_rule_1",
  "priority": "medium",
  "escalated_to": "data-architect",
  "sla_minutes": 60
}
```

---

## Observability Pipeline

### Step 1: Span Generation (In-Process)

```python
# Inside agent orchestration loop
from datetime import datetime

class SpanCollector:
    def __init__(self, trace_context: TraceContext):
        self.trace_context = trace_context
        self.spans = []
    
    def record_span(self, span_data: Dict):
        """Collect span locally."""
        self.spans.append({
            **span_data,
            "trace_id": self.trace_context.trace_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    def flush_to_insights(self, app_insights_client):
        """Send batch to Application Insights."""
        for span in self.spans:
            app_insights_client.track_trace(
                message=f"span: {span['span_type']}",
                severity_level=SeverityLevel.Information,
                properties=span
            )
```

### Step 2: Aggregation (Application Insights)

```kusto
// KQL Query: Aggregate all spans for a trace
traces
| where tostring(customDimensions["trace_id"]) == "a7f3-92c1-4e8b-11d7-5fk2m9p0"
| project 
    span_id = tostring(customDimensions["span_id"]),
    agent = tostring(customDimensions["agent_id"]),
    span_type = tostring(customDimensions["span_type"]),
    duration_ms = tolong(customDimensions["duration_ms"]),
    cost_usd = todouble(customDimensions["cost_usd"])
| summarize 
    total_duration_ms = sum(duration_ms),
    total_cost_usd = sum(cost_usd),
    span_count = count()
    by agent
```

### Step 3: Real-time Dashboard

**Dashboard: "Agent Observatory" (PowerBI / Grafana)**

```
┌─ Trace Details (Input: trace_id)
│  ├─ Timeline: Gantt chart of all spans (see parallelization)
│  ├─ Cost Breakdown: pie chart {LLM, tools, sub-agents, overhead}
│  ├─ Decision Tree: "Why did it escalate?"
│  └─ Audit Trail: Full decision log
│
├─ Agent Performance (Per-Agent Aggregate)
│  ├─ Success Rate: last 7 days
│  ├─ Avg Cost per Invocation
│  ├─ Trajectory Quality Trend
│  └─ Escalation Rate
│
└─ Wave Health (Per-Wave Aggregate)
   ├─ Gate 1, 2, 3 pass rates
   ├─ Cost per gate
   └─ Time to completion
```

---

## Cost Attribution

### Cost Model

```
Total_Cost_Per_Trace = Σ (LLM_tokens_cost + Tool_execution_cost + Sub_agent_cost)

LLM_tokens_cost = (tokens_input / 1M × $3) + (tokens_output / 1M × $15)  # Claude Opus 4

Tool_execution_cost = Duration_sec × $0.0001  # Sandbox/compute

Sub_agent_cost = Sub_agent_trace_cost  # Recursive
```

### Trace Cost Reporting

```json
{
  "trace_id": "a7f3-92c1-4e8b-11d7-5fk2m9p0",
  "wave": "clientebanco-g1",
  "gate": 2,
  "cost_breakdown": {
    "llm_tokens": {
      "input": 12450,
      "output": 3200,
      "cost_usd": 0.18
    },
    "tools": [
      {"name": "validate_data_contracts", "cost_usd": 0.05},
      {"name": "validate_data_model", "cost_usd": 0.03}
    ],
    "sub_agents": [
      {"agent": "quality-gate", "cost_usd": 0.12}
    ],
    "total_usd": 0.48,
    "attributes": {
      "agent": "data-modeler",
      "success": false,
      "escalated": true
    }
  }
}
```

### Monthly Cost Report

```
Agent              | Invocations | Avg Cost | Total Cost | Success Rate
data-modeler       | 142         | $0.52    | $73.84     | 89%
quality-gate       | 187         | $0.38    | $71.06     | 94%
logic-extractor    | 98          | $0.61    | $59.78     | 72%
code-generator     | 76          | $0.44    | $33.44     | 91%
---
Total (Gate 2)     | 503         | $0.48    | $241.12    | 87%
```

---

## Drift Detection

### Baseline Metrics

For each agent, establish baseline during first 30 days:

```json
{
  "agent_id": "data-modeler",
  "gate": 2,
  "baseline_period": "2026-05-17T00:00Z to 2026-06-16T23:59Z",
  "metrics": {
    "avg_duration_sec": 18.5,
    "p95_duration_sec": 45.2,
    "avg_cost_usd": 0.52,
    "success_rate": 0.89,
    "escalation_rate": 0.11,
    "trajectory_quality_avg": 0.79,
    "trajectory_quality_stdev": 0.08
  }
}
```

### Drift Alert Triggers

```yaml
drift_rules:
  - metric: "success_rate"
    baseline_value: 0.89
    threshold_drop: 0.10  # Drop > 10% = alert
    severity: "critical"
    
  - metric: "avg_cost_usd"
    baseline_value: 0.52
    threshold_increase: 1.5  # Increase > 50% = alert
    severity: "high"
    
  - metric: "trajectory_quality_avg"
    baseline_value: 0.79
    threshold_drop: 0.15  # Drop > 15% = investigate
    severity: "medium"
```

**Alert Example:**
```
🔴 DRIFT ALERT: data-modeler (Gate 2)
   Metric: success_rate
   Baseline: 89% → Current: 75%
   Change: -14% (CRITICAL)
   Period: Last 7 days
   Action: Investigate agent behavior change; check harness updates.
```

---

## Privacy & Security

### Sensitive Data Masking

```python
SENSITIVE_PATTERNS = [
    r"password\s*=\s*['\"].*?['\"]",  # password="xxx"
    r"api[-_]?key\s*[:=]\s*['\"]?[\w-]+['\"]?",  # api_key: "xxx"
    r"(?:https?://)?(?:user:)?\w+:[\w-]+@",  # https://user:pass@host
]

def mask_sensitive_data(span_data: Dict) -> Dict:
    """Remove sensitive info from traces before sending to cloud."""
    for key, value in span_data.items():
        if isinstance(value, str):
            for pattern in SENSITIVE_PATTERNS:
                span_data[key] = re.sub(pattern, "***REDACTED***", value)
    return span_data
```

### Data Retention

- **Traces:** 30 days (hot storage in Application Insights)
- **Aggregates:** 90 days (cost reports, metrics)
- **Audit logs:** 1 year (compliance)

---

## Implementation Roadmap

- [ ] **Week 1:** Implement `TraceContext` class + propagation in orchestrator
- [ ] **Week 2:** Add span collection to agent loop + tool execution
- [ ] **Week 3:** Set up Application Insights pipeline + KQL queries
- [ ] **Week 4:** Build "Agent Observatory" dashboard (PowerBI)
- [ ] **Week 5:** Establish baseline metrics for all agents
- [ ] **Week 6:** Configure drift detection alerts
- [ ] **Week 7:** Cost attribution report (monthly)
- [ ] **Week 8:** Privacy review + data masking rules

---

**Related Docs:**
- `HARNESS-MANIFEST.md` (Observability component)
- `HUMAN-AGENT-CHECKPOINTS.md` (Use traces for escalation decisions)
