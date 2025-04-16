# GPToggle

GPToggle is a sophisticated multi-provider Python tool for intelligent AI API interactions, designed to simplify and enhance AI-powered conversations through dynamic model selection and user-friendly interfaces.

## Features

- **Multi-Provider Support**: Access models from OpenAI, Anthropic (Claude), Google (Gemini), and xAI (Grok) through a unified interface
- **Intelligent Model Selection**: Automatically choose the best AI model based on your prompt
- **Model Comparison**: Compare responses from different providers and models side-by-side
- **Provider Management**: Enable, disable, and prioritize specific providers
- **CLI & Python API**: Use as a command-line tool or integrate into your Python projects

## Installation

```bash
pip install gptoggle
```

## Quick Start

```python
import os
from gptoggle import get_response, choose_provider_and_model

# Set up API keys for providers you want to use
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"
os.environ["GOOGLE_API_KEY"] = "your-google-key"
os.environ["XAI_API_KEY"] = "your-xai-key"

# Auto-select the best provider and model for your prompt
provider, model, reason = choose_provider_and_model("Create a Python function to calculate the Fibonacci sequence")
print(f"Selected {provider}:{model} because {reason}")

# Get a response from any provider and model
response = get_response(
    "What are the ethical implications of AI?",
    provider_name="claude",
    model="claude-3-opus-20240229"
)
print(response)
```

## CLI Usage

```bash
# Auto-select provider and model
gptoggle "Explain quantum computing in simple terms"

# Specify provider and model
gptoggle "Write a poem about AI" --provider openai --model gpt-4o

# Compare models from different providers
gptoggle "Debate the pros and cons of remote work" --compare openai:gpt-4o,claude:claude-3-opus-20240229
```

## Configuration

GPToggle uses environment variables for API keys:

- `OPENAI_API_KEY` - For OpenAI provider (GPT models)
- `ANTHROPIC_API_KEY` - For Claude provider
- `GOOGLE_API_KEY` - For Gemini provider
- `XAI_API_KEY` - For Grok provider

## License

MIT