/**
 * GPToggle Enhanced Example
 * 
 * This example demonstrates how to use the enhanced GPToggle features,
 * including task-specific model recommendations and component-specific
 * model suggestions within responses.
 * 
 * Make sure your API keys are set as environment variables:
 * - OPENAI_API_KEY for OpenAI
 * - ANTHROPIC_API_KEY for Claude
 * - GOOGLE_API_KEY for Gemini
 * - XAI_API_KEY for Grok
 */

// Import the GPToggle class
const { GPToggle, TASK_CATEGORIES } = require('./gptoggle_enhanced');

// Setup API keys from environment variables
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_API_KEY,
  grok: process.env.XAI_API_KEY
};

// Check available providers
function checkApiKeys() {
  console.log("Checking available providers...");
  const gptoggle = new GPToggle({}, apiKeys);
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

// Demonstrate recommendations for a single-task prompt
function demoSingleTask() {
  const prompt = "Create a marketing plan for a new eco-friendly water bottle.";
  
  console.log("\n===== Single Task Example =====");
  console.log(`Prompt: "${prompt}"\n`);
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  // Get model recommendation
  const recommendation = gptoggle.recommendModel(prompt);
  console.log(`Recommended model: ${recommendation.provider.charAt(0).toUpperCase() + recommendation.provider.slice(1)}'s ${recommendation.model}`);
  console.log(`Reason: ${recommendation.reason}`);
  
  // Get task recommendations
  const taskRecs = gptoggle.getTaskRecommendations(prompt);
  console.log("\nTask-specific recommendations:");
  
  for (const task of taskRecs.taskRecommendations) {
    console.log(`- ${task.taskDescription}:`);
    for (const rec of task.recommendations.slice(0, 2)) { // Show top 2
      console.log(`  * ${rec.provider.charAt(0).toUpperCase() + rec.provider.slice(1)}'s ${rec.model}`);
      console.log(`    ${rec.strength}`);
    }
  }
  
  // Uncomment to get actual response
  /*
  console.log("\nGetting response...");
  gptoggle.getResponse(prompt)
    .then(response => {
      console.log("\nResponse:");
      console.log(response);
    })
    .catch(error => {
      console.error("Error:", error.message);
    });
  */
}

// Demonstrate recommendations for a multi-task prompt
function demoMultiTask() {
  const prompt = "Create a marketing strategy for our new app and implement a simple landing page in HTML/CSS.";
  
  console.log("\n===== Multi-Task Example =====");
  console.log(`Prompt: "${prompt}"\n`);
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  // Get model recommendation
  const recommendation = gptoggle.recommendModel(prompt);
  console.log(`Recommended model: ${recommendation.provider.charAt(0).toUpperCase() + recommendation.provider.slice(1)}'s ${recommendation.model}`);
  console.log(`Reason: ${recommendation.reason}`);
  
  // Get detailed task recommendations
  const taskRecs = gptoggle.getTaskRecommendations(prompt);
  console.log("\nTask-specific recommendations:");
  
  for (const task of taskRecs.taskRecommendations) {
    console.log(`- ${task.taskDescription}:`);
    for (const rec of task.recommendations.slice(0, 2)) { // Show top 2
      console.log(`  * ${rec.provider.charAt(0).toUpperCase() + rec.provider.slice(1)}'s ${rec.model}`);
      console.log(`    ${rec.strength}`);
    }
  }
  
  // Generate model suggestions that would be embedded in the response
  const suggestions = gptoggle.generateModelSuggestions(
    prompt, 
    recommendation.provider, 
    recommendation.model
  );
  console.log("\nModel Suggestions that would be included in the response:");
  console.log(suggestions);
  
  // Uncomment to get actual response
  /*
  console.log("\nGetting response...");
  gptoggle.getResponse(prompt)
    .then(response => {
      console.log("\nResponse:");
      console.log(response);
    })
    .catch(error => {
      console.error("Error:", error.message);
    });
  */
}

// Main function
async function main() {
  console.log("GPToggle Enhanced Example");
  console.log("=========================");
  
  if (!checkApiKeys()) {
    return;
  }
  
  demoSingleTask();
  demoMultiTask();
}

main().catch(console.error);