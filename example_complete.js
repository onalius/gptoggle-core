#!/usr/bin/env node
/**
 * Complete GPToggle Example
 * 
 * This comprehensive example demonstrates all key features of both the enhanced
 * and model-agnostic versions of GPToggle, showcasing the core functionality
 * that developers can build upon.
 * 
 * Features demonstrated:
 * - Basic model recommendations
 * - Multi-task detection and analysis
 * - Provider-specific strengths
 * - Model registry and filtering
 * - Capability-based selection
 * - Follow-up task suggestions
 * - Component-specific recommendations
 */

const { GPToggle: EnhancedGPToggle } = require('./gptoggle_enhanced');
const { GPToggle: AgnosticGPToggle } = require('./gptoggle_model_agnostic');

function getApiKeys() {
  const keys = {};
  
  if (process.env.OPENAI_API_KEY) keys.openai = process.env.OPENAI_API_KEY;
  if (process.env.ANTHROPIC_API_KEY) keys.claude = process.env.ANTHROPIC_API_KEY;
  if (process.env.GOOGLE_AI_API_KEY) keys.gemini = process.env.GOOGLE_AI_API_KEY;
  if (process.env.XAI_API_KEY) keys.grok = process.env.XAI_API_KEY;
  
  // For model-agnostic version
  if (process.env.ANTHROPIC_API_KEY) keys.anthropic = process.env.ANTHROPIC_API_KEY;
  if (process.env.GOOGLE_AI_API_KEY) keys.google = process.env.GOOGLE_AI_API_KEY;
  if (process.env.XAI_API_KEY) keys.xai = process.env.XAI_API_KEY;
  
  return keys;
}

function demoEnhancedVersion() {
  console.log('\n=== Enhanced GPToggle v1.0.3+ Demo ===');
  
  const apiKeys = getApiKeys();
  if (Object.keys(apiKeys).length === 0) {
    console.log('No API keys found for enhanced demo');
    return;
  }
  
  const gptoggle = new EnhancedGPToggle({}, apiKeys);
  
  // 1. Basic recommendation
  console.log('\n1. Basic Model Recommendations:');
  const prompts = [
    "Write Python code for data analysis",
    "Create marketing copy for a new product",
    "Analyze this chart and provide insights"
  ];
  
  prompts.forEach(prompt => {
    const rec = gptoggle.recommendModel(prompt);
    console.log(`  "${prompt}"`);
    console.log(`  → ${rec.provider}:${rec.model} (${rec.reason})`);
  });
  
  // 2. Multi-task analysis
  console.log('\n2. Multi-Task Analysis:');
  const complexPrompt = "Create a comprehensive business proposal including market research, financial projections in Excel, and a presentation design with marketing materials.";
  const taskRecs = gptoggle.getTaskRecommendations(complexPrompt);
  
  console.log(`  Complex task: "${complexPrompt}"`);
  console.log(`  Overall: ${taskRecs.overallRecommendation.provider}:${taskRecs.overallRecommendation.model}`);
  console.log('  Task breakdown:');
  taskRecs.taskRecommendations.forEach(task => {
    const top = task.recommendations[0];
    console.log(`    ${task.taskDescription}: ${top.provider}:${top.model}`);
  });
  
  // 3. Follow-up suggestions
  console.log('\n3. Follow-up Task Suggestions:');
  const followups = gptoggle.getFollowupRecommendations("Build a React e-commerce website");
  console.log('  Original: "Build a React e-commerce website"');
  console.log('  Follow-up tasks:');
  followups.followupTasks.slice(0, 3).forEach(task => {
    const rec = task.recommendations[0];
    console.log(`    ${task.followupDescription}: ${rec.provider}:${rec.model}`);
  });
  
  return gptoggle;
}

function demoModelAgnosticVersion() {
  console.log('\n=== Model-Agnostic GPToggle v2.0+ Demo ===');
  
  const apiKeys = getApiKeys();
  if (Object.keys(apiKeys).length === 0) {
    console.log('No API keys found for model-agnostic demo');
    return;
  }
  
  const gptoggle = new AgnosticGPToggle({}, apiKeys);
  
  // Register enhanced model definitions
  const models = [
    {
      provider: "openai",
      modelId: "gpt-4o",
      displayName: "GPT-4o",
      capabilities: ["text", "vision", "code", "reasoning"],
      contextWindow: 128000,
      intelligence: 5,
      speed: 3,
      tiers: ["standard"]
    },
    {
      provider: "anthropic",
      modelId: "claude-3-opus-20240229",
      displayName: "Claude 3 Opus",
      capabilities: ["text", "vision", "reasoning", "creativity"],
      contextWindow: 200000,
      intelligence: 5,
      speed: 2,
      tiers: ["standard"]
    },
    {
      provider: "google",
      modelId: "gemini-1.5-pro",
      displayName: "Gemini 1.5 Pro",
      capabilities: ["text", "vision", "code", "math"],
      contextWindow: 2097152,
      intelligence: 4,
      speed: 3,
      tiers: ["standard"]
    }
  ];
  
  gptoggle.registerModels(models);
  
  // 1. Capability-based selection
  console.log('\n1. Capability-Based Selection:');
  const testCases = [
    { prompt: "Analyze this image and explain the contents", needs: "vision" },
    { prompt: "Solve complex calculus problems step by step", needs: "math" },
    { prompt: "Debug this JavaScript function and optimize it", needs: "code" },
    { prompt: "Write a philosophical essay on consciousness", needs: "reasoning" }
  ];
  
  testCases.forEach(test => {
    const rec = gptoggle.recommendModel(test.prompt);
    console.log(`  ${test.needs.toUpperCase()}: "${test.prompt}"`);
    console.log(`  → ${rec.provider}:${rec.model} (score: ${rec.score})`);
  });
  
  // 2. Model filtering
  console.log('\n2. Model Filtering:');
  const visionModels = gptoggle.getAvailableModels({ capability: 'vision' });
  const codeModels = gptoggle.getAvailableModels({ capability: 'code' });
  const standardTier = gptoggle.getAvailableModels({ tier: 'standard' });
  
  console.log(`  Vision models: ${visionModels.map(m => m.modelId).join(', ')}`);
  console.log(`  Code models: ${codeModels.map(m => m.modelId).join(', ')}`);
  console.log(`  Standard tier: ${standardTier.map(m => m.modelId).join(', ')}`);
  
  // 3. Requirements analysis
  console.log('\n3. Requirements Analysis:');
  const analyticalPrompt = "Create a machine learning model to predict stock prices, visualize the results, and write documentation explaining the mathematical concepts.";
  const analysis = gptoggle.recommendModel(analyticalPrompt);
  
  console.log(`  Complex prompt: "${analyticalPrompt}"`);
  console.log('  Detected requirements:');
  console.log(`    Complexity: ${analysis.requirements.complexity}/5`);
  console.log(`    Domains: ${analysis.requirements.domains.join(', ')}`);
  console.log(`    Context needed: ${analysis.requirements.minContextWindow} tokens`);
  console.log(`  → Recommended: ${analysis.provider}:${analysis.model}`);
  
  return gptoggle;
}

function demonstrateProviderStrengths() {
  console.log('\n=== Provider Strengths Comparison ===');
  
  const gptoggle = demoEnhancedVersion();
  if (!gptoggle) return;
  
  const taskTypes = ['marketing', 'coding', 'data_analysis', 'creative_writing'];
  const availableProviders = gptoggle.getAvailableProviders();
  
  console.log('Provider strengths by task type:');
  taskTypes.forEach(task => {
    console.log(`\n${task.toUpperCase().replace('_', ' ')}:`);
    availableProviders.forEach(provider => {
      const strength = gptoggle.config.providerStrengths[provider]?.[task] ||
                      gptoggle.config.providerStrengths[provider]?.general ||
                      'No specific strength defined';
      console.log(`  ${provider}: ${strength}`);
    });
  });
}

function demonstrateArchitectureComparison() {
  console.log('\n=== Architecture Comparison ===');
  
  console.log('\nEnhanced Version (v1.0.3+):');
  console.log('  • Task-specific recommendations');
  console.log('  • Pre-defined provider strengths');
  console.log('  • Component-specific suggestions');
  console.log('  • Follow-up task recommendations');
  console.log('  • Embedded model suggestions in responses');
  
  console.log('\nModel-Agnostic Version (v2.0+):');
  console.log('  • Dynamic model registry');
  console.log('  • Capability-based selection');
  console.log('  • Rich attribute scoring');
  console.log('  • Flexible model filtering');
  console.log('  • Requirements analysis engine');
  
  console.log('\nUse Enhanced Version When:');
  console.log('  • You want ready-to-use task detection');
  console.log('  • You need provider-specific recommendations');
  console.log('  • You want embedded suggestions in responses');
  console.log('  • You prefer configuration over registration');
  
  console.log('\nUse Model-Agnostic Version When:');
  console.log('  • You need custom model definitions');
  console.log('  • You want fine-grained capability control');
  console.log('  • You need sophisticated scoring algorithms');
  console.log('  • You want maximum flexibility');
}

function main() {
  console.log('GPToggle Complete Core Functionality Demo');
  console.log('==========================================');
  
  const apiKeys = getApiKeys();
  
  if (Object.keys(apiKeys).length === 0) {
    console.log('\nNo API keys found. Set environment variables:');
    console.log('  OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_AI_API_KEY, XAI_API_KEY');
    console.log('\nRunning limited demo with available functionality...\n');
  } else {
    console.log(`\nFound API keys for: ${Object.keys(apiKeys).join(', ')}\n`);
  }
  
  try {
    // Run comprehensive demos
    demoEnhancedVersion();
    demoModelAgnosticVersion();
    demonstrateProviderStrengths();
    demonstrateArchitectureComparison();
    
    console.log('\n=== Demo Summary ===');
    console.log('✓ Enhanced GPToggle: Task-focused with built-in intelligence');
    console.log('✓ Model-Agnostic GPToggle: Flexible with dynamic capabilities');
    console.log('✓ Provider strengths: Specialized recommendations per task type');
    console.log('✓ Multi-task detection: Handles complex, multi-component requests');
    console.log('✓ Follow-up suggestions: Anticipates workflow continuations');
    console.log('✓ Capability filtering: Find models by specific requirements');
    console.log('✓ Requirements analysis: Understands prompt complexity and needs');
    
    console.log('\n=== Core GPToggle Benefits ===');
    console.log('• Intelligent model selection reduces decision fatigue');
    console.log('• Multi-provider support prevents vendor lock-in');
    console.log('• Task-specific recommendations optimize results');
    console.log('• Extensible architecture supports custom implementations');
    console.log('• Rich metadata enables informed model choices');
    
    console.log('\n=== Next Steps for Developers ===');
    console.log('1. Choose the version that fits your use case');
    console.log('2. Integrate with your existing AI workflows');
    console.log('3. Customize provider priorities and model mappings');
    console.log('4. Build specialized interfaces for your domain');
    console.log('5. Contribute improvements back to the core library');
    
  } catch (error) {
    console.error('\nDemo error:', error.message);
    console.log('This is expected if API keys are not configured.');
  }
}

if (require.main === module) {
  main();
}

module.exports = { main, demoEnhancedVersion, demoModelAgnosticVersion };