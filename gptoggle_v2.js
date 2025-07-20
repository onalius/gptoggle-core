/**
 * GPToggle v2.0 - Model-Agnostic Implementation with Contextualized Intelligence
 * 
 * This module implements a model-agnostic version of GPToggle that features:
 * - Dynamic model registry
 * - Capability-based model selection
 * - Rich attribute scoring system
 * - Provider-agnostic interface
 * - Universal user profiles for personalization
 * - Query classification and contextual enhancement
 * - Adaptive learning from user interactions
 * 
 * @version 2.0.0
 */

/**
 * Universal User Profile class for contextualized AI interactions
 */
class UserProfile {
  constructor(userId) {
    this.userId = userId;
    this.communicationStyle = {
      tone: 'casual',
      verbosity: 'moderate',
      language: 'en',
      includeExplanations: true
    };
    this.expertise = {
      domains: [],
      skillLevel: {},
      interests: []
    };
    this.preferences = {
      prioritizeSpeed: false,
      adaptivePersonalization: true,
      contextualAwareness: true,
      privacyLevel: 'standard'
    };
    this.context = {
      recentInteractions: [],
      savedItems: [],
      learningPatterns: {
        commonTopics: [],
        timePatterns: {},
        contextualPreferences: {}
      }
    };
    this.serviceSpecific = {
      gptoggle: {
        enabled: true,
        configuration: { accessLevel: 'basic' },
        preferences: {}
      }
    };
    this.metadata = {
      createdAt: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
      version: '2.0.0',
      services: ['gptoggle']
    };
  }

  static createDefault(userId) {
    return new UserProfile(userId);
  }

  addInteraction(content, category = null, service = 'gptoggle') {
    const interaction = {
      content,
      timestamp: new Date().toISOString(),
      category,
      service
    };

    this.context.recentInteractions.unshift(interaction);
    this.context.recentInteractions = this.context.recentInteractions.slice(0, 100);

    // Update learning patterns
    if (category) {
      const commonTopics = this.context.learningPatterns.commonTopics;
      const existing = commonTopics.find(t => t.topic === category);

      if (existing) {
        existing.frequency += 1;
        existing.lastSeen = new Date().toISOString();
      } else {
        commonTopics.push({
          topic: category,
          frequency: 1,
          lastSeen: new Date().toISOString()
        });
      }

      // Sort by frequency and limit
      commonTopics.sort((a, b) => b.frequency - a.frequency);
      this.context.learningPatterns.commonTopics = commonTopics.slice(0, 20);
    }

    this.metadata.lastUpdated = new Date().toISOString();
  }

  updateProfileAdaptively(query, queryType, modelUsed = null) {
    const timestamp = new Date().toISOString();

    // Add to recent queries (FIFO with max 10)
    if (!this.context.recentQueries) {
      this.context.recentQueries = [];
    }
    this.context.recentQueries.unshift({
      query,
      type: queryType,
      timestamp
    });
    this.context.recentQueries = this.context.recentQueries.slice(0, 10);

    // Update interaction history
    if (!this.context.interactionHistory) {
      this.context.interactionHistory = {
        queryTypes: {},
        lastModelUsed: null,
        lastInteraction: null
      };
    }

    // Increment query type counter
    this.context.interactionHistory.queryTypes[queryType] = 
      (this.context.interactionHistory.queryTypes[queryType] || 0) + 1;

    // Update last used model and interaction time
    if (modelUsed) {
      this.context.interactionHistory.lastModelUsed = modelUsed;
    }
    this.context.interactionHistory.lastInteraction = timestamp;

    // Adaptive domain expertise detection
    this._updateDomainExpertise(query);

    // Adaptive tone analysis
    this._updateCommunicationTone(query);

    // Update metadata
    this.metadata.lastUpdated = timestamp;
  }

  _updateDomainExpertise(query) {
    const queryLower = query.toLowerCase();

    // Domain keyword mapping
    const domainKeywords = {
      'technology': ['code', 'programming', 'software', 'api', 'database', 'javascript', 'python', 'algorithm'],
      'business': ['contract', 'revenue', 'strategy', 'marketing', 'sales', 'finance', 'budget', 'roi'],
      'creative': ['design', 'art', 'story', 'creative', 'poem', 'music', 'melody', 'composition'],
      'education': ['learn', 'teach', 'study', 'lesson', 'tutorial', 'course', 'homework', 'assignment'],
      'science': ['research', 'experiment', 'data', 'analysis', 'hypothesis', 'theory', 'scientific'],
      'health': ['medical', 'health', 'nutrition', 'exercise', 'wellness', 'therapy', 'treatment'],
      'cooking': ['recipe', 'cook', 'ingredient', 'food', 'meal', 'kitchen', 'bake', 'prepare']
    };

    // Count domain matches
    Object.entries(domainKeywords).forEach(([domain, keywords]) => {
      const matches = keywords.filter(keyword => queryLower.includes(keyword)).length;
      if (matches > 0) {
        if (!this.expertise.domains.includes(domain)) {
          // Add new domain if multiple keywords detected
          if (matches >= 2) {
            this.expertise.domains.push(domain);
          }
        }

        // Update skill level based on frequency
        const currentLevel = this.expertise.skillLevel[domain] || 0;
        this.expertise.skillLevel[domain] = Math.min(currentLevel + matches, 10);
      }
    });
  }

  _updateCommunicationTone(query) {
    const queryLower = query.toLowerCase();

    // Casual indicators
    const casualIndicators = ['hey', 'hi', 'thanks', 'cool', 'awesome', 'lol', 'btw', 'gonna', 'wanna'];
    const casualCount = casualIndicators.filter(indicator => queryLower.includes(indicator)).length;

    // Formal indicators
    const formalIndicators = ['please', 'would you', 'could you', 'kindly', 'respectfully', 'sincerely'];
    const formalCount = formalIndicators.filter(indicator => queryLower.includes(indicator)).length;

    // Professional indicators
    const professionalIndicators = ['analyze', 'evaluate', 'assess', 'provide', 'demonstrate', 'implement'];
    const professionalCount = professionalIndicators.filter(indicator => queryLower.includes(indicator)).length;

    // Adaptive tone adjustment
    const totalInteractions = Object.values(this.context.interactionHistory?.queryTypes || {})
      .reduce((sum, count) => sum + count, 0);

    if (totalInteractions >= 3) { // Only adjust after sufficient interactions
      if (casualCount > formalCount + professionalCount) {
        this.communicationStyle.tone = 'casual';
      } else if (professionalCount > casualCount) {
        this.communicationStyle.tone = 'professional';
      } else if (formalCount > casualCount) {
        this.communicationStyle.tone = 'formal';
      }
    }
  }
}

/**
 * Query Classification system
 */
class QueryClassifier {
  constructor() {
    this.patterns = {
      'code': {
        keywords: ['code', 'program', 'function', 'debug', 'javascript', 'python', 'html', 'css', 'sql', 'api'],
        phrases: ['write a function', 'debug this', 'how to code', 'programming help'],
      },
      'creative': {
        keywords: ['write', 'create', 'imagine', 'story', 'poem', 'brainstorm', 'design', 'creative'],
        phrases: ['write a story', 'create content', 'brainstorm ideas'],
      },
      'factual': {
        keywords: ['what', 'when', 'where', 'who', 'how', 'explain', 'define', 'information', 'facts'],
        phrases: ['what is', 'explain to me', 'tell me about'],
      },
      'analytical': {
        keywords: ['analyze', 'compare', 'evaluate', 'assess', 'examine', 'review', 'study'],
        phrases: ['compare and contrast', 'analyze this', 'evaluate the'],
      },
      'business': {
        keywords: ['business', 'strategy', 'marketing', 'sales', 'profit', 'revenue', 'company'],
        phrases: ['business plan', 'marketing strategy', 'increase sales'],
      },
      'educational': {
        keywords: ['learn', 'teach', 'explain', 'lesson', 'tutorial', 'course', 'study'],
        phrases: ['teach me', 'learn about', 'tutorial on'],
      }
    };
  }

  classifyQuery(query) {
    const queryLower = query.toLowerCase();
    const scores = {};

    Object.entries(this.patterns).forEach(([queryType, config]) => {
      let score = 0;

      // Keyword matching
      const keywordMatches = config.keywords.filter(keyword => 
        queryLower.includes(keyword)
      ).length;
      score += keywordMatches * 2;

      // Phrase matching
      const phraseMatches = config.phrases.filter(phrase => 
        queryLower.includes(phrase)
      ).length;
      score += phraseMatches * 3;

      scores[queryType] = score;
    });

    // Find best match
    const sortedTypes = Object.entries(scores).sort(([,a], [,b]) => b - a);
    const bestType = sortedTypes[0];

    return {
      queryType: bestType[1] > 0 ? bestType[0] : 'general',
      confidence: bestType[1] > 0 ? Math.min(bestType[1] / 10, 1) : 0.5,
      scores
    };
  }
}

/**
 * Contextual Enhancement system
 */
class ContextualEnhancer {
  enhanceQuery(query, queryType, userProfile) {
    const enhancements = [];
    let enhancedQuery = query;

    // Apply query type enhancement
    const typeEnhancement = this.getTypeEnhancement(queryType);
    if (typeEnhancement) {
      enhancedQuery = `${typeEnhancement} ${enhancedQuery}`;
      enhancements.push(`Query type: ${queryType}`);
    }

    // Apply communication style
    const style = userProfile.communicationStyle;
    if (style.tone !== 'casual') {
      const toneInstruction = this.getToneInstruction(style.tone);
      enhancedQuery = `${toneInstruction} ${enhancedQuery}`;
      enhancements.push(`Tone: ${style.tone}`);
    }

    if (style.verbosity !== 'moderate') {
      const verbosityInstruction = this.getVerbosityInstruction(style.verbosity);
      enhancedQuery = `${verbosityInstruction} ${enhancedQuery}`;
      enhancements.push(`Verbosity: ${style.verbosity}`);
    }

    // Apply domain expertise
    if (userProfile.expertise.domains.length > 0) {
      const expertiseContext = `Context: User has expertise in ${userProfile.expertise.domains.join(', ')}. `;
      enhancedQuery = expertiseContext + enhancedQuery;
      enhancements.push('Domain expertise');
    }

    // Apply recent context
    const recentTopics = this.extractRecentTopics(userProfile.context.recentInteractions);
    if (recentTopics.length > 0) {
      const topicsStr = recentTopics.map(([topic, count]) => `${topic} (${count}x)`).join(', ');
      const contextNote = `Recent discussion topics: ${topicsStr}. `;
      enhancedQuery = contextNote + enhancedQuery;
      enhancements.push('Recent context');
    }

    return {
      enhanced: enhancedQuery,
      enhancements,
      original: query
    };
  }

  getTypeEnhancement(queryType) {
    const enhancements = {
      'code': 'You are a programming expert. Provide working code with best practices.',
      'creative': 'You are a creative assistant. Think imaginatively and provide original content.',
      'factual': 'Provide accurate, well-sourced factual information.',
      'analytical': 'Provide structured, logical analysis with clear reasoning.',
      'business': 'You are a business consultant. Provide practical, actionable advice.',
      'educational': 'You are a patient educator. Explain concepts clearly with examples.'
    };
    return enhancements[queryType] || '';
  }

  getToneInstruction(tone) {
    const instructions = {
      'formal': 'Please respond in a professional, formal tone.',
      'friendly': 'Please respond in a warm, friendly manner.',
      'professional': 'Please respond professionally and concisely.',
      'witty': 'Please respond with appropriate wit and clever insights.',
      'empathetic': 'Please respond with empathy and understanding.'
    };
    return instructions[tone] || '';
  }

  getVerbosityInstruction(verbosity) {
    const instructions = {
      'concise': 'Please provide a brief, focused response.',
      'detailed': 'Please provide a comprehensive, detailed response with examples.',
      'comprehensive': 'Please provide an exhaustive response covering all aspects.'
    };
    return instructions[verbosity] || '';
  }

  extractRecentTopics(interactions) {
    const topicCounts = {};
    interactions.slice(0, 10).forEach(interaction => {
      if (interaction.category) {
        topicCounts[interaction.category] = (topicCounts[interaction.category] || 0) + 1;
      }
    });

    return Object.entries(topicCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3);
  }
}

/**
 * Model registry and selection system
 */
class ModelRegistry {
  constructor() {
    this.models = new Map();
  }
  
  /**
   * Register a model with its capabilities and attributes
   * 
   * @param {Object} modelInfo - Model information and capabilities
   * @returns {ModelRegistry} - For method chaining
   */
  registerModel(modelInfo) {
    const { provider, modelId } = modelInfo;
    if (!provider || !modelId) {
      throw new Error("Model must have both provider and modelId attributes");
    }
    
    const modelKey = `${provider}:${modelId}`;
    this.models.set(modelKey, modelInfo);
    return this;
  }
  
  /**
   * Register multiple models at once from an array
   * 
   * @param {Array<Object>} modelsArray - Array of model information objects
   * @returns {ModelRegistry} - For method chaining
   */
  registerModelsFromArray(modelsArray) {
    modelsArray.forEach(model => this.registerModel(model));
    return this;
  }
  
  /**
   * Get a list of all registered models
   * 
   * @returns {Array<Object>} - All registered models
   */
  getAllModels() {
    return Array.from(this.models.values());
  }
  
  /**
   * Get models filtered by tier (e.g., "free", "standard")
   * 
   * @param {string} tier - The tier to filter by
   * @returns {Array<Object>} - Models in the specified tier
   */
  getModelsByTier(tier) {
    return this.getAllModels().filter(model => 
      model.tiers && model.tiers.includes(tier)
    );
  }
  
  /**
   * Get models filtered by provider (e.g., "openai", "anthropic")
   * 
   * @param {string} provider - The provider to filter by
   * @returns {Array<Object>} - Models from the specified provider
   */
  getModelsByProvider(provider) {
    return this.getAllModels().filter(model => 
      model.provider === provider
    );
  }
  
  /**
   * Get models filtered by capability (e.g., "vision", "code")
   * 
   * @param {string} capability - The capability to filter by
   * @returns {Array<Object>} - Models with the specified capability
   */
  getModelsByCapability(capability) {
    return this.getAllModels().filter(model => 
      model.capabilities && model.capabilities.includes(capability)
    );
  }
  
  /**
   * Check if a model exists in the registry
   * 
   * @param {string} provider - Provider name 
   * @param {string} modelId - Model ID
   * @returns {boolean} - Whether the model exists
   */
  hasModel(provider, modelId) {
    return this.models.has(`${provider}:${modelId}`);
  }
  
  /**
   * Get a specific model by provider and ID
   * 
   * @param {string} provider - Provider name
   * @param {string} modelId - Model ID
   * @returns {Object|undefined} - The model or undefined if not found
   */
  getModel(provider, modelId) {
    return this.models.get(`${provider}:${modelId}`);
  }
}

/**
 * Input analyzer for determining requirements from a prompt
 */
class InputAnalyzer {
  constructor() {
    // Keywords for detecting specific requirements
    this.VISION_KEYWORDS = [
      'image', 'picture', 'photo', 'diagram', 'chart', 'screenshot', 'graph',
      'infographic', 'illustration', 'visual', 'look at this', 'analyze this image'
    ];
    
    this.CODE_KEYWORDS = [
      'code', 'programming', 'function', 'algorithm', 'javascript', 'python', 'java',
      'c++', 'typescript', 'html', 'css', 'react', 'node', 'express', 'coding',
      'bug', 'debug', 'script', 'implementation', 'software', 'developer', 'compile'
    ];
    
    this.MATH_KEYWORDS = [
      'math', 'calculation', 'equation', 'formula', 'calculus', 'algebra', 'statistics',
      'probability', 'numerical', 'computation', 'solve', 'geometric', 'matrix', 'vector'
    ];
    
    this.CREATIVE_KEYWORDS = [
      'creative', 'story', 'poem', 'fiction', 'narrative', 'script', 'screenplay',
      'artistic', 'imaginative', 'design', 'invent', 'create', 'novel', 'write'
    ];
    
    this.REASONING_KEYWORDS = [
      'explain', 'reasoning', 'logic', 'rationale', 'justify', 'argument', 'analyze',
      'deduce', 'infer', 'step-by-step', 'step by step', 'breakdown', 'systematic'
    ];
  }
  
  /**
   * Count the number of words in a text string
   * 
   * @param {string} text - Input text
   * @returns {number} - Word count
   */
  countWords(text) {
    return text.trim().split(/\s+/).filter(Boolean).length;
  }
  
  /**
   * Check if text contains any of the specified keywords
   * 
   * @param {string} text - Input text
   * @param {string[]} keywords - List of keywords to check
   * @returns {boolean} - True if any keyword is found
   */
  containsKeywords(text, keywords) {
    const lowerText = text.toLowerCase();
    return keywords.some(keyword => lowerText.includes(keyword.toLowerCase()));
  }
  
  /**
   * Estimate the number of tokens in the text
   * A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text
   * 
   * @param {string} text - Input text
   * @returns {number} - Estimated token count
   */
  estimateTokens(text) {
    return Math.max(
      Math.ceil(text.length / 4),
      Math.ceil(this.countWords(text) * 0.75)
    );
  }
  
  /**
   * Assess the complexity of a prompt on a scale of 1-5
   * 
   * @param {string} text - Input text
   * @returns {number} - Complexity rating (1-5)
   */
  assessComplexity(text) {
    const wordCount = this.countWords(text);
    const tokenCount = this.estimateTokens(text);
    
    // Base complexity on length
    let complexity = 1;
    
    if (wordCount > 500 || tokenCount > 750) complexity += 1;
    if (wordCount > 1000 || tokenCount > 1500) complexity += 1;
    
    // Increase complexity for combined requirements
    let requirementCount = 0;
    if (this.containsKeywords(text, this.CODE_KEYWORDS)) requirementCount++;
    if (this.containsKeywords(text, this.MATH_KEYWORDS)) requirementCount++;
    if (this.containsKeywords(text, this.REASONING_KEYWORDS)) requirementCount++;
    
    if (requirementCount >= 2) complexity += 1;
    if (requirementCount >= 3) complexity += 1;
    
    // Cap at 5
    return Math.min(complexity, 5);
  }
  
  /**
   * Analyze input requirements from the prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} - Requirements object
   */
  analyzeRequirements(prompt) {
    const tokenCount = this.estimateTokens(prompt);
    const wordCount = this.countWords(prompt);
    const needsVision = this.containsKeywords(prompt, this.VISION_KEYWORDS);
    const needsCode = this.containsKeywords(prompt, this.CODE_KEYWORDS);
    const needsMath = this.containsKeywords(prompt, this.MATH_KEYWORDS);
    const needsCreativity = this.containsKeywords(prompt, this.CREATIVE_KEYWORDS);
    const needsReasoning = this.containsKeywords(prompt, this.REASONING_KEYWORDS);
    const complexity = this.assessComplexity(prompt);
    
    // Context window requirement is a multiple of the input length plus room for response
    const minContextWindow = Math.max(tokenCount * 4, 1000);
    
    // Detect domains/categories from the prompt
    const domains = [];
    if (needsCode) domains.push('code');
    if (needsMath) domains.push('math');
    if (needsCreativity) domains.push('creative');
    if (needsReasoning) domains.push('reasoning');
    if (domains.length === 0) domains.push('general');
    
    return {
      tokenCount,
      wordCount,
      needsVision,
      needsCode,
      needsMath,
      needsCreativity,
      needsReasoning,
      complexity,
      minContextWindow,
      isMultimodal: needsVision,
      domains
    };
  }
}

/**
 * Model scorer for ranking models based on requirements
 */
class ModelScorer {
  constructor() {
    // Scoring weights for different attributes
    this.weights = {
      vision: 50,
      contextWindow: 20,
      intelligence: 10,
      code: 25,
      math: 25,
      reasoning: 30,
      creativity: 15,
      speed: 15,
      provider: {
        'openai': { code: 10 },
        'anthropic': { reasoning: 10, creativity: 10 },
        'vertex': { math: 5 },
        'xai': { reasoning: 5 }
      }
    };
  }
  
  /**
   * Calculate a score for a model based on requirements
   * 
   * @param {Object} model - Model object with attributes
   * @param {Object} requirements - Requirements from input analysis
   * @returns {Object} - Score and reasons
   */
  scoreModel(model, requirements) {
    let score = 0;
    const reasons = [];
    
    // Critical capabilities check - automatic disqualification
    if (requirements.needsVision && !model.capabilities.includes('vision')) {
      return { 
        score: -9999, 
        reasons: ['lacks required vision capability'] 
      };
    }
    
    // Context window check
    if (model.contextWindow && model.contextWindow >= requirements.minContextWindow) {
      score += this.weights.contextWindow;
    } else if (model.contextWindow && model.contextWindow < requirements.minContextWindow) {
      score -= this.weights.contextWindow * 1.5;
      reasons.push('limited context window');
    }
    
    // Vision capability
    if (requirements.needsVision && model.capabilities.includes('vision')) {
      score += this.weights.vision;
      reasons.push('supports image analysis');
    }
    
    // Intelligence match for complexity
    if (model.intelligence) {
      const intelligenceMatch = model.intelligence - requirements.complexity;
      if (intelligenceMatch >= 0) {
        score += intelligenceMatch * this.weights.intelligence + 20;
        if (intelligenceMatch > 1) {
          reasons.push(`high intelligence rating (${model.intelligence}/5)`);
        }
      } else {
        score -= Math.abs(intelligenceMatch) * this.weights.intelligence * 1.5;
        reasons.push(`lower intelligence rating (${model.intelligence}/5)`);
      }
    }
    
    // Task-specific capability bonuses
    if (requirements.needsCode && model.capabilities.includes('code')) {
      score += this.weights.code;
      reasons.push('strong code capabilities');
    }
    
    if (requirements.needsMath && model.intelligence && model.intelligence >= 4) {
      score += this.weights.math;
      reasons.push('strong math capabilities');
    }
    
    if (requirements.needsReasoning && model.capabilities.includes('reasoning')) {
      score += this.weights.reasoning;
      reasons.push('specialized reasoning capabilities');
    }
    
    if (requirements.needsCreativity && model.capabilities.includes('creativity')) {
      score += this.weights.creativity;
      reasons.push('creative capabilities');
    }
    
    // Speed bonus for less complex tasks
    if (requirements.complexity <= 3 && model.speed && model.speed >= 4) {
      score += this.weights.speed;
      reasons.push(`fast response times (${model.speed}/5)`);
    }
    
    // Provider-specific bonuses based on observed strengths
    requirements.domains.forEach(domain => {
      if (this.weights.provider[model.provider] && 
          this.weights.provider[model.provider][domain]) {
        score += this.weights.provider[model.provider][domain];
        reasons.push(`${model.provider}'s strength in ${domain}`);
      }
    });
    
    return { score, reasons };
  }
  
  /**
   * Generate a human-readable explanation for model selection
   * 
   * @param {Object} model - Selected model
   * @param {string[]} reasons - Reasons for selection
   * @returns {string} - Human-readable explanation
   */
  generateExplanation(model, reasons) {
    const displayName = model.displayName || model.modelId;
    let explanation = `Selected ${displayName} because it `;
    
    if (reasons.length > 0) {
      if (reasons.length === 1) {
        explanation += reasons[0];
      } else {
        const lastReason = reasons[reasons.length - 1];
        const otherReasons = reasons.slice(0, -1);
        explanation += otherReasons.join(", ") + ` and ${lastReason}`;
      }
    } else {
      explanation += "is well-suited for general tasks";
    }
    
    return explanation + ".";
  }
}

/**
 * Main GPToggle v2.0 class with model-agnostic implementation and contextualized intelligence
 */
class GPToggle {
  /**
   * Initialize GPToggle v2.0 with API keys, configuration, and contextualized intelligence
   * 
   * @param {Object} config - Configuration object
   * @param {Object} apiKeys - API keys for different providers
   */
  constructor(config = {}, apiKeys = {}) {
    this.apiKeys = apiKeys;
    this.config = config;
    this.registry = new ModelRegistry();
    this.analyzer = new InputAnalyzer();
    this.scorer = new ModelScorer();
    this.providerHandlers = new Map();
    
    // Contextualized Intelligence v2.0 components
    this.queryClassifier = new QueryClassifier();
    this.contextualEnhancer = new ContextualEnhancer();
    this.userProfiles = new Map(); // Store user profiles
    
    // Version info
    this.version = "2.0.0";
    
    // Register built-in fallback models
    this.registerFallbackModels();
  }
  
  /**
   * Register minimal fallback models for emergency cases
   */
  registerFallbackModels() {
    this.registry.registerModel({
      provider: "openai",
      modelId: "gpt-3.5-turbo",
      displayName: "GPT-3.5 Turbo",
      capabilities: ["text", "code"],
      strengths: { general: 3, code: 3 },
      tiers: ["free"],
      contextWindow: 16000,
      intelligence: 3,
      speed: 4
    });
    
    // Only register if we have the API key
    if (this.apiKeys.anthropic) {
      this.registry.registerModel({
        provider: "anthropic",
        modelId: "claude-instant-1",
        displayName: "Claude Instant",
        capabilities: ["text", "reasoning"],
        strengths: { general: 3, reasoning: 3 },
        tiers: ["free"],
        contextWindow: 16000,
        intelligence: 3,
        speed: 4
      });
    }
  }
  
  /**
   * Register an API handler for a provider
   * 
   * @param {string} provider - Provider name
   * @param {Function} handler - API handler function
   * @returns {GPToggle} - For method chaining
   */
  registerProviderHandler(provider, handler) {
    this.providerHandlers.set(provider, handler);
    return this;
  }
  
  /**
   * Register a model in the registry
   * 
   * @param {Object} model - Model information
   * @returns {GPToggle} - For method chaining
   */
  registerModel(model) {
    this.registry.registerModel(model);
    return this;
  }
  
  /**
   * Register multiple models at once
   * 
   * @param {Array} models - Array of model objects
   * @returns {GPToggle} - For method chaining
   */
  registerModels(models) {
    this.registry.registerModelsFromArray(models);
    return this;
  }
  
  /**
   * Recommend the best model for a prompt
   * 
   * @param {string} prompt - User prompt
   * @param {Object} options - Options (tier, etc.)
   * @returns {Object} - Recommendation with provider, model and reason
   */
  recommendModel(prompt, options = {}) {
    // Get input requirements
    const requirements = this.analyzer.analyzeRequirements(prompt);
    
    // Get eligible models based on tier
    const models = options.tier 
      ? this.registry.getModelsByTier(options.tier)
      : this.registry.getAllModels();
    
    if (models.length === 0) {
      return {
        provider: "openai",
        model: "gpt-3.5-turbo",
        reason: "No eligible models found, using fallback"
      };
    }
    
    // Score each model
    const scoredModels = models.map(model => {
      const { score, reasons } = this.scorer.scoreModel(model, requirements);
      return { model, score, reasons };
    });
    
    // Sort by score (descending)
    scoredModels.sort((a, b) => b.score - a.score);
    
    // Select the highest-scoring model
    const selected = scoredModels[0];
    
    // Generate explanation
    const reason = this.scorer.generateExplanation(
      selected.model, 
      selected.reasons
    );
    
    return {
      provider: selected.model.provider,
      model: selected.model.modelId,
      reason: reason,
      requirements,
      score: selected.score
    };
  }
  
  /**
   * Get recommendations for specific tasks within a prompt
   * 
   * @param {string} prompt - User prompt
   * @param {Object} options - Options (tier, etc.)
   * @returns {Object} - Overall and task-specific recommendations
   */
  getTaskRecommendations(prompt, options = {}) {
    // Get overall recommendation
    const overall = this.recommendModel(prompt, options);
    
    // Get all eligible models
    const models = options.tier 
      ? this.registry.getModelsByTier(options.tier)
      : this.registry.getAllModels();
    
    // Get requirements
    const requirements = this.analyzer.analyzeRequirements(prompt);
    
    // Score each model
    const scoredModels = models.map(model => {
      const { score, reasons } = this.scorer.scoreModel(model, requirements);
      return { model, score, reasons };
    });
    
    // Sort by score (descending)
    scoredModels.sort((a, b) => b.score - a.score);
    
    // Take top 3 models for recommendations
    const topModels = scoredModels.slice(0, 3);
    
    // Format recommendations
    const recommendations = topModels.map(scored => {
      const rec = {
        provider: scored.model.provider,
        model: scored.model.modelId,
        reason: this.scorer.generateExplanation(scored.model, scored.reasons),
      };
      
      if (scored.model.intelligence) {
        rec.strength = `Intelligence: ${scored.model.intelligence}/5`;
      }
      
      return rec;
    });
    
    return {
      overall,
      recommendations
    };
  }
  
  /**
   * Get a response from any provider
   * 
   * @param {string} prompt - User prompt
   * @param {string} [providerName] - Provider name (auto-selected if not provided)
   * @param {string} [modelName] - Model name (auto-selected if not provided)
   * @param {Object} [params] - Generation parameters
   * @returns {Promise<string>} - Generated response
   */
  async getResponse(prompt, providerName, modelName, params = {}) {
    // Auto-select model if not specified
    if (!providerName || !modelName) {
      const recommendation = this.recommendModel(prompt, params);
      providerName = providerName || recommendation.provider;
      modelName = modelName || recommendation.model;
    }
    
    // Check if API key is available
    if (!this.apiKeys[providerName]) {
      throw new Error(`API key for ${providerName} not found`);
    }
    
    // Use registered provider handler if available
    if (this.providerHandlers.has(providerName)) {
      return this.providerHandlers.get(providerName)(
        prompt, modelName, this.apiKeys[providerName], params
      );
    }
    
    // Fallback to built-in handlers based on provider
    switch(providerName) {
      case 'openai':
        return this.openaiGetResponse(prompt, modelName, params);
      case 'anthropic':
        return this.anthropicGetResponse(prompt, modelName, params);
      default:
        throw new Error(`Provider ${providerName} not implemented and no custom handler registered`);
    }
  }
  
  /**
   * Get a response using the OpenAI API
   * 
   * @param {string} prompt - User prompt
   * @param {string} model - Model name
   * @param {Object} params - Generation parameters
   * @returns {Promise<string>} - Generated response
   */
  async openaiGetResponse(prompt, model, params = {}) {
    // Implementation depends on environment (Node.js vs browser)
    // This is a simplified version - actual implementation would use OpenAI SDK
    try {
      const OpenAI = await import('openai');
      const client = new OpenAI.OpenAI({
        apiKey: this.apiKeys.openai
      });
      
      const response = await client.chat.completions.create({
        model: model,
        messages: [{ role: "user", content: prompt }],
        temperature: params.temperature || 0.7,
        max_tokens: params.max_tokens || 1000
      });
      
      return response.choices[0].message.content;
    } catch (error) {
      throw new Error(`OpenAI API Error: ${error.message}`);
    }
  }
  
  /**
   * Get a response using the Anthropic Claude API
   * 
   * @param {string} prompt - User prompt
   * @param {string} model - Model name
   * @param {Object} params - Generation parameters
   * @returns {Promise<string>} - Generated response
   */
  async anthropicGetResponse(prompt, model, params = {}) {
    // Implementation depends on environment (Node.js vs browser)
    // This is a simplified version - actual implementation would use Anthropic SDK
    try {
      const Anthropic = await import('anthropic');
      const client = new Anthropic.Anthropic({
        apiKey: this.apiKeys.anthropic
      });
      
      const response = await client.messages.create({
        model: model,
        max_tokens: params.max_tokens || 1000,
        temperature: params.temperature || 0.7,
        messages: [
          { role: "user", content: prompt }
        ]
      });
      
      return response.content[0].text;
    } catch (error) {
      throw new Error(`Anthropic API Error: ${error.message}`);
    }
  }
}

// Sample models registry
const sampleModels = [
  {
    provider: "openai",
    modelId: "gpt-4o",
    displayName: "GPT-4o",
    capabilities: ["text", "vision", "code", "reasoning", "creativity"],
    strengths: { general: 5, code: 5, math: 4, creativity: 4, reasoning: 5 },
    weaknesses: ["hallucination"],
    contextWindow: 128000,
    intelligence: 5,
    speed: 4,
    tiers: ["standard"],
    pricing: {
      inputTokens: 0.00005,
      outputTokens: 0.00015
    },
    knowledgeCutoff: "2023-04",
    released: "2023-05-13",
    deprecated: false
  },
  {
    provider: "anthropic",
    modelId: "claude-3-opus",
    displayName: "Claude 3 Opus",
    capabilities: ["text", "vision", "reasoning", "creativity"],
    strengths: { general: 5, reasoning: 5, math: 4, creativity: 5 },
    weaknesses: ["code"],
    contextWindow: 200000,
    intelligence: 5,
    speed: 3,
    tiers: ["standard"],
    pricing: {
      inputTokens: 0.00005,
      outputTokens: 0.00015
    },
    knowledgeCutoff: "2023-08",
    released: "2024-03-04",
    deprecated: false
  },
  {
    provider: "anthropic",
    modelId: "claude-3-sonnet",
    displayName: "Claude 3 Sonnet",
    capabilities: ["text", "vision", "reasoning", "creativity"],
    strengths: { general: 4, reasoning: 4, math: 3, creativity: 4 },
    weaknesses: ["code"],
    contextWindow: 200000,
    intelligence: 4,
    speed: 4,
    tiers: ["standard"],
    pricing: {
      inputTokens: 0.00003,
      outputTokens: 0.00010
    },
    knowledgeCutoff: "2023-08",
    released: "2024-03-04",
    deprecated: false
  },
  // Example of adding a model from a new provider
  {
    provider: "xai",
    modelId: "grok-2",
    displayName: "Grok 2",
    capabilities: ["text", "code", "reasoning"],
    strengths: { general: 4, reasoning: 4, code: 3 },
    contextWindow: 130000,
    intelligence: 4,
    speed: 4,
    tiers: ["standard"],
    pricing: {
      inputTokens: 0.00003,
      outputTokens: 0.00010
    },
    knowledgeCutoff: "2023-12",
    released: "2024-04-11",
    deprecated: false
  }
];

// Example usage (for Node.js and browsers)
async function example() {
  // Initialize with API keys
  const gptoggle = new GPToggle({}, {
    openai: process.env.OPENAI_API_KEY,
    anthropic: process.env.ANTHROPIC_API_KEY,
    xai: process.env.XAI_API_KEY
  });
  
  // Register example models
  gptoggle.registerModels(sampleModels);
  
  // Register a custom provider handler
  gptoggle.registerProviderHandler('xai', async (prompt, model, apiKey, params) => {
    // Custom implementation for XAI/Grok API would go here
    return `This is a custom XAI handler responding to: ${prompt}`;
  });
  
  // Get recommendation for a prompt
  const recommendation = gptoggle.recommendModel(
    'Create a Python function that analyzes images to detect objects'
  );
  
  console.log('Recommendation:', recommendation);
  
  // Get task-specific recommendations
  const taskRecs = gptoggle.getTaskRecommendations(
    'Create a Python function that analyzes images to detect objects'
  );
  
  console.log('Task Recommendations:', JSON.stringify(taskRecs, null, 2));
  
  // Get a response (would call the API in a real implementation)
  const response = await gptoggle.getResponse(
    'Create a Python function that analyzes images to detect objects'
  );
  
  console.log('Response:', response);
}

// Export for Node.js
if (typeof module !== 'undefined') {
  module.exports = { GPToggle, ModelRegistry, InputAnalyzer, ModelScorer, sampleModels };
}

// For browsers
if (typeof window !== 'undefined') {
  window.GPToggle = GPToggle;
  window.ModelRegistry = ModelRegistry;
  window.InputAnalyzer = InputAnalyzer;
  window.ModelScorer = ModelScorer;
  window.sampleModels = sampleModels;
}