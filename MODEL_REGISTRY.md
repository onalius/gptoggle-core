# GPToggle Model Registry

## Overview

GPToggle v2.0 introduces a flexible, model-agnostic approach through a dynamic model registry system. This document explains how to use the model registry to register, manage, and select AI models with rich metadata.

## Key Features

- **Dynamic Model Registration**: Register models at runtime without code changes
- **Rich Model Metadata**: Detailed capability descriptions for intelligent selection
- **Capability-Based Selection**: Choose models based on specific requirements
- **Provider-Agnostic Interface**: Unified API across different AI providers

## Model Registry Format

Each model is registered with a comprehensive set of metadata attributes:

```python
model = {
    "provider": "openai",                    # Provider name (required)
    "model_id": "gpt-4o",                    # Model ID (required)
    "display_name": "GPT-4o",                # Human-readable name (optional)
    "capabilities": [                         # List of capabilities (required)
        "text", "vision", "code", 
        "reasoning", "creativity"
    ],
    "strengths": {                            # Strength ratings by domain (optional)
        "general": 5,                         # 1-5 scale
        "code": 5,
        "math": 4, 
        "creativity": 4,
        "reasoning": 5
    },
    "weaknesses": ["hallucination"],          # Known limitations (optional)
    "context_window": 128000,                 # Max context length in tokens (optional)
    "intelligence": 5,                        # Overall intelligence rating 1-5 (optional)
    "speed": 4,                               # Response speed rating 1-5 (optional)
    "tiers": ["standard"],                    # Pricing tiers (optional)
    "pricing": {                              # Cost information (optional)
        "input_tokens": 0.00005,
        "output_tokens": 0.00015
    },
    "knowledge_cutoff": "2023-04",            # Knowledge cutoff date (optional)
    "released": "2023-05-13",                 # Release date (optional)
    "deprecated": False                       # Deprecation status (optional)
}
```

## Registration Methods

### Register a Single Model

```python
from gptoggle_v2 import GPToggle

gptoggle = GPToggle(api_keys={"openai": "your-api-key"})

gptoggle.register_model({
    "provider": "openai",
    "model_id": "gpt-4o",
    "capabilities": ["text", "vision", "code"],
    "intelligence": 5,
    "context_window": 128000
})
```

### Register Multiple Models

```python
models = [
    {
        "provider": "openai",
        "model_id": "gpt-4o",
        "capabilities": ["text", "vision", "code"],
        "intelligence": 5
    },
    {
        "provider": "anthropic",
        "model_id": "claude-3-opus",
        "capabilities": ["text", "vision", "reasoning"],
        "intelligence": 5
    }
]

gptoggle.register_models(models)
```

## Custom Provider Handlers

You can register custom handlers for new AI providers:

```python
async def custom_provider_handler(prompt, model, api_key, params):
    # Custom implementation
    return f"Response to: {prompt}"
    
gptoggle.register_provider_handler("custom_provider", custom_provider_handler)
```

## Selection Process

When you call `recommend_model()`, GPToggle performs:

1. **Input Analysis**: Analyzes the prompt to identify requirements
2. **Filtering**: Filters models based on critical capability requirements
3. **Scoring**: Scores each eligible model using a weighted algorithm
4. **Ranking**: Ranks models by score and selects the best match
5. **Explanation**: Generates a human-readable explanation

Example:

```python
recommendation = gptoggle.recommend_model(
    "Create a Python function that analyzes images to detect objects"
)

# Result:
# {
#   "provider": "openai",
#   "model": "gpt-4o",
#   "reason": "Selected GPT-4o because it supports image analysis and has strong code capabilities.",
#   "requirements": {...},
#   "score": 158
# }
```

## Task-Specific Recommendations

For multi-faceted prompts, you can get more detailed recommendations:

```python
recommendations = gptoggle.get_task_recommendations(
    "Create a Python function that analyzes images to detect objects"
)

# Result includes overall recommendation and top alternatives:
# {
#   "overall": {...},
#   "recommendations": [
#     {"provider": "openai", "model": "gpt-4o", "reason": "..."},
#     {"provider": "anthropic", "model": "claude-3-opus", "reason": "..."}
#   ]
# }
```

## Adding New Capabilities

The capability system is extensible. To add new capabilities:

1. Add the capability to your model definitions
2. Update the analyzer to detect the new capability in prompts
3. Adjust scoring weights as needed

## Best Practices

1. **Provide Rich Metadata**: More detailed model attributes lead to better selection
2. **Use Consistent Scales**: Maintain consistent 1-5 ratings across models
3. **Regular Updates**: Update model attributes as capabilities evolve
4. **Custom Handlers**: Create specialized handlers for unique provider APIs
5. **Fallback Models**: Always register at least one reliable fallback model

## Migration from v1.x

If you're migrating from GPToggle v1.x:

1. Replace direct model references with the registry system
2. Convert hardcoded selection logic to use the recommendation engine
3. Update API calls to use the new provider-agnostic interface

See the migration guide for step-by-step instructions.