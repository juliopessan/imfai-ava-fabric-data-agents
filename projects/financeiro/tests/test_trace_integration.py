#!/usr/bin/env python3
"""Tests for TraceWriter integration in the (simulated) Financeiro waves 1-4 orchestrator.

Run from the repository root (works with pytest or plain unittest):
    python3 -m unittest projects/financeiro/tests/test_trace_integration.py
All trace output goes to temporary directories; no external service is used.
"""

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "projects" / "financeiro" / "scripts" / "FINANCEIRO_WAVES_1-4_PARALLEL_OPTIMIZED.py"

_spec = importlib.util.spec_from_file_location("financeiro_parallel_orchestrator", SCRIPT)
orch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orch)

WAVES = ["Wave 1", "Wave 2", "Wave 3", "Wave 4"]
GATES = [1, 2, 3]


def read_events(root):
    """Return every JSONL event under root; fails if any line is not valid JSON."""
    events = []
    for path in sorted(Path(root).rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            events.append(json.loads(line))
    return events


class TempTraceTestCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.trace_root = self.tmp / ".trace-logs"
        self.writer = orch.build_trace_writer(self.trace_root)

    def assert_one_event_per_gate(self, events, mode):
        keys = [(e["context"]["wave_id"], e["context"]["gate"]) for e in events
                if e["context"]["execution_mode"] == mode]
        self.assertEqual(len(keys), 12)
        self.assertEqual(sorted(keys), sorted((w, g) for w in WAVES for g in GATES))


class GateTraceTests(TempTraceTestCase):
    def test_serial_emits_one_event_per_gate(self):
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        o.execute_serial()
        events = read_events(self.trace_root)
        self.assert_one_event_per_gate(events, "serial")
        self.assertEqual(len(events), 12)
        self.assertEqual(o.trace_events_written, 12)

    def test_parallel_emits_one_event_per_gate_with_shared_writer(self):
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        o.execute_parallel()
        self.assertIs(o.trace_writer, self.writer)
        events = read_events(self.trace_root)
        self.assert_one_event_per_gate(events, "parallel")
        self.assertEqual(len(events), 12)
        self.assertEqual(len({e["trace_id"] for e in events}), 12)

    def test_event_fields_and_simulation_markers(self):
        orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer).execute_serial()
        for e in read_events(self.trace_root):
            self.assertEqual(e["trace_type"], "gate_scoring")
            self.assertTrue(e["context"]["wave"].startswith("financeiro-wave"))
            self.assertIn(e["context"]["gate"], GATES)
            self.assertEqual(e["operation"]["status"], "success")
            self.assertGreater(e["operation"]["duration_sec"], 0)
            self.assertEqual(e["metadata"]["data_origin"], "simulated")
            self.assertEqual(e["metadata"]["environment"], "simulation")
            self.assertIn("simulated", e["tags"])
            self.assertIn("estimated-metrics", e["tags"])
            # duration is the only measured value; tokens/cost/scores are estimates
            self.assertEqual(list(e["metrics"]["measured"]), ["duration_sec"])
            self.assertEqual(e["metrics"]["measured"]["duration_sec"], e["operation"]["duration_sec"])
            self.assertEqual(set(e["metrics"]["estimated"]), set(orch.ESTIMATED_FIELDS))
            self.assertEqual(e["metadata"]["estimated_fields"], orch.ESTIMATED_FIELDS)
            self.assertEqual(e["metadata"]["measured_fields"], ["duration_sec"])

    def test_no_etl_or_migration_events(self):
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        o.execute_serial()
        o.execute_parallel()
        events = read_events(self.trace_root)
        self.assertEqual({e["trace_type"] for e in events}, {"gate_scoring"})
        for sub in ("etl", "migrations", "agents", "workflows"):
            self.assertEqual(list((self.trace_root / sub).glob("*.jsonl")), [])

    def test_serial_and_parallel_share_one_writer(self):
        serial = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        parallel = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        serial.execute_serial()
        parallel.execute_parallel()
        events = read_events(self.trace_root)
        self.assertEqual(len(events), 24)
        self.assert_one_event_per_gate(events, "serial")
        self.assert_one_event_per_gate(events, "parallel")

    def test_concurrent_orchestrators_keep_valid_jsonl(self):
        orchestrators = [orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer) for _ in range(3)]
        threads = [threading.Thread(target=o.execute_parallel) for o in orchestrators]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        events = read_events(self.trace_root)  # raises on any corrupted line
        self.assertEqual(len(events), 36)
        by_run = {}
        for e in events:
            by_run.setdefault(e["context"]["run_id"], []).append(e)
        self.assertEqual(len(by_run), 3)
        for run_events in by_run.values():
            self.assert_one_event_per_gate(run_events, "parallel")

    def test_tracing_is_off_without_writer(self):
        o = orch.FinanceiroBrallelOrchestrator()
        waves, _ = o.execute_serial()
        self.assertEqual(sorted(waves), WAVES)
        self.assertEqual(o.trace_events_written, 0)
        self.assertEqual(read_events(self.trace_root), [])


class FailureTests(TempTraceTestCase):
    @staticmethod
    def _fail_wave2_gate2(o):
        original = o._calculate_tokens

        def failing(wave_id, gate_id, cached=False):
            if wave_id == "Wave 2" and gate_id == "GATE2":
                raise ValueError("simulated gate failure")
            return original(wave_id, gate_id, cached)

        o._calculate_tokens = failing

    def _assert_failure_event(self, mode):
        events = read_events(self.trace_root)
        failed = [e for e in events if e["operation"]["status"] == "failure"]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["context"]["wave_id"], "Wave 2")
        self.assertEqual(failed[0]["context"]["gate"], 2)
        self.assertEqual(failed[0]["context"]["execution_mode"], mode)
        self.assertIn("simulated gate failure", failed[0]["operation"]["error"])
        self.assertEqual(failed[0]["metrics"]["estimated"], {})
        self.assertIsNone(failed[0]["metadata"]["simulated_gate_result"])
        # no event for the gate that never ran
        self.assertNotIn(("Wave 2", 3), [(e["context"]["wave_id"], e["context"]["gate"]) for e in events])

    def test_gate_failure_serial_is_raised_and_traced(self):
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        self._fail_wave2_gate2(o)
        with self.assertRaisesRegex(ValueError, "simulated gate failure"):
            o.execute_serial()
        self._assert_failure_event("serial")

    def test_gate_failure_parallel_is_raised_and_traced(self):
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        self._fail_wave2_gate2(o)
        with self.assertRaisesRegex(ValueError, "simulated gate failure"):
            o.execute_parallel()
        self._assert_failure_event("parallel")

    def test_trace_write_returning_none_is_reported(self):
        class BrokenWriter:
            def write_trace(self, *args, **kwargs):
                return None  # same contract as TraceWriter on validation/write error

        o = orch.FinanceiroBrallelOrchestrator(trace_writer=BrokenWriter())
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(orch.TraceCaptureError) as ctx:
            o.execute_serial()
        self.assertEqual(len(ctx.exception.errors), 12)  # every gate still ran and every failure is listed
        self.assertEqual(len(o.wave_metrics), 4)
        self.assertEqual(o.trace_events_written, 0)
        self.assertIn("Trace not written", stderr.getvalue())

    def test_trace_write_exception_is_reported_in_parallel(self):
        class RaisingWriter:
            def write_trace(self, *args, **kwargs):
                raise OSError("disk full")

        o = orch.FinanceiroBrallelOrchestrator(trace_writer=RaisingWriter())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(orch.TraceCaptureError) as ctx:
            o.execute_parallel()
        self.assertEqual(len(ctx.exception.errors), 12)
        self.assertIn("disk full", str(ctx.exception))

    def test_real_writer_write_error_is_reported(self):
        # make the real TraceWriter fail to open its output file
        gates_dir = self.trace_root / "gates"
        gates_dir.rmdir()
        gates_dir.write_text("not a directory", encoding="utf-8")
        o = orch.FinanceiroBrallelOrchestrator(trace_writer=self.writer)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(orch.TraceCaptureError):
            o.execute_serial()
        self.assertEqual(o.trace_events_written, 0)


class CliTests(unittest.TestCase):
    def _run(self, cwd, *args, env_extra=None):
        env = {k: v for k, v in os.environ.items() if k != orch.TRACE_DIR_ENV}
        env.update(env_extra or {})
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, env=env,
                              capture_output=True, text=True, timeout=120)

    def test_cli_trace_dir_captures_both_runs_and_states_simulation(self):
        with tempfile.TemporaryDirectory() as tmp:
            trace_dir = Path(tmp) / "traces"
            result = self._run(tmp, "--trace-dir", str(trace_dir))
            self.assertEqual(result.returncode, 0, result.stderr)
            events = read_events(trace_dir)
            self.assertEqual(len(events), 24)
            for mode in ("serial", "parallel"):
                keys = [(e["context"]["wave_id"], e["context"]["gate"]) for e in events
                        if e["context"]["execution_mode"] == mode]
                self.assertEqual(sorted(keys), sorted((w, g) for w in WAVES for g in GATES))
            self.assertIn("SIMULATED", result.stdout)

    def test_cli_env_var_enables_tracing_and_default_is_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            trace_dir = Path(tmp) / "env-traces"
            result = self._run(tmp, env_extra={orch.TRACE_DIR_ENV: str(trace_dir)})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(read_events(trace_dir)), 24)
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(tmp).rglob("*.jsonl")), [])
            self.assertNotIn("Gate traces", result.stdout)


if __name__ == "__main__":
    unittest.main()
