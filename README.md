# GPToggle

GPToggle is a sophisticated multi-provider Python tool for intelligent AI API interactions, designed to simplify and enhance AI-powered conversations through dynamic model selection and user-friendly interfaces.

## Features

- **Multi-Provider Support**: Access models from OpenAI, Anthropic (Claude), Google (Gemini), and xAI (Grok) through a unified interface
- **Intelligent Model Selection**: Automatically choose the best AI model based on your prompt
- **Model Comparison**: Compare responses from different providers and models side-by-side
- **Provider Management**: Enable, disable, and prioritize specific providers
- **CLI & Python API**: Use as a command-line tool or integrate into your Python projects
- **Web Interface**: Interactive web UI for prompt submission and model comparison

## Project Structure

The project is organized into two main components:

### gptoggle-core
The core library containing the provider implementations and base functionality:
- Provider interfaces and implementations
- Configuration management
- Model selection and comparison logic
- Utility functions
- Python API

### gptoggle
The complete application including:
- Command-line interface
- Web interface (Flask)
- Installation utilities
- Documentation

## Installation

```bash
# Install the complete package
pip install gptoggle

# For developers working on the core library
pip install -e .
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

## Web Interface

GPToggle comes with a web interface built on Flask:

```bash
# Start the web server
python -m gptoggle.web

# Or run the main.py directly
python main.py
```

The web interface will be available at http://localhost:5000 by default.

## Developer Guide

### Project Organization

The project follows a modular architecture to ensure maintainability and extensibility:

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

### Adding a New Provider

To add a new provider:

1. Create a new provider class in the `providers/` directory
2. Inherit from `BaseProvider` and implement all required methods
3. Register the provider in `providers/__init__.py`
4. Add any provider-specific environment variables to the documentation

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_config.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT