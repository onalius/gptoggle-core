"""
Configuration settings for the AI model toggle system.
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

# Ratings configuration
RATINGS_FILE = "ratings.json"

@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    api_key: str = ""
    temperature: float = 0.7
    max_tokens: int = 1000
    max_comparison_tokens: int = 500  # Shorter responses for comparison

@dataclass
class Config:
    """Global configuration class."""
    # Provider configurations
    providers: Dict[str, ProviderConfig] = field(default_factory=dict)
    
    # Global settings
    active_provider: str = "openai"  # Default provider
    
    def __post_init__(self):
        """Initialize provider configurations."""
        # OpenAI
        self.providers["openai"] = ProviderConfig(
            api_key=os.environ.get("OPENAI_API_KEY", "")
        )
        
        # Anthropic Claude
        self.providers["claude"] = ProviderConfig(
            api_key=os.environ.get("ANTHROPIC_API_KEY", "")
        )
        
        # Google Gemini (future)
        # self.providers["gemini"] = ProviderConfig(
        #     api_key=os.environ.get("GEMINI_API_KEY", "")
        # )
    
    def get_provider_config(self, provider: Optional[str] = None) -> ProviderConfig:
        """Get configuration for the specified provider."""
        provider = provider or self.active_provider
        return self.providers.get(provider, ProviderConfig())
    
    def set_active_provider(self, provider: str) -> bool:
        """Set the active provider."""
        if provider in self.providers:
            self.active_provider = provider
            return True
        return False

# Create a global config instance
config = Config()