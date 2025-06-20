# GPToggle: Multi-Provider AI Model Wrapper

GPToggle is a comprehensive wrapper for multiple AI providers including OpenAI, Anthropic Claude, Google Gemini, Meta's Llama, Perplexity, and xAI Grok. It simplifies working with various AI APIs by providing automatic model selection, unified interface, and response comparison.

## Latest Version: 2.0.0 - Model-Agnostic Architecture (Beta)

**New in 2.0.0 (Beta):**
- **Dynamic Model Registry**: Register models at runtime without code changes
- **Rich Model Metadata**: Detailed capability descriptions for intelligent selection
- **Capability-Based Selection**: Choose models based on specific requirements
- **Provider-Agnostic Interface**: Unified API across different AI providers
- **Custom Provider Handlers**: Register handlers for any AI provider
- **Unified Scoring System**: Sophisticated selection algorithm with explanations

Read the [MODEL_REGISTRY.md](MODEL_REGISTRY.md) documentation for details on the new approach.

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

### 🤖 Multi-Provider Support
Support for major AI providers: OpenAI (GPT models), Anthropic Claude, Google Gemini, Meta's Llama, Perplexity, and xAI Grok

### 🧠 Intelligent Model Selection
- **Auto-Selection**: Automatically chooses the best model based on prompt characteristics
- **Capability-Based Selection**: Models chosen based on specific requirements (vision, code, math, reasoning)
- **Context-Aware Recommendations**: Considers prompt length, complexity, and task type

### 📊 Advanced Task Analysis
- **Multi-Task Detection**: Identifies different task types within a single prompt
- **Component-Specific Recommendations**: Suggests optimal models for each part of complex requests
- **Follow-up Task Suggestions**: Recommends models for likely next steps in your workflow

### 🔧 Multiple Implementation Options
- **JavaScript/TypeScript**: Browser and Node.js compatible with enhanced features
- **Python Package**: Full-featured package with provider integrations
- **Standalone Files**: Self-contained implementations requiring no installation
- **Model-Agnostic Architecture**: Dynamic model registry with rich metadata (v2.0+)

### 🚀 Developer-Friendly
- **Simple API**: Easy-to-use interface for all skill levels
- **Rich Documentation**: Comprehensive guides and examples
- **Flexible Configuration**: Customizable provider priorities and model mappings
- **TypeScript Support**: Full type definitions for model metadata and capabilities

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
- [MODEL_REGISTRY.md](MODEL_REGISTRY.md): Comprehensive guide to the v2.0 model registry system
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md): Instructions for migrating from v1.x to v2.0
- [CHANGELOG.md](gptoggle-core/docs/CHANGELOG.md): Version history and feature updates
- [REST_API_DOCS.md](REST_API_DOCS.md): REST API documentation (if using the API server)

## Examples

Check out the example scripts:

**v2.0 Examples (Model-Agnostic):**
- `example_v2.py`: Complete demonstration of the new model-agnostic approach
- `models_database.json`: Example model database with rich metadata

**v1.x Examples:**
- `gptoggle_enhanced_example.py`: Demonstrates multi-task detection
- `gptoggle_followup_example.py`: Shows follow-up task recommendations
- `llama_example.py`: Demonstrates Meta's Llama API integration
- `perplexity_example.py`: Shows Perplexity API with real-time web search
- `gptoggle-enhanced-example.js`: JavaScript example with all features

## Migration to v2.0

To migrate from v1.x to v2.0, see the [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

## License

MIT

## Contact

For questions or support, please contact:
- Email: lano@docdel.io
- GitHub: [github.com/onalius/gptoggle-core](https://github.com/onalius/gptoggle-core)