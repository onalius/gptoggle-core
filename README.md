# GPToggle - Multi-Provider AI Model Wrapper

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/yourusername/gptoggle/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/javascript-ES2020+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

**An advanced AI-powered development toolkit that revolutionizes coding workflows through intelligent, flexible multi-model interactions and comprehensive developer assistance.**

GPToggle is a comprehensive multi-provider AI model wrapper that provides intelligent model selection and unified access to various AI providers including OpenAI, Anthropic Claude, Google Gemini, Meta Llama, Perplexity, and xAI Grok. Features both CLI and web interfaces with sophisticated auto-triage capabilities and revolutionary **Modular Adaptive Intelligence** system.

## 🌟 Key Features

### 🤖 Multi-Provider AI Access
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Anthropic Claude**: Claude 3.5 Sonnet, Opus, Haiku
- **Google Gemini**: Gemini 1.5 Pro/Flash, Gemini Pro/Vision
- **xAI Grok**: Grok 2 and Grok Vision models
- **Meta Llama**: Llama API with 8B, 70B, and vision models
- **Perplexity**: Llama-Sonar models with real-time web search

### 🧠 Modular Adaptive Intelligence v2.0
- **Self-Creating Modules**: Automatically generate specialized knowledge containers from user interactions
- **6 Module Types**: Lists, planners, calendars, interests, trackers, goals
- **Universal Module IDs (UMID)**: Cross-platform module portability with standardized identification
- **Intelligent Lifecycle**: Automatic aging, archiving, and cleanup based on usage patterns
- **Cross-Service Export**: Export modules for use in ChatGPT, Notion, Slack, or any other platform

### 🎯 Intelligent Model Selection
- **Auto-Triage**: Analyzes prompts to recommend optimal models
- **Task Detection**: Six main categories (marketing, code, data analysis, etc.)
- **Capability-Based Selection**: Models chosen based on specific requirements
- **Provider Priority**: Configurable ordering for auto-selection

### 🌐 Multiple Implementation Options
- **Python Package**: Full-featured package via pip
- **JavaScript Library**: Browser and Node.js compatible
- **Standalone Files**: Self-contained implementation requiring no installation
- **REST API**: HTTP interface for language-agnostic access
- **Web Interface**: Flask-based UI with Bootstrap dark theme

## 🚀 Quick Start

### Installation

```bash
# Python
pip install gptoggle

# JavaScript/Node.js
npm install gptoggle
```

### Basic Usage

**Python:**
```python
from gptoggle import GPToggle

# Initialize GPToggle
gpt = GPToggle()

# Simple query with automatic provider selection
response = gpt.query("Explain quantum computing in simple terms")
print(response['response'])

# Automatic module creation
response = gpt.query("I need to buy milk, eggs, and bread")
# Creates a shopping list module automatically

# Module management
user_profile = gpt.get_user_profile()
summary = user_profile.get_modules_summary()
print(f"Total modules: {summary['totalModules']}")
```

**JavaScript:**
```javascript
import { GPToggle } from 'gptoggle';

const gpt = new GPToggle();

// Simple query
const result = await gpt.query("Write a Python function to sort a list");
console.log(result.response);

// Multi-provider comparison
const comparison = await gpt.compareProviders(
    "Explain the benefits of renewable energy",
    ['openai', 'claude', 'gemini']
);
```

### Web Interface

```bash
# Start the web server
python web/main.py

# Open browser to http://localhost:5000
```

## 🧩 Modular Adaptive Intelligence

GPToggle v2.0 introduces revolutionary adaptive modules that automatically emerge from user interactions:

### Automatic Module Creation

```python
# These queries automatically create specialized modules:

# Shopping List Module
gpt.query("I need to buy milk, eggs, bread, and bananas")

# Party Planning Module  
gpt.query("I'm planning a birthday party for March 15th with Alice and Bob")

# Learning Interest Module
gpt.query("I'm fascinated by Virginia Woolf's stream of consciousness writing")

# Exercise Tracker Module
gpt.query("I want to track my daily exercise - goal is 30 minutes")

# Goal Setting Module
gpt.query("My goal is to learn Spanish and be conversational by year-end")
```

### Universal Module IDs (UMID)

Every module gets a globally unique identifier for cross-platform compatibility:

```
gptoggle.list.a1b2c3d4.1721737200.x7z9
chatgpt.interest.e5f6g7h8.1721737201.m3p5
notion.tracker.i9j0k1l2.1721737202.q8w2
```

**Format**: `{service}.{moduleType}.{contextHash}.{timestamp}.{random}`

This enables seamless module export to any platform that adopts the UMID standard.

## 📁 Project Structure

```
gptoggle/
├── core/                   # Core library implementation
│   ├── gptoggle_v2.py     # Main Python library
│   └── gptoggle.js        # JavaScript implementation
├── modules/               # UMID system and module services
│   ├── umidGenerator.py   # Python UMID implementation
│   ├── umidGenerator.ts   # TypeScript UMID implementation
│   └── moduleServiceUMID.py # Enhanced module service
├── web/                   # Flask web interface
│   ├── main.py           # Web application entry point
│   ├── templates/        # HTML templates
│   └── static/          # CSS, JavaScript assets
├── docs/                  # Comprehensive documentation
│   ├── QUICK_START.md    # Getting started guide
│   ├── MODULE_GUIDE.md   # Modular intelligence guide
│   └── UMID_SPEC.md      # Universal Module ID specification
├── examples/             # Usage examples and demos
│   ├── basic_usage.py    # Python examples
│   ├── advanced_features.js # JavaScript examples
│   └── module_demos.py   # Module system demonstrations
└── tests/                # Test suite
    ├── test_core.py      # Core functionality tests
    └── test_modules.py   # Module system tests
```

## 🔧 Configuration

### API Keys Setup

```bash
# Required: At least one AI provider
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"

# Optional: Additional providers
export XAI_API_KEY="your-key-here"
export META_AI_API_KEY="your-key-here"
export PERPLEXITY_API_KEY="your-key-here"
```

### Provider Priority

```python
# Customize provider selection order
gpt = GPToggle(provider_priority=['claude', 'openai', 'gemini'])

# Module cleanup settings
gpt = GPToggle(module_cleanup_days=45)  # Default: 30 days
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
python -m pytest tests/ -v

# Core functionality
python tests/test_core.py

# Module system
python tests/test_modules.py

# Examples
python examples/basic_usage.py
node examples/advanced_features.js
```

## 📖 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Module Guide](docs/MODULE_GUIDE.md)** - Complete modular intelligence documentation
- **[UMID Specification](docs/UMID_SPEC.md)** - Universal Module ID technical specification
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and testing requirements
- Pull request process
- Issue reporting guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/gptoggle.git
cd gptoggle

# Install development dependencies
pip install -e .[dev]
npm install

# Run tests
python -m pytest tests/ -v
npm test
```

## 🌟 Advanced Features

### Cross-Provider Model Comparison

```python
comparison = gpt.compare_providers(
    "Explain the benefits of renewable energy",
    providers=['openai', 'claude', 'gemini']
)

for provider, response in comparison.items():
    print(f"\n{provider.upper()}:")
    print(response[:200] + "...")
```

### Module Export for Other Platforms

```python
# Export modules for use in other services
export_data = module_service.export_modules_for_service(
    user_profile, 
    target_service='notion'
)

# Import modules from another service
imported = module_service.import_modules_from_service(
    export_data,
    current_service='gptoggle'
)
```

### Batch Operations

```python
queries = [
    "Add cheese to my shopping list",
    "Schedule gym session for tomorrow",
    "Track my daily reading progress"
]

results = gpt.batch_query_with_modules(queries)
```

## 🎯 Use Cases

- **Development Assistance**: Multi-model code generation and review
- **Content Creation**: Leverage different AI strengths for various content types
- **Research & Analysis**: Compare insights across multiple AI perspectives
- **Personal Productivity**: Adaptive modules that grow with your needs
- **Team Collaboration**: Shared modules and cross-platform compatibility
- **Learning & Education**: Interest tracking and goal-oriented modules

## 📊 Performance

- **Module Operations**: < 10ms typical response time
- **Query Analysis**: < 5ms for pattern recognition
- **Data Extraction**: 90%+ accuracy for module creation
- **Memory Efficiency**: Minimal impact on system resources
- **Cross-Platform**: Native performance on all supported platforms

## 🗺️ Roadmap

### v2.1 (Q4 2025)
- Voice-activated module creation
- Visual module planning with diagrams
- Team collaboration features
- Advanced pattern recognition

### v2.2 (Q1 2026)
- AI-powered module suggestions
- Custom module templates
- Integration with external productivity tools
- Mobile-optimized interfaces

### Future Considerations
- Emotional intelligence modules
- Predictive module creation
- Advanced analytics dashboard
- Enterprise collaboration features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides in the `docs/` directory
- **Examples**: Working code examples in the `examples/` directory
- **Community**: Join our discussions for questions and ideas

## 🏆 Acknowledgments

- Built with love for the AI development community
- Inspired by the need for intelligent, adaptive AI assistance
- Thanks to all contributors and early adopters

---

**GPToggle v2.0** - Revolutionizing AI interactions through modular adaptive intelligence. 🚀