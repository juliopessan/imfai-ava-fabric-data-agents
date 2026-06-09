"""
Tests for KPIDashboardReporter — Wave KPI aggregation and dashboard generation.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.kpi_dashboard_report import (
    KPIDashboardReporter, GateKPI, WaveKPI
)


class TestKPIDashboardReporter:
    """Test suite for KPIDashboardReporter."""
    
    def test_initialization(self):
        """Test reporter initialization."""
        reporter = KPIDashboardReporter()
        assert len(reporter.gate_kpis) == 0
        assert len(reporter.historical_waves) == 0
    
    def test_add_gate_kpi(self):
        """Test adding gate KPI."""
        reporter = KPIDashboardReporter()
        reporter.add_gate_kpi(
            gate_number=1,
            completude=0.95,
            quality=0.92,
            error_count=2,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            status="approved"
        )
        
        assert len(reporter.gate_kpis) == 1
        assert reporter.gate_kpis[1].completude == 0.95
        assert reporter.gate_kpis[1].error_rate == 0.1  # 2/20
    
    def test_add_multiple_gate_kpis(self):
        """Test adding multiple gate KPIs."""
        reporter = KPIDashboardReporter()
        
        for gate_num in [1, 2, 3]:
            reporter.add_gate_kpi(
                gate_number=gate_num,
                completude=0.90 + (gate_num * 0.02),
                quality=0.88 + (gate_num * 0.03),
                error_count=gate_num,
                total_entities=20,
                reconciliation=0.95,
                artifact_count=5,
                status="approved" if gate_num < 3 else "conditional"
            )
        
        assert len(reporter.gate_kpis) == 3
    
    def test_calculate_wave_kpi_no_gates(self):
        """Test wave KPI with no gates."""
        reporter = KPIDashboardReporter()
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 0.0)
        
        assert wave_kpi.total_gates == 0
        assert wave_kpi.trend == "blocked"
        assert len(wave_kpi.critical_blockers) > 0
    
    def test_calculate_wave_kpi_all_approved(self):
        """Test wave KPI with all gates approved."""
        reporter = KPIDashboardReporter()
        
        for gate_num in [1, 2, 3]:
            reporter.add_gate_kpi(
                gate_number=gate_num,
                completude=0.95,
                quality=0.93,
                error_count=1,
                total_entities=20,
                reconciliation=0.98,
                artifact_count=5,
                status="approved"
            )
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 95.0)
        
        assert wave_kpi.gates_approved == 3
        assert wave_kpi.gates_blocked == 0
        assert wave_kpi.trend == "on_track"
        assert wave_kpi.overall_completude == pytest.approx(0.95, rel=1e-5)
    
    def test_calculate_wave_kpi_some_blocked(self):
        """Test wave KPI with blocked gates."""
        reporter = KPIDashboardReporter()
        
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        reporter.add_gate_kpi(2, 0.40, 0.50, 10, 20, 0.0, 2, "blocked")
        reporter.add_gate_kpi(3, 0.90, 0.88, 2, 20, 0.95, 5, "approved")
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 50.0)
        
        assert wave_kpi.gates_blocked == 1
        assert wave_kpi.trend == "blocked"
        assert any(c.lower() for c in wave_kpi.critical_blockers if "gate" in c.lower())
    
    def test_calculate_wave_kpi_at_risk(self):
        """Test wave KPI trending at_risk."""
        reporter = KPIDashboardReporter()
        
        for gate_num in [1, 2, 3]:
            reporter.add_gate_kpi(
                gate_number=gate_num,
                completude=0.70,
                quality=0.75,
                error_count=3,
                total_entities=20,
                reconciliation=0.80,
                artifact_count=3,
                status="conditional"
            )
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 40.0)
        
        assert wave_kpi.trend == "at_risk"
    
    def test_get_dashboard_data(self):
        """Test generating dashboard data."""
        reporter = KPIDashboardReporter()
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 95.0)
        dashboard = reporter.get_dashboard_data(wave_kpi)
        
        assert "wave" in dashboard
        assert "metrics" in dashboard
        assert "quality" in dashboard
        assert "gates" in dashboard
        assert "blockers" in dashboard
        
        assert dashboard["wave"]["id"] == "wave-001"
        assert dashboard["metrics"]["total_gates"] == 1
    
    def test_get_trend_analysis_insufficient_data(self):
        """Test trend analysis with insufficient data."""
        reporter = KPIDashboardReporter()
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        reporter.calculate_wave_kpi("wave-001", "test-project", 95.0)
        
        analysis = reporter.get_trend_analysis()
        assert "message" in analysis or "insufficient" in str(analysis).lower()
    
    def test_get_trend_analysis_with_history(self):
        """Test trend analysis with historical data."""
        reporter = KPIDashboardReporter()
        
        # First wave
        reporter.add_gate_kpi(1, 0.80, 0.80, 5, 20, 0.90, 3, "conditional")
        reporter.calculate_wave_kpi("wave-001", "test-project", 50.0)
        
        # Second wave (improved)
        reporter.gate_kpis = {}
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        reporter.calculate_wave_kpi("wave-002", "test-project", 95.0)
        
        analysis = reporter.get_trend_analysis()
        assert "progress_delta" in analysis
        assert analysis["progress_delta"] == 45.0  # 95 - 50
        assert analysis["trend_direction"] == "improving"
    
    def test_save_dashboard(self):
        """Test saving dashboard to file."""
        reporter = KPIDashboardReporter()
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 95.0)
        dashboard = reporter.get_dashboard_data(wave_kpi)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "dashboard.json"
            reporter.save_dashboard(dashboard, output_path)
            
            assert output_path.exists()
            with open(output_path) as f:
                saved = json.load(f)
            
            assert saved["wave"]["id"] == "wave-001"
    
    def test_get_kpi_summary_text(self):
        """Test generating summary text."""
        reporter = KPIDashboardReporter()
        reporter.add_gate_kpi(1, 0.95, 0.93, 1, 20, 0.98, 5, "approved")
        
        wave_kpi = reporter.calculate_wave_kpi("wave-001", "test-project", 95.0)
        summary = reporter.get_kpi_summary_text(wave_kpi)
        
        assert "wave-001" in summary
        assert "ON_TRACK" in summary
        assert "95.0%" in summary
