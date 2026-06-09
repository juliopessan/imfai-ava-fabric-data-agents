"""
Gate Audit Trail — Logs all gate decisions with approvers and justifications.
Creates immutable records for compliance and traceability.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json


class GateDecision(Enum):
    """Gate progression decision."""
    APPROVED = "approved"
    BLOCKED = "blocked"
    CONDITIONAL = "conditional"
    DEFERRED = "deferred"


@dataclass
class GateApprover:
    """Gate approver information."""
    name: str
    role: str
    email: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "timestamp": self.timestamp
        }


@dataclass
class GateAuditEntry:
    """Single gate audit log entry."""
    gate_number: int
    wave_id: str
    decision: GateDecision
    primary_approver: GateApprover
    secondary_approvers: List[GateApprover] = field(default_factory=list)
    justification: str = ""
    metrics_snapshot: Dict = field(default_factory=dict)
    risks_identified: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "gate_number": self.gate_number,
            "wave_id": self.wave_id,
            "decision": self.decision.value,
            "primary_approver": self.primary_approver.to_dict(),
            "secondary_approvers": [a.to_dict() for a in self.secondary_approvers],
            "justification": self.justification,
            "metrics_snapshot": self.metrics_snapshot,
            "risks_identified": self.risks_identified,
            "conditions": self.conditions,
            "timestamp": self.timestamp
        }


@dataclass
class WaveAuditTrail:
    """Complete audit trail for wave."""
    wave_id: str
    project_name: str
    gate_entries: List[GateAuditEntry] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "wave_id": self.wave_id,
            "project_name": self.project_name,
            "gate_entries": [e.to_dict() for e in self.gate_entries],
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }


class GateAuditTrailManager:
    """Manages gate audit trails."""
    
    def __init__(self):
        """Initialize manager."""
        self.trails: Dict[str, WaveAuditTrail] = {}
    
    def create_trail(
        self,
        wave_id: str,
        project_name: str
    ) -> WaveAuditTrail:
        """Create new audit trail."""
        trail = WaveAuditTrail(
            wave_id=wave_id,
            project_name=project_name
        )
        self.trails[wave_id] = trail
        return trail
    
    def log_gate_decision(
        self,
        wave_id: str,
        gate_number: int,
        decision: GateDecision,
        primary_approver: GateApprover,
        justification: str = "",
        metrics_snapshot: Optional[Dict] = None,
        risks: Optional[List[str]] = None,
        conditions: Optional[List[str]] = None,
        secondary_approvers: Optional[List[GateApprover]] = None
    ) -> GateAuditEntry:
        """
        Log gate decision to audit trail.
        
        Args:
            wave_id: Wave identifier
            gate_number: Gate number (1, 2, 3)
            decision: Gate decision (approved/blocked/etc)
            primary_approver: Main approver
            justification: Decision justification
            metrics_snapshot: Metrics at decision time
            risks: Risk identifications
            conditions: Conditions for approval
            secondary_approvers: Additional approvers
        
        Returns:
            Audit entry created
        """
        if wave_id not in self.trails:
            self.create_trail(wave_id, "unknown")
        
        trail = self.trails[wave_id]
        
        entry = GateAuditEntry(
            gate_number=gate_number,
            wave_id=wave_id,
            decision=decision,
            primary_approver=primary_approver,
            justification=justification,
            metrics_snapshot=metrics_snapshot or {},
            risks_identified=risks or [],
            conditions=conditions or [],
            secondary_approvers=secondary_approvers or []
        )
        
        trail.gate_entries.append(entry)
        trail.last_updated = datetime.utcnow().isoformat()
        
        return entry
    
    def get_gate_decisions(
        self,
        wave_id: str,
        gate_number: Optional[int] = None
    ) -> List[GateAuditEntry]:
        """Get gate decisions from trail."""
        if wave_id not in self.trails:
            return []
        
        trail = self.trails[wave_id]
        
        if gate_number is not None:
            return [e for e in trail.gate_entries if e.gate_number == gate_number]
        
        return trail.gate_entries
    
    def get_decision_history(self, wave_id: str) -> str:
        """Get human-readable decision history."""
        if wave_id not in self.trails:
            return f"No trail found for {wave_id}"
        
        trail = self.trails[wave_id]
        history = f"Gate Decision History - Wave {wave_id}\n"
        history += f"Project: {trail.project_name}\n"
        history += f"Created: {trail.created_at}\n\n"
        
        for entry in sorted(trail.gate_entries, key=lambda e: e.gate_number):
            history += f"Gate {entry.gate_number}: {entry.decision.value.upper()}\n"
            history += f"  Approver: {entry.primary_approver.name} ({entry.primary_approver.role})\n"
            if entry.secondary_approvers:
                history += f"  Secondary: {', '.join(a.name for a in entry.secondary_approvers)}\n"
            if entry.justification:
                history += f"  Justification: {entry.justification}\n"
            if entry.risks_identified:
                history += f"  Risks: {', '.join(entry.risks_identified)}\n"
            if entry.conditions:
                history += f"  Conditions: {', '.join(entry.conditions)}\n"
            history += "\n"
        
        return history
    
    def get_approver_history(self, approver_email: str) -> List[GateAuditEntry]:
        """Get all decisions made by approver."""
        decisions = []
        
        for trail in self.trails.values():
            for entry in trail.gate_entries:
                if entry.primary_approver.email == approver_email:
                    decisions.append(entry)
                elif any(a.email == approver_email for a in entry.secondary_approvers):
                    decisions.append(entry)
        
        return decisions
    
    def get_approval_chain(self, wave_id: str) -> Dict:
        """Get approval chain for wave."""
        if wave_id not in self.trails:
            return {}
        
        trail = self.trails[wave_id]
        chain = {}
        
        for entry in sorted(trail.gate_entries, key=lambda e: e.gate_number):
            chain[f"gate_{entry.gate_number}"] = {
                "decision": entry.decision.value,
                "primary_approver": entry.primary_approver.name,
                "approver_role": entry.primary_approver.role,
                "timestamp": entry.timestamp,
                "secondary_approvers": [a.name for a in entry.secondary_approvers]
            }
        
        return chain
    
    def check_consistency(self, wave_id: str) -> Tuple[bool, List[str]]:
        """
        Check consistency of audit trail.
        
        Returns:
            (is_consistent, list of inconsistencies)
        """
        inconsistencies = []
        
        if wave_id not in self.trails:
            return True, []
        
        trail = self.trails[wave_id]
        entries_by_gate = {}
        
        for entry in trail.gate_entries:
            if entry.gate_number in entries_by_gate:
                inconsistencies.append(f"Multiple entries for gate {entry.gate_number}")
            entries_by_gate[entry.gate_number] = entry
        
        # Check gate progression
        gates = sorted(entries_by_gate.keys())
        for i, gate in enumerate(gates):
            if i > 0:
                prev_gate = gates[i-1]
                prev_decision = entries_by_gate[prev_gate].decision
                
                # Current gate should not be approved if previous was blocked
                curr_decision = entries_by_gate[gate].decision
                if prev_decision == GateDecision.BLOCKED and curr_decision == GateDecision.APPROVED:
                    inconsistencies.append(f"Gate {gate} approved after Gate {prev_gate} was blocked")
        
        return len(inconsistencies) == 0, inconsistencies
    
    def generate_compliance_report(self, wave_id: str) -> str:
        """Generate compliance report."""
        is_consistent, inconsistencies = self.check_consistency(wave_id)
        
        report = f"Compliance Report - Wave {wave_id}\n"
        report += f"Audit Trail Consistency: {'PASS' if is_consistent else 'FAIL'}\n\n"
        
        if inconsistencies:
            report += "Issues Found:\n"
            for issue in inconsistencies:
                report += f"  - {issue}\n"
        
        trail = self.trails.get(wave_id)
        if trail:
            report += f"\nTotal Gate Decisions: {len(trail.gate_entries)}\n"
            report += f"Trail Created: {trail.created_at}\n"
            report += f"Last Updated: {trail.last_updated}\n"
        
        return report
    
    def save_trail(self, wave_id: str, file_path: str) -> None:
        """Save audit trail to file."""
        if wave_id not in self.trails:
            raise ValueError(f"No trail found for {wave_id}")
        
        with open(file_path, "w") as f:
            json.dump(self.trails[wave_id].to_dict(), f, indent=2)
    
    def load_trail(self, file_path: str) -> WaveAuditTrail:
        """Load audit trail from file."""
        with open(file_path, "r") as f:
            data = json.load(f)
        
        trail = WaveAuditTrail(
            wave_id=data["wave_id"],
            project_name=data["project_name"],
            created_at=data["created_at"],
            last_updated=data["last_updated"]
        )
        
        self.trails[data["wave_id"]] = trail
        return trail
