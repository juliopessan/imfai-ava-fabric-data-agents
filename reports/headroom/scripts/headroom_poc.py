#!/usr/bin/env python3
"""
Headroom PoC — Token Compression Validation

Quick proof-of-concept to validate Headroom token reduction on real DMF artifacts.

Usage:
    python headroom_poc.py --input <json-file> --agent <agent-name> [--output <file>]

Example:
    python headroom_poc.py \\
        --input projects/Financeiro/outputs/midstream/architecture.json \\
        --agent data-architect \\
        --output reports/headroom-poc-results.json
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Try to import headroom; provide helpful message if missing
try:
    from headroom import compress
    HEADROOM_INSTALLED = True
except ImportError:
    HEADROOM_INSTALLED = False
    print("⚠️  Headroom not installed. Install with: pip install headroom-ai")


def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON artifact file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON: {filepath}")
        sys.exit(1)


def mock_compress_fallback(data: Dict[str, Any], model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Fallback compression simulator (if Headroom not installed).
    Estimates token savings based on data type.
    """
    data_str = json.dumps(data, indent=2)
    estimated_input_tokens = len(data_str) // 4  # Rough estimate
    
    # Estimate compression ratio based on data structure
    if isinstance(data, dict):
        if "schema" in data or "tables" in data:
            ratio = 0.65  # Schema data: ~65% compression
        elif "queries" in data or "sql" in data:
            ratio = 0.45  # SQL: ~45% compression
        elif "logs" in data or "errors" in data:
            ratio = 0.15  # Logs: ~85% compression
        else:
            ratio = 0.50  # Default: 50% compression
    else:
        ratio = 0.50
    
    estimated_output_tokens = int(estimated_input_tokens * ratio)
    tokens_saved = estimated_input_tokens - estimated_output_tokens
    compression_ratio = tokens_saved / estimated_input_tokens if estimated_input_tokens > 0 else 0
    
    return {
        "tokensSaved": tokens_saved,
        "inputTokens": estimated_input_tokens,
        "outputTokens": estimated_output_tokens,
        "compressionRatio": compression_ratio,
        "method": "MOCK_ESTIMATE (Headroom not installed)",
        "warning": "⚠️  This is an estimate. Install Headroom for real compression: pip install headroom-ai"
    }


def compress_artifact(data: Dict[str, Any], agent: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """Compress artifact using Headroom (or fallback)."""
    
    if not HEADROOM_INSTALLED:
        print("📊 Using mock compression estimator (install Headroom for real results)")
        return mock_compress_fallback(data, model)
    
    try:
        # Attempt real Headroom compression
        messages = [
            {"role": "user", "content": json.dumps(data, indent=2)[:5000]}  # Limit content
        ]
        
        result = compress(messages, model=model)
        
        return {
            "tokensSaved": result.get("tokensSaved", 0),
            "inputTokens": result.get("inputTokens", 0),
            "outputTokens": result.get("outputTokens", 0),
            "compressionRatio": result.get("compressionRatio", 0),
            "method": "HEADROOM",
        }
    
    except Exception as e:
        print(f"⚠️  Headroom compression failed: {e}")
        print("   Falling back to mock estimate...")
        return mock_compress_fallback(data, model)


def calculate_cost_savings(tokens_saved: int, cost_per_mtok: float = 0.0015) -> float:
    """Calculate USD savings from token reduction."""
    mtokens = tokens_saved / 1_000_000
    return mtokens * cost_per_mtok


def format_report(
    agent: str,
    input_file: str,
    compression_result: Dict[str, Any],
    annualized: bool = False
) -> str:
    """Format compression results as readable report."""
    
    tokens_saved = compression_result.get("tokensSaved", 0)
    input_tokens = compression_result.get("inputTokens", 0)
    output_tokens = compression_result.get("outputTokens", 0)
    ratio = compression_result.get("compressionRatio", 0)
    method = compression_result.get("method", "unknown")
    
    usd_saved = calculate_cost_savings(tokens_saved)
    
    # Annualize for monthly usage pattern (Financeiro ~18K tokens/month)
    if annualized:
        monthly_tokens = input_tokens
        annual_tokens = monthly_tokens * 12
        annual_savings = annual_tokens * ratio / 1_000_000 * 0.0015
    else:
        annual_savings = None
    
    report = f"""
╔════════════════════════════════════════════════════════════════╗
║           HEADROOM TOKEN COMPRESSION PoC RESULTS               ║
╚════════════════════════════════════════════════════════════════╝

📋 Input Information
  Agent         : {agent}
  File          : {input_file}
  Method        : {method}
  Timestamp     : {datetime.now().isoformat()}

📊 Token Metrics
  Input Tokens  : {input_tokens:,}
  Output Tokens : {output_tokens:,}
  Tokens Saved  : {tokens_saved:,}
  Compression   : {ratio*100:.1f}%

💰 Cost Analysis
  Cost Saved    : ${usd_saved:.3f} USD (single handoff)
"""
    
    if annual_savings is not None:
        report += f"""  Annual (est.)  : ${annual_savings:.2f} USD
              (assuming {input_tokens:,} tokens/month pattern)
"""
    
    if "warning" in compression_result:
        report += f"\n⚠️  {compression_result['warning']}\n"
    
    report += """
✅ Next Steps
  1. If compression > 50%  → GO with full integration
  2. If compression < 30%  → NO-GO (not worth overhead)
  3. If 30-50%             → Evaluate on real workload

  Full strategy: reports/HEADROOM-INTEGRATION-STRATEGY.md
  Documentation: https://headroom-docs.vercel.app/docs/quickstart

╚════════════════════════════════════════════════════════════════╝
"""
    
    return report


def save_results(results: Dict[str, Any], output_file: Optional[str] = None):
    """Save results to JSON file."""
    if not output_file:
        return
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"✅ Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Headroom PoC — Validate token compression on DMF artifacts"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON artifact file (e.g., architecture.json)"
    )
    parser.add_argument(
        "--agent",
        required=True,
        help="Agent name for context (e.g., data-architect)"
    )
    parser.add_argument(
        "--output",
        help="Optional: Save results to JSON file"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "--annualize",
        action="store_true",
        help="Annualize cost savings (assumes 18K tokens/month pattern)"
    )
    
    args = parser.parse_args()
    
    # Load artifact
    print(f"📂 Loading artifact from: {args.input}")
    artifact_data = load_json_file(args.input)
    print(f"✅ Loaded {len(json.dumps(artifact_data))//1000}K artifact")
    
    # Compress
    print(f"🔄 Compressing for agent: {args.agent}")
    compression_result = compress_artifact(artifact_data, args.agent, args.model)
    print("✅ Compression complete")
    
    # Display report
    report = format_report(args.agent, args.input, compression_result, args.annualize)
    print(report)
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "input_file": args.input,
        "agent": args.agent,
        "model": args.model,
        "compression": compression_result,
        "cost_savings_usd": calculate_cost_savings(compression_result.get("tokensSaved", 0)),
    }
    save_results(results, args.output)


if __name__ == "__main__":
    main()
