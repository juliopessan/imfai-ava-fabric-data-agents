"""Tests for B-010: performance benchmark stage."""
import unittest

from scripts.performance_benchmark import (
    BenchmarkRun,
    BenchmarkReport,
    run_benchmark,
    BenchmarkStatus,
)


class PerformanceBenchmarkTests(unittest.TestCase):
    def test_pass_when_within_baseline(self) -> None:
        run = BenchmarkRun(
            wave_id="WAVE-001",
            entity="orders",
            rows_processed=1_000_000,
            duration_seconds=60.0,
            baseline_rows_per_second=10_000.0,  # 1M/60 ≈ 16k > baseline
        )
        report = run_benchmark(run)
        self.assertEqual(BenchmarkStatus.PASS, report.status)

    def test_fail_when_throughput_below_baseline(self) -> None:
        run = BenchmarkRun(
            wave_id="WAVE-001",
            entity="transactions",
            rows_processed=100,
            duration_seconds=60.0,
            baseline_rows_per_second=10_000.0,  # 100/60 ≈ 1.7 << 10k
        )
        report = run_benchmark(run)
        self.assertEqual(BenchmarkStatus.FAIL, report.status)

    def test_rows_per_second_computed(self) -> None:
        run = BenchmarkRun(
            wave_id="WAVE-001",
            entity="customers",
            rows_processed=300,
            duration_seconds=30.0,
            baseline_rows_per_second=5.0,
        )
        report = run_benchmark(run)
        self.assertAlmostEqual(10.0, report.rows_per_second, places=1)

    def test_report_includes_entity_and_wave(self) -> None:
        run = BenchmarkRun(
            wave_id="WAVE-002",
            entity="products",
            rows_processed=500,
            duration_seconds=10.0,
            baseline_rows_per_second=1.0,
        )
        report = run_benchmark(run)
        self.assertEqual("WAVE-002", report.wave_id)
        self.assertEqual("products", report.entity)

    def test_zero_duration_raises(self) -> None:
        run = BenchmarkRun(
            wave_id="WAVE-001",
            entity="edge",
            rows_processed=100,
            duration_seconds=0.0,
            baseline_rows_per_second=1.0,
        )
        with self.assertRaises(ValueError):
            run_benchmark(run)


if __name__ == "__main__":
    unittest.main()
