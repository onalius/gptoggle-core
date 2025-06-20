/**
 * GPToggle Model-Agnostic Implementation
 * 
 * This file demonstrates a model-agnostic approach to the GPToggle library
 * that can be used as a reference for updating the core implementation.
 * 
 * Key features:
 * - Dynamic model registry
 * - Capability-based model selection
 * - Rich attribute scoring system
 * - Provider-agnostic interface
 * 
 * @version 2.0.0
 */

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
    return text.split(/\s+/).filter(Boolean).length;
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
        'gemini': { math: 5 },
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
    let explanation = `Selected ${model.displayName || model.modelId} because it `;
    
    if (reasons.length > 0) {
      explanation += reasons.join(", ").replace(/,([^,]*)$/, ' and$1');
    } else {
      explanation += "is well-suited for general tasks";
    }
    
    return explanation + ".";
  }
}

/**
 * GPToggle class with model-agnostic implementation
 */
class GPToggle {
  /**
   * Initialize GPToggle with API keys and configuration
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
    if (this.apiKeys.claude) {
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
    const overallRecommendation = this.recommendModel(prompt, options);
    
    // For model-agnostic approach, we analyze the requirements
    // and provide recommendations for different aspects
    const requirements = this.analyzer.analyzeRequirements(prompt);
    
    const taskRecommendations = [];
    
    // Add specific recommendations for detected domains
    requirements.domains.forEach(domain => {
      const domainModels = this.registry.getAllModels().filter(model => 
        model.capabilities && model.capabilities.includes(domain)
      );
      
      if (domainModels.length > 0) {
        // Score models for this specific domain
        const scoredDomainModels = domainModels.map(model => {
          const { score, reasons } = this.scorer.scoreModel(model, requirements);
          return { model, score, reasons };
        });
        
        scoredDomainModels.sort((a, b) => b.score - a.score);
        
        taskRecommendations.push({
          domain: domain,
          description: `Models optimized for ${domain} tasks`,
          recommendations: scoredDomainModels.slice(0, 3).map(scored => ({
            provider: scored.model.provider,
            model: scored.model.modelId,
            displayName: scored.model.displayName,
            reasons: scored.reasons,
            score: scored.score
          }))
        });
      }
    });
    
    return {
      overallRecommendation,
      taskRecommendations,
      requirements
    };
  }
  
  /**
   * Get available providers based on API keys
   * 
   * @returns {string[]} - List of available providers
   */
  getAvailableProviders() {
    return Object.keys(this.apiKeys).filter(key => this.apiKeys[key]);
  }
  
  /**
   * Get available models filtered by various criteria
   * 
   * @param {Object} filters - Filter criteria
   * @returns {Array} - Filtered models
   */
  getAvailableModels(filters = {}) {
    let models = this.registry.getAllModels();
    
    // Filter by available API keys
    const availableProviders = this.getAvailableProviders();
    models = models.filter(model => availableProviders.includes(model.provider));
    
    // Apply additional filters
    if (filters.tier) {
      models = models.filter(model => 
        model.tiers && model.tiers.includes(filters.tier)
      );
    }
    
    if (filters.capability) {
      models = models.filter(model => 
        model.capabilities && model.capabilities.includes(filters.capability)
      );
    }
    
    if (filters.provider) {
      models = models.filter(model => model.provider === filters.provider);
    }
    
    return models;
  }
}

// Export for use in Node.js and browser environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GPToggle, ModelRegistry, InputAnalyzer, ModelScorer };
} else if (typeof window !== 'undefined') {
  window.GPToggle = GPToggle;
  window.ModelRegistry = ModelRegistry;
  window.InputAnalyzer = InputAnalyzer;
  window.ModelScorer = ModelScorer;
}