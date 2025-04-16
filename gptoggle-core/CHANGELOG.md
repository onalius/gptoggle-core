# Changelog

All notable changes to the GPToggle project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-04-16

### Added
- Initial release with multi-provider architecture
- Base provider class as a common interface for all AI providers
- Provider implementations:
  - OpenAI provider with support for GPT-4o, GPT-4-turbo, and GPT-3.5-turbo
  - Claude provider with support for Claude 3.5 Sonnet, Claude 3 Opus, Sonnet, and Haiku
  - Gemini provider with support for Gemini 1.5 Pro/Flash and Gemini Pro/Vision
  - Grok provider with support for Grok 2 and Grok Vision
- Intelligent model selection for each provider based on prompt analysis
- Configuration system for provider management with enable/disable capabilities
- Provider priority configuration for auto-selection sequence
- CLI interface for interacting with models
- Python API for programmatic access
- Model comparison functionality with user rating collection
- Comprehensive README with documentation and examples
- Installation scripts for development mode
- Test utilities to verify installation and functionality

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- API key handling via environment variables
- Warning system for missing API keys