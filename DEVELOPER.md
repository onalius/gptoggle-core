# GPToggle Developer Guide

This document provides detailed information for developers working with the GPToggle library, including architecture details, customization options, and best practices.

## Architecture Overview

The GPToggle project is organized into two main components:

1. **gptoggle-core**: The core library containing the provider implementations and base functionality
2. **gptoggle**: The complete application with CLI and web interfaces

### Core Components

- **Base Provider System**: Abstract base class defining the interface all providers must implement
- **Provider Registry**: Dynamic provider discovery and initialization
- **Configuration System**: Provider settings, API key management, and preferences
- **Triage System**: Intelligent model selection based on prompt analysis
- **Comparison System**: Tools for comparing responses from different models
- **Utilities**: Shared functionality to prevent circular imports

## Project Organization

```
gptoggle/
├── __init__.py            # Package exports
├── config.py              # Configuration management
├── utils.py               # Utility functions to avoid circular imports
├── chat.py                # CLI functionality
├── compare.py             # Model comparison functionality
├── providers/             # Provider implementations
│   ├── __init__.py        # Provider registry
│   ├── base_provider.py   # Abstract base class for providers
│   ├── openai_provider.py # OpenAI provider implementation
│   ├── claude_provider.py # Anthropic Claude provider
│   ├── gemini_provider.py # Google Gemini provider
│   └── grok_provider.py   # xAI Grok provider
└── triage.py              # Auto-selection logic

tests/                     # Test suite
├── __init__.py
├── test_config.py
└── test_triage.py

main.py                    # Flask web interface
static/                    # Web assets
templates/                 # HTML templates
```

## Module Dependencies

GPToggle is designed to minimize circular dependencies through careful module organization:

- `utils.py`: Contains shared functionality that would otherwise create circular imports
- `providers/__init__.py`: Centralizes provider registration and discovery
- `config.py`: Manages configuration without depending on provider implementations
- `__init__.py`: Exposes a clean public API while hiding implementation details

## Adding a New Provider

To add a new provider to GPToggle:

1. Create a new file in the `providers/` directory (e.g., `new_provider.py`)
2. Implement the BaseProvider interface:

```python
from typing import List, Dict, Any, Tuple
from gptoggle.providers.base_provider import BaseProvider

class NewProvider(BaseProvider):
    """Provider implementation for New AI Service."""
    
    def __init__(self):
        # Initialize client with API key
        self.client = None
        api_key = os.environ.get("NEW_PROVIDER_API_KEY", "")
        if api_key:
            self.client = NewProviderClient(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "new_provider"
    
    @property
    def available_models(self) -> List[str]:
        return ["model-1", "model-2", "vision-model"]
    
    @property
    def default_model(self) -> str:
        return "model-1"
    
    @property
    def model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        return {
            "model-1": {
                "context_window": 128000,
                "support_functions": True,
                "support_vision": False,
                "token_limit": 128000,
                "description": "Latest general purpose model"
            },
            "model-2": {
                "context_window": 32000,
                "support_functions": False,
                "support_vision": False,
                "token_limit": 32000,
                "description": "Faster and more efficient model"
            },
            "vision-model": {
                "context_window": 16000,
                "support_functions": False,
                "support_vision": True,
                "token_limit": 16000,
                "description": "Model with image understanding capabilities"
            }
        }
    
    def validate_api_key(self) -> bool:
        api_key = os.environ.get("NEW_PROVIDER_API_KEY")
        if not api_key:
            print("Error: NEW_PROVIDER_API_KEY environment variable not set.")
            return False
        return True
    
    def get_response(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        # Implementation for getting responses from this provider
        pass
    
    def choose_model(self, prompt: str) -> Tuple[str, str]:
        # Logic for selecting the best model for this provider based on the prompt
        pass
    
    def list_models(self) -> None:
        # Display available models for this provider
        pass
```

3. Register the provider in `providers/__init__.py`:

```python
# Add import
from gptoggle.providers.new_provider import NewProvider

def get_provider_class(provider_name: str):
    """Get the provider class by name."""
    provider_map = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "gemini": GeminiProvider,
        "grok": GrokProvider,
        "new_provider": NewProvider,  # Add the new provider here
    }
    return provider_map.get(provider_name)

def get_available_providers():
    """Get a list of all available provider names."""
    return ["openai", "claude", "gemini", "grok", "new_provider"]  # Add the new provider here
```

4. Update documentation to include the new provider's API key environment variable.

## Testing

Run tests using pytest:

```bash
pytest
```

Create specific tests for your new provider in the tests directory.

## Web Interface Customization

The Flask web interface in `main.py` can be customized with:

- Additional routes for provider-specific features
- UI enhancements in the templates directory
- New static assets

## CI/CD Considerations

When setting up CI/CD for GPToggle:

1. Ensure all API keys are available as environment variables in your CI environment (use secrets)
2. Run tests against all supported providers
3. Consider using provider mocks for faster testing

## Best Practices

1. **API Keys**: Never hardcode API keys; always use environment variables
2. **Error Handling**: Provide meaningful error messages when a provider is unavailable
3. **Backward Compatibility**: Maintain API compatibility when updating providers
4. **Documentation**: Keep provider capabilities and model lists up to date

## License

GPToggle is licensed under the MIT license. Your contributions should comply with this license.