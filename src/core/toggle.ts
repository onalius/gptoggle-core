/**
 * Enhanced Toggle Function for Contextualized Intelligence
 * 
 * This is the core toggle function that upgrades GPToggle from a simple model-selection
 * utility into a fully contextualized intelligence system.
 * 
 * @version 2.0.0
 */

import { UserProfile } from '../profile/userProfileService';
import { QueryTypeClassifier } from '../context/queryClassifier';
import { ContextualHelperManager } from '../context/contextualHelpers';
import { ModelRegistry } from './modelRegistry';
import { Logger } from '../utils/logger';

export interface ToggleRequest {
  query: string;
  userProfile: UserProfile;
  queryType?: string;
  overrideModel?: string;
  parameters?: {
    temperature?: number;
    maxTokens?: number;
    streaming?: boolean;
  };
}

export interface ToggleResponse {
  response: string;
  modelUsed: string;
  provider: string;
  queryType: string;
  contextualEnhancements: string[];
  suggestedFollowUp?: string;
  metadata: {
    processingTime: number;
    tokensUsed?: number;
    confidence: number;
  };
}

export class Toggle {
  private queryClassifier: QueryTypeClassifier;
  private helperManager: ContextualHelperManager;
  private modelRegistry: ModelRegistry;
  private logger: Logger;

  constructor() {
    this.queryClassifier = new QueryTypeClassifier();
    this.helperManager = new ContextualHelperManager();
    this.modelRegistry = new ModelRegistry();
    this.logger = new Logger();
  }

  /**
   * Main toggle function - the heart of contextualized intelligence
   * 
   * @param request - The toggle request containing query, user profile, and options
   * @returns Promise<ToggleResponse> - The contextualized response
   */
  async toggle(request: ToggleRequest): Promise<ToggleResponse> {
    const startTime = Date.now();
    
    try {
      // Step 1: Classify the query type if not provided
      const queryType = request.queryType || await this.queryClassifier.classifyQuery(request.query);
      
      this.logger.debug(`Query classified as: ${queryType}`);

      // Step 2: Apply contextual enhancements based on user profile and query type
      const enhancedQuery = await this.helperManager.applyContextualHelpers({
        originalQuery: request.query,
        queryType,
        userProfile: request.userProfile,
        tone: request.userProfile.tone,
        domainExpertise: request.userProfile.domainExpertise
      });

      this.logger.debug(`Query enhanced: ${enhancedQuery.enhancedQuery.substring(0, 100)}...`);

      // Step 3: Select the most appropriate model
      const selectedModel = request.overrideModel || await this.selectOptimalModel({
        query: enhancedQuery.enhancedQuery,
        queryType,
        userProfile: request.userProfile,
        enhancementContext: enhancedQuery.appliedEnhancements
      });

      this.logger.debug(`Model selected: ${selectedModel.provider}:${selectedModel.modelId}`);

      // Step 4: Generate response using the selected model
      const modelResponse = await this.modelRegistry.generateResponse({
        model: selectedModel,
        query: enhancedQuery.enhancedQuery,
        parameters: {
          temperature: request.parameters?.temperature ?? this.getDefaultTemperature(queryType),
          maxTokens: request.parameters?.maxTokens ?? this.getDefaultMaxTokens(queryType),
          streaming: request.parameters?.streaming ?? false
        }
      });

      // Step 5: Apply post-processing based on user preferences
      const finalResponse = await this.postProcessResponse({
        response: modelResponse.content,
        userProfile: request.userProfile,
        queryType,
        originalQuery: request.query
      });

      // Step 6: Generate follow-up suggestions
      const followUpSuggestion = await this.generateFollowUpSuggestion({
        originalQuery: request.query,
        response: finalResponse,
        queryType,
        userProfile: request.userProfile
      });

      const processingTime = Date.now() - startTime;

      return {
        response: finalResponse,
        modelUsed: selectedModel.modelId,
        provider: selectedModel.provider,
        queryType,
        contextualEnhancements: enhancedQuery.appliedEnhancements,
        suggestedFollowUp: followUpSuggestion,
        metadata: {
          processingTime,
          tokensUsed: modelResponse.tokensUsed,
          confidence: this.calculateConfidence(queryType, selectedModel, enhancedQuery.appliedEnhancements)
        }
      };

    } catch (error) {
      this.logger.error(`Toggle function error: ${error.message}`);
      throw new Error(`Failed to process toggle request: ${error.message}`);
    }
  }

  /**
   * Select the optimal model based on query characteristics and user preferences
   */
  private async selectOptimalModel(context: {
    query: string;
    queryType: string;
    userProfile: UserProfile;
    enhancementContext: string[];
  }): Promise<any> {
    
    // Get user's model preferences if they have premium access
    const userPreferences = context.userProfile.access.level === 'premium' 
      ? context.userProfile.preferences?.preferredModels 
      : undefined;

    // Get models capable of handling this query type
    const capableModels = await this.modelRegistry.getModelsByCapability({
      queryType: context.queryType,
      requiredFeatures: this.extractRequiredFeatures(context.query),
      userAccessLevel: context.userProfile.access.level
    });

    if (capableModels.length === 0) {
      throw new Error(`No available models for query type: ${context.queryType}`);
    }

    // Score models based on multiple factors
    const scoredModels = capableModels.map(model => ({
      model,
      score: this.scoreModel(model, context)
    }));

    // Sort by score and return the best match
    scoredModels.sort((a, b) => b.score - a.score);
    
    this.logger.debug(`Model scores: ${scoredModels.map(m => `${m.model.modelId}:${m.score}`).join(', ')}`);

    return scoredModels[0].model;
  }

  /**
   * Score a model based on its suitability for the current context
   */
  private scoreModel(model: any, context: {
    query: string;
    queryType: string;
    userProfile: UserProfile;
    enhancementContext: string[];
  }): number {
    let score = 0;

    // Base capability score
    const capabilities = model.capabilities || [];
    if (capabilities.includes(context.queryType)) {
      score += 50;
    }

    // Strength alignment
    const strengths = model.strengths || {};
    const queryTypeStrength = strengths[context.queryType] || strengths.general || 0;
    score += queryTypeStrength * 10;

    // User domain expertise bonus
    if (context.userProfile.domainExpertise.some(domain => 
        capabilities.includes(domain) || model.specializations?.includes(domain))) {
      score += 20;
    }

    // Premium model access
    if (context.userProfile.access.level === 'premium' && model.tier === 'premium') {
      score += 15;
    }

    // Speed vs quality preference
    if (context.userProfile.preferences?.prioritizeSpeed && model.speed > 3) {
      score += 10;
    } else if (!context.userProfile.preferences?.prioritizeSpeed && model.intelligence > 4) {
      score += 10;
    }

    // Recent usage patterns (from memory)
    const recentModels = context.userProfile.memory?.recentModels || [];
    if (recentModels.includes(model.modelId)) {
      score += 5; // Slight preference for familiar models
    }

    return score;
  }

  /**
   * Extract required features from the query
   */
  private extractRequiredFeatures(query: string): string[] {
    const features = [];
    
    if (query.toLowerCase().includes('image') || query.toLowerCase().includes('visual')) {
      features.push('vision');
    }
    if (query.toLowerCase().includes('code') || query.toLowerCase().includes('program')) {
      features.push('code');
    }
    if (query.toLowerCase().includes('math') || query.toLowerCase().includes('calculate')) {
      features.push('math');
    }
    if (query.length > 2000) {
      features.push('long_context');
    }

    return features;
  }

  /**
   * Get default temperature based on query type
   */
  private getDefaultTemperature(queryType: string): number {
    const temperatureMap: Record<string, number> = {
      'creative': 0.9,
      'factual': 0.1,
      'code': 0.2,
      'legal': 0.1,
      'emotional': 0.7,
      'analytical': 0.3
    };

    return temperatureMap[queryType as string] || 0.7;
  }

  /**
   * Get default max tokens based on query type
   */
  private getDefaultMaxTokens(queryType: string): number {
    const tokenMap: Record<string, number> = {
      'creative': 2000,
      'factual': 1000,
      'code': 1500,
      'legal': 2500,
      'emotional': 1200,
      'analytical': 1800
    };

    return tokenMap[queryType as string] || 1000;
  }

  /**
   * Post-process the response based on user preferences
   */
  private async postProcessResponse(context: {
    response: string;
    userProfile: UserProfile;
    queryType: string;
    originalQuery: string;
  }): Promise<string> {
    let processedResponse = context.response;

    // Apply tone adjustments if needed
    if (context.userProfile.tone !== 'casual') {
      processedResponse = await this.adjustResponseTone(processedResponse, context.userProfile.tone);
    }

    // Add disclaimers for legal queries
    if (context.queryType === 'legal') {
      processedResponse += '\n\n⚖️ Disclaimer: This response is for informational purposes only and does not constitute legal advice. Please consult with a qualified attorney for legal matters.';
    }

    // Add relevant expertise context
    if (context.userProfile.domainExpertise.length > 0) {
      const relevantExpertise = context.userProfile.domainExpertise.find(domain =>
        context.originalQuery.toLowerCase().includes(domain) || 
        processedResponse.toLowerCase().includes(domain)
      );
      
      if (relevantExpertise) {
        processedResponse += `\n\n💡 Given your expertise in ${relevantExpertise}, you might also consider...`;
      }
    }

    return processedResponse;
  }

  /**
   * Adjust response tone based on user preference
   */
  private async adjustResponseTone(response: string, tone: 'formal' | 'casual' | 'witty'): Promise<string> {
    // This would typically use a lightweight tone adjustment model or rules
    // For now, we'll use simple transformations
    
    switch (tone) {
      case 'formal':
        return response.replace(/\b(can't|won't|don't)\b/g, (match) => {
          const formal = { "can't": "cannot", "won't": "will not", "don't": "do not" };
          return formal[match] || match;
        });
        
      case 'witty':
        // Add occasional humor markers or clever turns of phrase
        return response + ' 😉';
        
      default:
        return response;
    }
  }

  /**
   * Generate follow-up suggestions based on the conversation
   */
  private async generateFollowUpSuggestion(context: {
    originalQuery: string;
    response: string;
    queryType: string;
    userProfile: UserProfile;
  }): Promise<string | undefined> {
    
    const followUpMap: Record<string, string[]> = {
      'code': [
        'Would you like me to explain how this code works?',
        'Should I help you test this implementation?',
        'Would you like suggestions for optimizing this code?'
      ],
      'creative': [
        'Would you like me to develop this idea further?',
        'Should I suggest alternative creative approaches?',
        'Would you like help refining the style or tone?'
      ],
      'factual': [
        'Would you like more detailed information on any aspect?',
        'Should I provide related topics you might find interesting?',
        'Would you like me to fact-check this information?'
      ],
      'analytical': [
        'Would you like me to analyze this from a different angle?',
        'Should I provide data visualization suggestions?',
        'Would you like help interpreting these results?'
      ]
    };

    const suggestions = followUpMap[context.queryType];
    if (suggestions && suggestions.length > 0) {
      // Randomly select a relevant follow-up
      const randomIndex = Math.floor(Math.random() * suggestions.length);
      return suggestions[randomIndex];
    }

    return undefined;
  }

  /**
   * Calculate confidence score for the response
   */
  private calculateConfidence(queryType: string, model: any, enhancements: string[]): number {
    let confidence = 0.7; // Base confidence

    // Model strength alignment
    const modelStrength = model.strengths?.[queryType] || model.strengths?.general || 3;
    confidence += (modelStrength - 3) * 0.1;

    // Enhancement boost
    confidence += enhancements.length * 0.05;

    // Cap at 0.95 to maintain humility
    return Math.min(0.95, Math.max(0.1, confidence));
  }
}

// Export default instance
export const toggle = new Toggle();