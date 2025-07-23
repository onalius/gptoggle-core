"""
Example script showing how to use the GPToggle package with Meta's Llama API.

This script demonstrates using the Meta Llama API integration in GPToggle,
specifically for generating text responses.

Make sure your META_AI_API_KEY environment variable is set.
"""

import os
import sys
from gptoggle_enhanced import get_response, recommend_model, get_task_recommendations

def check_api_key():
    """Check if Meta AI API key is set."""
    if not os.environ.get("META_AI_API_KEY"):
        print("META_AI_API_KEY environment variable is not set.")
        print("Please set it and try again.")
        return False
    return True

def demo_llama_response():
    """Demonstrate getting responses from Meta's Llama API."""
    print("\n=== Meta Llama API Response Demo ===\n")
    
    # Explicitly request Llama
    prompt = "Write a short poem about artificial intelligence."
    print(f"Prompt: {prompt}")
    
    try:
        # Get response specifically from Llama
        response = get_response(prompt, provider_name="llama", model_name="llama-3-70b-instruct")
        print("\nLlama 3 (70B) Response:")
        print(response)
        
        # Get response from Llama with the default model
        response = get_response(prompt, provider_name="llama")
        print("\nLlama 3 (Default) Response:")
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_auto_select_with_llama():
    """Demonstrate auto-selection with Llama as an option."""
    print("\n=== Auto-Selection with Llama Demo ===\n")
    
    # A prompt that might select Llama based on provider priority
    prompt = "Explain how neural networks process information."
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

def main():
    """Run the demonstration."""
    if not check_api_key():
        sys.exit(1)
    
    print("Meta Llama API Integration Example")
    print("==================================")
    
    demo_llama_response()
    demo_auto_select_with_llama()
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main()