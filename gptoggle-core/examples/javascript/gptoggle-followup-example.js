/**
 * GPToggle Follow-up Task Recommendations Example (JavaScript)
 * 
 * This example demonstrates the follow-up task recommendation feature,
 * which suggests specific models for potential follow-up tasks based on
 * the initial prompt.
 * 
 * Make sure your API keys are set as environment variables:
 * - OPENAI_API_KEY for OpenAI
 * - ANTHROPIC_API_KEY for Claude
 * - GOOGLE_API_KEY for Gemini
 * - XAI_API_KEY for Grok
 */

// Import the GPToggle class
const { GPToggle } = require('../../gptoggle_enhanced');

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_API_KEY,
  grok: process.env.XAI_API_KEY
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

/**
 * Check which API keys are available
 */
function checkApiKeys() {
  console.log("Checking available providers...");
  const providers = gptoggle.getAvailableProviders();
  
  if (providers.length === 0) {
    console.log("No API keys found. Please set at least one of the following environment variables:");
    console.log("- OPENAI_API_KEY: for OpenAI models (GPT-3.5, GPT-4o)");
    console.log("- ANTHROPIC_API_KEY: for Claude models");
    console.log("- GOOGLE_API_KEY: for Google Gemini models");
    console.log("- XAI_API_KEY: for xAI Grok models");
    return false;
  }
  
  console.log(`Available providers: ${providers.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(', ')}`);
  return true;
}

/**
 * Demonstrate recommendations for follow-up tasks
 */
async function demoFollowupRecommendations() {
  // Example 1: Business Strategy Prompt
  const businessPrompt = "Create a business plan for a SaaS startup in the AI space";
  
  console.log("\n===== Business Strategy Example =====");
  console.log(`Prompt: "${businessPrompt}"\n`);
  
  // Get model recommendation and detected tasks
  const recommendation = gptoggle.recommendModel(businessPrompt);
  console.log(`Recommended model: ${recommendation.provider.charAt(0).toUpperCase() + recommendation.provider.slice(1)}'s ${recommendation.model}`);
  console.log(`Reason: ${recommendation.reason}`);
  
  // Get task recommendations
  const taskRecs = gptoggle.getTaskRecommendations(businessPrompt);
  
  console.log("\nDetected Tasks:");
  taskRecs.task_recommendations.forEach(task => {
    console.log(`- ${task.task_description}`);
  });
  
  // Generate model suggestions (includes follow-up recommendations)
  const suggestions = gptoggle.generateModelSuggestions(
    businessPrompt, 
    recommendation.provider, 
    recommendation.model
  );
  
  console.log("\nModel Suggestions that would be included in the response:");
  console.log(suggestions);
  
  // Example 2: Multi-domain Prompt
  const multiPrompt = "Design a marketing strategy for our new app and implement a landing page with user authentication";
  
  console.log("\n===== Multi-Domain Example =====");
  console.log(`Prompt: "${multiPrompt}"\n`);
  
  // Get model recommendation and detected tasks
  const multiRecommendation = gptoggle.recommendModel(multiPrompt);
  console.log(`Recommended model: ${multiRecommendation.provider.charAt(0).toUpperCase() + multiRecommendation.provider.slice(1)}'s ${multiRecommendation.model}`);
  console.log(`Reason: ${multiRecommendation.reason}`);
  
  // Get task recommendations
  const multiTaskRecs = gptoggle.getTaskRecommendations(multiPrompt);
  
  console.log("\nDetected Tasks:");
  multiTaskRecs.task_recommendations.forEach(task => {
    console.log(`- ${task.task_description}`);
  });
  
  // Generate model suggestions (includes follow-up recommendations)
  const multiSuggestions = gptoggle.generateModelSuggestions(
    multiPrompt, 
    multiRecommendation.provider, 
    multiRecommendation.model
  );
  
  console.log("\nModel Suggestions that would be included in the response:");
  console.log(multiSuggestions);
}

/**
 * Main function
 */
async function main() {
  console.log("GPToggle Follow-up Task Recommendations Example (JavaScript)");
  console.log("==========================================================");
  
  if (!checkApiKeys()) {
    return;
  }
  
  await demoFollowupRecommendations();
}

// Run the main function
main().catch(error => {
  console.error("Error:", error);
});