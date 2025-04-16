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

from gptoggle import (
    get_response, 
    choose_provider_and_model, 
    compare_models,
    list_available_models,
    PROVIDERS,
    Config,
    config
)

def check_api_keys():
    """Check if the required API keys are set as environment variables."""
    missing_keys = []
    
    if not os.environ.get("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")
    
    if missing_keys:
        print(f"Warning: The following API keys are not set: {', '.join(missing_keys)}")
        print("Some examples may not work without the appropriate API keys.")
        print("\nTo set API keys:")
        
        if "OPENAI_API_KEY" in missing_keys:
            print("export OPENAI_API_KEY='your-openai-api-key'")
            
        if "ANTHROPIC_API_KEY" in missing_keys:
            print("export ANTHROPIC_API_KEY='your-anthropic-api-key'")
            
        return False
        
    return True

def demo_available_providers():
    """Demonstrate checking available providers."""
    print("\n=== Available AI Providers ===")
    
    for provider_name in PROVIDERS:
        print(f"- {provider_name}")
    
    # List models for each provider
    for provider_name in PROVIDERS:
        print(f"\n=== Available Models for {provider_name} ===")
        try:
            list_available_models(provider_name)
        except Exception as e:
            print(f"Error listing models for {provider_name}: {str(e)}")

def demo_auto_select():
    """Demonstrate auto-selection of provider and model."""
    prompts = [
        "What is the capital of France?",
        "Write a function in Python to find prime numbers up to n",
        "Write a short story about a robot that falls in love with a toaster",
        "Explain the pros and cons of quantum computing in simple terms"
    ]
    
    print("\n=== Auto-Selection of Provider and Model ===")
    
    for prompt in prompts:
        print(f"\nPrompt: \"{prompt}\"")
        try:
            provider, model, reason = choose_provider_and_model(prompt)
            print(f"Selected provider: {provider}")
            print(f"Selected model: {model}")
            print(f"Reason: {reason}")
        except Exception as e:
            print(f"Error: {str(e)}")

def demo_get_response():
    """Demonstrate getting responses from different providers."""
    print("\n=== Getting Responses from Different Providers ===")
    
    # OpenAI example
    if os.environ.get("OPENAI_API_KEY"):
        print("\n--- OpenAI Example ---")
        prompt = "Explain how a car engine works in simple terms"
        print(f"Prompt: \"{prompt}\"")
        try:
            response = get_response(prompt, provider_name="openai")
            print("Response:")
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Claude example
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n--- Claude Example ---")
        prompt = "What are the top 5 programming languages in 2025?"
        print(f"Prompt: \"{prompt}\"")
        try:
            response = get_response(prompt, provider_name="claude")
            print("Response:")
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")

def demo_compare():
    """Demonstrate comparing models across providers."""
    if os.environ.get("OPENAI_API_KEY") and os.environ.get("ANTHROPIC_API_KEY"):
        print("\n=== Comparing Models Across Providers ===")
        prompt = "Create a 5-day meal plan for a vegetarian diet"
        print(f"Prompt: \"{prompt}\"")
        try:
            print("Comparing OpenAI GPT-4o vs Claude Opus...")
            print("Results will be displayed and you'll be asked to rate which response is better.")
            compare_models(
                prompt, 
                [("openai", "gpt-4o"), ("claude", "claude-3-opus-20240229")]
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("\nSkipping comparison demo - requires both OpenAI and Anthropic API keys")

def demo_provider_customization():
    """Demonstrate provider customization capabilities."""
    print("\n=== Provider Customization ===")
    
    # Show current enabled providers
    print("Default enabled providers:", config.get_enabled_providers())
    print("Default provider priority:", config.get_provider_priority())
    
    # Disable a provider (if both are available)
    if "openai" in config.get_enabled_providers() and "claude" in config.get_enabled_providers():
        print("\n--- Example: Disabling a Provider ---")
        print("Disabling Claude provider...")
        config.disable_provider("claude")
        print("Enabled providers after disabling Claude:", config.get_enabled_providers())
        
        # Try auto-selection with disabled provider
        try:
            prompt = "What will the weather be like tomorrow?"
            print(f"\nAuto-selecting with prompt: \"{prompt}\"")
            provider, model, reason = choose_provider_and_model(prompt)
            print(f"Selected provider: {provider}")
            print(f"Selected model: {model}")
            print(f"Reason: {reason}")
        except Exception as e:
            print(f"Error: {str(e)}")
            
        # Re-enable the provider
        print("\nRe-enabling Claude provider...")
        config.enable_provider("claude")
        print("Enabled providers:", config.get_enabled_providers())
    
    # Change provider priority
    if "openai" in config.get_enabled_providers() and "claude" in config.get_enabled_providers():
        print("\n--- Example: Changing Provider Priority ---")
        print("Current priority:", config.get_provider_priority())
        
        # Set Claude as highest priority
        new_priority = ["claude", "openai"]
        print(f"Setting new priority: {new_priority}")
        config.set_provider_priority(new_priority)
        print("New priority:", config.get_provider_priority())
        
        # Try auto-selection with new priority
        try:
            prompt = "What are the best practices for database design?"
            print(f"\nAuto-selecting with prompt: \"{prompt}\"")
            provider, model, reason = choose_provider_and_model(prompt)
            print(f"Selected provider: {provider}")
            print(f"Selected model: {model}")
            print(f"Reason: {reason}")
        except Exception as e:
            print(f"Error: {str(e)}")
            
        # Reset priority to default
        default_priority = ["openai", "claude"]
        config.set_provider_priority(default_priority)
        
def main():
    """Run the demonstration."""
    print("GPToggle Multi-Provider Example")
    print("-" * 40)
    
    # Check API keys
    check_api_keys()
    
    # Run demos
    demo_available_providers()
    demo_auto_select()
    demo_get_response()
    demo_compare()
    demo_provider_customization()
    
    print("\nExample complete.")

if __name__ == "__main__":
    main()