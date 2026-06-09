"""
Wave Status Tracker — Consolidates gate progression across migration wave.
Provides real-time status summary: which gates are approved/conditional/blocked and progress %age.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class GateStatus:
    """Status of a single gate in the wave."""
    gate_number: int
    status: str  # approved, conditional, blocked
    score: float
    completude: float
    quality: float
    reconciliation: float
    errors_count: int
    timestamp: str


@dataclass
class WaveStatus:
    """Overall wave status across all three gates."""
    wave_id: str
    project_name: str
    gates: Dict[int, GateStatus]
    overall_status: str  # approved_all, conditional_any, blocked_any
    progress_percentage: float  # 0-100%
    next_gate: Optional[int]  # Which gate to focus on next
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_id": self.wave_id,
            "project_name": self.project_name,
            "gates": {str(k): asdict(v) for k, v in self.gates.items()},
            "overall_status": self.overall_status,
            "progress_percentage": self.progress_percentage,
            "next_gate": self.next_gate,
            "timestamp": self.timestamp
        }


class WaveStatusTracker:
    """Tracks and consolidates gate progression for a migration wave."""
    
    def __init__(self, wave_id: str, project_name: str):
        """Initialize tracker for a wave."""
        self.wave_id = wave_id
        self.project_name = project_name
        self.gates: Dict[int, GateStatus] = {}
    
    def add_gate_result(self, gate_number: int, validation_result: Dict[str, Any]) -> None:
        """Add a gate validation result to tracking."""
        if not isinstance(validation_result, dict):
            raise ValueError("validation_result must be a dictionary")
        
        if gate_number not in [1, 2, 3]:
            raise ValueError("gate_number must be 1, 2, or 3")
        
        # Determine status from score
        score = validation_result.get("score", validation_result.get("gatescore", 0.0))
        if score >= 0.85:
            status = "approved"
        elif score >= 0.70:
            status = "conditional"
        else:
            status = "blocked"
        
        self.gates[gate_number] = GateStatus(
            gate_number=gate_number,
            status=status,
            score=score,
            completude=validation_result.get("completude", 0.0),
            quality=validation_result.get("quality", 0.0),
            reconciliation=validation_result.get("reconciliation", 1.0),
            errors_count=len(validation_result.get("errors", [])),
            timestamp=datetime.now().isoformat()
        )
    
    def calculate_progress(self) -> float:
        """Calculate overall wave progress as percentage (0-100)."""
        if not self.gates:
            return 0.0
        
        # Progress = average completude across all gates
        total_completude = sum(g.completude for g in self.gates.values())
        return (total_completude / len(self.gates)) * 100
    
    def determine_overall_status(self) -> str:
        """Determine overall wave status based on gates."""
        if not self.gates:
            return "no_data"
        
        statuses = [g.status for g in self.gates.values()]
        
        if all(s == "approved" for s in statuses):
            return "approved_all"
        elif "blocked" in statuses:
            return "blocked_any"
        else:
            return "conditional_any"
    
    def get_next_gate(self) -> Optional[int]:
        """Determine next gate to focus on."""
        for gate_num in [1, 2, 3]:
            if gate_num not in self.gates:
                return gate_num
            
            if self.gates[gate_num].status != "approved":
                return gate_num
        
        return None  # All gates approved
    
    def get_status(self) -> WaveStatus:
        """Get consolidated wave status."""
        progress = self.calculate_progress()
        overall = self.determine_overall_status()
        next_gate = self.get_next_gate()
        
        return WaveStatus(
            wave_id=self.wave_id,
            project_name=self.project_name,
            gates=self.gates,
            overall_status=overall,
            progress_percentage=progress,
            next_gate=next_gate,
            timestamp=datetime.now().isoformat()
        )
    
    def get_recommendations(self) -> List[str]:
        """Get prioritized recommendations for wave progression."""
        recommendations = []
        status = self.get_status()
        
        # Overall recommendations
        if status.overall_status == "blocked_any":
            for gate_num, gate in status.gates.items():
                if gate.status == "blocked":
                    recommendations.append(
                        f"Gate {gate_num} is blocked (score {gate.score:.2f}). "
                        f"Fix {gate.errors_count} error(s) and increase completude to ≥90%."
                    )
        
        elif status.overall_status == "conditional_any":
            for gate_num, gate in status.gates.items():
                if gate.status == "conditional":
                    recommendations.append(
                        f"Gate {gate_num} is conditional (score {gate.score:.2f}). "
                        f"Improve quality to reach approval threshold (0.85)."
                    )
        
        # Gate 3 specific recommendations
        if 3 in status.gates and status.gates[3].reconciliation < 0.95:
            recommendations.append(
                f"Gate 3 reconciliation is low ({status.gates[3].reconciliation:.2f}). "
                f"Must reach 0.95+ for approval. Validate row counts and schema."
            )
        
        # Progress recommendations
        if status.progress_percentage < 50:
            recommendations.append(
                f"Wave progress is {status.progress_percentage:.0f}%. "
                f"Focus on completing artifacts for Gate {status.next_gate}."
            )
        
        return recommendations if recommendations else ["All gates on track for approval."]
    
    def save_to_file(self, output_path: Path) -> None:
        """Save wave status to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        status = self.get_status()
        with open(output_path, 'w') as f:
            json.dump(status.to_dict(), f, indent=2)


def track_wave_status(validation_results: Dict[str, Any], wave_id: str, project_name: str) -> WaveStatus:
    """Helper function: Track wave status from validation results."""
    tracker = WaveStatusTracker(wave_id, project_name)
    
    for gate_num in [1, 2, 3]:
        gate_key = f"gate_{gate_num}"
        if gate_key in validation_results:
            tracker.add_gate_result(gate_num, validation_results[gate_key])
    
    return tracker.get_status()
