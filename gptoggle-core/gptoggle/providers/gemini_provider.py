"""
Google Vertex AI Gemini provider implementation.
"""

import os
import sys
from typing import List, Dict, Any, Tuple

import google.generativeai as genai
from ..providers.base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    """Provider implementation for Google's Gemini models."""

    def __init__(self):
        # Initialize the Gemini client with API key
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)

    def name(self) -> str:
        return "gemini"

    def available_models(self) -> List[str]:
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro-vision",
            "gemini-pro",
        ]

    def default_model(self) -> str:
        return "gemini-1.5-pro"

    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "gemini-1.5-pro": {
                "context_window": 1000000,  # 1M tokens
                "support_functions": True,
                "max_output_tokens": 8192,
                "supports_vision": True,
                "description": "Google's most advanced multimodal model with 1M token context window",
            },
            "gemini-1.5-flash": {
                "context_window": 1000000,  # 1M tokens
                "support_functions": True,
                "max_output_tokens": 8192,
                "supports_vision": True,
                "description": "Fast and efficient model with 1M token context window",
            },
            "gemini-pro-vision": {
                "context_window": 32768,
                "support_functions": False,
                "max_output_tokens": 2048,
                "supports_vision": True,
                "description": "Vision-specialized model that can process images",
            },
            "gemini-pro": {
                "context_window": 32768,
                "support_functions": True,
                "max_output_tokens": 8192,
                "supports_vision": False,
                "description": "Efficient text-only model with strong reasoning capabilities",
            },
        }

    def validate_api_key(self) -> bool:
        """Check if the Google API key is set."""
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            print("Please set your Google API key using:")
            print("export GOOGLE_API_KEY='your-api-key'")
            return False
        return True

    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified Gemini model."""
        try:
            # Make sure the model is available
            if model not in self.available_models():
                return f"Error: Model '{model}' is not available for the Gemini provider."

            # Initialize the model
            gemini_model = genai.GenerativeModel(model_name=model)
            
            # Generate response
            response = gemini_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating response from Gemini: {str(e)}"

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
        """Select the most appropriate Gemini model based on the prompt."""
        # Default model for most cases
        default_model = self.default_model()
        
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
        
        # Long context handling
        if estimated_tokens > 100000:
            if needs_vision:
                return "gemini-1.5-pro", "Selected for very long input with image processing needs"
            else:
                return "gemini-1.5-flash", "Selected for very long input with high efficiency"
        
        # Image processing needs
        if needs_vision:
            if is_code_related or estimated_tokens > 10000:
                return "gemini-1.5-pro", "Selected for image processing with code analysis or long context"
            else:
                return "gemini-pro-vision", "Selected for image processing tasks"
        
        # Code tasks
        if is_code_related:
            return "gemini-1.5-pro", "Selected for code-related tasks"
        
        # Creative tasks
        if is_creative:
            return "gemini-1.5-pro", "Selected for creative content generation"
        
        # For shorter, simpler queries
        if estimated_tokens < 5000 and not is_code_related and not is_creative:
            return "gemini-pro", "Selected for efficient handling of shorter, standard queries"
        
        # Default for everything else
        return default_model, "Selected as the default high-quality model for general use"

    def list_models(self) -> None:
        """Display all available Gemini models."""
        capabilities = self.model_capabilities()
        print(f"Available models for {self.name()}:")
        
        for model_name in self.available_models():
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