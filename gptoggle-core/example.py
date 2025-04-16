#!/usr/bin/env python3
"""
Example script showing how to use the GPToggle package with multiple providers.

This script demonstrates the main features of GPToggle, including:
- Using different AI providers
- Auto-selecting models
- Getting responses
- Comparing models across providers
"""

import os
import sys

from gptoggle import Config, get_response, choose_provider_and_model, compare_models
from gptoggle.providers import get_available_providers

def check_api_keys():
    """Check if the required API keys are set as environment variables."""
    api_keys = {
        "openai": os.environ.get("OPENAI_API_KEY"),
        "claude": os.environ.get("ANTHROPIC_API_KEY"),
        "gemini": os.environ.get("GOOGLE_API_KEY"),
        "grok": os.environ.get("XAI_API_KEY"),
    }
    
    available_keys = {k: bool(v) for k, v in api_keys.items()}
    
    print("API Key Status:")
    for provider, available in available_keys.items():
        status = "✓ Available" if available else "✗ Not Set"
        print(f"  {provider.upper()}: {status}")
    print()
    
    return any(available_keys.values())

def demo_available_providers():
    """Demonstrate checking available providers."""
    print("\n=== Available Providers ===")
    providers = get_available_providers()
    print(f"All providers: {', '.join(providers)}")
    
    # Get global configuration
    config = Config()
    enabled_providers = config.get_enabled_providers()
    print(f"Enabled providers: {', '.join(enabled_providers)}")
    
    priority = config.get_provider_priority()
    print(f"Priority order: {', '.join(priority)}")
    print()

def demo_auto_select():
    """Demonstrate auto-selection of provider and model."""
    print("\n=== Auto-Selection Demo ===")
    
    prompt = "Write a Python function to calculate the Fibonacci sequence"
    print(f"Prompt: {prompt}")
    
    provider, model, reason = choose_provider_and_model(prompt)
    print(f"Selected provider: {provider}")
    print(f"Selected model: {model}")
    print(f"Reason: {reason}")
    print()

def demo_get_response():
    """Demonstrate getting responses from different providers."""
    print("\n=== Get Response Demo ===")
    
    # First, try with a specific provider and model
    provider = "openai"
    model = "gpt-3.5-turbo"
    prompt = "Explain quantum computing in simple terms"
    
    print(f"Getting response from {provider}:{model}...")
    response = get_response(prompt, provider, model)
    print(f"\nResponse from {provider}:{model}:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    print()
    
    # Next, try with auto-selection
    prompt = "Tell me a short joke about programming"
    print(f"Getting response with auto-selection for: '{prompt}'")
    provider, model, reason = choose_provider_and_model(prompt)
    print(f"Auto-selected: {provider}:{model}")
    print(f"Reason: {reason}")
    
    response = get_response(prompt, provider, model)
    print(f"\nResponse from auto-selected {provider}:{model}:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    print()

def demo_compare():
    """Demonstrate comparing models across providers."""
    print("\n=== Model Comparison Demo ===")
    
    prompt = "Explain the difference between quantum computing and classical computing"
    print(f"Prompt: {prompt}")
    
    # Check available providers
    config = Config()
    enabled_providers = config.get_enabled_providers()
    
    # Ensure we have at least 2 providers for comparison
    if len(enabled_providers) < 2:
        print("Need at least 2 enabled providers with API keys for comparison.")
        print(f"Currently enabled: {', '.join(enabled_providers)}")
        return
    
    # Get the first two providers for comparison
    provider1, provider2 = enabled_providers[:2]
    
    # Choose default models for each
    model_pairs = [
        (provider1, get_response(prompt, provider1, None).split()[0]),  # This is a hack to get the model name
        (provider2, get_response(prompt, provider2, None).split()[0])   # Should be replaced with a proper method
    ]
    
    print(f"Comparing {provider1} and {provider2}...")
    compare_models(prompt, model_pairs)

def demo_provider_customization():
    """Demonstrate provider customization capabilities."""
    print("\n=== Provider Customization Demo ===")
    
    # Create a custom configuration
    config = Config()
    
    # Get current state
    print("Current configuration:")
    print(f"  Active provider: {config.active_provider}")
    print(f"  Enabled providers: {', '.join(config.get_enabled_providers())}")
    print(f"  Priority order: {', '.join(config.get_provider_priority())}")
    print()
    
    # Change configuration
    print("Customizing configuration...")
    config.set_active_provider("claude")
    
    # Disable a provider
    if "gemini" in config.get_enabled_providers():
        config.disable_provider("gemini")
    
    # Change priority
    new_priority = ["claude", "openai", "grok", "gemini"]
    config.set_provider_priority(new_priority)
    
    # Show updated configuration
    print("Updated configuration:")
    print(f"  Active provider: {config.active_provider}")
    print(f"  Enabled providers: {', '.join(config.get_enabled_providers())}")
    print(f"  Priority order: {', '.join(config.get_provider_priority())}")
    print()

def main():
    """Run the demonstration."""
    print("GPToggle Demonstration\n")
    
    # Check for API keys
    if not check_api_keys():
        print("Warning: No API keys are set. Most functions will not work properly.")
        print("Please set at least one of the following environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        print("  - GOOGLE_API_KEY")
        print("  - XAI_API_KEY")
        sys.exit(1)
    
    # Run demonstrations
    demo_available_providers()
    demo_provider_customization()
    demo_auto_select()
    
    # These demos make actual API calls
    if input("Run demos that make API calls? (y/n): ").lower() == 'y':
        demo_get_response()
        demo_compare()
    else:
        print("Skipping API call demos.")

if __name__ == "__main__":
    main()