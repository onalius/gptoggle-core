"""
Configuration settings and model list for the OpenAI chat wrapper.
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Any

# The model list is based on OpenAI's available models
# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
AVAILABLE_MODELS = [
    "gpt-4o",           # Latest and most capable model
    "gpt-4-turbo",      # GPT-4 Turbo
    "gpt-4",            # Original GPT-4
    "gpt-3.5-turbo",    # Balanced option for most tasks
    "gpt-3.5-turbo-16k" # GPT-3.5 with extended context
]

# Default model to use when auto-triage can't determine
DEFAULT_MODEL = "gpt-3.5-turbo"

# Model capabilities classification
MODEL_CAPABILITIES = {
    "gpt-4o": {
        "max_tokens": 128000,
        "capabilities": ["code", "creative", "reasoning", "long_context"],
        "tier": "premium"
    },
    "gpt-4-turbo": {
        "max_tokens": 128000,
        "capabilities": ["code", "creative", "reasoning", "long_context"],
        "tier": "premium"
    },
    "gpt-4": {
        "max_tokens": 8192,
        "capabilities": ["code", "creative", "reasoning"],
        "tier": "premium"
    },
    "gpt-3.5-turbo": {
        "max_tokens": 4096,
        "capabilities": ["general"],
        "tier": "standard"
    },
    "gpt-3.5-turbo-16k": {
        "max_tokens": 16384,
        "capabilities": ["general", "long_context"],
        "tier": "standard"
    }
}

# Keywords for triaging
CODE_KEYWORDS = [
    'code', 'program', 'function', 'algorithm', 'debug', 
    'programming', 'developer', 'software', 'bug', 'error',
    'syntax', 'compile', 'python', 'javascript', 'java', 
    'c++', 'html', 'css', 'api', 'database', 'sql', 
    'repository', 'git', 'github', 'class', 'interface',
    'implementation', 'tests', 'testing'
]

CREATIVE_KEYWORDS = [
    'story', 'poem', 'creative', 'write', 'novel', 
    'fiction', 'narrative', 'character', 'plot', 'setting',
    'imagine', 'fantasy', 'scene', 'dialogue', 'script',
    'lyrics', 'song', 'art', 'design', 'create', 'invent',
    'generate', 'compose', 'author', 'creative', 'artistic'
]

# API Configuration
@dataclass
class OpenAIConfig:
    api_key: str = os.environ.get("OPENAI_API_KEY", "")
    temperature: float = 0.7
    max_tokens: int = 1000
    max_comparison_tokens: int = 500  # Shorter responses for comparison

# Create a global config instance
openai_config = OpenAIConfig()

# Rating configuration
RATINGS_FILE = "ratings.json"
