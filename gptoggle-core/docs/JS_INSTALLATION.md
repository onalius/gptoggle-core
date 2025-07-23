# JavaScript Installation Guide for GPToggle

This guide covers the installation and usage of GPToggle in JavaScript environments, including Node.js and browser-based applications.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Node.js Installation](#nodejs-installation)
  - [Option 1: npm Package](#option-1-npm-package)
  - [Option 2: Standalone File](#option-2-standalone-file)
- [Browser Installation](#browser-installation)
  - [Direct Script Include](#direct-script-include)
  - [Module Bundlers](#module-bundlers)
- [API Keys Configuration](#api-keys-configuration)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)

## Prerequisites

Before installing GPToggle for JavaScript, make sure you have:

- Node.js 14.x or higher (for Node.js usage)
- A modern browser that supports ES6 (for browser usage)
- API keys for the providers you want to use

## Node.js Installation

### Option 1: npm Package

Install GPToggle via npm:

```bash
npm install github:onalius/gptoggle-core
```

or using yarn:

```bash
yarn add github:onalius/gptoggle-core
```

Then import and use it in your code:

```javascript
// CommonJS import
const { GPToggle } = require('gptoggle-core');

// Or ES Module import
// import { GPToggle } from 'gptoggle-core';

// Setup API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_API_KEY,
  grok: process.env.XAI_API_KEY
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Use GPToggle
async function example() {
  const response = await gptoggle.getResponse("What is quantum computing?");
  console.log(response);
}

example();
```

### Option 2: Standalone File

If you prefer not to use npm, you can download the standalone JavaScript file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_enhanced.js -o gptoggle_enhanced.js
```

Then use it in your Node.js project:

```javascript
const { GPToggle } = require('./gptoggle_enhanced.js');

// Rest of the code is the same as above
```

## Browser Installation

### Direct Script Include

You can include GPToggle directly in your HTML:

```html
<script src="https://cdn.jsdelivr.net/gh/onalius/gptoggle-core@main/gptoggle_enhanced.js"></script>

<script>
  // GPToggle is now available as a global variable
  const gptoggle = new GPToggle({}, {
    openai: "your-openai-key" // Store API keys securely!
  });
  
  async function getResponse() {
    const prompt = document.getElementById('prompt').value;
    const response = await gptoggle.getResponse(prompt);
    document.getElementById('response').textContent = response;
  }
</script>
```

### Module Bundlers

When using bundlers like webpack, Rollup, or Parcel:

```javascript
import { GPToggle } from 'gptoggle-core';
// Or if using the standalone file
// import { GPToggle } from './gptoggle_enhanced.js';

// Initialize and use GPToggle as shown above
```

## API Keys Configuration

In Node.js, you can use environment variables:

```javascript
// Load environment variables from .env file
require('dotenv').config();

const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_API_KEY,
  grok: process.env.XAI_API_KEY
};
```

In browsers, you'll need to handle API keys carefully:

```javascript
// IMPORTANT: This is for demonstration only
// In production, keep API keys on the server side and use a backend API
// Never expose API keys in client-side code

// Example using localStorage (only for development/testing)
const apiKeys = {
  openai: localStorage.getItem('openai-api-key')
};

// Better approach: Use a backend API
async function getResponseFromBackend(prompt) {
  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });
  return await response.json();
}
```

## Basic Usage

### Getting a Response

```javascript
const response = await gptoggle.getResponse("What is quantum computing?");
console.log(response);
```

### Auto-selecting a Model

```javascript
const prompt = "Explain the principles of machine learning";
const recommendation = gptoggle.recommendModel(prompt);
console.log(`Recommended provider: ${recommendation.provider}`);
console.log(`Recommended model: ${recommendation.model}`);
console.log(`Reason: ${recommendation.reason}`);
```

### Using a Specific Provider and Model

```javascript
const response = await gptoggle.getResponse(
  "What is quantum computing?",
  "openai",  // Provider
  "gpt-4o",  // Model
  { temperature: 0.7, max_tokens: 500 }  // Parameters
);
console.log(response);
```

## Advanced Usage

### Task-Specific Recommendations

```javascript
const prompt = "Design a marketing strategy and implement a landing page";
const taskRecs = gptoggle.getTaskRecommendations(prompt);

console.log("Overall recommendation:", taskRecs.overall_recommendation);
console.log("Task-specific recommendations:");
taskRecs.task_recommendations.forEach(task => {
  console.log(`- ${task.task_description}:`);
  task.recommendations.forEach(rec => {
    console.log(`  * ${rec.provider}'s ${rec.model}`);
  });
});
```

### Model Suggestions with Follow-up Tasks

```javascript
const prompt = "Create a business plan for a SaaS startup";
const provider = "openai";
const model = "gpt-4o";

const suggestions = gptoggle.generateModelSuggestions(prompt, provider, model);
console.log(suggestions);
// This will include follow-up task recommendations
```

### Checking Available Providers

```javascript
const providers = gptoggle.getAvailableProviders();
console.log("Available providers:", providers);
```

For more examples, check the `examples/javascript/` directory in the repository. The browser example (`browser-example.html`) shows a complete implementation with a form-based interface.

---

For more information or help, check the [GitHub repository](https://github.com/onalius/gptoggle-core) or contact the developers at lano@docdel.io.