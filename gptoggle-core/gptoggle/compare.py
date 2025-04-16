"""
This module handles the comparison of responses from different models and providers,
and manages the user rating system.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

from gptoggle.config import config
from gptoggle.chat import get_response

# File path for storing user ratings
RATINGS_FILE = os.path.expanduser("~/.gptoggle/ratings.json")

def get_responses(prompt: str, model_pairs: List[Tuple[str, str]]) -> Dict[str, str]:
    """
    Get responses from multiple models for the same prompt.
    
    Args:
        prompt: The user's prompt
        model_pairs: List of (provider_name, model_name) tuples
        
    Returns:
        Dictionary mapping provider:model to their responses
    """
    responses = {}
    
    for provider_name, model_name in model_pairs:
        # Get provider-specific configuration
        provider_config = config.get_provider_config(provider_name)
        
        # Use shorter token limit for comparisons
        max_tokens = provider_config.max_comparison_tokens
        
        # Generate response
        response = get_response(
            prompt=prompt,
            provider_name=provider_name,
            model=model_name,
            max_tokens=max_tokens
        )
        
        # Store response
        model_key = f"{provider_name}:{model_name}"
        responses[model_key] = response
    
    return responses

def display_comparison(responses: Dict[str, str]) -> None:
    """
    Display the responses from different models side by side.
    
    Args:
        responses: Dictionary mapping provider:model to their responses
    """
    # Get models in a consistent order
    models = sorted(responses.keys())
    
    # Check if we have exactly 2 models (most common case)
    if len(models) == 2:
        # Print header
        print("\n" + "=" * 80)
        print(f"MODEL COMPARISON: {models[0]} vs {models[1]}")
        print("=" * 80 + "\n")
        
        # Print responses side by side
        print(f"[1] {models[0]}:")
        print("-" * 80)
        print(responses[models[0]])
        print("\n" + "-" * 80 + "\n")
        
        print(f"[2] {models[1]}:")
        print("-" * 80)
        print(responses[models[1]])
        print("\n" + "-" * 80)
    else:
        # Print each response sequentially for 3+ models
        print("\nMODEL COMPARISON:")
        print("=" * 80 + "\n")
        
        for i, model in enumerate(models, 1):
            print(f"[{i}] {model}:")
            print("-" * 80)
            print(responses[model])
            print("\n" + "-" * 80 + "\n")

def get_user_rating() -> int:
    """
    Prompt the user to rate which response was better.
    
    Returns:
        The user's rating (1 or 2)
    """
    while True:
        rating = input("Which response was better? Enter 1 or 2 (or 0 to skip rating): ")
        if rating in ["0", "1", "2"]:
            return int(rating)
        print("Invalid input. Please enter 1, 2, or 0 to skip.")

def save_rating(prompt: str, model_pairs: List[Tuple[str, str]], responses: Dict[str, str], preferred: int) -> None:
    """
    Save the user's rating to a JSON file.
    
    Args:
        prompt: The original prompt
        model_pairs: List of (provider_name, model_name) tuples
        responses: Dictionary mapping provider:model to their responses
        preferred: The user's preferred response (1 or 2)
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(RATINGS_FILE), exist_ok=True)
    
    # Load existing ratings if file exists
    ratings_data = []
    if os.path.exists(RATINGS_FILE):
        try:
            with open(RATINGS_FILE, "r") as f:
                ratings_data = json.load(f)
        except json.JSONDecodeError:
            # Handle case where file exists but isn't valid JSON
            ratings_data = []
    
    # Create new rating entry
    models = sorted([f"{p}:{m}" for p, m in model_pairs])
    rating_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "models": models,
        "responses": responses,
        "preferred_index": preferred - 1 if preferred > 0 else None,
        "preferred_model": models[preferred - 1] if preferred > 0 else None
    }
    
    # Add to ratings data
    ratings_data.append(rating_entry)
    
    # Save to file
    with open(RATINGS_FILE, "w") as f:
        json.dump(ratings_data, f, indent=2)
    
    # Print confirmation
    if preferred > 0:
        print(f"Rating saved: {models[preferred - 1]} preferred for this prompt.")
    else:
        print("Rating skipped.")

def compare_models(prompt: str, model_pairs: List[Tuple[str, str]]) -> None:
    """
    Compare responses from different models and save user ratings.
    
    Args:
        prompt: The user's prompt
        model_pairs: List of (provider_name, model_name) tuples
    """
    # Validate input
    if len(model_pairs) < 2:
        print("Error: At least two models are required for comparison.")
        return
    
    # Get responses from all models
    print("Generating responses from all models...")
    responses = get_responses(prompt, model_pairs)
    
    # Display side-by-side comparison
    display_comparison(responses)
    
    # Get user rating
    user_rating = get_user_rating()
    
    # Save the rating
    if user_rating > 0:
        save_rating(prompt, model_pairs, responses, user_rating)
    else:
        print("Rating skipped.")