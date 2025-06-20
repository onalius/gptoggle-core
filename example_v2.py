"""
GPToggle v2.0 Example - Model-Agnostic Implementation

This example demonstrates how to use the new model-agnostic version
of GPToggle (v2.0) with its dynamic model registry.

Features demonstrated:
- Initializing with multiple provider API keys
- Registering models with rich metadata
- Customizing model registry
- Getting smart model recommendations
- Using provider-agnostic responses
- Registering custom API handlers
"""

import os
import asyncio
from pprint import pprint
from gptoggle_v2 import GPToggle


def check_api_keys():
    """Check which API keys are available in the environment."""
    keys = {
        "OpenAI": os.environ.get("OPENAI_API_KEY"),
        "Anthropic": os.environ.get("ANTHROPIC_API_KEY"),
        "Google": os.environ.get("GOOGLE_API_KEY"),
        "xAI": os.environ.get("XAI_API_KEY"),
        "Perplexity": os.environ.get("PERPLEXITY_API_KEY"),
    }
    
    print("Available API Keys:")
    for provider, key in keys.items():
        status = "✓ Available" if key else "✗ Not found"
        print(f"  {provider}: {status}")
    print()
    
    return {k.lower(): v for k, v in keys.items() if v}


def register_custom_models(gptoggle):
    """Register some custom models with rich metadata."""
    # Example of registering a custom model with detailed metadata
    gptoggle.register_model({
        "provider": "custom",
        "model_id": "my-fine-tuned-model",
        "display_name": "My Fine-tuned Model",
        "capabilities": ["text", "code", "domain-specific"],
        "strengths": {"domain-specific": 5, "code": 4},
        "context_window": 8000,
        "intelligence": 4,
        "speed": 5,
        "description": "A custom fine-tuned model for my specific domain"
    })
    
    # You can also update an existing model with new capabilities
    if gptoggle.registry.has_model("openai", "gpt-4o"):
        # Get the existing model
        model = gptoggle.registry.get_model("openai", "gpt-4o")
        # Add a new capability
        if "domain-specific" not in model["capabilities"]:
            model["capabilities"].append("domain-specific")
        # Update strengths
        model["strengths"]["domain-specific"] = 4
        # Re-register the updated model
        gptoggle.register_model(model)


async def demo_model_recommendations(gptoggle):
    """Demonstrate the model recommendation system."""
    prompts = [
        "Write a Python function to analyze an image and detect objects",
        "Create a bedtime story about a dragon who loves mathematics",
        "Explain quantum computing to a 10-year-old",
        "Debug this JavaScript code: function add(a, b) { reutrn a + b; }"
    ]
    
    print("=== Model Recommendations ===")
    for prompt in prompts:
        print(f"\nPrompt: \"{prompt}\"")
        recommendation = gptoggle.recommend_model(prompt)
        print(f"  Recommended: {recommendation['provider']}:{recommendation['model']}")
        print(f"  Reason: {recommendation['reason']}")
    
    # Show task-specific recommendations
    complex_prompt = "Create a web application that uses computer vision to detect objects and displays the results on a dashboard"
    print("\n=== Task-Specific Recommendations ===")
    print(f"Complex prompt: \"{complex_prompt}\"")
    
    task_recs = gptoggle.get_task_recommendations(complex_prompt)
    print(f"\nOverall recommendation: {task_recs['overall']['provider']}:{task_recs['overall']['model']}")
    print(f"Reason: {task_recs['overall']['reason']}")
    
    print("\nAlternative models:")
    for i, rec in enumerate(task_recs['recommendations'], 1):
        print(f"  {i}. {rec['provider']}:{rec['model']}")
        print(f"     {rec['reason']}")
        if 'strength' in rec:
            print(f"     {rec['strength']}")


async def register_custom_handler(gptoggle):
    """Demonstrate registering a custom provider handler."""
    # Create a custom handler for a hypothetical API
    async def custom_api_handler(prompt, model, api_key, params):
        print(f"[Custom handler] Processing request for model: {model}")
        print(f"[Custom handler] Using API key: {api_key[:4]}...")
        print(f"[Custom handler] Parameters: {params}")
        
        # In a real handler, this would call the actual API
        return f"This is a response from the custom API handler for prompt: '{prompt}'"
    
    # Register the handler with GPToggle
    gptoggle.register_provider_handler("custom", custom_api_handler)
    
    # Add our custom model if not already added
    if not gptoggle.registry.has_model("custom", "my-fine-tuned-model"):
        register_custom_models(gptoggle)
    
    # Use the custom handler
    print("\n=== Custom API Handler ===")
    response = await gptoggle.get_response(
        "Test the custom handler",
        provider_name="custom",
        model_name="my-fine-tuned-model",
        params={"temperature": 0.5, "custom_param": "value"}
    )
    
    print("\nResponse from custom handler:")
    print(response)


async def main():
    """Run the demonstration."""
    print("GPToggle v2.0 Example - Model-Agnostic Implementation\n")
    
    # Check which API keys we have available
    api_keys = check_api_keys()
    
    # Initialize GPToggle with available API keys
    gptoggle = GPToggle(api_keys=api_keys)
    
    # Load the sample models that come with GPToggle v2
    # In a real application, you might load these from a database or JSON file
    from gptoggle_v2 import sample_models
    gptoggle.register_models(sample_models)
    
    # Register some custom models
    register_custom_models(gptoggle)
    
    # Demonstrate model recommendations
    await demo_model_recommendations(gptoggle)
    
    # Demonstrate custom API handler
    await register_custom_handler(gptoggle)
    
    print("\nExample completed!")


if __name__ == "__main__":
    asyncio.run(main())