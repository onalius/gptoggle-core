"""
Tests for the config module.
"""
import pytest
from gptoggle import OpenAIConfig, AVAILABLE_MODELS

def test_available_models():
    """Test that available models list is not empty."""
    assert len(AVAILABLE_MODELS) > 0
    
def test_model_capabilities():
    """Test that the model capabilities dictionary contains the expected models."""
    from gptoggle.config import MODEL_CAPABILITIES
    
    # Check that all available models have capability definitions
    for model in AVAILABLE_MODELS:
        assert model in MODEL_CAPABILITIES
        
    # Check that the capability definitions have the expected keys
    for model, capabilities in MODEL_CAPABILITIES.items():
        assert "max_tokens" in capabilities
        assert "capabilities" in capabilities
        assert "tier" in capabilities
        
        # Check that capabilities is a list
        assert isinstance(capabilities["capabilities"], list)
        
        # Check that tier is either standard or premium
        assert capabilities["tier"] in ["standard", "premium"]
        
def test_openai_config():
    """Test OpenAIConfig class."""
    config = OpenAIConfig(api_key="test_key", temperature=0.5, max_tokens=200)
    
    assert config.api_key == "test_key"
    assert config.temperature == 0.5
    assert config.max_tokens == 200
    
    # Test default values
    default_config = OpenAIConfig()
    assert hasattr(default_config, "temperature")
    assert hasattr(default_config, "max_tokens")
    assert hasattr(default_config, "max_comparison_tokens")