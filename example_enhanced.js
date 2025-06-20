#!/usr/bin/env node
/**
 * GPToggle Enhanced Example
 * 
 * This example demonstrates the enhanced features of GPToggle v1.0.3+
 * including task-specific recommendations and component-specific suggestions.
 * 
 * Make sure your API keys are set as environment variables:
 * - OPENAI_API_KEY for OpenAI
 * - ANTHROPIC_API_KEY for Claude
 * - GOOGLE_AI_API_KEY for Gemini
 * - XAI_API_KEY for Grok
 */

const { GPToggle } = require('./gptoggle_enhanced');

function checkApiKeys() {
  const apiKeys = {};
  
  if (process.env.OPENAI_API_KEY) {
    apiKeys.openai = process.env.OPENAI_API_KEY;
    console.log('✓ OpenAI API key found');
  }
  
  if (process.env.ANTHROPIC_API_KEY) {
    apiKeys.claude = process.env.ANTHROPIC_API_KEY;
    console.log('✓ Anthropic API key found');
  }
  
  if (process.env.GOOGLE_AI_API_KEY) {
    apiKeys.gemini = process.env.GOOGLE_AI_API_KEY;
    console.log('✓ Google AI API key found');
  }
  
  if (process.env.XAI_API_KEY) {
    apiKeys.grok = process.env.XAI_API_KEY;
    console.log('✓ xAI API key found');
  }
  
  if (Object.keys(apiKeys).length === 0) {
    console.log('❌ No API keys found. Please set at least one of:');
    console.log('   - OPENAI_API_KEY');
    console.log('   - ANTHROPIC_API_KEY'); 
    console.log('   - GOOGLE_AI_API_KEY');
    console.log('   - XAI_API_KEY');
    return null;
  }
  
  return apiKeys;
}

function demoBasicRecommendation() {
  console.log('\n=== Basic Model Recommendation ===');
  
  const apiKeys = checkApiKeys();
  if (!apiKeys) return null;
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  const prompts = [
    "Explain quantum computing",
    "Write a Python function to sort a list",
    "Create a marketing plan for a new product",
    "Analyze this image and describe what you see",
    "Write a creative story about space exploration"
  ];
  
  for (const prompt of prompts) {
    console.log(`\nPrompt: "${prompt}"`);
    const recommendation = gptoggle.recommendModel(prompt);
    console.log(`Recommended: ${recommendation.provider}:${recommendation.model}`);
    console.log(`Reason: ${recommendation.reason}`);
  }
  
  return gptoggle;
}

function demoTaskRecommendations() {
  console.log('\n=== Task-Specific Recommendations ===');
  
  const gptoggle = demoBasicRecommendation();
  if (!gptoggle) return;
  
  const multiTaskPrompt = "Create a comprehensive marketing campaign for our new mobile app, including social media content, a landing page with HTML/CSS code, and data analysis of our target audience demographics.";
  
  console.log(`\nMulti-task prompt: "${multiTaskPrompt}"`);
  
  const taskRecs = gptoggle.getTaskRecommendations(multiTaskPrompt);
  
  console.log('\nOverall recommendation:');
  console.log(`  Provider: ${taskRecs.overallRecommendation.provider}`);
  console.log(`  Model: ${taskRecs.overallRecommendation.model}`);
  console.log(`  Reason: ${taskRecs.overallRecommendation.reason}`);
  
  console.log('\nTask-specific recommendations:');
  taskRecs.taskRecommendations.forEach(task => {
    console.log(`\n${task.taskDescription}:`);
    task.recommendations.slice(0, 2).forEach((rec, index) => {
      console.log(`  ${index + 1}. ${rec.provider}:${rec.model}`);
      console.log(`     Strength: ${rec.strength}`);
    });
  });
}

function demoFollowupRecommendations() {
  console.log('\n=== Follow-up Task Recommendations ===');
  
  const gptoggle = demoBasicRecommendation();
  if (!gptoggle) return;
  
  const prompts = [
    "Write a React component for user authentication",
    "Create a data analysis report from our sales data",
    "Design a marketing strategy for our B2B product"
  ];
  
  for (const prompt of prompts) {
    console.log(`\nOriginal task: "${prompt}"`);
    
    const followups = gptoggle.getFollowupRecommendations(prompt);
    
    if (followups.followupTasks.length > 0) {
      console.log('Likely follow-up tasks:');
      followups.followupTasks.forEach(followup => {
        console.log(`  • ${followup.followupDescription}`);
        const topRec = followup.recommendations[0];
        console.log(`    Recommended: ${topRec.provider}:${topRec.model}`);
      });
    }
  }
}

function demoComponentSuggestions() {
  console.log('\n=== Component-Specific Model Suggestions ===');
  
  const gptoggle = demoBasicRecommendation();
  if (!gptoggle) return;
  
  const complexPrompt = "Help me build a complete e-commerce website: design the user interface, write the backend API in Node.js, create a marketing landing page, and analyze competitor pricing data.";
  
  console.log(`\nComplex prompt: "${complexPrompt}"`);
  
  // Get recommendations
  const recommendation = gptoggle.recommendModel(complexPrompt);
  console.log(`\nSelected: ${recommendation.provider}:${recommendation.model}`);
  
  // Generate component-specific suggestions
  const suggestions = gptoggle.generateModelSuggestions(
    complexPrompt, 
    recommendation.provider, 
    recommendation.model
  );
  
  console.log('\nComponent-specific suggestions:');
  console.log(suggestions);
}

async function demoRealResponse() {
  console.log('\n=== Real API Response with Embedded Suggestions ===');
  
  const apiKeys = checkApiKeys();
  if (!apiKeys) return;
  
  // Only demo if we have at least OpenAI or Claude
  if (!apiKeys.openai && !apiKeys.claude) {
    console.log('Skipping real API demo - need OpenAI or Claude API key');
    return;
  }
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  const prompt = "Create a simple marketing email template and a basic HTML/CSS layout for it.";
  
  console.log(`\nPrompt: "${prompt}"`);
  console.log('Getting response with embedded model suggestions...\n');
  
  try {
    const response = await gptoggle.getResponse(prompt);
    console.log('Response:');
    console.log(response);
  } catch (error) {
    console.log(`Error getting response: ${error.message}`);
    console.log('This is normal if API keys are not configured or have insufficient credits.');
  }
}

function demoProviderStrengths() {
  console.log('\n=== Provider Strengths Analysis ===');
  
  const gptoggle = demoBasicRecommendation();
  if (!gptoggle) return;
  
  const tasks = ['marketing', 'coding', 'data_analysis', 'creative_writing'];
  const providers = gptoggle.getAvailableProviders();
  
  console.log('Provider strengths by task:');
  
  for (const task of tasks) {
    console.log(`\n${task.toUpperCase()}:`);
    for (const provider of providers) {
      const strength = gptoggle.config.providerStrengths[provider][task] || 
                      gptoggle.config.providerStrengths[provider].general;
      console.log(`  ${provider}: ${strength}`);
    }
  }
}

async function main() {
  console.log('GPToggle Enhanced Features Example');
  console.log('=================================');
  
  try {
    // Run all demos
    demoBasicRecommendation();
    demoTaskRecommendations();
    demoFollowupRecommendations();
    demoComponentSuggestions();
    demoProviderStrengths();
    
    // Real API demo (commented out by default to avoid using credits)
    // await demoRealResponse();
    
    console.log('\n=== Demo Complete ===');
    console.log('Enhanced features demonstrated:');
    console.log('- Multi-task detection and recommendations');
    console.log('- Follow-up task suggestions');
    console.log('- Component-specific model suggestions');
    console.log('- Provider strength analysis');
    console.log('- Embedded suggestions in responses');
    
  } catch (error) {
    console.error('Demo error:', error.message);
  }
}

// Run the demo
if (require.main === module) {
  main();
}

module.exports = { main };