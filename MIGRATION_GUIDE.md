# Migrating from GPToggle v1.x to v2.0

This guide helps you migrate from the hardcoded model approach in GPToggle v1.x to the new model-agnostic implementation in v2.0.

## Key Changes in v2.0

- **Dynamic Model Registry**: Models are now registered at runtime instead of being hardcoded
- **Rich Model Metadata**: Models have detailed capabilities and attributes
- **Capability-Based Selection**: Models are selected based on capabilities rather than categories
- **Provider Handlers**: Custom API handlers can be registered for new providers

## Step-by-Step Migration Guide

### 1. Update Imports

**v1.x:**
```python
from gptoggle import get_response, recommend_model
# or
from gptoggle_enhanced import get_response, get_task_recommendations
```

**v2.0:**
```python
from gptoggle_v2 import GPToggle
```

### 2. Initialize GPToggle Class

**v1.x:**
```python
# No initialization needed
response = get_response("Your prompt")
```

**v2.0:**
```python
# Initialize with API keys
gptoggle = GPToggle(api_keys={
    "openai": os.environ.get("OPENAI_API_KEY"),
    "anthropic": os.environ.get("ANTHROPIC_API_KEY")
})

# Register models (built-in sample_models or your own)
from gptoggle_v2 import sample_models
gptoggle.register_models(sample_models)

# Now use the instance
response = await gptoggle.get_response("Your prompt")
```

### 3. Getting Responses

**v1.x:**
```python
# Simple response
response = get_response("Your prompt")

# Specifying provider and model
response = get_response("Your prompt", provider_name="openai", model_name="gpt-4")

# With parameters
response = get_response("Your prompt", temperature=0.8, max_tokens=500)
```

**v2.0:**
```python
# Simple response (note: async/await is now required)
response = await gptoggle.get_response("Your prompt")

# Specifying provider and model
response = await gptoggle.get_response("Your prompt", provider_name="openai", model_name="gpt-4o")

# With parameters
response = await gptoggle.get_response("Your prompt", params={"temperature": 0.8, "max_tokens": 500})
```

### 4. Model Recommendations

**v1.x:**
```python
recommendation = recommend_model("Your prompt")
provider, model, reason = recommendation
```

**v2.0:**
```python
recommendation = gptoggle.recommend_model("Your prompt")
# recommendation is a dictionary with keys:
# - provider
# - model
# - reason
# - requirements
# - score
```

### 5. Task-Specific Recommendations

**v1.x:**
```python
task_recommendations = get_task_recommendations("Your prompt")
# Returns dictionary with overall_recommendation and task_recommendations
```

**v2.0:**
```python
task_recommendations = gptoggle.get_task_recommendations("Your prompt")
# Returns dictionary with overall and recommendations
```

### 6. Converting Hardcoded Models to Registry

If you previously added custom models by modifying the source code, you'll now need to register them using the registry:

**v1.x:**
```python
# In source code:
MODELS = {
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "anthropic": ["claude-instant-1", "claude-2"]
}
```

**v2.0:**
```python
# Register models at runtime:
gptoggle.register_model({
    "provider": "openai",
    "model_id": "gpt-3.5-turbo",
    "capabilities": ["text", "code"],
    "intelligence": 3,
    "speed": 4
})

gptoggle.register_model({
    "provider": "openai",
    "model_id": "gpt-4",
    "capabilities": ["text", "code", "reasoning"],
    "intelligence": 4,
    "speed": 3
})
```

For bulk registration, create a list of model objects:

```python
models = [
    {
        "provider": "openai",
        "model_id": "gpt-3.5-turbo",
        "capabilities": ["text", "code"],
        "intelligence": 3
    },
    {
        "provider": "anthropic",
        "model_id": "claude-instant-1",
        "capabilities": ["text"],
        "intelligence": 3
    }
]

gptoggle.register_models(models)
```

### 7. Adding Custom Providers

**v1.x:**
```python
# Would require source code modifications
```

**v2.0:**
```python
# Register a custom handler
async def my_provider_handler(prompt, model, api_key, params):
    # Implementation here
    return "Response text"
    
gptoggle.register_provider_handler("my_provider", my_provider_handler)

# Register models for this provider
gptoggle.register_model({
    "provider": "my_provider",
    "model_id": "my-model",
    "capabilities": ["text"],
    "intelligence": 3
})

# Use it
response = await gptoggle.get_response("Prompt", provider_name="my_provider", model_name="my-model")
```

## Rich Model Attributes Reference

For best results, provide detailed model metadata:

```python
model = {
    "provider": "openai",                    # Required
    "model_id": "gpt-4o",                    # Required
    "display_name": "GPT-4o",                # Optional
    "capabilities": [                         # Required
        "text", "vision", "code", 
        "reasoning", "creativity"
    ],
    "strengths": {                            # Optional
        "general": 5,                         # 1-5 scale
        "code": 5,
        "math": 4, 
        "creativity": 4,
        "reasoning": 5
    },
    "weaknesses": ["hallucination"],          # Optional
    "context_window": 128000,                 # Optional
    "intelligence": 5,                        # Optional, 1-5 scale
    "speed": 4,                               # Optional, 1-5 scale
    "tiers": ["standard"],                    # Optional
    "pricing": {                              # Optional
        "input_tokens": 0.00005,
        "output_tokens": 0.00015
    },
    "knowledge_cutoff": "2023-04",            # Optional
    "released": "2023-05-13",                 # Optional
    "deprecated": False                       # Optional
}
```

## Loading Models from JSON

For larger applications, store model definitions in a JSON file:

```python
import json

# Load models from JSON file
with open('models.json', 'r') as f:
    models = json.load(f)
    
gptoggle.register_models(models)
```

## Examples

See the `example_v2.py` file for complete examples of using GPToggle v2.0.