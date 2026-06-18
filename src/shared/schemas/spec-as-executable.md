# Spec-as-Executable Schema — DMF v3
# Purpose: Convert static specifications into machine-verifiable contracts
# Date: 2026-06-16

## Overview

Instead of specifications being documents that humans read but code doesn't enforce, we make them **executable assertions** that agents verify continuously.

Two-part model:
1. **Declarative Spec** (YAML): What are the requirements?
2. **Executable Validators** (Python): How do we verify?

---

## 1. DATA CONTRACT SCHEMA (Declarative)

```yaml
# projects/bradesco/specs/data-contracts.yaml

data_contracts:
  version: "1.0.0"
  
  contracts:
    - entity_name: "DIM_CUSTOMER"
      source: "PROD.dbo.CUSTOMER"
      target: "FABRIC.dimensions.DIM_CUSTOMER"
      
      # Business keys (unique identifier)
      business_keys:
        - "customer_id"
      
      # Columns: Schema contract
      columns:
        - name: "customer_id"
          data_type: "BIGINT"
          nullable: false
          description: "Primary key"
          pii: false
          
        - name: "customer_name"
          data_type: "NVARCHAR(255)"
          nullable: true
          description: "Full name"
          pii: true  # Personal data; encrypt
          
        - name: "email"
          data_type: "NVARCHAR(255)"
          nullable: true
          description: "Contact email"
          pii: true  # Personal data; encrypt
          
        - name: "created_date"
          data_type: "DATE"
          nullable: false
          description: "Record creation date"
          pii: false
      
      # Reconciliation: How to compare source ↔ target?
      reconciliation:
        method: "row_hash"  # or: "column_checksum" | "count_only"
        
        # Hash algorithm to compare rows
        hash_function: "MD5"  # or: "SHA256" | "SHA1"
        
        # Columns to include in hash (leave NULL = all)
        hash_columns: null  # [col1, col2] or null for all
        
        # Tolerances
        tolerances:
          row_count_variance_pct: 0.1  # Allow 0.1% difference
          hash_mismatch_pct: 0.01      # Allow 0.01% mismatched rows
          nulls_variance_pct: 1.0      # Allow 1% difference in NULL counts
      
      # Data quality rules (SLAs)
      quality_rules:
        - rule_id: "DQ_CUST_001"
          description: "No NULL customer_ids"
          assertion: "customer_id IS NOT NULL"
          severity: "critical"  # critical | high | medium | low
          
        - rule_id: "DQ_CUST_002"
          description: "customer_id > 0"
          assertion: "customer_id > 0"
          severity: "high"
          
        - rule_id: "DQ_CUST_003"
          description: "created_date <= TODAY"
          assertion: "created_date <= CAST(GETDATE() AS DATE)"
          severity: "medium"
      
      # Performance SLAs
      performance_sla:
        - metric: "row_count"
          expected_value: 5000000  # 5M rows
          tolerance_pct: 0.5
          
        - metric: "load_duration_sec"
          expected_value: 600  # 10 minutes
          tolerance_pct: 20
        
        - metric: "query_latency_p95_ms"
          query: "SELECT * FROM DIM_CUSTOMER WHERE customer_id = ?"
          expected_value: 100
          tolerance_pct: 10

    - entity_name: "FCT_TRANSACTION"
      source: "PROD.dbo.TRANSACTION"
      target: "FABRIC.facts.FCT_TRANSACTION"
      
      business_keys:
        - "transaction_id"
        - "source_system"
      
      columns:
        - name: "transaction_id"
          data_type: "BIGINT"
          nullable: false
        
        - name: "source_system"
          data_type: "NVARCHAR(50)"
          nullable: false
        
        - name: "customer_id"
          data_type: "BIGINT"
          nullable: false
          # Foreign key: must exist in DIM_CUSTOMER
          fk_contract: "DIM_CUSTOMER.customer_id"
        
        - name: "amount"
          data_type: "DECIMAL(18, 2)"
          nullable: false
        
        - name: "transaction_date"
          data_type: "DATE"
          nullable: false
      
      quality_rules:
        - rule_id: "DQ_TXN_001"
          description: "amount > 0"
          assertion: "amount > 0"
          severity: "critical"
        
        - rule_id: "DQ_TXN_002"
          description: "transaction_date <= TODAY"
          assertion: "transaction_date <= CAST(GETDATE() AS DATE)"
          severity: "high"
        
        - rule_id: "DQ_TXN_003"
          description: "Foreign key: customer_id exists in DIM_CUSTOMER"
          assertion: "customer_id IN (SELECT customer_id FROM DIM_CUSTOMER)"
          severity: "critical"
      
      reconciliation:
        method: "row_hash"
        tolerances:
          row_count_variance_pct: 0.05
          hash_mismatch_pct: 0.001
```

---

## 2. EXECUTABLE VALIDATORS (Python)

```python
# src/shared/scripts/data_contract_validator.py

from dataclasses import dataclass
from typing import Dict, List, Optional
import hashlib
import logging

@dataclass
class DataContractValidator:
    """
    Verifies that actual data matches the spec contract.
    Runs after deployment; blocks go-live if failures detected.
    """
    
    def __init__(self, contract_yaml: str, source_conn, target_conn):
        self.contract = yaml.safe_load(contract_yaml)
        self.source = source_conn
        self.target = target_conn
        self.results = []
    
    def validate_all(self) -> Dict:
        """Main entry point: validate entire spec."""
        for entity_contract in self.contract["data_contracts"]["contracts"]:
            self._validate_entity(entity_contract)
        
        return self._summarize_results()
    
    def _validate_entity(self, entity_contract: Dict) -> Dict:
        """Validate a single entity against its contract."""
        
        entity_name = entity_contract["entity_name"]
        logger.info(f"Validating {entity_name}")
        
        results = {
            "entity": entity_name,
            "checks": {
                "schema": self._validate_schema(entity_contract),
                "quality": self._validate_quality_rules(entity_contract),
                "reconciliation": self._validate_reconciliation(entity_contract),
                "performance": self._validate_performance_sla(entity_contract)
            }
        }
        
        # Aggregate score
        results["overall_score"] = self._aggregate_score(results["checks"])
        self.results.append(results)
        
        return results
    
    def _validate_schema(self, entity_contract: Dict) -> Dict:
        """
        Check: Target schema matches contract definition.
        - Column names, data types, nullability.
        """
        
        target_table = entity_contract["target"]
        columns_contract = entity_contract["columns"]
        
        # Query target schema
        target_schema = self.target.describe(target_table)
        
        checks = []
        for col_spec in columns_contract:
            col_name = col_spec["name"]
            col_target_type = target_schema.get(col_name, {}).get("type")
            col_contract_type = col_spec["data_type"]
            col_nullable = col_spec.get("nullable", True)
            col_target_nullable = target_schema.get(col_name, {}).get("nullable", True)
            
            check = {
                "column": col_name,
                "passed": (col_target_type == col_contract_type and 
                          col_target_nullable == col_nullable),
                "details": {
                    "expected_type": col_contract_type,
                    "actual_type": col_target_type,
                    "expected_nullable": col_nullable,
                    "actual_nullable": col_target_nullable
                }
            }
            checks.append(check)
        
        return {
            "checks": checks,
            "score": sum(1 for c in checks if c["passed"]) / len(checks)
        }
    
    def _validate_quality_rules(self, entity_contract: Dict) -> Dict:
        """
        Execute quality assertions.
        - Example: SELECT COUNT(*) FROM table WHERE amount <= 0
        """
        
        target_table = entity_contract["target"]
        quality_rules = entity_contract.get("quality_rules", [])
        
        checks = []
        for rule in quality_rules:
            rule_id = rule["rule_id"]
            assertion = rule["assertion"]
            severity = rule["severity"]
            
            # Build SQL: SELECT COUNT(*) FROM target WHERE NOT(assertion)
            sql = f"""
            SELECT COUNT(*) as violations
            FROM {target_table}
            WHERE NOT ({assertion})
            """
            
            result = self.target.execute(sql).fetchone()
            violations = result[0]
            
            passed = (violations == 0)
            
            check = {
                "rule_id": rule_id,
                "passed": passed,
                "violations": violations,
                "severity": severity,
                "assertion": assertion
            }
            checks.append(check)
            
            if not passed and severity == "critical":
                logger.error(f"CRITICAL: {rule_id} failed with {violations} violations")
        
        # Score: critical failures = 0, high = 0.25 penalty, etc.
        critical_failures = sum(1 for c in checks if not c["passed"] and c["severity"] == "critical")
        score = 0 if critical_failures > 0 else 0.95  # Simplified
        
        return {"checks": checks, "score": score}
    
    def _validate_reconciliation(self, entity_contract: Dict) -> Dict:
        """
        Compare source ↔ target row counts and hashes.
        - Tolerance: allow X% variance.
        """
        
        source_table = entity_contract["source"]
        target_table = entity_contract["target"]
        recon_spec = entity_contract["reconciliation"]
        
        # Row counts
        source_count = self.source.execute(f"SELECT COUNT(*) FROM {source_table}").fetchone()[0]
        target_count = self.target.execute(f"SELECT COUNT(*) FROM {target_table}").fetchone()[0]
        
        row_variance_pct = abs(source_count - target_count) / source_count * 100
        row_tolerance = recon_spec["tolerances"]["row_count_variance_pct"]
        
        row_check = {
            "metric": "row_count",
            "source": source_count,
            "target": target_count,
            "variance_pct": row_variance_pct,
            "tolerance_pct": row_tolerance,
            "passed": row_variance_pct <= row_tolerance
        }
        
        # Hash matching (if applicable)
        hash_check = None
        if recon_spec["method"] == "row_hash":
            hash_check = self._validate_row_hashes(
                source_table, target_table, recon_spec
            )
        
        checks = [row_check]
        if hash_check:
            checks.append(hash_check)
        
        score = (
            (1.0 if row_check["passed"] else 0.5) *
            (1.0 if (not hash_check or hash_check["passed"]) else 0.5)
        )
        
        return {"checks": checks, "score": score}
    
    def _validate_row_hashes(self, source_table, target_table, recon_spec) -> Dict:
        """Compare row-level hashes."""
        
        hash_function = recon_spec.get("hash_function", "MD5")
        tolerance = recon_spec["tolerances"]["hash_mismatch_pct"]
        
        # Simplified: count rows where hash differs
        sql_compare = f"""
        WITH source_hashes AS (
            SELECT 
                {hash_function}(CAST(ROW_NUMBER() OVER (ORDER BY *) AS VARCHAR)) as row_hash
            FROM {source_table}
        ),
        target_hashes AS (
            SELECT 
                {hash_function}(CAST(ROW_NUMBER() OVER (ORDER BY *) AS VARCHAR)) as row_hash
            FROM {target_table}
        )
        SELECT 
            COUNT(*) as hash_mismatches
        FROM (
            SELECT row_hash FROM source_hashes
            UNION ALL
            SELECT row_hash FROM target_hashes
        ) x
        GROUP BY row_hash
        HAVING COUNT(*) = 1
        """
        
        mismatches = self.target.execute(sql_compare).fetchone()[0]
        total = self.source.execute(f"SELECT COUNT(*) FROM {source_table}").fetchone()[0]
        mismatch_pct = (mismatches / total * 100) if total > 0 else 0
        
        return {
            "metric": "row_hash_match",
            "mismatches": mismatches,
            "total_rows": total,
            "mismatch_pct": mismatch_pct,
            "tolerance_pct": tolerance,
            "passed": mismatch_pct <= tolerance
        }
    
    def _validate_performance_sla(self, entity_contract: Dict) -> Dict:
        """Check performance metrics against SLAs."""
        
        target_table = entity_contract["target"]
        sla_specs = entity_contract.get("performance_sla", [])
        
        checks = []
        for sla in sla_specs:
            metric = sla["metric"]
            expected = sla["expected_value"]
            tolerance_pct = sla.get("tolerance_pct", 10)
            
            if metric == "row_count":
                actual = self.target.execute(f"SELECT COUNT(*) FROM {target_table}").fetchone()[0]
                variance = abs(actual - expected) / expected * 100
                passed = variance <= tolerance_pct
                
                check = {
                    "metric": metric,
                    "expected": expected,
                    "actual": actual,
                    "variance_pct": variance,
                    "tolerance_pct": tolerance_pct,
                    "passed": passed
                }
            
            elif metric == "load_duration_sec":
                # From observability traces
                duration = self._get_last_load_duration(target_table)
                variance = abs(duration - expected) / expected * 100
                passed = variance <= tolerance_pct
                
                check = {
                    "metric": metric,
                    "expected": expected,
                    "actual": duration,
                    "variance_pct": variance,
                    "tolerance_pct": tolerance_pct,
                    "passed": passed
                }
            
            checks.append(check)
        
        score = sum(1 for c in checks if c["passed"]) / len(checks) if checks else 1.0
        return {"checks": checks, "score": score}
    
    def _aggregate_score(self, checks: Dict) -> float:
        """
        Combine all check scores into one.
        Weights: schema(20%) | quality(30%) | reconciliation(30%) | performance(20%)
        """
        
        weights = {
            "schema": 0.20,
            "quality": 0.30,
            "reconciliation": 0.30,
            "performance": 0.20
        }
        
        total_score = sum(
            checks[key]["score"] * weights[key]
            for key in checks if key in weights
        )
        
        return total_score
    
    def _summarize_results(self) -> Dict:
        """Final report."""
        
        entity_scores = [r["overall_score"] for r in self.results]
        overall_score = sum(entity_scores) / len(entity_scores) if entity_scores else 0
        
        critical_failures = sum(
            len([c for c in r["checks"].get("quality", {}).get("checks", [])
                 if not c["passed"] and c["severity"] == "critical"])
            for r in self.results
        )
        
        return {
            "status": "passed" if overall_score >= 0.85 and critical_failures == 0 else "failed",
            "overall_score": overall_score,
            "entity_results": self.results,
            "critical_failures": critical_failures,
            "timestamp": datetime.utcnow().isoformat()
        }
```

---

## 3. INTEGRATION WITH GATE 3

```python
# src/shared/scripts/validate_gate3_artifacts.py (updated)

def validate_gate3_artifacts(wave_id: str, target_conn) -> GateScore:
    """
    Gate 3: Verify post-deployment data matches spec contracts.
    """
    
    # Load contracts from wave spec
    contract_yaml = load_spec(f"projects/{wave_id}/specs/data-contracts.yaml")
    source_conn = get_source_connection(wave_id)
    
    validator = DataContractValidator(
        contract_yaml=contract_yaml,
        source_conn=source_conn,
        target_conn=target_conn
    )
    
    validation_result = validator.validate_all()
    
    # Convert validation result → GateScore
    gate_score = GateScore(
        completude=0.95,  # If all entities pass
        qualidade=validation_result["overall_score"],
        risco_residual=0.05,  # No risks if reconciliation passes
        reconciliacao=validation_result["overall_score"]  # Key for Gate 3
    )
    
    # If critical_failures > 0, block deployment
    if validation_result["critical_failures"] > 0:
        raise GateBlockedException(
            gate=3,
            reason="Critical data quality failures detected",
            details=validation_result
        )
    
    return gate_score
```

---

## 4. BENEFIT: Spec-as-Code

Before (Document-Driven):
```
Spec document:
"The DIM_CUSTOMER table must not have NULL customer_ids"

Reality:
- Document is static; nobody re-reads it
- DQ rule forgotten in production
- Data quality fails; post-mortem shows "spec wasn't followed"
```

After (Executable Spec):
```
Spec YAML + Validator:
quality_rules:
  - rule_id: "DQ_CUST_001"
    assertion: "customer_id IS NOT NULL"
    severity: "critical"

Execution:
- Every deployment: validator runs
- If violated: gate blocks + alerts architect
- Enforcement is automatic; no human memory needed
```

---

## ADOPTION CHECKLIST

- [ ] Write data contracts YAML for all entities
- [ ] Implement `DataContractValidator` class
- [ ] Integrate into Gate 3 validators
- [ ] Test on sandbox with mock source/target
- [ ] Document SLA metrics per entity
- [ ] Train architects on spec authoring
- [ ] Add "Spec Review" to PR checklist for gates

---

**Related Docs:**
- `wave-config-extended.yaml` (Contains specifications section)
- `HUMAN-AGENT-CHECKPOINTS.md` (Escalation if validator fails)
