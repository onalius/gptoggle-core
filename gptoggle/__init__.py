"""
GPToggle: A multi-provider AI model wrapper with auto-model selection and comparison capabilities.
"""

# Version information (MAJOR.MINOR.PATCH) following Semantic Versioning 2.0.0
# MAJOR: Incompatible API changes
# MINOR: Functionality added in a backward compatible manner
# PATCH: Backward compatible bug fixes
__version__ = "1.0.0"  # Major update with multi-provider architecture

# Core functionality
from gptoggle.config import Config, config
from gptoggle.utils import get_response, choose_provider_and_model, get_provider_instance
from gptoggle.chat import list_available_models
from gptoggle.compare import compare_models

# Import provider classes for direct access if needed
from gptoggle.providers.base_provider import BaseProvider
from gptoggle.providers.openai_provider import OpenAIProvider
from gptoggle.providers.claude_provider import ClaudeProvider
from gptoggle.providers.gemini_provider import GeminiProvider
from gptoggle.providers.grok_provider import GrokProvider