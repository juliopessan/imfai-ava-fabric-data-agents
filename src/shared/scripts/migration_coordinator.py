#!/usr/bin/env python3
"""
Migration Coordinator — Headroom handoff integration (Phase 1).

Compresses the payload handed from one agent to the next. Compression is an
optimisation only: if the compressor raises or exceeds the timeout, the
ORIGINAL payload is delivered unchanged and the failure is reported in the
result (never raised).
"""
from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from .headroom_context_manager import HeadroomContextManager
except ImportError:  # executed as a plain script
    from headroom_context_manager import HeadroomContextManager

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass
class HandoffResult:
    """Outcome of a coordinated handoff."""
    content: Any  # what the next agent receives
    compressed: bool
    method: Optional[str] = None  # "headroom" | "mock" | None when not compressed
    error: Optional[str] = None  # set when the original was delivered due to a failure
    stats: Optional[Dict[str, Any]] = None


class MigrationCoordinator:
    """Coordinates agent handoffs with safe (fail-open) compression."""

    def __init__(
        self,
        context_manager: HeadroomContextManager | None = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    ):
        self.context_manager = context_manager or HeadroomContextManager()
        self.timeout_seconds = timeout_seconds

    def process_handoff(
        self, payload: str | dict, source_agent: str, target_agent: str
    ) -> HandoffResult:
        """Compress ``payload``; on error or timeout deliver it unchanged."""
        outcome: Dict[str, Any] = {}

        def _run() -> None:
            try:
                outcome["value"] = self.context_manager.compress_handoff(
                    payload, source_agent, target_agent
                )
            except BaseException as exc:  # noqa: BLE001 - fail open on anything
                outcome["error"] = exc

        worker = threading.Thread(target=_run, name="handoff-compress", daemon=True)
        worker.start()
        worker.join(self.timeout_seconds)

        if worker.is_alive():
            error = f"compression timed out after {self.timeout_seconds}s"
        elif "error" in outcome:
            exc = outcome["error"]
            error = f"{type(exc).__name__}: {exc}"
        else:
            compressed, stats = outcome["value"]
            return HandoffResult(
                content=compressed,
                compressed=True,
                method=stats.method,
                stats=stats.to_dict(),
            )

        logger.warning(
            f"Handoff {source_agent} → {target_agent}: {error}. Delivering original payload."
        )
        return HandoffResult(content=payload, compressed=False, error=error)
