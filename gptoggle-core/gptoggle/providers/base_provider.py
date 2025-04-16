"""
Base provider class for AI model service integrations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional

class BaseProvider(ABC):
    """
    Abstract base class that all AI provider implementations must inherit from.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the provider."""
        pass
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """Return a list of available models for this provider."""
        pass
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """Return the default model for this provider."""
        pass
    
    @property
    @abstractmethod
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Return capabilities of each model."""
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """Check if the API key for this provider is set and valid."""
        pass
    
    @abstractmethod
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Get a response from the specified model."""
        pass
    
    @abstractmethod
    def choose_model(self, prompt: str) -> Tuple[str, str]:
        """Select the most appropriate model for this prompt."""
        pass
    
    @abstractmethod
    def list_models(self) -> None:
        """Display available models and their capabilities."""
        pass