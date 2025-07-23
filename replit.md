# GPToggle - Multi-Provider AI Model Wrapper

## Overview

GPToggle is a sophisticated AI model wrapper system that provides intelligent routing and selection across multiple AI providers (OpenAI, Anthropic Claude, Google Gemini, xAI Grok, Meta Llama, and Perplexity). The system features automatic model selection based on query content, user profiling, adaptive module management, and cross-platform module portability through Universal Module Identifiers (UMID).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

GPToggle follows a modular, provider-agnostic architecture that enables seamless integration across multiple AI services while maintaining sophisticated user context and adaptive intelligence capabilities.

### Core Components

1. **Multi-Provider Engine**: Abstracts API calls across different AI providers with intelligent fallback mechanisms
2. **Query Classification System**: Analyzes prompts to determine optimal model selection based on content type (creative, technical, analytical, etc.)
3. **User Profile Management**: Maintains contextualized user preferences, domain expertise, and interaction history
4. **Adaptive Module System**: Automatically creates and manages specialized knowledge containers (lists, planners, trackers) based on user interactions
5. **Universal Module Identifier (UMID)**: Cross-platform module identification system for seamless data portability

## Key Components

### Backend Architecture

- **Core Engine** (`core/gptoggle_v2.py`): Model-agnostic implementation with dynamic model registry and capability-based selection
- **Enhanced Module Service** (`modules/moduleServiceUMID.py`): Manages adaptive user modules with UMID integration
- **Provider Abstractions**: Unified interface for OpenAI, Claude, Gemini, Grok, Llama, and Perplexity APIs
- **Configuration Management**: Centralized provider priority, model mappings, and parameter settings

### Frontend Architecture

- **Web Interface** (`web/main.py`): Flask-based web UI for interactive model testing and comparison
- **REST API** (`examples/rest_api.py`): HTTP endpoints for external service integration
- **Client Libraries**: Python and JavaScript/Node.js clients for programmatic access

### Module System

- **Automatic Module Detection**: Recognizes patterns in user queries to create specialized modules (shopping lists, calendars, task planners)
- **UMID Generation** (`modules/umidGenerator.py`): Creates globally unique identifiers for cross-platform module compatibility
- **Module Evolution**: Modules adapt and grow based on continued usage patterns
- **Cross-Reference Capabilities**: Modules build relationships with other modules for enhanced context

## Data Flow

1. **Query Processing**: User input is analyzed for intent, complexity, and domain requirements
2. **Provider Selection**: System selects optimal AI provider and model based on query characteristics and user profile
3. **Response Generation**: Query is sent to selected provider with appropriate parameters
4. **Module Analysis**: Response is analyzed for potential module creation or updates
5. **Context Updates**: User profile and modules are updated based on interaction patterns
6. **Response Delivery**: Enhanced response with embedded model suggestions and follow-up recommendations

## External Dependencies

### AI Provider APIs
- **OpenAI API**: GPT models (gpt-3.5-turbo, gpt-4o)
- **Anthropic API**: Claude models (claude-3-sonnet, claude-3-opus)
- **Google AI API**: Gemini models (gemini-pro, gemini-1.5-pro)
- **xAI API**: Grok models (grok-beta, grok-2-1212)
- **Meta AI API**: Llama models (llama-3-70b-instruct)
- **Perplexity API**: Sonar models with online search capabilities

### Required Environment Variables
```
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
XAI_API_KEY=your-xai-key
META_AI_API_KEY=your-meta-key
PERPLEXITY_API_KEY=your-perplexity-key
```

### Python Dependencies
- `requests`: HTTP client for API calls
- `flask`: Web framework for UI and REST API
- `flask-cors`: Cross-origin request handling
- Standard library modules: `json`, `os`, `sys`, `re`, `datetime`, `hashlib`

### JavaScript Dependencies
- `node-fetch`: HTTP client for Node.js (fallback for older Node.js versions)
- Built-in `fetch` for modern Node.js environments

## Deployment Strategy

### Development Environment
1. Clone repository and install dependencies
2. Set required API keys as environment variables
3. Run examples directly: `python examples/basic_usage.py`
4. Start web interface: `python web/main.py`
5. Launch REST API server: `python examples/rest_api.py`

### Production Deployment
1. **Containerization**: Docker-ready Flask application with environment variable configuration
2. **API Gateway**: REST API can be deployed behind load balancers for scaling
3. **Database Integration**: User profiles and modules can be persisted to databases (prepared for Postgres integration)
4. **Cross-Platform Integration**: UMID system enables module sharing across different services and platforms

### Scaling Considerations
- **Provider Load Balancing**: Automatic failover between providers based on availability and rate limits
- **Caching Layer**: Response caching for common queries to reduce API costs
- **Module Storage**: Adaptive modules designed for efficient storage and retrieval in database systems
- **Multi-Service Architecture**: UMID system supports distributed module management across microservices

The architecture prioritizes flexibility, scalability, and cross-platform compatibility while maintaining sophisticated AI routing capabilities and user context awareness.