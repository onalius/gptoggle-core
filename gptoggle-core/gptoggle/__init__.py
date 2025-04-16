"""
GPToggle: A multi-provider AI model wrapper with auto-model selection and comparison capabilities.
"""

__version__ = "0.2.0"

from .chat import get_response, list_available_models, choose_provider_and_model
from .compare import compare_models
from .config import Config, ProviderConfig
from .providers import PROVIDERS, DEFAULT_PROVIDER

__all__ = [
    "get_response",
    "list_available_models",
    "choose_provider_and_model",
    "compare_models",
    "Config",
    "ProviderConfig",
    "PROVIDERS",
    "DEFAULT_PROVIDER",
]