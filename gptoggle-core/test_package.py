#!/usr/bin/env python3
"""
Test script to verify the gptoggle package installation.
"""

import sys

def test_imports():
    """Test importing the gptoggle package."""
    print("Testing imports...")
    
    try:
        import gptoggle
        print(f"✓ Successfully imported gptoggle v{gptoggle.__version__}")
        
        from gptoggle import Config, get_response, choose_provider_and_model, compare_models
        print("✓ Successfully imported core functions")
        
        from gptoggle.providers import get_available_providers, get_provider_class
        print("✓ Successfully imported provider utilities")
        
        from gptoggle.providers.base_provider import BaseProvider
        print("✓ Successfully imported base provider")
        
        from gptoggle.providers import (
            OpenAIProvider,
            ClaudeProvider,
            GeminiProvider, 
            GrokProvider
        )
        print("✓ Successfully imported provider implementations")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    return True

def test_model_selection():
    """Test the model selection functionality."""
    print("\nTesting model selection...")
    
    from gptoggle import choose_provider_and_model
    
    try:
        provider, model, reason = choose_provider_and_model("Write a Python function to calculate the Fibonacci sequence")
        print(f"✓ Auto-selected provider: {provider}, model: {model}")
        print(f"  Reason: {reason}")
    except Exception as e:
        print(f"✗ Model selection error: {e}")
        return False
    
    return True

def test_config():
    """Test the configuration module."""
    print("\nTesting configuration...")
    
    from gptoggle import Config
    from gptoggle.providers import get_available_providers
    
    try:
        config = Config()
        print(f"✓ Created configuration instance")
        
        providers = get_available_providers()
        print(f"✓ Available providers: {', '.join(providers)}")
        
        enabled = config.get_enabled_providers()
        print(f"✓ Enabled providers: {', '.join(enabled) if enabled else 'None'}")
        
        priority = config.get_provider_priority()
        print(f"✓ Provider priority: {', '.join(priority)}")
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("GPToggle Package Test\n")
    
    if not test_imports():
        print("\nImport tests failed. Please ensure the package is installed correctly.")
        sys.exit(1)
    
    if not test_config():
        print("\nConfiguration tests failed.")
        sys.exit(1)
    
    if not test_model_selection():
        print("\nModel selection tests failed.")
        sys.exit(1)
    
    print("\nAll tests passed! The package is installed correctly and functioning.")
    print("\nNote: To use the package with actual API calls, you need to set API keys")
    print("for at least one provider as environment variables.")

if __name__ == "__main__":
    main()