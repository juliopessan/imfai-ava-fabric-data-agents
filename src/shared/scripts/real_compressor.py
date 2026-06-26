"""
Real Compressor — genuine, measured token reduction with no external native
dependency.

Exists because the real `headroom-ai` package (github.com/juliopessan/headroom)
only ships its Rust-accelerated compression core (`headroom._core`) for macOS
and Linux (manylinux). There is no Windows wheel, so on Windows the real
compression engine is unavailable and must not be silently faked.

This module replaces the old `_compress_mock()` heuristic (which guessed a
compression ratio from a fixed lookup table keyed off string sniffing, with
zero relationship to what was actually sent). Everything here is measured:
token counts come from a real tokenizer, and the ratio reported is the actual
before/after delta of a real, lossless, reversible transform — never a guess.

Transform applied:
1. Columnar dedup of uniform list[dict] structures (the same idea as
   Headroom's SmartCrusher): repeated key strings across N rows are hoisted
   once instead of repeated N times. Lossless and reversible via
   `expand_columnar`.
2. Compact (no-whitespace) JSON serialization instead of indent=2.

For non-JSON text (markdown, SQL, logs), only whitespace normalization is
applied — real but modest, which is the honest answer for unstructured text.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

_COLUMNAR_MARKER = "__columnar__"

_encoding = None
_tiktoken_available: bool | None = None


def _get_encoding():
    """Lazy singleton tiktoken encoding. Falls back to a word-based counter."""
    global _encoding, _tiktoken_available
    if _tiktoken_available is not None:
        return _encoding

    try:
        import tiktoken

        _encoding = tiktoken.get_encoding("cl100k_base")
        _tiktoken_available = True
        logger.debug("real_compressor: using tiktoken cl100k_base for token counts")
    except Exception as exc:  # pragma: no cover - exercised only without tiktoken
        _encoding = None
        _tiktoken_available = False
        logger.warning(
            "real_compressor: tiktoken unavailable (%s). Falling back to a "
            "whitespace-split token estimate — counts will be approximate.",
            exc,
        )
    return _encoding


def count_tokens(text: str) -> int:
    """Real token count. Uses tiktoken when available; otherwise a labeled approximation."""
    if not text:
        return 0
    encoding = _get_encoding()
    if encoding is not None:
        return len(encoding.encode(text))
    # Documented approximation, not a silent character-count guess.
    return len(re.findall(r"\S+", text))


def tokenizer_method() -> str:
    """Which counting strategy is actually active right now."""
    _get_encoding()
    return "tiktoken-cl100k_base" if _tiktoken_available else "whitespace-approx"


def _is_uniform_dict_list(value: Any) -> bool:
    if not isinstance(value, list) or len(value) < 2:
        return False
    if not all(isinstance(item, dict) for item in value):
        return False
    first_keys = list(value[0].keys())
    return all(list(item.keys()) == first_keys for item in value)


def _columnar_dedup(obj: Any) -> Any:
    """Recursively hoist repeated dict keys out of uniform list[dict] arrays."""
    if isinstance(obj, dict):
        return {key: _columnar_dedup(val) for key, val in obj.items()}
    if isinstance(obj, list):
        if _is_uniform_dict_list(obj):
            keys = list(obj[0].keys())
            return {
                _COLUMNAR_MARKER: True,
                "keys": keys,
                "rows": [[_columnar_dedup(item[k]) for k in keys] for item in obj],
            }
        return [_columnar_dedup(item) for item in obj]
    return obj


def expand_columnar(obj: Any) -> Any:
    """Reverse of `_columnar_dedup` — restores the original list[dict] shape."""
    if isinstance(obj, dict):
        if obj.get(_COLUMNAR_MARKER):
            keys = obj["keys"]
            return [dict(zip(keys, row)) for row in obj["rows"]]
        return {key: expand_columnar(val) for key, val in obj.items()}
    if isinstance(obj, list):
        return [expand_columnar(item) for item in obj]
    return obj


def _normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@dataclass
class CompressionOutcome:
    compressed_text: str
    input_tokens: int
    output_tokens: int
    tokens_saved: int
    compression_ratio: float
    method: str
    reversible: bool


def compress_artifact(data: str | dict, *, min_tokens_to_compress: int = 50) -> CompressionOutcome:
    """Apply real, measured, reversible compression to a handoff artifact."""
    if isinstance(data, dict):
        before_text = json.dumps(data, indent=2, default=str)
        input_tokens = count_tokens(before_text)

        if input_tokens < min_tokens_to_compress:
            return CompressionOutcome(
                compressed_text=before_text,
                input_tokens=input_tokens,
                output_tokens=input_tokens,
                tokens_saved=0,
                compression_ratio=0.0,
                method="python-real-skipped-too-small",
                reversible=True,
            )

        deduped = _columnar_dedup(data)
        after_text = json.dumps(deduped, separators=(",", ":"), default=str)
        output_tokens = count_tokens(after_text)
        method = "python-real-columnar"
    else:
        before_text = str(data)
        input_tokens = count_tokens(before_text)

        if input_tokens < min_tokens_to_compress:
            return CompressionOutcome(
                compressed_text=before_text,
                input_tokens=input_tokens,
                output_tokens=input_tokens,
                tokens_saved=0,
                compression_ratio=0.0,
                method="python-real-skipped-too-small",
                reversible=True,
            )

        after_text = _normalize_whitespace(before_text)
        output_tokens = count_tokens(after_text)
        method = "python-real-whitespace"

    # Never report a "saving" that didn't actually happen.
    output_tokens = min(output_tokens, input_tokens)
    tokens_saved = input_tokens - output_tokens
    ratio = (tokens_saved / input_tokens) if input_tokens > 0 else 0.0

    return CompressionOutcome(
        compressed_text=after_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        tokens_saved=tokens_saved,
        compression_ratio=ratio,
        method=method,
        reversible=method != "python-real-whitespace",
    )
