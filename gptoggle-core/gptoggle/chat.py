#!/usr/bin/env python3
"""
A multi-provider CLI wrapper for AI APIs with intelligent model selection and comparison capabilities.

Usage:
    python -m gptoggle.chat "Your question here"
    python -m gptoggle.chat "Your question here" --provider openai --model gpt-4o
    python -m gptoggle.chat "Your question here" --provider claude --model claude-3-opus-20240229
    python -m gptoggle.chat "Your question here" --compare openai:gpt-4o,claude:claude-3-opus-20240229
"""

import argparse
import sys
import os
from typing import List, Dict, Tuple, Optional

from . import config
from .providers import PROVIDERS, DEFAULT_PROVIDER
from .compare import compare_models

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Multi-provider CLI wrapper for AI APIs with auto-model selection"
    )
    parser.add_argument(
        "prompt", 
        type=str, 
        nargs="?",
        help="The prompt or question to send to the API"
    )
    parser.add_argument(
        "--provider", 
        type=str, 
        help=f"AI provider to use (e.g., {', '.join(PROVIDERS.keys())})"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        help="Override the auto-selected model (specific to provider)"
    )
    parser.add_argument(
        "--compare", 
        type=str, 
        help="Compare responses from two models (format: provider1:model1,provider2:model2)"
    )
    parser.add_argument(
        "--list-models", 
        action="store_true", 
        help="List all available models for the selected provider(s)"
    )
    parser.add_argument(
        "--list-providers", 
        action="store_true", 
        help="List all available AI providers"
    )
    
    return parser.parse_args()

def get_provider_instance(provider_name: str):
    """Get provider instance by name."""
    if provider_name not in PROVIDERS:
        print(f"Error: Unknown provider '{provider_name}'")
        print(f"Available providers: {', '.join(PROVIDERS.keys())}")
        return None
    
    provider_class = PROVIDERS[provider_name]
    return provider_class()

def list_providers():
    """Display all available AI providers."""
    print("Available AI providers:")
    for provider_name in PROVIDERS:
        print(f"- {provider_name}")
    print(f"\nDefault provider: {DEFAULT_PROVIDER}")
    print("\nUse --provider to specify a provider, e.g.:")
    print(f"  gptoggle \"Your prompt\" --provider claude")

def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Check for list-providers flag
    if args.list_providers:
        list_providers()
        return
    
    # Determine the provider to use
    provider_name = args.provider or config.config.active_provider
    provider = get_provider_instance(provider_name)
    if not provider:
        return
    
    # Check for list-models flag
    if args.list_models:
        if args.provider:
            provider.list_models()
        else:
            # Show models for all providers
            for provider_name in PROVIDERS:
                provider_instance = get_provider_instance(provider_name)
                provider_instance.list_models()
                print()
        return
    
    # Make sure we have a prompt
    if not args.prompt:
        print("Error: Please provide a prompt.")
        print("Usage: gptoggle \"Your prompt\"")
        return
    
    # Get the prompt
    prompt = args.prompt
    
    # Compare mode
    if args.compare:
        try:
            model_specs = args.compare.split(',')
            if len(model_specs) != 2:
                print("Error: --compare requires exactly two models separated by a comma")
                return
            
            # Parse provider:model specifications
            model_pairs = []
            for spec in model_specs:
                if ':' in spec:
                    provider_name, model_name = spec.split(':', 1)
                    provider_instance = get_provider_instance(provider_name)
                    if not provider_instance:
                        return
                    if model_name not in provider_instance.available_models:
                        print(f"Error: Invalid model '{model_name}' for provider '{provider_name}'")
                        return
                    model_pairs.append((provider_name, model_name))
                else:
                    # Default to active provider
                    model_name = spec
                    if model_name not in provider.available_models:
                        print(f"Error: Invalid model '{model_name}' for provider '{provider_name}'")
                        return
                    model_pairs.append((provider_name, model_name))
            
            # Run comparison
            compare_models(prompt, model_pairs)
            return
        except Exception as e:
            print(f"Error parsing comparison specification: {e}")
            print("Format should be: provider1:model1,provider2:model2")
            print("Example: openai:gpt-4o,claude:claude-3-opus-20240229")
            return
    
    # Validate API key for the provider
    if not provider.validate_api_key():
        return
    
    # Single model mode
    if args.model:
        model = args.model
        reason = "Manually selected by user"
        
        # Validate model exists for this provider
        if model not in provider.available_models:
            print(f"Error: Invalid model '{model}' for provider '{provider_name}'")
            print("Available models:")
            provider.list_models()
            return
    else:
        # Auto-select model based on prompt
        model, reason = provider.choose_model(prompt)
    
    # Get response
    print(f"Using provider: {provider_name}")
    if not args.model:  # Only show auto-select info if not manually specified
        print(f"Auto-selected model: {model}")
        print(f"Reason: {reason}")
    
    print(f"Getting response from {model}...")
    
    # Get provider-specific settings
    provider_config = config.config.get_provider_config(provider_name)
    response = provider.get_response(
        prompt=prompt, 
        model=model,
        temperature=provider_config.temperature,
        max_tokens=provider_config.max_tokens
    )
    
    # Print response
    print("\n----- Response -----")
    print(response)
    print("--------------------")

def get_response(prompt: str, provider_name: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Get a response from the specified provider and model.
    For use as a Python API.
    
    Args:
        prompt: The user's prompt
        provider_name: The provider to use (e.g., "openai", "claude")
        model: The model to use (specific to provider)
        
    Returns:
        The model's response as a string
    """
    # Determine provider
    provider_name = provider_name or config.config.active_provider
    provider = get_provider_instance(provider_name)
    if not provider:
        return f"Error: Unknown provider '{provider_name}'"
    
    # Validate API key
    if not provider.validate_api_key():
        return f"Error: API key not set for provider '{provider_name}'"
    
    # Determine model
    if model is None:
        model, _ = provider.choose_model(prompt)
    elif model not in provider.available_models:
        return f"Error: Invalid model '{model}' for provider '{provider_name}'"
    
    # Get provider-specific settings
    provider_config = config.config.get_provider_config(provider_name)
    
    # Get response
    return provider.get_response(
        prompt=prompt, 
        model=model,
        temperature=provider_config.temperature,
        max_tokens=provider_config.max_tokens
    )

def choose_provider_and_model(prompt: str) -> Tuple[str, str, str]:
    """
    Automatically select the best provider and model for a prompt.
    For use as a Python API.
    
    Args:
        prompt: The user's prompt
        
    Returns:
        A tuple of (provider_name, model_name, reason)
    """
    # Get enabled providers in priority order
    priority_providers = config.config.get_provider_priority()
    
    if not priority_providers:
        raise ValueError("No providers are enabled. Enable at least one provider using config.enable_provider().")
    
    # Try each provider to get their model recommendations
    recommendations = []
    
    for provider_name in priority_providers:
        if provider_name in PROVIDERS:
            provider_class = PROVIDERS[provider_name]
            provider = provider_class()
            
            # Skip providers with missing API keys
            if not provider.validate_api_key():
                continue
                
            model, reason = provider.choose_model(prompt)
            recommendations.append((provider_name, model, reason))
    
    # If we have recommendations, return the highest priority one
    if recommendations:
        return recommendations[0]
    
    # If no providers are available (e.g., no API keys set), raise an error
    raise ValueError("No providers with valid API keys are available. Please set at least one API key.")

def list_available_models(provider_name: Optional[str] = None):
    """
    Display all available models for the specified provider(s).
    For use as a Python API.
    
    Args:
        provider_name: Name of the provider, or None for all enabled providers
    """
    if provider_name:
        # Check if this specific provider is enabled
        if provider_name in config.config.get_enabled_providers():
            provider = get_provider_instance(provider_name)
            if provider:
                provider.list_models()
        else:
            print(f"Provider '{provider_name}' is not enabled. "
                  f"Use config.enable_provider('{provider_name}') to enable it.")
    else:
        # Show enabled providers in priority order
        enabled_providers = config.config.get_provider_priority()
        
        if not enabled_providers:
            print("No providers are currently enabled. "
                  "Use config.enable_provider(provider_name) to enable a provider.")
            return
            
        for provider_name in enabled_providers:
            if provider_name in PROVIDERS:
                provider = get_provider_instance(provider_name)
                if provider:
                    print(f"\n=== Models for {provider_name} ===")
                    provider.list_models()
                    print()

if __name__ == "__main__":
    main()