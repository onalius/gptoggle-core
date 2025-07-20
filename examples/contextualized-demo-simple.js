/**
 * Simple JavaScript Demo of GPToggle Contextualized Intelligence v2.0
 * 
 * This demo showcases the key features of the upgraded GPToggle system:
 * - Universal user profiles for personalization
 * - Query classification and contextual enhancement
 * - Intelligent model selection based on user preferences
 * - Adaptive learning from user interactions
 * 
 * @version 2.0.0
 */

// Simulated GPToggle v2.0 Contextualized Intelligence System
class GPToggleV2 {
  constructor() {
    this.profiles = new Map();
    this.models = this.initializeModels();
    this.queryClassifier = new QueryClassifier();
    this.contextualHelpers = new ContextualHelpers();
  }

  initializeModels() {
    return [
      {
        provider: 'openai',
        modelId: 'gpt-4o',
        displayName: 'GPT-4o',
        capabilities: ['text', 'vision', 'code', 'reasoning'],
        strengths: { general: 5, code: 5, reasoning: 5, creativity: 4 },
        tier: 'standard',
        intelligence: 5,
        speed: 3
      },
      {
        provider: 'anthropic',
        modelId: 'claude-3-opus',
        displayName: 'Claude 3 Opus',
        capabilities: ['text', 'vision', 'reasoning', 'creativity'],
        strengths: { general: 5, reasoning: 5, creativity: 5, code: 4 },
        tier: 'premium',
        intelligence: 5,
        speed: 2
      },
      {
        provider: 'google',
        modelId: 'gemini-1.5-pro',
        displayName: 'Gemini 1.5 Pro',
        capabilities: ['text', 'vision', 'code', 'math'],
        strengths: { general: 4, math: 5, code: 4, reasoning: 4 },
        tier: 'standard',
        intelligence: 4,
        speed: 3
      }
    ];
  }

  // Create or load user profile
  async loadUserProfile(userId) {
    if (this.profiles.has(userId)) {
      return this.profiles.get(userId);
    }

    // Create default universal profile
    const defaultProfile = {
      userId,
      communicationStyle: {
        tone: 'casual',
        verbosity: 'moderate',
        language: 'en',
        includeExplanations: true
      },
      expertise: {
        domains: [],
        skillLevel: {},
        interests: []
      },
      preferences: {
        prioritizeSpeed: false,
        adaptivePersonalization: true,
        contextualAwareness: true,
        privacyLevel: 'standard'
      },
      context: {
        recentInteractions: [],
        savedItems: [],
        learningPatterns: {
          commonTopics: [],
          timePatterns: {},
          contextualPreferences: {}
        }
      },
      serviceSpecific: {
        gptoggle: {
          enabled: true,
          configuration: { accessLevel: 'basic' },
          preferences: {}
        }
      },
      metadata: {
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
        version: '2.0.0',
        services: ['gptoggle']
      }
    };

    this.profiles.set(userId, defaultProfile);
    return defaultProfile;
  }

  // Main contextualized toggle function
  async toggle(request) {
    const { query, userId, overrideModel } = request;
    const startTime = Date.now();

    try {
      // Step 1: Load user profile
      const userProfile = await this.loadUserProfile(userId);

      // Step 2: Classify query
      const queryType = this.queryClassifier.classifyQuery(query);

      // Step 3: Apply contextual enhancements
      const enhancedQuery = this.contextualHelpers.enhanceQuery({
        originalQuery: query,
        queryType,
        userProfile
      });

      // Step 4: Select optimal model
      const selectedModel = overrideModel || this.selectModel({
        queryType,
        userProfile,
        enhancedQuery
      });

      // Step 5: Generate response (simulated)
      const response = await this.generateResponse({
        model: selectedModel,
        query: enhancedQuery.enhanced,
        userProfile
      });

      // Step 6: Update user context
      await this.updateUserContext(userId, query, queryType, selectedModel.modelId);

      const processingTime = Date.now() - startTime;

      return {
        response: response.content,
        modelUsed: selectedModel.modelId,
        provider: selectedModel.provider,
        queryType,
        contextualEnhancements: enhancedQuery.appliedEnhancements,
        suggestedFollowUp: this.generateFollowUp(queryType),
        metadata: {
          processingTime,
          confidence: 0.85,
          userPersonalized: true
        }
      };

    } catch (error) {
      console.error('Toggle error:', error.message);
      throw error;
    }
  }

  // Select optimal model based on context
  selectModel({ queryType, userProfile, enhancedQuery }) {
    let candidates = this.models.filter(model => {
      // Check access level
      const accessLevel = userProfile.serviceSpecific.gptoggle?.configuration?.accessLevel || 'basic';
      if (accessLevel === 'basic' && model.tier === 'premium') {
        return false;
      }

      // Check capabilities
      const capability = this.getRequiredCapability(queryType);
      return capability ? model.capabilities.includes(capability) : true;
    });

    if (candidates.length === 0) {
      candidates = this.models.filter(m => m.tier !== 'premium');
    }

    // Score models
    const scored = candidates.map(model => ({
      model,
      score: this.scoreModel(model, queryType, userProfile)
    }));

    scored.sort((a, b) => b.score - a.score);
    return scored[0].model;
  }

  scoreModel(model, queryType, userProfile) {
    let score = 0;

    // Base capability score
    const strength = model.strengths[queryType] || model.strengths.general || 3;
    score += strength * 20;

    // Speed preference
    if (userProfile.preferences.prioritizeSpeed && model.speed > 3) {
      score += 15;
    } else if (!userProfile.preferences.prioritizeSpeed && model.intelligence > 4) {
      score += 15;
    }

    // Domain expertise bonus
    if (userProfile.expertise.domains.length > 0) {
      const relevant = userProfile.expertise.domains.some(domain => 
        this.isDomainRelevant(domain, queryType)
      );
      if (relevant) score += 10;
    }

    return score;
  }

  isDomainRelevant(domain, queryType) {
    const relevanceMap = {
      'technology': ['code', 'technical'],
      'science': ['factual', 'analytical', 'mathematical'],
      'business': ['business', 'analytical'],
      'education': ['educational', 'factual']
    };

    return relevanceMap[domain]?.includes(queryType) || false;
  }

  getRequiredCapability(queryType) {
    const capabilityMap = {
      'code': 'code',
      'mathematical': 'math',
      'creative': 'creativity',
      'analytical': 'reasoning',
      'technical': 'reasoning'
    };

    return capabilityMap[queryType];
  }

  // Simulate response generation
  async generateResponse({ model, query, userProfile }) {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

    const tone = userProfile.communicationStyle.tone;
    const verbosity = userProfile.communicationStyle.verbosity;

    let response = `[Simulated Response from ${model.displayName}]\n\n`;
    
    if (verbosity === 'detailed') {
      response += `This is a comprehensive response to your query: "${query.substring(0, 50)}..."\n\n`;
    }

    response += `I've processed your request with consideration for your ${tone} communication preference. `;
    
    if (userProfile.expertise.domains.length > 0) {
      response += `Given your expertise in ${userProfile.expertise.domains.join(', ')}, `;
    }

    response += `here's the information you requested:\n\n`;
    response += `[The actual AI model would provide the real response here, tailored to your profile and context.]`;

    if (userProfile.communicationStyle.includeExplanations) {
      response += `\n\nExplanation: This response was personalized based on your user profile, including your communication preferences, expertise areas, and interaction history.`;
    }

    return {
      content: response,
      tokensUsed: Math.floor(response.length / 4)
    };
  }

  // Update user context with interaction
  async updateUserContext(userId, query, queryType, modelUsed) {
    const profile = this.profiles.get(userId);
    
    // Add interaction
    profile.context.recentInteractions.unshift({
      content: query,
      timestamp: new Date().toISOString(),
      category: queryType,
      service: 'gptoggle'
    });

    // Maintain limit
    profile.context.recentInteractions = profile.context.recentInteractions.slice(0, 50);

    // Update learning patterns
    const existingTopic = profile.context.learningPatterns.commonTopics.find(t => t.topic === queryType);
    if (existingTopic) {
      existingTopic.frequency += 1;
      existingTopic.lastSeen = new Date().toISOString();
    } else {
      profile.context.learningPatterns.commonTopics.push({
        topic: queryType,
        frequency: 1,
        lastSeen: new Date().toISOString()
      });
    }

    // Sort by frequency
    profile.context.learningPatterns.commonTopics.sort((a, b) => b.frequency - a.frequency);

    profile.metadata.lastUpdated = new Date().toISOString();
  }

  generateFollowUp(queryType) {
    const followUpMap = {
      'code': 'Would you like me to explain how this code works or help you test it?',
      'creative': 'Should I help you develop this idea further or explore alternative approaches?',
      'factual': 'Would you like more detailed information on any specific aspect?',
      'analytical': 'Should I analyze this from a different perspective or provide additional data?',
      'business': 'Would you like me to help with implementation strategies or risk analysis?'
    };

    return followUpMap[queryType] || 'Is there anything else you\'d like to explore about this topic?';
  }
}

// Query Classification System
class QueryClassifier {
  constructor() {
    this.patterns = {
      'code': ['code', 'program', 'function', 'debug', 'javascript', 'python', 'html'],
      'creative': ['write', 'create', 'imagine', 'story', 'poem', 'brainstorm'],
      'factual': ['what', 'when', 'where', 'who', 'explain', 'define', 'information'],
      'analytical': ['analyze', 'compare', 'evaluate', 'assess', 'examine'],
      'business': ['business', 'strategy', 'marketing', 'sales', 'profit'],
      'mathematical': ['calculate', 'solve', 'equation', 'formula', 'math'],
      'educational': ['learn', 'teach', 'explain', 'lesson', 'tutorial'],
      'technical': ['technical', 'engineering', 'system', 'architecture']
    };
  }

  classifyQuery(query) {
    const queryLower = query.toLowerCase();
    const scores = {};

    for (const [type, keywords] of Object.entries(this.patterns)) {
      scores[type] = keywords.filter(keyword => 
        queryLower.includes(keyword)
      ).length;
    }

    const bestType = Object.entries(scores)
      .sort(([,a], [,b]) => b - a)[0];

    return bestType[1] > 0 ? bestType[0] : 'general';
  }
}

// Contextual Enhancement System
class ContextualHelpers {
  enhanceQuery({ originalQuery, queryType, userProfile }) {
    let enhanced = originalQuery;
    const appliedEnhancements = [];

    // Apply query type enhancement
    const typeEnhancement = this.getTypeEnhancement(queryType);
    if (typeEnhancement) {
      enhanced = `${typeEnhancement} ${enhanced}`;
      appliedEnhancements.push(`Query type: ${queryType}`);
    }

    // Apply tone preference
    const tone = userProfile.communicationStyle.tone;
    if (tone !== 'casual') {
      const toneInstruction = this.getToneInstruction(tone);
      enhanced = `${toneInstruction} ${enhanced}`;
      appliedEnhancements.push(`Tone: ${tone}`);
    }

    // Apply verbosity preference
    const verbosity = userProfile.communicationStyle.verbosity;
    if (verbosity !== 'moderate') {
      const verbosityInstruction = this.getVerbosityInstruction(verbosity);
      enhanced = `${verbosityInstruction} ${enhanced}`;
      appliedEnhancements.push(`Verbosity: ${verbosity}`);
    }

    // Apply domain expertise context
    if (userProfile.expertise.domains.length > 0) {
      enhanced = `Context: User has expertise in ${userProfile.expertise.domains.join(', ')}. ${enhanced}`;
      appliedEnhancements.push('Domain expertise');
    }

    return {
      enhanced,
      appliedEnhancements
    };
  }

  getTypeEnhancement(queryType) {
    const enhancements = {
      'code': 'You are a programming expert. Provide working code with best practices.',
      'creative': 'You are a creative assistant. Think imaginatively and originally.',
      'factual': 'You are a knowledgeable assistant. Provide accurate, verified information.',
      'analytical': 'You are an analytical expert. Provide structured, logical analysis.',
      'business': 'You are a business consultant. Provide practical, actionable advice.',
      'mathematical': 'You are a mathematics expert. Show step-by-step solutions.',
      'educational': 'You are a patient educator. Explain concepts clearly with examples.',
      'technical': 'You are a technical expert. Provide detailed technical information.'
    };

    return enhancements[queryType];
  }

  getToneInstruction(tone) {
    const instructions = {
      'formal': 'Please respond in a professional, formal tone.',
      'friendly': 'Please respond in a warm, friendly manner.',
      'professional': 'Please respond professionally and concisely.',
      'witty': 'Please respond with appropriate wit and clever insights.',
      'empathetic': 'Please respond with empathy and understanding.'
    };

    return instructions[tone];
  }

  getVerbosityInstruction(verbosity) {
    const instructions = {
      'concise': 'Please provide a brief, focused response.',
      'detailed': 'Please provide a comprehensive, detailed response with examples.',
      'comprehensive': 'Please provide an exhaustive response covering all aspects.'
    };

    return instructions[verbosity];
  }
}

// Demo Function
async function runContextualizedDemo() {
  console.log('🚀 GPToggle v2.0 Contextualized Intelligence Demo');
  console.log('=' .repeat(60));

  const gptoggle = new GPToggleV2();

  // Create different user profiles for demonstration
  const users = [
    {
      id: 'developer-alice',
      setupProfile: (profile) => {
        profile.communicationStyle.tone = 'casual';
        profile.communicationStyle.verbosity = 'detailed';
        profile.expertise.domains = ['technology', 'engineering'];
        profile.serviceSpecific.gptoggle.configuration.accessLevel = 'premium';
        return profile;
      }
    },
    {
      id: 'student-bob',
      setupProfile: (profile) => {
        profile.communicationStyle.tone = 'friendly';
        profile.communicationStyle.verbosity = 'moderate';
        profile.expertise.domains = ['education'];
        profile.preferences.prioritizeSpeed = true;
        return profile;
      }
    },
    {
      id: 'business-carol',
      setupProfile: (profile) => {
        profile.communicationStyle.tone = 'professional';
        profile.communicationStyle.verbosity = 'concise';
        profile.expertise.domains = ['business', 'finance'];
        profile.serviceSpecific.gptoggle.configuration.accessLevel = 'premium';
        return profile;
      }
    }
  ];

  // Demo queries
  const testQueries = [
    'Write a Python function to sort a list',
    'Explain machine learning algorithms',
    'Create a marketing strategy for a new product',
    'How do I calculate compound interest?'
  ];

  // Setup user profiles
  for (const user of users) {
    const profile = await gptoggle.loadUserProfile(user.id);
    user.setupProfile(profile);
    console.log(`\n👤 Setup profile for ${user.id}`);
  }

  // Test queries with different users
  for (const query of testQueries) {
    console.log(`\n📝 Testing Query: "${query}"`);
    console.log('-'.repeat(50));

    for (const user of users) {
      console.log(`\n👤 Response for ${user.id}:`);
      
      try {
        const result = await gptoggle.toggle({
          query,
          userId: user.id
        });

        console.log(`   Model: ${result.provider}:${result.modelUsed}`);
        console.log(`   Type: ${result.queryType}`);
        console.log(`   Enhancements: ${result.contextualEnhancements.join(', ')}`);
        console.log(`   Processing Time: ${result.metadata.processingTime}ms`);
        console.log(`   Response Preview: ${result.response.substring(0, 100)}...`);
        console.log(`   Follow-up: ${result.suggestedFollowUp}`);

      } catch (error) {
        console.log(`   ❌ Error: ${error.message}`);
      }
    }
  }

  // Show learning patterns
  console.log(`\n\n🧠 Learning Patterns Analysis`);
  console.log('-'.repeat(50));

  for (const user of users) {
    const profile = gptoggle.profiles.get(user.id);
    console.log(`\n👤 ${user.id}:`);
    console.log(`   Total Interactions: ${profile.context.recentInteractions.length}`);
    console.log(`   Common Topics: ${profile.context.learningPatterns.commonTopics.map(t => `${t.topic} (${t.frequency})`).join(', ')}`);
    console.log(`   Communication Style: ${profile.communicationStyle.tone}, ${profile.communicationStyle.verbosity}`);
    console.log(`   Expertise: ${profile.expertise.domains.join(', ')}`);
  }

  console.log(`\n✅ Demo completed! GPToggle v2.0 provides contextualized intelligence.`);
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GPToggleV2, runContextualizedDemo };
}

// Run demo if script is executed directly
if (typeof window === 'undefined' && require.main === module) {
  runContextualizedDemo().catch(console.error);
}