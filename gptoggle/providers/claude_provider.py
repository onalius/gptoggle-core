"""
Anthropic Claude provider implementation.
"""

import os
import json
from typing import List, Dict, Any, Tuple

try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    print("Anthropic package not installed. Install with 'pip install anthropic'")

from gptoggle.providers.base_provider import BaseProvider

class ClaudeProvider(BaseProvider):
    """Provider implementation for Anthropic's Claude models."""
    
    def __init__(self):
        self.client = None
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if api_key:
            self.client = Anthropic(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "claude"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "claude-3-5-sonnet-20241022",  #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2",
        ]
    
    @property
    def default_model(self) -> str:
        return "claude-3-5-sonnet-20241022"  #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    
    @property
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "claude-3-5-sonnet-20241022": {
                "context_window": 200000,  # 200K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Anthropic's newest and most capable model with excellent reasoning, 200K context, and vision",
            },
            "claude-3-opus-20240229": {
                "context_window": 200000,  # 200K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Most powerful Claude model with superior reasoning and intelligence",
            },
            "claude-3-sonnet-20240229": {
                "context_window": 200000,  # 200K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Excellent balance of intelligence and speed",
            },
            "claude-3-haiku-20240307": {
                "context_window": 200000,  # 200K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Fastest and most compact Claude model",
            },
            "claude-2.1": {
                "context_window": 100000,
                "support_functions": False,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Previous generation Claude with strong reasoning",
            },
            "claude-2.0": {
                "context_window": 100000,
                "support_functions": False,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Older Claude model with good reasoning capabilities",
            },
            "claude-instant-1.2": {
                "context_window": 100000,
                "support_functions": False,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Fastest of previous Claude generation",
            },
        }
    
    def validate_api_key(self) -> bool:
        """Check if the Anthropic API key is set."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable not set.")
            print("Please set your Anthropic API key using:")
            print("export ANTHROPIC_API_KEY='your-api-key'")
            return False
        return True
    
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified Claude model."""
        try:
            # Make sure the API key is set
            if not self.validate_api_key():
                return "Error: Anthropic API key not set."
            
            # Reinitialize client if needed
            if not self.client:
                api_key = os.environ.get("ANTHROPIC_API_KEY", "")
                self.client = Anthropic(api_key=api_key)
            
            # Make sure the model is available
            if model not in self.available_models:
                return f"Error: Model '{model}' is not available for the Claude provider."
            
            # Generate response
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating response from Claude: {str(e)}"
    
    def count_words(self, text: str) -> int:
        """Count the number of words in a text string."""
        return len(text.split())
    
    def contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if the text contains any of the specified keywords."""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the text.
        A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
        """
        return len(text) // 4
    
    def choose_model(self, prompt: str) -> Tuple[str, str]:
        """Select the most appropriate Claude model based on the prompt."""
        # Default model for most cases
        default_model = self.default_model
        
        # Estimate token count
        estimated_tokens = self.estimate_tokens(prompt)
        
        # Check for image analysis keywords
        image_keywords = ["image", "picture", "photo", "analyze image", "describe image"]
        needs_vision = self.contains_keywords(prompt, image_keywords)
        
        # Check for code-related keywords
        code_keywords = ["code", "function", "algorithm", "programming", "python", "javascript"]
        is_code_related = self.contains_keywords(prompt, code_keywords)
        
        # Check for creative tasks
        creative_keywords = ["creative", "story", "poem", "write", "generate"]
        is_creative = self.contains_keywords(prompt, creative_keywords)
        
        # Check for complex reasoning
        reasoning_keywords = ["analyze", "explain", "reason", "ethics", "philosophy", "complex"]
        needs_reasoning = self.contains_keywords(prompt, reasoning_keywords)
        
        # For complex reasoning tasks
        if needs_reasoning or is_code_related:
            if estimated_tokens > 10000:
                return "claude-3-opus-20240229", "Selected for complex reasoning with long context"
            else:
                return "claude-3-5-sonnet-20241022", "Selected for complex reasoning tasks"
        
        # For creative tasks
        if is_creative:
            return "claude-3-5-sonnet-20241022", "Selected for creative content generation"
        
        # For image analysis
        if needs_vision:
            return "claude-3-5-sonnet-20241022", "Selected for vision capabilities"
        
        # For very simple, short queries
        if estimated_tokens < 1500 and not is_code_related and not is_creative and not needs_reasoning:
            return "claude-3-haiku-20240307", "Selected for efficiency with shorter, simpler queries"
        
        # Default for everything else
        return default_model, "Selected as the default high-quality model for general use"
    
    def list_models(self) -> None:
        """Display all available Claude models."""
        capabilities = self.model_capabilities
        print(f"Available models for {self.name}:")
        
        for model_name in self.available_models:
            model_info = capabilities.get(model_name, {})
            description = model_info.get("description", "No description available")
            context_window = model_info.get("context_window", "Unknown")
            supports_vision = model_info.get("supports_vision", False)
            
            vision_support = "Yes" if supports_vision else "No"
            
            print(f"- {model_name}")
            print(f"  Description: {description}")
            print(f"  Context window: {context_window} tokens")
            print(f"  Vision support: {vision_support}")
            print()