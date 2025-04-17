/**
 * GPToggle JavaScript Example
 * 
 * This example demonstrates how to use GPToggle in a Node.js environment.
 * Make sure you have your API keys set as environment variables.
 */

// Import the GPToggle class
const { GPToggle } = require('./gptoggle.js');

// Import required modules for Node.js environment
const axios = require('axios');

// Setup your API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_AI_API_KEY,
  grok: process.env.GROK_API_KEY
};

// Create a GPToggle instance with custom configuration
const gptoggle = new GPToggle({
  providerPriority: ['openai', 'claude', 'gemini'],  // Prioritize OpenAI, then Claude, then Gemini
  models: {
    openai: {
      default: 'gpt-3.5-turbo',
      advanced: 'gpt-4o',
      vision: 'gpt-4o'
    }
  }
}, apiKeys);

// Example 1: Check available providers based on API keys
console.log("Available providers:", gptoggle.getAvailableProviders());

// Example 2: Get a model recommendation for a specific prompt
const prompt = "Generate a Python function to calculate Fibonacci numbers";
const recommendation = gptoggle.recommendModel(prompt);
console.log("Recommended model:", recommendation);

// Example 3: Get a response from the recommended model
async function getResponse() {
  try {
    console.log("Sending prompt:", prompt);
    const response = await gptoggle.getResponse(prompt);
    console.log("Response:", response);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// Execute the async function
getResponse();