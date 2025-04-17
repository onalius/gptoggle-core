# GPToggle: Multi-Provider AI Model Wrapper

GPToggle is a comprehensive wrapper for multiple AI providers including OpenAI, Anthropic Claude, Google Gemini, and xAI Grok. It simplifies working with various AI APIs by providing automatic model selection, unified interface, and response comparison.

## Features

- 🤖 **Multi-Provider Support**: Use OpenAI (GPT models), Anthropic Claude, Google Gemini, and xAI Grok with a single interface
- 🔄 **Auto-Model Selection**: Intelligently chooses the best model based on prompt characteristics
- 📊 **Task-Specific Recommendations**: Provides specific model recommendations for different task components in a prompt
- 🔮 **Follow-up Task Suggestions**: Suggests optimal models for likely follow-up tasks
- 🌐 **Multiple Implementations**: Available as Python package, standalone Python file, or JavaScript library
- 🚀 **Simple Installation**: Multiple installation options for different environments

## Quick Start

### Python Installation

#### Option 1: Install via pip (Recommended)

```bash
pip install gptoggle-core
```

#### Option 2: Use the Standalone File

Download the standalone file directly:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.py -o gptoggle_enhanced.py
```

Then use it in your code:

```python
from gptoggle_enhanced import get_response, recommend_model

# Get a response using auto-selected model
response = get_response("What is quantum computing?")

# Get component-specific recommendations
provider, model, reason, tasks = recommend_model("Create a marketing plan and implement a landing page")
```

### JavaScript Installation

#### Option 1: NPM Installation

```bash
npm install github:onalius/gptoggle-core
```

#### Option 2: Standalone JavaScript File

Download the standalone file directly:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js
```

Then use it in your code:

```javascript
const { GPToggle } = require('./gptoggle_enhanced.js');

// Setup your API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Get a response with auto-model selection
const response = await gptoggle.getResponse("What is quantum computing?");
```

## Features in Detail

### Task-Specific Recommendations

GPToggle can identify different task components in a complex prompt and recommend the best model for each:

```python
from gptoggle_enhanced import get_task_recommendations

prompt = "Design a marketing campaign for our eco-friendly product line and implement a landing page"
recommendations = get_task_recommendations(prompt)

# This will show recommendations specifically for the marketing and coding components
print(recommendations)
```

### Follow-up Task Suggestions

GPToggle can predict likely follow-up tasks and suggest the best models for them:

```python
from gptoggle_enhanced import get_followup_recommendations

# Get follow-up recommendations based on detected tasks
followups = get_followup_recommendations(recommendations["task_recommendations"])

# This will show recommendations for tasks like "content creation", "deployment", etc.
print(followups)
```

## Documentation

For more detailed instructions, see the following guides:

- [CHANGELOG.md](docs/CHANGELOG.md): Version history and feature updates
- [JS_INSTALLATION.md](docs/JS_INSTALLATION.md): Detailed JavaScript installation guide
- [REPLIT_INSTALLATION.md](docs/REPLIT_INSTALLATION.md): Installation guide for Replit environments

## Examples

Check out the example scripts in the `examples` directory:

- `gptoggle_enhanced_example.py`: Demonstrates multi-task detection
- `gptoggle_followup_example.py`: Shows follow-up task recommendations
- `gptoggle-enhanced-example.js`: JavaScript example for all features

## API Keys

GPToggle requires API keys for the providers you want to use:

- OpenAI: Set as environment variable `OPENAI_API_KEY`
- Claude: Set as environment variable `ANTHROPIC_API_KEY`
- Gemini: Set as environment variable `GOOGLE_API_KEY`
- Grok: Set as environment variable `XAI_API_KEY`

## License

MIT

## Contact

For questions or support, please contact:
- Email: lano@docdel.io
- GitHub: [github.com/onalius/gptoggle-core](https://github.com/onalius/gptoggle-core)