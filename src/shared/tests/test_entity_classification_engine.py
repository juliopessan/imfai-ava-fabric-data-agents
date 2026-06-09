"""
Tests for EntityClassificationEngine — Data sensitivity classification.
"""

import pytest
from src.shared.scripts.entity_classification_engine import (
    EntityClassificationEngine, SensitivityLevel, ClassificationReason
)


class TestEntityClassificationEngine:
    """Test suite for EntityClassificationEngine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = EntityClassificationEngine()
        assert len(engine.rules) > 0  # Has default rules
        assert len(engine.classifications) == 0
    
    def test_default_rules_exist(self):
        """Test default classification rules exist."""
        engine = EntityClassificationEngine()
        
        # Check some default rules
        assert any("ssn" in rule.pattern.lower() for rule in engine.rules.values())
        assert any("email" in rule.pattern.lower() for rule in engine.rules.values())
        assert any("credit" in rule.pattern.lower() for rule in engine.rules.values())
    
    def test_classify_public_entity(self):
        """Test classifying public entity."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "public_data",
            ["id", "name", "description"]
        )
        
        assert classification.sensitivity_level == SensitivityLevel.PUBLIC
        assert len(classification.detected_reasons) == 0
    
    def test_classify_pii_entity(self):
        """Test classifying PII entity."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "customer",
            ["customer_id", "email", "phone"]
        )
        
        assert classification.sensitivity_level in [SensitivityLevel.CONFIDENTIAL, SensitivityLevel.RESTRICTED]
        assert len(classification.detected_reasons) > 0
    
    def test_classify_restricted_entity(self):
        """Test classifying restricted entity."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "sensitive_health",
            ["patient_id", "medical_record", "date_of_birth"]
        )
        
        assert classification.sensitivity_level == SensitivityLevel.RESTRICTED
        assert classification.requires_encryption
        assert classification.requires_audit
        assert classification.requires_masking
    
    def test_column_classifications(self):
        """Test individual column classifications."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "mixed_data",
            ["id", "email", "name", "credit_card"]
        )
        
        assert classification.column_classifications["id"] == SensitivityLevel.PUBLIC
        assert classification.column_classifications["email"] in [SensitivityLevel.CONFIDENTIAL, SensitivityLevel.RESTRICTED]
        assert classification.column_classifications["credit_card"] == SensitivityLevel.RESTRICTED
    
    def test_add_custom_rule(self):
        """Test adding custom classification rule."""
        engine = EntityClassificationEngine()
        
        from src.shared.scripts.entity_classification_engine import ClassificationRule
        custom_rule = ClassificationRule(
            rule_id="custom_1",
            name="Custom Pattern",
            pattern=".*secret.*",
            sensitivity=SensitivityLevel.RESTRICTED,
            reason=ClassificationReason.ENCRYPTION_REQUIRED
        )
        
        engine.add_rule(custom_rule)
        
        classification = engine.classify_entity(
            "test",
            ["secret_key"]
        )
        
        assert classification.sensitivity_level == SensitivityLevel.RESTRICTED
    
    def test_get_restricted_entities(self):
        """Test filtering restricted entities."""
        engine = EntityClassificationEngine()
        
        engine.classify_entity("public_data", ["id", "name"])
        engine.classify_entity("restricted_data", ["patient_id", "medical_record"])
        engine.classify_entity("normal_data", ["product_id", "price"])
        
        restricted = engine.get_restricted_entities()
        assert len(restricted) >= 1
        assert any(c.entity_name == "restricted_data" for c in restricted)
    
    def test_encryption_requirements(self):
        """Test encryption requirement detection."""
        engine = EntityClassificationEngine()
        
        engine.classify_entity("encrypted_needed", ["credit_card", "account"])
        
        encryption_needed = engine.get_entities_requiring_encryption()
        assert len(encryption_needed) > 0
        assert any(c.entity_name == "encrypted_needed" for c in encryption_needed)
    
    def test_audit_requirements(self):
        """Test audit trail requirement detection."""
        engine = EntityClassificationEngine()
        
        engine.classify_entity("auditable", ["salary", "medical_record"])
        
        audit_needed = engine.get_entities_requiring_audit()
        assert len(audit_needed) > 0
    
    def test_masking_requirements(self):
        """Test masking requirement detection."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "masked_needed",
            ["ssn", "patient_id"]
        )
        
        assert classification.requires_masking is True
    
    def test_sensitivity_distribution(self):
        """Test sensitivity distribution calculation."""
        engine = EntityClassificationEngine()
        
        engine.classify_entity("public_1", ["id", "name"])
        engine.classify_entity("public_2", ["date", "description"])
        engine.classify_entity("confidential", ["email", "phone"])
        engine.classify_entity("restricted", ["credit_card", "ssn"])
        
        distribution = engine.get_sensitivity_distribution()
        
        assert distribution["public"] >= 2
        assert distribution["confidential"] >= 1
        assert distribution["restricted"] >= 1
    
    def test_case_insensitive_matching(self):
        """Test pattern matching is case-insensitive."""
        engine = EntityClassificationEngine()
        
        classification = engine.classify_entity(
            "mixed_case",
            ["Email", "PHONE", "SSN_Field"]
        )
        
        assert len(classification.detected_reasons) > 0
    
    def test_generate_classification_report(self):
        """Test report generation."""
        engine = EntityClassificationEngine()
        
        engine.classify_entity("public", ["id", "name"])
        engine.classify_entity("restricted", ["credit_card"])
        
        report = engine.generate_classification_report()
        
        assert "Entity Classification Report" in report
        assert "Total Entities: 2" in report
        assert "restricted" in report.lower() or "RESTRICTED" in report
    
    def test_multiple_entities_independent(self):
        """Test classifying multiple entities independently."""
        engine = EntityClassificationEngine()
        
        class1 = engine.classify_entity("entity_1", ["id", "name"])
        class2 = engine.classify_entity("entity_2", ["email", "phone"])
        class3 = engine.classify_entity("entity_3", ["credit_card", "ssn"])
        
        assert class1.sensitivity_level != class3.sensitivity_level
        assert class1.entity_name in engine.classifications
        assert class2.entity_name in engine.classifications
        assert class3.entity_name in engine.classifications
