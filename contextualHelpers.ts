/**
 * Contextual Helper Manager
 * 
 * Applies contextual enhancements to user queries based on query type,
 * user profile, and domain expertise to improve AI response quality.
 * 
 * @version 2.0.0
 */

import { UserProfile } from '../profile/userProfileService';
import { QueryType } from './queryClassifier';
import { Logger } from '../utils/logger';

export interface ContextualEnhancementRequest {
  originalQuery: string;
  queryType: QueryType;
  userProfile: UserProfile;
  tone: 'formal' | 'casual' | 'witty';
  domainExpertise: string[];
}

export interface ContextualEnhancementResult {
  enhancedQuery: string;
  appliedEnhancements: string[];
  metadata: {
    originalLength: number;
    enhancedLength: number;
    enhancementCount: number;
  };
}

export class ContextualHelperManager {
  private logger: Logger;

  constructor() {
    this.logger = new Logger();
  }

  /**
   * Apply contextual enhancements to a query
   */
  async applyContextualHelpers(request: ContextualEnhancementRequest): Promise<ContextualEnhancementResult> {
    const { originalQuery, queryType, userProfile } = request;
    const appliedEnhancements: string[] = [];
    let enhancedQuery = originalQuery;

    try {
      // Apply query type specific enhancements
      const typeEnhancement = await this.applyQueryTypeEnhancement(enhancedQuery, queryType);
      if (typeEnhancement.enhanced !== enhancedQuery) {
        enhancedQuery = typeEnhancement.enhanced;
        appliedEnhancements.push(typeEnhancement.description);
      }

      // Apply user profile enhancements
      const profileEnhancement = await this.applyUserProfileEnhancement(enhancedQuery, userProfile);
      if (profileEnhancement.enhanced !== enhancedQuery) {
        enhancedQuery = profileEnhancement.enhanced;
        appliedEnhancements.push(profileEnhancement.description);
      }

      // Apply domain expertise enhancements
      const domainEnhancement = await this.applyDomainExpertiseEnhancement(
        enhancedQuery, 
        userProfile.domainExpertise,
        queryType
      );
      if (domainEnhancement.enhanced !== enhancedQuery) {
        enhancedQuery = domainEnhancement.enhanced;
        appliedEnhancements.push(domainEnhancement.description);
      }

      // Apply tone adjustments
      const toneEnhancement = await this.applyToneEnhancement(enhancedQuery, userProfile.tone);
      if (toneEnhancement.enhanced !== enhancedQuery) {
        enhancedQuery = toneEnhancement.enhanced;
        appliedEnhancements.push(toneEnhancement.description);
      }

      // Apply verbosity preferences
      const verbosityEnhancement = await this.applyVerbosityEnhancement(
        enhancedQuery,
        userProfile.preferences?.verbosityLevel || 'moderate'
      );
      if (verbosityEnhancement.enhanced !== enhancedQuery) {
        enhancedQuery = verbosityEnhancement.enhanced;
        appliedEnhancements.push(verbosityEnhancement.description);
      }

      this.logger.debug(`Applied ${appliedEnhancements.length} contextual enhancements`);

      return {
        enhancedQuery,
        appliedEnhancements,
        metadata: {
          originalLength: originalQuery.length,
          enhancedLength: enhancedQuery.length,
          enhancementCount: appliedEnhancements.length
        }
      };

    } catch (error) {
      this.logger.error(`Error applying contextual helpers: ${error.message}`);
      return {
        enhancedQuery: originalQuery,
        appliedEnhancements: [],
        metadata: {
          originalLength: originalQuery.length,
          enhancedLength: originalQuery.length,
          enhancementCount: 0
        }
      };
    }
  }

  /**
   * Apply query type specific enhancements
   */
  private async applyQueryTypeEnhancement(query: string, queryType: QueryType): Promise<{
    enhanced: string;
    description: string;
  }> {
    const enhancements: Record<QueryType, (query: string) => string> = {
      factual: (q) => `You are a knowledgeable assistant providing accurate, well-sourced information. ${q} Please provide factual, verifiable information and cite sources when possible.`,
      
      creative: (q) => `You are a creative assistant helping with imaginative tasks. Think outside the box and be innovative. ${q}`,
      
      legal: (q) => `You are a helpful legal information assistant. ${q} Please include relevant disclaimers and note that this is informational only, not legal advice.`,
      
      emotional: (q) => `You are a supportive and empathetic assistant. Please respond with care and understanding. ${q} Provide thoughtful, compassionate guidance.`,
      
      analytical: (q) => `You are an analytical assistant skilled at breaking down complex problems. ${q} Please provide structured analysis with clear reasoning.`,
      
      code: (q) => `You are a programming assistant with expertise in software development. ${q} Please provide working code with explanations and best practices.`,
      
      mathematical: (q) => `You are a mathematics expert. ${q} Please show your work step-by-step and explain the mathematical concepts involved.`,
      
      educational: (q) => `You are a patient educator skilled at explaining complex topics clearly. ${q} Please structure your explanation for learning and include examples.`,
      
      conversational: (q) => `You are a friendly conversational partner. ${q} Feel free to be casual and engaging in your response.`,
      
      technical: (q) => `You are a technical expert with deep knowledge in engineering and technology. ${q} Please provide detailed technical information.`,
      
      business: (q) => `You are a business consultant with expertise in strategy and operations. ${q} Please provide practical business insights.`,
      
      health: (q) => `You are a health information assistant. ${q} Please note that this is for informational purposes only and not a substitute for professional medical advice.`,
      
      general: (q) => q // No enhancement for general queries
    };

    const enhancer = enhancements[queryType];
    const enhanced = enhancer(query);
    
    return {
      enhanced,
      description: `Query type enhancement: ${queryType}`
    };
  }

  /**
   * Apply user profile specific enhancements
   */
  private async applyUserProfileEnhancement(query: string, userProfile: UserProfile): Promise<{
    enhanced: string;
    description: string;
  }> {
    let enhanced = query;
    const enhancements: string[] = [];

    // Add context from recent queries for continuity
    if (userProfile.memory?.recentQueries && userProfile.memory.recentQueries.length > 0) {
      const recentTopics = this.extractTopicsFromRecentQueries(userProfile.memory.recentQueries);
      if (recentTopics.length > 0) {
        enhanced = `Context: You've recently been discussing ${recentTopics.join(', ')}. ${enhanced}`;
        enhancements.push('recent context');
      }
    }

    // Add preferences context
    if (userProfile.preferences?.includeExplanations) {
      enhanced += ' Please include explanations for your recommendations.';
      enhancements.push('explanation preference');
    }

    // Language preference
    if (userProfile.preferences?.language && userProfile.preferences.language !== 'en') {
      enhanced = `Please respond in ${this.getLanguageName(userProfile.preferences.language)}. ${enhanced}`;
      enhancements.push('language preference');
    }

    return {
      enhanced,
      description: enhancements.length > 0 ? `Profile enhancements: ${enhancements.join(', ')}` : 'No profile enhancements'
    };
  }

  /**
   * Apply domain expertise enhancements
   */
  private async applyDomainExpertiseEnhancement(
    query: string, 
    domainExpertise: string[], 
    queryType: QueryType
  ): Promise<{
    enhanced: string;
    description: string;
  }> {
    if (domainExpertise.length === 0) {
      return { enhanced: query, description: 'No domain expertise' };
    }

    // Check if query is related to user's expertise domains
    const relevantDomains = domainExpertise.filter(domain => 
      this.isQueryRelatedToDomain(query, domain, queryType)
    );

    if (relevantDomains.length === 0) {
      return { enhanced: query, description: 'No relevant domain expertise' };
    }

    const domainContext = this.getDomainContextualGuidance(relevantDomains[0]);
    const enhanced = `Given your expertise in ${relevantDomains.join(' and ')}, ${domainContext} ${query}`;

    return {
      enhanced,
      description: `Domain expertise: ${relevantDomains.join(', ')}`
    };
  }

  /**
   * Apply tone enhancements
   */
  private async applyToneEnhancement(query: string, tone: 'formal' | 'casual' | 'witty'): Promise<{
    enhanced: string;
    description: string;
  }> {
    const toneInstructions: Record<string, string> = {
      formal: 'Please respond in a professional, formal tone using proper grammar and avoiding contractions.',
      casual: 'Please respond in a friendly, conversational tone as if speaking to a colleague.',
      witty: 'Please respond with a touch of wit and clever insights while maintaining helpfulness.'
    };

    const instruction = toneInstructions[tone];
    if (!instruction || tone === 'casual') {
      return { enhanced: query, description: 'Default tone' };
    }

    return {
      enhanced: `${instruction} ${query}`,
      description: `Tone adjustment: ${tone}`
    };
  }

  /**
   * Apply verbosity preferences
   */
  private async applyVerbosityEnhancement(
    query: string, 
    verbosity: 'concise' | 'moderate' | 'detailed'
  ): Promise<{
    enhanced: string;
    description: string;
  }> {
    const verbosityInstructions: Record<string, string> = {
      concise: 'Please provide a concise, focused response without unnecessary elaboration.',
      moderate: '', // Default, no enhancement needed
      detailed: 'Please provide a comprehensive, detailed response with examples and thorough explanations.'
    };

    const instruction = verbosityInstructions[verbosity];
    if (!instruction) {
      return { enhanced: query, description: 'Default verbosity' };
    }

    return {
      enhanced: `${instruction} ${query}`,
      description: `Verbosity: ${verbosity}`
    };
  }

  /**
   * Extract topics from recent queries for context
   */
  private extractTopicsFromRecentQueries(recentQueries: any[]): string[] {
    const topics: string[] = [];
    const recentCount = Math.min(3, recentQueries.length);

    for (let i = 0; i < recentCount; i++) {
      const query = recentQueries[i];
      if (query.queryType && query.queryType !== 'general') {
        topics.push(query.queryType);
      }
    }

    return [...new Set(topics)]; // Remove duplicates
  }

  /**
   * Check if query is related to a domain
   */
  private isQueryRelatedToDomain(query: string, domain: string, queryType: QueryType): boolean {
    const domainKeywords: Record<string, string[]> = {
      tech: ['technology', 'software', 'programming', 'code', 'computer', 'digital', 'tech'],
      finance: ['money', 'investment', 'financial', 'budget', 'economics', 'finance', 'market'],
      health: ['health', 'medical', 'doctor', 'medicine', 'fitness', 'nutrition', 'wellness'],
      education: ['learn', 'teach', 'education', 'study', 'school', 'academic', 'research'],
      legal: ['legal', 'law', 'court', 'attorney', 'contract', 'regulation', 'compliance'],
      marketing: ['marketing', 'advertising', 'brand', 'campaign', 'promotion', 'sales'],
      science: ['science', 'research', 'experiment', 'theory', 'hypothesis', 'data'],
      engineering: ['engineering', 'design', 'system', 'technical', 'architecture', 'build']
    };

    const keywords = domainKeywords[domain as keyof typeof domainKeywords] || [];
    const queryLower = query.toLowerCase();

    // Check if query contains domain-related keywords
    const hasKeywords = keywords.some(keyword => queryLower.includes(keyword));
    
    // Check if query type aligns with domain
    const queryTypeAlignment: Record<string, QueryType[]> = {
      tech: ['code', 'technical', 'analytical'],
      finance: ['analytical', 'business', 'factual'],
      health: ['health', 'factual', 'educational'],
      legal: ['legal', 'factual', 'analytical'],
      science: ['factual', 'analytical', 'mathematical', 'educational']
    };

    const alignedTypes = queryTypeAlignment[domain] || [];
    const hasTypeAlignment = alignedTypes.includes(queryType);

    return hasKeywords || hasTypeAlignment;
  }

  /**
   * Get contextual guidance for a domain
   */
  private getDomainContextualGuidance(domain: string): string {
    const guidance: Record<string, string> = {
      tech: 'consider the latest technology trends and best practices.',
      finance: 'focus on practical financial implications and risk considerations.',
      health: 'prioritize safety and evidence-based information.',
      education: 'structure the response for clear learning outcomes.',
      legal: 'emphasize accuracy and include appropriate disclaimers.',
      marketing: 'consider brand impact and target audience perspectives.',
      science: 'emphasize scientific rigor and evidence-based conclusions.',
      engineering: 'focus on practical implementation and system design principles.'
    };

    return guidance[domain] || 'apply your professional expertise to';
  }

  /**
   * Get language name from ISO code
   */
  private getLanguageName(languageCode: string): string {
    const languages: Record<string, string> = {
      'en': 'English',
      'es': 'Spanish',
      'fr': 'French',
      'de': 'German',
      'it': 'Italian',
      'pt': 'Portuguese',
      'ru': 'Russian',
      'ja': 'Japanese',
      'ko': 'Korean',
      'zh': 'Chinese',
      'ar': 'Arabic',
      'hi': 'Hindi'
    };

    return languages[languageCode] || languageCode;
  }
}