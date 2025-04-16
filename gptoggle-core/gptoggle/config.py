"""
Configuration settings for the AI model toggle system.

This module provides configuration options for the GPToggle system, including:
- Provider-specific settings (API keys, temperature, etc.)
- Global configuration (active providers, default provider, etc.)
- Customization options for enabled providers and their priority
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

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
    
    # Active provider for direct calls without provider specification
    active_provider: str = "openai"  # Default provider
    
    # List of enabled providers and their priority order
    enabled_providers: List[str] = field(default_factory=list)
    provider_priority: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize provider configurations."""
        # Initialize configurations for all known providers
        self.providers = {
            "openai": ProviderConfig(api_key=os.environ.get("OPENAI_API_KEY", "")),
            "claude": ProviderConfig(api_key=os.environ.get("ANTHROPIC_API_KEY", "")),
            "gemini": ProviderConfig(api_key=os.environ.get("GOOGLE_API_KEY", "")),
            "grok": ProviderConfig(api_key=os.environ.get("XAI_API_KEY", "")),
        }
        
        # Enable providers that have API keys set
        self.enabled_providers = []
        for provider_name, config in self.providers.items():
            if config.api_key:
                self.enabled_providers.append(provider_name)
        
        # Set default priority order based on general capability/cost balance
        self.provider_priority = ["openai", "claude", "gemini", "grok"]
    
    def get_provider_config(self, provider: Optional[str] = None) -> ProviderConfig:
        """Get configuration for the specified provider."""
        provider_name = provider or self.active_provider
        return self.providers.get(provider_name, ProviderConfig())
    
    def set_active_provider(self, provider: str) -> bool:
        """Set the active provider."""
        if provider in self.providers:
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
        if provider in self.providers and provider in self.enabled_providers:
            self.enabled_providers.remove(provider)
            return True
        return False
    
    def get_enabled_providers(self) -> List[str]:
        """
        Get a list of all enabled providers.
        
        Returns:
            List of enabled provider names
        """
        return self.enabled_providers.copy()
    
    def set_provider_priority(self, priority_list: List[str]) -> bool:
        """
        Set the priority order for providers when auto-selecting.
        
        Args:
            priority_list: List of provider names in priority order (highest first)
            
        Returns:
            True if successful, False if any provider in the list doesn't exist
        """
        # Validate all providers in the list
        if not all(p in self.providers for p in priority_list):
            return False
        
        self.provider_priority = priority_list
        return True
    
    def get_provider_priority(self) -> List[str]:
        """
        Get the current provider priority list.
        
        Returns:
            List of provider names in priority order
        """
        return self.provider_priority.copy()

# Global configuration instance
config = Config()