#!/usr/bin/env python3
"""
GPToggle Test Installation Script

This script verifies that GPToggle is correctly installed and configured.
It checks for available providers and performs a simple recommendation test.
"""

import os
import sys
from pprint import pprint

try:
    # Try importing from the installed package
    from gptoggle import get_available_providers, recommend_model, get_task_recommendations
    IMPORT_SOURCE = "installed package"
except ImportError:
    try:
        # Fall back to importing from the standalone file
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from gptoggle_enhanced import get_available_providers, recommend_model, get_task_recommendations
        IMPORT_SOURCE = "standalone file"
    except ImportError:
        print("Error: GPToggle could not be imported.")
        print("Please make sure you have installed the package or have the gptoggle_enhanced.py file available.")
        sys.exit(1)

def main():
    """Run tests to verify installation."""
    print(f"GPToggle Installation Test (imported from {IMPORT_SOURCE})")
    print("=" * 50)
    
    # Check available providers
    providers = get_available_providers()
    if providers:
        print(f"Available providers: {', '.join(p.capitalize() for p in providers)}")
    else:
        print("No providers available. Please set at least one of the following environment variables:")
        print("- OPENAI_API_KEY: for OpenAI models (GPT-3.5, GPT-4o)")
        print("- ANTHROPIC_API_KEY: for Claude models")
        print("- GOOGLE_API_KEY: for Google Gemini models")
        print("- XAI_API_KEY: for xAI Grok models")
        return
    
    # Test model recommendation
    print("\nTesting model recommendation:")
    test_prompt = "What is quantum computing?"
    provider, model, reason, _ = recommend_model(test_prompt)
    print(f"Prompt: \"{test_prompt}\"")
    print(f"Recommended model: {provider.capitalize()}'s {model}")
    print(f"Reason: {reason}")
    
    # Test task-specific recommendations
    print("\nTesting task-specific recommendations:")
    multi_prompt = "Design a marketing strategy and code a landing page"
    task_recs = get_task_recommendations(multi_prompt)
    
    print(f"Prompt: \"{multi_prompt}\"")
    if task_recs["task_recommendations"]:
        print("Detected tasks:")
        for task in task_recs["task_recommendations"]:
            print(f"- {task['task_description']}")
            if task["recommendations"]:
                top_rec = task["recommendations"][0]
                print(f"  Recommended model: {top_rec['provider'].capitalize()}'s {top_rec['model']}")
    
    print("\nInstallation test completed successfully!")

if __name__ == "__main__":
    main()