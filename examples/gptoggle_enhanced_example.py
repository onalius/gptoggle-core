#!/usr/bin/env python3
"""
GPToggle Enhanced Example

This example demonstrates how to use the enhanced GPToggle features,
including task-specific model recommendations and component-specific
model suggestions within responses.

Make sure your API keys are set as environment variables:
- OPENAI_API_KEY for OpenAI
- ANTHROPIC_API_KEY for Claude
- GOOGLE_API_KEY for Gemini
- XAI_API_KEY for Grok
"""

import os
from pprint import pprint
from gptoggle_enhanced import (
    get_response, 
    recommend_model, 
    get_task_recommendations, 
    get_available_providers,
    generate_model_suggestions
)

def check_api_keys():
    """Check if required API keys are set."""
    print("Checking available providers...")
    providers = get_available_providers()
    
    if not providers:
        print("No API keys found. Please set at least one of the following environment variables:")
        print("- OPENAI_API_KEY: for OpenAI models (GPT-3.5, GPT-4o)")
        print("- ANTHROPIC_API_KEY: for Claude models")
        print("- GOOGLE_API_KEY: for Google Gemini models")
        print("- XAI_API_KEY: for xAI Grok models")
        return False
    
    print(f"Available providers: {', '.join(p.capitalize() for p in providers)}")
    return True

def demo_single_task():
    """Demonstrate recommendations for a single-task prompt."""
    prompt = "Create a marketing plan for a new eco-friendly water bottle."
    
    print("\n===== Single Task Example =====")
    print(f"Prompt: \"{prompt}\"\n")
    
    # Get model recommendation
    provider, model, reason, tasks = recommend_model(prompt)
    print(f"Recommended model: {provider.capitalize()}'s {model}")
    print(f"Reason: {reason}")
    
    # Get task recommendations
    task_recs = get_task_recommendations(prompt)
    print("\nTask-specific recommendations:")
    for task in task_recs["task_recommendations"]:
        print(f"- {task['task_description']}:")
        for rec in task["recommendations"][:2]:  # Show top 2
            print(f"  * {rec['provider'].capitalize()}'s {rec['model']}")
            print(f"    {rec['strength']}")
    
    # Uncomment to get actual response
    # print("\nGetting response...")
    # response = get_response(prompt)
    # print("\nResponse:")
    # print(response)

def demo_multi_task():
    """Demonstrate recommendations for a multi-task prompt."""
    prompt = "Create a marketing campaign for our eco-friendly product line and develop a landing page in HTML/CSS to showcase it."
    
    print("\n===== Multi-Task Example =====")
    print(f"Prompt: \"{prompt}\"\n")
    
    # Get model recommendation
    provider, model, reason, tasks = recommend_model(prompt)
    print(f"Recommended model: {provider.capitalize()}'s {model}")
    print(f"Reason: {reason}")
    
    # Get detailed task recommendations
    task_recs = get_task_recommendations(prompt)
    print("\nTask-specific recommendations:")
    for task in task_recs["task_recommendations"]:
        print(f"- {task['task_description']}:")
        for rec in task["recommendations"][:2]:  # Show top 2
            print(f"  * {rec['provider'].capitalize()}'s {rec['model']}")
            print(f"    {rec['strength']}")
    
    # Generate model suggestions that would be embedded in the response
    suggestions = generate_model_suggestions(prompt, provider, model)
    print("\nModel Suggestions that would be included in the response:")
    print(suggestions)
    
    # Uncomment to get actual response
    # print("\nGetting response...")
    # response = get_response(prompt)
    # print("\nResponse:")
    # print(response)

def main():
    """Run the demonstration."""
    print("GPToggle Enhanced Example")
    print("=========================")
    
    if not check_api_keys():
        return
    
    demo_single_task()
    demo_multi_task()

if __name__ == "__main__":
    main()