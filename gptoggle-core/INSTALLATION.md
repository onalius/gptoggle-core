# GPToggle Installation Guide

This guide covers the various ways to install and use GPToggle in different environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Python Installation](#python-installation)
  - [Option 1: Install via pip](#option-1-install-via-pip)
  - [Option 2: Install from source](#option-2-install-from-source)
  - [Option 3: Use standalone files](#option-3-use-standalone-files)
- [JavaScript Installation](#javascript-installation)
  - [Option 1: Install via npm](#option-1-install-via-npm)
  - [Option 2: Use standalone JavaScript files](#option-2-use-standalone-javascript-files)
  - [Option 3: Browser Usage](#option-3-browser-usage)
- [Replit Environment](#replit-environment)
- [API Keys Setup](#api-keys-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

GPToggle requires:

- **Python**: Python 3.8 or higher
- **JavaScript**: Node.js 14.x or higher (for JavaScript usage)

You'll also need API keys for the providers you want to use:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic Claude: https://console.anthropic.com/
- Google Gemini: https://ai.google.dev/
- xAI Grok: https://x.ai/

## Python Installation

### Option 1: Install via pip

The recommended way to install GPToggle is via pip:

```bash
pip install gptoggle-core
```

After installation, you can import and use the package:

```python
from gptoggle import get_response, recommend_model

# Get a response using auto-selected model
response = get_response("What is quantum computing?")
print(response)
```

### Option 2: Install from source

Clone the repository or download the source code, then install:

```bash
# Clone the repository
git clone https://github.com/onalius/gptoggle-core.git
cd gptoggle-core

# Install using the provided script
python install.py
```

Or use the regular Python installation process:

```bash
pip install -e .
```

### Option 3: Use standalone files

If you prefer not to install a package, you can use the standalone Python modules:

```bash
# Download the standalone enhanced file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.py -o gptoggle_enhanced.py

# Use in your code
from gptoggle_enhanced import get_response, recommend_model

response = get_response("What is quantum computing?")
print(response)
```

## JavaScript Installation

### Option 1: Install via npm

Install GPToggle via npm:

```bash
npm install github:onalius/gptoggle-core
```

Then use it in your code:

```javascript
// CommonJS import
const { GPToggle } = require('gptoggle-core');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Use GPToggle
async function example() {
  const response = await gptoggle.getResponse("What is quantum computing?");
  console.log(response);
}

example();
```

### Option 2: Use standalone JavaScript files

Download the standalone JavaScript file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js
```

Then use it in your code:

```javascript
const { GPToggle } = require('./gptoggle_enhanced.js');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Use GPToggle
async function example() {
  const response = await gptoggle.getResponse("What is quantum computing?");
  console.log(response);
}

example();
```

### Option 3: Browser Usage

For browser usage, include the file in your HTML:

```html
<script src="https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js"></script>

<script>
  // Initialize GPToggle with your API keys
  const apiKeys = {
    openai: "your-openai-key", // Store these securely!
    // Add other providers as needed
  };
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  // Use GPToggle
  async function example() {
    const response = await gptoggle.getResponse("What is quantum computing?");
    console.log(response);
  }
  
  example();
</script>
```

**Note**: For browser usage, we recommend storing API keys securely and not directly in client-side code.

Check out the fully functional browser example at `examples/javascript/browser-example.html`.

## Replit Environment

For Replit environments, use the provided installation script:

```bash
# In your Replit project
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/replit_install.sh | bash
```

Or if you've already downloaded or cloned the repository:

```bash
./replit_install.sh
```

This script handles the Replit-specific installation requirements to avoid self-dependency issues.

## API Keys Setup

GPToggle looks for API keys in environment variables:

- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Gemini: `GOOGLE_API_KEY`
- Grok: `XAI_API_KEY`

For development, you can create a .env file:

```
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
XAI_API_KEY=...
```

Then load it in your Python code:

```python
from dotenv import load_dotenv
load_dotenv()  # Install with: pip install python-dotenv
```

Or in Node.js:

```javascript
require('dotenv').config();  // Install with: npm install dotenv
```

## Troubleshooting

### Common Issues

1. **"No module named 'openai'"** (or similar for other providers)
   
   Install the required provider package:
   ```bash
   pip install openai  # Or anthropic, google-generativeai, etc.
   ```
   
   Or install with provider dependencies:
   ```bash
   pip install 'gptoggle-core[openai]'  # Or [claude], [gemini], [all]
   ```

2. **"API key not found in environment variables"**
   
   Make sure you've set the appropriate environment variables as mentioned in the [API Keys Setup](#api-keys-setup) section.

3. **Self-dependency issues in Replit**
   
   Use the Replit installation script which handles these issues:
   ```bash
   ./replit_install.sh
   ```

### Getting Help

If you encounter any issues not covered here, please:

1. Check the [GitHub issues](https://github.com/onalius/gptoggle-core/issues) for similar problems
2. Create a new issue if your problem hasn't been reported
3. Contact the developers at lano@docdel.io

---

For additional installation options and updates, check the [GitHub repository](https://github.com/onalius/gptoggle-core).