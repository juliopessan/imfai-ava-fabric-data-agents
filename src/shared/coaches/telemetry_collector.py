"""
DMF Coach — Telemetry Collector

Captures agent execution events and stores them for analysis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TelemetryCollector:
    """Collects and stores agent execution telemetry."""

    def __init__(self, telemetry_dir: str = ".coach/telemetry"):
        self.telemetry_dir = Path(telemetry_dir)
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)

    def log_execution(
        self,
        agent_id: str,
        wave: str,
        gate: int,
        model: str,
        tokens_in: int,
        tokens_out: int,
        artifact_filename: str,
        artifact_size: int,
        execution_time_sec: float,
        status: str = "success",
        artifact_lines: Optional[int] = None,
        artifact_sections: Optional[int] = None,
        artifact_entities: Optional[int] = None,
        validation_passed: bool = True,
        context_window_used_pct: Optional[float] = None,
        auto_compactions: int = 0,
        context_resets: int = 0,
        agent_role: Optional[str] = None,
        model_provider: str = "anthropic",
        input_cost_per_mille: float = 3.00,
        output_cost_per_mille: float = 15.00,
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Log an agent execution event.

        Args:
            agent_id: Agent identifier (e.g., 'data-architect')
            wave: Wave name (e.g., 'clientebanco_wave_2')
            gate: Gate number (1, 2, or 3)
            model: Model name (e.g., 'claude-opus-4-1')
            tokens_in: Input tokens consumed
            tokens_out: Output tokens generated
            artifact_filename: Name of output file (e.g., 'architecture.md')
            artifact_size: Artifact size in bytes
            execution_time_sec: Execution duration in seconds
            status: Execution status ('success', 'partial', 'error', 'timeout')
            ... (optional fields)

        Returns:
            Dict containing the recorded event
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        total_tokens = tokens_in + tokens_out
        cost_usd = (
            tokens_in * input_cost_per_mille / 1000.0
            + tokens_out * output_cost_per_mille / 1000.0
        )

        event = {
            "timestamp": timestamp,
            "wave": wave,
            "gate": gate,
            "agent_id": agent_id,
            "agent_role": agent_role or f"Agent {agent_id}",
            "model": {
                "provider": model_provider,
                "name": model,
                "input_tokens_per_mille": input_cost_per_mille,
                "output_tokens_per_mille": output_cost_per_mille,
            },
            "execution": {
                "start_time": datetime.utcnow().isoformat() + "Z",  # Approximation
                "end_time": timestamp,
                "duration_sec": execution_time_sec,
                "status": status,
            },
            "tokens": {
                "input": tokens_in,
                "output": tokens_out,
                "total": total_tokens,
                "cost_usd": round(cost_usd, 4),
            },
            "artifact": {
                "filename": artifact_filename,
                "size_bytes": artifact_size,
                "line_count": artifact_lines,
                "section_count": artifact_sections,
                "references_entities": artifact_entities,
                "validation_passed": validation_passed,
            },
            "context": {
                "context_window_used_pct": context_window_used_pct,
                "auto_compactions": auto_compactions,
                "context_resets": context_resets,
            },
            "output": {
                "completion_reason": "end_turn" if status == "success" else "error",
                "stop_reason": error_message or "completed",
            },
        }

        # Remove None values for cleaner JSON
        event = self._clean_dict(event)

        # Save to JSONL file (one event per line)
        self._save_event(wave, event)

        logger.info(
            f"Logged {agent_id} execution in {wave} Gate {gate} "
            f"({tokens_in} tokens in, {tokens_out} out, ${cost_usd:.3f})"
        )

        return event

    def _save_event(self, wave: str, event: Dict[str, Any]) -> None:
        """Save event to JSONL file."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.telemetry_dir / f"{wave}_{today}.jsonl"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def _clean_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values recursively."""
        if isinstance(d, dict):
            return {k: self._clean_dict(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [self._clean_dict(i) for i in d]
        return d

    def read_wave_events(self, wave: str) -> list:
        """Read all events for a given wave."""
        events = []
        for log_file in self.telemetry_dir.glob(f"{wave}_*.jsonl"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    events.append(json.loads(line))
        return events

    def summarize_wave(self, wave: str) -> Dict[str, Any]:
        """Generate summary statistics for a wave."""
        events = self.read_wave_events(wave)
        if not events:
            return {"wave": wave, "event_count": 0}

        total_tokens = sum(e["tokens"]["total"] for e in events)
        total_cost = sum(e["tokens"].get("cost_usd", 0) for e in events)
        total_time = sum(e["execution"]["duration_sec"] for e in events)
        artifact_size = sum(e["artifact"]["size_bytes"] for e in events if e["artifact"]["size_bytes"])

        agents_used = set(e["agent_id"] for e in events)
        gates_covered = sorted(set(e["gate"] for e in events))

        return {
            "wave": wave,
            "event_count": len(events),
            "agents_used": list(agents_used),
            "gates_covered": gates_covered,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 2),
            "total_execution_time_sec": round(total_time, 2),
            "total_artifact_size_bytes": artifact_size,
            "avg_execution_time_sec": round(total_time / len(events), 2) if events else 0,
        }


# Global instance (can be customized)
collector = TelemetryCollector()


def log_execution(**kwargs) -> Dict[str, Any]:
    """Convenience function for logging."""
    return collector.log_execution(**kwargs)
