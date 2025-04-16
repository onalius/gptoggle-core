"""
OpenAI provider implementation.
"""
import os
import re
from typing import Dict, List, Any, Tuple

from openai import OpenAI

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

class OpenAIProvider(BaseProvider):
    """Provider implementation for OpenAI's models."""
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def available_models(self) -> List[str]:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        return [
            "gpt-4o",           # Latest and most capable model
            "gpt-4-turbo",      # GPT-4 Turbo
            "gpt-4",            # Original GPT-4
            "gpt-3.5-turbo",    # Balanced option for most tasks
            "gpt-3.5-turbo-16k" # GPT-3.5 with extended context
        ]
    
    @property
    def default_model(self) -> str:
        return "gpt-3.5-turbo"
    
    @property
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
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
    
    def validate_api_key(self) -> bool:
        """Check if the OpenAI API key is set."""
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            print("Please set your OpenAI API key with:")
            print("export OPENAI_API_KEY='your-api-key'")
            return False
        return True
    
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified OpenAI model."""
        if not self.validate_api_key():
            return "Error: API key not set"
            
        api_key = os.environ.get("OPENAI_API_KEY", "")
        client = OpenAI(api_key=api_key)
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
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
        """Select the most appropriate OpenAI model based on the prompt."""
        # Check prompt length
        token_estimate = self.estimate_tokens(prompt)
        word_count = self.count_words(prompt)
        
        # Check for specialized content
        has_code_keywords = self.contains_keywords(prompt, CODE_KEYWORDS)
        has_creative_keywords = self.contains_keywords(prompt, CREATIVE_KEYWORDS)
        
        # Decision logic
        if token_estimate > 4000 or word_count > 1000:
            # For very long prompts, use models with longer context
            if has_code_keywords or has_creative_keywords:
                # If it's complex and code or creative related, use top model
                return ("gpt-4o", "Selected for handling long, complex content with code or creative elements.")
            else:
                # For long but general prompts
                return ("gpt-3.5-turbo-16k", "Selected for handling long general content efficiently.")
        
        # For code-related tasks, prefer more capable models
        if has_code_keywords:
            return ("gpt-4o", "Selected for superior code understanding and generation capabilities.")
        
        # For creative tasks, prefer more capable models
        if has_creative_keywords:
            return ("gpt-4o", "Selected for enhanced creative writing and storytelling abilities.")
        
        # Default to the balanced option
        return (self.default_model, "Selected as the balanced option for general-purpose queries.")
    
    def list_models(self) -> None:
        """Display all available OpenAI models."""
        print("Available OpenAI models:")
        for model in self.available_models:
            capabilities = self.model_capabilities.get(model, {})
            tier = capabilities.get("tier", "unknown")
            max_tokens = capabilities.get("max_tokens", "unknown")
            print(f"- {model} (Tier: {tier}, Max tokens: {max_tokens})")