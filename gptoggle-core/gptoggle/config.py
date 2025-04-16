"""
Configuration settings for the AI model toggle system.

This module provides configuration options for the GPToggle system, including:
- Provider-specific settings (API keys, temperature, etc.)
- Global configuration (active providers, default provider, etc.)
- Customization options for enabled providers and their priority
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
    
    # Provider management
    enabled_providers: List[str] = field(default_factory=list)
    provider_priority: List[str] = field(default_factory=list)
    
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
        
        # Google Gemini
        self.providers["gemini"] = ProviderConfig(
            api_key=os.environ.get("GOOGLE_API_KEY", "")
        )
        
        # X AI (xAI) Grok
        self.providers["grok"] = ProviderConfig(
            api_key=os.environ.get("XAI_API_KEY", "")
        )
        
        # Default to all providers enabled
        self.enabled_providers = list(self.providers.keys())
        
        # Default priority (can be customized by users)
        self.provider_priority = list(self.providers.keys())
    
    def get_provider_config(self, provider: Optional[str] = None) -> ProviderConfig:
        """Get configuration for the specified provider."""
        provider = provider or self.active_provider
        return self.providers.get(provider, ProviderConfig())
    
    def set_active_provider(self, provider: str) -> bool:
        """Set the active provider."""
        if provider in self.providers and provider in self.enabled_providers:
            self.active_provider = provider
            return True
        return False
    
    def enable_provider(self, provider: str) -> bool:
        """
        Enable a specific provider.
        
        Args:
            provider: The provider name to enable
            
        Returns:
            True if successful, False if provider doesn't exist
        """
        if provider in self.providers and provider not in self.enabled_providers:
            self.enabled_providers.append(provider)
            return True
        return False
    
    def disable_provider(self, provider: str) -> bool:
        """
        Disable a specific provider.
        
        Args:
            provider: The provider name to disable
            
        Returns:
            True if successful, False if provider doesn't exist or is already disabled
        """
        if provider in self.enabled_providers:
            self.enabled_providers.remove(provider)
            # If we disabled the active provider, switch to the first available one
            if provider == self.active_provider and self.enabled_providers:
                self.active_provider = self.enabled_providers[0]
            return True
        return False
    
    def get_enabled_providers(self) -> List[str]:
        """
        Get a list of all enabled providers.
        
        Returns:
            List of enabled provider names
        """
        return self.enabled_providers
    
    def set_provider_priority(self, priority_list: List[str]) -> bool:
        """
        Set the priority order for providers when auto-selecting.
        
        Args:
            priority_list: List of provider names in priority order (highest first)
            
        Returns:
            True if successful, False if any provider in the list doesn't exist
        """
        # Check all providers exist
        if not all(p in self.providers for p in priority_list):
            return False
            
        # Check all enabled providers are included
        missing_providers = [p for p in self.enabled_providers if p not in priority_list]
        
        # Update priority list, adding any enabled providers that were missing at the end
        self.provider_priority = priority_list + missing_providers
        return True
    
    def get_provider_priority(self) -> List[str]:
        """
        Get the current provider priority list.
        
        Returns:
            List of provider names in priority order
        """
        # Filter out any disabled providers
        return [p for p in self.provider_priority if p in self.enabled_providers]

# Create a global config instance
config = Config()