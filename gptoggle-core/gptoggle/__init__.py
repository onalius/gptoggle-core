"""
GPToggle - Multi-Provider AI Model Wrapper

This package provides a comprehensive wrapper for multiple AI providers:
- OpenAI (GPT models)
- Anthropic Claude
- Google Gemini
- xAI Grok

It includes features for automatic model selection, task-specific recommendations,
and follow-up task suggestions.

Example usage:
    >>> from gptoggle import get_response
    >>> response = get_response("What is quantum computing?")
    
    >>> # Get task-specific recommendations
    >>> from gptoggle import get_task_recommendations
    >>> recommendations = get_task_recommendations("Design a marketing campaign and code a landing page")
    >>> print(recommendations)
    
    >>> # Get follow-up task suggestions
    >>> from gptoggle import get_followup_recommendations
    >>> followups = get_followup_recommendations(recommendations["task_recommendations"])
    >>> print(followups)
"""

__version__ = "1.0.3"
__author__ = "GPToggle Team"
__email__ = "lano@docdel.io"
__license__ = "MIT"
__description__ = "Multi-provider AI model wrapper with intelligent model selection"
__url__ = "https://github.com/onalius/gptoggle-core"

# Import main functionality from enhanced module
from gptoggle_enhanced import (
    get_response,
    recommend_model,
    get_task_recommendations,
    get_followup_recommendations,
    generate_model_suggestions,
    get_available_providers
)

# Legacy compatibility
from gptoggle_minimal import (
    openai_get_response,
    claude_get_response,
    gemini_get_response,
    grok_get_response
)

# Expose key functionality at the package level
__all__ = [
    "get_response",
    "recommend_model",
    "get_task_recommendations",
    "get_followup_recommendations",
    "generate_model_suggestions",
    "get_available_providers",
    "openai_get_response",
    "claude_get_response",
    "gemini_get_response",
    "grok_get_response"
]