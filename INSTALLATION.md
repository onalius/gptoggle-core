# GPToggle Installation Guide

This guide covers various ways to install GPToggle and troubleshoot common installation issues.

## Standard Installation

The simplest way to install GPToggle is via pip:

```bash
pip install gptoggle-package
```

## Development Installation

For development or to install the latest version directly from GitHub:

```bash
# Clone the repository
git clone https://github.com/yourusername/gptoggle.git
cd gptoggle

# Install in development mode
pip install -e .
```

## Troubleshooting Common Installation Issues

### Self-Dependencies Error

If you encounter an error about self-dependencies when installing from GitHub, use one of these solutions:

1. **Use the package name on PyPI**:
   ```bash
   pip install gptoggle-package
   ```

2. **For development installation**:
   ```bash
   pip install -e . --no-deps
   pip install openai anthropic google-generativeai rich flask
   ```

### Import Errors

If you're getting import errors after installation:

1. Make sure you're importing from the correct package name:
   ```python
   import gptoggle  # Import the package
   from gptoggle import get_response, recommend_model  # Import specific functions
   ```

2. Verify the installation:
   ```bash
   python -c "import gptoggle; print(gptoggle.__version__)"
   ```

### API Key Configuration

GPToggle requires API keys to function properly. Set them as environment variables:

```python
import os

# Set API keys for the providers you want to use
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"
os.environ["GOOGLE_API_KEY"] = "your-google-key"
os.environ["XAI_API_KEY"] = "your-xai-key"
```

## Dependencies

GPToggle depends on the following packages:

- `openai>=1.0.0` - For OpenAI and Grok providers
- `anthropic>=0.5.0` - For Claude provider
- `google-generativeai>=0.3.0` - For Gemini provider
- `rich>=10.0.0` - For terminal formatting
- `flask>=2.0.0` - For web interface

### Optional Dependencies

For development purposes, you can install additional dependencies:

```bash
pip install gptoggle-package[dev]
```

This includes:
- `pytest>=7.0.0`
- `black>=22.0.0`
- `isort>=5.0.0`
- `flake8>=4.0.0`

## Using in a Replit Environment

For Replit environments, you may need to use specific installation strategies:

```bash
# Use the package name specifically for installation
pip install gptoggle-package

# Or install directly from GitHub with specific flags
pip install git+https://github.com/yourusername/gptoggle.git@main#egg=gptoggle-package --no-deps
pip install openai anthropic google-generativeai rich flask
```

## Usage after Installation

After installation, verify that you can import and use the package:

```python
import gptoggle

# Check version
print(gptoggle.__version__)

# Set up API keys
import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"

# Use the recommended model function
model = gptoggle.recommend_model("What is the capital of France?")
print(f"Recommended model: {model}")

# Get a response
response = gptoggle.get_response("What is the capital of France?")
print(response)
```

## Using the CLI

After installation, you should be able to use the `gptoggle` command:

```bash
gptoggle "What is the meaning of life?"
```

## Starting the Web Interface

To use the web interface:

```bash
# Either run the module directly
python -m gptoggle.web

# Or use the main.py script
python main.py
```

## Getting Help

If you continue to experience installation issues, please:

1. Check the [GitHub repository](https://github.com/yourusername/gptoggle) for the latest instructions
2. Open an issue with details about your environment and the specific error
3. Contact the maintainers at lano@docdel.io