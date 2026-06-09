"""
Tests for WaveStatusTracker — gate progression tracking and wave consolidation.
"""

import pytest
from datetime import datetime
from src.shared.scripts.wave_status_tracker import WaveStatusTracker, WaveStatus, GateStatus, track_wave_status


class TestWaveStatusTracker:
    """Test suite for WaveStatusTracker class."""
    
    def test_initialization(self):
        """Test tracker initialization."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        assert tracker.wave_id == "wave-001"
        assert tracker.project_name == "test-project"
        assert len(tracker.gates) == 0
    
    def test_add_gate_result_approved(self):
        """Test adding an approved gate result."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        result = {
            "score": 0.92,
            "completude": 1.0,
            "quality": 0.95,
            "reconciliation": 1.0,
            "errors": []
        }
        
        tracker.add_gate_result(1, result)
        assert len(tracker.gates) == 1
        assert tracker.gates[1].status == "approved"
        assert tracker.gates[1].score == 0.92
    
    def test_add_gate_result_conditional(self):
        """Test adding a conditional gate result."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        result = {
            "score": 0.75,
            "completude": 0.85,
            "quality": 0.80,
            "errors": ["minor_warning"]
        }
        
        tracker.add_gate_result(2, result)
        assert tracker.gates[2].status == "conditional"
        assert tracker.gates[2].errors_count == 1
    
    def test_add_gate_result_blocked(self):
        """Test adding a blocked gate result."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        result = {
            "score": 0.45,
            "completude": 0.5,
            "quality": 0.40,
            "errors": ["missing_artifact_1", "missing_artifact_2"]
        }
        
        tracker.add_gate_result(3, result)
        assert tracker.gates[3].status == "blocked"
        assert tracker.gates[3].errors_count == 2
    
    def test_add_gate_result_invalid_gate_number(self):
        """Test adding result with invalid gate number."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        result = {"score": 0.5}
        
        with pytest.raises(ValueError, match="gate_number must be 1, 2, or 3"):
            tracker.add_gate_result(4, result)
    
    def test_add_gate_result_invalid_result_type(self):
        """Test adding result with invalid type."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        with pytest.raises(ValueError, match="validation_result must be a dictionary"):
            tracker.add_gate_result(1, "invalid")
    
    def test_calculate_progress_no_gates(self):
        """Test progress calculation with no gates."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        assert tracker.calculate_progress() == 0.0
    
    def test_calculate_progress_mixed_gates(self):
        """Test progress calculation with mixed completude."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {"score": 0.9, "completude": 1.0, "quality": 0.9})
        tracker.add_gate_result(2, {"score": 0.8, "completude": 0.8, "quality": 0.8})
        tracker.add_gate_result(3, {"score": 0.5, "completude": 0.5, "quality": 0.5})
        
        progress = tracker.calculate_progress()
        # Average of [1.0, 0.8, 0.5] = 0.767 * 100 = 76.7%
        assert 76.0 < progress < 77.0
    
    def test_determine_overall_status_all_approved(self):
        """Test overall status when all gates approved."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        for gate_num in [1, 2, 3]:
            tracker.add_gate_result(gate_num, {
                "score": 0.90,
                "completude": 1.0,
                "quality": 0.95,
                "errors": []
            })
        
        assert tracker.determine_overall_status() == "approved_all"
    
    def test_determine_overall_status_any_blocked(self):
        """Test overall status when any gate is blocked."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        tracker.add_gate_result(2, {"score": 0.45, "completude": 0.5, "quality": 0.40, "errors": ["error1"]})
        tracker.add_gate_result(3, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        
        assert tracker.determine_overall_status() == "blocked_any"
    
    def test_determine_overall_status_any_conditional(self):
        """Test overall status with conditional gates."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        tracker.add_gate_result(2, {"score": 0.75, "completude": 0.8, "quality": 0.75, "errors": []})
        tracker.add_gate_result(3, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        
        assert tracker.determine_overall_status() == "conditional_any"
    
    def test_get_next_gate_missing_gate(self):
        """Test next gate detection when gate missing."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        
        assert tracker.get_next_gate() == 2
    
    def test_get_next_gate_blocked_gate(self):
        """Test next gate detection when gate blocked."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        tracker.add_gate_result(2, {"score": 0.45, "completude": 0.5, "quality": 0.40, "errors": ["error"]})
        
        assert tracker.get_next_gate() == 2  # Focus on fixing Gate 2
    
    def test_get_next_gate_all_approved(self):
        """Test next gate when all gates approved."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        for gate_num in [1, 2, 3]:
            tracker.add_gate_result(gate_num, {
                "score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []
            })
        
        assert tracker.get_next_gate() is None
    
    def test_get_status_complete(self):
        """Test get_status returns WaveStatus object."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        tracker.add_gate_result(2, {"score": 0.75, "completude": 0.8, "quality": 0.75, "errors": []})
        
        status = tracker.get_status()
        assert isinstance(status, WaveStatus)
        assert status.wave_id == "wave-001"
        assert status.project_name == "test-project"
        assert status.overall_status == "conditional_any"
        assert status.next_gate == 2
    
    def test_get_recommendations_blocked_gate(self):
        """Test recommendations for blocked gate."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        tracker.add_gate_result(1, {
            "score": 0.30, "completude": 0.3, "quality": 0.25, 
            "errors": ["error1", "error2", "error3"]
        })
        
        recs = tracker.get_recommendations()
        assert any("blocked" in r.lower() for r in recs)
        assert any("error" in r.lower() for r in recs)
    
    def test_get_recommendations_gate3_reconciliation_low(self):
        """Test recommendations when Gate 3 reconciliation low."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        
        for gate_num in [1, 2]:
            tracker.add_gate_result(gate_num, {
                "score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []
            })
        
        tracker.add_gate_result(3, {
            "score": 0.60, "completude": 1.0, "quality": 0.95, 
            "reconciliation": 0.60, "errors": []
        })
        
        recs = tracker.get_recommendations()
        assert any("reconciliation" in r.lower() for r in recs)
    
    def test_to_dict_conversion(self):
        """Test WaveStatus conversion to dict."""
        tracker = WaveStatusTracker("wave-001", "test-project")
        tracker.add_gate_result(1, {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []})
        
        status = tracker.get_status()
        status_dict = status.to_dict()
        
        assert "wave_id" in status_dict
        assert "gates" in status_dict
        assert "1" in status_dict["gates"]


class TestTrackWaveStatusHelper:
    """Test suite for track_wave_status helper function."""
    
    def test_track_wave_status_from_validation_results(self):
        """Test tracking wave status from validation results."""
        validation_results = {
            "gate_1": {"score": 0.90, "completude": 1.0, "quality": 0.95, "errors": []},
            "gate_2": {"score": 0.75, "completude": 0.8, "quality": 0.75, "errors": []},
            "gate_3": {"score": 0.75, "completude": 0.8, "quality": 0.75, "errors": []},
        }
        
        status = track_wave_status(validation_results, "wave-001", "test-project")
        
        assert status.wave_id == "wave-001"
        assert status.project_name == "test-project"
        assert len(status.gates) == 3
        assert status.overall_status == "conditional_any"
