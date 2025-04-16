"""
X AI (xAI) Grok provider implementation.

Note: Grok uses an API that's compatible with the OpenAI client library.
"""

import os
import sys
from typing import List, Dict, Any, Tuple

from openai import OpenAI
from ..providers.base_provider import BaseProvider

class GrokProvider(BaseProvider):
    """Provider implementation for xAI's Grok models."""

    def __init__(self):
        # Initialize the Grok client with API key
        self.client = None
        api_key = os.environ.get("XAI_API_KEY", "")
        if api_key:
            self.client = OpenAI(
                base_url="https://api.x.ai/v1",
                api_key=api_key
            )

    def name(self) -> str:
        return "grok"

    def available_models(self) -> List[str]:
        return [
            "grok-2-1212",
            "grok-2-vision-1212",
            "grok-beta",
            "grok-vision-beta",
        ]

    def default_model(self) -> str:
        return "grok-2-1212"

    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "grok-2-1212": {
                "context_window": 131072,  # 128K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "xAI's latest large language model with 128K context window",
            },
            "grok-2-vision-1212": {
                "context_window": 8192,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Vision-capable version of Grok-2",
            },
            "grok-beta": {
                "context_window": 131072,  # 128K tokens
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": False,
                "description": "Original Grok model with 128K context window",
            },
            "grok-vision-beta": {
                "context_window": 8192,
                "support_functions": True,
                "max_output_tokens": 4096,
                "supports_vision": True,
                "description": "Vision-capable version of the original Grok model",
            },
        }

    def validate_api_key(self) -> bool:
        """Check if the X AI API key is set."""
        api_key = os.environ.get("XAI_API_KEY")
        if not api_key:
            print("Error: XAI_API_KEY environment variable not set.")
            print("Please set your xAI API key using:")
            print("export XAI_API_KEY='your-api-key'")
            return False
        return True

    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified Grok model."""
        try:
            # Make sure the API key is set
            if not self.validate_api_key():
                return "Error: XAI API key not set."
            
            # Reinitialize client if needed
            if not self.client:
                api_key = os.environ.get("XAI_API_KEY", "")
                self.client = OpenAI(
                    base_url="https://api.x.ai/v1",
                    api_key=api_key
                )
            
            # Make sure the model is available
            if model not in self.available_models():
                return f"Error: Model '{model}' is not available for the Grok provider."

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
            return f"Error generating response from Grok: {str(e)}"

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
        """Select the most appropriate Grok model based on the prompt."""
        # Default model for most cases
        default_model = self.default_model()
        
        # Estimate token count
        estimated_tokens = self.estimate_tokens(prompt)
        
        # Check for image analysis keywords
        image_keywords = ["image", "picture", "photo", "analyze image", "describe image"]
        needs_vision = self.contains_keywords(prompt, image_keywords)
        
        # Image processing needs
        if needs_vision:
            return "grok-2-vision-1212", "Selected for image processing capabilities"
        
        # For normal text prompts
        return default_model, "Selected as the default high-quality model for general use"

    def list_models(self) -> None:
        """Display all available Grok models."""
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