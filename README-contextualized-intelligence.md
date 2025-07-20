# GPToggle Contextualized Intelligence v2.0

## Overview

GPToggle v2.0 transforms the core library from a simple model-selection utility into a fully contextualized intelligence system. This upgrade enables GPToggle to understand user queries, factor in user profiles, and apply contextual helpers to provide truly personalized AI interactions.

## Key Features

### 🎯 Contextualized Intelligence
- **User Profile System**: Universal, service-agnostic user profiles
- **Query Classification**: Intelligent analysis of user intent and query type
- **Contextual Helpers**: Dynamic query enhancement based on user context
- **Adaptive Model Selection**: Smart model choice based on user preferences and task requirements

### 🧠 Universal User Profiles
The new user profile system is designed to be universally applicable across different services and applications:

- **Communication Style**: Tone, verbosity, language preferences
- **Expertise & Interests**: Professional domains, skill levels, and areas of interest
- **Behavioral Preferences**: Speed vs. quality, personalization settings, privacy levels
- **Context & Learning**: Interaction history, saved items, learned patterns
- **Service-Specific Config**: Extensible configuration for different services

### 🔍 Intelligent Query Processing
- **Automatic Classification**: 13+ query types (factual, creative, legal, emotional, etc.)
- **Context Enhancement**: Query enrichment based on user profile and history
- **Model Optimization**: Capability-based model selection with user preference weighting
- **Follow-up Suggestions**: Intelligent next-step recommendations

## Architecture

```
lib/
└── contextualized-intelligence.js  # Complete contextualized intelligence system

TypeScript Modules (for advanced integration):
├── toggle.ts                      # Main contextualized intelligence engine
├── modelRegistry.ts               # Model management and selection
├── userProfileSchema.json         # Universal user profile schema
├── userProfileService.ts          # Profile management service
├── queryClassifier.ts             # Query type classification
├── contextualHelpers.ts           # Context-aware query enhancement
├── logger.ts                      # Logging utilities
└── config.ts                      # Configuration management

Examples:
├── contextualized-demo-simple.js  # JavaScript demo
└── contextualized-intelligence-demo.ts  # TypeScript demo
```

## Quick Start

### Basic Usage

```javascript
// Using the standalone library
const { ContextualizedIntelligence } = require('./lib/contextualized-intelligence');

// Initialize the system
const ci = new ContextualizedIntelligence();

// Process a query with contextualized intelligence
const result = await ci.processQuery(
  'Explain machine learning algorithms',
  'user-123'
);

console.log(`Query Type: ${result.queryType}`);
console.log(`Confidence: ${result.confidence}`);
console.log(`Enhancements: ${result.enhancements.join(', ')}`);
console.log(`Enhanced Query: ${result.enhancedQuery}`);
```

### Advanced Integration with GPToggle

```typescript
import { Toggle, ToggleRequest } from './toggle';
import { UserProfileService } from './userProfileService';

// Initialize the system
const toggle = new Toggle();
const profileService = new UserProfileService();

// Load or create user profile
const userProfile = await profileService.loadProfile('user-123');

// Create a contextualized request
const request: ToggleRequest = {
  query: 'Explain machine learning algorithms',
  userProfile: userProfile,
  parameters: {
    temperature: 0.7,
    maxTokens: 1500
  }
};

// Get contextualized response
const response = await toggle.toggle(request);

console.log(`Model Used: ${response.provider}:${response.modelUsed}`);
console.log(`Query Type: ${response.queryType}`);
console.log(`Enhancements: ${response.contextualEnhancements.join(', ')}`);
console.log(`Response: ${response.response}`);
```

### User Profile Management

```javascript
// Load or create a user profile
const userProfile = await ci.loadUserProfile('developer-alice');

// Customize the profile
userProfile.communicationStyle.tone = 'casual';
userProfile.communicationStyle.verbosity = 'detailed';
userProfile.expertise.domains = ['technology', 'engineering'];
userProfile.expertise.skillLevel = { 
  'javascript': 'expert', 
  'python': 'advanced' 
};

// Add interactions to build context
userProfile.addInteraction(
  'How do I optimize database queries?',
  'technical',
  'my-service'
);

// Save the profile
await ci.saveUserProfile(userProfile);
```

### Service-Specific Integration

```javascript
// Configure service-specific settings
const profile = await ci.loadUserProfile('user-123');

profile.configureService('gptoggle', {
  preferredModels: ['gpt-4o', 'claude-3-opus'],
  accessLevel: 'premium',
  enableFollowUpSuggestions: true
});

profile.configureService('my-ai-service', {
  customSetting: 'value',
  featureFlags: ['advanced_analysis', 'real_time_learning']
});

await ci.saveUserProfile(profile);
```

## Universal Profile Schema

The user profile schema is designed to be reusable across different AI services and applications:

### Core Structure
- **Communication Style**: How users prefer to receive responses
- **Expertise**: Professional background and skill levels
- **Preferences**: Behavioral and service preferences
- **Context**: Interaction history and learned patterns
- **Service-Specific**: Extensible configuration for individual services

### Benefits for Other Services
1. **Standardization**: Common profile format across AI services
2. **Portability**: Users can transfer profiles between services
3. **Consistency**: Uniform personalization experience
4. **Extensibility**: Easy to add service-specific features

## Query Classification System

The system automatically classifies queries into types for better processing:

- **Factual**: Information requests, definitions, explanations
- **Creative**: Writing, brainstorming, artistic tasks
- **Code**: Programming, debugging, technical implementation
- **Analytical**: Data analysis, comparisons, evaluations
- **Legal**: Legal questions, compliance, regulations
- **Emotional**: Support, advice, empathetic responses
- **Educational**: Learning, teaching, tutorials
- **Business**: Strategy, marketing, professional advice
- **Health**: Medical questions, wellness advice
- **Technical**: Engineering, system design, architecture

## Contextual Enhancement System

The contextual helper system enhances queries based on:

1. **Query Type**: Applies type-specific instructions and formatting
2. **User Expertise**: Leverages domain knowledge for relevant context
3. **Communication Style**: Adjusts tone, verbosity, and explanation level
4. **Recent Context**: Uses interaction history for continuity
5. **Service Preferences**: Applies service-specific configurations

## Model Selection Intelligence

Enhanced model selection considers:

- **Task Suitability**: Model capabilities aligned with query type
- **User Preferences**: Preferred models and performance priorities
- **Access Level**: Available models based on user tier
- **Performance History**: Past model effectiveness for similar tasks
- **Resource Constraints**: Speed vs. quality trade-offs

## Examples and Demos

Run the demos to see all features in action:

```bash
# JavaScript demo (no dependencies required)
node examples/contextualized-demo-simple.js

# TypeScript demo (requires ts-node)
npx ts-node examples/contextualized-intelligence-demo.ts
```

The demo showcases:
- User profile analysis
- Query classification
- Contextualized responses for different user types
- Learning and adaptation over time
- Enhanced model recommendations

## Testing

Comprehensive test suite covers:
- Basic toggle functionality
- User profile integration
- Query classification accuracy
- Contextual enhancement effectiveness
- Model selection logic
- Error handling and edge cases

```bash
npm test
```

## Migration from v1.x

The v2.0 upgrade maintains backward compatibility while adding contextualized intelligence:

1. **Existing Functionality**: All v1.x features continue to work
2. **Optional Enhancement**: Contextualized features are additive
3. **Gradual Adoption**: Can implement user profiles incrementally
4. **Universal Compatibility**: Profile schema works with any service

## Future Enhancements

- **Multi-Language Support**: Enhanced internationalization
- **Advanced Learning**: Machine learning for better personalization
- **Cross-Service Sync**: Profile synchronization across services
- **Real-Time Adaptation**: Dynamic preference learning
- **Privacy Controls**: Granular data handling preferences

## Contributing

To contribute to the contextualized intelligence system:

1. Follow the established architecture patterns
2. Ensure universal applicability of profile schemas
3. Add comprehensive tests for new features
4. Document service integration examples
5. Maintain backward compatibility

The GPToggle v2.0 contextualized intelligence system represents a significant advancement in personalized AI interactions, providing a foundation that other services can build upon for consistent, intelligent user experiences.