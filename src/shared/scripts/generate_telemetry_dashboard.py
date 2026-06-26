"""
Generate HTML Dashboard with Execution Telemetry

Displays:
1. Side panel: execution metrics, tokens, cost, status
2. Agent timeline: expandable phases and decisions
3. Business intelligence: outcomes and impact
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def generate_metrics_panel(telemetry_report: Dict[str, Any]) -> str:
    """Generate the side panel with key metrics."""
    metrics = telemetry_report.get("metrics", {})
    execution = telemetry_report.get("execution", {})
    
    # Calculate status color
    status_colors = {
        "Starting...": "#fbbf24",
        "In progress (0-10s)": "#60a5fa",
        "Processing": "#a78bfa",
        "Almost completed": "#34d399",
        "Completed": "#10b981"
    }
    status_color = status_colors.get(metrics.get("status", "Processing"), "#60a5fa")
    
    html = f"""
    <div class="metrics-side-panel">
        <div class="panel-header" style="background: linear-gradient(135deg, #5c2d91 0%, #ff6b35 100%);">
            <h2>Execution Summary</h2>
        </div>
        
        <div class="metrics-grid">
            <!-- Time -->
            <div class="metric-card">
                <div class="metric-label">⏳ Execution Time</div>
                <div class="metric-value" style="font-size: 28px; font-weight: bold;">
                    {metrics.get('elapsed_time', '0s')}
                </div>
            </div>
            
            <!-- Tokens -->
            <div class="metric-card">
                <div class="metric-label">🔤 Token Consumption</div>
                <div class="metric-value" style="font-size: 24px; font-weight: bold;">
                    {metrics.get('total_tokens', 0):,}
                </div>
                <small style="color: #666;">
                    Input: {metrics.get('input_tokens', 0):,} | 
                    Output: {metrics.get('output_tokens', 0):,}
                </small>
            </div>
            
            <!-- Cost -->
            <div class="metric-card">
                <div class="metric-label">💰 Execution Cost</div>
                <div class="metric-value" style="font-size: 24px; font-weight: bold; color: #10b981;">
                    ${metrics.get('cost_usd', 0):.4f}
                </div>
            </div>
            
            <!-- Status -->
            <div class="metric-card" style="background-color: {status_color}22; border-left: 4px solid {status_color};">
                <div class="metric-label">✓ Status</div>
                <div class="metric-value" style="color: {status_color}; font-weight: bold;">
                    {metrics.get('status', 'Processing')}
                </div>
            </div>
            
            <!-- Cache Hit Rate -->
            <div class="metric-card">
                <div class="metric-label">💾 Cache Hit Rate</div>
                <div class="metric-value" style="font-size: 20px; font-weight: bold;">
                    {metrics.get('cache_hit_rate', 0)*100:.1f}%
                </div>
            </div>
        </div>
        
        <div class="details-section">
            <h3>Execution Breakdown</h3>
            <div class="breakdown-list">
                <div class="breakdown-item">
                    <span class="breakdown-label">🔧 Tools Executed</span>
                    <span class="breakdown-value">{execution.get('tool_calls', 0)}</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">📡 MCP Calls</span>
                    <span class="breakdown-value">{execution.get('mcp_calls', 0)}</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">📚 RAG Retrievals</span>
                    <span class="breakdown-value">{execution.get('rag_retrievals', 0)}</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">💭 Memory Lookups</span>
                    <span class="breakdown-value">{execution.get('memory_lookups', 0)}</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">📊 Phases</span>
                    <span class="breakdown-value">{execution.get('phases_completed', 0)}</span>
                </div>
            </div>
        </div>
        
        <div class="workflow-info">
            <div><strong>Agent:</strong> {telemetry_report.get('metadata', {}).get('agent', 'N/A')}</div>
            <div><strong>Workflow:</strong> {telemetry_report.get('metadata', {}).get('workflow', 'N/A')}</div>
        </div>
    </div>
    """
    return html


def generate_timeline(timeline_events: List[Dict[str, Any]]) -> str:
    """Generate expandable execution timeline."""
    html = """
    <div class="timeline-section">
        <h2>Agent Execution Timeline</h2>
        <div class="timeline">
    """
    
    for i, event in enumerate(timeline_events):
        is_expanded = i == 0  # First item expanded
        expanded_class = "expanded" if is_expanded else ""
        
        html += f"""
            <div class="timeline-item {expanded_class}">
                <div class="timeline-marker" onclick="toggleTimeline(this)">
                    <span class="timeline-icon">{event.get('icon', '•')}</span>
                </div>
                <div class="timeline-content" onclick="toggleTimeline(this.previousElementSibling)">
                    <div class="timeline-type">{event.get('type', 'Event')}</div>
                    <div class="timeline-detail">{event.get('detail', '')}</div>
                    <small class="timeline-timestamp">{event.get('timestamp', '')}</small>
                </div>
            </div>
        """
    
    html += """
        </div>
    </div>
    """
    return html


def generate_business_intelligence(outcomes: List[Dict[str, Any]]) -> str:
    """Generate business intelligence summary from agent outcomes."""
    html = """
    <div class="business-intelligence-section">
        <h2>Business Intelligence</h2>
        <div class="bi-outcomes">
    """
    
    # Group outcomes by category
    by_category = {}
    for outcome in outcomes:
        cat = outcome.get("category", "Other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(outcome)
    
    for category, items in by_category.items():
        html += f"""
            <div class="bi-category">
                <h3>📊 {category}</h3>
                <div class="bi-flow">
        """
        
        for item in items:
            # Color coding based on impact
            impact_colors = {
                "Critical": "#ef4444",
                "High": "#f97316",
                "Medium": "#eab308",
                "Low": "#84cc16"
            }
            color = impact_colors.get(item.get("impact", "Medium"), "#3b82f6")
            
            html += f"""
                    <div class="bi-item" style="border-left: 4px solid {color};">
                        <div class="bi-metric">{item.get('metric', 'Metric')}</div>
                        <div class="bi-value" style="color: {color}; font-size: 18px; font-weight: bold;">
                            {item.get('value', 'N/A')}
                        </div>
                        <div class="bi-impact">{item.get('impact', 'N/A')} Impact</div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
    
    html += """
        </div>
    </div>
    """
    return html


def generate_full_telemetry_dashboard(telemetry_report: Dict[str, Any], 
                                     title: str = "Fabricae v3 - Execution Dashboard") -> str:
    """Generate complete HTML dashboard with all telemetry."""
    
    metrics_panel = generate_metrics_panel(telemetry_report)
    timeline = generate_timeline(telemetry_report.get("timeline", []))
    bi_section = generate_business_intelligence(telemetry_report.get("business_outcomes", []))
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                color: #333;
            }}
            
            .container {{
                display: grid;
                grid-template-columns: 320px 1fr;
                gap: 20px;
                padding: 20px;
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            /* Side Panel */
            .metrics-side-panel {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 20px;
                position: sticky;
                top: 20px;
                height: fit-content;
            }}
            
            .panel-header {{
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin: -20px -20px 20px -20px;
            }}
            
            .panel-header h2 {{
                font-size: 18px;
                font-weight: 600;
            }}
            
            .metrics-grid {{
                display: grid;
                gap: 12px;
                margin-bottom: 20px;
            }}
            
            .metric-card {{
                background: #f9fafb;
                border-left: 4px solid #5c2d91;
                padding: 12px;
                border-radius: 4px;
            }}
            
            .metric-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }}
            
            .metric-value {{
                font-size: 20px;
                font-weight: bold;
                color: #1a1a1a;
            }}
            
            small {{
                display: block;
                font-size: 11px;
                color: #999;
                margin-top: 4px;
            }}
            
            .details-section {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #eee;
            }}
            
            .details-section h3 {{
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 12px;
            }}
            
            .breakdown-list {{
                display: grid;
                gap: 8px;
            }}
            
            .breakdown-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px;
                background: #f9fafb;
                border-radius: 4px;
                font-size: 13px;
            }}
            
            .breakdown-label {{
                font-weight: 500;
            }}
            
            .breakdown-value {{
                background: #5c2d91;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-weight: 600;
                font-size: 12px;
            }}
            
            .workflow-info {{
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #eee;
                font-size: 12px;
                color: #666;
            }}
            
            .workflow-info div {{
                margin: 4px 0;
            }}
            
            /* Main Content */
            .main-content {{
                display: grid;
                gap: 20px;
            }}
            
            .timeline-section,
            .business-intelligence-section {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 30px;
            }}
            
            h2 {{
                color: #1a1a1a;
                font-size: 24px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            /* Timeline */
            .timeline {{
                position: relative;
                padding: 20px 0;
            }}
            
            .timeline::before {{
                content: '';
                position: absolute;
                left: 20px;
                top: 0;
                bottom: 0;
                width: 2px;
                background: linear-gradient(to bottom, #5c2d91, transparent);
            }}
            
            .timeline-item {{
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
                position: relative;
            }}
            
            .timeline-marker {{
                flex-shrink: 0;
                width: 44px;
                height: 44px;
                background: white;
                border: 3px solid #5c2d91;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .timeline-marker:hover {{
                background: #5c2d91;
                color: white;
                transform: scale(1.1);
            }}
            
            .timeline-content {{
                flex: 1;
                padding: 15px;
                background: #f9fafb;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
            }}
            
            .timeline-item.expanded .timeline-content {{
                background: #ede9fe;
                border-left: 4px solid #5c2d91;
            }}
            
            .timeline-type {{
                font-weight: 600;
                color: #5c2d91;
                margin-bottom: 4px;
            }}
            
            .timeline-detail {{
                color: #333;
                font-size: 14px;
                margin-bottom: 4px;
            }}
            
            .timeline-timestamp {{
                color: #999;
                font-size: 11px;
            }}
            
            /* Business Intelligence */
            .bi-outcomes {{
                display: grid;
                gap: 30px;
            }}
            
            .bi-category h3 {{
                color: #5c2d91;
                font-size: 16px;
                margin-bottom: 15px;
            }}
            
            .bi-flow {{
                display: grid;
                gap: 12px;
            }}
            
            .bi-item {{
                background: #f9fafb;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #3b82f6;
                transition: all 0.3s;
            }}
            
            .bi-item:hover {{
                transform: translateX(5px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            
            .bi-metric {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }}
            
            .bi-value {{
                font-size: 20px;
                font-weight: bold;
                margin: 8px 0;
            }}
            
            .bi-impact {{
                font-size: 11px;
                color: #999;
                font-weight: 500;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    grid-template-columns: 1fr;
                }}
                
                .metrics-side-panel {{
                    position: relative;
                    top: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {metrics_panel}
            
            <div class="main-content">
                {timeline}
                {bi_section}
            </div>
        </div>
        
        <script>
            function toggleTimeline(marker) {{
                const item = marker.closest('.timeline-item');
                item.classList.toggle('expanded');
            }}
            
            // Auto-expand all items on load if screen is wide enough
            window.addEventListener('load', () => {{
                if (window.innerWidth > 768) {{
                    document.querySelectorAll('.timeline-item').forEach(item => {{
                        item.classList.add('expanded');
                    }});
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html


def generate_telemetry_report(telemetry_json_file: Path, output_html: Path):
    """Load telemetry JSON and generate dashboard."""
    with open(telemetry_json_file) as f:
        report = json.load(f)
    
    html = generate_full_telemetry_dashboard(report)
    output_html.write_text(html)
    print(f"✓ Telemetry dashboard generated: {output_html}")


if __name__ == "__main__":
    # Example telemetry data
    sample_telemetry = {
        "metadata": {
            "workflow": "Data Migration - Financeiro",
            "agent": "discovery-scout",
            "start_time": datetime.now().isoformat(),
            "elapsed_time": "6m 59s",
            "elapsed_seconds": 419
        },
        "metrics": {
            "input_tokens": 2100,
            "output_tokens": 1600,
            "total_tokens": 3700,
            "cost_usd": 0.0142,
            "status": "Almost completed",
            "cache_hit_rate": 0.75
        },
        "execution": {
            "tool_calls": 5,
            "mcp_calls": 3,
            "rag_retrievals": 4,
            "memory_lookups": 7,
            "phases_completed": 6
        },
        "timeline": [
            {
                "timestamp": "2026-06-08T10:30:45",
                "type": "Agent Started",
                "detail": "discovery-scout initialized",
                "icon": "🚀"
            },
            {
                "timestamp": "2026-06-08T10:30:47",
                "type": "Memory Search",
                "detail": "Previous decisions lookup",
                "icon": "💾"
            },
            {
                "timestamp": "2026-06-08T10:30:50",
                "type": "RAG Query",
                "detail": "Azure API docs retrieved",
                "icon": "📚"
            },
            {
                "timestamp": "2026-06-08T10:31:00",
                "type": "Tool Execution",
                "detail": "Azure SDK call",
                "icon": "🔧"
            },
            {
                "timestamp": "2026-06-08T10:31:15",
                "type": "MCP Request",
                "detail": "Analysis microservice",
                "icon": "📡"
            },
            {
                "timestamp": "2026-06-08T10:37:30",
                "type": "Decision",
                "detail": "45 entities recommended",
                "icon": "🎯"
            },
            {
                "timestamp": "2026-06-08T10:37:45",
                "type": "Response Generated",
                "detail": "Report compiled",
                "icon": "✓"
            }
        ],
        "business_outcomes": [
            {
                "category": "Contract Analysis",
                "metric": "Documents Analyzed",
                "value": "5 contracts",
                "impact": "Critical"
            },
            {
                "category": "Contract Analysis",
                "metric": "Compliance Issues Found",
                "value": "3 issues",
                "impact": "High"
            },
            {
                "category": "Financial Impact",
                "metric": "Potential Exposure",
                "value": "$42,000",
                "impact": "Critical"
            },
            {
                "category": "Recommendations",
                "metric": "Actions Generated",
                "value": "17 recommendations",
                "impact": "High"
            },
            {
                "category": "Cost Optimization",
                "metric": "Execution Cost",
                "value": "$0.014",
                "impact": "Low"
            }
        ]
    }
    
    html = generate_full_telemetry_dashboard(sample_telemetry)
    output_path = Path("sample_telemetry_dashboard.html")
    output_path.write_text(html)
    print(f"✓ Sample dashboard generated: {output_path}")
