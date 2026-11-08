#!/usr/bin/env python3
"""
Headroom Context Manager
Integrates token compression into agent handoffs using Headroom.
Part of DMF Phase 1 implementation (starting 2026-06-22).

Engine selection:
1. Headroom (``headroom`` package) when it is importable and ``use_mock`` is False.
2. Project fallback compressor (``_compress_mock``) otherwise, or when Headroom
   fails at call time.

Token counts and ratios are measured on the real input/output text
(1 token ≈ 4 characters), not taken from heuristic estimates.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import sys

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
    method: str  # "headroom" or "mock" (project fallback compressor)
    timestamp: str
    reversible: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class HeadroomContextManager:
    """
    Manage token compression for agent handoffs.
    
    Falls back gracefully to the project compressor if real Headroom is unavailable.
    Implements: Try Headroom → project compressor fallback
    """
    
    def __init__(self, project_root: str | None = None, use_mock: bool = False):
        """Initialize context manager."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.use_mock = use_mock
        self.headroom_available = self._check_headroom()
        self.compression_stats: list[CompressionStats] = []
        
        if not self.headroom_available:
            logger.warning("⚠️  Headroom not available. Using project fallback compressor.")
            self.use_mock = True

    def _check_headroom(self) -> bool:
        """Check if real Headroom is available."""
        if self.use_mock:
            return False
        
        try:
            import headroom  # noqa: F401
            logger.info("✅ Headroom library available")
            return True
        except ImportError:
            logger.debug("ℹ️  Headroom not installed. Fallback compressor enabled.")
            return False

    def compress_handoff(
        self,
        data: str | dict,
        source_agent: str,
        target_agent: str,
        model: str = "gpt-4o",
    ) -> tuple[str, CompressionStats]:
        """
        Compress data for handoff between agents.
        
        Args:
            data: Artifact data (JSON string or dict)
            source_agent: Name of agent producing data
            target_agent: Name of agent consuming data
            model: LLM model for compression hints
            
        Returns:
            (compressed_data, stats)
        """
        # Convert dict to JSON string if needed
        if isinstance(data, dict):
            data_str = json.dumps(data, indent=2)
        else:
            data_str = data

        input_tokens = self._estimate_tokens(data_str)
        
        start_time = datetime.now()
        
        if self.headroom_available and not self.use_mock:
            compressed, method = self._compress_real(data_str, model)
        else:
            compressed, method = self._compress_mock(data_str, model), "mock"
        
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Measured on the actual output, not on a heuristic estimate.
        output_tokens = self._estimate_tokens(compressed)
        tokens_saved = input_tokens - output_tokens
        ratio = tokens_saved / input_tokens
        
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
            reversible=method == "headroom",
        )
        
        self.compression_stats.append(stats)
        
        logger.info(
            f"📦 Handoff {source_agent} → {target_agent} [{method}]: "
            f"{input_tokens:,} → {output_tokens:,} tokens ({ratio*100:.1f}% compression)"
        )
        
        return compressed, stats

    def _compress_real(self, data: str, model: str) -> tuple[str, str]:
        """
        Compress using real Headroom library.

        Returns (compressed, method). Any Headroom failure (missing API,
        exception, unusable result) falls back to the project compressor.
        """
        try:
            from headroom import compress, Configuration
            
            config = Configuration(model=model)
            result = compress(data, config=config)
            return self._extract_text(result), "headroom"
        except Exception as e:
            logger.warning(f"Real Headroom failed: {e}. Falling back to project compressor.")
            return self._compress_mock(data, model), "mock"

    @staticmethod
    def _extract_text(result: Any) -> str:
        """Get the compressed text from a Headroom result."""
        if isinstance(result, str):
            return result
        if isinstance(result, dict) and isinstance(result.get("content"), str):
            return result["content"]
        content = getattr(result, "content", None)
        if isinstance(content, str):
            return content
        raise TypeError(f"Unsupported Headroom result type: {type(result).__name__}")

    def _compress_mock(self, data: str, model: str) -> str:
        """
        Project fallback compressor (no external dependency).

        Deterministic and content-preserving:
        - valid JSON: re-serialised without indentation or extra whitespace
        - anything else: trailing whitespace and repeated blank lines removed
        """
        try:
            return json.dumps(json.loads(data), separators=(",", ":"), ensure_ascii=False)
        except (ValueError, TypeError):
            pass

        out: list[str] = []
        for line in data.splitlines():
            line = line.rstrip()
            if not line and (not out or not out[-1]):
                continue
            out.append(line)
        return "\n".join(out).strip("\n")

    def retrieve_if_needed(self, data: str, retrieval_id: str) -> str:
        """
        Retrieve original data if compression used reversible CCR.
        
        For now, returns data as-is (neither engine keeps an original store yet).
        Real Headroom would call CCR retriever here.
        """
        return data

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
        
        # Calculate cost savings (rough estimate)
        # ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
        input_cost = (total_input / 1_000_000) * 0.075
        output_cost = (total_output / 1_000_000) * 0.30
        total_cost = input_cost + output_cost
        
        # With compression
        output_cost_compressed = (total_output / 1_000_000) * 0.30
        total_cost_compressed = input_cost + output_cost_compressed
        
        cost_saved = total_cost - total_cost_compressed
        
        return {
            "total_handoffs": len(self.compression_stats),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens_saved": total_saved,
            "avg_compression_ratio": avg_ratio,
            "cost_saved_usd": round(cost_saved, 6),
            "method": "headroom" if self.headroom_available else "mock",
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

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation: 1 token ≈ 4 characters."""
        return max(1, len(text) // 4)

    def save_stats(self, output_file: str | Path):
        """Save compression stats to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        stats = self.get_stats()
        output_path.write_text(json.dumps(stats, indent=2))
        logger.info(f"💾 Stats saved to {output_path}")


# Module initialization
if __name__ == "__main__":
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
