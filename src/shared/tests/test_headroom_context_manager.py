"""
Tests for HeadroomContextManager — engine selection, fallback and compression.

Written with unittest.TestCase so they run under pytest and plain unittest.
Headroom is faked through sys.modules, so no native dependency is needed.
"""

import json
import sys
import types
import unittest
from unittest import mock

from src.shared.scripts.headroom_context_manager import HeadroomContextManager

PAYLOAD = {
    "table": "fact_sales",
    "columns": [f"col_{i}" for i in range(40)],
    "rows": 1000,
}


def fake_headroom(compress=None):
    """Build a fake `headroom` module whose compress() calls are recorded."""
    module = types.ModuleType("headroom")
    module.calls = []

    def default_compress(data, config=None):
        module.calls.append((data, config))
        return data[: len(data) // 2]

    module.compress = compress or default_compress
    module.Configuration = lambda model=None: {"model": model}
    return module


class TestEngineSelection(unittest.TestCase):
    def test_headroom_installed_is_detected(self):
        with mock.patch.dict(sys.modules, {"headroom": fake_headroom()}):
            manager = HeadroomContextManager()
        self.assertTrue(manager.headroom_available)
        self.assertFalse(manager.use_mock)

    def test_headroom_missing_is_detected(self):
        with mock.patch.dict(sys.modules, {"headroom": None}):
            manager = HeadroomContextManager()
        self.assertFalse(manager.headroom_available)
        self.assertTrue(manager.use_mock)

    def test_use_mock_forces_fallback_even_if_headroom_installed(self):
        with mock.patch.dict(sys.modules, {"headroom": fake_headroom()}):
            manager = HeadroomContextManager(use_mock=True)
        self.assertFalse(manager.headroom_available)


class TestHeadroomEngine(unittest.TestCase):
    def test_compress_goes_through_headroom_engine(self):
        module = fake_headroom()
        with mock.patch.dict(sys.modules, {"headroom": module}):
            manager = HeadroomContextManager()
            with mock.patch.object(manager, "_compress_mock") as fallback:
                compressed, stats = manager.compress_handoff(PAYLOAD, "a", "b", model="m1")
        self.assertEqual(len(module.calls), 1)
        self.assertEqual(module.calls[0][1], {"model": "m1"})
        fallback.assert_not_called()
        self.assertEqual(stats.method, "headroom")
        self.assertEqual(compressed, module.calls[0][0][: len(module.calls[0][0]) // 2])

    def test_headroom_exception_falls_back_to_project_compressor(self):
        def boom(data, config=None):
            raise RuntimeError("native crash")

        with mock.patch.dict(sys.modules, {"headroom": fake_headroom(boom)}):
            manager = HeadroomContextManager()
            compressed, stats = manager.compress_handoff(PAYLOAD, "a", "b")
        self.assertEqual(stats.method, "mock")
        self.assertEqual(json.loads(compressed), PAYLOAD)

    def test_headroom_unusable_result_falls_back(self):
        with mock.patch.dict(sys.modules, {"headroom": fake_headroom(lambda d, config=None: 42)}):
            manager = HeadroomContextManager()
            _, stats = manager.compress_handoff(PAYLOAD, "a", "b")
        self.assertEqual(stats.method, "mock")

    def test_headroom_result_object_with_content_is_accepted(self):
        result = types.SimpleNamespace(content="short")
        with mock.patch.dict(
            sys.modules, {"headroom": fake_headroom(lambda d, config=None: result)}
        ):
            manager = HeadroomContextManager()
            compressed, stats = manager.compress_handoff(PAYLOAD, "a", "b")
        self.assertEqual(compressed, "short")
        self.assertEqual(stats.method, "headroom")


class TestFallbackEngine(unittest.TestCase):
    def test_native_dependency_absent_calls_fallback_compressor(self):
        with mock.patch.dict(sys.modules, {"headroom": None}):
            manager = HeadroomContextManager()
            with mock.patch.object(
                manager, "_compress_mock", return_value="x"
            ) as fallback:
                compressed, stats = manager.compress_handoff(PAYLOAD, "a", "b")
        fallback.assert_called_once()
        self.assertEqual(compressed, "x")
        self.assertEqual(stats.method, "mock")

    def test_fallback_minifies_json_without_losing_content(self):
        manager = HeadroomContextManager(use_mock=True)
        compressed, stats = manager.compress_handoff(PAYLOAD, "a", "b")
        self.assertEqual(json.loads(compressed), PAYLOAD)
        self.assertLess(len(compressed), len(json.dumps(PAYLOAD, indent=2)))
        self.assertGreater(stats.tokens_saved, 0)

    def test_fallback_collapses_blank_lines_and_trailing_spaces(self):
        manager = HeadroomContextManager(use_mock=True)
        text = "# Title   \n\n\n\nbody line  \n\n"
        self.assertEqual(manager._compress_mock(text, "m"), "# Title\n\nbody line")


class TestCompressionStats(unittest.TestCase):
    def test_stats_are_measured_from_real_output(self):
        manager = HeadroomContextManager(use_mock=True)
        text = json.dumps(PAYLOAD, indent=4)
        compressed, stats = manager.compress_handoff(text, "a", "b")
        self.assertEqual(stats.input_tokens, len(text) // 4)
        self.assertEqual(stats.output_tokens, len(compressed) // 4)
        self.assertEqual(stats.tokens_saved, stats.input_tokens - stats.output_tokens)
        self.assertAlmostEqual(
            stats.compression_ratio, stats.tokens_saved / stats.input_tokens
        )

    def test_empty_payload_does_not_fail(self):
        manager = HeadroomContextManager(use_mock=True)
        compressed, stats = manager.compress_handoff("", "a", "b")
        self.assertEqual(compressed, "")
        self.assertEqual(stats.input_tokens, 1)

    def test_aggregated_stats_by_agent_pair(self):
        manager = HeadroomContextManager(use_mock=True)
        manager.compress_handoff(PAYLOAD, "scout", "architect")
        manager.compress_handoff(PAYLOAD, "scout", "architect")
        summary = manager.get_stats()
        self.assertEqual(summary["total_handoffs"], 2)
        self.assertEqual(summary["by_agent"]["scout → architect"]["count"], 2)
        self.assertEqual(summary["method"], "mock")


if __name__ == "__main__":
    unittest.main()
