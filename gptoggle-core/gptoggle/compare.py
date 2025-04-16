"""
This module handles the comparison of responses from different models and providers,
and manages the user rating system.
"""
import json
import os
import datetime
from typing import Dict, List, Any, Tuple

from . import config
from .providers import PROVIDERS

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
        # Get provider instance
        provider_class = PROVIDERS[provider_name]
        provider = provider_class()
        
        # Get provider-specific config
        provider_config = config.config.get_provider_config(provider_name)
        
        try:
            # Validate API key
            if not provider.validate_api_key():
                responses[f"{provider_name}:{model_name}"] = f"Error: API key not set for provider '{provider_name}'"
                continue
                
            # Get response
            response = provider.get_response(
                prompt=prompt, 
                model=model_name,
                temperature=provider_config.temperature,
                max_tokens=provider_config.max_comparison_tokens
            )
            responses[f"{provider_name}:{model_name}"] = response
        except Exception as e:
            responses[f"{provider_name}:{model_name}"] = f"Error: {str(e)}"
    
    return responses

def display_comparison(responses: Dict[str, str]) -> None:
    """
    Display the responses from different models side by side.
    
    Args:
        responses: Dictionary mapping provider:model to their responses
    """
    for i, (model_key, response) in enumerate(responses.items(), 1):
        print(f"\n--- Response {i} (Model: {model_key}) ---")
        print(response)
        print("-" * 80)

def get_user_rating() -> int:
    """
    Prompt the user to rate which response was better.
    
    Returns:
        The user's rating (1 or 2)
    """
    while True:
        try:
            rating = int(input("\nWhich response was better? (1 or 2): "))
            if rating in [1, 2]:
                return rating
            print("Please enter either 1 or 2.")
        except ValueError:
            print("Please enter a valid number (1 or 2).")

def save_rating(prompt: str, model_pairs: List[Tuple[str, str]], responses: Dict[str, str], preferred: int) -> None:
    """
    Save the user's rating to a JSON file.
    
    Args:
        prompt: The original prompt
        model_pairs: List of (provider_name, model_name) tuples
        responses: Dictionary mapping provider:model to their responses
        preferred: The user's preferred response (1 or 2)
    """
    # Create the ratings file if it doesn't exist
    if not os.path.exists(config.RATINGS_FILE):
        with open(config.RATINGS_FILE, 'w') as f:
            json.dump([], f)
    
    # Load existing ratings
    try:
        with open(config.RATINGS_FILE, 'r') as f:
            ratings = json.load(f)
    except json.JSONDecodeError:
        # If the file is empty or malformed, start with an empty list
        ratings = []
    
    # Map the user's preference to the actual model pairs
    preferred_model_pair = model_pairs[preferred - 1]
    non_preferred_model_pair = model_pairs[1 - (preferred - 1)]
    
    # Format for logging
    preferred_key = f"{preferred_model_pair[0]}:{preferred_model_pair[1]}"
    non_preferred_key = f"{non_preferred_model_pair[0]}:{non_preferred_model_pair[1]}"
    
    # Create a new rating entry
    rating_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "prompt": prompt,
        "models_compared": [
            {
                "provider": model_pairs[0][0],
                "model": model_pairs[0][1]
            },
            {
                "provider": model_pairs[1][0],
                "model": model_pairs[1][1]
            }
        ],
        "preferred": {
            "provider": preferred_model_pair[0],
            "model": preferred_model_pair[1]
        },
        "non_preferred": {
            "provider": non_preferred_model_pair[0],
            "model": non_preferred_model_pair[1]
        },
        "responses": responses
    }
    
    # Add the new rating to the list
    ratings.append(rating_entry)
    
    # Save the updated ratings
    with open(config.RATINGS_FILE, 'w') as f:
        json.dump(ratings, f, indent=2)
    
    print(f"Rating saved to {config.RATINGS_FILE}")

def compare_models(prompt: str, model_pairs: List[Tuple[str, str]]) -> None:
    """
    Compare responses from different models and save user ratings.
    
    Args:
        prompt: The user's prompt
        model_pairs: List of (provider_name, model_name) tuples
    """
    # Format for display
    model_display = [f"{provider}:{model}" for provider, model in model_pairs]
    print(f"Comparing responses from: {', '.join(model_display)}")
    
    # Get responses
    responses = get_responses(prompt, model_pairs)
    
    # Display comparison
    display_comparison(responses)
    
    # Get user rating
    preferred = get_user_rating()
    
    # Save rating
    save_rating(prompt, model_pairs, responses, preferred)
    
    # Show confirmation
    preferred_provider, preferred_model = model_pairs[preferred - 1]
    print(f"You preferred the response from {preferred_provider}:{preferred_model}")