/**
 * Query Classifier
 * 
 * Classifies user queries into specific types for better contextualized responses.
 * 
 * @version 2.0.0
 */

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

export class QueryClassifier {
  /**
   * Classify a query into one of the predefined types
   */
  classifyQuery(query: string): QueryType {
    const queryLower = query.toLowerCase();

    // Code-related queries
    if (this.isCodeQuery(queryLower)) {
      return 'code';
    }

    // Mathematical queries
    if (this.isMathematicalQuery(queryLower)) {
      return 'mathematical';
    }

    // Legal queries
    if (this.isLegalQuery(queryLower)) {
      return 'legal';
    }

    // Health queries
    if (this.isHealthQuery(queryLower)) {
      return 'health';
    }

    // Business queries
    if (this.isBusinessQuery(queryLower)) {
      return 'business';
    }

    // Emotional/support queries
    if (this.isEmotionalQuery(queryLower)) {
      return 'emotional';
    }

    // Creative queries
    if (this.isCreativeQuery(queryLower)) {
      return 'creative';
    }

    // Analytical queries
    if (this.isAnalyticalQuery(queryLower)) {
      return 'analytical';
    }

    // Technical queries
    if (this.isTechnicalQuery(queryLower)) {
      return 'technical';
    }

    // Educational queries
    if (this.isEducationalQuery(queryLower)) {
      return 'educational';
    }

    // Conversational queries
    if (this.isConversationalQuery(queryLower)) {
      return 'conversational';
    }

    // Factual queries
    if (this.isFactualQuery(queryLower)) {
      return 'factual';
    }

    return 'general';
  }

  private isCodeQuery(query: string): boolean {
    const codeKeywords = [
      'code', 'program', 'function', 'class', 'method', 'algorithm',
      'python', 'javascript', 'java', 'c++', 'sql', 'html', 'css',
      'debug', 'error', 'syntax', 'compile', 'runtime', 'variable',
      'array', 'object', 'string', 'integer', 'boolean', 'loop',
      'if statement', 'for loop', 'while loop', 'api', 'framework',
      'library', 'import', 'export', 'return', 'print', 'console.log'
    ];
    return codeKeywords.some(keyword => query.includes(keyword));
  }

  private isMathematicalQuery(query: string): boolean {
    const mathKeywords = [
      'calculate', 'equation', 'formula', 'mathematics', 'algebra',
      'geometry', 'calculus', 'statistics', 'probability', 'solve',
      'derivative', 'integral', 'matrix', 'vector', 'theorem',
      'proof', 'graph', 'plot', 'function', 'variable', 'coefficient'
    ];
    const mathSymbols = /[+\-*/=<>∑∏∂∫√π]/;
    return mathKeywords.some(keyword => query.includes(keyword)) || mathSymbols.test(query);
  }

  private isLegalQuery(query: string): boolean {
    const legalKeywords = [
      'legal', 'law', 'attorney', 'lawyer', 'court', 'judge', 'trial',
      'contract', 'agreement', 'lawsuit', 'regulation', 'statute',
      'constitutional', 'rights', 'liability', 'negligence', 'tort',
      'criminal', 'civil', 'defendant', 'plaintiff', 'evidence',
      'jurisdiction', 'precedent', 'compliance', 'violation'
    ];
    return legalKeywords.some(keyword => query.includes(keyword));
  }

  private isHealthQuery(query: string): boolean {
    const healthKeywords = [
      'health', 'medical', 'doctor', 'medicine', 'disease', 'symptom',
      'treatment', 'diagnosis', 'therapy', 'hospital', 'clinic',
      'nutrition', 'diet', 'exercise', 'fitness', 'wellness',
      'mental health', 'psychology', 'depression', 'anxiety',
      'medication', 'prescription', 'vaccine', 'surgery', 'cancer'
    ];
    return healthKeywords.some(keyword => query.includes(keyword));
  }

  private isBusinessQuery(query: string): boolean {
    const businessKeywords = [
      'business', 'company', 'revenue', 'profit', 'loss', 'investment',
      'marketing', 'sales', 'customer', 'client', 'strategy', 'plan',
      'budget', 'finance', 'accounting', 'economics', 'market',
      'competition', 'startup', 'entrepreneur', 'management',
      'leadership', 'team', 'project', 'meeting', 'presentation'
    ];
    return businessKeywords.some(keyword => query.includes(keyword));
  }

  private isEmotionalQuery(query: string): boolean {
    const emotionalKeywords = [
      'feel', 'feeling', 'emotion', 'sad', 'happy', 'angry', 'frustrated',
      'worried', 'anxious', 'stressed', 'depressed', 'overwhelmed',
      'excited', 'nervous', 'scared', 'afraid', 'love', 'hate',
      'support', 'help me', 'advice', 'guidance', 'comfort',
      'relationship', 'family', 'friend', 'personal'
    ];
    const emotionalPatterns = [
      /i feel/i, /i'm feeling/i, /i am feeling/i, /makes me/i,
      /i need help/i, /i don't know/i, /i'm confused/i, /i'm lost/i
    ];
    return emotionalKeywords.some(keyword => query.includes(keyword)) ||
           emotionalPatterns.some(pattern => pattern.test(query));
  }

  private isCreativeQuery(query: string): boolean {
    const creativeKeywords = [
      'creative', 'create', 'design', 'art', 'artistic', 'imagine',
      'story', 'poem', 'song', 'music', 'paint', 'draw', 'sketch',
      'novel', 'character', 'plot', 'narrative', 'fiction',
      'brainstorm', 'ideas', 'inspiration', 'innovative', 'original',
      'write', 'writing', 'compose', 'craft', 'invent'
    ];
    return creativeKeywords.some(keyword => query.includes(keyword));
  }

  private isAnalyticalQuery(query: string): boolean {
    const analyticalKeywords = [
      'analyze', 'analysis', 'compare', 'comparison', 'evaluate',
      'assessment', 'data', 'statistics', 'trend', 'pattern',
      'research', 'study', 'examine', 'investigate', 'breakdown',
      'pros and cons', 'advantages', 'disadvantages', 'impact',
      'correlation', 'causation', 'hypothesis', 'conclusion'
    ];
    return analyticalKeywords.some(keyword => query.includes(keyword));
  }

  private isTechnicalQuery(query: string): boolean {
    const technicalKeywords = [
      'technical', 'technology', 'engineering', 'system', 'network',
      'server', 'database', 'architecture', 'infrastructure', 'protocol',
      'configuration', 'setup', 'installation', 'deployment',
      'security', 'performance', 'optimization', 'troubleshoot',
      'specification', 'documentation', 'integration', 'platform'
    ];
    return technicalKeywords.some(keyword => query.includes(keyword));
  }

  private isEducationalQuery(query: string): boolean {
    const educationalKeywords = [
      'learn', 'teach', 'explain', 'understand', 'education', 'lesson',
      'tutorial', 'guide', 'how to', 'what is', 'why does', 'when did',
      'where is', 'who was', 'define', 'definition', 'concept',
      'theory', 'principle', 'example', 'demonstrate', 'show me',
      'step by step', 'instructions', 'course', 'training'
    ];
    const questionWords = /^(what|why|how|when|where|who|which)/i;
    return educationalKeywords.some(keyword => query.includes(keyword)) ||
           questionWords.test(query);
  }

  private isConversationalQuery(query: string): boolean {
    const conversationalKeywords = [
      'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
      'how are you', 'what\'s up', 'nice to meet', 'thanks', 'thank you',
      'please', 'excuse me', 'sorry', 'goodbye', 'bye', 'see you',
      'chat', 'talk', 'conversation', 'discuss', 'opinion', 'think'
    ];
    const conversationalPatterns = [
      /^(hello|hi|hey)/i, /how are you/i, /what do you think/i,
      /in your opinion/i, /let's talk/i, /can we chat/i
    ];
    return conversationalKeywords.some(keyword => query.includes(keyword)) ||
           conversationalPatterns.some(pattern => pattern.test(query));
  }

  private isFactualQuery(query: string): boolean {
    const factualKeywords = [
      'fact', 'information', 'data', 'statistic', 'number', 'date',
      'history', 'when', 'where', 'who', 'what', 'population',
      'capital', 'country', 'city', 'president', 'government',
      'discovery', 'invention', 'event', 'year', 'century'
    ];
    const factualPatterns = [
      /when (was|did|is)/i, /where (is|was)/i, /who (is|was)/i,
      /what (is|was) the/i, /how many/i, /how much/i
    ];
    return factualKeywords.some(keyword => query.includes(keyword)) ||
           factualPatterns.some(pattern => pattern.test(query));
  }
}