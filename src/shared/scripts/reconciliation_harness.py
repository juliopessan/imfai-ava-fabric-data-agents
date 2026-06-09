"""
Reconciliation Harness — Orchestrates Gate 3 reconciliation validation checks.
Validates: row count parity, schema completeness, data quality thresholds.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import json


class ReconciliationType(Enum):
    """Reconciliation check types."""
    ROW_COUNT = "row_count"
    SCHEMA = "schema"
    DATA_QUALITY = "data_quality"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"


class ReconciliationStatus(Enum):
    """Status of reconciliation check."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    NOT_RUN = "not_run"


@dataclass
class ReconciliationCheck:
    """Single reconciliation check result."""
    check_type: ReconciliationType
    entity_name: str
    source_count: int
    target_count: int
    threshold: float  # 0.00 to 1.00
    status: ReconciliationStatus
    variance_pct: float
    message: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "check_type": self.check_type.value,
            "entity_name": self.entity_name,
            "source_count": self.source_count,
            "target_count": self.target_count,
            "threshold": self.threshold,
            "status": self.status.value,
            "variance_pct": round(self.variance_pct, 2),
            "message": self.message,
            "timestamp": self.timestamp
        }


@dataclass
class ReconciliationResult:
    """Overall reconciliation result for entity."""
    entity_name: str
    checks: List[ReconciliationCheck] = field(default_factory=list)
    passed_count: int = 0
    failed_count: int = 0
    warning_count: int = 0
    overall_status: ReconciliationStatus = ReconciliationStatus.NOT_RUN
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "entity_name": self.entity_name,
            "checks": [c.to_dict() for c in self.checks],
            "passed_count": self.passed_count,
            "failed_count": self.failed_count,
            "warning_count": self.warning_count,
            "overall_status": self.overall_status.value,
            "timestamp": self.timestamp
        }


@dataclass
class WaveReconciliationReport:
    """Wave-level reconciliation report."""
    wave_id: str
    project_name: str
    entity_results: List[ReconciliationResult] = field(default_factory=list)
    total_entities: int = 0
    passed_entities: int = 0
    failed_entities: int = 0
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    reconciliation_score: float = 0.0
    can_proceed_to_production: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "wave_id": self.wave_id,
            "project_name": self.project_name,
            "entity_results": [r.to_dict() for r in self.entity_results],
            "total_entities": self.total_entities,
            "passed_entities": self.passed_entities,
            "failed_entities": self.failed_entities,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "reconciliation_score": round(self.reconciliation_score, 4),
            "can_proceed_to_production": self.can_proceed_to_production,
            "timestamp": self.timestamp
        }


class ReconciliationHarness:
    """Orchestrates Gate 3 reconciliation validation."""
    
    def __init__(self):
        """Initialize harness."""
        self.entity_results: Dict[str, ReconciliationResult] = {}
        self.wave_report: Optional[WaveReconciliationReport] = None
    
    def run_row_count_check(
        self,
        entity_name: str,
        source_count: int,
        target_count: int,
        threshold: float = 0.99
    ) -> ReconciliationCheck:
        """
        Validate row count parity between source and target.
        
        Args:
            entity_name: Name of entity
            source_count: Row count in source
            target_count: Row count in target
            threshold: Acceptable variance (default 0.99 = 99% match)
        
        Returns:
            ReconciliationCheck with result
        """
        variance = target_count / source_count if source_count > 0 else 0.0
        variance_pct = (1.0 - variance) * 100 if variance > 0 else 100.0
        
        if variance >= threshold:
            status = ReconciliationStatus.PASSED
            message = f"Row count match: {source_count} → {target_count} ({variance:.2%})"
        elif variance >= (threshold - 0.05):
            status = ReconciliationStatus.WARNING
            message = f"Row count variance acceptable: {source_count} → {target_count} ({variance:.2%})"
        else:
            status = ReconciliationStatus.FAILED
            message = f"Row count mismatch: {source_count} → {target_count} ({variance:.2%})"
        
        check = ReconciliationCheck(
            check_type=ReconciliationType.ROW_COUNT,
            entity_name=entity_name,
            source_count=source_count,
            target_count=target_count,
            threshold=threshold,
            status=status,
            variance_pct=variance_pct,
            message=message
        )
        
        return check
    
    def run_schema_check(
        self,
        entity_name: str,
        source_columns: int,
        target_columns: int,
        matching_columns: int
    ) -> ReconciliationCheck:
        """
        Validate schema completeness.
        
        Args:
            entity_name: Name of entity
            source_columns: Column count in source
            target_columns: Column count in target
            matching_columns: Matching column count
        
        Returns:
            ReconciliationCheck with result
        """
        schema_match = matching_columns / source_columns if source_columns > 0 else 0.0
        variance_pct = (1.0 - schema_match) * 100
        
        if schema_match >= 0.98:
            status = ReconciliationStatus.PASSED
            message = f"Schema match: {matching_columns}/{source_columns} columns"
        elif schema_match >= 0.95:
            status = ReconciliationStatus.WARNING
            message = f"Schema partial match: {matching_columns}/{source_columns} columns"
        else:
            status = ReconciliationStatus.FAILED
            message = f"Schema mismatch: {matching_columns}/{source_columns} columns"
        
        check = ReconciliationCheck(
            check_type=ReconciliationType.SCHEMA,
            entity_name=entity_name,
            source_count=source_columns,
            target_count=target_columns,
            threshold=0.98,
            status=status,
            variance_pct=variance_pct,
            message=message
        )
        
        return check
    
    def run_data_quality_check(
        self,
        entity_name: str,
        null_count: int,
        duplicate_count: int,
        total_records: int,
        threshold: float = 0.95
    ) -> ReconciliationCheck:
        """
        Validate data quality metrics.
        
        Args:
            entity_name: Name of entity
            null_count: Count of null values
            duplicate_count: Count of duplicates
            total_records: Total record count
            threshold: Acceptable quality threshold (0.95 = 95% valid)
        
        Returns:
            ReconciliationCheck with result
        """
        invalid_count = null_count + duplicate_count
        quality_score = (total_records - invalid_count) / total_records if total_records > 0 else 0.0
        variance_pct = (1.0 - quality_score) * 100
        
        if quality_score >= threshold:
            status = ReconciliationStatus.PASSED
            message = f"Data quality acceptable: {quality_score:.2%} valid ({null_count} nulls, {duplicate_count} duplicates)"
        elif quality_score >= (threshold - 0.05):
            status = ReconciliationStatus.WARNING
            message = f"Data quality marginal: {quality_score:.2%} valid ({null_count} nulls, {duplicate_count} duplicates)"
        else:
            status = ReconciliationStatus.FAILED
            message = f"Data quality poor: {quality_score:.2%} valid ({null_count} nulls, {duplicate_count} duplicates)"
        
        check = ReconciliationCheck(
            check_type=ReconciliationType.DATA_QUALITY,
            entity_name=entity_name,
            source_count=total_records - invalid_count,
            target_count=total_records,
            threshold=threshold,
            status=status,
            variance_pct=variance_pct,
            message=message
        )
        
        return check
    
    def add_entity_check(
        self,
        entity_name: str,
        check: ReconciliationCheck
    ) -> None:
        """Add check result to entity."""
        if entity_name not in self.entity_results:
            self.entity_results[entity_name] = ReconciliationResult(entity_name=entity_name)
        
        result = self.entity_results[entity_name]
        result.checks.append(check)
        
        if check.status == ReconciliationStatus.PASSED:
            result.passed_count += 1
        elif check.status == ReconciliationStatus.FAILED:
            result.failed_count += 1
        else:
            result.warning_count += 1
        
        # Update overall status
        if result.failed_count > 0:
            result.overall_status = ReconciliationStatus.FAILED
        elif result.warning_count > 0:
            result.overall_status = ReconciliationStatus.WARNING
        else:
            result.overall_status = ReconciliationStatus.PASSED
    
    def calculate_wave_reconciliation(
        self,
        wave_id: str,
        project_name: str
    ) -> WaveReconciliationReport:
        """
        Calculate wave-level reconciliation report.
        
        Args:
            wave_id: Wave identifier
            project_name: Project name
        
        Returns:
            Wave reconciliation report
        """
        self.wave_report = WaveReconciliationReport(
            wave_id=wave_id,
            project_name=project_name
        )
        
        self.wave_report.total_entities = len(self.entity_results)
        
        for entity_name, result in self.entity_results.items():
            self.wave_report.entity_results.append(result)
            
            if result.overall_status == ReconciliationStatus.PASSED:
                self.wave_report.passed_entities += 1
            else:
                self.wave_report.failed_entities += 1
            
            self.wave_report.total_checks += len(result.checks)
            self.wave_report.passed_checks += result.passed_count
            self.wave_report.failed_checks += result.failed_count
        
        # Calculate reconciliation score (0.0 to 1.0)
        if self.wave_report.total_checks > 0:
            self.wave_report.reconciliation_score = (
                self.wave_report.passed_checks / self.wave_report.total_checks
            )
        
        # Gate 3 requirement: reconciliation ≥ 0.95
        self.wave_report.can_proceed_to_production = (
            self.wave_report.reconciliation_score >= 0.95 and
            self.wave_report.failed_entities == 0
        )
        
        return self.wave_report
    
    def get_failed_entities(self) -> List[ReconciliationResult]:
        """Get entities with failed reconciliation."""
        return [
            r for r in self.entity_results.values()
            if r.overall_status == ReconciliationStatus.FAILED
        ]
    
    def get_warning_entities(self) -> List[ReconciliationResult]:
        """Get entities with warnings."""
        return [
            r for r in self.entity_results.values()
            if r.overall_status == ReconciliationStatus.WARNING
        ]
    
    def generate_remediation_plan(self) -> Dict[str, List[str]]:
        """Generate remediation plan for failed checks."""
        plan = {}
        
        for entity_name, result in self.entity_results.items():
            failed_checks = [c for c in result.checks if c.status == ReconciliationStatus.FAILED]
            if failed_checks:
                plan[entity_name] = [
                    f"[{c.check_type.value}] {c.message}"
                    for c in failed_checks
                ]
        
        return plan
    
    def get_reconciliation_summary(self) -> str:
        """Generate human-readable summary."""
        if not self.wave_report:
            return "No wave report generated yet"
        
        summary = (
            f"Wave Reconciliation Summary\n"
            f"Wave: {self.wave_report.wave_id}\n"
            f"Project: {self.wave_report.project_name}\n"
            f"Entities: {self.wave_report.passed_entities}/{self.wave_report.total_entities} passed\n"
            f"Checks: {self.wave_report.passed_checks}/{self.wave_report.total_checks} passed\n"
            f"Reconciliation Score: {self.wave_report.reconciliation_score:.2%}\n"
            f"Can Proceed to Production: {self.wave_report.can_proceed_to_production}\n"
        )
        
        return summary
    
    def save_report(self, file_path: str) -> None:
        """Save reconciliation report to file."""
        if not self.wave_report:
            raise ValueError("No wave report to save")
        
        with open(file_path, "w") as f:
            json.dump(self.wave_report.to_dict(), f, indent=2)
    
    def load_report(self, file_path: str) -> WaveReconciliationReport:
        """Load reconciliation report from file."""
        with open(file_path, "r") as f:
            data = json.load(f)
        
        report = WaveReconciliationReport(
            wave_id=data["wave_id"],
            project_name=data["project_name"],
            total_entities=data["total_entities"],
            passed_entities=data["passed_entities"],
            failed_entities=data["failed_entities"],
            total_checks=data["total_checks"],
            passed_checks=data["passed_checks"],
            failed_checks=data["failed_checks"],
            reconciliation_score=data["reconciliation_score"],
            can_proceed_to_production=data["can_proceed_to_production"],
            timestamp=data["timestamp"]
        )
        
        self.wave_report = report
        return report
