"""
Entity Quality Reporter — Generates quality metrics and trend reports for entities.
Consolidates quality data across gates and identifies improvement opportunities.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class EntityQualityMetric:
    """Quality metrics for an entity across time."""
    entity_name: str
    gate_name: str
    timestamp: str
    completude: float
    quality: float
    error_count: int
    quality_trend: str  # "improving", "stable", "declining"


class EntityQualityReporter:
    """Generates quality reports for entities."""
    
    def __init__(self):
        """Initialize reporter."""
        self.metrics: List[EntityQualityMetric] = []
    
    def add_metric(
        self,
        entity_name: str,
        gate_name: str,
        completude: float,
        quality: float,
        error_count: int
    ) -> None:
        """Add a quality metric."""
        metric = EntityQualityMetric(
            entity_name=entity_name,
            gate_name=gate_name,
            timestamp=datetime.utcnow().isoformat(),
            completude=completude,
            quality=quality,
            error_count=error_count,
            quality_trend="stable"  # Will be updated by trend analysis
        )
        
        self.metrics.append(metric)
    
    def get_metrics_for_entity(self, entity_name: str) -> List[EntityQualityMetric]:
        """Get all metrics for an entity."""
        return [m for m in self.metrics if m.entity_name == entity_name]
    
    def calculate_trends(self) -> Dict[str, str]:
        """Calculate quality trends by entity."""
        trends = {}
        
        # Group by entity
        by_entity: Dict[str, List[EntityQualityMetric]] = {}
        for metric in self.metrics:
            if metric.entity_name not in by_entity:
                by_entity[metric.entity_name] = []
            by_entity[metric.entity_name].append(metric)
        
        # Calculate trend for each entity
        for entity, metrics in by_entity.items():
            if len(metrics) < 2:
                trends[entity] = "insufficient_data"
                continue
            
            # Sort by timestamp
            sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)
            
            # Compare first and last
            first_quality = sorted_metrics[0].quality
            last_quality = sorted_metrics[-1].quality
            
            if last_quality > first_quality + 0.05:
                trend = "improving"
            elif last_quality < first_quality - 0.05:
                trend = "declining"
            else:
                trend = "stable"
            
            trends[entity] = trend
        
        # Update metrics with trends
        for metric in self.metrics:
            metric.quality_trend = trends.get(metric.entity_name, "unknown")
        
        return trends
    
    def generate_entity_report(self, entity_name: str) -> Dict[str, Any]:
        """Generate detailed report for an entity."""
        metrics = self.get_metrics_for_entity(entity_name)
        
        if not metrics:
            return {
                "entity_name": entity_name,
                "error": "No metrics found for entity"
            }
        
        # Calculate stats
        completude_values = [m.completude for m in metrics]
        quality_values = [m.quality for m in metrics]
        error_counts = [m.error_count for m in metrics]
        
        return {
            "entity_name": entity_name,
            "metric_count": len(metrics),
            "average_completude": sum(completude_values) / len(completude_values),
            "average_quality": sum(quality_values) / len(quality_values),
            "min_quality": min(quality_values),
            "max_quality": max(quality_values),
            "total_errors": sum(error_counts),
            "trend": metrics[-1].quality_trend if metrics else "unknown",
            "gates_analyzed": list(set(m.gate_name for m in metrics)),
            "recommendations": self._get_recommendations(metrics)
        }
    
    def _get_recommendations(self, metrics: List[EntityQualityMetric]) -> List[str]:
        """Generate recommendations based on metrics."""
        recs = []
        
        # Low completude
        if metrics and metrics[-1].completude < 0.90:
            recs.append("Completude below 90% - investigate missing data")
        
        # Low quality
        if metrics and metrics[-1].quality < 0.80:
            recs.append("Quality score below 80% - review data validation rules")
        
        # High error count
        if metrics and metrics[-1].error_count > 5:
            recs.append(f"High error count ({metrics[-1].error_count}) - data quality review needed")
        
        # Declining trend
        if metrics and metrics[-1].quality_trend == "declining":
            recs.append("Quality declining - investigate root cause")
        
        return recs if recs else ["Entity quality is acceptable"]
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate summary report across all entities."""
        self.calculate_trends()
        
        entities = set(m.entity_name for m in self.metrics)
        entity_reports = {e: self.generate_entity_report(e) for e in entities}
        
        # Calculate aggregate statistics
        all_completude = [m.completude for m in self.metrics]
        all_quality = [m.quality for m in self.metrics]
        
        return {
            "report_timestamp": datetime.utcnow().isoformat(),
            "total_entities": len(entities),
            "total_metrics": len(self.metrics),
            "average_completude": sum(all_completude) / len(all_completude) if all_completude else 0,
            "average_quality": sum(all_quality) / len(all_quality) if all_quality else 0,
            "entities_improving": len([e for e, r in entity_reports.items() if r.get("trend") == "improving"]),
            "entities_declining": len([e for e, r in entity_reports.items() if r.get("trend") == "declining"]),
            "entity_details": entity_reports
        }
    
    def save_report(self, report: Dict[str, Any], output_path) -> None:
        """Save report to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
    
    def to_list(self) -> List[Dict[str, Any]]:
        """Convert metrics to list of dicts."""
        return [asdict(m) for m in self.metrics]
