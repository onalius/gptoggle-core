#!/usr/bin/env python3
"""
Test script to verify the gptoggle package installation.
"""
import os
import sys


def test_imports():
    """Test importing the gptoggle package."""
    try:
        from gptoggle import (
            Config,
            get_response,
            choose_provider_and_model,
            compare_models,
            BaseProvider,
            OpenAIProvider,
            ClaudeProvider,
            GeminiProvider,
            GrokProvider,
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_config():
    """Test the configuration module."""
    try:
        from gptoggle.config import Config, ProviderConfig
        
        # Create a config
        config = Config()
        
        # Check that we have providers
        if not config.providers:
            print("✗ No providers found in configuration")
            return False
            
        # Check enabled providers
        enabled = config.get_enabled_providers()
        print(f"✓ Enabled providers: {', '.join(enabled)}")
        
        # Check provider priority
        priority = config.get_provider_priority()
        print(f"✓ Provider priority: {', '.join(priority)}")
        
        # Check if we can get provider configs
        for provider in config.providers:
            provider_config = config.get_provider_config(provider)
            if not isinstance(provider_config, ProviderConfig):
                print(f"✗ Failed to get config for {provider}")
                return False
                
        print("✓ Configuration tests successful")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_model_selection():
    """Test the model selection functionality."""
    try:
        from gptoggle import choose_provider_and_model
        
        # Test with a simple prompt
        prompt = "What is the capital of France?"
        provider, model, reason = choose_provider_and_model(prompt)
        
        print(f"✓ Auto-selected provider: {provider}")
        print(f"✓ Auto-selected model: {model}")
        print(f"✓ Selection reason: {reason}")
        
        return True
    except Exception as e:
        print(f"✗ Model selection error: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing GPToggle Package")
    print("======================")
    
    # Check for API keys
    api_keys = {
        "OpenAI": os.environ.get("OPENAI_API_KEY", ""),
        "Claude": os.environ.get("ANTHROPIC_API_KEY", ""),
        "Gemini": os.environ.get("GOOGLE_API_KEY", ""),
        "Grok": os.environ.get("XAI_API_KEY", ""),
    }

    available_providers = [name for name, key in api_keys.items() if key]
    
    if not available_providers:
        print("Warning: No API keys found. Some tests may fail.")
        print("Required environment variables:")
        print("  - OPENAI_API_KEY: For OpenAI provider (GPT models)")
        print("  - ANTHROPIC_API_KEY: For Claude provider")
        print("  - GOOGLE_API_KEY: For Gemini provider")
        print("  - XAI_API_KEY: For Grok provider")
    else:
        print(f"Available providers: {', '.join(available_providers)}")
    
    # Run tests
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Model Selection Test", test_model_selection),
    ]
    
    success = True
    for name, test_func in tests:
        print(f"\n[{name}]")
        if not test_func():
            success = False
    
    print("\nTest Summary")
    if success:
        print("✓ All tests passed")
    else:
        print("✗ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()