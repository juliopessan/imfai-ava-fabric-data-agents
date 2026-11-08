# Headroom Phase 1 — Execution Guide

Compression of agent handoffs with Headroom, with an automatic fallback to the
project compressor. This guide covers running it and its test suite.
It does not claim savings targets: the numbers reported by the code are
measured on the actual payloads handed off (1 token ≈ 4 characters).

## Components

| File | Role |
|------|------|
| `src/shared/scripts/headroom_context_manager.py` | Chooses the engine and compresses a handoff |
| `src/shared/scripts/migration_coordinator.py` | `MigrationCoordinator.process_handoff()` — calls the context manager, fail-open |
| `src/shared/tests/test_headroom_context_manager.py` | Engine selection, fallback, compression tests |
| `src/shared/tests/test_migration_coordinator.py` | Error/timeout/fail-open tests |

## Prerequisites

- Python 3.11 (same as `Dockerfile` and CI).
- Test runner: `pytest` (`pip install -r config/requirements-dev.txt`). The tests are
  `unittest.TestCase` classes, so `python -m unittest` also works with no install.
- Headroom is **optional**: `pip install headroom-ai` (see
  `reports/headroom/docs/HEADROOM-INTEGRATION-STRATEGY.md`). Without it the
  fallback compressor is used. The tests fake Headroom, so they need neither
  the package nor network access.

## Supported platforms

- Linux, macOS and Windows with Python 3.11 (fallback path is pure Python: runs everywhere).
- Headroom engine: only where the `headroom` package installs and imports
  (it has native parts). Everywhere else the fallback is selected automatically.

## Engine selection and fallback paths

1. `import headroom` succeeds and `use_mock=False` → **Headroom** (`stats.method == "headroom"`).
2. `headroom` missing (ImportError) or `use_mock=True` → **project fallback compressor**
   (`stats.method == "mock"`): minifies JSON; for other text removes trailing
   whitespace and repeated blank lines. Content is preserved.
3. Headroom raises or returns an unusable result at call time → same fallback, per call.
4. In `MigrationCoordinator.process_handoff()`, if compression raises (any engine) or
   exceeds `timeout_seconds` (default 30 s) → the **original payload is delivered
   unchanged**; `HandoffResult.compressed` is `False` and `HandoffResult.error` says why.

## Usage

```python
from src.shared.scripts.migration_coordinator import MigrationCoordinator

result = MigrationCoordinator(timeout_seconds=30).process_handoff(
    payload, source_agent="discovery-scout", target_agent="data-architect"
)
deliver(result.content)          # compressed, or original on failure/timeout
print(result.method, result.stats)
```

## Run the test suite

```bash
python -m pytest src/shared/tests -q                 # whole repository suite
python -m pytest src/shared/tests/test_headroom_context_manager.py \
                 src/shared/tests/test_migration_coordinator.py -v   # Headroom Phase 1 only
# without pytest:
python -m unittest src.shared.tests.test_headroom_context_manager \
                   src.shared.tests.test_migration_coordinator -v
```

## Out of scope (Phase 1)

Metrics dashboard, cloud telemetry, drift detection, and any savings target
without an observed benchmark.
