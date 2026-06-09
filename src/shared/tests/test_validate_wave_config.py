"""Tests for validate_wave_config.py"""

import pytest
import yaml
from pathlib import Path
from src.shared.scripts.validate_wave_config import WaveConfigValidator, validate_wave_config


class TestWaveConfigValidator:
    """Test WaveConfigValidator class."""
    
    def test_missing_config_file(self, temp_project_dir):
        """Test validation fails when config file missing."""
        nonexistent = temp_project_dir / "nonexistent.yaml"
        validator = WaveConfigValidator(nonexistent)
        result = validator.validate()
        
        assert result.valid is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()
    
    def test_empty_yaml_file(self, temp_project_dir):
        """Test validation fails on empty YAML."""
        config_file = temp_project_dir / "wave-config.yaml"
        config_file.write_text("")
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert "empty" in result.errors[0].lower()
    
    def test_invalid_yaml_syntax(self, temp_project_dir):
        """Test validation fails on malformed YAML."""
        config_file = temp_project_dir / "wave-config.yaml"
        config_file.write_text("invalid: yaml: syntax: [")
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert "yaml" in result.errors[0].lower()
    
    def test_valid_minimal_config(self, temp_project_dir, sample_wave_config):
        """Test validation passes with minimal valid config."""
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is True
        assert len(result.errors) == 0
        assert result.score > 0.85
    
    def test_missing_required_field_wave_id(self, temp_project_dir, sample_wave_config):
        """Test validation fails when wave_id is missing."""
        del sample_wave_config["wave_id"]
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("wave_id" in err for err in result.errors)
    
    def test_missing_required_field_entities(self, temp_project_dir, sample_wave_config):
        """Test validation fails when entities is missing."""
        del sample_wave_config["entities"]
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("entities" in err for err in result.errors)
    
    def test_invalid_platform(self, temp_project_dir, sample_wave_config):
        """Test validation fails with invalid target_platform."""
        sample_wave_config["target_platform"] = "invalid-platform"
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("platform" in err.lower() for err in result.errors)
    
    def test_empty_entities_list_warning(self, temp_project_dir, sample_wave_config):
        """Test warning when entities list is empty."""
        sample_wave_config["entities"] = []
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is True  # Not an error, just warning
        assert any("empty" in w.lower() for w in result.warnings)
    
    def test_entity_missing_name(self, temp_project_dir, sample_wave_config):
        """Test validation fails when entity missing 'name'."""
        sample_wave_config["entities"] = [{"source_schema": "public"}]
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("name" in err for err in result.errors)
    
    def test_no_gates_required_warning(self, temp_project_dir, sample_wave_config):
        """Test warning when no gates are required."""
        sample_wave_config["gates"] = {
            "gate1_required": False,
            "gate2_required": False,
            "gate3_required": False
        }
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is True
        assert any("gates" in w.lower() for w in result.warnings)
    
    def test_wrong_field_type_entities(self, temp_project_dir, sample_wave_config):
        """Test validation fails when entities is not a list."""
        sample_wave_config["entities"] = "not_a_list"
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("list" in err.lower() for err in result.errors)
    
    def test_score_calculation(self, temp_project_dir, sample_wave_config):
        """Test score is calculated correctly."""
        config_file = temp_project_dir / "wave-config.yaml"
        
        # Valid config
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.score == 1.0  # No errors/warnings
    
    def test_score_with_errors(self, temp_project_dir, sample_wave_config):
        """Test score decreases with errors."""
        del sample_wave_config["wave_id"]
        del sample_wave_config["entities"]
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        # 2 errors × 0.15 penalty = 0.70
        assert result.score == pytest.approx(0.70, abs=0.01)


class TestValidateWaveConfigFunction:
    """Test the public validate_wave_config function."""
    
    def test_function_returns_dict(self, temp_project_dir, sample_wave_config):
        """Test function returns a dict."""
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        result = validate_wave_config(str(config_file))
        
        assert isinstance(result, dict)
        assert "valid" in result
        assert "errors" in result
        assert "warnings" in result
        assert "score" in result
    
    def test_function_with_valid_config(self, temp_project_dir, sample_wave_config):
        """Test function validates successfully."""
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        result = validate_wave_config(str(config_file))
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_very_large_entity_count(self, temp_project_dir, sample_wave_config):
        """Test with large number of entities."""
        sample_wave_config["entities"] = [
            {"name": f"table_{i}", "source_schema": "public"}
            for i in range(1000)
        ]
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is True
    
    def test_special_characters_in_fields(self, temp_project_dir, sample_wave_config):
        """Test with special characters in field values."""
        sample_wave_config["project_name"] = "Projeto-Migracao_2026 (v1.0) @Alpha"
        sample_wave_config["wave_id"] = "wave-001-α-β-γ"
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is True
    
    def test_null_valued_required_field(self, temp_project_dir, sample_wave_config):
        """Test with null value for required field."""
        sample_wave_config["discovery_owner"] = None
        config_file = temp_project_dir / "wave-config.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(sample_wave_config, f)
        
        validator = WaveConfigValidator(config_file)
        result = validator.validate()
        
        assert result.valid is False
        assert any("empty" in err.lower() for err in result.errors)
