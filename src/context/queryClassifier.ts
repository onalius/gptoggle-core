/**
 * Query Type Classifier
 * 
 * Classifies user queries into different types to enable contextual enhancements
 * and appropriate model selection.
 * 
 * @version 2.0.0
 */

import { Logger } from '../utils/logger';

export type QueryType = 
  | 'factual'
  | 'creative' 
  | 'legal'
  | 'emotional'
  | 'analytical'
  | 'code'
  | 'mathematical'
  | 'educational'
  | 'conversational'
  | 'technical'
  | 'business'
  | 'health'
  | 'general';

export interface ClassificationResult {
  queryType: QueryType;
  confidence: number;
  reasoning: string;
  alternativeTypes?: QueryType[];
}

export class QueryTypeClassifier {
  private logger: Logger;
  
  // Keywords and patterns for each query type
  private readonly patterns: Record<QueryType, {
    keywords: string[];
    patterns: RegExp[];
    phrases: string[];
  }> = {
    factual: {
      keywords: ['what', 'when', 'where', 'who', 'how many', 'facts', 'information', 'define', 'explain'],
      patterns: [/^(what|when|where|who|how) (is|are|was|were|did|does|do)/i],
      phrases: ['tell me about', 'information about', 'facts about']
    },
    creative: {
      keywords: ['write', 'create', 'imagine', 'story', 'poem', 'creative', 'brainstorm', 'invent', 'design'],
      patterns: [/^(write|create|imagine|design) (a|an|some)/i, /story|poem|creative|brainstorm/i],
      phrases: ['write a', 'create a', 'come up with', 'think of']
    },
    legal: {
      keywords: ['legal', 'law', 'court', 'contract', 'attorney', 'lawsuit', 'regulation', 'compliance', 'rights'],
      patterns: [/legal|law|court|contract|attorney|lawsuit|regulation|compliance/i],
      phrases: ['legal advice', 'according to law', 'contract terms']
    },
    emotional: {
      keywords: ['feel', 'sad', 'happy', 'angry', 'worried', 'stressed', 'anxious', 'depressed', 'support'],
      patterns: [/i feel|i'm (sad|happy|angry|worried|stressed|anxious|depressed)/i],
      phrases: ['i feel', 'help me cope', 'emotional support']
    },
    analytical: {
      keywords: ['analyze', 'compare', 'evaluate', 'assess', 'examine', 'study', 'research', 'data', 'statistics'],
      patterns: [/^(analyze|compare|evaluate|assess|examine)/i, /data|statistics|research/i],
      phrases: ['break down', 'pros and cons', 'analyze the']
    },
    code: {
      keywords: ['code', 'program', 'function', 'algorithm', 'debug', 'javascript', 'python', 'html', 'css', 'api'],
      patterns: [/^(write|create|debug|fix|optimize) .* (code|function|program|script)/i, /(javascript|python|html|css|java|c\+\+|api)/i],
      phrases: ['write code', 'programming', 'software development']
    },
    mathematical: {
      keywords: ['calculate', 'solve', 'equation', 'formula', 'mathematics', 'algebra', 'geometry', 'statistics'],
      patterns: [/^(calculate|solve|compute)/i, /equation|formula|mathematics|algebra|geometry/i],
      phrases: ['math problem', 'calculate the', 'solve for']
    },
    educational: {
      keywords: ['learn', 'teach', 'explain', 'understand', 'lesson', 'tutorial', 'study', 'homework'],
      patterns: [/^(teach|explain|help me understand)/i, /lesson|tutorial|study|homework/i],
      phrases: ['help me learn', 'teach me', 'i need to understand']
    },
    conversational: {
      keywords: ['hello', 'hi', 'chat', 'talk', 'conversation', 'discuss'],
      patterns: [/^(hello|hi|hey)/i, /^(let's|can we) (chat|talk|discuss)/i],
      phrases: ['just chatting', 'casual conversation']
    },
    technical: {
      keywords: ['technical', 'engineering', 'system', 'architecture', 'implementation', 'infrastructure'],
      patterns: [/technical|engineering|system|architecture|implementation|infrastructure/i],
      phrases: ['technical details', 'system design', 'how does it work']
    },
    business: {
      keywords: ['business', 'strategy', 'marketing', 'sales', 'profit', 'revenue', 'investment', 'finance'],
      patterns: [/business|strategy|marketing|sales|profit|revenue|investment|finance/i],
      phrases: ['business plan', 'market analysis', 'financial']
    },
    health: {
      keywords: ['health', 'medical', 'doctor', 'symptoms', 'medicine', 'disease', 'treatment'],
      patterns: [/health|medical|doctor|symptoms|medicine|disease|treatment/i],
      phrases: ['health advice', 'medical question', 'symptoms of']
    },
    general: {
      keywords: [],
      patterns: [],
      phrases: []
    }
  };

  constructor() {
    this.logger = new Logger();
  }

  /**
   * Classify a query and return the most likely type
   */
  async classifyQuery(query: string): Promise<QueryType> {
    const result = await this.classifyQueryDetailed(query);
    return result.queryType;
  }

  /**
   * Classify a query and return detailed classification information
   */
  async classifyQueryDetailed(query: string): Promise<ClassificationResult> {
    if (!query || query.trim().length === 0) {
      return {
        queryType: 'general',
        confidence: 1.0,
        reasoning: 'Empty query defaults to general type'
      };
    }

    const normalizedQuery = query.toLowerCase().trim();
    const scores: Record<QueryType, number> = {} as Record<QueryType, number>;

    // Initialize all scores to 0
    Object.keys(this.patterns).forEach(type => {
      scores[type as QueryType] = 0;
    });

    // Score each query type based on keyword matches, patterns, and phrases
    for (const [type, config] of Object.entries(this.patterns)) {
      const queryType = type as QueryType;
      
      if (queryType === 'general') continue; // Skip general, it's the fallback

      let typeScore = 0;

      // Keyword matching
      for (const keyword of config.keywords) {
        if (normalizedQuery.includes(keyword.toLowerCase())) {
          typeScore += 1;
        }
      }

      // Pattern matching
      for (const pattern of config.patterns) {
        if (pattern.test(normalizedQuery)) {
          typeScore += 2; // Patterns are more specific than keywords
        }
      }

      // Phrase matching
      for (const phrase of config.phrases) {
        if (normalizedQuery.includes(phrase.toLowerCase())) {
          typeScore += 1.5;
        }
      }

      scores[queryType] = typeScore;
    }

    // Find the highest scoring type
    const sortedTypes = Object.entries(scores)
      .filter(([_, score]) => score > 0)
      .sort(([, a], [, b]) => b - a);

    if (sortedTypes.length === 0) {
      return {
        queryType: 'general',
        confidence: 0.8,
        reasoning: 'No specific patterns matched, classified as general'
      };
    }

    const [bestType, bestScore] = sortedTypes[0];
    const maxPossibleScore = Math.max(
      this.patterns[bestType as QueryType].keywords.length,
      this.patterns[bestType as QueryType].patterns.length * 2,
      this.patterns[bestType as QueryType].phrases.length * 1.5
    );

    const confidence = Math.min(0.95, bestScore / Math.max(maxPossibleScore, 1));
    
    const alternativeTypes = sortedTypes
      .slice(1, 3)
      .map(([type]) => type as QueryType);

    this.logger.debug(`Query "${query.substring(0, 50)}..." classified as ${bestType} with confidence ${confidence.toFixed(2)}`);

    return {
      queryType: bestType as QueryType,
      confidence,
      reasoning: this.generateReasoning(bestType as QueryType, bestScore, normalizedQuery),
      alternativeTypes: alternativeTypes.length > 0 ? alternativeTypes : undefined
    };
  }

  /**
   * Generate human-readable reasoning for the classification
   */
  private generateReasoning(queryType: QueryType, score: number, query: string): string {
    const config = this.patterns[queryType];
    const matchedKeywords = config.keywords.filter(keyword => 
      query.includes(keyword.toLowerCase())
    );
    const matchedPatterns = config.patterns.filter(pattern => 
      pattern.test(query)
    );

    let reasoning = `Classified as ${queryType} based on `;
    const reasons = [];

    if (matchedKeywords.length > 0) {
      reasons.push(`keywords: ${matchedKeywords.join(', ')}`);
    }

    if (matchedPatterns.length > 0) {
      reasons.push(`pattern matches`);
    }

    if (reasons.length === 0) {
      return `Classified as ${queryType} based on general characteristics`;
    }

    return reasoning + reasons.join(' and ');
  }

  /**
   * Get all supported query types
   */
  getSupportedTypes(): QueryType[] {
    return Object.keys(this.patterns) as QueryType[];
  }

  /**
   * Add custom patterns for a query type
   */
  addCustomPattern(queryType: QueryType, keywords?: string[], patterns?: RegExp[], phrases?: string[]): void {
    if (!this.patterns[queryType]) {
      this.patterns[queryType] = { keywords: [], patterns: [], phrases: [] };
    }

    if (keywords) {
      this.patterns[queryType].keywords.push(...keywords);
    }
    if (patterns) {
      this.patterns[queryType].patterns.push(...patterns);
    }
    if (phrases) {
      this.patterns[queryType].phrases.push(...phrases);
    }

    this.logger.debug(`Added custom patterns for query type: ${queryType}`);
  }
}