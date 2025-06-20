#!/usr/bin/env node
/**
 * GPToggle Model-Agnostic Example
 * 
 * This example demonstrates the new model-agnostic approach in GPToggle v2.0
 * showing how to register models dynamically and use capability-based selection.
 * 
 * Make sure your API keys are set as environment variables:
 * - OPENAI_API_KEY for OpenAI
 * - ANTHROPIC_API_KEY for Claude
 * - GOOGLE_AI_API_KEY for Gemini
 * - XAI_API_KEY for Grok
 */

// Import the model-agnostic GPToggle
const { GPToggle, ModelRegistry } = require('./gptoggle_model_agnostic');

function checkApiKeys() {
  const apiKeys = {};
  
  if (process.env.OPENAI_API_KEY) {
    apiKeys.openai = process.env.OPENAI_API_KEY;
    console.log('✓ OpenAI API key found');
  }
  
  if (process.env.ANTHROPIC_API_KEY) {
    apiKeys.anthropic = process.env.ANTHROPIC_API_KEY;
    console.log('✓ Anthropic API key found');
  }
  
  if (process.env.GOOGLE_AI_API_KEY) {
    apiKeys.google = process.env.GOOGLE_AI_API_KEY;
    console.log('✓ Google AI API key found');
  }
  
  if (process.env.XAI_API_KEY) {
    apiKeys.xai = process.env.XAI_API_KEY;
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

function demoModelRegistration() {
  console.log('\n=== Model Registration Demo ===');
  
  // Create a new GPToggle instance
  const apiKeys = checkApiKeys();
  if (!apiKeys) return;
  
  const gptoggle = new GPToggle({}, apiKeys);
  
  // Register additional models with rich metadata
  const advancedModels = [
    {
      provider: "openai",
      modelId: "gpt-4o",
      displayName: "GPT-4o",
      capabilities: ["text", "vision", "code", "reasoning"],
      strengths: { general: 5, code: 5, reasoning: 5, creativity: 4 },
      tiers: ["standard"],
      contextWindow: 128000,
      intelligence: 5,
      speed: 3
    },
    {
      provider: "anthropic", 
      modelId: "claude-3-opus-20240229",
      displayName: "Claude 3 Opus",
      capabilities: ["text", "vision", "reasoning", "creativity"],
      strengths: { general: 5, reasoning: 5, creativity: 5, code: 4 },
      tiers: ["standard"],
      contextWindow: 200000,
      intelligence: 5,
      speed: 2
    },
    {
      provider: "google",
      modelId: "gemini-1.5-pro",
      displayName: "Gemini 1.5 Pro",
      capabilities: ["text", "vision", "code", "math"],
      strengths: { general: 4, math: 5, code: 4, reasoning: 4 },
      tiers: ["standard"],
      contextWindow: 2097152,
      intelligence: 4,
      speed: 3
    }
  ];
  
  // Register the models
  gptoggle.registerModels(advancedModels);
  
  console.log(`Registered ${advancedModels.length} advanced models`);
  console.log('Available models:', gptoggle.getAvailableModels().map(m => `${m.provider}:${m.modelId}`));
  
  return gptoggle;
}

function demoCapabilityBasedSelection() {
  console.log('\n=== Capability-Based Selection Demo ===');
  
  const gptoggle = demoModelRegistration();
  if (!gptoggle) return;
  
  const testPrompts = [
    "Analyze this image and explain what you see",
    "Write a complex mathematical proof for the Pythagorean theorem",
    "Create a React component for a user authentication form",
    "Write a creative short story about time travel",
    "Explain quantum computing in simple terms"
  ];
  
  for (const prompt of testPrompts) {
    console.log(`\nPrompt: "${prompt}"`);
    
    const recommendation = gptoggle.recommendModel(prompt);
    console.log(`Recommended: ${recommendation.provider}:${recommendation.model}`);
    console.log(`Reason: ${recommendation.reason}`);
    console.log(`Score: ${recommendation.score}`);
    
    // Get task-specific recommendations
    const taskRecs = gptoggle.getTaskRecommendations(prompt);
    if (taskRecs.taskRecommendations.length > 0) {
      console.log('Task-specific recommendations:');
      taskRecs.taskRecommendations.forEach(task => {
        const top = task.recommendations[0];
        console.log(`  ${task.domain}: ${top.provider}:${top.model} (${top.reasons.join(', ')})`);
      });
    }
  }
}

function demoModelFiltering() {
  console.log('\n=== Model Filtering Demo ===');
  
  const gptoggle = demoModelRegistration();
  if (!gptoggle) return;
  
  // Filter by capability
  const visionModels = gptoggle.getAvailableModels({ capability: 'vision' });
  console.log('Vision-capable models:', visionModels.map(m => `${m.provider}:${m.modelId}`));
  
  const codeModels = gptoggle.getAvailableModels({ capability: 'code' });
  console.log('Code-capable models:', codeModels.map(m => `${m.provider}:${m.modelId}`));
  
  // Filter by tier
  const standardModels = gptoggle.getAvailableModels({ tier: 'standard' });
  console.log('Standard tier models:', standardModels.map(m => `${m.provider}:${m.modelId}`));
  
  // Filter by provider
  const openaiModels = gptoggle.getAvailableModels({ provider: 'openai' });
  console.log('OpenAI models:', openaiModels.map(m => m.modelId));
}

function demoRequirementsAnalysis() {
  console.log('\n=== Requirements Analysis Demo ===');
  
  const gptoggle = demoModelRegistration();
  if (!gptoggle) return;
  
  const complexPrompt = `
    I need help with a comprehensive data science project. Please analyze this sales dataset, 
    create visualizations showing quarterly trends, write Python code to implement a machine 
    learning model for sales prediction, and explain the mathematical concepts behind the 
    regression analysis. Also, help me debug this JavaScript function that's not working properly.
  `;
  
  const recommendation = gptoggle.recommendModel(complexPrompt);
  console.log('Complex prompt analysis:');
  console.log(`Requirements detected:`, recommendation.requirements);
  console.log(`Recommended model: ${recommendation.provider}:${recommendation.model}`);
  console.log(`Reasoning: ${recommendation.reason}`);
  
  // Show task breakdown
  const taskRecs = gptoggle.getTaskRecommendations(complexPrompt);
  console.log('\nTask breakdown:');
  taskRecs.taskRecommendations.forEach(task => {
    console.log(`\n${task.domain}:`);
    task.recommendations.slice(0, 2).forEach((rec, i) => {
      console.log(`  ${i + 1}. ${rec.provider}:${rec.model} (score: ${rec.score})`);
      console.log(`     Reasons: ${rec.reasons.join(', ')}`);
    });
  });
}

function main() {
  console.log('GPToggle Model-Agnostic Example');
  console.log('===============================');
  
  // Check API keys first
  const apiKeys = checkApiKeys();
  if (!apiKeys) {
    return;
  }
  
  try {
    // Run all demos
    demoModelRegistration();
    demoCapabilityBasedSelection();
    demoModelFiltering();
    demoRequirementsAnalysis();
    
    console.log('\n=== Demo Complete ===');
    console.log('The model-agnostic approach provides:');
    console.log('- Dynamic model registration');
    console.log('- Capability-based selection');
    console.log('- Rich scoring and reasoning');
    console.log('- Flexible filtering options');
    
  } catch (error) {
    console.error('Demo error:', error.message);
  }
}

// Run the demo
if (require.main === module) {
  main();
}

module.exports = { main };