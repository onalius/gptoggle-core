#!/usr/bin/env node

/**
 * GPToggle v2.0 Contextualized Intelligence Example (JavaScript)
 * 
 * This example demonstrates the new contextualized intelligence features
 * integrated directly into the GPToggle core system.
 */

// Import GPToggle v2.0 classes (assuming they're in the same file or properly exported)
// For this demo, we'll assume the classes are available in the global scope

// Check if we're in Node.js or browser environment
const isNode = typeof process !== 'undefined' && process.versions && process.versions.node;

if (isNode) {
  // In Node.js, we might need to require the file
  eval(require('fs').readFileSync('./gptoggle_v2.js', 'utf8'));
}

function main() {
  console.log("🚀 GPToggle v2.0 Contextualized Intelligence Demo (JavaScript)");
  console.log("=".repeat(70));
  
  // Initialize GPToggle v2.0
  const gptoggle = new GPToggle();
  
  // Sample models for demonstration
  const sampleModels = [
    {
      provider: "openai",
      modelId: "gpt-4o", 
      displayName: "GPT-4o",
      tiers: ["premium"],
      capabilities: ["code", "reasoning", "vision"],
      intelligence: 5,
      speed: 4,
      contextWindow: 128000,
      pricing: { input: 0.005, output: 0.015 }
    },
    {
      provider: "anthropic",
      modelId: "claude-3-opus",
      displayName: "Claude 3 Opus", 
      tiers: ["premium"],
      capabilities: ["reasoning", "code", "creativity"],
      intelligence: 5,
      speed: 3,
      contextWindow: 200000,
      pricing: { input: 0.015, output: 0.075 }
    },
    {
      provider: "google",
      modelId: "gemini-1.5-pro",
      displayName: "Gemini 1.5 Pro",
      tiers: ["standard"],
      capabilities: ["reasoning", "math", "vision"], 
      intelligence: 4,
      speed: 4,
      contextWindow: 1000000,
      pricing: { input: 0.0035, output: 0.0105 }
    }
  ];
  
  // Register models
  gptoggle.registerModelsFromArray(sampleModels);
  
  // Create different user profiles for demonstration
  const profiles = {
    developer: createDeveloperProfile(),
    student: createStudentProfile(),
    business: createBusinessProfile()
  };
  
  // Test queries
  const testQueries = [
    "Write a Python function to sort a list",
    "Explain machine learning algorithms", 
    "Create a marketing strategy for a new product",
    "How do I calculate compound interest?"
  ];
  
  // Demonstrate contextualized responses
  testQueries.forEach(query => {
    console.log(`\n📝 Testing Query: "${query}"`);
    console.log("-".repeat(50));
    
    Object.entries(profiles).forEach(([profileType, profile]) => {
      console.log(`\n👤 Response for ${profileType}:`);
      
      const startTime = Date.now();
      
      // Get contextualized response
      const response = gptoggle.getContextualizedResponse(query, profile);
      
      const processingTime = Date.now() - startTime;
      
      console.log(`   Model: ${response.provider}:${response.modelUsed}`);
      console.log(`   Type: ${response.queryType}`);
      console.log(`   Enhancements: ${response.contextualEnhancements.join(', ')}`);
      console.log(`   Processing Time: ${processingTime}ms`);
      
      // Simulate AI response
      const aiResponse = simulateAiResponse(response);
      console.log(`   Response Preview: ${aiResponse.substring(0, 100)}...`);
      
      console.log(`   Follow-up: ${response.followUpSuggestion}`);
    });
  });
  
  // Show learning patterns
  console.log(`\n🧠 Learning Patterns Analysis`);
  console.log("-".repeat(50));
  
  Object.entries(profiles).forEach(([profileType, profile]) => {
    console.log(`\n👤 ${profileType}:`);
    const analysis = analyzeProfilePatterns(profile);
    Object.entries(analysis).forEach(([key, value]) => {
      console.log(`   ${key}: ${value}`);
    });
  });
  
  console.log("\n✅ Demo completed! GPToggle v2.0 provides contextualized intelligence.");
}

function createDeveloperProfile() {
  const profile = UserProfile.createDefault("developer-alice");
  profile.communicationStyle.tone = 'casual';
  profile.communicationStyle.verbosity = 'detailed';
  profile.expertise.domains = ['technology', 'engineering'];
  profile.expertise.skillLevel = {
    'javascript': 'expert',
    'python': 'advanced', 
    'machine_learning': 'intermediate'
  };
  profile.expertise.interests = ['AI', 'web development', 'automation'];
  return profile;
}

function createStudentProfile() {
  const profile = UserProfile.createDefault("student-bob");
  profile.communicationStyle.tone = 'friendly';
  profile.communicationStyle.verbosity = 'moderate';
  profile.communicationStyle.includeExplanations = true;
  profile.expertise.domains = ['education'];
  profile.expertise.skillLevel = {
    'python': 'beginner',
    'math': 'intermediate'
  };
  profile.expertise.interests = ['learning', 'programming', 'science'];
  return profile;
}

function createBusinessProfile() {
  const profile = UserProfile.createDefault("business-carol");
  profile.communicationStyle.tone = 'professional';
  profile.communicationStyle.verbosity = 'concise';
  profile.expertise.domains = ['business', 'finance'];
  profile.expertise.skillLevel = {
    'business_strategy': 'expert',
    'marketing': 'advanced',
    'finance': 'expert'
  };
  profile.expertise.interests = ['strategy', 'growth', 'innovation'];
  return profile;
}

function simulateAiResponse(response) {
  const modelName = response.modelUsed || 'unknown';
  const enhancements = response.contextualEnhancements || [];
  
  let base;
  if (modelName.includes('gpt')) {
    base = `[Simulated Response from ${modelName}]`;
  } else if (modelName.includes('claude')) {
    base = `[Simulated Response from Claude]`;
  } else if (modelName.includes('gemini')) {
    base = `[Simulated Response from Gemini]`;
  } else {
    base = `[Simulated Response from ${modelName}]`;
  }
  
  if (enhancements.some(e => e.includes('detailed'))) {
    return `${base}\n\nThis is a comprehensive response to your query: "${response.originalQuery.substring(0, 50)}..."`;
  } else if (enhancements.some(e => e.includes('concise'))) {
    return `${base}\n\nI've processed your request with consideration for your professional communication style.`;
  } else if (enhancements.some(e => e.includes('friendly'))) {
    return `${base}\n\nI've processed your request with consideration for your friendly communication style.`;
  }
  
  return `${base}\n\nThis is a standard response to your query.`;
}

function analyzeProfilePatterns(profile) {
  const interactions = profile.context.recentInteractions;
  
  return {
    'Total Interactions': interactions.length,
    'Common Topics': profile.context.learningPatterns.commonTopics
      .slice(0, 3)
      .map(t => `${t.topic} (${t.frequency})`)
      .join(', '),
    'Communication Style': `${profile.communicationStyle.tone}, ${profile.communicationStyle.verbosity}`,
    'Expertise': profile.expertise.domains.join(', ')
  };
}

// Run the demo
if (isNode) {
  main();
} else {
  // In browser, wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', main);
  } else {
    main();
  }
}