import unittest

from scripts.wave_status_tracker import (
    GateStatus,
    PhaseStatus,
    WaveStatusTracker,
)


class GateStatusTests(unittest.TestCase):
    def test_not_started_when_no_artifacts(self) -> None:
        gs = GateStatus(gate=1, artifacts_present=0, artifacts_total=5)
        self.assertEqual(gs.phase_status, PhaseStatus.NOT_STARTED)

    def test_in_progress_when_partial_artifacts(self) -> None:
        gs = GateStatus(gate=1, artifacts_present=3, artifacts_total=5)
        self.assertEqual(gs.phase_status, PhaseStatus.IN_PROGRESS)

    def test_complete_when_all_artifacts_no_score(self) -> None:
        gs = GateStatus(gate=1, artifacts_present=5, artifacts_total=5)
        self.assertEqual(gs.phase_status, PhaseStatus.COMPLETE)

    def test_complete_when_all_artifacts_and_passing_score(self) -> None:
        gs = GateStatus(gate=2, artifacts_present=5, artifacts_total=5, gate_score=88.0)
        self.assertEqual(gs.phase_status, PhaseStatus.COMPLETE)

    def test_blocked_when_all_artifacts_but_low_score(self) -> None:
        gs = GateStatus(gate=3, artifacts_present=8, artifacts_total=8, gate_score=65.0)
        self.assertEqual(gs.phase_status, PhaseStatus.BLOCKED)

    def test_artifacts_pct_zero_when_no_total(self) -> None:
        gs = GateStatus(gate=1)
        self.assertEqual(gs.artifacts_pct, 0.0)

    def test_artifacts_pct_calculation(self) -> None:
        gs = GateStatus(gate=2, artifacts_present=3, artifacts_total=5)
        self.assertEqual(gs.artifacts_pct, 60.0)


class WaveStatusTrackerTests(unittest.TestCase):
    def test_initial_state_all_not_started(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-001")
        summary = tracker.summary()
        self.assertEqual(summary.wave_id, "WAVE-001")
        self.assertEqual(summary.overall_pct, 0.0)
        for gs in summary.gates:
            self.assertEqual(gs.phase_status, PhaseStatus.NOT_STARTED)

    def test_set_gate_artifacts(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-002")
        tracker.set_gate_artifacts(1, present=5, total=5)
        tracker.set_gate_artifacts(2, present=3, total=5)
        tracker.set_gate_artifacts(3, present=0, total=8)

        summary = tracker.summary()
        self.assertEqual(summary.gates[0].artifacts_present, 5)
        self.assertEqual(summary.gates[1].artifacts_present, 3)
        self.assertEqual(summary.gates[2].artifacts_present, 0)
        # overall: 8 out of 18
        expected_pct = round(8 / 18 * 100, 1)
        self.assertEqual(summary.overall_pct, expected_pct)

    def test_set_gate_score(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-003")
        tracker.set_gate_artifacts(1, present=5, total=5)
        tracker.set_gate_score(1, 92.0)

        summary = tracker.summary()
        self.assertEqual(summary.gates[0].gate_score, 92.0)
        self.assertEqual(summary.gates[0].phase_status, PhaseStatus.COMPLETE)

    def test_invalid_gate_raises(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-X")
        with self.assertRaises(ValueError):
            tracker.set_gate_artifacts(4, present=1, total=1)
        with self.assertRaises(ValueError):
            tracker.set_gate_score(0, 80.0)

    def test_summary_str_contains_wave_id(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-010")
        tracker.set_gate_artifacts(1, present=5, total=5)
        tracker.set_gate_score(1, 88.0)
        output = str(tracker.summary())
        self.assertIn("WAVE-010", output)
        self.assertIn("Gate 1", output)
        self.assertIn("COMPLETE", output)

    def test_blocked_gate_appears_in_summary(self) -> None:
        tracker = WaveStatusTracker(wave_id="WAVE-BLK")
        tracker.set_gate_artifacts(3, present=8, total=8)
        tracker.set_gate_score(3, 55.0)
        summary = tracker.summary()
        self.assertEqual(summary.gates[2].phase_status, PhaseStatus.BLOCKED)


if __name__ == "__main__":
    unittest.main()
