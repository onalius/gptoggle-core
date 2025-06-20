# GPToggle Quick Start Guide

Get up and running with GPToggle in under 5 minutes. Choose your preferred implementation:

## JavaScript/TypeScript (Recommended)

### 1. Get the Core Files

**Option A: Use Enhanced Version (v1.0.3+)**
```bash
# Download the enhanced JavaScript implementation
curl -O https://raw.githubusercontent.com/your-repo/gptoggle/main/gptoggle_enhanced.js
```

**Option B: Use Model-Agnostic Version (v2.0+)**
```bash
# Download the model-agnostic implementation
curl -O https://raw.githubusercontent.com/your-repo/gptoggle/main/gptoggle_model_agnostic.js
```

### 2. Set Up API Keys

Create a `.env` file or set environment variables:
```bash
export OPENAI_API_KEY="your-openai-key-here"
export ANTHROPIC_API_KEY="your-claude-key-here"
export GOOGLE_AI_API_KEY="your-gemini-key-here"
export XAI_API_KEY="your-grok-key-here"
```

### 3. Basic Usage

**Enhanced Version:**
```javascript
const { GPToggle } = require('./gptoggle_enhanced');

// Initialize with API keys
const gptoggle = new GPToggle({}, {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY,
  gemini: process.env.GOOGLE_AI_API_KEY,
  grok: process.env.XAI_API_KEY
});

// Get automatic model recommendation
const recommendation = gptoggle.recommendModel("Write a Python function to calculate fibonacci numbers");
console.log(`Recommended: ${recommendation.provider}:${recommendation.model}`);
console.log(`Reason: ${recommendation.reason}`);

// Get task-specific recommendations for complex prompts
const taskRecs = gptoggle.getTaskRecommendations("Create a marketing plan and build a React signup form");
console.log(JSON.stringify(taskRecs, null, 2));
```

**Model-Agnostic Version:**
```javascript
const { GPToggle } = require('./gptoggle_model_agnostic');

// Initialize and register models
const gptoggle = new GPToggle({}, {
  openai: process.env.OPENAI_API_KEY,
  anthropic: process.env.ANTHROPIC_API_KEY
});

// Register models with rich metadata
gptoggle.registerModel({
  provider: "openai",
  modelId: "gpt-4o",
  displayName: "GPT-4o",
  capabilities: ["text", "vision", "code", "reasoning"],
  contextWindow: 128000,
  intelligence: 5,
  speed: 3,
  tiers: ["standard"]
});

// Get capability-based recommendations
const recommendation = gptoggle.recommendModel("Analyze this data and create visualizations");
console.log(recommendation);
```

## Python

### 1. Install

```bash
# Install from the gptoggle package
pip install gptoggle-core

# Or use standalone file
curl -O https://raw.githubusercontent.com/your-repo/gptoggle/main/gptoggle_minimal.py
```

### 2. Basic Usage

```python
from gptoggle import get_response, recommend_model

# Set API keys as environment variables first
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
os.environ['ANTHROPIC_API_KEY'] = 'your-key-here'

# Get automatic recommendation
recommendation = recommend_model("Create a data analysis script in Python")
print(f"Recommended: {recommendation['provider']}:{recommendation['model']}")

# Get response with auto-selection
response = get_response("Explain machine learning concepts")
print(response)
```

## Browser Usage

### 1. Include in HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>GPToggle Browser Example</title>
</head>
<body>
    <script src="gptoggle_enhanced.js"></script>
    <script>
        // Initialize GPToggle
        const gptoggle = new GPToggle({}, {
            openai: 'your-openai-key',
            claude: 'your-claude-key'
        });
        
        // Get recommendation
        const recommendation = gptoggle.recommendModel("Help me design a website");
        console.log(recommendation);
        
        // For security, avoid putting API keys directly in frontend code
        // Consider using a backend proxy for API calls
    </script>
</body>
</html>
```

## Key Features to Try

### 1. Multi-Task Detection
```javascript
const prompt = "Create a marketing email campaign, write the HTML template, and analyze competitor pricing";
const taskRecs = gptoggle.getTaskRecommendations(prompt);
// Returns recommendations for marketing, coding, and data analysis tasks
```

### 2. Follow-up Suggestions
```javascript
const followups = gptoggle.getFollowupRecommendations("Write a React component for user authentication");
// Suggests follow-up tasks like testing, documentation, optimization
```

### 3. Provider-Specific Strengths
```javascript
const recommendation = gptoggle.recommendModel("Write creative marketing copy");
// Likely recommends Claude for creative writing
// Explains: "Claude excels at understanding brand voice and creative copywriting"
```

### 4. Model Registry (v2.0+)
```javascript
// Filter models by capabilities
const visionModels = gptoggle.getAvailableModels({ capability: 'vision' });
const codeModels = gptoggle.getAvailableModels({ capability: 'code' });

// Filter by tier
const freeModels = gptoggle.getAvailableModels({ tier: 'free' });
```

## Configuration Options

### Custom Provider Priority
```javascript
const config = {
  providerPriority: ['claude', 'openai', 'gemini', 'grok'], // Your preferred order
  defaultParams: {
    temperature: 0.7,
    maxTokens: 1500
  }
};

const gptoggle = new GPToggle(config, apiKeys);
```

### Custom Model Mappings
```javascript
const config = {
  models: {
    openai: {
      creative: 'gpt-4o',      // Use GPT-4o for creative tasks
      technical: 'gpt-4-turbo', // Use GPT-4 Turbo for technical tasks
      default: 'gpt-3.5-turbo'
    }
  }
};
```

## Next Steps

1. **Explore Examples**: Check out `example_enhanced.js` and `example_model_agnostic.js` for detailed usage patterns
2. **Read Documentation**: See the full documentation in the repository
3. **Try Different Providers**: Experiment with different AI providers to see their strengths
4. **Customize Configuration**: Adjust provider priorities and model mappings for your use case

## Common Issues

**No API Keys Found**: Make sure environment variables are set correctly
```bash
echo $OPENAI_API_KEY  # Should show your key
```

**Provider Not Available**: Check if the API key is valid and has sufficient credits

**Model Not Found**: Ensure you're using correct model names for each provider

## Getting Help

- Check the main documentation in `README.md`
- Look at example files for usage patterns
- Review the changelog for recent updates
- Test with simple prompts first before complex multi-task requests