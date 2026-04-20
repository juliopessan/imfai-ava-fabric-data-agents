"""
reconciliation_checks.py
B-009 — Row-count and checksum reconciliation for high-risk entities.

Supports two operation modes:

**DISCONNECTED mode** (default): operator extracts data from source and target
systems externally (CSV export, manual query) and passes the rows as Python
lists or CSV file paths.  No live database connection is required by this
module.

**CONNECTED mode**: operator provides callable adapters (``RowLoader``) that
fetch rows on demand — e.g., a function that runs a SQL query and returns
``list[dict]``.  The module invokes these callables and then applies the same
checksum / row-count logic.

Checksum is computed as SHA-256 of the canonical JSON serialization of all
rows (sorted by key for determinism). Row count is checked independently.

Usage — disconnected (in-memory):
    from scripts.reconciliation_checks import reconcile_checksums

    report = reconcile_checksums(
        entity="orders",
        source_rows=[{"id": 1, "amount": 100}, ...],
        target_rows=[{"id": 1, "amount": 100}, ...],
    )
    print(report)

Usage — disconnected (CSV files):
    from scripts.reconciliation_checks import reconcile_from_sources, ReconciliationMode
    from pathlib import Path

    report = reconcile_from_sources(
        entity="orders",
        source_loader=Path("exports/source_orders.csv"),
        target_loader=Path("exports/target_orders.csv"),
        mode=ReconciliationMode.DISCONNECTED,
    )

Usage — connected (callable adapters):
    from scripts.reconciliation_checks import reconcile_from_sources, ReconciliationMode

    def fetch_source() -> list[dict]:
        # e.g. execute SQL query against source system
        return [{"id": 1, "amount": 100}]

    def fetch_target() -> list[dict]:
        # e.g. execute SQL query against target platform
        return [{"id": 1, "amount": 100}]

    report = reconcile_from_sources(
        entity="orders",
        source_loader=fetch_source,
        target_loader=fetch_target,
        mode=ReconciliationMode.CONNECTED,
    )
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Union


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

RowLoader = Union[
    list[dict],          # in-memory rows (disconnected shorthand)
    Path,                # CSV file path (disconnected file-based)
    Callable[[], list[dict]],  # callable adapter (connected)
]


class ReconciliationMode(Enum):
    """Operation mode for reconciliation data retrieval.

    DISCONNECTED: rows are supplied externally (in-memory lists or CSV files).
                  No live database connection is needed.
    CONNECTED:    rows are fetched via callable adapters provided by the
                  operator (e.g., SQL query functions, REST API calls).
    """
    DISCONNECTED = "DISCONNECTED"
    CONNECTED = "CONNECTED"


class ReconciliationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ReconciliationReport:
    entity: str
    status: ReconciliationStatus
    source_count: int
    target_count: int
    source_checksum: str
    target_checksum: str
    count_mismatch: bool
    checksum_mismatch: bool
    mode: ReconciliationMode = ReconciliationMode.DISCONNECTED

    def __str__(self) -> str:
        lines = [
            f"Reconciliation [{self.entity}] ({self.mode.value}): {self.status.value}",
            f"  Source rows  : {self.source_count}",
            f"  Target rows  : {self.target_count}",
            f"  Source SHA256: {self.source_checksum[:16]}...",
            f"  Target SHA256: {self.target_checksum[:16]}...",
        ]
        if self.count_mismatch:
            lines.append(f"  ERROR: row count mismatch ({self.source_count} != {self.target_count})")
        if self.checksum_mismatch:
            lines.append("  ERROR: checksum mismatch — data was modified")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _canonical_json(rows: list[dict]) -> str:
    """Produce a deterministic JSON string for a list of dicts."""
    normalized = [
        {k: row[k] for k in sorted(row.keys())}
        for row in rows
    ]
    return json.dumps(normalized, sort_keys=True, ensure_ascii=False)


def compute_checksum(rows: list[dict]) -> str:
    """SHA-256 checksum of the canonical row set."""
    payload = _canonical_json(rows).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_rows_from_csv(path: Path) -> list[dict]:
    """Load rows from a CSV file as a list of dicts.

    Each row in the CSV becomes a ``dict`` keyed by the header names.
    All values are strings; callers requiring typed values should cast
    after loading.

    Args:
        path: Path to the CSV file.

    Returns:
        List of row dicts.

    Raises:
        FileNotFoundError: if *path* does not exist.
        ValueError: if the CSV has no header row.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header row: {path}")
        return [dict(row) for row in reader]


def _resolve_loader(loader: RowLoader, mode: ReconciliationMode) -> list[dict]:
    """Resolve a RowLoader to a concrete list of rows.

    Dispatch table:
    - ``list``      → returned as-is (in-memory disconnected)
    - ``Path``      → CSV load (file-based disconnected)
    - ``callable``  → called with no args (connected adapter)
    """
    if isinstance(loader, list):
        return loader
    if isinstance(loader, Path):
        if mode is ReconciliationMode.CONNECTED:
            raise ValueError(
                "Path-based loaders require DISCONNECTED mode. "
                "Use a callable adapter for CONNECTED mode."
            )
        return load_rows_from_csv(loader)
    if callable(loader):
        return loader()
    raise TypeError(f"Unsupported RowLoader type: {type(loader)!r}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def reconcile_checksums(
    entity: str,
    source_rows: list[dict],
    target_rows: list[dict],
) -> ReconciliationReport:
    """Compare source and target by row count and SHA-256 checksum.

    This is the original disconnected in-memory API.  Rows must be provided
    as Python lists — no database connection is made.
    """
    src_checksum = compute_checksum(source_rows)
    tgt_checksum = compute_checksum(target_rows)
    count_mismatch = len(source_rows) != len(target_rows)
    checksum_mismatch = src_checksum != tgt_checksum
    passed = not count_mismatch and not checksum_mismatch
    return ReconciliationReport(
        entity=entity,
        status=ReconciliationStatus.PASS if passed else ReconciliationStatus.FAIL,
        source_count=len(source_rows),
        target_count=len(target_rows),
        source_checksum=src_checksum,
        target_checksum=tgt_checksum,
        count_mismatch=count_mismatch,
        checksum_mismatch=checksum_mismatch,
        mode=ReconciliationMode.DISCONNECTED,
    )


def reconcile_from_sources(
    entity: str,
    source_loader: RowLoader,
    target_loader: RowLoader,
    mode: ReconciliationMode = ReconciliationMode.DISCONNECTED,
) -> ReconciliationReport:
    """High-level reconciliation API supporting both operation modes.

    Args:
        entity:        Entity name (for reporting).
        source_loader: Source data — list of dicts, Path to CSV, or callable.
        target_loader: Target data — list of dicts, Path to CSV, or callable.
        mode:          ``ReconciliationMode.DISCONNECTED`` (default) or
                       ``ReconciliationMode.CONNECTED``.

    Returns:
        ``ReconciliationReport`` with status, counts, and checksums.

    Examples:
        # Disconnected — CSV files exported from source/target:
        reconcile_from_sources(
            "orders",
            Path("exports/src.csv"),
            Path("exports/tgt.csv"),
            mode=ReconciliationMode.DISCONNECTED,
        )

        # Connected — callable adapters:
        reconcile_from_sources(
            "orders",
            source_loader=lambda: db_source.query("SELECT * FROM orders"),
            target_loader=lambda: db_target.query("SELECT * FROM orders"),
            mode=ReconciliationMode.CONNECTED,
        )
    """
    source_rows = _resolve_loader(source_loader, mode)
    target_rows = _resolve_loader(target_loader, mode)

    src_checksum = compute_checksum(source_rows)
    tgt_checksum = compute_checksum(target_rows)
    count_mismatch = len(source_rows) != len(target_rows)
    checksum_mismatch = src_checksum != tgt_checksum
    passed = not count_mismatch and not checksum_mismatch

    return ReconciliationReport(
        entity=entity,
        status=ReconciliationStatus.PASS if passed else ReconciliationStatus.FAIL,
        source_count=len(source_rows),
        target_count=len(target_rows),
        source_checksum=src_checksum,
        target_checksum=tgt_checksum,
        count_mismatch=count_mismatch,
        checksum_mismatch=checksum_mismatch,
        mode=mode,
    )
