"""
Execution Telemetry System for Fabricae v3

Provides real-time tracking of:
- Execution time (wall clock)
- Token consumption estimation
- Cost calculation (Claude Haiku @ $0.80/M tokens input, $2.40/M tokens output)
- Agent actions
- Tool executions
- MCP calls
- RAG retrievals
- Memory lookups
- Cache hit rate

Usage:
    telemetry = ExecutionTelemetry(workflow_name="Migration Analysis", agent_name="discovery-scout")
    
    with telemetry.track_phase("Upstream Discovery", "Phase B"):
        # your code here
        pass
    
    telemetry.add_tool_call("Azure API", cost=0.005)
    telemetry.add_rag_retrieval(docs_retrieved=10, tokens_used=250)
    telemetry.add_memory_lookup(hits=3, misses=1)
    
    report = telemetry.generate_report()
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ExecutionTelemetry:
    """Track agent execution metrics and business outcomes."""

    def __init__(self, workflow_name: str, agent_name: str, output_dir: Optional[Path] = None):
        self.workflow_name = workflow_name
        self.agent_name = agent_name
        self.output_dir = Path(output_dir) if output_dir else Path(".")
        
        self.start_time = time.time()
        self.start_datetime = datetime.now()
        
        # Metrics
        self.input_tokens = 0
        self.output_tokens = 0
        self.tool_calls: List[Dict[str, Any]] = []
        self.mcp_calls: List[Dict[str, Any]] = []
        self.rag_retrievals: List[Dict[str, Any]] = []
        self.memory_lookups: List[Dict[str, Any]] = []
        self.phases: List[Dict[str, Any]] = []
        self.business_outcomes: List[Dict[str, Any]] = []
        
        # Pricing (Claude Haiku)
        self.price_per_input_mtok = 0.80  # $0.80 per million tokens
        self.price_per_output_mtok = 2.40  # $2.40 per million tokens
        
        self.current_phase = None
        self.current_phase_start = None
        self.cache_hit_rate = 0.0

    def track_phase(self, phase_name: str, phase_id: str):
        """Context manager to track a phase."""
        return PhaseTracker(self, phase_name, phase_id)

    def add_tool_call(self, tool_name: str, status: str = "success", cost: float = 0.0, 
                      duration: float = 0.0, tokens_used: int = 0):
        """Record a tool execution."""
        self.tool_calls.append({
            "tool": tool_name,
            "status": status,
            "cost": cost,
            "duration": duration,
            "tokens": tokens_used,
            "timestamp": datetime.now().isoformat()
        })
        self.output_tokens += tokens_used

    def add_mcp_call(self, endpoint: str, method: str = "GET", status_code: int = 200, 
                    duration: float = 0.0, tokens_used: int = 0):
        """Record an MCP server call."""
        self.mcp_calls.append({
            "endpoint": endpoint,
            "method": method,
            "status": status_code,
            "duration": duration,
            "tokens": tokens_used,
            "timestamp": datetime.now().isoformat()
        })
        self.output_tokens += tokens_used

    def add_rag_retrieval(self, index_name: str, docs_retrieved: int, 
                         query_tokens: int = 0, retrieval_tokens: int = 0):
        """Record a RAG retrieval."""
        self.rag_retrievals.append({
            "index": index_name,
            "docs_retrieved": docs_retrieved,
            "query_tokens": query_tokens,
            "retrieval_tokens": retrieval_tokens,
            "timestamp": datetime.now().isoformat()
        })
        self.input_tokens += query_tokens
        self.output_tokens += retrieval_tokens

    def add_memory_lookup(self, memory_type: str, query: str, hits: int, misses: int, tokens_used: int = 0):
        """Record a memory lookup."""
        self.memory_lookups.append({
            "type": memory_type,
            "query": query,
            "hits": hits,
            "misses": misses,
            "tokens": tokens_used,
            "timestamp": datetime.now().isoformat()
        })
        self.output_tokens += tokens_used
        
        # Update cache hit rate
        total_lookups = hits + misses
        if total_lookups > 0:
            self.cache_hit_rate = hits / total_lookups

    def add_business_outcome(self, category: str, metric: str, value: Any, impact: str):
        """Record a business outcome from agent action."""
        self.business_outcomes.append({
            "category": category,
            "metric": metric,
            "value": value,
            "impact": impact,
            "timestamp": datetime.now().isoformat()
        })

    def record_phase(self, phase_name: str, phase_id: str, duration: float, status: str = "success"):
        """Record a completed phase."""
        self.phases.append({
            "name": phase_name,
            "id": phase_id,
            "duration": duration,
            "status": status
        })

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        return time.time() - self.start_time

    @property
    def total_tokens(self) -> int:
        """Get total tokens (input + output)."""
        return self.input_tokens + self.output_tokens

    @property
    def execution_cost(self) -> float:
        """Calculate execution cost in USD."""
        input_cost = (self.input_tokens / 1_000_000) * self.price_per_input_mtok
        output_cost = (self.output_tokens / 1_000_000) * self.price_per_output_mtok
        return input_cost + output_cost

    @property
    def status(self) -> str:
        """Determine status based on execution progress."""
        total_events = len(self.tool_calls) + len(self.mcp_calls) + len(self.rag_retrievals)
        if total_events == 0:
            return "Starting..."
        elif self.elapsed_time < 10:
            return "In progress (0-10s)"
        elif total_events > 5:
            return "Almost completed"
        else:
            return "Processing"

    def generate_timeline(self) -> List[Dict[str, Any]]:
        """Generate execution timeline with all events."""
        timeline = []
        
        # Collect all timestamped events
        all_events = []
        
        for tool in self.tool_calls:
            all_events.append({
                "timestamp": tool["timestamp"],
                "type": "Tool Execution",
                "detail": f"{tool['tool']} ({tool['status']})",
                "icon": "🔧"
            })
        
        for mcp in self.mcp_calls:
            all_events.append({
                "timestamp": mcp["timestamp"],
                "type": "MCP Request",
                "detail": f"{mcp['endpoint']} ({mcp['status']})",
                "icon": "📡"
            })
        
        for rag in self.rag_retrievals:
            all_events.append({
                "timestamp": rag["timestamp"],
                "type": "RAG Retrieval",
                "detail": f"{rag['index']}: {rag['docs_retrieved']} docs",
                "icon": "📚"
            })
        
        for mem in self.memory_lookups:
            all_events.append({
                "timestamp": mem["timestamp"],
                "type": "Memory Lookup",
                "detail": f"{mem['type']}: {mem['hits']} hits, {mem['misses']} misses",
                "icon": "💾"
            })
        
        # Sort by timestamp
        all_events.sort(key=lambda x: x["timestamp"])
        
        return all_events

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive execution report."""
        elapsed = self.elapsed_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
        
        return {
            "metadata": {
                "workflow": self.workflow_name,
                "agent": self.agent_name,
                "start_time": self.start_datetime.isoformat(),
                "elapsed_time": time_str,
                "elapsed_seconds": elapsed
            },
            "metrics": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "total_tokens": self.total_tokens,
                "cost_usd": round(self.execution_cost, 4),
                "status": self.status,
                "cache_hit_rate": round(self.cache_hit_rate, 2)
            },
            "execution": {
                "tool_calls": len(self.tool_calls),
                "mcp_calls": len(self.mcp_calls),
                "rag_retrievals": len(self.rag_retrievals),
                "memory_lookups": len(self.memory_lookups),
                "phases_completed": len(self.phases)
            },
            "timeline": self.generate_timeline(),
            "phases": self.phases,
            "business_outcomes": self.business_outcomes,
            "details": {
                "tools": self.tool_calls,
                "mcp": self.mcp_calls,
                "rag": self.rag_retrievals,
                "memory": self.memory_lookups
            }
        }

    def to_json(self, output_file: Optional[Path] = None) -> str:
        """Export telemetry as JSON."""
        report = self.generate_report()
        json_str = json.dumps(report, indent=2)
        
        if output_file:
            output_file = Path(output_file)
            output_file.write_text(json_str)
        
        return json_str

    def to_html_panel(self) -> str:
        """Generate HTML side panel with metrics."""
        report = self.generate_report()
        metrics = report["metrics"]
        execution = report["execution"]
        
        html = f"""
        <div class="execution-panel">
            <div class="panel-header">
                <h3>Execution Metrics</h3>
            </div>
            
            <div class="metrics-summary">
                <div class="metric-item">
                    <span class="metric-icon">⏳</span>
                    <div class="metric-content">
                        <div class="metric-label">Execution Time</div>
                        <div class="metric-value">{metrics['elapsed_time']}</div>
                    </div>
                </div>
                
                <div class="metric-item">
                    <span class="metric-icon">🔤</span>
                    <div class="metric-content">
                        <div class="metric-label">Token Consumption</div>
                        <div class="metric-value">{metrics['total_tokens']:,} tokens</div>
                        <small>in: {metrics['input_tokens']:,} | out: {metrics['output_tokens']:,}</small>
                    </div>
                </div>
                
                <div class="metric-item">
                    <span class="metric-icon">💰</span>
                    <div class="metric-content">
                        <div class="metric-label">Cost</div>
                        <div class="metric-value">${metrics['cost_usd']:.4f}</div>
                    </div>
                </div>
                
                <div class="metric-item">
                    <span class="metric-icon">✓</span>
                    <div class="metric-content">
                        <div class="metric-label">Status</div>
                        <div class="metric-value">{metrics['status']}</div>
                    </div>
                </div>
            </div>
            
            <div class="execution-details">
                <h4>Execution Details</h4>
                <ul>
                    <li><strong>Agent:</strong> {report['metadata']['agent']}</li>
                    <li><strong>Workflow:</strong> {report['metadata']['workflow']}</li>
                    <li><strong>Tools Executed:</strong> {execution['tool_calls']}</li>
                    <li><strong>MCP Calls:</strong> {execution['mcp_calls']}</li>
                    <li><strong>RAG Retrievals:</strong> {execution['rag_retrievals']}</li>
                    <li><strong>Memory Lookups:</strong> {execution['memory_lookups']}</li>
                    <li><strong>Cache Hit Rate:</strong> {metrics['cache_hit_rate']*100:.1f}%</li>
                </ul>
            </div>
        </div>
        """
        return html


class PhaseTracker:
    """Context manager for tracking execution phases."""

    def __init__(self, telemetry: ExecutionTelemetry, phase_name: str, phase_id: str):
        self.telemetry = telemetry
        self.phase_name = phase_name
        self.phase_id = phase_id
        self.phase_start = None

    def __enter__(self):
        self.phase_start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.phase_start
        status = "error" if exc_type else "success"
        self.telemetry.record_phase(self.phase_name, self.phase_id, duration, status)
        return False


# Example usage
if __name__ == "__main__":
    telemetry = ExecutionTelemetry("Data Migration", "discovery-scout")
    
    with telemetry.track_phase("Inventory Discovery", "Phase B"):
        time.sleep(0.5)
        telemetry.add_tool_call("Azure API", "success", 0.005, 0.3, 150)
        telemetry.add_rag_retrieval("docs-index", 15, 45, 120)
        telemetry.add_memory_lookup("architecture", "previous decisions", 3, 1, 50)
        telemetry.add_business_outcome("Inventory", "Entities discovered", 545, "Complete legacy mapping")
    
    report = telemetry.generate_report()
    print(json.dumps(report, indent=2))
