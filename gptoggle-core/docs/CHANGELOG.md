# Changelog

All notable changes to the GPToggle project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-04-17 - Task-Specific Recommendations & Follow-up Task Suggestions

GPToggle v1.0.3 introduces advanced recommendation capabilities for multi-faceted prompts, including task-specific model recommendations, component-specific suggestions within responses, and recommendations for likely follow-up tasks.

### Added
- Task-specific model recommendations for multi-faceted prompts
- Component-specific model suggestions embedded in responses
- Follow-up task recommendations based on detected prompt components
- Enhanced model selection rationale with detailed task analysis
- Task detection system with six main categories:
  - Marketing plans and strategies
  - Code implementation and technical development
  - Data analysis and statistical interpretation
  - Creative content and narrative
  - Business strategy and planning
  - Product design and development
- Provider strength profiles for different task types
- Follow-up task categories with provider-specific model recommendations
- New API methods:
  - `getTaskRecommendations()` - Get recommendations for each task component in a prompt
  - `getFollowupRecommendations()` - Get recommendations for likely follow-up tasks
  - `generateModelSuggestions()` - Generate component and follow-up suggestions for responses
- Enhanced configuration with specialized model categories (creative, technical, analytical)
- Example scripts demonstrating the new features:
  - `gptoggle_enhanced_example.py` - Python example for multi-task detection
  - `gptoggle_followup_example.py` - Python example for follow-up task recommendations
  - `gptoggle-enhanced-example.js` - JavaScript example

### Changed
- Improved model recommendation rationale with task-specific context
- Enhanced response generation to include model suggestions for both current and follow-up tasks
- Expanded provider priority system to include task-specific rankings
- Added rich metadata for tasks including likely follow-up activities

## [1.0.2] - 2025-04-17 - Enhanced JavaScript Support & Documentation

GPToggle v1.0.2 adds better JavaScript support with npm package compatibility and improved documentation.

### Added
- Added package.json file for npm installation support
- Detailed JavaScript installation guide (JS_INSTALLATION.md)
- Web interface documentation (WEB_INTERFACE.md)
- Browser-based example with localStorage API key storage
- Enhanced README with both Python and JavaScript usage examples
- Expanded Replit installation guide to cover both Python and JavaScript

### Fixed
- Fixed repository URLs across all documentation files
- Improved installation instructions for JavaScript environments
- Fixed npm installation issues with proper package configuration

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