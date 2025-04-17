# Changelog

All notable changes to the GPToggle project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-04-17 - Improved Installation & Cross-Platform Compatibility

GPToggle v1.0.1 focuses on improving installation and compatibility across different environments, including Replit.

### Added
- Built-in Replit environment detection in setup.py
- REST API example in examples/rest_api.py for HTTP-based access
- Client libraries in both Python and Node.js 
- Installation helper script (install.py) for automatic environment detection
- Detailed Replit-specific installation guide (REPLIT_INSTALLATION.md)
- Recommend_model function for backward compatibility
- Standalone Python module (gptoggle_minimal.py) for import-free usage
- Native JavaScript implementation (gptoggle.js) for web environments
- Replit installation shell script (replit_install.sh) for one-line setup
- Comprehensive REST API documentation (REST_API_DOCS.md)

### Fixed
- Self-dependency installation issues in Replit
- Package naming conflicts through environment detection
- Documentation gaps for installation across platforms
- Circular import issues with utils.py module
- Missing package data and templates

### Changed
- Improved dependency management with optional components
- Setup.py now adapts to different environments
- Better error handling during installation

## [1.0.0] - 2025-04-16 - Multi-Provider Architecture

GPToggle v1.0.0 introduces a complete overhaul with a new multi-provider architecture. This version expands beyond the initial OpenAI-only implementation to include support for multiple AI providers (Claude, Gemini, and Grok).

### Added
- Multi-provider architecture with pluggable provider system
- Base provider class as a common interface for all AI providers
- New provider implementations:
  - Claude provider with support for Claude 3.5 Sonnet, Claude 3 Opus, Sonnet, and Haiku
  - Gemini provider with support for Gemini 1.5 Pro/Flash and Gemini Pro/Vision
  - Grok provider with support for Grok 2 and Grok Vision
- Enhanced OpenAI provider with support for GPT-4o, GPT-4-turbo, and GPT-3.5-turbo
- Intelligent model selection for each provider based on prompt analysis
- Configuration system for provider management with enable/disable capabilities
- Provider priority configuration for auto-selection sequence
- Expanded CLI interface for interacting with models across providers
- Comprehensive Python API for programmatic access
- Cross-provider model comparison functionality with user rating collection
- Installation scripts for development mode
- Test utilities to verify installation and functionality
- Utilities module (utils.py) to centralize shared functionality and prevent circular imports

### Changed
- Complete architecture redesign to support multiple providers
- Refactored configuration system to handle provider-specific settings
- Updated command-line interface with provider selection capabilities
- Enhanced auto-selection logic with provider priority
- Reorganized project structure for better maintainability:
  - Created a dedicated utilities module to prevent circular imports
  - Improved provider initialization and configuration handling
  - Streamlined import hierarchy
  - Better separation between core libraries and user interfaces
- Fixed Flask web interface to properly display and use models from all providers

### Security
- API key handling via environment variables
- Warning system for missing API keys

## [0.1.0] - 2025-01-15 - Initial Release

Initial release with OpenAI support only.

### Added
- Basic CLI interface for OpenAI API
- Simple model selection between GPT-4 and GPT-3.5-turbo
- Configuration via environment variables