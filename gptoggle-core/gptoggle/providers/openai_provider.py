"""
OpenAI provider implementation.
"""

import os
from typing import List, Dict, Any, Tuple

try:
    import openai
    from openai import OpenAI
except ImportError:
    print("OpenAI package not installed. Install with 'pip install openai'")

from gptoggle.providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    """Provider implementation for OpenAI's models."""
    
    def __init__(self):
        # Initialize the OpenAI client if the API key is set
        self.client = None
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            "gpt-4-turbo",
            "gpt-4-vision-preview",
            "gpt-4",
            "gpt-3.5-turbo",
            "dall-e-3",
        ]
    
    @property
    def default_model(self) -> str:
        return "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
    
    @property
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "gpt-4o": {
                "context_window": 128000,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "OpenAI's most powerful and cost-effective model with vision capabilities",
            },
            "gpt-4-turbo": {
                "context_window": 128000,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "More powerful than GPT-3.5, with broad general knowledge and domain expertise",
            },
            "gpt-4-vision-preview": {
                "context_window": 128000,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "GPT-4 with vision capabilities, can analyze and respond to images",
            },
            "gpt-4": {
                "context_window": 8192,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Original GPT-4 model with strong reasoning capabilities",
            },
            "gpt-3.5-turbo": {
                "context_window": 16385,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Fast and cost-effective model for most common use cases",
            },
            "dall-e-3": {
                "context_window": 0,  # No text context window for image generation model
                "support_functions": False,
                "max_output_tokens": 0,  # No text output
                "supports_vision": False,  # Input only
                "description": "Advanced image generation model with high photorealism",
            },
        }
    
    def validate_api_key(self) -> bool:
        """Check if the OpenAI API key is set."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            print("Please set your OpenAI API key using:")
            print("export OPENAI_API_KEY='your-api-key'")
            return False
        return True
    
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified OpenAI model."""
        try:
            # Make sure the API key is set
            if not self.validate_api_key():
                return "Error: OpenAI API key not set."
            
            # Reinitialize client if needed
            if not self.client:
                api_key = os.environ.get("OPENAI_API_KEY", "")
                self.client = OpenAI(api_key=api_key)
            
            # Make sure the model is available
            if model not in self.available_models:
                return f"Error: Model '{model}' is not available for the OpenAI provider."
            
            # Special handling for image generation model
            if model == "dall-e-3":
                return "Error: DALL-E 3 is an image generation model and cannot process text prompts in this interface."
            
            # Generate response
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response from OpenAI: {str(e)}"
    
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
        """Select the most appropriate OpenAI model based on the prompt."""
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
        
        # Check for long inputs that require a large context window
        if estimated_tokens > 7000:
            if needs_vision:
                return "gpt-4o", "Selected for vision capabilities and large context window"
            return "gpt-4-turbo", "Selected for large context window"
        
        # For image analysis
        if needs_vision:
            return "gpt-4o", "Selected for vision capabilities"
        
        # For code-heavy prompts
        if is_code_related:
            return "gpt-4o", "Selected for code-related tasks"
        
        # For creative tasks
        if is_creative and estimated_tokens > 1500:
            return "gpt-4o", "Selected for creative tasks with medium complexity"
        
        # For simple, shorter requests
        if not is_code_related and not is_creative and estimated_tokens < 1500:
            return "gpt-3.5-turbo", "Selected for efficiency with shorter, simpler queries"
        
        # Default for everything else
        return default_model, "Selected as the default high-quality model for general use"
    
    def list_models(self) -> None:
        """Display all available OpenAI models."""
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