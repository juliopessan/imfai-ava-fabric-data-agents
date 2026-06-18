#!/usr/bin/env python3
"""
Dashboard Server — Serve executive dashboard with live token metrics
Lightweight Flask app that generates HTML reports with dynamic token data.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


class DashboardServer:
    """Serve executive dashboard with live metrics."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """Initialize dashboard server."""
        self.host = host
        self.port = port
        self.app = Flask(__name__) if FLASK_AVAILABLE else None
        self.metrics = {}
        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes."""
        if not self.app:
            return

        @self.app.route("/")
        def dashboard():
            """Serve main dashboard."""
            html = self._generate_dashboard_html()
            return html

        @self.app.route("/api/metrics")
        def metrics_api():
            """JSON API for metrics."""
            return jsonify(self.metrics)

        @self.app.route("/health")
        def health():
            """Health check."""
            return jsonify({"status": "ok", "timestamp": Path.cwd()})

    def _generate_dashboard_html(self) -> str:
        """Generate HTML dashboard with embedded metrics."""
        from token_metrics_collector import TokenMetricsCollector

        # Get or generate metrics
        if not self.metrics:
            self.metrics = TokenMetricsCollector.generate_sample_metrics()

        # Build metrics HTML
        metrics_html = self._build_metrics_section()

        # Load base dashboard
        dashboard_path = Path(__file__).parent / "executive-dashboard.html"
        html = dashboard_path.read_text(encoding='utf-8')

        # Insert metrics section after "Performance Indicators"
        insertion_point = "<!-- KEY METRICS & PERFORMANCE -->"
        metrics_section = f"""
        <!-- TOKEN USAGE METRICS -->
        <section class="ava-section">
            <div class="ava-accent-bar"></div>
            <h2>Token Usage Analytics</h2>
            <p>Real-time token consumption metrics across all migration agents and phases.</p>
            
            {metrics_html}
        </section>
        """

        html = html.replace(insertion_point, insertion_point + "\n" + metrics_section)
        return html

    def _build_metrics_section(self) -> str:
        """Build HTML metrics section from data."""
        metrics = self.metrics

        # Phase breakdown
        phase_rows = ""
        total_tokens = metrics.get("total", 0)
        for phase, tokens in metrics.get("by_phase", {}).items():
            pct = (tokens / total_tokens * 100) if total_tokens > 0 else 0
            width = int(pct)
            phase_rows += f"""
            <div style="margin-bottom: var(--ava-space-4);">
                <div style="display: flex; justify-content: space-between; margin-bottom: var(--ava-space-2);">
                    <span style="font-weight: 600; text-transform: capitalize;">{phase}</span>
                    <span style="font-size: 12px; color: var(--ava-grey-50);">{tokens:,} tokens ({pct:.1f}%)</span>
                </div>
                <div class="ava-progress">
                    <div class="ava-progress__bar" style="width: {width}%"></div>
                </div>
            </div>
            """

        # Top agents
        agent_rows = ""
        for agent, data in sorted(
            metrics.get("by_agent", {}).items(),
            key=lambda x: x[1]["tokens"],
            reverse=True,
        )[:5]:
            agent_rows += f"""
            <tr>
                <td><strong>{agent}</strong></td>
                <td>{data.get('phase', 'unknown')}</td>
                <td>{data.get('tokens', 0):,}</td>
                <td>{data.get('calls', 0)}</td>
            </tr>
            """

        # Cost estimate (GPT pricing)
        total_mtokens = total_tokens / 1_000_000
        cost_usd = round(total_mtokens * 0.0015, 2)

        return f"""
        <div class="ava-grid ava-grid--2col">
            <div class="ava-card">
                <h5>📊 Phase Distribution</h5>
                {phase_rows}
            </div>
            <div class="ava-card">
                <h5>💰 Cost Analysis</h5>
                <div style="font-size: 32px; font-weight: 700; color: var(--ava-orange); margin-bottom: var(--ava-space-2);">${cost_usd}</div>
                <p style="font-size: 13px; color: var(--ava-grey-60); margin-bottom: var(--ava-space-3);">
                    Total estimated cost (GPT-4 pricing)
                </p>
                <table style="font-size: 12px; width: 100%; line-height: 1.8;">
                    <tr>
                        <td>Total Tokens:</td>
                        <td style="text-align: right;"><strong>{total_tokens:,}</strong></td>
                    </tr>
                    <tr>
                        <td>Million Tokens:</td>
                        <td style="text-align: right;"><strong>{total_mtokens:.2f}M</strong></td>
                    </tr>
                    <tr>
                        <td>Rate:</td>
                        <td style="text-align: right;"><strong>$0.0015/MTok</strong></td>
                    </tr>
                </table>
            </div>
        </div>

        <div class="ava-grid ava-grid--1col ava-mt-6">
            <div class="ava-card">
                <h5>🤖 Top Agents by Token Consumption</h5>
                <table class="ava-table">
                    <thead>
                        <tr>
                            <th>Agent</th>
                            <th>Phase</th>
                            <th>Tokens</th>
                            <th>Calls</th>
                        </tr>
                    </thead>
                    <tbody>
                        {agent_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def run(self, debug: bool = False):
        """Start the Flask server."""
        if not self.app:
            print("❌ Flask not installed. Install with: pip install flask")
            return

        url = f"http://{self.host}:{self.port}"
        print(f"\n🚀 Dashboard Server Starting")
        print(f"   URL: {url}")
        print(f"   API: {url}/api/metrics")
        print(f"   Health: {url}/health\n")

        self.app.run(host=self.host, port=self.port, debug=debug)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Serve executive dashboard with token metrics")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--metrics", help="Path to metrics JSON file")
    args = parser.parse_args()

    server = DashboardServer(host=args.host, port=args.port)

    # Load custom metrics if provided
    if args.metrics:
        try:
            server.metrics = json.loads(Path(args.metrics).read_text(encoding='utf-8'))
            print(f"✅ Loaded metrics from {args.metrics}")
        except Exception as e:
            print(f"⚠️  Failed to load metrics: {e}")

    server.run(debug=args.debug)


if __name__ == "__main__":
    main()
