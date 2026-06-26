"""
Real OTel tracing for migration gate transitions.

Implements docs/OBSERVABILITY-AND-TRACES.md using the standard OpenTelemetry
SDK directly instead of the bespoke TraceContext/SpanCollector sketched in
that doc. Spans are real OTel spans from the start, so Azure Monitor (or any
other OTel-compatible backend) can be wired in later as just another
exporter — nothing about how spans are created needs to change.

Default sink: a JSONL file under the wave's outputs directory. No Azure
credentials required to get real traces today.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Sequence

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)

logger = logging.getLogger(__name__)

_lock = Lock()
_providers_by_trace_file: Dict[Path, TracerProvider] = {}


class JSONLSpanExporter(SpanExporter):
    """Append-only JSONL span sink — no external service, no credentials."""

    def __init__(self, output_file: Path):
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        try:
            with self.output_file.open("a", encoding="utf-8") as fh:
                for span in spans:
                    fh.write(json.dumps(self._span_to_dict(span)) + "\n")
            return SpanExportResult.SUCCESS
        except Exception:
            logger.exception("JSONLSpanExporter failed to write spans to %s", self.output_file)
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:  # pragma: no cover - nothing to release
        pass

    @staticmethod
    def _span_to_dict(span: ReadableSpan) -> Dict[str, Any]:
        ctx = span.get_span_context()
        parent = span.parent
        duration_ms = None
        if span.end_time and span.start_time:
            duration_ms = (span.end_time - span.start_time) / 1_000_000
        return {
            "trace_id": format(ctx.trace_id, "032x"),
            "span_id": format(ctx.span_id, "016x"),
            "parent_span_id": format(parent.span_id, "016x") if parent else None,
            "name": span.name,
            "duration_ms": duration_ms,
            "status": span.status.status_code.name,
            "attributes": dict(span.attributes or {}),
        }


def get_tracer(
    trace_file: str | Path,
    service_name: str = "dmf-migration-coordinator",
    *,
    use_simple_processor: bool = False,
) -> trace.Tracer:
    """Return a real OTel tracer that writes spans to *trace_file* (JSONL).

    `use_simple_processor=True` exports each span synchronously — useful for
    tests/CLI runs where the process exits immediately after the last span
    and a BatchSpanProcessor's background flush might not get a chance to run.
    """
    trace_file = Path(trace_file)

    with _lock:
        provider = _providers_by_trace_file.get(trace_file)
        if provider is None:
            provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
            exporter = JSONLSpanExporter(trace_file)
            processor = SimpleSpanProcessor(exporter) if use_simple_processor else BatchSpanProcessor(exporter)
            provider.add_span_processor(processor)
            _providers_by_trace_file[trace_file] = provider

    return provider.get_tracer(service_name)
