#!/usr/bin/env python3
"""
Financeiro TIER 1 Validation Runner

Executes all TIER 1 validators against Financeiro project and generates comprehensive report.
Usage: python run_Financeiro_tier1_validation.py [--output-dir reports/Financeiro/]
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.shared.scripts.validate_wave_config import WaveConfigValidator
from src.shared.scripts.validate_gate1_artifacts import Gate1ArtifactsValidator
from src.shared.scripts.validate_gate2_artifacts import Gate2ArtifactsValidator
from src.shared.scripts.validate_gate3_artifacts import Gate3ArtifactsValidator
from src.shared.scripts.gate_score_report import GateScoreCalculator


def run_validation() -> Dict[str, Any]:
    """Execute all TIER 1 validations against Financeiro project."""
    
    project_path = Path("projects/Financeiro")
    results = {
        "timestamp": datetime.now().isoformat(),
        "project": "Financeiro",
        "status": "pending",
        "validations": {}
    }
    
    # Step 1: Wave Config Validation
    print("=" * 80)
    print("STEP 1: Wave Config Validation")
    print("=" * 80)
    
    wave_config_path = project_path / "wave-config.yaml"
    if not wave_config_path.exists():
        print(f"[ERROR] wave-config.yaml not found at {wave_config_path}")
        results["validations"]["wave_config"] = {
            "status": "ERROR",
            "message": "wave-config.yaml not found"
        }
    else:
        try:
            wave_validator = WaveConfigValidator(str(wave_config_path))
            wave_result = wave_validator.validate()
            results["validations"]["wave_config"] = {
                "status": "valid" if wave_result.valid else "invalid",
                "score": wave_result.score,
                "errors": wave_result.errors,
                "warnings": wave_result.warnings
            }
            print(f"[OK] Wave Config Validation: score={wave_result.score:.2f}, valid={wave_result.valid}")
            if wave_result.errors:
                for err in wave_result.errors:
                    print(f"   [ERROR] {err}")
            if wave_result.warnings:
                for warn in wave_result.warnings:
                    print(f"   [WARNING] {warn}")
        except Exception as e:
            print(f"[ERROR] Error during wave config validation: {e}")
            results["validations"]["wave_config"] = {
                "status": "ERROR",
                "message": str(e)
            }
            return results
    
    # Extract wave_id for gate validations
    try:
        import yaml
        with open(wave_config_path) as f:
            wave_config = yaml.safe_load(f)
        wave_id = wave_config.get("wave_id", "unknown")
    except Exception as e:
        print(f"❌ Could not extract wave_id: {e}")
        wave_id = "unknown"
    
    # Step 2: Gate 1 Validation
    print("\n" + "=" * 80)
    print("STEP 2: Gate 1 (Upstream) Validation")
    print("=" * 80)
    
    gate1_path = project_path / "outputs" / "upstream"
    if not gate1_path.exists():
        print(f"[ERROR] Gate 1 directory not found at {gate1_path}")
        results["validations"]["gate_1"] = {
            "status": "ERROR",
            "message": f"Directory not found: {gate1_path}"
        }
    else:
        try:
            gate1_validator = Gate1ArtifactsValidator(str(gate1_path))
            gate1_result = gate1_validator.validate()
            results["validations"]["gate_1"] = {
                "status": "valid" if gate1_result.valid else "invalid",
                "completude": gate1_result.completude,
                "quality": gate1_result.quality,
                "errors": gate1_result.errors,
                "warnings": gate1_result.warnings,
                "artifacts_found": gate1_result.artifacts_found,
                "artifacts_missing": gate1_result.artifacts_missing
            }
            print(f"[OK] Gate 1 Validation: valid={gate1_result.valid}")
            print(f"   Completude: {gate1_result.completude:.1%} ({len(gate1_result.artifacts_found)} artifacts found)")
            print(f"   Quality: {gate1_result.quality:.2f}")
            if gate1_result.artifacts_missing:
                print(f"   Missing artifacts: {', '.join(gate1_result.artifacts_missing)}")
            for err in gate1_result.errors:
                print(f"   [ERROR] {err}")
            for warn in gate1_result.warnings:
                print(f"   [WARNING] {warn}")
        except Exception as e:
            print(f"[ERROR] Error during Gate 1 validation: {e}")
            results["validations"]["gate_1"] = {
                "status": "ERROR",
                "message": str(e)
            }
    
    # Step 3: Gate 2 Validation
    print("\n" + "=" * 80)
    print("STEP 3: Gate 2 (Midstream) Validation")
    print("=" * 80)
    
    gate2_path = project_path / "outputs" / "midstream"
    if not gate2_path.exists():
        print(f"[ERROR] Gate 2 directory not found at {gate2_path}")
        results["validations"]["gate_2"] = {
            "status": "ERROR",
            "message": f"Directory not found: {gate2_path}"
        }
    else:
        try:
            gate2_validator = Gate2ArtifactsValidator(str(gate2_path))
            gate2_result = gate2_validator.validate()
            results["validations"]["gate_2"] = {
                "status": "valid" if gate2_result.valid else "invalid",
                "completude": gate2_result.completude,
                "quality": gate2_result.quality,
                "errors": gate2_result.errors,
                "warnings": gate2_result.warnings,
                "artifacts_found": gate2_result.artifacts_found,
                "artifacts_missing": gate2_result.artifacts_missing
            }
            print(f"[OK] Gate 2 Validation: valid={gate2_result.valid}")
            print(f"   Completude: {gate2_result.completude:.1%} ({len(gate2_result.artifacts_found)} artifacts found)")
            print(f"   Quality: {gate2_result.quality:.2f}")
            if gate2_result.artifacts_missing:
                print(f"   Missing artifacts: {', '.join(gate2_result.artifacts_missing)}")
            for err in gate2_result.errors:
                print(f"   [ERROR] {err}")
            for warn in gate2_result.warnings:
                print(f"   [WARNING] {warn}")
        except Exception as e:
            print(f"[ERROR] Error during Gate 2 validation: {e}")
            results["validations"]["gate_2"] = {
                "status": "ERROR",
                "message": str(e)
            }
    
    # Step 4: Gate 3 Validation (CRITICAL)
    print("\n" + "=" * 80)
    print("STEP 4: Gate 3 (Downstream) Validation - CRITICAL")
    print("=" * 80)
    
    gate3_path = project_path / "outputs" / "downstream"
    if not gate3_path.exists():
        print(f"[ERROR] Gate 3 directory not found at {gate3_path}")
        results["validations"]["gate_3"] = {
            "status": "ERROR",
            "message": f"Directory not found: {gate3_path}"
        }
    else:
        try:
            gate3_validator = Gate3ArtifactsValidator(str(gate3_path))
            gate3_result = gate3_validator.validate()
            results["validations"]["gate_3"] = {
                "status": "valid" if gate3_result.valid else "invalid",
                "completude": gate3_result.completude,
                "quality": gate3_result.quality,
                "reconciliation": gate3_result.reconciliation,
                "errors": gate3_result.errors,
                "warnings": gate3_result.warnings,
                "artifacts_found": gate3_result.artifacts_found,
                "artifacts_missing": gate3_result.artifacts_missing
            }
            print(f"[OK] Gate 3 Validation: valid={gate3_result.valid}")
            print(f"   Completude: {gate3_result.completude:.1%}")
            print(f"   Quality: {gate3_result.quality:.2f}")
            print(f"   Reconciliation (CRITICAL): {gate3_result.reconciliation:.2f} {'[PASSED]' if gate3_result.reconciliation >= 0.95 else '[FAILED]'}")
            for err in gate3_result.errors:
                print(f"   [ERROR] {err}")
            for warn in gate3_result.warnings:
                print(f"   [WARNING] {warn}")
        except Exception as e:
            print(f"[ERROR] Error during Gate 3 validation: {e}")
            results["validations"]["gate_3"] = {
                "status": "ERROR",
                "message": str(e)
            }
    
    # Step 5: GateScore Calculation (if all gates present)
    print("\n" + "=" * 80)
    print("STEP 5: GateScore Calculation")
    print("=" * 80)
    
    if all(k in results["validations"] and results["validations"][k].get("status") != "ERROR" 
           for k in ["gate_1", "gate_2", "gate_3"]):
        try:
            # Calculate individual gate scores
            gates_scores = {}
            for gate_num in [1, 2, 3]:
                gate_key = f"gate_{gate_num}"
                gate_data = results["validations"][gate_key]
                
                # For Gate 3, reconciliation is critical
                reconciliation = gate_data.get("reconciliation", 1.0) if gate_num == 3 else 1.0
                
                calculator = GateScoreCalculator(gate_number=gate_num, wave_id=wave_id)
                score_result = calculator.calculate(
                    completude=gate_data["completude"],
                    quality=gate_data["quality"],
                    residual_risk=0.1,  # Default assumption
                    reconciliation=reconciliation
                )
                
                gates_scores[gate_key] = {
                    "score": score_result.score,
                    "status": score_result.status,
                    "recommendations": score_result.recommendations
                }
                
                status_icon = {"approved": "[OK]", "conditional": "[INFO]", "blocked": "[FAIL]"}.get(score_result.status, "[?]")
                print(f"\n{status_icon} Gate {gate_num} GateScore: {score_result.score:.2f} ({score_result.status.upper()})")
                for rec in score_result.recommendations[:3]:  # Top 3 recommendations
                    print(f"   • {rec}")
            
            results["gate_scores"] = gates_scores
            
            # Overall status
            statuses = [s["status"] for s in gates_scores.values()]
            if all(s == "approved" for s in statuses):
                results["overall_status"] = "[OK] ALL GATES APPROVED"
            elif any(s == "blocked" for s in statuses):
                results["overall_status"] = "[FAIL] ONE OR MORE GATES BLOCKED"
            else:
                results["overall_status"] = "[INFO] CONDITIONAL APPROVAL"
            
        except Exception as e:
            print(f"[ERROR] Error during GateScore calculation: {e}")
            results["gate_scores"] = {"error": str(e)}
    
    results["status"] = "complete"
    return results


def main():
    """Main entry point."""
    print("\n" + "[Financeiro TIER 1 VALIDATION RUNNER]" + "\n")
    
    # Run validation
    results = run_validation()
    
    # Print summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Status: {results.get('overall_status', 'Unknown')}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Project: {results['project']}")
    
    # Save results to JSON
    output_path = Path("reports/Financeiro/tier1-validation-results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return 0 if results["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
