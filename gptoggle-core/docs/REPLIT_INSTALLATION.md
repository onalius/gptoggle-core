# Installing GPToggle in Replit

This guide covers the installation and usage of GPToggle specifically in Replit environments, addressing the unique considerations for Replit projects.

## Table of Contents
- [Quick Installation](#quick-installation)
- [Python Installation](#python-installation)
  - [Option 1: One-line Installer](#option-1-one-line-installer)
  - [Option 2: Manual Installation](#option-2-manual-installation)
  - [Option 3: Standalone File](#option-3-standalone-file)
- [JavaScript Installation in Replit](#javascript-installation-in-replit)
  - [Option 1: npm Installation](#option-1-npm-installation)
  - [Option 2: Standalone File](#option-2-standalone-file-1)
- [Setting up API Keys in Replit](#setting-up-api-keys-in-replit)
- [Example Usage in Replit](#example-usage-in-replit)
- [Troubleshooting Replit-Specific Issues](#troubleshooting-replit-specific-issues)

## Quick Installation

For the fastest installation in Replit, run this command in your Replit Shell:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/replit_install.sh | bash
```

This script will handle Replit-specific installation requirements and prompt you to install provider-specific dependencies.

## Python Installation

### Option 1: One-line Installer

The recommended way to install GPToggle in Replit is using the installation script:

```bash
# In your Replit shell
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/replit_install.sh | bash
```

This script:
1. Detects the Replit environment
2. Uses a special package name to avoid self-dependency issues
3. Prompts you to install provider-specific dependencies
4. Verifies the installation

### Option 2: Manual Installation

If you prefer to install manually:

```bash
# Clone the repository
git clone https://github.com/onalius/gptoggle-core.git
cd gptoggle-core

# Install using the special Replit configuration
python -m pip install -e .

# Install provider-specific dependencies as needed
python -m pip install openai  # For OpenAI
python -m pip install anthropic  # For Claude
python -m pip install google-generativeai  # For Gemini
```

### Option 3: Standalone File

For the simplest approach with no installation:

```bash
# Download the standalone file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.py -o gptoggle_enhanced.py

# Use directly in your code
from gptoggle_enhanced import get_response
```

## JavaScript Installation in Replit

### Option 1: npm Installation

In a Node.js Replit:

```bash
# Initialize npm if you haven't already
npm init -y

# Install from GitHub
npm install github:onalius/gptoggle-core

# Install provider dependencies if needed
npm install openai
```

Then use in your code:

```javascript
const { GPToggle } = require('gptoggle-core');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY
  // Add other providers as needed
};

// Create and use GPToggle
const gptoggle = new GPToggle({}, apiKeys);
```

### Option 2: Standalone File

```bash
# Download the standalone file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js

# Use in your code
const { GPToggle } = require('./gptoggle_enhanced.js');
```

## Setting up API Keys in Replit

In Replit, you should store API keys as Secrets:

1. Click on the "Tools" icon in the left sidebar
2. Select "Secrets"
3. Add your API keys with these exact names:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `GOOGLE_API_KEY`
   - `XAI_API_KEY`

GPToggle will automatically detect and use these keys from environment variables.

## Example Usage in Replit

Here's a simple example for a Python Replit:

```python
# main.py
from gptoggle import get_response, recommend_model

def main():
    # Test GPToggle
    prompt = "What is quantum computing?"
    
    # Get recommendation
    provider, model, reason, _ = recommend_model(prompt)
    print(f"Recommended model: {provider}'s {model}")
    print(f"Reason: {reason}")
    
    # Get response
    print("\nGetting response...")
    response = get_response(prompt)
    print("\nResponse:")
    print(response)

if __name__ == "__main__":
    main()
```

For JavaScript in Replit:

```javascript
// index.js
const { GPToggle } = require('gptoggle-core');

// Initialize GPToggle with API keys from Replit Secrets
const gptoggle = new GPToggle();

async function main() {
  const prompt = "What is quantum computing?";
  
  // Get recommendation
  const recommendation = gptoggle.recommendModel(prompt);
  console.log(`Recommended model: ${recommendation.provider}'s ${recommendation.model}`);
  console.log(`Reason: ${recommendation.reason}`);
  
  // Get response
  console.log("\nGetting response...");
  const response = await gptoggle.getResponse(prompt);
  console.log("\nResponse:");
  console.log(response);
}

main().catch(console.error);
```

## Troubleshooting Replit-Specific Issues

### Self-dependency issues

If you encounter errors about self-dependencies:

```
ERROR: circular dependency detected: gptoggle-core -> gptoggle-core
```

Use the Replit installation script which handles this automatically:

```bash
./replit_install.sh
```

### Import errors

If you get import errors despite installing the package:

```
ModuleNotFoundError: No module named 'gptoggle'
```

Try:
1. Check if the package is installed with `pip list | grep gptoggle`
2. Restart your Replit (sometimes needed after installations)
3. Try using the standalone file approach

### API key issues

If GPToggle reports missing API keys:

1. Check that you've added the keys in "Secrets" with the correct names
2. Make sure the keys are valid (not expired or revoked)
3. Verify you have access to the specific models you're trying to use

### Other issues

For other issues specific to Replit:

1. Try using the "Shell" instead of the "Console" for installations
2. Make sure your Replit has the correct language selected in the .replit file
3. For Node.js projects, check that the "Run" command is correctly configured

---

For more help with Replit-specific issues, check the [GPToggle GitHub repository](https://github.com/onalius/gptoggle-core) or contact the developers at lano@docdel.io.