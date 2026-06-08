#!/usr/bin/env python
"""
Example: Token Metrics & Dashboard Server — Complete Workflow

This script demonstrates how to:
1. Collect token metrics from a migration wave
2. Generate a dashboard with token metrics
3. Start a web server to serve the dashboard via URL
"""

import sys
import importlib.util
from pathlib import Path

# Load modules with hyphens in name
reports_dir = Path(__file__).parent
sys.path.insert(0, str(reports_dir))

# Import token_metrics_collector
spec = importlib.util.spec_from_file_location("token_metrics_collector", 
                                               reports_dir / "token_metrics_collector.py")
token_metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(token_metrics)

# Import generate_dashboard (note: hyphenated name)
spec = importlib.util.spec_from_file_location("generate_dashboard", 
                                               reports_dir / "generate-dashboard.py")
gen_dash = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_dash)

TokenMetricsCollector = token_metrics.TokenMetricsCollector
DashboardGenerator = gen_dash.DashboardGenerator

def main():
    """Run example workflow."""
    print("\n" + "="*70)
    print("🚀 Token Metrics & Dashboard — Example Workflow")
    print("="*70 + "\n")

    # Step 1: Generate sample metrics
    print("📊 Step 1: Collecting Token Metrics...")
    metrics = TokenMetricsCollector.generate_sample_metrics()
    
    print(f"   ✅ Total tokens: {metrics['total']:,}")
    print(f"   ✅ Upstream:   {metrics['by_phase'].get('upstream', 0):,}")
    print(f"   ✅ Midstream:  {metrics['by_phase'].get('midstream', 0):,}")
    print(f"   ✅ Downstream: {metrics['by_phase'].get('downstream', 0):,}")
    print()

    # Step 2: Generate dashboard with metrics
    print("🎨 Step 2: Generating Dashboard...")
    gen = DashboardGenerator(None, None)
    gen.token_metrics = metrics
    gen.wave_config = {
        "wave_name": "DEMO-001",
        "entities": [
            {"name": "customer_dim", "rows": 1_500_000},
            {"name": "orders_fact", "rows": 25_000_000},
            {"name": "product_dim", "rows": 50_000},
        ]
    }
    gen.gate_scores = {
        "gate1": {"score": 0.92, "status": "approved"},
        "gate2": {"score": 0.78, "status": "in_review"},
        "gate3": {"score": None, "status": "pending"},
    }
    
    output_path = "example-dashboard.html"
    gen.generate(output_path)
    print(f"   ✅ Dashboard created: {output_path}")
    print()

    # Step 3: Show server startup command
    print("🌐 Step 3: Starting Dashboard Server...")
    print(f"   Run this command to start the web server:")
    print()
    print(f"   $ python dashboard_server.py --port 8000")
    print()
    print(f"   Then open: http://127.0.0.1:8000")
    print(f"   API:       http://127.0.0.1:8000/api/metrics")
    print()

    # Step 4: Show cost analysis
    print("💰 Step 4: Cost Analysis")
    total_tokens = metrics['total']
    total_mtokens = total_tokens / 1_000_000
    cost_usd = total_mtokens * 0.0015
    print(f"   Total tokens: {total_tokens:,}")
    print(f"   M tokens: {total_mtokens:.2f}M")
    print(f"   Rate: $0.001500 per M tokens (GPT-4)")
    print(f"   Estimated cost: ${cost_usd:.2f} USD")
    print()

    # Step 5: Show top agents
    print("🏆 Step 5: Top Agents by Token Usage")
    agents_sorted = sorted(
        metrics['by_agent'].items(),
        key=lambda x: x[1]['tokens'],
        reverse=True
    )[:5]
    for i, (agent, data) in enumerate(agents_sorted, 1):
        print(f"   {i}. {agent:30s} : {data['tokens']:>8,} tokens ({data['phase']})")
    print()

    print("="*70)
    print("✅ Workflow complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
