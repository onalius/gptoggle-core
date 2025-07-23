/**
 * GPToggle.js - A JavaScript implementation of core GPToggle functionality
 * 
 * This library provides browser and Node.js compatible functions for:
 * - Auto-selecting the appropriate model based on prompt content
 * - Accessing multiple AI providers through their APIs
 * 
 * @version 1.0.1
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
      vision: 'gpt-4o'
    },
    claude: {
      default: 'claude-3-sonnet-20240229',
      advanced: 'claude-3-opus-20240229',
      vision: 'claude-3-opus-20240229'
    },
    gemini: {
      default: 'gemini-pro',
      advanced: 'gemini-1.5-pro',
      vision: 'gemini-pro-vision'
    },
    grok: {
      default: 'grok-beta',
      advanced: 'grok-2-1212',
      vision: 'grok-2-vision-1212'
    }
  },
  
  // Default generation parameters
  defaultParams: {
    temperature: 0.7,
    maxTokens: 1000
  }
};

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
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.apiKeys = apiKeys;
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
    
    // Vision/image keywords
    const visionKeywords = [
      'image', 'picture', 'photo', 'diagram', 'graph', 'chart', 
      'screenshot', 'analyze this', 'what\'s in this', 'look at'
    ];
    
    // Code-related keywords
    const codeKeywords = [
      'code', 'function', 'algorithm', 'programming', 'python', 'javascript',
      'java', 'c++', 'html', 'css', 'api', 'database', 'sql', 'debug',
      'error', 'bug', 'fix', 'implement', 'class', 'object', 'method'
    ];
    
    // Creative tasks
    const creativeKeywords = [
      'create', 'generate', 'write', 'draft', 'compose', 'story', 'poem',
      'creative', 'fiction', 'imagine', 'design', 'innovative', 'novel', 'unique'
    ];
    
    // Check for specific requirements
    const needsVision = containsKeywords(prompt, visionKeywords);
    const needsCoding = containsKeywords(prompt, codeKeywords);
    const needsCreativity = containsKeywords(prompt, creativeKeywords);
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
        reason: reason
      };
    }
    
    // Fallback to first available provider with default model
    const providerName = availableProviders[0];
    return {
      provider: providerName,
      model: this.config.models[providerName].default,
      reason: 'Selected as fallback option based on available API keys'
    };
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
    if (typeof fetch === 'undefined') {
      // Node.js environment
      try {
        const { OpenAI } = await import('openai');
        const client = new OpenAI({ apiKey: this.apiKeys.openai });
        const response = await client.chat.completions.create({
          model: model,
          messages: [{ role: 'user', content: prompt }],
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
            messages: [{ role: 'user', content: prompt }],
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
    if (typeof fetch === 'undefined') {
      // Node.js environment
      try {
        const Anthropic = await import('anthropic');
        const client = new Anthropic.Anthropic({ apiKey: this.apiKeys.claude });
        const response = await client.messages.create({
          model: model,
          max_tokens: params.maxTokens,
          temperature: params.temperature,
          messages: [{ role: 'user', content: prompt }]
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
            messages: [{ role: 'user', content: prompt }]
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
  module.exports = GPToggle;
}

// Example usage:
/*
// Browser:
const gptoggle = new GPToggle({}, {
  openai: 'your-openai-key',
  claude: 'your-claude-key'
});

// Node.js:
const GPToggle = require('./gptoggle');
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
  
  // Get a response
  const response = await gptoggle.getResponse('What is the meaning of life?');
  console.log(response);
}

example().catch(console.error);
*/