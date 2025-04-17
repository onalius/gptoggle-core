# GPToggle Installation Guide for Replit

This guide provides special instructions for installing and using GPToggle in Replit environments.

## Python Installation in Replit

### Option 1: Install via pip

In some Replit environments, you might face self-dependency issues. Try one of these methods:

```bash
# Method 1: Standard installation
pip install gptoggle-core

# Method 2: Installation with renamed package (if you face dependency issues)
pip install gptoggle-ai-wrapper-library-pkg
```

### Option 2: Use One-Line Installation Script

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/replit_install.sh | bash
```

### Option 3: Standalone Python File (No Installation)

Download the standalone file directly:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_minimal.py -o gptoggle_minimal.py
```

Then use it in your Python code:

```python
from gptoggle_minimal import get_response, recommend_model

response = get_response("Your prompt here")
```

## JavaScript Installation in Replit

### Option 1: NPM Installation

```bash
npm install github:onalius/gptoggle-core
```

Then use it in your JavaScript code:

```javascript
const { GPToggle } = require('gptoggle-js');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);
```

### Option 2: Standalone JavaScript File

Download the standalone file directly:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

Make sure to install axios:

```bash
npm install axios
```

Then use it in your JavaScript code:

```javascript
const { GPToggle } = require('./gptoggle.js');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);
```

## Setting Up API Keys in Replit

In Replit, you should set your API keys as environment variables:

1. Go to the "Secrets" tab in your Repl
2. Add the following keys:
   - `OPENAI_API_KEY` for OpenAI
   - `ANTHROPIC_API_KEY` for Claude
   - `GOOGLE_AI_API_KEY` for Gemini
   - `GROK_API_KEY` for Grok

## Web Interface in Replit

If you want to use the web interface, create a new file called `app.py` with this content:

```python
import os
from flask import Flask, render_template, request, jsonify
from gptoggle_minimal import get_response, recommend_model, get_available_providers

app = Flask(__name__)

@app.route('/')
def index():
    providers = get_available_providers()
    return render_template('index.html', providers=providers)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    provider = data.get('provider') if data.get('provider') != 'auto' else None
    model = data.get('model') if data.get('model') != 'auto' else None
    
    try:
        response = get_response(prompt, provider, model)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    prompt = data.get('prompt')
    
    try:
        provider, model = recommend_model(prompt)
        return jsonify({'provider': provider, 'model': model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

And make sure to install Flask:

```bash
pip install flask
```

## Troubleshooting in Replit

### Python Installation Issues

If you encounter issues with pip installation, try:

```bash
# Remove any previous installations
pip uninstall -y gptoggle-core gptoggle-ai-wrapper-library-pkg

# Install with --no-deps flag to avoid dependency conflicts
pip install --no-deps gptoggle-core
```

### JavaScript/npm Installation Issues

If you encounter issues with npm installation, use the standalone file method instead:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

## Need More Help?

For more detailed instructions and examples, check the main [README.md](README.md) and [API_REFERENCE.md](API_REFERENCE.md).