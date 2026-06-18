#!/usr/bin/env python3
"""
Generate dynamic executive dashboard from wave config and gate scores.
Integrates real migration data and token metrics into HTML template.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class DashboardGenerator:
    """Generate Avanade-branded executive dashboard from migration data."""

    TEMPLATE_PATH = Path(__file__).parent / "executive-dashboard.html"
    OUTPUT_DIR = Path(__file__).parent

    def __init__(self, wave_config_path: str | None = None, gate_scores_path: str | None = None):
        """Initialize generator with optional data sources."""
        self.wave_config = self._load_json(wave_config_path) if wave_config_path else {}
        self.gate_scores = self._load_json(gate_scores_path) if gate_scores_path else {}
        self.token_metrics = {}
        self.timestamp = datetime.now().isoformat()

    def _load_json(self, path: str | None) -> Dict[str, Any]:
        """Safely load JSON file."""
        if not path:
            return {}
        try:
            p = Path(path)
            if p.exists():
                return json.loads(p.read_text())
        except Exception as e:
            print(f"⚠️  Failed to load {path}: {e}", file=sys.stderr)
        return {}

    def generate(self, output_path: str | None = None) -> str:
        """Generate HTML dashboard with live data."""
        html = self.TEMPLATE_PATH.read_text(encoding='utf-8')

        # Insert generated timestamp
        html = html.replace(
            "<!-- GENERATED_AT -->",
            f"<!-- Generated: {self.timestamp} -->"
        )

        # Update metrics if wave config available
        if self.wave_config.get("entities"):
            entity_count = len(self.wave_config["entities"])
            html = html.replace(
                "<div class=\"ava-metric__label\">Active Agents</div>",
                f"<div class=\"ava-metric__label\">{entity_count} Entities to Migrate</div>",
                1
            )

        # Update gate statuses if scores available
        if self.gate_scores:
            html = self._update_gate_statuses(html)

        # Inject token metrics section
        if self.token_metrics:
            html = self._inject_token_metrics(html)

        # Save if output path provided
        if output_path:
            Path(output_path).write_text(html, encoding='utf-8')
            print(f"✅ Dashboard generated: {output_path}")
            return output_path

        return html

    def load_token_metrics(self, metrics_path: str) -> None:
        """Load token metrics from JSON file."""
        try:
            self.token_metrics = json.loads(Path(metrics_path).read_text(encoding='utf-8'))
            print(f"✅ Loaded token metrics from {metrics_path}")
        except Exception as e:
            print(f"⚠️  Failed to load token metrics: {e}")

    def _inject_token_metrics(self, html: str) -> str:
        """Inject token metrics section into HTML."""
        if not self.token_metrics:
            return html

        metrics = self.token_metrics
        total_tokens = metrics.get("total", 0)

        # Build phase breakdown
        phase_rows = ""
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

        # Build top agents
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

        # Cost estimate
        total_mtokens = total_tokens / 1_000_000
        cost_usd = round(total_mtokens * 0.0015, 2)

        metrics_section = f"""
        <!-- TOKEN USAGE METRICS INJECTED -->
        <section class="ava-section">
            <div class="ava-accent-bar"></div>
            <h2>Token Usage Analytics</h2>
            <p>Real-time token consumption metrics across all migration agents and phases.</p>
            
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
        </section>
        """

        # Insert after "Performance Indicators" section
        insertion_point = "<!-- KEY METRICS & PERFORMANCE -->"
        html = html.replace(insertion_point, metrics_section + "\n" + insertion_point)
        return html

    def _update_gate_statuses(self, html: str) -> str:
        """Update gate flow section with actual scores."""
        gate_map = {
            "gate1": {
                "selector": "🟢 Gate 1",
                "label": "Gate 1: Discovery",
            },
            "gate2": {
                "selector": "🟡 Gate 2",
                "label": "Gate 2: Architecture",
            },
            "gate3": {
                "selector": "🔴 Gate 3",
                "label": "Gate 3: Execution",
            },
        }

        for gate_key, gate_info in gate_map.items():
            if gate_key not in self.gate_scores:
                continue

            score = self.gate_scores[gate_key].get("score", 0.0)
            status_html = self._generate_status_badge(score, gate_key)

            # Replace status badge in gate flow
            html = html.replace(
                f'<div class="ava-status ava-status--green" style="margin-top: var(--ava-space-3);">\n                        <span class="ava-status__dot" style="background: var(--ava-success);"></span>\n                        ✅ Approved\n                    </div>',
                status_html,
                1,
            )

        return html

    def _generate_status_badge(self, score: float, gate: str) -> str:
        """Generate status badge HTML based on score."""
        thresholds = {
            "🟢": (0.85, "Approved", "success"),
            "🟡": (0.70, "In Review", "amber"),
            "🔴": (0.00, "Blocked", "red"),
        }

        if score is None:
            emoji, label, color = "🔴", "❌ Pending", "red"
        elif score >= 0.85:
            emoji, label, color = "🟢", "✅ Approved", "success"
        elif score >= 0.70:
            emoji, label, color = "🟡", "⚠️ In Review", "amber"
        else:
            emoji, label, color = "🔴", "❌ Blocked", "red"

        if score is not None:
            score_display = f" (Score: {score:.2f})"
        else:
            score_display = " (Pending)"

        return (
            f'<div class="ava-status ava-status--{color}" style="margin-top: var(--ava-space-3);">\n'
            f'<span class="ava-status__dot" style="background: var(--ava-{color});"></span>\n'
            f'{emoji} {label}{score_display}\n'
            f'</div>'
        )

    @staticmethod
    def generate_sample(output_path: str | None = None) -> str:
        """Generate dashboard with sample data for testing."""
        sample_config = {
            "wave_name": "WAVE-001",
            "entities": [
                {"name": "customer_dim", "rows": 1_500_000},
                {"name": "orders_fact", "rows": 25_000_000},
                {"name": "product_dim", "rows": 50_000},
            ]
        }

        sample_scores = {
            "gate1": {"score": 0.92, "status": "approved"},
            "gate2": {"score": 0.78, "status": "in_review"},
            "gate3": {"score": None, "status": "pending"},
        }

        gen = DashboardGenerator(
            wave_config_path=None,
            gate_scores_path=None,
        )
        gen.wave_config = sample_config
        gen.gate_scores = sample_scores
        
        # Add sample token metrics
        try:
            from token_metrics_collector import TokenMetricsCollector
            gen.token_metrics = TokenMetricsCollector.generate_sample_metrics()
        except ImportError:
            pass

        if output_path is None:
            output_path = str(gen.OUTPUT_DIR / "executive-dashboard-WAVE-001.html")

        return gen.generate(output_path)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate executive dashboard with live data")
    parser.add_argument("--wave-config", help="Path to wave-config.json")
    parser.add_argument("--gate-scores", help="Path to gate-scores.json")
    parser.add_argument("--token-metrics", help="Path to token-metrics.json")
    parser.add_argument("--output", help="Output HTML file (default: reports/executive-dashboard-generated.html)")
    parser.add_argument("--sample", action="store_true", help="Generate sample dashboard for testing")
    args = parser.parse_args()

    if args.sample:
        output = DashboardGenerator.generate_sample(args.output)
        print(f"✅ Sample dashboard generated: {output}")
        return 0

    gen = DashboardGenerator(args.wave_config, args.gate_scores)
    
    # Load token metrics if provided
    if args.token_metrics:
        gen.load_token_metrics(args.token_metrics)
    else:
        # Try to generate sample metrics
        try:
            from token_metrics_collector import TokenMetricsCollector
            gen.token_metrics = TokenMetricsCollector.generate_sample_metrics()
            print("ℹ️  Using sample token metrics (no --token-metrics provided)")
        except ImportError:
            pass
    
    output_path = args.output or str(gen.OUTPUT_DIR / "executive-dashboard-generated.html")
    gen.generate(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
