"""
Provider modules for different AI model services.
"""

# Import all providers
from .openai_provider import OpenAIProvider
from .claude_provider import ClaudeProvider

# Dictionary mapping provider names to their respective classes
PROVIDERS = {
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    # "gemini": GeminiProvider,  # To be added in the future
}

# Default provider
DEFAULT_PROVIDER = "openai"

__all__ = [
    "OpenAIProvider",
    "ClaudeProvider",
    "PROVIDERS",
    "DEFAULT_PROVIDER",
]