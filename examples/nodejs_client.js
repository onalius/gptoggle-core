/**
 * GPToggle Node.js API Client Example
 * 
 * This example shows how to interact with the GPToggle REST API from Node.js.
 * First, start the GPToggle REST API server:
 *   python examples/rest_api.py
 * 
 * Then run this script:
 *   node examples/nodejs_client.js
 */

// Use fetch in Node.js (Node.js 18+ has built-in fetch)
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// API base URL
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Get all available providers
 */
async function getProviders() {
  try {
    const response = await fetch(`${API_BASE_URL}/providers`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Unknown error');
    }
    
    console.log('Available Providers:');
    data.providers.forEach(provider => {
      console.log(`- ${provider}`);
    });
    return data.providers;
  } catch (error) {
    console.error('Error getting providers:', error.message);
    return [];
  }
}

/**
 * Get all available models for a provider
 */
async function getModels(provider = 'openai') {
  try {
    const response = await fetch(`${API_BASE_URL}/models?provider=${provider}`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Unknown error');
    }
    
    console.log(`\nAvailable Models for ${provider}:`);
    data.models.forEach(model => {
      console.log(`- ${model}`);
    });
    return data.models;
  } catch (error) {
    console.error('Error getting models:', error.message);
    return [];
  }
}

/**
 * Get a recommended model for a prompt
 */
async function getRecommendedModel(prompt) {
  try {
    const response = await fetch(`${API_BASE_URL}/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Unknown error');
    }
    
    console.log(`\nRecommended Model for prompt "${prompt}":`);
    console.log(`- ${data.model}`);
    return data.model;
  } catch (error) {
    console.error('Error getting recommended model:', error.message);
    return null;
  }
}

/**
 * Generate a response for a prompt
 */
async function generateResponse(prompt, provider = null, model = null) {
  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,
        provider,
        model,
        temperature: 0.7,
        max_tokens: 1000
      }),
    });
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Unknown error');
    }
    
    console.log(`\nResponse for prompt "${prompt}":`);
    console.log(data.response);
    return data.response;
  } catch (error) {
    console.error('Error generating response:', error.message);
    return null;
  }
}

/**
 * Main function to run the examples
 */
async function main() {
  console.log('GPToggle Node.js Client Example\n');
  
  // Get all providers
  await getProviders();
  
  // Get models for OpenAI
  await getModels('openai');
  
  // Get recommended model for a prompt
  const prompt = 'Explain the theory of relativity in simple terms';
  const recommendedModel = await getRecommendedModel(prompt);
  
  // Generate a response using the recommended model
  if (recommendedModel) {
    const [provider, model] = recommendedModel.split(':');
    await generateResponse(prompt, provider, model);
  }
  
  // Or use a specific provider and model
  await generateResponse('Who was Albert Einstein?', 'openai', 'gpt-4o');
}

// Run the example
main().catch(error => {
  console.error('Error in main:', error);
});