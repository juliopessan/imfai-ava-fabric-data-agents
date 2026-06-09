"""
KPI Dashboard Report — Aggregates wave-level KPIs and generates dashboard data.
Consolidates metrics across gates for visibility, trending, and executive dashboards.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class GateKPI:
    """KPIs for a single gate."""
    gate_number: int
    completude: float
    quality: float
    error_rate: float       # errors / total entities
    reconciliation: float
    artifact_count: int
    status: str  # "approved", "conditional", "blocked"


@dataclass
class WaveKPI:
    """Wave-level KPIs aggregated across gates."""
    wave_id: str
    project_name: str
    timestamp: str
    total_gates: int
    gates_approved: int
    gates_blocked: int
    overall_completude: float
    overall_quality: float
    overall_error_rate: float
    average_reconciliation: float
    progress_percentage: float
    trend: str  # "on_track", "at_risk", "blocked"
    critical_blockers: List[str]


class KPIDashboardReporter:
    """Generates KPI dashboards for waves."""
    
    def __init__(self):
        """Initialize reporter."""
        self.gate_kpis: Dict[int, GateKPI] = {}
        self.historical_waves: List[WaveKPI] = []
    
    def add_gate_kpi(
        self,
        gate_number: int,
        completude: float,
        quality: float,
        error_count: int,
        total_entities: int,
        reconciliation: float,
        artifact_count: int,
        status: str
    ) -> None:
        """Add KPI for a gate."""
        error_rate = error_count / total_entities if total_entities > 0 else 0
        
        self.gate_kpis[gate_number] = GateKPI(
            gate_number=gate_number,
            completude=completude,
            quality=quality,
            error_rate=error_rate,
            reconciliation=reconciliation,
            artifact_count=artifact_count,
            status=status
        )
    
    def calculate_wave_kpi(
        self,
        wave_id: str,
        project_name: str,
        progress_percentage: float
    ) -> WaveKPI:
        """Calculate wave-level KPI from gate KPIs."""
        if not self.gate_kpis:
            return WaveKPI(
                wave_id=wave_id,
                project_name=project_name,
                timestamp=datetime.utcnow().isoformat(),
                total_gates=0,
                gates_approved=0,
                gates_blocked=0,
                overall_completude=0.0,
                overall_quality=0.0,
                overall_error_rate=0.0,
                average_reconciliation=0.0,
                progress_percentage=0.0,
                trend="blocked",
                critical_blockers=["No gates have been validated"]
            )
        
        # Aggregate gate metrics
        completudes = [kpi.completude for kpi in self.gate_kpis.values()]
        qualities = [kpi.quality for kpi in self.gate_kpis.values()]
        error_rates = [kpi.error_rate for kpi in self.gate_kpis.values()]
        reconciliations = [kpi.reconciliation for kpi in self.gate_kpis.values()]
        
        gates_approved = len([k for k in self.gate_kpis.values() if k.status == "approved"])
        gates_blocked = len([k for k in self.gate_kpis.values() if k.status == "blocked"])
        
        # Determine trend
        if gates_blocked > 0:
            trend = "blocked"
        elif progress_percentage < 50:
            trend = "at_risk"
        else:
            trend = "on_track"
        
        # Identify critical blockers
        critical_blockers = []
        for gate_num, kpi in self.gate_kpis.items():
            if kpi.status == "blocked":
                if kpi.completude < 0.5:
                    critical_blockers.append(f"Gate {gate_num}: Completude only {kpi.completude:.1%}")
                if kpi.error_rate > 0.1:
                    critical_blockers.append(f"Gate {gate_num}: High error rate {kpi.error_rate:.1%}")
        
        wave_kpi = WaveKPI(
            wave_id=wave_id,
            project_name=project_name,
            timestamp=datetime.utcnow().isoformat(),
            total_gates=len(self.gate_kpis),
            gates_approved=gates_approved,
            gates_blocked=gates_blocked,
            overall_completude=sum(completudes) / len(completudes) if completudes else 0.0,
            overall_quality=sum(qualities) / len(qualities) if qualities else 0.0,
            overall_error_rate=sum(error_rates) / len(error_rates) if error_rates else 0.0,
            average_reconciliation=sum(reconciliations) / len(reconciliations) if reconciliations else 0.0,
            progress_percentage=progress_percentage,
            trend=trend,
            critical_blockers=critical_blockers if critical_blockers else ["None"]
        )
        
        self.historical_waves.append(wave_kpi)
        return wave_kpi
    
    def get_dashboard_data(self, wave_kpi: WaveKPI) -> Dict[str, Any]:
        """Generate dashboard-ready data."""
        return {
            "wave": {
                "id": wave_kpi.wave_id,
                "project": wave_kpi.project_name,
                "timestamp": wave_kpi.timestamp,
                "trend": wave_kpi.trend,
                "progress": wave_kpi.progress_percentage
            },
            "metrics": {
                "total_gates": wave_kpi.total_gates,
                "approved": wave_kpi.gates_approved,
                "blocked": wave_kpi.gates_blocked,
                "conditional": wave_kpi.total_gates - wave_kpi.gates_approved - wave_kpi.gates_blocked
            },
            "quality": {
                "overall_completude": round(wave_kpi.overall_completude, 3),
                "overall_quality": round(wave_kpi.overall_quality, 3),
                "average_error_rate": round(wave_kpi.overall_error_rate, 3),
                "average_reconciliation": round(wave_kpi.average_reconciliation, 3)
            },
            "gates": {
                str(num): asdict(kpi)
                for num, kpi in self.gate_kpis.items()
            },
            "blockers": wave_kpi.critical_blockers
        }
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """Analyze KPI trends across wave history."""
        if len(self.historical_waves) < 2:
            return {"message": "Insufficient historical data for trend analysis"}
        
        latest = self.historical_waves[-1]
        previous = self.historical_waves[-2]
        
        return {
            "progress_delta": latest.progress_percentage - previous.progress_percentage,
            "quality_delta": latest.overall_quality - previous.overall_quality,
            "approved_gates_delta": latest.gates_approved - previous.gates_approved,
            "blocked_gates_delta": latest.gates_blocked - previous.gates_blocked,
            "trend_direction": "improving" if latest.progress_percentage > previous.progress_percentage else "declining"
        }
    
    def save_dashboard(self, dashboard_data: Dict[str, Any], output_path) -> None:
        """Save dashboard data to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
    
    def get_kpi_summary_text(self, wave_kpi: WaveKPI) -> str:
        """Generate human-readable KPI summary."""
        lines = [
            f"Wave {wave_kpi.wave_id} ({wave_kpi.project_name})",
            f"  Progress: {wave_kpi.progress_percentage:.1f}%",
            f"  Status: {wave_kpi.trend.upper()}",
            f"  Quality: {wave_kpi.overall_quality:.2f} | Completude: {wave_kpi.overall_completude:.1%}",
            f"  Gates: {wave_kpi.gates_approved} approved, {wave_kpi.gates_blocked} blocked",
        ]
        
        if wave_kpi.critical_blockers and wave_kpi.critical_blockers[0] != "None":
            lines.append("  Critical Issues:")
            for blocker in wave_kpi.critical_blockers[:3]:
                lines.append(f"    - {blocker}")
        
        return "\n".join(lines)
