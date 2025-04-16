"""
Utility functions for the GPToggle package.
This module contains shared functions to avoid circular imports.
"""

from typing import Dict, List, Optional, Tuple, Any

from gptoggle.config import config
from gptoggle.providers import get_provider_class, get_available_providers

# Cache of provider instances
_provider_instances = {}

def get_provider_instance(provider_name: str):
    """Get provider instance by name."""
    if provider_name not in _provider_instances:
        provider_class = get_provider_class(provider_name)
        if not provider_class:
            return None
        
        # The provider classes handle their own configuration
        _provider_instances[provider_name] = provider_class()
        
    return _provider_instances[provider_name]

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
    priority = config.get_provider_priority()
    enabled = config.get_enabled_providers()
    
    # Filter priority list to only include enabled providers
    available_providers = [p for p in priority if p in enabled]
    
    if not available_providers:
        return "none", "none", "No enabled providers with valid API keys"
    
    # Helper variables to track the best option
    selected_provider = None
    selected_model = None 
    selection_reason = ""
    
    # Check each provider in priority order
    for provider_name in available_providers:
        provider = get_provider_instance(provider_name)
        if not provider or not provider.validate_api_key():
            continue
        
        # Let the provider suggest a model
        model, reason = provider.choose_model(prompt)
        
        # First valid provider becomes our choice
        if not selected_provider:
            selected_provider = provider_name
            selected_model = model
            selection_reason = f"Selected provider '{provider_name}' due to priority order. {reason}"
            break
    
    # Fallback if no valid provider found
    if not selected_provider:
        return "none", "none", "No available providers could process this request"
    
    # Ensure we return strings for all values
    return str(selected_provider), str(selected_model), str(selection_reason)

def get_response(
    prompt: str, 
    provider_name: Optional[str] = None, 
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Get a response from the specified provider and model.
    For use as a Python API.
    
    Args:
        prompt: The user's prompt
        provider_name: The provider to use (e.g., "openai", "claude")
        model: The model to use (specific to provider)
        temperature: Temperature for response generation
        max_tokens: Maximum tokens for the response
        
    Returns:
        The model's response as a string
    """
    # Auto-select provider and model if not specified
    if not provider_name or not model:
        provider_name, model, _ = choose_provider_and_model(prompt)
        
    # Use active provider if none specified
    if not provider_name:
        provider_name = config.active_provider
    
    # Get provider instance
    provider = get_provider_instance(provider_name)
    if not provider:
        return f"Error: Provider '{provider_name}' not available."
    
    # Validate API key
    if not provider.validate_api_key():
        return f"Error: API key not set for provider '{provider_name}'."
    
    # Auto-select model if none specified
    if not model:
        model, reason = provider.choose_model(prompt)
    
    # Generate response
    return provider.get_response(prompt, model, temperature, max_tokens)


def recommend_model(prompt: str) -> str:
    """
    Recommend a model for a given prompt.
    This is an alias for choose_provider_and_model for backward compatibility.
    
    Args:
        prompt: The user's prompt
        
    Returns:
        A string in format "provider:model" representing the recommended model
    """
    provider, model, reason = choose_provider_and_model(prompt)
    return f"{provider}:{model}"