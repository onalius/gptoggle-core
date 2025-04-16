"""
Tests for the config module.
"""
import pytest
from gptoggle.config import Config

def test_available_providers():
    """Test that providers list is not empty."""
    config = Config()
    assert len(config.providers) > 0
    
def test_provider_configuration():
    """Test provider configuration functionality."""
    from gptoggle.config import Config, ProviderConfig
    
    config = Config()
    
    # Test that we can retrieve provider configs
    for provider_name in ["openai", "claude", "gemini", "grok"]:
        provider_config = config.get_provider_config(provider_name)
        assert isinstance(provider_config, ProviderConfig)
        
        # Test that the provider config has basic attributes
        assert hasattr(provider_config, "temperature")
        assert hasattr(provider_config, "max_tokens")
        assert hasattr(provider_config, "max_comparison_tokens")
        
def test_provider_enable_disable():
    """Test provider enable/disable functionality."""
    from gptoggle.config import Config
    
    config = Config()
    
    # Test enabling a provider
    result = config.enable_provider("openai")
    assert result is True
    assert "openai" in config.get_enabled_providers()
    
    # Test disabling a provider
    result = config.disable_provider("openai")
    assert result is True
    assert "openai" not in config.get_enabled_providers()
    
    # Re-enable for other tests
    config.enable_provider("openai")
    
def test_provider_priority():
    """Test provider priority functionality."""
    from gptoggle.config import Config
    
    config = Config()
    
    # Ensure multiple providers are enabled
    config.enable_provider("openai")
    config.enable_provider("claude")
    
    # Test setting priority
    new_priority = ["claude", "openai"]
    result = config.set_provider_priority(new_priority)
    assert result is True
    
    # Test that priority is correctly retrieved
    current_priority = config.get_provider_priority()
    assert current_priority == new_priority