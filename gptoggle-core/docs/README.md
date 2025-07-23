# GPToggle: Multi-Provider AI Model Wrapper

GPToggle is a comprehensive wrapper for multiple AI providers including OpenAI, Anthropic Claude, Google Gemini, and xAI Grok. It simplifies working with various AI APIs by providing automatic model selection, unified interface, and response comparison.

## Features

- 🤖 **Multi-Provider Support**: Use OpenAI (GPT models), Anthropic Claude, Google Gemini, and xAI Grok with a single interface
- 🔄 **Auto-Model Selection**: Intelligently chooses the best model based on prompt characteristics
- 📊 **Response Comparison**: Compare responses from different models side by side
- 🌐 **Multiple Implementations**: Available as Python package, standalone Python file, or JavaScript library
- 🚀 **Simple Installation**: Multiple installation options for different environments

## Quick Start

### Python Installation

#### Option 1: Install via pip (Recommended)

```bash
pip install gptoggle-core
```

#### Option 2: Standalone File (No Installation)

Download the standalone Python file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_minimal.py -o gptoggle_minimal.py
```

### JavaScript Installation

#### Option 1: Install via npm (For Node.js Projects)

```bash
npm install github:onalius/gptoggle-core
```

#### Option 2: Standalone File (For Any Environment)

Download the standalone JavaScript file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

## Basic Usage

### Python

```python
# With installed package
from gptoggle import get_response

# Or with standalone file
from gptoggle_minimal import get_response

# Auto-select provider and model
response = get_response("Explain quantum computing in simple terms")

# Specify provider and/or model
response = get_response("Write a Python function", provider_name="openai", model_name="gpt-4o")
```

### JavaScript

```javascript
// With npm installation
const { GPToggle } = require('gptoggle-js');

// Or with standalone file
const { GPToggle } = require('./gptoggle.js');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_AI_API_KEY,
  grok: process.env.GROK_API_KEY
};

// Create GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Auto-select model
const response = await gptoggle.getResponse("Explain quantum computing in simple terms");

// Specify provider and model
const response = await gptoggle.getResponse("Write a Python function", "openai", "gpt-4o");
```

## Advanced Usage

### Model Comparison

#### Python

```python
from gptoggle import compare_models

compare_models("Explain quantum computing", ["gpt-4o", "claude-3-opus-20240229"])
```

#### JavaScript

```javascript
const responses = {};
responses.gpt4 = await gptoggle.getResponse("Explain quantum computing", "openai", "gpt-4o");
responses.claude = await gptoggle.getResponse("Explain quantum computing", "claude", "claude-3-opus-20240229");
console.log("GPT-4o:", responses.gpt4);
console.log("Claude:", responses.claude);
```

### Custom Provider Priority

#### Python

```python
import os
from gptoggle import set_provider_priority

# Prioritize Claude over OpenAI
set_provider_priority(["claude", "openai", "gemini", "grok"])
```

#### JavaScript

```javascript
const config = {
  providerPriority: ['claude', 'openai', 'gemini', 'grok']
};

const gptoggle = new GPToggle(config, apiKeys);
```

## Documentation

- [Python Installation](INSTALLATION.md) - Detailed Python installation guide
- [JavaScript Installation](JS_INSTALLATION.md) - Detailed JavaScript installation guide
- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Replit Installation](REPLIT_INSTALLATION.md) - Special instructions for Replit environments

## License

MIT License

## Contact

For questions or support, contact lano@docdel.io