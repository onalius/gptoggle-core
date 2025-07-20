/**
 * Model Registry
 * 
 * Manages the registry of available AI models, their capabilities, and provides
 * model selection and response generation functionality.
 * 
 * @version 2.0.0
 */

import { Logger } from '../utils/logger';
import { QueryType } from '../context/queryClassifier';

export interface ModelMetadata {
  provider: string;
  modelId: string;
  displayName: string;
  capabilities: string[];
  strengths: Record<string, number>; // 1-5 scale
  tier: 'basic' | 'standard' | 'premium' | 'enterprise';
  contextWindow: number;
  intelligence: number; // 1-5 scale
  speed: number; // 1-5 scale
  costPerToken?: number;
  specializations?: string[];
  features?: string[]; // vision, code, math, etc.
}

export interface ModelSelectionCriteria {
  queryType: QueryType;
  requiredFeatures: string[];
  userAccessLevel: 'basic' | 'premium' | 'enterprise';
  prioritizeSpeed?: boolean;
  maxCost?: number;
}

export interface GenerationRequest {
  model: ModelMetadata;
  query: string;
  parameters: {
    temperature: number;
    maxTokens: number;
    streaming: boolean;
  };
}

export interface GenerationResponse {
  content: string;
  tokensUsed?: number;
  cost?: number;
  responseTime: number;
  model: string;
  provider: string;
}

export class ModelRegistry {
  private models: Map<string, ModelMetadata> = new Map();
  private logger: Logger;

  constructor() {
    this.logger = new Logger();
    this.initializeDefaultModels();
  }

  /**
   * Initialize with default model configurations
   */
  private initializeDefaultModels(): void {
    const defaultModels: ModelMetadata[] = [
      // OpenAI Models
      {
        provider: 'openai',
        modelId: 'gpt-4o',
        displayName: 'GPT-4o',
        capabilities: ['text', 'vision', 'code', 'reasoning', 'math'],
        strengths: { general: 5, code: 5, reasoning: 5, creativity: 4, math: 4 },
        tier: 'standard',
        contextWindow: 128000,
        intelligence: 5,
        speed: 3,
        costPerToken: 0.000015,
        specializations: ['general_purpose', 'code_generation', 'analysis'],
        features: ['vision', 'code', 'math', 'reasoning']
      },
      {
        provider: 'openai',
        modelId: 'gpt-4-turbo',
        displayName: 'GPT-4 Turbo',
        capabilities: ['text', 'vision', 'code', 'reasoning'],
        strengths: { general: 5, code: 4, reasoning: 5, creativity: 4 },
        tier: 'standard',
        contextWindow: 128000,
        intelligence: 5,
        speed: 2,
        costPerToken: 0.000010,
        specializations: ['reasoning', 'analysis', 'writing'],
        features: ['vision', 'code']
      },
      {
        provider: 'openai',
        modelId: 'gpt-3.5-turbo',
        displayName: 'GPT-3.5 Turbo',
        capabilities: ['text', 'code'],
        strengths: { general: 4, code: 3, reasoning: 3, creativity: 3 },
        tier: 'basic',
        contextWindow: 16385,
        intelligence: 3,
        speed: 5,
        costPerToken: 0.0000015,
        specializations: ['general_purpose', 'quick_responses'],
        features: ['code']
      },

      // Anthropic Models
      {
        provider: 'anthropic',
        modelId: 'claude-3-opus-20240229',
        displayName: 'Claude 3 Opus',
        capabilities: ['text', 'vision', 'reasoning', 'creativity', 'analysis'],
        strengths: { general: 5, reasoning: 5, creativity: 5, code: 4, writing: 5 },
        tier: 'premium',
        contextWindow: 200000,
        intelligence: 5,
        speed: 2,
        costPerToken: 0.000075,
        specializations: ['reasoning', 'creative_writing', 'analysis'],
        features: ['vision', 'long_context']
      },
      {
        provider: 'anthropic',
        modelId: 'claude-3-sonnet-20240229',
        displayName: 'Claude 3 Sonnet',
        capabilities: ['text', 'vision', 'reasoning', 'code'],
        strengths: { general: 4, reasoning: 4, creativity: 4, code: 4 },
        tier: 'standard',
        contextWindow: 200000,
        intelligence: 4,
        speed: 3,
        costPerToken: 0.000015,
        specializations: ['balanced_performance', 'coding', 'writing'],
        features: ['vision', 'long_context']
      },

      // Google Models
      {
        provider: 'google',
        modelId: 'gemini-1.5-pro',
        displayName: 'Gemini 1.5 Pro',
        capabilities: ['text', 'vision', 'code', 'math', 'reasoning'],
        strengths: { general: 4, math: 5, code: 4, reasoning: 4, multimodal: 5 },
        tier: 'standard',
        contextWindow: 2097152,
        intelligence: 4,
        speed: 3,
        costPerToken: 0.0000125,
        specializations: ['mathematics', 'multimodal', 'long_context'],
        features: ['vision', 'math', 'ultra_long_context']
      },
      {
        provider: 'google',
        modelId: 'gemini-1.5-flash',
        displayName: 'Gemini 1.5 Flash',
        capabilities: ['text', 'vision', 'code'],
        strengths: { general: 3, code: 3, speed: 5, multimodal: 4 },
        tier: 'basic',
        contextWindow: 1048576,
        intelligence: 3,
        speed: 5,
        costPerToken: 0.000001,
        specializations: ['fast_responses', 'multimodal'],
        features: ['vision', 'speed']
      },

      // xAI Models
      {
        provider: 'xai',
        modelId: 'grok-2',
        displayName: 'Grok 2',
        capabilities: ['text', 'reasoning', 'real_time'],
        strengths: { general: 4, reasoning: 4, real_time: 5, personality: 5 },
        tier: 'premium',
        contextWindow: 131072,
        intelligence: 4,
        speed: 3,
        costPerToken: 0.000020,
        specializations: ['real_time_info', 'personality', 'current_events'],
        features: ['real_time', 'personality']
      }
    ];

    defaultModels.forEach(model => {
      this.registerModel(model);
    });

    this.logger.info(`Initialized model registry with ${defaultModels.length} default models`);
  }

  /**
   * Register a new model in the registry
   */
  registerModel(model: ModelMetadata): void {
    const modelKey = `${model.provider}:${model.modelId}`;
    this.models.set(modelKey, model);
    this.logger.debug(`Registered model: ${modelKey}`);
  }

  /**
   * Get models by capability requirements
   */
  async getModelsByCapability(criteria: ModelSelectionCriteria): Promise<ModelMetadata[]> {
    const availableModels = Array.from(this.models.values());

    return availableModels.filter(model => {
      // Check access level
      if (!this.hasAccess(model, criteria.userAccessLevel)) {
        return false;
      }

      // Check required features
      if (criteria.requiredFeatures.length > 0) {
        const hasAllFeatures = criteria.requiredFeatures.every(feature =>
          model.features?.includes(feature) || model.capabilities.includes(feature)
        );
        if (!hasAllFeatures) {
          return false;
        }
      }

      // Check if model is suitable for query type
      const queryTypeCapability = this.getQueryTypeCapability(criteria.queryType);
      if (queryTypeCapability && !model.capabilities.includes(queryTypeCapability)) {
        // Check if model has relevant strength
        const strength = model.strengths[criteria.queryType] || model.strengths.general || 0;
        if (strength < 3) {
          return false;
        }
      }

      return true;
    });
  }

  /**
   * Generate response using specified model
   */
  async generateResponse(request: GenerationRequest): Promise<GenerationResponse> {
    const startTime = Date.now();
    
    try {
      // This would typically call the actual AI provider API
      // For now, we'll simulate the response generation
      const response = await this.callProviderAPI(request);
      
      const responseTime = Date.now() - startTime;
      
      return {
        content: response.content,
        tokensUsed: response.tokensUsed,
        cost: this.calculateCost(request.model, response.tokensUsed || 0),
        responseTime,
        model: request.model.modelId,
        provider: request.model.provider
      };

    } catch (error) {
      this.logger.error(`Failed to generate response with ${request.model.provider}:${request.model.modelId}: ${error.message}`);
      throw new Error(`Model generation failed: ${error.message}`);
    }
  }

  /**
   * Get all available models
   */
  getAvailableModels(): ModelMetadata[] {
    return Array.from(this.models.values());
  }

  /**
   * Get model by provider and ID
   */
  getModel(provider: string, modelId: string): ModelMetadata | undefined {
    return this.models.get(`${provider}:${modelId}`);
  }

  /**
   * Get models filtered by access level
   */
  getModelsByAccessLevel(accessLevel: 'basic' | 'premium' | 'enterprise'): ModelMetadata[] {
    return Array.from(this.models.values()).filter(model => 
      this.hasAccess(model, accessLevel)
    );
  }

  /**
   * Check if user has access to a model
   */
  private hasAccess(model: ModelMetadata, userAccessLevel: 'basic' | 'premium' | 'enterprise'): boolean {
    const accessHierarchy = {
      'basic': ['basic'],
      'premium': ['basic', 'standard', 'premium'],
      'enterprise': ['basic', 'standard', 'premium', 'enterprise']
    };

    return accessHierarchy[userAccessLevel].includes(model.tier);
  }

  /**
   * Map query type to required capability
   */
  private getQueryTypeCapability(queryType: QueryType): string | undefined {
    const capabilityMap: Record<QueryType, string | undefined> = {
      'code': 'code',
      'mathematical': 'math',
      'creative': 'creativity',
      'analytical': 'reasoning',
      'factual': 'text',
      'legal': 'reasoning',
      'emotional': 'text',
      'educational': 'text',
      'conversational': 'text',
      'technical': 'reasoning',
      'business': 'reasoning',
      'health': 'reasoning',
      'general': undefined
    };

    return capabilityMap[queryType];
  }

  /**
   * Calculate cost based on model and tokens used
   */
  private calculateCost(model: ModelMetadata, tokensUsed: number): number | undefined {
    if (!model.costPerToken) {
      return undefined;
    }

    return model.costPerToken * tokensUsed;
  }

  /**
   * Simulate calling provider API (placeholder implementation)
   */
  private async callProviderAPI(request: GenerationRequest): Promise<{
    content: string;
    tokensUsed?: number;
  }> {
    // This is a placeholder implementation
    // In a real implementation, this would call the actual AI provider APIs
    
    const { model, query, parameters } = request;
    
    // Simulate API call delay based on model speed
    const delay = Math.max(500, (6 - model.speed) * 1000);
    await new Promise(resolve => setTimeout(resolve, delay));

    // Generate a simulated response
    const simulatedResponse = this.generateSimulatedResponse(query, model);
    const estimatedTokens = Math.ceil(simulatedResponse.length / 4); // Rough token estimation

    return {
      content: simulatedResponse,
      tokensUsed: estimatedTokens
    };
  }

  /**
   * Generate a simulated response for testing
   */
  private generateSimulatedResponse(query: string, model: ModelMetadata): string {
    return `This is a simulated response from ${model.displayName} for the query: "${query.substring(0, 50)}${query.length > 50 ? '...' : ''}". 

This response demonstrates the contextualized intelligence capabilities of GPToggle-core v2.0. The system has:
- Classified your query type
- Applied contextual enhancements based on your profile
- Selected the optimal model (${model.displayName}) for this task
- Generated this personalized response

In a real implementation, this would be the actual AI model response from ${model.provider}.`;
  }

  /**
   * Get model recommendations based on query characteristics
   */
  getModelRecommendations(queryType: QueryType, userAccessLevel: 'basic' | 'premium' | 'enterprise'): ModelMetadata[] {
    const available = this.getModelsByAccessLevel(userAccessLevel);
    
    // Score models based on their suitability for the query type
    const scored = available.map(model => ({
      model,
      score: this.scoreModelForQueryType(model, queryType)
    }));

    // Sort by score and return top recommendations
    scored.sort((a, b) => b.score - a.score);
    
    return scored.slice(0, 3).map(item => item.model);
  }

  /**
   * Score a model's suitability for a query type
   */
  private scoreModelForQueryType(model: ModelMetadata, queryType: QueryType): number {
    let score = 0;

    // Base score from model's strength in this query type
    const queryTypeStrength = model.strengths[queryType] || 0;
    score += queryTypeStrength * 20;

    // General intelligence bonus
    score += model.intelligence * 5;

    // Capability match bonus
    const capability = this.getQueryTypeCapability(queryType);
    if (capability && model.capabilities.includes(capability)) {
      score += 15;
    }

    // Feature match bonus
    if (model.features) {
      const relevantFeatures = this.getRelevantFeatures(queryType);
      const matchingFeatures = model.features.filter(f => relevantFeatures.includes(f));
      score += matchingFeatures.length * 5;
    }

    return score;
  }

  /**
   * Get relevant features for a query type
   */
  private getRelevantFeatures(queryType: QueryType): string[] {
    const featureMap: Record<QueryType, string[]> = {
      'code': ['code'],
      'mathematical': ['math'],
      'analytical': ['reasoning'],
      'creative': ['personality'],
      'factual': ['real_time'],
      'legal': ['reasoning'],
      'emotional': ['personality'],
      'educational': ['reasoning'],
      'conversational': ['personality'],
      'technical': ['code', 'reasoning'],
      'business': ['reasoning', 'real_time'],
      'health': ['reasoning'],
      'general': []
    };

    return featureMap[queryType] || [];
  }
}