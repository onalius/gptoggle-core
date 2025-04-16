# Changelog

All notable changes to the GPToggle project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Changed
- Complete architecture redesign to support multiple providers
- Refactored configuration system to handle provider-specific settings
- Updated command-line interface with provider selection capabilities
- Enhanced auto-selection logic with provider priority

### Security
- API key handling via environment variables
- Warning system for missing API keys

## [0.1.0] - 2025-01-15 - Initial Release

Initial release with OpenAI support only.

### Added
- Basic CLI interface for OpenAI API
- Simple model selection between GPT-4 and GPT-3.5-turbo
- Configuration via environment variables