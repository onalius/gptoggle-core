"""
GPToggle: A ChatGPT API wrapper with auto-model selection and comparison capabilities.
"""

__version__ = "0.1.0"

from .chat import get_response, list_available_models
from .compare import compare_models
from .triage import choose_model
from .config import OpenAIConfig, AVAILABLE_MODELS

__all__ = [
    "get_response",
    "list_available_models",
    "compare_models",
    "choose_model",
    "OpenAIConfig",
    "AVAILABLE_MODELS",
]