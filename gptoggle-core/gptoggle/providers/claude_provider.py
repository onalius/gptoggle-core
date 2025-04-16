"""
Anthropic Claude provider implementation.
"""
import os
import re
from typing import Dict, List, Any, Tuple

import anthropic
from anthropic import Anthropic

from .base_provider import BaseProvider

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

class ClaudeProvider(BaseProvider):
    """Provider implementation for Anthropic's Claude models."""
    
    @property
    def name(self) -> str:
        return "claude"
    
    @property
    def available_models(self) -> List[str]:
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024.
        # do not change this unless explicitly requested by the user
        return [
            "claude-3-5-sonnet-20241022",  # Latest and most capable model
            "claude-3-opus-20240229",      # Strongest reasoning and writing
            "claude-3-sonnet-20240229",    # Balanced performance and cost
            "claude-3-haiku-20240307",     # Fastest model
            "claude-2.1"                   # Legacy model
        ]
    
    @property
    def default_model(self) -> str:
        return "claude-3-sonnet-20240229"
    
    @property
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "claude-3-5-sonnet-20241022": {
                "max_tokens": 200000,
                "capabilities": ["code", "creative", "reasoning", "long_context", "vision"],
                "tier": "premium"
            },
            "claude-3-opus-20240229": {
                "max_tokens": 200000,
                "capabilities": ["code", "creative", "reasoning", "long_context", "vision"],
                "tier": "premium"
            },
            "claude-3-sonnet-20240229": {
                "max_tokens": 200000,
                "capabilities": ["code", "creative", "reasoning", "long_context", "vision"],
                "tier": "standard"
            },
            "claude-3-haiku-20240307": {
                "max_tokens": 200000,
                "capabilities": ["general", "fast", "vision"],
                "tier": "economy"
            },
            "claude-2.1": {
                "max_tokens": 100000,
                "capabilities": ["general", "long_context"],
                "tier": "legacy"
            }
        }
    
    def validate_api_key(self) -> bool:
        """Check if the Anthropic API key is set."""
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable is not set.")
            print("Please set your Anthropic API key with:")
            print("export ANTHROPIC_API_KEY='your-api-key'")
            return False
        return True
    
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified Claude model."""
        if not self.validate_api_key():
            return "Error: API key not set"
            
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        client = Anthropic(api_key=api_key)
        
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def count_words(self, text: str) -> int:
        """Count the number of words in a text string."""
        return len(text.split())
    
    def contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if the text contains any of the specified keywords."""
        text_lower = text.lower()
        for keyword in keywords:
            # Use word boundaries to match whole words
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                return True
        return False
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the text.
        A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
        """
        return len(text) // 4  # Simple character-based estimation
    
    def choose_model(self, prompt: str) -> Tuple[str, str]:
        """Select the most appropriate Claude model based on the prompt."""
        # Check prompt length
        token_estimate = self.estimate_tokens(prompt)
        word_count = self.count_words(prompt)
        
        # Check for specialized content
        has_code_keywords = self.contains_keywords(prompt, CODE_KEYWORDS)
        has_creative_keywords = self.contains_keywords(prompt, CREATIVE_KEYWORDS)
        
        # Decision logic for Claude models
        if token_estimate > 50000 or word_count > 12500:
            # All Claude 3 models handle up to 200k tokens, but use the most powerful
            # for very long contexts to ensure high quality responses
            return ("claude-3-opus-20240229", "Selected for handling extremely long content with high quality.")
            
        # For code tasks, prefer Opus for best reasoning capabilities
        if has_code_keywords:
            return ("claude-3-opus-20240229", "Selected for superior code understanding and reasoning abilities.")
        
        # For creative tasks, Sonnet offers a good balance of creativity and efficiency
        if has_creative_keywords:
            return ("claude-3-sonnet-20240229", "Selected for strong creative writing capabilities at optimal cost.")
        
        # For shorter, simpler queries, Haiku is the fastest option
        if token_estimate < 2000 and not (has_code_keywords or has_creative_keywords):
            return ("claude-3-haiku-20240307", "Selected for fast responses to simple queries.")
        
        # Default to Sonnet for balanced performance
        return (self.default_model, "Selected as the balanced option for general-purpose queries.")
    
    def list_models(self) -> None:
        """Display all available Claude models."""
        print("Available Claude models:")
        for model in self.available_models:
            capabilities = self.model_capabilities.get(model, {})
            tier = capabilities.get("tier", "unknown")
            max_tokens = capabilities.get("max_tokens", "unknown")
            print(f"- {model} (Tier: {tier}, Max tokens: {max_tokens})")