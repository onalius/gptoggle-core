# JavaScript Installation Guide for GPToggle

This guide explains how to use the JavaScript implementation of GPToggle in different environments.

## Option 1: NPM Installation (Recommended for Node.js Projects)

You can install GPToggle directly from GitHub using npm:

```bash
npm install github:onalius/gptoggle-core
```

Then import and use it in your JavaScript code:

```javascript
const { GPToggle } = require('gptoggle-js');

// Setup your API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_AI_API_KEY,
  grok: process.env.GROK_API_KEY
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);

// Example: Get a recommendation for a prompt
const prompt = "Generate a Python function to calculate Fibonacci numbers";
const recommendation = gptoggle.recommendModel(prompt);
console.log("Recommended model:", recommendation);
```

## Option 2: Direct Download (For Any Environment)

If you prefer not to use npm or are working in a restricted environment, you can download and use the standalone file:

### For Node.js:

1. Download the standalone file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

2. Make sure to install the axios dependency:

```bash
npm install axios
```

3. Use it in your code:

```javascript
const { GPToggle } = require('./gptoggle.js');

// Setup your API keys
const apiKeys = {
  openai: process.env.OPENAI_API_KEY
  // Add other providers as needed
};

// Create a GPToggle instance
const gptoggle = new GPToggle({}, apiKeys);
```

### For Web Browsers:

1. Download the standalone file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

2. Include it in your HTML:

```html
<script src="gptoggle.js"></script>

<script>
  // Create a GPToggle instance
  const gptoggle = new GPToggle({}, {
    openai: 'your-openai-api-key'
    // Add other providers as needed
  });
  
  // Use GPToggle
  const recommendation = gptoggle.recommendModel("Your prompt here");
  console.log(recommendation);
</script>
```

## API Keys

GPToggle requires API keys for the providers you want to use:

- OpenAI: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Claude: Get your API key from [Anthropic Console](https://console.anthropic.com/)
- Gemini: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Grok: Get your API key from [xAI](https://x.ai/)

## Examples

Check out the example files in the repository for more detailed usage:

- `gptoggle-example.js` - Node.js example
- `gptoggle-web-example.html` - Web browser example

## Customization

You can customize provider priority and models by passing a configuration object:

```javascript
const config = {
  providerPriority: ['openai', 'claude', 'gemini'], // Order of preference
  models: {
    openai: {
      default: 'gpt-3.5-turbo',
      advanced: 'gpt-4o',
      vision: 'gpt-4o'
    }
    // Add other providers as needed
  }
};

const gptoggle = new GPToggle(config, apiKeys);
```