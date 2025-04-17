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

# Try to import the package - this will work if installed
try:
    from gptoggle import (
        Config,
        get_response,
        choose_provider_and_model,
        compare_models
    )
except ImportError:
    # If not installed, try to import from relative path
    sys.path.insert(0, ".")
    from gptoggle import (
        Config,
        get_response,
        choose_provider_and_model,
        compare_models
    )


def check_api_keys():
    """Check if the required API keys are set as environment variables."""
    api_keys = {
        "OpenAI": os.environ.get("OPENAI_API_KEY", ""),
        "Claude": os.environ.get("ANTHROPIC_API_KEY", ""),
        "Gemini": os.environ.get("GOOGLE_API_KEY", ""),
        "Grok": os.environ.get("XAI_API_KEY", ""),
        "Llama": os.environ.get("META_AI_API_KEY", ""),
        "Perplexity": os.environ.get("PERPLEXITY_API_KEY", ""),
    }

    available_providers = [name for name, key in api_keys.items() if key]
    
    if not available_providers:
        print("Warning: No API keys found. Please set at least one API key to use GPToggle.")
        print("Required environment variables:")
        print("  - OPENAI_API_KEY: For OpenAI provider (GPT models)")
        print("  - ANTHROPIC_API_KEY: For Claude provider")
        print("  - GOOGLE_API_KEY: For Gemini provider")
        print("  - XAI_API_KEY: For Grok provider")
        print("  - META_AI_API_KEY: For Meta's Llama provider")
        print("  - PERPLEXITY_API_KEY: For Perplexity provider")
        return False
    
    print(f"Available providers: {', '.join(available_providers)}")
    return True


def demo_available_providers():
    """Demonstrate checking available providers."""
    print("\n=== Available Providers ===")
    config = Config()
    providers = config.get_enabled_providers()
    
    print(f"Enabled providers: {', '.join(providers)}")
    print(f"Current priority: {', '.join(config.get_provider_priority())}")
    
    # Disable one provider
    if "gemini" in providers:
        config.disable_provider("gemini")
        print(f"Disabled 'gemini': {', '.join(config.get_enabled_providers())}")
        
        # Re-enable it
        config.enable_provider("gemini")
        print(f"Re-enabled 'gemini': {', '.join(config.get_enabled_providers())}")
    
    # Change priority
    if "openai" in providers and "claude" in providers:
        config.set_provider_priority(["claude", "openai"])
        print(f"Changed priority: {', '.join(config.get_provider_priority())}")


def demo_auto_select():
    """Demonstrate auto-selection of provider and model."""
    print("\n=== Auto-selection ===")
    
    prompts = [
        "What is the capital of France?",
        "Write a function in Python to calculate factorial recursively",
        "Create a poem about artificial intelligence",
    ]
    
    for prompt in prompts:
        provider, model, reason = choose_provider_and_model(prompt)
        print(f"Prompt: {prompt}")
        print(f"Selected: {provider}:{model}")
        print(f"Reason: {reason}")
        print()


def demo_get_response():
    """Demonstrate getting responses from different providers."""
    print("\n=== Getting Responses ===")
    
    prompt = "Explain quantum computing in 3 sentences."
    
    # Auto-select
    provider, model, reason = choose_provider_and_model(prompt)
    print(f"Auto-selected: {provider}:{model} because {reason}")
    
    response = get_response(prompt, provider_name=provider, model=model)
    print(f"\nResponse from {provider}:{model}:")
    print(f"{response}\n")
    
    # Try with specific providers if available
    config = Config()
    if "claude" in config.get_enabled_providers():
        response = get_response(
            prompt, 
            provider_name="claude", 
            model="claude-3-sonnet-20240229"
        )
        print("Response from claude:claude-3-sonnet-20240229:")
        print(f"{response}\n")
        
    if "llama" in config.get_enabled_providers():
        response = get_response(
            prompt, 
            provider_name="llama", 
            model="llama-3-8b-instruct"
        )
        print("Response from llama:llama-3-8b-instruct:")
        print(f"{response}\n")
        
    if "perplexity" in config.get_enabled_providers():
        response = get_response(
            prompt, 
            provider_name="perplexity", 
            model="llama-3.1-sonar-small-128k-online"
        )
        print("Response from perplexity:llama-3.1-sonar-small-128k-online:")
        print(f"{response}\n")


def demo_compare():
    """Demonstrate comparing models across providers."""
    print("\n=== Comparing Models ===")
    
    # Only run the demo if we have multiple providers enabled
    config = Config()
    enabled_providers = config.get_enabled_providers()
    
    if len(enabled_providers) < 2:
        print("Need at least 2 enabled providers for comparison.")
        return
        
    # Find available provider pairs
    provider_pairs = []
    
    if "openai" in enabled_providers and "claude" in enabled_providers:
        provider_pairs.append(("openai", "gpt-4o"))
        provider_pairs.append(("claude", "claude-3-opus-20240229"))
    elif "openai" in enabled_providers and "gemini" in enabled_providers:
        provider_pairs.append(("openai", "gpt-4o"))
        provider_pairs.append(("gemini", "gemini-1.5-pro"))
    elif "openai" in enabled_providers and "llama" in enabled_providers:
        provider_pairs.append(("openai", "gpt-4o"))
        provider_pairs.append(("llama", "llama-3-70b-instruct"))
    elif "openai" in enabled_providers and "perplexity" in enabled_providers:
        provider_pairs.append(("openai", "gpt-4o"))
        provider_pairs.append(("perplexity", "llama-3.1-sonar-large-128k-online"))
    
    if not provider_pairs:
        print("No suitable provider pairs found for comparison.")
        return
        
    print(f"Comparing: {provider_pairs[0][0]}:{provider_pairs[0][1]} vs {provider_pairs[1][0]}:{provider_pairs[1][1]}")
    
    # This will prompt for user input to rate the responses
    # We'll run in non-interactive mode for this demo
    try:
        prompt = "Explain the difference between classical and quantum computing."
        print(f"Prompt: {prompt}")
        print("(In a real application, this would collect user ratings)")
        
        # Get the responses without the interactive comparison
        responses = {}
        for provider, model in provider_pairs:
            response = get_response(prompt, provider_name=provider, model=model)
            responses[f"{provider}:{model}"] = response
            
        # Display responses
        for source, text in responses.items():
            print(f"\n=== Response from {source} ===")
            print(text[:200] + "..." if len(text) > 200 else text)
    except Exception as e:
        print(f"Error in comparison: {e}")


def demo_provider_customization():
    """Demonstrate provider customization capabilities."""
    print("\n=== Provider Customization ===")
    
    config = Config()
    
    # Get config for OpenAI
    openai_config = config.get_provider_config("openai")
    print(f"OpenAI temperature: {openai_config.temperature}")
    print(f"OpenAI max_tokens: {openai_config.max_tokens}")
    
    # Modify provider settings (temporary for this session)
    openai_config.temperature = 0.9
    print(f"Modified OpenAI temperature: {openai_config.temperature}")
    
    # Check if Llama is available and get its config
    if "llama" in config.get_enabled_providers():
        llama_config = config.get_provider_config("llama")
        print(f"\nLlama temperature: {llama_config.temperature}")
        print(f"Llama max_tokens: {llama_config.max_tokens}")
        
        # Modify settings
        llama_config.temperature = 0.8
        print(f"Modified Llama temperature: {llama_config.temperature}")
    
    # Check if Perplexity is available and get its config
    if "perplexity" in config.get_enabled_providers():
        perplexity_config = config.get_provider_config("perplexity")
        print(f"\nPerplexity temperature: {perplexity_config.temperature}")
        print(f"Perplexity max_tokens: {perplexity_config.max_tokens}")
        
        # Modify settings
        perplexity_config.temperature = 0.5
        print(f"Modified Perplexity temperature: {perplexity_config.temperature}")


def main():
    """Run the demonstration."""
    print("GPToggle Demonstration")
    print("=====================")
    
    if not check_api_keys():
        sys.exit(1)
    
    demo_available_providers()
    demo_auto_select()
    demo_get_response()
    demo_compare()
    demo_provider_customization()
    
    print("\nDemonstration complete!")


if __name__ == "__main__":
    main()