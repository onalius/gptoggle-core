/**
 * GPToggle Client Library for Node.js
 * 
 * This library provides a simple way to connect to a GPToggle REST API
 * from Node.js applications.
 */

// Use node-fetch for Node.js versions that don't have built-in fetch
let fetchImplementation;
try {
  // Try to use built-in fetch (Node.js 18+)
  fetchImplementation = fetch;
} catch (e) {
  // Fallback to node-fetch if available
  try {
    fetchImplementation = require('node-fetch');
  } catch (e) {
    console.warn('Neither built-in fetch nor node-fetch is available. Please install node-fetch: npm install node-fetch');
    fetchImplementation = (...args) => Promise.reject(new Error('Fetch not available'));
  }
}

class GPToggleClient {
  /**
   * Create a new GPToggle client
   * 
   * @param {string} apiUrl - The URL of the GPToggle API (without trailing slash)
   */
  constructor(apiUrl) {
    // Use the provided API URL or check environment variable
    this.apiUrl = apiUrl || process.env.GPTOGGLE_API_URL;
    
    if (!this.apiUrl) {
      throw new Error('GPToggle API URL is required. Either provide it as a parameter or set the GPTOGGLE_API_URL environment variable.');
    }
    
    // Remove trailing slash if present
    this.apiUrl = this.apiUrl.replace(/\/$/, '');
    
    // Add /api if not present
    if (!this.apiUrl.endsWith('/api')) {
      this.apiUrl = `${this.apiUrl}/api`;
    }
  }
  
  /**
   * Get a list of available providers
   * 
   * @returns {Promise<string[]>} Array of provider names
   */
  async getProviders() {
    const response = await fetchImplementation(`${this.apiUrl}/providers`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to get providers');
    }
    
    return data.providers;
  }
  
  /**
   * Get a list of available models for a provider
   * 
   * @param {string} provider - The provider name
   * @returns {Promise<string[]>} Array of model names
   */
  async getModels(provider = 'openai') {
    const response = await fetchImplementation(`${this.apiUrl}/models?provider=${provider}`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to get models');
    }
    
    return data.models;
  }
  
  /**
   * Get a recommended model for a prompt
   * 
   * @param {string} prompt - The prompt to get a recommendation for
   * @returns {Promise<string>} The recommended model in the format "provider:model"
   */
  async recommendModel(prompt) {
    const response = await fetchImplementation(`${this.apiUrl}/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to get recommendation');
    }
    
    return data.model;
  }
  
  /**
   * Generate a response for a prompt
   * 
   * @param {object} options - Generation options
   * @param {string} options.prompt - The prompt to generate a response for
   * @param {string} [options.provider] - The provider to use (optional)
   * @param {string} [options.model] - The model to use (optional)
   * @param {number} [options.temperature=0.7] - The temperature to use
   * @param {number} [options.max_tokens=1000] - The maximum number of tokens to generate
   * @returns {Promise<string>} The generated response
   */
  async generateResponse(options) {
    if (!options.prompt) {
      throw new Error('Prompt is required');
    }
    
    const response = await fetchImplementation(`${this.apiUrl}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: options.prompt,
        provider: options.provider,
        model: options.model,
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 1000,
      }),
    });
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to generate response');
    }
    
    return data.response;
  }
}

module.exports = GPToggleClient;

// Example usage:
/*
const GPToggleClient = require('./client_library');

// Create a client
const client = new GPToggleClient('https://your-gptoggle-api.domain.com');

// Use the client
async function example() {
  // Get available providers
  const providers = await client.getProviders();
  console.log('Available providers:', providers);
  
  // Get a recommended model
  const model = await client.recommendModel('What is the meaning of life?');
  console.log('Recommended model:', model);
  
  // Generate a response
  const response = await client.generateResponse({
    prompt: 'What is the meaning of life?'
  });
  console.log('Response:', response);
}

example().catch(console.error);
*/