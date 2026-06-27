#!/usr/bin/env python3
"""
Analyze trace logs for patterns, errors, and insights
Detecta anomalias, bottlenecks, padrões de sucesso/falha
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import sys

def load_traces(jsonl_file):
    """Load all traces from a JSONL file"""
    traces = []
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    trace = json.loads(line.strip())
                    traces.append(trace)
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Error on line {line_num}: {e}")
                    print(f"   Content: {line[:100]}...")
    except FileNotFoundError:
        print(f"❌ File not found: {jsonl_file}")
        return []
    
    return traces

def analyze_traces(traces):
    """Analyze traces for patterns and errors"""
    
    if not traces:
        print("❌ No traces to analyze")
        return
    
    print("\n" + "="*80)
    print("📊 TRACE LOGS ANALYSIS — FINANCEIRO WAVE 2")
    print("="*80)
    
    # 1. OVERVIEW
    print(f"\n📈 OVERVIEW")
    print(f"  Total Events: {len(traces)}")
    print(f"  Date Range: {traces[0]['timestamp']} → {traces[-1]['timestamp']}")
    
    # 2. Trace Type Distribution
    print(f"\n📋 TRACE TYPE DISTRIBUTION")
    trace_types = defaultdict(int)
    for trace in traces:
        trace_types[trace.get('trace_type', 'unknown')] += 1
    
    for trace_type, count in sorted(trace_types.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(traces)) * 100
        print(f"  {trace_type:25} {count:3} ({pct:5.1f}%)")
    
    # 3. Status Distribution
    print(f"\n✅ STATUS DISTRIBUTION")
    statuses = defaultdict(int)
    for trace in traces:
        status = trace.get('operation', {}).get('status', 'unknown')
        statuses[status] += 1
    
    for status, count in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(traces)) * 100
        emoji = "✅" if status == "success" else "⚠️" if status == "partial" else "❌"
        print(f"  {emoji} {status:15} {count:3} ({pct:5.1f}%)")
    
    # 4. Performance Metrics
    print(f"\n⏱️  PERFORMANCE METRICS")
    durations = []
    for trace in traces:
        duration = trace.get('operation', {}).get('duration_sec')
        if duration is not None:
            durations.append(duration)
    
    if durations:
        min_dur = min(durations)
        max_dur = max(durations)
        avg_dur = sum(durations) / len(durations)
        print(f"  Min Duration: {min_dur:.2f}s")
        print(f"  Max Duration: {max_dur:.2f}s")
        print(f"  Avg Duration: {avg_dur:.2f}s")
        print(f"  Total Duration: {sum(durations):.2f}s")
    
    # 5. Token Usage
    print(f"\n📦 TOKEN USAGE")
    tokens_in = sum([t.get('metrics', {}).get('tokens_in', 0) for t in traces])
    tokens_out = sum([t.get('metrics', {}).get('tokens_out', 0) for t in traces])
    cost_usd = sum([t.get('metrics', {}).get('cost_usd', 0) for t in traces])
    
    print(f"  Total Input Tokens: {tokens_in:,}")
    print(f"  Total Output Tokens: {tokens_out:,}")
    print(f"  Total Tokens: {tokens_in + tokens_out:,}")
    print(f"  Estimated Cost: ${cost_usd:.4f} USD")
    if tokens_in > 0:
        input_output_ratio = tokens_out / tokens_in
        print(f"  Input/Output Ratio: 1:{input_output_ratio:.2f}")
    
    # 6. Agent Performance
    print(f"\n🤖 AGENT PERFORMANCE")
    agents = defaultdict(lambda: {"count": 0, "success": 0, "failure": 0, "avg_duration": 0, "durations": []})
    
    for trace in traces:
        agent_id = trace.get('context', {}).get('agent_id')
        if agent_id:
            agents[agent_id]["count"] += 1
            status = trace.get('operation', {}).get('status')
            if status == "success":
                agents[agent_id]["success"] += 1
            elif status == "failure":
                agents[agent_id]["failure"] += 1
            
            duration = trace.get('operation', {}).get('duration_sec')
            if duration is not None:
                agents[agent_id]["durations"].append(duration)
    
    for agent_id, stats in sorted(agents.items(), key=lambda x: x[1]["count"], reverse=True):
        success_rate = (stats["success"] / stats["count"]) * 100 if stats["count"] > 0 else 0
        avg_dur = sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else 0
        print(f"  {agent_id:30} | Runs: {stats['count']:3} | Success: {success_rate:5.1f}% | Avg: {avg_dur:6.2f}s")
    
    # 7. Error Analysis
    print(f"\n❌ ERROR ANALYSIS")
    errors = defaultdict(list)
    for trace in traces:
        status = trace.get('operation', {}).get('status')
        if status in ['failure', 'timeout', 'partial']:
            error = trace.get('operation', {}).get('error', 'N/A')
            error_type = trace.get('operation', {}).get('error_type', 'unknown')
            errors[error_type].append({
                'timestamp': trace.get('timestamp'),
                'agent': trace.get('context', {}).get('agent_id'),
                'error': error
            })
    
    if errors:
        for error_type, instances in sorted(errors.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {error_type} ({len(instances)} occurrences)")
            for instance in instances[:2]:  # Show first 2
                print(f"    • {instance['timestamp']} | {instance['agent']}: {instance['error'][:60]}")
            if len(instances) > 2:
                print(f"    ... and {len(instances) - 2} more")
    else:
        print("  ✅ No errors detected!")
    
    # 8. Wave & Gate Analysis
    print(f"\n🏢 WAVE & GATE ANALYSIS")
    waves = defaultdict(lambda: {"gates": set(), "count": 0})
    for trace in traces:
        wave = trace.get('context', {}).get('wave')
        gate = trace.get('context', {}).get('gate')
        if wave:
            waves[wave]["count"] += 1
            if gate:
                waves[wave]["gates"].add(gate)
    
    for wave, info in sorted(waves.items()):
        gates_str = ', '.join(str(g) for g in sorted(info["gates"])) if info["gates"] else "N/A"
        print(f"  {wave:30} | Events: {info['count']:3} | Gates: {gates_str}")
    
    # 9. Patterns & Anomalies
    print(f"\n🔍 PATTERNS & ANOMALIES")
    
    # Pattern 1: Long-running operations
    long_ops = [t for t in traces if t.get('operation', {}).get('duration_sec', 0) > avg_dur * 2]
    if long_ops:
        print(f"  ⚠️  Long-running operations ({len(long_ops)} detected):")
        for op in sorted(long_ops, key=lambda x: x.get('operation', {}).get('duration_sec', 0), reverse=True)[:3]:
            duration = op.get('operation', {}).get('duration_sec')
            agent = op.get('context', {}).get('agent_id', 'unknown')
            print(f"    • {agent}: {duration:.2f}s (baseline: {avg_dur:.2f}s)")
    
    # Pattern 2: Retries
    retries = [t for t in traces if t.get('operation', {}).get('retry_count', 0) > 0]
    if retries:
        print(f"  🔄 Retried operations ({len(retries)} detected):")
        for op in retries:
            retry_count = op.get('operation', {}).get('retry_count', 0)
            agent = op.get('context', {}).get('agent_id', 'unknown')
            print(f"    • {agent}: {retry_count} retries")
    
    # Pattern 3: Cost anomalies
    costs = [t.get('metrics', {}).get('cost_usd', 0) for t in traces if 'metrics' in t]
    if costs:
        avg_cost = sum(costs) / len(costs)
        expensive = [t for t in traces if t.get('metrics', {}).get('cost_usd', 0) > avg_cost * 3]
        if expensive:
            print(f"  💰 Expensive operations ({len(expensive)} detected, avg: ${avg_cost:.4f}):")
            for op in sorted(expensive, key=lambda x: x.get('metrics', {}).get('cost_usd', 0), reverse=True)[:3]:
                cost = op.get('metrics', {}).get('cost_usd', 0)
                agent = op.get('context', {}).get('agent_id', 'unknown')
                print(f"    • {agent}: ${cost:.4f} (vs avg ${avg_cost:.4f})")
    
    # Pattern 4: Data quality metrics
    print(f"  📊 Data Quality Metrics:")
    coverage_pcts = [t.get('metrics', {}).get('coverage_pct', 100) for t in traces if 'coverage_pct' in t.get('metrics', {})]
    error_rates = [t.get('metrics', {}).get('error_rate', 0) for t in traces if 'error_rate' in t.get('metrics', {})]
    
    if coverage_pcts:
        avg_coverage = sum(coverage_pcts) / len(coverage_pcts)
        print(f"    • Average Coverage: {avg_coverage:.2f}%")
    
    if error_rates:
        avg_error_rate = sum(error_rates) / len(error_rates)
        print(f"    • Average Error Rate: {avg_error_rate:.4f}")
    
    # 10. Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    
    issues = []
    
    if errors:
        issues.append(f"❌ Fix {len(errors)} error types affecting reliability")
    
    if long_ops:
        issues.append(f"⚠️  Optimize {len(long_ops)} long-running operations (>2x average)")
    
    if retries:
        issues.append(f"🔄 Investigate {len(retries)} operations requiring retries")
    
    failure_count = sum([1 for t in traces if t.get('operation', {}).get('status') in ['failure', 'timeout']])
    if failure_count > 0:
        failure_rate = (failure_count / len(traces)) * 100
        if failure_rate > 5:
            issues.append(f"🔴 Failure rate is {failure_rate:.1f}% — investigate root causes")
    
    if not issues:
        print("  ✅ Trace logs look healthy! No major issues detected.")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    
    print("\n" + "="*80 + "\n")

def main():
    trace_file = Path(".trace-logs/agents/agent_execution_financeiro-wave2_2026-06-18_example.jsonl")
    
    if not trace_file.exists():
        print(f"❌ Trace file not found: {trace_file}")
        print(f"   Looking in: {trace_file.absolute()}")
        sys.exit(1)
    
    print(f"📖 Loading traces from: {trace_file}")
    traces = load_traces(str(trace_file))
    
    if traces:
        analyze_traces(traces)
    else:
        print("❌ No traces loaded")

if __name__ == "__main__":
    main()
