"""
Provider modules for different AI model services.
"""

from ..providers.openai_provider import OpenAIProvider
from ..providers.claude_provider import ClaudeProvider
from ..providers.gemini_provider import GeminiProvider
from ..providers.grok_provider import GrokProvider

# Dictionary mapping provider names to provider classes
PROVIDERS = {
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "gemini": GeminiProvider,
    "grok": GrokProvider
}

# Default provider
DEFAULT_PROVIDER = "openai"