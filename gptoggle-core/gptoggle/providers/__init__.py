"""
Provider implementations for various AI model services.
"""

from gptoggle.providers.base_provider import BaseProvider
from gptoggle.providers.openai_provider import OpenAIProvider
from gptoggle.providers.claude_provider import ClaudeProvider
from gptoggle.providers.gemini_provider import GeminiProvider
from gptoggle.providers.grok_provider import GrokProvider

# Dictionary mapping provider names to their implementation classes
PROVIDER_REGISTRY = {
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "gemini": GeminiProvider,
    "grok": GrokProvider,
}

def get_provider_class(provider_name: str):
    """Get the provider class by name."""
    return PROVIDER_REGISTRY.get(provider_name)

def get_available_providers():
    """Get a list of all available provider names."""
    return list(PROVIDER_REGISTRY.keys())