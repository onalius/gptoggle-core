/**
 * Contextualized Intelligence Demo
 * 
 * This example demonstrates the enhanced GPToggle-core with contextualized intelligence
 * capabilities including user profiles, query classification, and contextual helpers.
 * 
 * @version 2.0.0
 */

import { Toggle, ToggleRequest } from '../src/core/toggle';
import { UserProfileService, UserProfile } from '../src/profile/userProfileService';
import { Logger, LogLevel } from '../src/utils/logger';

// Demo user profiles
const demoProfiles: UserProfile[] = [
  {
    userId: 'developer-alice',
    tone: 'casual',
    domainExpertise: ['tech', 'engineering', 'data_science'],
    preferences: {
      preferredModels: ['gpt-4o', 'claude-3-opus'],
      prioritizeSpeed: false,
      verbosityLevel: 'detailed',
      includeExplanations: true,
      language: 'en'
    },
    memory: {
      recentQueries: [
        {
          query: 'How do I optimize database queries?',
          timestamp: new Date(Date.now() - 86400000).toISOString(),
          queryType: 'technical',
          modelUsed: 'gpt-4o'
        },
        {
          query: 'Explain microservices architecture',
          timestamp: new Date(Date.now() - 172800000).toISOString(),
          queryType: 'technical',
          modelUsed: 'claude-3-opus'
        }
      ],
      favorites: [],
      recentModels: ['gpt-4o', 'claude-3-opus', 'gemini-1.5-pro']
    },
    access: {
      level: 'premium',
      premiumFeatures: ['advanced_models', 'unlimited_queries', 'analytics']
    },
    metadata: {
      createdAt: new Date(Date.now() - 2592000000).toISOString(),
      lastUpdated: new Date().toISOString(),
      version: '2.0.0',
      source: 'onboarding'
    }
  },
  {
    userId: 'student-bob',
    tone: 'formal',
    domainExpertise: ['education', 'science'],
    preferences: {
      prioritizeSpeed: true,
      verbosityLevel: 'moderate',
      includeExplanations: true,
      language: 'en'
    },
    memory: {
      recentQueries: [
        {
          query: 'Explain photosynthesis',
          timestamp: new Date(Date.now() - 43200000).toISOString(),
          queryType: 'educational',
          modelUsed: 'gpt-3.5-turbo'
        }
      ],
      favorites: [],
      recentModels: ['gpt-3.5-turbo', 'gemini-1.5-flash']
    },
    access: {
      level: 'basic'
    },
    metadata: {
      createdAt: new Date(Date.now() - 604800000).toISOString(),
      lastUpdated: new Date().toISOString(),
      version: '2.0.0',
      source: 'manual'
    }
  },
  {
    userId: 'businesswoman-carol',
    tone: 'witty',
    domainExpertise: ['business', 'marketing', 'finance'],
    preferences: {
      preferredModels: ['claude-3-opus', 'gpt-4-turbo'],
      prioritizeSpeed: false,
      verbosityLevel: 'concise',
      includeExplanations: false,
      language: 'en'
    },
    memory: {
      recentQueries: [
        {
          query: 'Create a marketing strategy for a new product',
          timestamp: new Date(Date.now() - 21600000).toISOString(),
          queryType: 'business',
          modelUsed: 'claude-3-opus'
        },
        {
          query: 'Analyze market trends for Q4',
          timestamp: new Date(Date.now() - 64800000).toISOString(),
          queryType: 'analytical',
          modelUsed: 'gpt-4-turbo'
        }
      ],
      favorites: [
        {
          content: 'Always include ROI calculations in business proposals',
          type: 'response',
          timestamp: new Date(Date.now() - 432000000).toISOString(),
          tags: ['business', 'finance']
        }
      ],
      recentModels: ['claude-3-opus', 'gpt-4-turbo', 'perplexity-sonar']
    },
    access: {
      level: 'enterprise',
      premiumFeatures: ['advanced_models', 'unlimited_queries', 'priority_support', 'analytics', 'api_access']
    },
    metadata: {
      createdAt: new Date(Date.now() - 7776000000).toISOString(),
      lastUpdated: new Date().toISOString(),
      version: '2.0.0',
      source: 'api'
    }
  }
];

// Demo queries that showcase different capabilities
const demoQueries = [
  {
    query: 'Write a Python function to process large datasets efficiently',
    expectedType: 'code',
    description: 'Technical coding query for developer'
  },
  {
    query: 'How do neural networks learn?',
    expectedType: 'educational',
    description: 'Educational query for student'
  },
  {
    query: 'Create a compelling elevator pitch for our startup',
    expectedType: 'creative',
    description: 'Business creative query'
  },
  {
    query: 'What are the legal implications of data privacy regulations?',
    expectedType: 'legal',
    description: 'Legal analysis query'
  },
  {
    query: 'Analyze the pros and cons of remote work policies',
    expectedType: 'analytical',
    description: 'Business analytical query'
  },
  {
    query: 'I\'m feeling overwhelmed with my workload, any advice?',
    expectedType: 'emotional',
    description: 'Emotional support query'
  }
];

class ContextualizedIntelligenceDemo {
  private toggle: Toggle;
  private profileService: UserProfileService;
  private logger: Logger;

  constructor() {
    this.logger = new Logger(LogLevel.INFO);
    this.toggle = new Toggle();
    this.profileService = new UserProfileService();
    
    // Initialize demo profiles
    this.initializeDemoProfiles();
  }

  /**
   * Initialize demo profiles in the profile service
   */
  private async initializeDemoProfiles(): Promise<void> {
    for (const profile of demoProfiles) {
      await this.profileService.saveProfile(profile);
    }
    this.logger.info(`Initialized ${demoProfiles.length} demo profiles`);
  }

  /**
   * Run the complete demo showcasing all features
   */
  async runDemo(): Promise<void> {
    console.log('🚀 GPToggle Contextualized Intelligence Demo');
    console.log('=' .repeat(60));
    console.log();

    // Demo 1: Show user profile analysis
    await this.demoUserProfileAnalysis();
    
    // Demo 2: Show query classification
    await this.demoQueryClassification();
    
    // Demo 3: Show contextualized responses for different users
    await this.demoContextualizedResponses();
    
    // Demo 4: Show learning and adaptation
    await this.demoLearningAndAdaptation();

    console.log();
    console.log('✅ Demo completed! GPToggle now provides contextualized intelligence.');
    console.log();
  }

  /**
   * Demo user profile analysis capabilities
   */
  private async demoUserProfileAnalysis(): Promise<void> {
    console.log('📊 User Profile Analysis Demo');
    console.log('-'.repeat(40));

    for (const profile of demoProfiles) {
      console.log(`\n👤 User: ${profile.userId}`);
      console.log(`   Tone: ${profile.tone}`);
      console.log(`   Expertise: ${profile.domainExpertise.join(', ')}`);
      console.log(`   Access Level: ${profile.access.level}`);
      
      const analysis = this.profileService.analyzeUserPatterns(profile);
      console.log(`   Common Query Types: ${analysis.commonQueryTypes.map(t => t.type).join(', ')}`);
      console.log(`   Preferred Models: ${analysis.modelEffectiveness && Object.keys(analysis.modelEffectiveness).join(', ') || 'None yet'}`);
    }
  }

  /**
   * Demo query classification capabilities
   */
  private async demoQueryClassification(): Promise<void> {
    console.log('\n\n🔍 Query Classification Demo');
    console.log('-'.repeat(40));

    for (const { query, expectedType, description } of demoQueries) {
      const result = await this.toggle['queryClassifier'].classifyQueryDetailed(query);
      
      console.log(`\n📝 Query: "${query}"`);
      console.log(`   Description: ${description}`);
      console.log(`   Classified as: ${result.queryType} (confidence: ${(result.confidence * 100).toFixed(1)}%)`);
      console.log(`   Reasoning: ${result.reasoning}`);
      
      if (result.alternativeTypes) {
        console.log(`   Alternative types: ${result.alternativeTypes.join(', ')}`);
      }
    }
  }

  /**
   * Demo contextualized responses for different user types
   */
  private async demoContextualizedResponses(): Promise<void> {
    console.log('\n\n🎯 Contextualized Response Demo');
    console.log('-'.repeat(40));

    const testQuery = 'Explain machine learning algorithms';
    
    for (const profile of demoProfiles) {
      console.log(`\n👤 Response for ${profile.userId}:`);
      
      const request: ToggleRequest = {
        query: testQuery,
        userProfile: profile
      };

      try {
        const response = await this.toggle.toggle(request);
        
        console.log(`   Model Selected: ${response.provider}:${response.modelUsed}`);
        console.log(`   Query Type: ${response.queryType}`);
        console.log(`   Enhancements Applied: ${response.contextualEnhancements.join(', ')}`);
        console.log(`   Confidence: ${(response.metadata.confidence * 100).toFixed(1)}%`);
        console.log(`   Processing Time: ${response.metadata.processingTime}ms`);
        console.log(`   Response Preview: ${response.response.substring(0, 150)}...`);
        
        if (response.suggestedFollowUp) {
          console.log(`   Follow-up Suggestion: ${response.suggestedFollowUp}`);
        }
        
        // Update user memory with this query
        await this.profileService.addQueryToMemory(
          profile.userId,
          testQuery,
          response.queryType,
          response.modelUsed
        );
        
      } catch (error) {
        console.log(`   ❌ Error: ${error.message}`);
      }
    }
  }

  /**
   * Demo learning and adaptation capabilities
   */
  private async demoLearningAndAdaptation(): Promise<void> {
    console.log('\n\n🧠 Learning and Adaptation Demo');
    console.log('-'.repeat(40));

    const userId = 'developer-alice';
    const profile = await this.profileService.loadProfile(userId);

    console.log(`\n👤 Learning patterns for ${userId}:`);
    
    // Simulate several queries to show learning
    const learningQueries = [
      'Debug this Python code',
      'Optimize database performance',
      'Implement a REST API',
      'Design system architecture'
    ];

    for (const query of learningQueries) {
      const request: ToggleRequest = {
        query,
        userProfile: profile
      };

      try {
        const response = await this.toggle.toggle(request);
        await this.profileService.addQueryToMemory(
          userId,
          query,
          response.queryType,
          response.modelUsed
        );
        
        console.log(`   Added: "${query}" -> ${response.queryType} (${response.modelUsed})`);
      } catch (error) {
        console.log(`   ❌ Error processing "${query}": ${error.message}`);
      }
    }

    // Show updated patterns
    const updatedProfile = await this.profileService.loadProfile(userId);
    const analysis = this.profileService.analyzeUserPatterns(updatedProfile);
    
    console.log(`\n📈 Updated Learning Patterns:`);
    console.log(`   Common Query Types: ${analysis.commonQueryTypes.map(t => `${t.type} (${t.frequency})`).join(', ')}`);
    console.log(`   Recent Models: ${updatedProfile.memory?.recentModels?.slice(0, 3).join(', ') || 'None'}`);
    console.log(`   Total Queries Tracked: ${updatedProfile.memory?.recentQueries?.length || 0}`);

    // Demo adding a favorite
    await this.profileService.addFavorite(
      userId,
      'Always use async/await for better performance',
      'response',
      ['python', 'performance']
    );
    
    console.log(`   ⭐ Added favorite coding tip`);
  }

  /**
   * Demo model recommendation improvements
   */
  async demoModelRecommendations(): Promise<void> {
    console.log('\n\n🎯 Enhanced Model Recommendations');
    console.log('-'.repeat(40));

    for (const profile of demoProfiles) {
      console.log(`\n👤 Recommendations for ${profile.userId}:`);
      
      const recommendations = this.profileService.getModelRecommendations(profile, 'code');
      console.log(`   For coding tasks: ${recommendations.slice(0, 3).join(', ')}`);
      
      const businessRecs = this.profileService.getModelRecommendations(profile, 'business');
      console.log(`   For business tasks: ${businessRecs.slice(0, 3).join(', ')}`);
    }
  }
}

// Run the demo if this file is executed directly
if (require.main === module) {
  const demo = new ContextualizedIntelligenceDemo();
  demo.runDemo().catch(console.error);
}

export { ContextualizedIntelligenceDemo };