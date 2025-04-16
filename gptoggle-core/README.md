# GPToggle Core

GPToggle is a multi-provider AI wrapper with intelligent model selection, comparison, and switching capabilities.

## Features

- **Multi-Provider Support**: Seamlessly switch between OpenAI, Claude, and more (Gemini coming soon)
- **Auto-triage Model Selection**: Automatically selects the most appropriate model based on your prompt
- **Cross-Provider Comparison**: Compare responses from different AI providers and models
- **Command Line Interface**: Use GPToggle directly from the command line
- **Python API**: Import GPToggle into your Python projects

## Installation

### From PyPI (Coming Soon)

```bash
pip install gptoggle
```

### From GitHub

```bash
pip install git+https://github.com/gptoggle/gptoggle-core.git
```

### Development Installation

```bash
git clone https://github.com/gptoggle/gptoggle-core.git
cd gptoggle-core
pip install -e .
```

## Usage

### CLI Usage

#### Set up your API keys

```bash
# Set OpenAI API key
export OPENAI_API_KEY='your-openai-api-key'

# Set Anthropic API key (for Claude)
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

#### Auto-select the best model for your prompt:

```bash
gptoggle "Write a short story about a robot learning to paint"
```

#### Specify a provider and model manually:

```bash
gptoggle "Explain quantum computing in simple terms" --provider openai --model gpt-4o

# Or use Claude
gptoggle "Create a marketing strategy for a new coffee shop" --provider claude --model claude-3-opus-20240229
```

#### Compare responses across providers:

```bash
gptoggle "Solve this coding challenge: implement a function to reverse a linked list" --compare openai:gpt-4o,claude:claude-3-opus-20240229
```

#### List available providers:

```bash
gptoggle --list-providers
```

#### List available models for all providers:

```bash
gptoggle --list-models

# Or for a specific provider
gptoggle --provider claude --list-models
```

### Python API Usage

```python
import os
from gptoggle import get_response, choose_provider_and_model, compare_models, config

# Set your API keys
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"

# Auto-select the best provider and model
provider, model, reason = choose_provider_and_model("Write code to implement a binary search tree in Python")
print(f"Selected provider: {provider}")
print(f"Selected model: {model}")
print(f"Reason: {reason}")

# Get a response from OpenAI
response = get_response("Explain the theory of relativity", provider_name="openai")
print(response)

# Get a response from Claude
response = get_response("Summarize the history of artificial intelligence", provider_name="claude")
print(response)

# Compare models across providers
compare_models(
    "Design a database schema for an e-commerce application", 
    [("openai", "gpt-4o"), ("claude", "claude-3-opus-20240229")]
)
```

### Customizing Providers

GPToggle allows you to easily customize which providers are enabled and their priority for auto-selection:

```python
from gptoggle import config

# Check which providers are enabled
print(config.get_enabled_providers())  # By default, all providers are enabled

# Disable a provider you don't want to use
config.disable_provider("claude")

# Re-enable a provider
config.enable_provider("claude")

# Change the priority order for auto-selection
# This will make Claude the first choice when auto-selecting a provider
config.set_provider_priority(["claude", "openai"])

# Get the current priority order
print(config.get_provider_priority())
```

## How Model Selection Works

GPToggle uses provider-specific triage algorithms to determine the most appropriate model based on:

1. **Prompt Length**: For very long prompts, models with longer context windows are preferred
2. **Code Keywords**: If your prompt contains programming-related keywords, code-optimized models are selected
3. **Creative Content**: For creative tasks like storytelling or content generation, models with better creative capabilities are chosen
4. **General Knowledge**: For standard informational queries, a balanced model is selected

## Provider Support

### OpenAI (Default)
- GPT-4o
- GPT-4 Turbo
- GPT-4
- GPT-3.5 Turbo
- GPT-3.5 Turbo with 16k context

### Anthropic Claude
- Claude 3.5 Sonnet (newest)
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku
- Claude 2.1

### Google Gemini (Coming Soon)
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Gemini 1.0 Pro
- Gemini 1.0

## License

MIT License

## For More Information

Visit [GPToggle.com](https://gptoggle.com) for more information, documentation, and to explore premium features.