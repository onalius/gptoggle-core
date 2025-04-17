# GPToggle

A sophisticated Python library for intelligent AI API interactions, designed to simplify and enhance AI-powered conversations through dynamic model selection and provider management.

## Features

- **Multi-Provider Support**: Interact with multiple AI providers through a unified interface
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Google (Gemini)
  - xAI (Grok)
  
- **Intelligent Model Selection**: Automatically selects the most appropriate model based on:
  - Prompt length and complexity
  - Content type (code, creative writing, general questions)
  - Visual content requirements
  - Required context window size
  
- **Model Comparison**: Compare responses from different models side by side and collect user ratings

- **Customizable Provider Management**:
  - Enable/disable specific providers
  - Set provider priority for auto-selection
  - Configure provider-specific settings

## Installation

```bash
pip install gptoggle
```

Or for development:

```bash
git clone https://github.com/onalius/gptoggle-core.git
cd gptoggle-core
pip install -e .
```

## Getting Started

### API Keys

You need to set API keys for the providers you want to use:

```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-key"

# For Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"

# For Google Gemini
export GOOGLE_API_KEY="your-google-key"

# For xAI Grok
export XAI_API_KEY="your-xai-key"
```

### CLI Usage

```bash
# Basic usage with auto-provider and model selection
gptoggle "Tell me about quantum computing"

# Specify provider and model
gptoggle "Tell me about quantum computing" --provider openai --model gpt-4o

# Compare models from different providers
gptoggle "Tell me about quantum computing" --compare openai:gpt-4o,claude:claude-3-opus-20240229

# List available providers
gptoggle --list-providers

# List available models for a specific provider
gptoggle --list-models --provider openai
```

### Python API Usage

```python
from gptoggle import Config, get_response, choose_provider_and_model

# Auto-select provider and model
provider, model, reason = choose_provider_and_model("Write a Python function to calculate Fibonacci numbers")
print(f"Selected {provider}:{model} because: {reason}")

# Get response from a specific provider and model
response = get_response(
    prompt="Explain quantum computing like I'm five",
    provider_name="claude",
    model="claude-3-opus-20240229"
)
print(response)

# Customize provider configuration
config = Config()
config.enable_provider("openai")
config.enable_provider("claude")
config.disable_provider("gemini")
config.set_provider_priority(["claude", "openai"])
```

## Provider Customization

You can customize which providers are enabled and their priority order:

```python
from gptoggle import Config

config = Config()

# Enable only certain providers
config.disable_provider("openai")
config.disable_provider("grok")

# Set provider priority (highest first)
config.set_provider_priority(["claude", "gemini"])

# Set active provider for direct calls
config.set_active_provider("claude")
```

## Model Auto-Selection

GPToggle can intelligently select models based on prompt characteristics:

- Long context (>10K tokens) → Models with large context windows
- Code-related content → Models with strong coding abilities
- Creative writing → Models with strong creative capabilities
- Image analysis → Models with vision capabilities
- Short, simple queries → Faster, more efficient models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, contact lano@docdel.io.