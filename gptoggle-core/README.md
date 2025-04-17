# GPToggle Core: Multi-Provider AI Model Wrapper

GPToggle is a comprehensive wrapper for multiple AI providers including OpenAI (GPT models), Anthropic Claude, Google Gemini, and xAI Grok. It simplifies working with various AI APIs by providing automatic model selection, unified interface, and task-specific recommendations.

## Version 1.0.3

The latest version (1.0.3) introduces task-specific recommendations, component-specific suggestions, and follow-up task recommendations for a more intelligent model selection experience.

## Features

- 🤖 **Multi-Provider Support**: Use OpenAI, Claude, Gemini, and Grok with a single interface
- 🔄 **Auto-Model Selection**: Intelligently chooses the best model based on prompt characteristics 
- 📊 **Task-Specific Recommendations**: Provides specific model recommendations for different task components in a prompt
- 🔮 **Follow-up Task Suggestions**: Suggests optimal models for likely follow-up tasks
- 🌐 **Multiple Implementations**: Available as Python package, standalone file, or JavaScript library
- 🚀 **Simple Installation**: Multiple options for different environments

## Documentation

- [INSTALLATION.md](INSTALLATION.md): Comprehensive installation guide for all environments
- [docs/JS_INSTALLATION.md](docs/JS_INSTALLATION.md): JavaScript-specific installation instructions
- [docs/REPLIT_INSTALLATION.md](docs/REPLIT_INSTALLATION.md): Replit-specific installation guide
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Version history and feature updates

## Quick Start

### Installation Options

**Python:**
```bash
# Option 1: Install via pip
pip install gptoggle-core

# Option 2: Run the installation script
python install.py

# Option 3: Standalone file (no installation)
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.py -o gptoggle_enhanced.py
```

**JavaScript:**
```bash
# Option 1: Install via npm
npm install github:onalius/gptoggle-core

# Option 2: Standalone file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js
```

**Replit:**
```bash
# One-line installation script for Replit
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/replit_install.sh | bash
```

### Basic Usage

**Python:**
```python
# Import from the package
from gptoggle import get_response, recommend_model, get_task_recommendations

# Auto-select model and get a response
response = get_response("What is quantum computing?")
print(response)

# Get task-specific recommendations
recommendations = get_task_recommendations("Design a marketing campaign and create a landing page")
print(recommendations)
```

**JavaScript:**
```javascript
// Import the package
const { GPToggle } = require('gptoggle-core');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Auto-select model and get a response
const response = await gptoggle.getResponse("What is quantum computing?");
console.log(response);

// Get task-specific recommendations
const recommendations = gptoggle.getTaskRecommendations(
  "Design a marketing campaign and create a landing page"
);
console.log(recommendations);
```

## Example Scripts

Check out the examples to see GPToggle in action:

**Python Examples:**
- `examples/python/gptoggle_enhanced_example.py`: Multi-task detection and recommendations
- `examples/python/gptoggle_followup_example.py`: Follow-up task recommendations
- `examples/test_installation.py`: Verify your installation

**JavaScript Examples:**
- `examples/javascript/gptoggle-enhanced-example.js`: Multi-task detection and recommendations
- `examples/javascript/gptoggle-followup-example.js`: Follow-up task recommendations
- `examples/javascript/browser-example.html`: In-browser usage with UI

## Quick Test

Run the quickstart script to test your installation:

```bash
./quickstart.sh
```

This script will guide you through testing GPToggle with your API keys.

## API Keys

GPToggle requires API keys for the providers you want to use:

- OpenAI: `OPENAI_API_KEY` - [Get key](https://platform.openai.com/api-keys)
- Claude: `ANTHROPIC_API_KEY` - [Get key](https://console.anthropic.com/)
- Gemini: `GOOGLE_API_KEY` - [Get key](https://ai.google.dev/)
- Grok: `XAI_API_KEY` - [Get key](https://x.ai/)

## License

MIT

## Contact

For questions or support, please contact:
- Email: lano@docdel.io
- GitHub: [github.com/onalius/gptoggle-core](https://github.com/onalius/gptoggle-core)