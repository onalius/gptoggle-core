"""
Example script showing how to use the GPToggle package with Perplexity API.

This script demonstrates using the Perplexity API integration in GPToggle,
specifically for generating responses with Perplexity's Llama-Sonar models,
which provide up-to-date information via online search.

Make sure your PERPLEXITY_API_KEY environment variable is set.
"""

import os
import sys
from gptoggle_enhanced import get_response, recommend_model, get_task_recommendations

def check_api_key():
    """Check if Perplexity API key is set."""
    if not os.environ.get("PERPLEXITY_API_KEY"):
        print("PERPLEXITY_API_KEY environment variable is not set.")
        print("Please set it and try again.")
        return False
    return True

def demo_perplexity_response():
    """Demonstrate getting responses from Perplexity API."""
    print("\n=== Perplexity API Response Demo ===\n")
    
    # Explicitly request Perplexity - a query that benefits from up-to-date information
    prompt = "What are the latest advancements in AI as of 2024? Provide a concise summary."
    print(f"Prompt: {prompt}")
    
    try:
        # Get response specifically from Perplexity's small model
        response = get_response(prompt, provider_name="perplexity", model_name="llama-3.1-sonar-small-128k-online")
        print("\nPerplexity (Small) Response:")
        print(response)
        
        # Get response from Perplexity's larger model
        response = get_response(prompt, provider_name="perplexity", model_name="llama-3.1-sonar-large-128k-online")
        print("\nPerplexity (Large) Response:")
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_auto_select_with_perplexity():
    """Demonstrate auto-selection with Perplexity as an option."""
    print("\n=== Auto-Selection with Perplexity Demo ===\n")
    
    # A prompt that might select Perplexity based on data analysis needs
    prompt = "Analyze the current market trends for electric vehicles and provide key insights."
    print(f"Prompt: {prompt}")
    
    try:
        # Get provider and model recommendation
        provider, model, reason, _ = recommend_model(prompt)
        print(f"\nRecommended provider: {provider}")
        print(f"Recommended model: {model}")
        print(f"Reason: {reason}")
        
        # Get task recommendations
        task_recs = get_task_recommendations(prompt)
        
        # Show all provider recommendations for the detected tasks
        if task_recs["task_recommendations"]:
            print("\nTask-specific recommendations:")
            for task in task_recs["task_recommendations"]:
                print(f"- {task['task_description']}:")
                for rec in task["recommendations"]:
                    print(f"  * {rec['provider'].capitalize()}'s {rec['model']}")
                    print(f"    Strength: {rec['strength']}")
        
        # Get the auto-selected response
        print("\nGetting response from auto-selected provider...")
        response = get_response(prompt)
        print(f"\nResponse from {provider} ({model}):")
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def compare_current_events_knowledge():
    """Compare Perplexity with other providers on current events knowledge."""
    print("\n=== Current Events Knowledge Comparison ===\n")
    
    # A prompt that tests current knowledge
    prompt = "What were the major technology announcements from the last month? List the top 3."
    print(f"Prompt: {prompt}")
    
    providers = ["perplexity", "openai", "claude"]
    for provider in providers:
        if provider == "perplexity" and not os.environ.get("PERPLEXITY_API_KEY"):
            print(f"\nSkipping {provider} (API key not set)")
            continue
        if provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
            print(f"\nSkipping {provider} (API key not set)")
            continue
        if provider == "claude" and not os.environ.get("ANTHROPIC_API_KEY"):
            print(f"\nSkipping {provider} (API key not set)")
            continue
        
        try:
            print(f"\nGetting response from {provider}...")
            response = get_response(prompt, provider_name=provider)
            print(f"Response from {provider}:")
            print(response)
        except Exception as e:
            print(f"Error with {provider}: {str(e)}")

def main():
    """Run the demonstration."""
    if not check_api_key():
        sys.exit(1)
    
    print("Perplexity API Integration Example")
    print("==================================")
    
    demo_perplexity_response()
    demo_auto_select_with_perplexity()
    compare_current_events_knowledge()
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main()