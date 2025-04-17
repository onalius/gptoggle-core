#!/usr/bin/env python3
"""
GPToggle Minimal - Standalone version of core GPToggle functionality

This standalone file provides the core functionality of GPToggle without requiring
installation. It includes the intelligent model selection and basic API access for
multiple providers (OpenAI, Claude, Gemini, Grok).

Usage:
    # Download this file and use directly
    from gptoggle_minimal import get_response, recommend_model

    # Get a response using auto-selected model
    response = get_response("What is quantum computing?")
    
    # Get a recommendation for a specific prompt
    provider, model = recommend_model("Generate a Python function for sorting")
    print(f"Recommended model: {provider}:{model}")
"""

import os
import re
import sys
from typing import Dict, List, Optional, Tuple, Union, Any

# Version information
__version__ = "1.0.1"

#################################################
# Configuration
#################################################

# Provider priority for auto-selection (in descending order)
PROVIDER_PRIORITY = ["openai", "claude", "gemini", "grok"]

# Model mappings for each provider
MODELS = {
    "openai": {
        "default": "gpt-3.5-turbo",
        "advanced": "gpt-4o",
        "vision": "gpt-4o"
    },
    "claude": {
        "default": "claude-3-sonnet-20240229",
        "advanced": "claude-3-opus-20240229",
        "vision": "claude-3-opus-20240229"
    },
    "gemini": {
        "default": "gemini-pro",
        "advanced": "gemini-1.5-pro",
        "vision": "gemini-pro-vision"
    },
    "grok": {
        "default": "grok-beta",
        "advanced": "grok-2-1212",
        "vision": "grok-2-vision-1212"
    }
}

# API key environment variables
API_KEY_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "grok": "XAI_API_KEY"
}

# Default generation parameters
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 1000
}

#################################################
# Auto-Triage Functions
#################################################

def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    return len(text.split())

def contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if the text contains any of the specified keywords."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in the text.
    A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
    """
    return len(text) // 4

def recommend_model(prompt: str) -> Tuple[str, str]:
    """
    Recommend the appropriate provider and model based on the prompt characteristics.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        A tuple of (provider_name, model_name)
    """
    # Get available providers
    available_providers = get_available_providers()
    
    if not available_providers:
        raise ValueError("No API keys set for any supported providers. Please set at least one API key.")
    
    # Features to check
    token_count = estimate_tokens(prompt)
    word_count = count_words(prompt)
    
    # Vision/image keywords
    vision_keywords = [
        "image", "picture", "photo", "diagram", "graph", "chart", 
        "screenshot", "analyze this", "what's in this", "look at"
    ]
    
    # Code-related keywords
    code_keywords = [
        "code", "function", "algorithm", "programming", "python", "javascript",
        "java", "c++", "html", "css", "api", "database", "sql", "debug",
        "error", "bug", "fix", "implement", "class", "object", "method"
    ]
    
    # Creative tasks
    creative_keywords = [
        "create", "generate", "write", "draft", "compose", "story", "poem",
        "creative", "fiction", "imagine", "design", "innovative", "novel", "unique"
    ]
    
    # Check for specific requirements
    needs_vision = contains_keywords(prompt, vision_keywords)
    needs_coding = contains_keywords(prompt, code_keywords)
    needs_creativity = contains_keywords(prompt, creative_keywords)
    needs_advanced = token_count > 2000 or word_count > 500 or needs_coding
    
    # Provider selection based on capabilities and priority
    for provider_name in PROVIDER_PRIORITY:
        if provider_name not in available_providers:
            continue
            
        # Select model based on requirements
        if needs_vision:
            return provider_name, MODELS[provider_name]["vision"]
        elif needs_advanced:
            return provider_name, MODELS[provider_name]["advanced"]
        else:
            return provider_name, MODELS[provider_name]["default"]
    
    # Fallback to first available provider with default model
    provider_name = available_providers[0]
    return provider_name, MODELS[provider_name]["default"]

#################################################
# Provider API Functions
#################################################

def get_available_providers() -> List[str]:
    """Get a list of available providers based on API keys."""
    available = []
    for provider, env_var in API_KEY_ENV_VARS.items():
        if os.environ.get(env_var):
            available.append(provider)
    return available

def get_response(
    prompt: str, 
    provider_name: Optional[str] = None, 
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Get a response from the specified provider and model.
    
    Args:
        prompt: The user's prompt
        provider_name: The provider to use (auto-selected if None)
        model_name: The model to use (auto-selected if None)
        temperature: Temperature setting (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        The model's response text
    """
    # Auto-select provider and model if not specified
    if not provider_name or not model_name:
        provider_name, model_name = recommend_model(prompt)
    
    # Check if API key is available
    env_var = API_KEY_ENV_VARS.get(provider_name)
    if not env_var or not os.environ.get(env_var):
        raise ValueError(f"API key for {provider_name} not found. Please set {env_var} environment variable.")
    
    # Call the appropriate provider function
    if provider_name == "openai":
        return openai_get_response(prompt, model_name, temperature, max_tokens)
    elif provider_name == "claude":
        return claude_get_response(prompt, model_name, temperature, max_tokens)
    elif provider_name == "gemini":
        return gemini_get_response(prompt, model_name, temperature, max_tokens)
    elif provider_name == "grok":
        return grok_get_response(prompt, model_name, temperature, max_tokens)
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")

def openai_get_response(
    prompt: str, 
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the OpenAI API."""
    try:
        import openai
        
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except ImportError:
        raise ImportError("OpenAI package not installed. Install with: pip install openai")
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")

def claude_get_response(
    prompt: str, 
    model: str = "claude-3-sonnet-20240229",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the Anthropic Claude API."""
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except ImportError:
        raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
    except Exception as e:
        raise Exception(f"Error calling Claude API: {str(e)}")

def gemini_get_response(
    prompt: str, 
    model: str = "gemini-pro",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the Google Gemini API."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model_obj = genai.GenerativeModel(model_name=model)
        response = model_obj.generate_content(
            prompt,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
        )
        return response.text
    except ImportError:
        raise ImportError("Google Generative AI package not installed. Install with: pip install google-generativeai")
    except Exception as e:
        raise Exception(f"Error calling Gemini API: {str(e)}")

def grok_get_response(
    prompt: str, 
    model: str = "grok-beta",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the xAI Grok API."""
    try:
        import openai
        
        client = openai.OpenAI(
            base_url="https://api.x.ai/v1", 
            api_key=os.environ.get("XAI_API_KEY")
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except ImportError:
        raise ImportError("OpenAI package not installed. Install with: pip install openai")
    except Exception as e:
        raise Exception(f"Error calling Grok API: {str(e)}")

#################################################
# Main Execution
#################################################

if __name__ == "__main__":
    """Simple CLI interface when run directly."""
    if len(sys.argv) < 2:
        print(f"GPToggle Minimal v{__version__}")
        print("Usage: python gptoggle_minimal.py 'Your prompt here'")
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    provider, model = recommend_model(user_prompt)
    print(f"Using {provider}:{model}")
    
    try:
        response = get_response(user_prompt, provider, model)
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)