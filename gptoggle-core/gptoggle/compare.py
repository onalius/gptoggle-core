"""
This module handles the comparison of responses from different models
and manages the user rating system.
"""
import json
import os
import datetime
from typing import Dict, List, Any, Tuple
from openai import OpenAI

from . import config

def get_responses(prompt: str, models: List[str]) -> Dict[str, str]:
    """
    Get responses from multiple models for the same prompt.
    
    Args:
        prompt: The user's prompt
        models: List of model names to get responses from
        
    Returns:
        Dictionary mapping model names to their responses
    """
    client = OpenAI(api_key=config.openai_config.api_key)
    responses = {}
    
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.openai_config.temperature,
                max_tokens=config.openai_config.max_comparison_tokens,
            )
            responses[model] = response.choices[0].message.content
        except Exception as e:
            responses[model] = f"Error getting response from {model}: {str(e)}"
    
    return responses

def display_comparison(responses: Dict[str, str]) -> None:
    """
    Display the responses from different models side by side.
    
    Args:
        responses: Dictionary mapping model names to their responses
    """
    for i, (model, response) in enumerate(responses.items(), 1):
        print(f"\n--- Response {i} (Model: {model}) ---")
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

def save_rating(prompt: str, models: List[str], responses: Dict[str, str], preferred: int) -> None:
    """
    Save the user's rating to a JSON file.
    
    Args:
        prompt: The original prompt
        models: List of models used
        responses: Dictionary mapping model names to their responses
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
    
    # Map the user's preference to the actual model
    preferred_model = models[preferred - 1]
    non_preferred_model = models[1 - (preferred - 1)]
    
    # Create a new rating entry
    rating_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "prompt": prompt,
        "models_compared": models,
        "preferred_model": preferred_model,
        "non_preferred_model": non_preferred_model,
        "responses": responses
    }
    
    # Add the new rating to the list
    ratings.append(rating_entry)
    
    # Save the updated ratings
    with open(config.RATINGS_FILE, 'w') as f:
        json.dump(ratings, f, indent=2)
    
    print(f"Rating saved to {config.RATINGS_FILE}")

def compare_models(prompt: str, models: List[str]) -> None:
    """
    Compare responses from different models and save user ratings.
    
    Args:
        prompt: The user's prompt
        models: List of model names to compare
    """
    print(f"Comparing responses from models: {', '.join(models)}")
    responses = get_responses(prompt, models)
    display_comparison(responses)
    preferred = get_user_rating()
    save_rating(prompt, models, responses, preferred)
    print(f"You preferred the response from {models[preferred - 1]}")