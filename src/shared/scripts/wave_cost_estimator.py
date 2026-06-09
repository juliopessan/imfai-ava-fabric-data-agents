"""
Wave Cost Estimator — Forecasts migration costs based on metrics.
Calculates data volume costs, compute hours, and resource requirements.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import json


class CostCategory(Enum):
    """Cost category types."""
    DATA_STORAGE = "data_storage"
    COMPUTE = "compute"
    NETWORK = "network"
    LICENSING = "licensing"
    LABOR = "labor"
    CONTINGENCY = "contingency"


class ResourceTier(Enum):
    """Resource tier levels."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    XLARGE = "xlarge"


@dataclass
class CostItem:
    """Single cost line item."""
    category: CostCategory
    resource_type: str
    quantity: float
    unit_cost: float
    duration_days: int = 30
    total_cost: float = field(default=0.0)
    notes: str = ""
    
    def __post_init__(self):
        """Calculate total cost."""
        self.total_cost = self.quantity * self.unit_cost * (self.duration_days / 30)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "category": self.category.value,
            "resource_type": self.resource_type,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "duration_days": self.duration_days,
            "total_cost": round(self.total_cost, 2),
            "notes": self.notes
        }


@dataclass
class MigrationCostEstimate:
    """Complete migration cost estimate."""
    wave_id: str
    project_name: str
    total_entities: int = 0
    data_volume_gb: float = 0.0
    estimated_days: int = 30
    cost_items: List[CostItem] = field(default_factory=list)
    total_compute_hours: float = 0.0
    total_data_cost: float = 0.0
    total_labor_hours: float = 0.0
    breakdown: Dict[str, float] = field(default_factory=dict)
    total_cost: float = 0.0
    cost_per_gb: float = 0.0
    contingency_pct: float = 0.15
    final_cost_with_contingency: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "wave_id": self.wave_id,
            "project_name": self.project_name,
            "total_entities": self.total_entities,
            "data_volume_gb": round(self.data_volume_gb, 2),
            "estimated_days": self.estimated_days,
            "cost_items": [c.to_dict() for c in self.cost_items],
            "total_compute_hours": round(self.total_compute_hours, 2),
            "total_data_cost": round(self.total_data_cost, 2),
            "total_labor_hours": round(self.total_labor_hours, 2),
            "breakdown": {k: round(v, 2) for k, v in self.breakdown.items()},
            "total_cost": round(self.total_cost, 2),
            "cost_per_gb": round(self.cost_per_gb, 4),
            "contingency_pct": self.contingency_pct,
            "final_cost_with_contingency": round(self.final_cost_with_contingency, 2),
            "timestamp": self.timestamp
        }


class WaveCostEstimator:
    """Estimates wave-level migration costs."""
    
    # Cost rates (in USD, can be customized)
    DATA_STORAGE_PER_GB_PER_MONTH = 0.023  # Azure storage
    COMPUTE_HOURS_PER_GB = 0.01  # Migration compute
    COMPUTE_RATE_PER_HOUR = 15.0  # hourly rate
    LABOR_RATE_PER_HOUR = 85.0  # labor cost
    NETWORK_PER_GB = 0.02  # data transfer
    
    def __init__(self):
        """Initialize estimator."""
        self.estimates: Dict[str, MigrationCostEstimate] = {}
    
    def estimate_data_storage_cost(
        self,
        data_volume_gb: float,
        months: int = 1
    ) -> float:
        """Calculate data storage cost."""
        return data_volume_gb * self.DATA_STORAGE_PER_GB_PER_MONTH * months
    
    def estimate_compute_cost(
        self,
        data_volume_gb: float,
        resource_tier: ResourceTier = ResourceTier.MEDIUM
    ) -> float:
        """Calculate compute cost based on data volume."""
        hours_multiplier = {
            ResourceTier.SMALL: 0.5,
            ResourceTier.MEDIUM: 1.0,
            ResourceTier.LARGE: 1.5,
            ResourceTier.XLARGE: 2.0
        }
        
        hours = data_volume_gb * self.COMPUTE_HOURS_PER_GB * hours_multiplier[resource_tier]
        return hours * self.COMPUTE_RATE_PER_HOUR
    
    def estimate_network_cost(self, data_volume_gb: float) -> float:
        """Calculate network/data transfer cost."""
        return data_volume_gb * self.NETWORK_PER_GB
    
    def estimate_labor_cost(
        self,
        total_entities: int,
        hours_per_entity: float = 4.0
    ) -> float:
        """Calculate labor cost."""
        total_hours = total_entities * hours_per_entity
        return total_hours * self.LABOR_RATE_PER_HOUR
    
    def estimate_licensing_cost(
        self,
        data_volume_gb: float,
        tool_licenses: int = 1
    ) -> float:
        """Calculate licensing cost (e.g., migration tools)."""
        base_license = 5000.0 * tool_licenses
        volume_charge = max(0, (data_volume_gb - 100) * 10)  # $10/GB beyond 100GB
        return base_license + volume_charge
    
    def create_estimate(
        self,
        wave_id: str,
        project_name: str,
        total_entities: int,
        data_volume_gb: float,
        estimated_days: int = 30,
        resource_tier: ResourceTier = ResourceTier.MEDIUM
    ) -> MigrationCostEstimate:
        """
        Create comprehensive cost estimate.
        
        Args:
            wave_id: Wave identifier
            project_name: Project name
            total_entities: Number of entities to migrate
            data_volume_gb: Total data volume in GB
            estimated_days: Estimated migration duration
            resource_tier: Resource tier for compute
        
        Returns:
            Complete cost estimate
        """
        estimate = MigrationCostEstimate(
            wave_id=wave_id,
            project_name=project_name,
            total_entities=total_entities,
            data_volume_gb=data_volume_gb,
            estimated_days=estimated_days
        )
        
        # Data storage cost
        storage_cost = self.estimate_data_storage_cost(data_volume_gb, months=1)
        storage_item = CostItem(
            category=CostCategory.DATA_STORAGE,
            resource_type="Azure Data Lake Storage",
            quantity=data_volume_gb,
            unit_cost=self.DATA_STORAGE_PER_GB_PER_MONTH,
            notes=f"Storage for {estimated_days} days"
        )
        estimate.cost_items.append(storage_item)
        
        # Compute cost
        compute_cost = self.estimate_compute_cost(data_volume_gb, resource_tier)
        hours = data_volume_gb * self.COMPUTE_HOURS_PER_GB * (1.0 if resource_tier == ResourceTier.MEDIUM else 1.5)
        estimate.total_compute_hours = hours
        compute_item = CostItem(
            category=CostCategory.COMPUTE,
            resource_type=f"Azure Databricks ({resource_tier.value})",
            quantity=hours,
            unit_cost=self.COMPUTE_RATE_PER_HOUR,
            notes=f"{hours:.1f} compute hours"
        )
        estimate.cost_items.append(compute_item)
        
        # Network cost
        network_cost = self.estimate_network_cost(data_volume_gb)
        network_item = CostItem(
            category=CostCategory.NETWORK,
            resource_type="Data Transfer (Egress)",
            quantity=data_volume_gb,
            unit_cost=self.NETWORK_PER_GB,
            notes="Cross-region egress"
        )
        estimate.cost_items.append(network_item)
        
        # Labor cost
        labor_cost = self.estimate_labor_cost(total_entities, hours_per_entity=4.0)
        estimate.total_labor_hours = total_entities * 4.0
        labor_item = CostItem(
            category=CostCategory.LABOR,
            resource_type="Migration Engineering",
            quantity=estimate.total_labor_hours,
            unit_cost=self.LABOR_RATE_PER_HOUR,
            notes=f"{estimate.total_labor_hours:.0f} engineering hours"
        )
        estimate.cost_items.append(labor_item)
        
        # Licensing cost
        licensing_cost = self.estimate_licensing_cost(data_volume_gb, tool_licenses=1)
        licensing_item = CostItem(
            category=CostCategory.LICENSING,
            resource_type="Migration Tools & Licenses",
            quantity=1,
            unit_cost=licensing_cost,
            duration_days=estimated_days,
            notes="Migration toolkit license"
        )
        estimate.cost_items.append(licensing_item)
        
        # Calculate totals
        estimate.total_cost = sum(item.total_cost for item in estimate.cost_items)
        
        # Breakdown by category
        for item in estimate.cost_items:
            if item.category.value not in estimate.breakdown:
                estimate.breakdown[item.category.value] = 0.0
            estimate.breakdown[item.category.value] += item.total_cost
        
        # Cost per GB
        if data_volume_gb > 0:
            estimate.cost_per_gb = estimate.total_cost / data_volume_gb
        
        # Add contingency (15% by default)
        contingency_cost = estimate.total_cost * estimate.contingency_pct
        contingency_item = CostItem(
            category=CostCategory.CONTINGENCY,
            resource_type="Contingency Reserve",
            quantity=1,
            unit_cost=contingency_cost,
            duration_days=estimated_days,
            notes=f"{estimate.contingency_pct*100:.0f}% contingency"
        )
        estimate.cost_items.append(contingency_item)
        estimate.breakdown["contingency"] = contingency_cost
        
        # Final cost with contingency
        estimate.final_cost_with_contingency = estimate.total_cost + contingency_cost
        
        self.estimates[wave_id] = estimate
        return estimate
    
    def get_cost_summary(self, wave_id: str) -> str:
        """Get human-readable cost summary."""
        if wave_id not in self.estimates:
            return f"No estimate found for {wave_id}"
        
        est = self.estimates[wave_id]
        
        summary = (
            f"Migration Cost Estimate\n"
            f"Wave: {est.wave_id}\n"
            f"Project: {est.project_name}\n"
            f"Entities: {est.total_entities}\n"
            f"Data Volume: {est.data_volume_gb:.1f} GB\n"
            f"Duration: {est.estimated_days} days\n"
            f"\nCost Breakdown:\n"
        )
        
        for category, cost in sorted(est.breakdown.items()):
            summary += f"  {category}: ${cost:,.2f}\n"
        
        summary += f"\nBase Total: ${est.total_cost:,.2f}\n"
        summary += f"With {est.contingency_pct*100:.0f}% Contingency: ${est.final_cost_with_contingency:,.2f}\n"
        summary += f"Cost per GB: ${est.cost_per_gb:.4f}\n"
        
        return summary
    
    def save_estimate(self, wave_id: str, file_path: str) -> None:
        """Save estimate to file."""
        if wave_id not in self.estimates:
            raise ValueError(f"No estimate found for {wave_id}")
        
        with open(file_path, "w") as f:
            json.dump(self.estimates[wave_id].to_dict(), f, indent=2)
    
    def load_estimate(self, file_path: str) -> MigrationCostEstimate:
        """Load estimate from file."""
        with open(file_path, "r") as f:
            data = json.load(f)
        
        estimate = MigrationCostEstimate(
            wave_id=data["wave_id"],
            project_name=data["project_name"],
            total_entities=data["total_entities"],
            data_volume_gb=data["data_volume_gb"],
            estimated_days=data["estimated_days"],
            total_compute_hours=data["total_compute_hours"],
            total_labor_hours=data["total_labor_hours"],
            breakdown=data["breakdown"],
            total_cost=data["total_cost"],
            cost_per_gb=data["cost_per_gb"],
            contingency_pct=data["contingency_pct"],
            final_cost_with_contingency=data["final_cost_with_contingency"],
            timestamp=data["timestamp"]
        )
        
        self.estimates[data["wave_id"]] = estimate
        return estimate
    
    def compare_estimates(self, wave_ids: List[str]) -> Dict:
        """Compare multiple estimates."""
        comparison = {}
        
        for wave_id in wave_ids:
            if wave_id in self.estimates:
                est = self.estimates[wave_id]
                comparison[wave_id] = {
                    "total_entities": est.total_entities,
                    "data_volume_gb": est.data_volume_gb,
                    "total_cost": est.total_cost,
                    "final_cost": est.final_cost_with_contingency,
                    "cost_per_gb": est.cost_per_gb,
                    "cost_per_entity": est.final_cost_with_contingency / est.total_entities if est.total_entities > 0 else 0
                }
        
        return comparison
