/**
 * GPToggle.js - Enhanced Multi-Provider AI Model Wrapper
 * 
 * Main entry point for the NPM package. This file exports the GPToggle class
 * from the enhanced version of the library.
 * 
 * @version 1.0.3
 */

// Import the GPToggle class from the enhanced implementation
const { GPToggle } = require('./gptoggle_enhanced');

// Re-export the class as the main export
module.exports = {
  GPToggle,
  
  // For compatibility and convenience, also provide direct exports
  // of the main functions that users might want to access
  
  /**
   * Get a response from any provider with auto-model selection
   * 
   * @param {string} prompt - User prompt
   * @param {string} [providerName] - Provider name (auto-selected if not provided)
   * @param {string} [modelName] - Model name (auto-selected if not provided)
   * @param {Object} [params] - Generation parameters
   * @returns {Promise<string>} Generated response
   */
  getResponse: async (prompt, providerName, modelName, params = {}) => {
    const gptoggle = new GPToggle();
    return await gptoggle.getResponse(prompt, providerName, modelName, params);
  },
  
  /**
   * Recommend the best provider and model for a given prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} Object containing provider, model, and reason
   */
  recommendModel: (prompt) => {
    const gptoggle = new GPToggle();
    return gptoggle.recommendModel(prompt);
  },
  
  /**
   * Generate comprehensive task-specific recommendations for a prompt
   * 
   * @param {string} prompt - User prompt
   * @returns {Object} Object with overall and task-specific recommendations
   */
  getTaskRecommendations: (prompt) => {
    const gptoggle = new GPToggle();
    return gptoggle.getTaskRecommendations(prompt);
  },
  
  /**
   * Get a list of available providers based on API keys
   * 
   * @returns {string[]} List of available providers
   */
  getAvailableProviders: () => {
    const gptoggle = new GPToggle();
    return gptoggle.getAvailableProviders();
  }
};