"""
Tests for MigrationCoordinator — fail-open handoff compression.

Written with unittest.TestCase so they run under pytest and plain unittest.
"""

import sys
import threading
import unittest
from unittest import mock

from src.shared.scripts.headroom_context_manager import HeadroomContextManager
from src.shared.scripts.migration_coordinator import MigrationCoordinator

ORIGINAL = '{\n  "entities": 45,\n  "metrics": 1200\n}'


class RaisingManager:
    def compress_handoff(self, data, source, target, model="gpt-4o"):
        raise RuntimeError("compressor exploded")


class HangingManager:
    def __init__(self):
        self.release = threading.Event()

    def compress_handoff(self, data, source, target, model="gpt-4o"):
        self.release.wait(5)
        return "late", None


class TestMigrationCoordinator(unittest.TestCase):
    def test_compressor_error_delivers_original_unchanged(self):
        result = MigrationCoordinator(RaisingManager()).process_handoff(ORIGINAL, "a", "b")
        self.assertIs(result.content, ORIGINAL)
        self.assertFalse(result.compressed)
        self.assertIn("RuntimeError", result.error)

    def test_compressor_timeout_delivers_original_unchanged(self):
        manager = HangingManager()
        try:
            coordinator = MigrationCoordinator(manager, timeout_seconds=0.05)
            result = coordinator.process_handoff(ORIGINAL, "a", "b")
        finally:
            manager.release.set()
        self.assertIs(result.content, ORIGINAL)
        self.assertFalse(result.compressed)
        self.assertIn("timed out", result.error)

    def test_dict_payload_is_delivered_as_same_object_on_error(self):
        payload = {"entities": 45}
        result = MigrationCoordinator(RaisingManager()).process_handoff(payload, "a", "b")
        self.assertIs(result.content, payload)
        self.assertEqual(payload, {"entities": 45})

    def test_success_delivers_compressed_content_and_stats(self):
        manager = HeadroomContextManager(use_mock=True)
        result = MigrationCoordinator(manager).process_handoff(ORIGINAL, "scout", "architect")
        self.assertTrue(result.compressed)
        self.assertIsNone(result.error)
        self.assertEqual(result.content, '{"entities":45,"metrics":1200}')
        self.assertEqual(result.method, "mock")
        self.assertEqual(result.stats["target_agent"], "architect")

    def test_coordinator_uses_fallback_when_headroom_absent(self):
        with mock.patch.dict(sys.modules, {"headroom": None}):
            coordinator = MigrationCoordinator()
        result = coordinator.process_handoff(ORIGINAL, "a", "b")
        self.assertTrue(result.compressed)
        self.assertEqual(result.method, "mock")


if __name__ == "__main__":
    unittest.main()
