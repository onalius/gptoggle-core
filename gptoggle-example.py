#!/usr/bin/env python3
"""
GPToggle Python Example

This example demonstrates how to use the standalone gptoggle_minimal.py file
without installing the full package.

Make sure your API keys are set as environment variables:
- OPENAI_API_KEY for OpenAI
- ANTHROPIC_API_KEY for Claude
- GOOGLE_AI_API_KEY for Gemini
- GROK_API_KEY for Grok
"""

import os
import sys
from typing import Optional

# Import functions from the standalone module
from gptoggle_minimal import (
    recommend_model,
    get_response,
    get_available_providers
)

def check_api_keys():
    """Check if required API keys are set."""
    providers = []
    if os.environ.get('OPENAI_API_KEY'):
        providers.append('OpenAI')
    if os.environ.get('ANTHROPIC_API_KEY'):
        providers.append('Claude')
    if os.environ.get('GOOGLE_AI_API_KEY'):
        providers.append('Gemini')
    if os.environ.get('GROK_API_KEY'):
        providers.append('Grok')
        
    if not providers:
        print("Warning: No API keys found. Set at least one of these environment variables:")
        print("- OPENAI_API_KEY for OpenAI")
        print("- ANTHROPIC_API_KEY for Claude")
        print("- GOOGLE_AI_API_KEY for Gemini")
        print("- GROK_API_KEY for Grok")
    else:
        print(f"API keys found for: {', '.join(providers)}")

def demo_available_providers():
    """Demonstrate checking available providers."""
    print("\n=== Available Providers ===")
    providers = get_available_providers()
    print(f"Providers with valid API keys: {', '.join(providers)}")

def demo_auto_select(prompt: str):
    """Demonstrate auto-selection of provider and model."""
    print("\n=== Auto Model Selection ===")
    provider, model = recommend_model(prompt)
    print(f"For prompt: '{prompt}'")
    print(f"Recommended provider: {provider}")
    print(f"Recommended model: {model}")

def demo_get_response(prompt: str, provider: Optional[str] = None, model: Optional[str] = None):
    """Demonstrate getting responses."""
    print("\n=== Getting Response ===")
    provider_str = provider if provider else "auto-selected"
    model_str = model if model else "auto-selected"
    print(f"Provider: {provider_str}")
    print(f"Model: {model_str}")
    print(f"Prompt: '{prompt}'")
    
    try:
        print("\nGenerating response...")
        response = get_response(prompt, provider, model)
        print("\nResponse:")
        print("-" * 50)
        print(response)
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run the demonstration."""
    # Check for API keys
    check_api_keys()
    
    # Demo available providers
    demo_available_providers()
    
    # Demo auto model selection
    prompt = "Explain quantum computing in simple terms."
    demo_auto_select(prompt)
    
    # Demo getting a response
    demo_get_response(prompt)
    
    # Optional: Try with specific provider/model
    if os.environ.get('OPENAI_API_KEY'):
        custom_prompt = "Write a Python function to calculate Fibonacci numbers."
        demo_get_response(custom_prompt, provider="openai", model="gpt-3.5-turbo")

if __name__ == "__main__":
    main()