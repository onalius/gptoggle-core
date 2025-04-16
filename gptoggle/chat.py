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
from typing import Dict, List, Optional, Tuple, Any

from gptoggle.config import config
from gptoggle.providers import get_provider_class, get_available_providers
from gptoggle.utils import get_provider_instance, get_response, choose_provider_and_model
from gptoggle.compare import compare_models as compare_models_func

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="GPToggle: Multi-provider AI model wrapper")
    
    # Command group for basic prompt
    parser.add_argument("prompt", nargs="?", help="The prompt to send to the AI")
    
    # Provider and model specification
    parser.add_argument("--provider", "-p", help="The AI provider to use (e.g., openai, claude)")
    parser.add_argument("--model", "-m", help="The model to use (specific to the provider)")
    
    # Model comparison
    parser.add_argument(
        "--compare", "-c", 
        help="Compare responses from different models. Format: provider1:model1,provider2:model2"
    )
    
    # List available providers and models
    parser.add_argument("--list-providers", action="store_true", help="List all available AI providers")
    parser.add_argument("--list-models", action="store_true", help="List available models for the specified provider")
    
    # Advanced options
    parser.add_argument("--temperature", "-t", type=float, default=0.7, help="Temperature for response generation")
    parser.add_argument("--max-tokens", type=int, default=1000, help="Maximum tokens for the response")
    
    return parser.parse_args()

# We use get_provider_instance from utils.py instead

def list_providers():
    """Display all available AI providers."""
    providers = get_available_providers()
    enabled_providers = config.get_enabled_providers()
    priority = config.get_provider_priority()
    
    print("Available AI Providers:")
    for i, provider in enumerate(providers):
        status = "ENABLED" if provider in enabled_providers else "DISABLED"
        priority_str = f"Priority: {priority.index(provider) + 1}" if provider in priority else ""
        print(f"{i+1}. {provider.upper()} - {status} {priority_str}")
        
        # Check if API key is set
        provider_config = config.get_provider_config(provider)
        if provider_config.api_key:
            print(f"   API Key: Set")
        else:
            print(f"   API Key: Not set (required for use)")
            print(f"   Set with: export {provider.upper()}_API_KEY='your-api-key'")
        
        # Get instance details if available
        instance = get_provider_instance(provider)
        if instance and instance.validate_api_key():
            print(f"   Default model: {instance.default_model}")
            print(f"   Available models: {len(instance.available_models)}")
        print()

def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # List providers if requested
    if args.list_providers:
        list_providers()
        return
    
    # List models for a provider if requested
    if args.list_models:
        provider_name = args.provider or config.active_provider
        instance = get_provider_instance(provider_name)
        if instance:
            instance.list_models()
        else:
            print(f"Error: Provider '{provider_name}' not available.")
        return
    
    # Make sure we have a prompt for other operations
    if not args.prompt:
        print("Error: Please provide a prompt or use --list-providers/--list-models.")
        return
    
    # Handle model comparison
    if args.compare:
        try:
            # Parse provider:model pairs
            model_pairs = []
            for pair in args.compare.split(","):
                provider, model = pair.split(":")
                model_pairs.append((provider, model))
            
            # Run comparison
            compare_models_func(args.prompt, model_pairs)
            return
        except Exception as e:
            print(f"Error parsing comparison models: {e}")
            print("Format should be: provider1:model1,provider2:model2")
            return
    
    # Handle single model response
    if args.provider and args.model:
        # User specified both provider and model
        response = get_response(args.prompt, args.provider, args.model, args.temperature, args.max_tokens)
        print(response)
    elif args.provider:
        # User specified provider but not model, auto-select model
        instance = get_provider_instance(args.provider)
        if not instance:
            print(f"Error: Provider '{args.provider}' not available.")
            return
        
        model, reason = instance.choose_model(args.prompt)
        print(f"Auto-selected model: {model}")
        print(f"Reason: {reason}\n")
        
        response = get_response(args.prompt, args.provider, model, args.temperature, args.max_tokens)
        print(response)
    else:
        # User didn't specify provider or model, auto-select both
        provider, model, reason = choose_provider_and_model(args.prompt)
        print(f"Auto-selected provider: {provider}, model: {model}")
        print(f"Reason: {reason}\n")
        
        response = get_response(args.prompt, provider, model, args.temperature, args.max_tokens)
        print(response)

# We use get_response from utils.py instead

# We use choose_provider_and_model from utils.py instead

def list_available_models(provider_name: Optional[str] = None):
    """
    Display all available models for the specified provider(s).
    For use as a Python API.
    
    Args:
        provider_name: Name of the provider, or None for all enabled providers
    """
    if provider_name:
        # List models for specific provider
        provider = get_provider_instance(provider_name)
        if provider:
            provider.list_models()
        else:
            print(f"Error: Provider '{provider_name}' not available.")
    else:
        # List models for all enabled providers
        enabled = config.get_enabled_providers()
        for provider_name in enabled:
            provider = get_provider_instance(provider_name)
            if provider and provider.validate_api_key():
                provider.list_models()
                print()

if __name__ == "__main__":
    main()