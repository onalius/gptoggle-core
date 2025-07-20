# GPToggle - Multi-Provider AI Model Wrapper

## Overview

GPToggle is a comprehensive multi-provider AI model wrapper that provides intelligent model selection and unified access to various AI providers including OpenAI, Anthropic Claude, Google Gemini, Meta Llama, Perplexity, and xAI Grok. The application features both CLI and web interfaces, with sophisticated auto-triage capabilities for optimal model selection based on prompt characteristics.

## System Architecture

### Frontend Architecture
- **Flask Web Interface**: Provides a responsive web UI with Bootstrap dark theme for interacting with AI models
- **Static Web Assets**: CSS styling and JavaScript for enhanced user experience
- **Template System**: HTML templates using Jinja2 for dynamic content rendering
- **CLI Interface**: Command-line tool for direct interaction with AI providers

### Backend Architecture
- **Multi-Provider System**: Pluggable architecture supporting multiple AI providers through a common interface
- **Base Provider Pattern**: Abstract base class ensuring consistent implementation across all providers
- **Configuration Management**: Centralized configuration system for provider settings and API key management
- **Intelligent Triage System**: Auto-selection logic that analyzes prompts to recommend optimal models

### Core Components
- **Provider Registry**: Dynamic discovery and initialization of available AI providers
- **Model Selection Engine**: Task-specific recommendations with capability-based selection
- **Comparison System**: Cross-provider model comparison with user rating collection
- **Configuration System**: Provider management with enable/disable capabilities and priority ordering

## Key Components

### AI Providers
- **OpenAI Provider**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo models
- **Claude Provider**: Claude 3.5 Sonnet, Claude 3 Opus, Sonnet, and Haiku
- **Gemini Provider**: Gemini 1.5 Pro/Flash and Gemini Pro/Vision
- **Grok Provider**: Grok 2 and Grok Vision models
- **Llama Provider**: Meta's Llama API with 8B, 70B, and vision models
- **Perplexity Provider**: Llama-Sonar models with real-time web search

### Model Selection Features
- **Task Detection**: Six main categories (marketing, code, data analysis, etc.)
- **Component-Specific Suggestions**: Embedded model recommendations within responses
- **Follow-up Task Recommendations**: Suggests optimal models for subsequent tasks
- **Capability-Based Selection**: Models chosen based on specific requirements rather than categories

### Implementation Options
- **Python Package**: Full-featured package available via pip
- **Standalone Files**: Self-contained Python files requiring no installation
- **JavaScript Library**: Browser and Node.js compatible implementation
- **REST API**: HTTP interface for language-agnostic access

## Data Flow

1. **Input Processing**: User prompts are analyzed for characteristics (length, complexity, task type)
2. **Provider Selection**: Intelligent triage system selects optimal provider based on prompt analysis
3. **Model Recommendation**: Specific model chosen within provider based on task requirements
4. **API Communication**: Secure API calls to selected provider with standardized parameters
5. **Response Processing**: Model responses are formatted and returned with optional model suggestions
6. **Comparison Flow**: Multiple models can be queried simultaneously for response comparison

## External Dependencies

### Core AI Provider APIs
- **OpenAI API**: GPT model access via REST API
- **Anthropic API**: Claude model integration
- **Google AI API**: Gemini model access
- **xAI API**: Grok model integration
- **Meta AI API**: Llama model access
- **Perplexity API**: Real-time web-enabled models

### Python Dependencies
- **Flask**: Web framework for UI and API endpoints
- **openai**: Official OpenAI Python client
- **anthropic**: Official Anthropic Python client
- **google-generativeai**: Google's Gemini client library
- **requests**: HTTP client for API communications

### JavaScript Dependencies
- **axios**: HTTP client for browser and Node.js
- **Bootstrap**: UI framework for responsive web interface

## Deployment Strategy

### Replit Deployment
- **Autoscale Target**: Configured for automatic scaling based on demand
- **Gunicorn Server**: Production WSGI server for Flask application
- **Port Configuration**: Application runs on port 5000 with external port 80
- **Multi-Runtime Support**: Python 3.11 and Node.js 20 for hybrid functionality

### Environment Configuration
- **API Key Management**: Secure storage via environment variables
- **Provider Priority**: Configurable ordering for auto-selection
- **Model Registry**: Dynamic runtime registration of models with rich metadata

### Installation Options
- **Development Mode**: Editable installation for local development
- **Production Deployment**: Packaged installation via pip or npm
- **Standalone Usage**: Self-contained files for restricted environments
- **Web Interface**: Flask-based UI with REST API endpoints

## Changelog

- June 20, 2025: Initial setup
- June 20, 2025: Enhanced core GPToggle functionality with model-agnostic architecture and advanced task analysis
- July 20, 2025: **Major v2.0 Upgrade**: Implemented contextualized intelligence system with universal user profiles, query classification, and contextual helpers for personalized AI interactions

## Recent Changes

✓ Enhanced JavaScript implementations with task-specific recommendations
✓ Model-agnostic architecture with dynamic registry and capability-based selection  
✓ TypeScript model metadata definitions with pricing and capability information
✓ Comprehensive example files demonstrating enhanced features
✓ Updated documentation structure with quick start guide
✓ **Contextualized Intelligence System v2.0**: Upgraded core to support user profiles, query classification, and contextual helpers
✓ **Universal User Profile Schema**: Created service-agnostic profile system for broader adoption
✓ **Intelligent Query Processing**: Added 13+ query type classification with contextual enhancement
✓ **Adaptive Model Selection**: Implemented capability-based selection with user preference weighting
→ GPToggle v2.0 now provides contextualized intelligence foundation for universal adoption

## User Preferences

Preferred communication style: Simple, everyday language.
Focus: Providing core GPToggle functionality as a reusable foundation library, not full-stack application architecture.