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
"""

__version__ = "1.0.3"

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