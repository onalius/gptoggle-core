#!/usr/bin/env python3
"""
GPToggle Follow-up Task Recommendations Example

This example demonstrates the follow-up task recommendation feature,
which suggests specific models for potential follow-up tasks based on
the initial prompt.

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
    get_followup_recommendations, 
    generate_model_suggestions,
    get_available_providers
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

def demo_followup_recommendations():
    """Demonstrate recommendations for follow-up tasks."""
    # Example 1: Business Strategy Prompt
    business_prompt = "Create a business plan for a SaaS startup in the AI space"
    
    print("\n===== Business Strategy Example =====")
    print(f"Prompt: \"{business_prompt}\"\n")
    
    # Get model recommendation and detected tasks
    provider, model, reason, detected_tasks = recommend_model(business_prompt)
    print(f"Recommended model: {provider.capitalize()}'s {model}")
    print(f"Reason: {reason}")
    
    # Get task recommendations
    task_recs = get_task_recommendations(business_prompt)
    
    print("\nDetected Tasks:")
    for task in task_recs["task_recommendations"]:
        print(f"- {task['task_description']}")
    
    # Get follow-up recommendations
    followup_recs = get_followup_recommendations(task_recs["task_recommendations"])
    
    print("\nRecommended Follow-up Tasks:")
    for followup in followup_recs:
        print(f"- {followup['description']}")
        top_rec = followup["recommendations"][0]
        print(f"  Recommended model: {top_rec['provider'].capitalize()}'s {top_rec['model']}")
    
    # Generate model suggestions
    suggestions = generate_model_suggestions(business_prompt, provider, model)
    print("\nModel Suggestions that would be included in the response:")
    print(suggestions)
    
    # Example 2: Multi-domain Prompt
    multi_prompt = "Design a marketing strategy for our new app and implement a landing page with user authentication"
    
    print("\n===== Multi-Domain Example =====")
    print(f"Prompt: \"{multi_prompt}\"\n")
    
    # Get model recommendation and detected tasks
    provider, model, reason, detected_tasks = recommend_model(multi_prompt)
    print(f"Recommended model: {provider.capitalize()}'s {model}")
    print(f"Reason: {reason}")
    
    # Get task recommendations
    task_recs = get_task_recommendations(multi_prompt)
    
    print("\nDetected Tasks:")
    for task in task_recs["task_recommendations"]:
        print(f"- {task['task_description']}")
    
    # Get follow-up recommendations
    followup_recs = get_followup_recommendations(task_recs["task_recommendations"])
    
    print("\nRecommended Follow-up Tasks:")
    for followup in followup_recs:
        print(f"- {followup['description']}")
        top_rec = followup["recommendations"][0]
        print(f"  Recommended model: {top_rec['provider'].capitalize()}'s {top_rec['model']}")
    
    # Generate model suggestions
    suggestions = generate_model_suggestions(multi_prompt, provider, model)
    print("\nModel Suggestions that would be included in the response:")
    print(suggestions)

def main():
    """Run the demonstration."""
    print("GPToggle Follow-up Task Recommendations Example")
    print("==============================================")
    
    if not check_api_keys():
        return
    
    demo_followup_recommendations()

if __name__ == "__main__":
    main()