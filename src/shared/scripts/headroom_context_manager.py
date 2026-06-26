#!/usr/bin/env python3
"""
Headroom Context Manager
Integrates token compression into agent handoffs.

Tries the real Headroom engine (github.com/juliopessan/headroom, published as
`headroom-ai`) first. That engine's compression is implemented in a Rust
extension (`headroom._core`) which only ships prebuilt wheels for macOS and
Linux (manylinux) — there is no Windows build. On platforms without the
native core, this falls back to `real_compressor`: genuine, measured,
reversible compression (tiktoken counts + columnar JSON dedup), never a
fabricated ratio.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import model_pricing
import real_compressor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompressionStats:
    """Track compression metrics for a handoff."""
    source_agent: str
    target_agent: str
    input_tokens: int
    output_tokens: int
    compression_ratio: float
    tokens_saved: int
    latency_ms: float
    method: str  # "headroom-native" | "python-real-columnar" | "python-real-whitespace" | ...
    timestamp: str
    reversible: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class HeadroomContextManager:
    """
    Manage token compression for agent handoffs.

    Tries the real Headroom native engine first; falls back to real_compressor
    (genuine measured compression, no native dependency) when unavailable.
    """

    def __init__(self, project_root: str | None = None, use_mock: bool = False):
        """Initialize context manager.

        `use_mock` forces the real_compressor fallback even when the native
        Headroom engine is importable — useful for tests/CI determinism.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.use_mock = use_mock
        self.headroom_available = self._check_headroom()
        self.compression_stats: list[CompressionStats] = []

        if not self.headroom_available:
            logger.info(
                "ℹ️  Headroom native engine unavailable on this platform "
                "(no headroom._core build) — using real_compressor (%s).",
                real_compressor.tokenizer_method(),
            )
            self.use_mock = True

    def _check_headroom(self) -> bool:
        """Check if the real Headroom *native* engine is actually usable.

        Importing the `headroom` package alone is not sufficient: PyPI only
        publishes the compiled `_core` extension for macOS/Linux, so on
        Windows `import headroom` succeeds but compression silently no-ops.
        We require `headroom._core` to confirm the real engine will do
        anything.
        """
        if self.use_mock:
            return False

        try:
            import headroom  # noqa: F401
            import headroom._core  # noqa: F401
            logger.info("✅ Headroom native engine available (headroom._core)")
            return True
        except ImportError:
            logger.debug(
                "ℹ️  headroom._core not available (no Windows wheel published). "
                "real_compressor fallback enabled."
            )
            return False

    def compress_handoff(
        self,
        data: str | dict,
        source_agent: str,
        target_agent: str,
        model: str = "claude-haiku-4-5",
    ) -> tuple[str, CompressionStats]:
        """
        Compress data for handoff between agents.

        Args:
            data: Artifact data (JSON string or dict)
            source_agent: Name of agent producing data
            target_agent: Name of agent consuming data
            model: Model name, used for native Headroom's cache-alignment hints

        Returns:
            (compressed_data, stats) — all token counts in `stats` are measured,
            never derived from a guessed ratio.
        """
        start_time = datetime.now()

        if self.headroom_available and not self.use_mock:
            compressed, input_tokens, output_tokens, method = self._compress_real(data, model)
        else:
            outcome = real_compressor.compress_artifact(data)
            compressed = outcome.compressed_text
            input_tokens = outcome.input_tokens
            output_tokens = outcome.output_tokens
            method = outcome.method

        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        tokens_saved = input_tokens - output_tokens
        ratio = (tokens_saved / input_tokens) if input_tokens > 0 else 0.0

        stats = CompressionStats(
            source_agent=source_agent,
            target_agent=target_agent,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            compression_ratio=ratio,
            tokens_saved=tokens_saved,
            latency_ms=elapsed_ms,
            method=method,
            timestamp=datetime.now().isoformat(),
        )

        self.compression_stats.append(stats)

        logger.info(
            f"📦 Handoff {source_agent} → {target_agent}: "
            f"{input_tokens:,} → {output_tokens:,} tokens ({ratio*100:.1f}% measured, method={method})"
        )

        return compressed, stats

    def _compress_real(self, data: str | dict, model: str) -> tuple[str, int, int, str]:
        """Compress using the real Headroom native engine (headroom._core)."""
        try:
            from headroom import compress, CompressConfig

            content = json.dumps(data, indent=2, default=str) if isinstance(data, dict) else str(data)
            messages = [{"role": "user", "content": content}]
            config = CompressConfig(kompress_model="disabled", protect_recent=0, compress_user_messages=True)
            result = compress(messages, model=model, config=config)

            compressed_content = result.messages[0]["content"] if result.messages else content
            return compressed_content, result.tokens_before, result.tokens_after, "headroom-native"
        except Exception as exc:
            logger.warning("Real Headroom engine failed (%s). Falling back to real_compressor.", exc)
            outcome = real_compressor.compress_artifact(data)
            return outcome.compressed_text, outcome.input_tokens, outcome.output_tokens, outcome.method

    def retrieve_if_needed(self, data: str) -> str:
        """
        Reverse a real_compressor columnar transform back to its original shape.
        No-op for whitespace-only or native-engine output (already plain text/JSON).
        """
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
        return json.dumps(real_compressor.expand_columnar(parsed), indent=2)

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated compression statistics."""
        if not self.compression_stats:
            return {"message": "No compressions yet"}
        
        total_input = sum(s.input_tokens for s in self.compression_stats)
        total_output = sum(s.output_tokens for s in self.compression_stats)
        total_saved = sum(s.tokens_saved for s in self.compression_stats)
        avg_ratio = sum(s.compression_ratio for s in self.compression_stats) / len(
            self.compression_stats
        )
        
        # Real per-model pricing (model_pricing.py), applied to real measured tokens.
        cost_saved = model_pricing.estimate_cost_usd(total_saved, 0)

        return {
            "total_handoffs": len(self.compression_stats),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens_saved": total_saved,
            "avg_compression_ratio": avg_ratio,
            "cost_saved_usd": round(cost_saved, 6),
            "method": "headroom-native" if self.headroom_available else real_compressor.tokenizer_method(),
            "by_agent": self._stats_by_agent(),
            "timeline": [s.to_dict() for s in self.compression_stats[-10:]],  # Last 10
        }

    def _stats_by_agent(self) -> Dict[str, Dict[str, Any]]:
        """Aggregate stats by agent pair."""
        by_pair = {}
        for stat in self.compression_stats:
            key = f"{stat.source_agent} → {stat.target_agent}"
            if key not in by_pair:
                by_pair[key] = {
                    "count": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "tokens_saved": 0,
                }
            by_pair[key]["count"] += 1
            by_pair[key]["input_tokens"] += stat.input_tokens
            by_pair[key]["output_tokens"] += stat.output_tokens
            by_pair[key]["tokens_saved"] += stat.tokens_saved
        
        return by_pair

    def save_stats(self, output_file: str | Path):
        """Save compression stats to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        stats = self.get_stats()
        output_path.write_text(json.dumps(stats, indent=2))
        logger.info(f"💾 Stats saved to {output_path}")


# Module initialization
if __name__ == "__main__":
    import sys as _sys

    if hasattr(_sys.stdout, "reconfigure"):
        _sys.stdout.reconfigure(encoding="utf-8")

    # Example usage
    manager = HeadroomContextManager(use_mock=True)
    
    test_data = {
        "table": "large_fact_table",
        "columns": [f"col_{i}" for i in range(100)],
        "rows": 10_000_000,
    }
    
    compressed, stats = manager.compress_handoff(
        test_data,
        source_agent="discovery-scout",
        target_agent="data-architect",
    )
    
    print(f"✅ Compression: {stats.compression_ratio*100:.1f}%")
    print(f"   Saved: {stats.tokens_saved:,} tokens")
    print(f"\nStats:\n{json.dumps(manager.get_stats(), indent=2)}")
