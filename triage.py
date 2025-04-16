"""
This module contains the auto-triage logic to select the best model for a given prompt.
"""
import re
from typing import List, Dict, Any
import config

def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    return len(text.split())

def contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if the text contains any of the specified keywords."""
    text_lower = text.lower()
    for keyword in keywords:
        # Use word boundaries to match whole words
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
            return True
    return False

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in the text.
    A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
    """
    return len(text) // 4  # Simple character-based estimation

def choose_model(prompt: str) -> str:
    """
    Auto-triage function to select the appropriate model based on the prompt characteristics.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        The selected model name
    """
    # Check prompt length
    token_estimate = estimate_tokens(prompt)
    word_count = count_words(prompt)
    
    # Check for specialized content
    has_code_keywords = contains_keywords(prompt, config.CODE_KEYWORDS)
    has_creative_keywords = contains_keywords(prompt, config.CREATIVE_KEYWORDS)
    
    # Decision logic
    if token_estimate > 4000 or word_count > 1000:
        # For very long prompts, use models with longer context
        if has_code_keywords or has_creative_keywords:
            # If it's complex and code or creative related, use top model
            return "gpt-4o"
        else:
            # For long but general prompts
            return "gpt-3.5-turbo-16k"
    
    # For code-related tasks, prefer more capable models
    if has_code_keywords:
        return "gpt-4o"
    
    # For creative tasks, prefer more capable models
    if has_creative_keywords:
        return "gpt-4o"
    
    # Default to the balanced option
    return config.DEFAULT_MODEL
