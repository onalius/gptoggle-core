# GPToggle: Multi-Provider AI Model Wrapper

GPToggle is a comprehensive wrapper for multiple AI providers including OpenAI, Anthropic Claude, Google Gemini, Meta's Llama, Perplexity, and xAI Grok. It simplifies working with various AI APIs by providing automatic model selection, unified interface, and response comparison.

## Latest Version: 1.0.4 - Meta Llama and Perplexity Integration

**New in 1.0.4:**
- Added support for Meta's Llama API (llama-3-8b-instruct, llama-3-70b-instruct, llama-3-vision)
- Added support for Perplexity API (llama-3.1-sonar models with up-to-date web information)
- Updated provider priority ranking to include new providers
- Created dedicated example files for Llama and Perplexity integrations
- Task-specific recommendations now include the new providers

**New in 1.0.3:**
- Task-specific model recommendations for multi-faceted prompts
- Component-specific model suggestions embedded in responses
- Follow-up task recommendations based on detected prompt components
- Enhanced model selection rationale with detailed task analysis
- 6 task categories with provider-specific model strengths

## Core Features

- 🤖 **Multi-Provider Support**: OpenAI (GPT models), Anthropic Claude, Google Gemini, Meta's Llama, Perplexity, and xAI Grok
- 🔄 **Auto-Model Selection**: Intelligently chooses the best model based on prompt characteristics
- 📊 **Task-Specific Recommendations**: Specific model recommendations for different components in a prompt
- 🔮 **Follow-up Task Suggestions**: Optimal models for likely follow-up tasks
- 🌐 **Multiple Implementations**: Python package, standalone file, or JavaScript library
- 🚀 **Simple Installation**: Multiple options for different environments

## Installation

### Main Package: `gptoggle-core`

The main package for Python and JavaScript code is in the `gptoggle-core` directory.

For detailed installation instructions, see:
- [Python Installation](gptoggle-core/docs/README.md)
- [JavaScript Installation](gptoggle-core/docs/JS_INSTALLATION.md)
- [Replit Installation](gptoggle-core/docs/REPLIT_INSTALLATION.md)

### Quick Start with Python

```bash
# Option 1: Install via pip (recommended)
pip install gptoggle-core

# Option 2: Install from source
cd gptoggle-core
python install.py
```

### Quick Start with JavaScript

```bash
# Option 1: Install via npm
npm install github:onalius/gptoggle-core

# Option 2: Use the standalone file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js
```

## Documentation

For more detailed information:
- [CHANGELOG.md](gptoggle-core/docs/CHANGELOG.md): Version history and feature updates
- [REST_API_DOCS.md](REST_API_DOCS.md): REST API documentation (if using the API server)

## Examples

Check out the example scripts:
- `gptoggle_enhanced_example.py`: Demonstrates multi-task detection
- `gptoggle_followup_example.py`: Shows follow-up task recommendations
- `llama_example.py`: Demonstrates Meta's Llama API integration
- `perplexity_example.py`: Shows Perplexity API with real-time web search
- `gptoggle-enhanced-example.js`: JavaScript example with all features

## License

MIT

## Contact

For questions or support, please contact:
- Email: lano@docdel.io
- GitHub: [github.com/onalius/gptoggle-core](https://github.com/onalius/gptoggle-core)