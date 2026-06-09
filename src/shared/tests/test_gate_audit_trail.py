"""
Tests for GateAuditTrailManager — Gate decision audit logging.
"""

import pytest
from src.shared.scripts.gate_audit_trail import (
    GateAuditTrailManager, GateApprover, GateDecision
)


class TestGateAuditTrailManager:
    """Test suite for GateAuditTrailManager."""
    
    def test_initialization(self):
        """Test manager initialization."""
        manager = GateAuditTrailManager()
        assert len(manager.trails) == 0
    
    def test_create_trail(self):
        """Test creating audit trail."""
        manager = GateAuditTrailManager()
        trail = manager.create_trail("wave-001", "test-project")
        
        assert trail.wave_id == "wave-001"
        assert trail.project_name == "test-project"
        assert "wave-001" in manager.trails
    
    def test_log_gate_decision(self):
        """Test logging gate decision."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="John Doe",
            role="Technical Lead",
            email="john@example.com"
        )
        
        entry = manager.log_gate_decision(
            wave_id="wave-001",
            gate_number=1,
            decision=GateDecision.APPROVED,
            primary_approver=approver,
            justification="All validations passed"
        )
        
        assert entry.gate_number == 1
        assert entry.decision == GateDecision.APPROVED
        assert entry.primary_approver.name == "John Doe"
    
    def test_log_gate_decision_creates_trail(self):
        """Test logging creates trail if needed."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Jane Smith",
            role="Data Lead",
            email="jane@example.com"
        )
        
        manager.log_gate_decision(
            wave_id="wave-002",
            gate_number=2,
            decision=GateDecision.CONDITIONAL,
            primary_approver=approver
        )
        
        assert "wave-002" in manager.trails
    
    def test_log_multiple_gates(self):
        """Test logging multiple gate decisions."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        for gate in [1, 2, 3]:
            manager.log_gate_decision(
                wave_id="wave-001",
                gate_number=gate,
                decision=GateDecision.APPROVED,
                primary_approver=approver
            )
        
        trail = manager.trails["wave-001"]
        assert len(trail.gate_entries) == 3
    
    def test_get_gate_decisions_all(self):
        """Test retrieving all gate decisions."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        for gate in [1, 2, 3]:
            manager.log_gate_decision(
                wave_id="wave-001",
                gate_number=gate,
                decision=GateDecision.APPROVED,
                primary_approver=approver
            )
        
        decisions = manager.get_gate_decisions("wave-001")
        assert len(decisions) == 3
    
    def test_get_gate_decisions_by_gate(self):
        """Test retrieving specific gate decision."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        manager.log_gate_decision("wave-001", 1, GateDecision.APPROVED, approver)
        manager.log_gate_decision("wave-001", 2, GateDecision.BLOCKED, approver)
        manager.log_gate_decision("wave-001", 3, GateDecision.APPROVED, approver)
        
        gate2_decisions = manager.get_gate_decisions("wave-001", gate_number=2)
        assert len(gate2_decisions) == 1
        assert gate2_decisions[0].decision == GateDecision.BLOCKED
    
    def test_get_decision_history(self):
        """Test decision history generation."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="John Doe",
            role="Lead",
            email="john@example.com"
        )
        
        manager.log_gate_decision(
            "wave-001", 1, GateDecision.APPROVED, approver,
            justification="Ready to proceed"
        )
        
        history = manager.get_decision_history("wave-001")
        assert "Gate Decision History" in history
        assert "wave-001" in history
        assert "Ready to proceed" in history
    
    def test_secondary_approvers(self):
        """Test recording secondary approvers."""
        manager = GateAuditTrailManager()
        
        primary = GateApprover(
            name="Primary",
            role="Lead",
            email="primary@example.com"
        )
        
        secondary = GateApprover(
            name="Secondary",
            role="Reviewer",
            email="secondary@example.com"
        )
        
        entry = manager.log_gate_decision(
            wave_id="wave-001",
            gate_number=1,
            decision=GateDecision.APPROVED,
            primary_approver=primary,
            secondary_approvers=[secondary]
        )
        
        assert len(entry.secondary_approvers) == 1
        assert entry.secondary_approvers[0].name == "Secondary"
    
    def test_metrics_snapshot(self):
        """Test capturing metrics snapshot."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        metrics = {
            "completude": 0.95,
            "quality": 0.92,
            "error_rate": 0.02
        }
        
        entry = manager.log_gate_decision(
            wave_id="wave-001",
            gate_number=1,
            decision=GateDecision.APPROVED,
            primary_approver=approver,
            metrics_snapshot=metrics
        )
        
        assert entry.metrics_snapshot == metrics
    
    def test_conditions(self):
        """Test recording conditional approvals."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        conditions = [
            "Must resolve schema issues",
            "Reconciliation must reach 95%"
        ]
        
        entry = manager.log_gate_decision(
            wave_id="wave-001",
            gate_number=2,
            decision=GateDecision.CONDITIONAL,
            primary_approver=approver,
            conditions=conditions
        )
        
        assert len(entry.conditions) == 2
    
    def test_get_approver_history(self):
        """Test getting decisions by approver."""
        manager = GateAuditTrailManager()
        
        approver1 = GateApprover(
            name="Approver1",
            role="Lead",
            email="approver1@example.com"
        )
        
        approver2 = GateApprover(
            name="Approver2",
            role="Lead",
            email="approver2@example.com"
        )
        
        manager.log_gate_decision("wave-001", 1, GateDecision.APPROVED, approver1)
        manager.log_gate_decision("wave-002", 1, GateDecision.APPROVED, approver2)
        manager.log_gate_decision("wave-003", 1, GateDecision.APPROVED, approver1)
        
        history = manager.get_approver_history("approver1@example.com")
        assert len(history) == 2
    
    def test_get_approval_chain(self):
        """Test getting approval chain."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        for gate in [1, 2, 3]:
            manager.log_gate_decision(
                "wave-001", gate, GateDecision.APPROVED, approver
            )
        
        chain = manager.get_approval_chain("wave-001")
        assert len(chain) == 3
        assert "gate_1" in chain
        assert chain["gate_1"]["decision"] == "approved"
    
    def test_check_consistency(self):
        """Test consistency checking."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        manager.log_gate_decision("wave-001", 1, GateDecision.APPROVED, approver)
        manager.log_gate_decision("wave-001", 2, GateDecision.APPROVED, approver)
        
        is_consistent, issues = manager.check_consistency("wave-001")
        assert is_consistent is True
        assert len(issues) == 0
    
    def test_check_consistency_blocked_then_approved(self):
        """Test consistency detects blocked then approved."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        manager.log_gate_decision("wave-001", 1, GateDecision.BLOCKED, approver)
        manager.log_gate_decision("wave-001", 2, GateDecision.APPROVED, approver)
        
        is_consistent, issues = manager.check_consistency("wave-001")
        assert is_consistent is False
        assert len(issues) > 0
    
    def test_generate_compliance_report(self):
        """Test compliance report generation."""
        manager = GateAuditTrailManager()
        
        approver = GateApprover(
            name="Approver",
            role="Lead",
            email="approver@example.com"
        )
        
        manager.log_gate_decision("wave-001", 1, GateDecision.APPROVED, approver)
        
        report = manager.generate_compliance_report("wave-001")
        assert "Compliance Report" in report
        assert "wave-001" in report
        assert "PASS" in report or "FAIL" in report
