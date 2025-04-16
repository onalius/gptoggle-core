#!/usr/bin/env python3
"""
Example script showing how to use the gptoggle package.

This script demonstrates the main features of gptoggle, including:
- Auto-selecting models
- Getting responses
- Comparing models
"""

import os
import sys
from gptoggle import get_response, choose_model, compare_models, list_available_models

def check_api_key():
    """Check if the OpenAI API key is set as an environment variable."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key with:")
        print("export OPENAI_API_KEY='your-api-key'")
        return False
    return True

def demo_auto_select():
    """Demonstrate auto-selection of models."""
    prompts = [
        "What is the capital of France?",
        "Write a function in Python to find the greatest common divisor of two numbers",
        "Write a short story about a robot learning to paint",
        "Explain the theory of relativity in simple terms that a 10-year-old would understand"
    ]
    
    print("\n=== Auto-Selection Demo ===")
    for prompt in prompts:
        model, reason = choose_model(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Selected model: {model}")
        print(f"Reason: {reason}")

def demo_get_response():
    """Demonstrate getting responses from models."""
    prompt = "What are three interesting facts about space?"
    model = "gpt-3.5-turbo"  # Using a faster model for the demo
    
    print("\n=== Response Demo ===")
    print(f"Prompt: {prompt}")
    print(f"Model: {model}")
    print("\nGetting response...")
    response = get_response(prompt, model)
    print("\nResponse:")
    print(response)

def main():
    """Run the demonstration."""
    if not check_api_key():
        return
    
    print("=== GPToggle Demo ===")
    print("This script demonstrates the main features of the gptoggle package.\n")
    
    # Show available models
    print("Available models:")
    list_available_models()
    
    # Demo auto-selection
    demo_auto_select()
    
    # Demo response (only if requested)
    user_input = input("\nWould you like to see a sample response? (y/n): ")
    if user_input.lower() == 'y':
        demo_get_response()
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main()