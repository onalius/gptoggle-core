#!/usr/bin/env python3
"""
A CLI wrapper for the OpenAI API with auto-model selection and comparison capabilities.

Usage:
    python chat.py "Your question here"
    python chat.py "Your question here" --model gpt-4o
    python chat.py "Your question here" --compare gpt-4o,gpt-3.5-turbo
"""

import argparse
import sys
import os
from typing import List, Optional
from openai import OpenAI

import config
import triage
import compare

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CLI wrapper for OpenAI ChatGPT API with auto-model selection"
    )
    parser.add_argument(
        "prompt", 
        type=str, 
        help="The prompt or question to send to the API"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        help="Override the auto-selected model (e.g., gpt-4o, gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--compare", 
        type=str, 
        help="Compare responses from two models (comma-separated, e.g., gpt-4o,gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--list-models", 
        action="store_true", 
        help="List all available models"
    )
    
    return parser.parse_args()

def validate_model(model: str) -> bool:
    """Check if the specified model is valid."""
    return model in config.AVAILABLE_MODELS

def validate_api_key() -> bool:
    """Validate that the OpenAI API key is set."""
    if not config.openai_config.api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key with:")
        print("export OPENAI_API_KEY='your-api-key'")
        return False
    return True

def get_response(prompt: str, model: str) -> str:
    """
    Get a response from the specified model.
    
    Args:
        prompt: The user's prompt
        model: The model to use
        
    Returns:
        The model's response
    """
    client = OpenAI(api_key=config.openai_config.api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.openai_config.temperature,
            max_tokens=config.openai_config.max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def list_available_models():
    """Display all available models."""
    print("Available models:")
    for model in config.AVAILABLE_MODELS:
        capabilities = config.MODEL_CAPABILITIES.get(model, {})
        tier = capabilities.get("tier", "unknown")
        max_tokens = capabilities.get("max_tokens", "unknown")
        print(f"- {model} (Tier: {tier}, Max tokens: {max_tokens})")

def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Check for list-models flag
    if args.list_models:
        list_available_models()
        return
    
    # Validate API key
    if not validate_api_key():
        return
    
    # Get the prompt
    prompt = args.prompt
    
    # Compare mode
    if args.compare:
        models = args.compare.split(',')
        
        # Validate models
        for model in models:
            if not validate_model(model):
                print(f"Error: Invalid model '{model}'. Use --list-models to see available models.")
                return
        
        # Ensure exactly two models for comparison
        if len(models) != 2:
            print("Error: --compare requires exactly two models separated by a comma")
            return
        
        # Run comparison
        compare.compare_models(prompt, models)
        return
    
    # Single model mode
    if args.model:
        model = args.model
        reason = "Manually selected by user"
    else:
        model, reason = triage.choose_model(prompt)
    
    # Validate model
    if not validate_model(model):
        print(f"Error: Invalid model '{model}'. Use --list-models to see available models.")
        return
    
    # Get the auto-triaged model if none is specified
    if not args.model:
        print(f"Auto-selected model: {model}")
        print(f"Reason: {reason}")
    
    # Get response
    print(f"Getting response from {model}...")
    response = get_response(prompt, model)
    
    # Print response
    print("\n----- Response -----")
    print(response)
    print("--------------------")

if __name__ == "__main__":
    main()
