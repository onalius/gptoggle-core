# GPToggle Quick Start Guide

Get up and running with GPToggle in under 5 minutes! This guide covers installation, basic usage, and your first adaptive modules.

## 📦 Installation

### Option 1: Python Package (Recommended)
```bash
pip install gptoggle
```

### Option 2: JavaScript/TypeScript Package
```bash
npm install gptoggle
```

### Option 3: Standalone Files
Download individual files for no-installation usage:
- [gptoggle_v2.py](../core/gptoggle_v2.py) - Python standalone
- [gptoggle.js](../core/gptoggle.js) - JavaScript standalone

## 🔑 API Key Setup

GPToggle supports multiple AI providers. Set up at least one:

```bash
# OpenAI (recommended for beginners)
export OPENAI_API_KEY="sk-your-key-here"

# Anthropic Claude
export ANTHROPIC_API_KEY="your-key-here"

# Google Gemini
export GOOGLE_API_KEY="your-key-here"

# Optional: Other providers
export XAI_API_KEY="your-key-here"
export META_AI_API_KEY="your-key-here"
export PERPLEXITY_API_KEY="your-key-here"
```

Don't have API keys? Get them here:
- [OpenAI API](https://platform.openai.com/api-keys)
- [Anthropic Claude](https://console.anthropic.com/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚀 First Steps

### 1. Basic Query (Python)
```python
from gptoggle_v2 import GPToggle

# Initialize GPToggle
gpt = GPToggle()

# Simple query
response = gpt.query("Explain quantum computing in simple terms")
print(response['response'])
```

### 2. Basic Query (JavaScript)
```javascript
import { GPToggle } from 'gptoggle';

const gpt = new GPToggle();

// Simple query
const result = await gpt.query("Explain quantum computing in simple terms");
console.log(result.response);
```

### 3. Web Interface
```bash
# Start the web server
python web/main.py

# Open browser to http://localhost:5000
```

## 🧩 Your First Adaptive Modules

The magic of GPToggle v2.0 is its ability to automatically create and manage modules based on your needs.

### Shopping List Module
```python
# This automatically creates a shopping list module
response = gpt.query("I need to buy milk, eggs, bread, and bananas for this week")

print(response['response'])
print(f"Modules created: {len(response.get('moduleActions', []))}")

# Add more items to the same list
response = gpt.query("Also add cheese and yogurt to my shopping list")
```

### Party Planning Module
```python
# This creates a party planning module
response = gpt.query("I'm planning a birthday party for March 15th with Alice, Bob, and Charlie")

# The system automatically extracts:
# - Date: March 15th
# - Guests: Alice, Bob, Charlie
# - Type: Birthday party

# Add tasks to the party plan
response = gpt.query("Add tasks: book venue, order cake, send invitations")
```

### Learning Interest Module
```python
# This creates an interest tracking module
response = gpt.query("I'm fascinated by Virginia Woolf and her stream of consciousness writing")

# The system tracks:
# - Keywords: Virginia Woolf, stream of consciousness, writing
# - Interest level and engagement
# - Related learning topics
```

### Calendar Module
```python
# This creates a calendar/schedule module
response = gpt.query("I have soccer practice scheduled for July 5th at 3 PM")

# Add more events
response = gpt.query("Also schedule dentist appointment for July 10th")
```

## 🎯 Understanding Module Actions

When GPToggle processes your queries, it can take several actions:

```python
response = gpt.query("Add apples to my grocery list and schedule gym session for tomorrow")

# Check what modules were affected
for action in response.get('moduleActions', []):
    print(f"Action: {action['action']}")           # create, update, or access
    print(f"Module Type: {action['moduleType']}")  # list, planner, calendar, etc.
    print(f"Success: {action['success']}")         # True if successful
```

## 🔍 Viewing Your Modules

```python
# Get user profile with all modules
user_profile = gpt.get_user_profile()

# Get modules summary
summary = user_profile.get_modules_summary()
print(f"Total modules: {summary['totalModules']}")
print(f"Active modules: {len(summary['activeModules'])}")

# List modules by type
for module_type, count in summary['modulesByType'].items():
    if count > 0:
        print(f"{module_type.title()} modules: {count}")
```

## 🔄 Multi-Provider Usage

GPToggle can automatically select the best AI provider for your task, or you can specify one:

```python
# Automatic provider selection (default)
response = gpt.query("Write a creative story about a robot")

# Specify a provider
response = gpt.query("Analyze this data", provider="claude")

# Compare responses across providers
comparison = gpt.compare_providers(
    "Explain the benefits of renewable energy",
    providers=['openai', 'claude', 'gemini']
)

for provider, response in comparison.items():
    print(f"\n{provider.upper()}:")
    print(response[:200] + "...")
```

## 🌐 Universal Module IDs (UMID)

Every module gets a globally unique identifier that works across platforms:

```python
from modules.umidGenerator import UMIDGenerator

# Create your own module IDs
generator = UMIDGenerator('my-app')
umid = generator.generate_umid('list', ['shopping', 'groceries'])
print(f"Universal Module ID: {umid}")

# Example output: my-app.list.a1b2c3d4.1721737200.x7z9
```

This means modules created in GPToggle can be exported and used in other applications!

## ⚙️ Configuration

### Customize Provider Priority
```python
# Prefer Claude over OpenAI
gpt = GPToggle(provider_priority=['claude', 'openai', 'gemini'])
```

### Module Cleanup Settings
```python
# Configure how long modules stay active
gpt = GPToggle(module_cleanup_days=45)  # Default is 30 days
```

### Web Interface Configuration
```python
# In web/main.py, customize the Flask app
app.config['GPTOGGLE_THEME'] = 'dark'  # or 'light'
app.config['GPTOGGLE_MAX_MODULES'] = 100
```

## 🚨 Troubleshooting

### Common Issues

**"No API key found"**
```bash
# Make sure you've exported your API key
echo $OPENAI_API_KEY  # Should show your key

# If empty, export it:
export OPENAI_API_KEY="your-key-here"
```

**"Module not created"**
```python
# Check if the query was clear enough
response = gpt.query("Buy stuff")  # Too vague
response = gpt.query("I need to buy milk and eggs")  # Clear and specific
```

**"Provider not available"**
```python
# Check available providers
print(gpt.get_available_providers())

# Use a different provider
response = gpt.query("Hello", provider="claude")
```

### Getting Help

1. **Check the logs**: Look for error messages in the console
2. **Verify API keys**: Make sure they're valid and have credits
3. **Test with simple queries**: Start with basic requests
4. **Check documentation**: See the full [API Reference](API_REFERENCE.md)

## 📚 Next Steps

Now that you have GPToggle running:

1. **Explore Examples**: Check out the [examples/](../examples/) directory
2. **Read the Module Guide**: Learn more about [adaptive modules](MODULE_GUIDE.md)
3. **Try Advanced Features**: See [advanced usage patterns](API_REFERENCE.md#advanced-usage)
4. **Build Something**: Create your own application using GPToggle
5. **Contribute**: Help improve GPToggle by [contributing](../CONTRIBUTING.md)

## 💡 Pro Tips

- **Be specific**: Clear queries create better modules
- **Use natural language**: Write like you're talking to a person
- **Check module actions**: See what GPToggle created or updated
- **Experiment with providers**: Different AIs excel at different tasks
- **Export modules**: Use UMID system for cross-platform compatibility

Ready to build intelligent applications with adaptive modules? Let's go! 🚀