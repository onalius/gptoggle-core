/**
 * GPToggle Enhanced - A JavaScript implementation of core GPToggle functionality
 * 
 * This library provides browser and Node.js compatible functions for:
 * - Auto-selecting the appropriate model based on prompt content
 * - Accessing multiple AI providers through their APIs
 * - Task-specific model recommendations
 * - Component-specific model suggestions
 * - Follow-up task recommendations
 * 
 * @version 1.0.3
 */

/**
 * Configuration
 */
const DEFAULT_CONFIG = {
  // Provider priority (in descending order)
  providerPriority: ['openai', 'claude', 'gemini', 'grok'],
  
  // Model mappings for each provider
  models: {
    openai: {
      default: 'gpt-3.5-turbo',
      advanced: 'gpt-4o',
      vision: 'gpt-4o',
      creative: 'gpt-4o',
      technical: 'gpt-4o',
      analytical: 'gpt-4o'
    },
    claude: {
      default: 'claude-3-sonnet-20240229',
      advanced: 'claude-3-opus-20240229',
      vision: 'claude-3-opus-20240229',
      creative: 'claude-3-opus-20240229',
      technical: 'claude-3-sonnet-20240229',
      analytical: 'claude-3-opus-20240229'
    },
    gemini: {
      default: 'gemini-pro',
      advanced: 'gemini-1.5-pro',
      vision: 'gemini-pro-vision',
      creative: 'gemini-1.5-pro',
      technical: 'gemini-1.5-pro',
      analytical: 'gemini-1.5-pro'
    },
    grok: {
      default: 'grok-beta',
      advanced: 'grok-2-1212',
      vision: 'grok-2-vision-1212',
      creative: 'grok-2-1212',
      technical: 'grok-2-1212',
      analytical: 'grok-2-1212'
    }
  },
  
  // Default generation parameters
  defaultParams: {
    temperature: 0.7,
    maxTokens: 1000
  },
  
  // Provider strengths by task
  providerStrengths: {
    openai: {
      marketing: 'GPT models excel at market analysis, trend identification, and strategic planning.',
      coding: 'GPT-4o has strong coding capabilities across multiple languages and frameworks.',
      data_analysis: 'GPT models excel at interpreting and explaining data patterns and statistics.',
      creative_writing: 'GPT models generate highly coherent and creative content with good context awareness.',
      general: 'GPT models provide well-rounded capabilities for most general tasks.'
    },
    claude: {
      marketing: 'Claude excels at understanding brand voice, creative copywriting, and marketing strategy.',
      coding: 'Claude can explain complex code clearly and provide well-documented implementations.',
      data_analysis: 'Claude provides thorough and thoughtful data interpretations with nuanced analysis.',
      creative_writing: 'Claude generates nuanced and contextually appropriate creative content with strong narrative abilities.',
      general: 'Claude offers detailed, thoughtful responses with strong reasoning capabilities.'
    },
    gemini: {
      marketing: 'Gemini offers strong analytical capabilities for market research and data-driven marketing.',
      coding: 'Gemini has up-to-date knowledge of programming languages, frameworks, and best practices.',
      data_analysis: 'Gemini provides data-driven insights with strong analytical reasoning and pattern recognition.',
      creative_writing: 'Gemini generates diverse and contextually relevant creative content with good structure.',
      general: 'Gemini provides balanced responses with both technical accuracy and creativity.'
    },
    grok: {
      marketing: 'Grok provides concise, direct marketing advice with contemporary trend awareness.',
      coding: 'Grok excels at efficient code solutions with modern programming techniques.',
      data_analysis: 'Grok offers straightforward data insights with good technical precision.',
      creative_writing: 'Grok generates creative content with a distinct voice and contemporary references.',
      general: 'Grok delivers concise, practical responses with current information.'
    }
  }
};

// Task categories for detection
const TASK_CATEGORIES = [
  {
    name: 'marketing',
    description: 'Marketing plan or strategy',
    keywords: ['marketing plan', 'campaign', 'advertising', 'brand', 'market analysis', 'audience', 'promotion', 'SEO', 'social media', 'content strategy', 'marketing campaign'],
    providerRanking: ['claude', 'openai', 'gemini', 'grok']
  },
  {
    name: 'coding',
    description: 'Code implementation or technical development',
    keywords: ['code', 'function', 'algorithm', 'programming', 'debug', 'software', 'develop', 'implementation', 'script', 'module', 'library', 'API', 'database', 'framework'],
    providerRanking: ['openai', 'gemini', 'claude', 'grok']
  },
  {
    name: 'data_analysis',
    description: 'Data analysis or statistical interpretation',
    keywords: ['analyze data', 'statistics', 'dataset', 'correlation', 'trends', 'metrics', 'dashboard', 'visualization', 'forecast', 'insights', 'patterns', 'regression'],
    providerRanking: ['gemini', 'openai', 'claude', 'grok']
  },
  {
    name: 'creative_writing',
    description: 'Creative content or narrative',
    keywords: ['story', 'creative', 'narrative', 'write', 'content', 'article', 'blog post', 'fiction', 'poem', 'script', 'essay', 'copywriting'],
    providerRanking: ['claude', 'openai', 'gemini', 'grok']
  }
];

/**
 * Utility functions
 */

/**
 * Count the number of words in a text string
 * 
 * @param {string} text - Input text
 * @returns {number} Word count
 */
function countWords(text) {
  return text.split(/\s+/).filter(Boolean).length;
}

/**
 * Check if text contains any of the specified keywords
 * 
 * @param {string} text - Input text
 * @param {string[]} keywords - List of keywords to check
 * @returns {boolean} True if any keyword is found
 */
function containsKeywords(text, keywords) {
  const lowerText = text.toLowerCase();
  return keywords.some(keyword => lowerText.includes(keyword.toLowerCase()));
}

/**
 * Estimate the number of tokens in the text
 * A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text
 * 
 * @param {string} text - Input text
 * @returns {number} Estimated token count
 */
function estimateTokens(text) {
  return Math.floor(text.length / 4);
}

/**
 * GPToggle Class
 */
class GPToggle {
  /**
   * Create a new GPToggle instance
   * 
   * @param {Object} config - Configuration object
   * @param {Object} apiKeys - API keys for different providers
   */
  constructor(config = {}, apiKeys = {}) {
    this.config = { ...DEFAULT_CONFIG };
    
    // Deep merge models and providerStrengths
    if (config.models) {
      for (const provider in config.models) {
        this.config.models[provider] = {
          ...this.config.models[provider],
          ...config.models[provider]
        };
      }
    }
    
    // Merge other config properties
    if (config.providerPriority) this.config.providerPriority = config.providerPriority;
    if (config.defaultParams) this.config.defaultParams = {...this.config.defaultParams, ...config.defaultParams};
    
    // Store API keys
    this.apiKeys = apiKeys;
    
    // Keywords for analysis
    this.visionKeywords = [
      'image', 'picture', 'photo', 'diagram', 'graph', 'chart', 
      'screenshot', 'analyze this', 'what\'s in this', 'look at'
    ];
    this.codeKeywords = [
      'code', 'function', 'algorithm', 'programming', 'python', 'javascript',
      'java', 'c++', 'html', 'css', 'api', 'database', 'sql', 'debug',
      'error', 'bug', 'fix', 'implement', 'class', 'object', 'method'
    ];
    this.creativeKeywords = [
      'create', 'generate', 'write', 'draft', 'compose', 'story', 'poem',
      'creative', 'fiction', 'imagine', 'design', 'innovative', 'novel', 'unique'
    ];
  }

  /**
   * Get available providers based on API keys
   * 
   * @returns {string[]} List of available providers
   */
  getAvailableProviders() {
    return Object.keys(this.apiKeys).filter(provider => 
      this.apiKeys[provider] && this.config.models[provider]
    );
  }

  /**
   * Recommend the best provider and model for a given prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} Object containing provider, model, and reason
   */
  recommendModel(prompt) {
    const availableProviders = this.getAvailableProviders();
    
    if (availableProviders.length === 0) {
      throw new Error('No API keys set for any supported providers');
    }
    
    // Features to check
    const tokenCount = estimateTokens(prompt);
    const wordCount = countWords(prompt);
    
    // Check for specific requirements
    const needsVision = containsKeywords(prompt, this.visionKeywords);
    const needsCoding = containsKeywords(prompt, this.codeKeywords);
    const needsCreativity = containsKeywords(prompt, this.creativeKeywords);
    const needsAdvanced = tokenCount > 2000 || wordCount > 500 || needsCoding;
    
    let reason = '';
    if (needsVision) {
      reason = 'The prompt appears to involve image analysis or visual content';
    } else if (needsAdvanced) {
      reason = needsCoding 
        ? 'The prompt involves code or programming tasks'
        : 'The prompt requires advanced reasoning or is complex/lengthy';
    } else if (needsCreativity) {
      reason = 'The prompt involves creative writing or content generation';
    } else {
      reason = 'The prompt is a standard request suitable for a baseline model';
    }
    
    // Identify tasks for more specific recommendation
    const detectedTasks = this.identifyTasks(prompt);
    if (detectedTasks.length > 0) {
      reason += '. ';
      if (detectedTasks.length === 1) {
        reason += `Task identified: ${detectedTasks[0].taskDescription}`;
      } else {
        reason += `Multiple tasks identified: ${detectedTasks.map(t => t.taskDescription).join(', ')}`;
      }
    }
    
    // Provider selection based on capabilities and priority
    for (const providerName of this.config.providerPriority) {
      if (!availableProviders.includes(providerName)) {
        continue;
      }
      
      // Select model based on requirements
      const modelType = needsVision ? 'vision' : (needsAdvanced ? 'advanced' : 'default');
      const model = this.config.models[providerName][modelType];
      
      return {
        provider: providerName,
        model: model,
        reason: reason,
        detectedTasks: detectedTasks
      };
    }
    
    // Fallback to first available provider with default model
    const providerName = availableProviders[0];
    return {
      provider: providerName,
      model: this.config.models[providerName].default,
      reason: 'Selected as fallback option based on available API keys',
      detectedTasks: detectedTasks
    };
  }
  
  /**
   * Identifies distinct task types within a prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Array} Array of identified tasks with names and descriptions
   */
  identifyTasks(prompt) {
    const detectedTasks = [];
    
    // Check each task category
    for (const category of TASK_CATEGORIES) {
      if (containsKeywords(prompt, category.keywords)) {
        detectedTasks.push({
          taskName: category.name,
          taskDescription: category.description,
          providerRanking: category.providerRanking
        });
      }
    }
    
    return detectedTasks;
  }
  
  /**
   * Generate task-specific model recommendations for different parts of a prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} Overall recommendation and task-specific recommendations
   */
  getTaskRecommendations(prompt) {
    // Get the overall recommendation first
    const overallRecommendation = this.recommendModel(prompt);
    
    // Get specific recommendations for each detected task
    const taskRecommendations = [];
    
    for (const task of overallRecommendation.detectedTasks) {
      const availableProviders = this.getAvailableProviders();
      const recommendations = [];
      
      // Get recommendations for each provider
      for (const provider of availableProviders) {
        let modelType;
        switch (task.taskName) {
          case 'marketing':
          case 'creative_writing':
            modelType = 'creative';
            break;
          case 'coding':
            modelType = 'technical';
            break;
          case 'data_analysis':
            modelType = 'analytical';
            break;
          default:
            modelType = 'default';
        }
        
        const model = this.config.models[provider][modelType] || this.config.models[provider].default;
        const strength = this.config.providerStrengths[provider][task.taskName] || 
                         this.config.providerStrengths[provider].general;
        
        recommendations.push({
          provider: provider,
          model: model,
          strength: strength
        });
      }
      
      // Sort by the task's provider ranking if available
      if (task.providerRanking) {
        recommendations.sort((a, b) => {
          const aIndex = task.providerRanking.indexOf(a.provider);
          const bIndex = task.providerRanking.indexOf(b.provider);
          // If provider not in ranking, put it at the end
          return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
        });
      }
      
      taskRecommendations.push({
        taskName: task.taskName,
        taskDescription: task.taskDescription,
        recommendations: recommendations
      });
    }
    
    return {
      overallRecommendation: overallRecommendation,
      taskRecommendations: taskRecommendations
    };
  }
  
  /**
   * Generate component-specific model suggestions to be included in a response
   * 
   * @param {string} prompt - User prompt
   * @param {string} selectedProvider - The provider actually being used
   * @param {string} selectedModel - The model actually being used
   * @returns {string} Suggestions text to append to the response
   */
  generateModelSuggestions(prompt, selectedProvider, selectedModel) {
    const taskRecommendations = this.getTaskRecommendations(prompt);
    
    // If no tasks were detected, return an empty string
    if (taskRecommendations.taskRecommendations.length === 0) {
      return '';
    }
    
    let suggestions = '\n\n---\n**GPToggle Model Recommendations:**\n\n';
    
    if (taskRecommendations.taskRecommendations.length === 1) {
      const task = taskRecommendations.taskRecommendations[0];
      suggestions += `For this ${task.taskDescription.toLowerCase()} task:\n\n`;
      
      // Add recommendations, highlighting the current model
      for (let i = 0; i < Math.min(2, task.recommendations.length); i++) {
        const rec = task.recommendations[i];
        if (rec.provider === selectedProvider && rec.model === selectedModel) {
          suggestions += `- **Current model: ${rec.provider.charAt(0).toUpperCase() + rec.provider.slice(1)}'s ${rec.model}**\n  ${rec.strength}\n\n`;
        } else {
          suggestions += `- Alternative: ${rec.provider.charAt(0).toUpperCase() + rec.provider.slice(1)}'s ${rec.model}\n  ${rec.strength}\n\n`;
        }
      }
    } else {
      suggestions += 'Your request contains multiple components that might benefit from different AI models:\n\n';
      
      for (const task of taskRecommendations.taskRecommendations) {
        suggestions += `**${task.taskDescription}:**\n`;
        // Get the top recommendation for this task
        const topRec = task.recommendations[0];
        
        if (topRec.provider === selectedProvider && topRec.model === selectedModel) {
          suggestions += `- **Current model: ${topRec.provider.charAt(0).toUpperCase() + topRec.provider.slice(1)}'s ${topRec.model}** is well-suited for this.\n  ${topRec.strength}\n\n`;
        } else {
          suggestions += `- **Recommended: ${topRec.provider.charAt(0).toUpperCase() + topRec.provider.slice(1)}'s ${topRec.model}** might provide better results.\n  ${topRec.strength}\n\n`;
        }
      }
      
      suggestions += 'For optimal results, consider breaking your request into separate prompts targeted at the recommended models for each component.';
    }
    
    return suggestions;
  }

  /**
   * Get follow-up task recommendations based on the current prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} Follow-up recommendations
   */
  getFollowupRecommendations(prompt) {
    const detectedTasks = this.identifyTasks(prompt);
    const followupTasks = [];
    
    // Define likely follow-up tasks for each main task type
    const followupMapping = {
      'marketing': [
        { name: 'content_creation', description: 'Create marketing content', providerRanking: ['claude', 'openai', 'gemini', 'grok'] },
        { name: 'data_analysis', description: 'Analyze campaign performance', providerRanking: ['gemini', 'openai', 'claude', 'grok'] },
        { name: 'coding', description: 'Implement tracking or automation', providerRanking: ['openai', 'gemini', 'claude', 'grok'] }
      ],
      'coding': [
        { name: 'testing', description: 'Write tests for the code', providerRanking: ['openai', 'gemini', 'claude', 'grok'] },
        { name: 'documentation', description: 'Document the implementation', providerRanking: ['claude', 'openai', 'gemini', 'grok'] },
        { name: 'optimization', description: 'Optimize performance', providerRanking: ['openai', 'gemini', 'claude', 'grok'] }
      ],
      'data_analysis': [
        { name: 'visualization', description: 'Create data visualizations', providerRanking: ['gemini', 'openai', 'claude', 'grok'] },
        { name: 'reporting', description: 'Generate analysis reports', providerRanking: ['claude', 'gemini', 'openai', 'grok'] },
        { name: 'prediction', description: 'Build predictive models', providerRanking: ['gemini', 'openai', 'claude', 'grok'] }
      ],
      'creative_writing': [
        { name: 'editing', description: 'Edit and refine content', providerRanking: ['claude', 'openai', 'gemini', 'grok'] },
        { name: 'formatting', description: 'Format for publication', providerRanking: ['openai', 'claude', 'gemini', 'grok'] },
        { name: 'promotion', description: 'Create promotional materials', providerRanking: ['claude', 'openai', 'gemini', 'grok'] }
      ]
    };
    
    // Generate follow-up recommendations based on detected tasks
    for (const task of detectedTasks) {
      const followups = followupMapping[task.taskName] || [];
      
      for (const followup of followups) {
        const availableProviders = this.getAvailableProviders();
        const recommendations = [];
        
        // Get recommendations for each provider
        for (const provider of availableProviders) {
          let modelType;
          switch (followup.name) {
            case 'content_creation':
            case 'creative_writing':
            case 'editing':
              modelType = 'creative';
              break;
            case 'coding':
            case 'testing':
            case 'optimization':
              modelType = 'technical';
              break;
            case 'data_analysis':
            case 'visualization':
            case 'prediction':
              modelType = 'analytical';
              break;
            default:
              modelType = 'default';
          }
          
          const model = this.config.models[provider][modelType] || this.config.models[provider].default;
          const strength = this.config.providerStrengths[provider][followup.name] || 
                           this.config.providerStrengths[provider].general;
          
          recommendations.push({
            provider: provider,
            model: model,
            strength: strength
          });
        }
        
        // Sort by the followup task's provider ranking
        if (followup.providerRanking) {
          recommendations.sort((a, b) => {
            const aIndex = followup.providerRanking.indexOf(a.provider);
            const bIndex = followup.providerRanking.indexOf(b.provider);
            return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
          });
        }
        
        followupTasks.push({
          originalTask: task.taskName,
          followupName: followup.name,
          followupDescription: followup.description,
          recommendations: recommendations
        });
      }
    }
    
    return {
      detectedTasks: detectedTasks,
      followupTasks: followupTasks
    };
  } component.\n';
    }
    
    return suggestions;
  }

  /**
   * Get a response using the OpenAI API
   * 
   * @param {string} prompt - User prompt
   * @param {string} model - Model name
   * @param {Object} params - Generation parameters
   * @returns {Promise<string>} Generated response
   */
  async openaiGetResponse(prompt, model, params) {
    // Generate model suggestions to append to the prompt
    const suggestions = this.generateModelSuggestions(prompt, 'openai', model);
    const augmentedPrompt = prompt + (suggestions ? 
      '\n\nAfter your response, include the following text verbatim:\n' + suggestions : '');
    
    if (typeof fetch === 'undefined') {
      // Node.js environment
      try {
        const { OpenAI } = await import('openai');
        const client = new OpenAI({ apiKey: this.apiKeys.openai });
        const response = await client.chat.completions.create({
          model: model,
          messages: [{ role: 'user', content: augmentedPrompt }],
          temperature: params.temperature,
          max_tokens: params.maxTokens
        });
        return response.choices[0].message.content;
      } catch (error) {
        throw new Error(`OpenAI API error: ${error.message}`);
      }
    } else {
      // Browser environment
      try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiKeys.openai}`
          },
          body: JSON.stringify({
            model: model,
            messages: [{ role: 'user', content: augmentedPrompt }],
            temperature: params.temperature,
            max_tokens: params.maxTokens
          })
        });
        
        if (!response.ok) {
          const error = await response.json();
          throw new Error(`OpenAI API error: ${error.error.message}`);
        }
        
        const data = await response.json();
        return data.choices[0].message.content;
      } catch (error) {
        throw new Error(`OpenAI API error: ${error.message}`);
      }
    }
  }

  /**
   * Get a response using the Anthropic Claude API
   * 
   * @param {string} prompt - User prompt
   * @param {string} model - Model name
   * @param {Object} params - Generation parameters
   * @returns {Promise<string>} Generated response
   */
  async claudeGetResponse(prompt, model, params) {
    // Generate model suggestions to append to the prompt
    const suggestions = this.generateModelSuggestions(prompt, 'claude', model);
    const augmentedPrompt = prompt + (suggestions ? 
      '\n\nAfter your response, include the following text verbatim:\n' + suggestions : '');
    
    if (typeof fetch === 'undefined') {
      // Node.js environment
      try {
        const Anthropic = await import('anthropic');
        const client = new Anthropic.Anthropic({ apiKey: this.apiKeys.claude });
        const response = await client.messages.create({
          model: model,
          max_tokens: params.maxTokens,
          temperature: params.temperature,
          messages: [{ role: 'user', content: augmentedPrompt }]
        });
        return response.content[0].text;
      } catch (error) {
        throw new Error(`Claude API error: ${error.message}`);
      }
    } else {
      // Browser environment
      try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': this.apiKeys.claude,
            'anthropic-version': '2023-06-01'
          },
          body: JSON.stringify({
            model: model,
            max_tokens: params.maxTokens,
            temperature: params.temperature,
            messages: [{ role: 'user', content: augmentedPrompt }]
          })
        });
        
        if (!response.ok) {
          const error = await response.json();
          throw new Error(`Claude API error: ${error.error?.message || 'Unknown error'}`);
        }
        
        const data = await response.json();
        return data.content[0].text;
      } catch (error) {
        throw new Error(`Claude API error: ${error.message}`);
      }
    }
  }

  /**
   * Get a response from any provider
   * 
   * @param {string} prompt - User prompt
   * @param {string} [providerName] - Provider name (auto-selected if not provided)
   * @param {string} [modelName] - Model name (auto-selected if not provided)
   * @param {Object} [params] - Generation parameters
   * @returns {Promise<string>} Generated response
   */
  async getResponse(prompt, providerName, modelName, params = {}) {
    // Use default parameters with any provided overrides
    const parameters = {
      ...this.config.defaultParams,
      ...params
    };
    
    // Auto-select provider and model if not specified
    if (!providerName || !modelName) {
      const recommendation = this.recommendModel(prompt);
      providerName = providerName || recommendation.provider;
      modelName = modelName || recommendation.model;
    }
    
    // Check if API key is available
    if (!this.apiKeys[providerName]) {
      throw new Error(`API key for ${providerName} not found`);
    }
    
    // Call the appropriate provider function
    if (providerName === 'openai') {
      return this.openaiGetResponse(prompt, modelName, parameters);
    } else if (providerName === 'claude') {
      return this.claudeGetResponse(prompt, modelName, parameters);
    } else {
      throw new Error(`Provider ${providerName} not implemented in JavaScript client yet`);
    }
  }
}

// Export for Node.js
if (typeof module !== 'undefined') {
  module.exports = { GPToggle, TASK_CATEGORIES };
}

// Example usage:
/*
// Browser:
const gptoggle = new GPToggle({}, {
  openai: 'your-openai-key',
  claude: 'your-claude-key'
});

// Node.js:
const { GPToggle } = require('./gptoggle_enhanced');
const gptoggle = new GPToggle({}, {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY
});

// Use the library:
async function example() {
  // Auto-select provider and model
  const recommendation = gptoggle.recommendModel('Explain quantum computing');
  console.log(`Recommended: ${recommendation.provider}:${recommendation.model}`);
  console.log(`Reason: ${recommendation.reason}`);
  
  // Get detailed task recommendations
  const taskRecs = gptoggle.getTaskRecommendations('Create a marketing plan and code a signup form in React');
  console.log(JSON.stringify(taskRecs, null, 2));
  
  // Get a response with embedded model suggestions
  const response = await gptoggle.getResponse('Create a marketing plan and code a signup form in React');
  console.log(response);
}

example().catch(console.error);
*/