#!/usr/bin/env python3
"""
GPToggle Enhanced - Standalone version with advanced recommendation capabilities

This standalone file provides enhanced GPToggle functionality without requiring
installation. It includes intelligent model selection with task-specific recommendations
and component-specific suggestions within responses.

Usage:
    # Download this file and use directly
    from gptoggle_enhanced import get_response, recommend_model, get_task_recommendations

    # Get a response using auto-selected model with embedded model suggestions
    response = get_response("Create a marketing plan and implement a landing page")
    
    # Get task-specific recommendations for a multi-faceted prompt
    recommendations = get_task_recommendations("Design a logo and code a website")
    print(f"Overall model: {recommendations['overall_recommendation']}")
    print(f"Task-specific recommendations: {recommendations['task_recommendations']}")
"""

import os
import re
import sys
import json
from typing import Dict, List, Optional, Tuple, Union, Any

# Version information
__version__ = "1.0.2"

#################################################
# Configuration
#################################################

# Provider priority for auto-selection (in descending order)
PROVIDER_PRIORITY = ["openai", "claude", "gemini", "llama", "perplexity", "grok"]

# Model mappings for each provider
MODELS = {
    "openai": {
        "default": "gpt-3.5-turbo",
        "advanced": "gpt-4o",
        "vision": "gpt-4o",
        "creative": "gpt-4o",
        "technical": "gpt-4o",
        "analytical": "gpt-4o"
    },
    "claude": {
        "default": "claude-3-sonnet-20240229",
        "advanced": "claude-3-opus-20240229",
        "vision": "claude-3-opus-20240229",
        "creative": "claude-3-opus-20240229",
        "technical": "claude-3-sonnet-20240229",
        "analytical": "claude-3-opus-20240229"
    },
    "gemini": {
        "default": "gemini-pro",
        "advanced": "gemini-1.5-pro",
        "vision": "gemini-pro-vision",
        "creative": "gemini-1.5-pro",
        "technical": "gemini-1.5-pro",
        "analytical": "gemini-1.5-pro"
    },
    "grok": {
        "default": "grok-beta",
        "advanced": "grok-2-1212",
        "vision": "grok-2-vision-1212",
        "creative": "grok-2-1212",
        "technical": "grok-2-1212",
        "analytical": "grok-2-1212"
    },
    "llama": {
        "default": "llama-3-8b-instruct",
        "advanced": "llama-3-70b-instruct",
        "vision": "llama-3-vision",
        "creative": "llama-3-70b-instruct",
        "technical": "llama-3-70b-instruct",
        "analytical": "llama-3-70b-instruct"
    },
    "perplexity": {
        "default": "llama-3.1-sonar-small-128k-online",
        "advanced": "llama-3.1-sonar-large-128k-online",
        "vision": "llama-3.1-sonar-small-128k-online",  # Limited vision capability
        "creative": "llama-3.1-sonar-large-128k-online",
        "technical": "llama-3.1-sonar-large-128k-online",
        "analytical": "llama-3.1-sonar-large-128k-online"
    }
}

# API key environment variables
API_KEY_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "grok": "XAI_API_KEY",
    "perplexity": "PERPLEXITY_API_KEY",
    "llama": "META_AI_API_KEY"  # Meta AI's hosted API key
}

# Default generation parameters
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 1000
}

# Provider strengths by task
PROVIDER_STRENGTHS = {
    "openai": {
        "marketing": "GPT models excel at market analysis, trend identification, and strategic planning.",
        "coding": "GPT-4o has strong coding capabilities across multiple languages and frameworks.",
        "data_analysis": "GPT models excel at interpreting and explaining data patterns and statistics.",
        "creative_writing": "GPT models generate highly coherent and creative content with good context awareness.",
        "general": "GPT models provide well-rounded capabilities for most general tasks."
    },
    "claude": {
        "marketing": "Claude excels at understanding brand voice, creative copywriting, and marketing strategy.",
        "coding": "Claude can explain complex code clearly and provide well-documented implementations.",
        "data_analysis": "Claude provides thorough and thoughtful data interpretations with nuanced analysis.",
        "creative_writing": "Claude generates nuanced and contextually appropriate creative content with strong narrative abilities.",
        "general": "Claude offers detailed, thoughtful responses with strong reasoning capabilities."
    },
    "gemini": {
        "marketing": "Gemini offers strong analytical capabilities for market research and data-driven marketing.",
        "coding": "Gemini has up-to-date knowledge of programming languages, frameworks, and best practices.",
        "data_analysis": "Gemini provides data-driven insights with strong analytical reasoning and pattern recognition.",
        "creative_writing": "Gemini generates diverse and contextually relevant creative content with good structure.",
        "general": "Gemini provides balanced responses with both technical accuracy and creativity."
    },
    "grok": {
        "marketing": "Grok provides concise, direct marketing advice with contemporary trend awareness.",
        "coding": "Grok excels at efficient code solutions with modern programming techniques.",
        "data_analysis": "Grok offers straightforward data insights with good technical precision.",
        "creative_writing": "Grok generates creative content with a distinct voice and contemporary references.",
        "general": "Grok delivers concise, practical responses with current information."
    },
    "llama": {
        "marketing": "Llama models provide balanced marketing advice with strong contextual understanding.",
        "coding": "Llama models offer robust code generation with clean implementations.",
        "data_analysis": "Llama models deliver clear explanations of data patterns with solid technical foundations.",
        "creative_writing": "Llama models generate coherent creative content with good narrative flow.",
        "general": "Llama models give well-balanced responses with strong reasoning and knowledge application."
    },
    "perplexity": {
        "marketing": "Perplexity (via Llama-Sonar) provides research-based marketing insights with current web information.",
        "coding": "Perplexity (via Llama-Sonar) offers up-to-date code solutions from modern references.",
        "data_analysis": "Perplexity (via Llama-Sonar) combines strong analytical skills with access to recent data sources.",
        "creative_writing": "Perplexity (via Llama-Sonar) generates creative content informed by diverse online references.",
        "general": "Perplexity (via Llama-Sonar) excels at retrieving and synthesizing current information from the web."
    }
}

# Task categories for detection
TASK_CATEGORIES = [
    {
        "name": "marketing",
        "description": "Marketing plan or strategy",
        "keywords": ["marketing plan", "campaign", "advertising", "brand", "market analysis", 
                     "audience", "promotion", "SEO", "social media", "content strategy", 
                     "marketing campaign"],
        "provider_ranking": ["claude", "openai", "gemini", "llama", "perplexity", "grok"],
        "likely_followups": [
            "audience_research", "competitive_analysis", "content_creation", 
            "social_media_strategy", "advertising_budget"
        ]
    },
    {
        "name": "coding",
        "description": "Code implementation or technical development",
        "keywords": ["code", "function", "algorithm", "programming", "debug", "software", 
                     "develop", "implementation", "script", "module", "library", "API", 
                     "database", "framework", "html", "css", "javascript", "landing page", "webpage"],
        "provider_ranking": ["openai", "gemini", "claude", "llama", "perplexity", "grok"],
        "likely_followups": [
            "debugging", "testing", "deployment", "optimization", 
            "security", "database_design", "api_integration"
        ]
    },
    {
        "name": "data_analysis",
        "description": "Data analysis or statistical interpretation",
        "keywords": ["analyze data", "statistics", "dataset", "correlation", "trends", 
                     "metrics", "dashboard", "visualization", "forecast", "insights", 
                     "patterns", "regression"],
        "provider_ranking": ["gemini", "openai", "claude", "llama", "perplexity", "grok"],
        "likely_followups": [
            "data_visualization", "predictive_modeling", "statistical_testing", 
            "report_generation", "insights_interpretation", "trend_analysis"
        ]
    },
    {
        "name": "creative_writing",
        "description": "Creative content or narrative",
        "keywords": ["story", "creative", "narrative", "write", "content", "article", 
                     "blog post", "fiction", "poem", "script", "essay", "copywriting"],
        "provider_ranking": ["claude", "openai", "gemini", "llama", "perplexity", "grok"],
        "likely_followups": [
            "content_editing", "story_continuation", "character_development", 
            "dialogue_creation", "narrative_structure", "style_refinement"
        ]
    },
    {
        "name": "business_strategy",
        "description": "Business strategy or planning",
        "keywords": ["business plan", "strategy", "startup", "venture", "business model",
                    "revenue", "profit", "market entry", "scaling", "growth", "ROI", 
                    "investment", "financial projection"],
        "provider_ranking": ["claude", "openai", "gemini", "llama", "perplexity", "grok"],
        "likely_followups": [
            "financial_modeling", "competitive_analysis", "market_sizing", 
            "funding_strategy", "operational_planning", "risk_assessment"
        ]
    },
    {
        "name": "product_development",
        "description": "Product design or development",
        "keywords": ["product design", "UX", "UI", "user experience", "product management",
                    "feature", "prototype", "MVP", "product roadmap", "user testing", "design"],
        "provider_ranking": ["openai", "claude", "gemini", "llama", "perplexity", "grok"],
        "likely_followups": [
            "user_research", "wireframing", "prototyping", "usability_testing", 
            "feature_prioritization", "design_system_creation"
        ]
    }
]

# Followup task categories
FOLLOWUP_CATEGORIES = {
    # Marketing followups
    "audience_research": {
        "description": "Market and audience research",
        "provider_ranking": ["claude", "openai", "gemini", "llama", "perplexity"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229", 
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "llama": "llama-3-70b-instruct",
            "perplexity": "llama-3.1-sonar-large-128k-online"
        }
    },
    "competitive_analysis": {
        "description": "Competitive analysis and positioning",
        "provider_ranking": ["openai", "claude", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229", 
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "content_creation": {
        "description": "Content creation and copywriting",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229", 
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "social_media_strategy": {
        "description": "Social media strategy and planning",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229", 
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "advertising_budget": {
        "description": "Advertising budget allocation",
        "provider_ranking": ["openai", "claude", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229", 
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    
    # Coding followups
    "debugging": {
        "description": "Code debugging and error fixing",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "testing": {
        "description": "Unit testing and test strategy",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "deployment": {
        "description": "Deployment and DevOps",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "optimization": {
        "description": "Code optimization and performance",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "security": {
        "description": "Security and vulnerability assessment",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "database_design": {
        "description": "Database design and optimization",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "api_integration": {
        "description": "API design and integration",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    
    # Data analysis followups
    "data_visualization": {
        "description": "Data visualization techniques",
        "provider_ranking": ["gemini", "openai", "claude"],
        "suggested_models": {
            "gemini": "gemini-1.5-pro",
            "openai": "gpt-4o",
            "claude": "claude-3-opus-20240229"
        }
    },
    "predictive_modeling": {
        "description": "Predictive modeling and forecasting",
        "provider_ranking": ["gemini", "openai", "claude"],
        "suggested_models": {
            "gemini": "gemini-1.5-pro",
            "openai": "gpt-4o",
            "claude": "claude-3-opus-20240229"
        }
    },
    "statistical_testing": {
        "description": "Statistical hypothesis testing",
        "provider_ranking": ["gemini", "openai", "claude"],
        "suggested_models": {
            "gemini": "gemini-1.5-pro",
            "openai": "gpt-4o",
            "claude": "claude-3-opus-20240229"
        }
    },
    "report_generation": {
        "description": "Data report generation",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    
    # Creative writing followups
    "content_editing": {
        "description": "Content editing and refinement",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "story_continuation": {
        "description": "Story continuation and development",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    
    # Business strategy followups
    "financial_modeling": {
        "description": "Financial modeling and projections",
        "provider_ranking": ["openai", "claude", "gemini"],
        "suggested_models": {
            "openai": "gpt-4o",
            "claude": "claude-3-opus-20240229",
            "gemini": "gemini-1.5-pro"
        }
    },
    "market_sizing": {
        "description": "Market sizing and opportunity assessment",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "funding_strategy": {
        "description": "Funding strategy and investor relations",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    
    # Product development followups
    "user_research": {
        "description": "User research and interviews",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    },
    "wireframing": {
        "description": "Wireframing and prototyping",
        "provider_ranking": ["openai", "gemini", "claude"],
        "suggested_models": {
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "claude": "claude-3-opus-20240229"
        }
    },
    "usability_testing": {
        "description": "Usability testing planning",
        "provider_ranking": ["claude", "openai", "gemini"],
        "suggested_models": {
            "claude": "claude-3-opus-20240229",
            "openai": "gpt-4o",
            "gemini": "gemini-1.5-pro"
        }
    }
}

#################################################
# Auto-Triage Functions
#################################################

def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    return len(text.split())

def contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if the text contains any of the specified keywords."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in the text.
    A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
    """
    return len(text) // 4

def identify_tasks(prompt: str) -> List[Dict[str, Any]]:
    """
    Identify distinct task types within a prompt.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        List of identified tasks with name, description, and provider ranking
    """
    detected_tasks = []
    
    # Check each task category
    for category in TASK_CATEGORIES:
        if contains_keywords(prompt, category["keywords"]):
            detected_tasks.append({
                "task_name": category["name"],
                "task_description": category["description"],
                "provider_ranking": category["provider_ranking"]
            })
    
    return detected_tasks

def recommend_model(prompt: str) -> Tuple[str, str, str, List[Dict[str, Any]]]:
    """
    Recommend the appropriate provider and model based on the prompt characteristics.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        A tuple of (provider_name, model_name, reason, detected_tasks)
    """
    # Get available providers
    available_providers = get_available_providers()
    
    if not available_providers:
        raise Exception("No API keys set for any supported providers")
    
    # Vision/image keywords
    vision_keywords = [
        "image", "picture", "photo", "diagram", "graph", "chart",
        "screenshot", "analyze this", "what's in this", "look at"
    ]
    
    # Code-related keywords
    code_keywords = [
        "code", "function", "algorithm", "programming", "python", "javascript",
        "java", "c++", "html", "css", "api", "database", "sql", "debug", 
        "error", "bug", "fix", "implement", "class", "object", "method"
    ]
    
    # Creative tasks
    creative_keywords = [
        "create", "generate", "write", "draft", "compose", "story", "poem",
        "creative", "fiction", "imagine", "design", "innovative", "novel", "unique"
    ]
    
    # Features to check
    token_count = estimate_tokens(prompt)
    word_count = count_words(prompt)
    
    # Check for specific requirements
    needs_vision = contains_keywords(prompt, vision_keywords)
    needs_coding = contains_keywords(prompt, code_keywords)
    needs_creativity = contains_keywords(prompt, creative_keywords)
    needs_advanced = token_count > 2000 or word_count > 500 or needs_coding
    
    # Determine reason
    if needs_vision:
        reason = "The prompt appears to involve image analysis or visual content"
    elif needs_advanced:
        reason = ("The prompt involves code or programming tasks" if needs_coding 
                 else "The prompt requires advanced reasoning or is complex/lengthy")
    elif needs_creativity:
        reason = "The prompt involves creative writing or content generation"
    else:
        reason = "The prompt is a standard request suitable for a baseline model"
    
    # Identify tasks for more specific recommendation
    detected_tasks = identify_tasks(prompt)
    if detected_tasks:
        reason += ". "
        if len(detected_tasks) == 1:
            reason += f"Task identified: {detected_tasks[0]['task_description']}"
        else:
            reason += f"Multiple tasks identified: {', '.join(t['task_description'] for t in detected_tasks)}"
    
    # Provider selection based on capabilities and priority
    for provider in PROVIDER_PRIORITY:
        if provider not in available_providers:
            continue
        
        # Select model based on requirements
        model_type = "vision" if needs_vision else ("advanced" if needs_advanced else "default")
        model = MODELS[provider][model_type]
        
        return provider, model, reason, detected_tasks
    
    # Fallback to first available provider
    provider = available_providers[0]
    return provider, MODELS[provider]["default"], "Selected as fallback based on available API keys", detected_tasks

def get_task_recommendations(prompt: str) -> Dict[str, Any]:
    """
    Generate comprehensive task-specific recommendations for a prompt.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        Dictionary with overall recommendation and task-specific recommendations
    """
    # Get the overall recommendation first
    provider, model, reason, detected_tasks = recommend_model(prompt)
    
    overall_recommendation = {
        "provider": provider,
        "model": model,
        "reason": reason
    }
    
    # Get specific recommendations for each detected task
    task_recommendations = []
    
    for task in detected_tasks:
        available_providers = get_available_providers()
        recommendations = []
        
        # Get recommendations for each provider
        for provider in available_providers:
            model_type = ""
            if task["task_name"] in ["marketing", "creative_writing"]:
                model_type = "creative"
            elif task["task_name"] == "coding":
                model_type = "technical"
            elif task["task_name"] == "data_analysis":
                model_type = "analytical"
            else:
                model_type = "default"
            
            model = MODELS[provider].get(model_type, MODELS[provider]["default"])
            strength = PROVIDER_STRENGTHS[provider].get(task["task_name"], 
                                                      PROVIDER_STRENGTHS[provider]["general"])
            
            recommendations.append({
                "provider": provider,
                "model": model,
                "strength": strength
            })
        
        # Sort by the task's provider ranking if available
        if "provider_ranking" in task:
            def get_ranking_index(rec):
                try:
                    return task["provider_ranking"].index(rec["provider"])
                except ValueError:
                    return len(task["provider_ranking"])  # Put at the end if not found
            
            recommendations.sort(key=get_ranking_index)
        
        task_recommendations.append({
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "recommendations": recommendations
        })
    
    return {
        "overall_recommendation": overall_recommendation,
        "task_recommendations": task_recommendations
    }

def get_followup_recommendations(detected_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate recommendations for likely follow-up tasks based on detected tasks.
    
    Args:
        detected_tasks: List of tasks detected in the prompt
        
    Returns:
        List of follow-up task recommendations
    """
    followup_recommendations = []
    available_providers = get_available_providers()
    
    # Get likely follow-ups for each detected task
    for task in detected_tasks:
        task_name = task.get("task_name", "")
        
        # Find the original task category to get likely follow-ups
        for category in TASK_CATEGORIES:
            if category["name"] == task_name:
                # Get the likely follow-up tasks for this category
                for followup_id in category.get("likely_followups", [])[:3]:  # Limit to top 3
                    # Skip if this followup is already in our recommendations
                    if any(f["followup_id"] == followup_id for f in followup_recommendations):
                        continue
                    
                    # Get the follow-up details
                    followup = FOLLOWUP_CATEGORIES.get(followup_id)
                    if not followup:
                        continue
                    
                    # Generate provider-specific recommendations
                    provider_recommendations = []
                    for provider in followup["provider_ranking"]:
                        if provider not in available_providers:
                            continue
                            
                        model = followup["suggested_models"].get(provider)
                        if not model:
                            continue
                            
                        provider_recommendations.append({
                            "provider": provider,
                            "model": model,
                            "strength": PROVIDER_STRENGTHS[provider].get(task_name, PROVIDER_STRENGTHS[provider]["general"])
                        })
                    
                    if provider_recommendations:
                        followup_recommendations.append({
                            "followup_id": followup_id,
                            "description": followup["description"],
                            "related_to": task_name,
                            "recommendations": provider_recommendations
                        })
                
                break
    
    return followup_recommendations

def generate_model_suggestions(prompt: str, selected_provider: str, selected_model: str) -> str:
    """
    Generate component-specific model suggestions to be included in a response.
    
    Args:
        prompt: User prompt
        selected_provider: The provider actually being used
        selected_model: The model actually being used
        
    Returns:
        Suggestions text to append to the response
    """
    task_recommendations = get_task_recommendations(prompt)
    
    # If no tasks were detected, return an empty string
    if not task_recommendations["task_recommendations"]:
        return ""
    
    suggestions = "\n\n---\n**GPToggle Model Recommendations:**\n\n"
    
    # Part 1: Current Task Recommendations
    if len(task_recommendations["task_recommendations"]) == 1:
        task = task_recommendations["task_recommendations"][0]
        suggestions += f"For this {task['task_description'].lower()} task:\n\n"
        
        # Add recommendations, highlighting the current model
        for i, rec in enumerate(task["recommendations"][:2]):  # Limit to top 2
            if rec["provider"] == selected_provider and rec["model"] == selected_model:
                suggestions += f"- **Current model: {rec['provider'].capitalize()}'s {rec['model']}**\n  {rec['strength']}\n\n"
            else:
                suggestions += f"- Alternative: {rec['provider'].capitalize()}'s {rec['model']}\n  {rec['strength']}\n\n"
    else:
        suggestions += "Your request contains multiple components that might benefit from different AI models:\n\n"
        
        for task in task_recommendations["task_recommendations"]:
            suggestions += f"**{task['task_description']}:**\n"
            # Get the top recommendation for this task
            if task["recommendations"]:
                top_rec = task["recommendations"][0]
                
                if top_rec["provider"] == selected_provider and top_rec["model"] == selected_model:
                    suggestions += f"- **Current model: {top_rec['provider'].capitalize()}'s {top_rec['model']}** is well-suited for this.\n  {top_rec['strength']}\n\n"
                else:
                    suggestions += f"- **Recommended: {top_rec['provider'].capitalize()}'s {top_rec['model']}** might provide better results.\n  {top_rec['strength']}\n\n"
        
        suggestions += "For optimal results, consider breaking your request into separate prompts targeted at the recommended models for each component.\n"
    
    # Part 2: Follow-up Task Recommendations
    followup_recommendations = get_followup_recommendations(task_recommendations["task_recommendations"])
    
    if followup_recommendations:
        suggestions += "\n**For potential follow-up tasks, consider these model recommendations:**\n\n"
        
        for followup in followup_recommendations[:3]:  # Limit to top 3 follow-ups
            suggestions += f"**{followup['description']}:** "
            
            # Get the top recommendation
            top_rec = followup["recommendations"][0]
            model_suggestion = f"{top_rec['provider'].capitalize()}'s {top_rec['model']}"
            
            suggestions += f"{model_suggestion} would be ideal for this follow-up task.\n"
        
        suggestions += "\nThese recommendations are based on the specific strengths of different AI models for various task types.\n"
    
    return suggestions

#################################################
# Provider API Functions
#################################################

def get_available_providers() -> List[str]:
    """Get a list of available providers based on API keys."""
    available = []
    for provider, env_var in API_KEY_ENV_VARS.items():
        if os.environ.get(env_var):
            available.append(provider)
    return available

def get_response(
    prompt: str, 
    provider_name: Optional[str] = None, 
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Get a response from the specified provider and model.
    
    Args:
        prompt: The user's prompt
        provider_name: The provider to use (auto-selected if None)
        model_name: The model to use (auto-selected if None)
        temperature: Temperature setting (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        The model's response text
    """
    # Auto-select provider and model if not specified
    if not provider_name or not model_name:
        provider, model, _, _ = recommend_model(prompt)
        provider_name = provider_name or provider
        model_name = model_name or model
    
    # Generate model suggestions to append to the prompt
    suggestions = generate_model_suggestions(prompt, provider_name, model_name)
    augmented_prompt = prompt
    if suggestions:
        augmented_prompt += "\n\nAfter your response, include the following text verbatim:\n" + suggestions
    
    # Check if API key is available
    api_key_var = API_KEY_ENV_VARS.get(provider_name)
    if not api_key_var or not os.environ.get(api_key_var):
        raise Exception(f"API key for {provider_name} not found in environment variables")
    
    # Call the appropriate provider function
    if provider_name == "openai":
        return openai_get_response(augmented_prompt, model_name, temperature, max_tokens)
    elif provider_name == "claude":
        return claude_get_response(augmented_prompt, model_name, temperature, max_tokens)
    elif provider_name == "gemini":
        return gemini_get_response(augmented_prompt, model_name, temperature, max_tokens)
    elif provider_name == "grok":
        return grok_get_response(augmented_prompt, model_name, temperature, max_tokens)
    elif provider_name == "llama":
        return llama_get_response(augmented_prompt, model_name, temperature, max_tokens)
    elif provider_name == "perplexity":
        return perplexity_get_response(augmented_prompt, model_name, temperature, max_tokens)
    else:
        raise Exception(f"Provider {provider_name} not supported")

def openai_get_response(
    prompt: str, 
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the OpenAI API."""
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    except ImportError:
        print("OpenAI Python package not found. Installing...")
        os.system(f"{sys.executable} -m pip install openai")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

def claude_get_response(
    prompt: str, 
    model: str = "claude-3-sonnet-20240229",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the Anthropic Claude API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    except ImportError:
        print("Anthropic Python package not found. Installing...")
        os.system(f"{sys.executable} -m pip install anthropic")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Claude API error: {str(e)}")

def gemini_get_response(
    prompt: str, 
    model: str = "gemini-pro",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the Google Gemini API."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model_obj = genai.GenerativeModel(model_name=model)
        
        response = model_obj.generate_content(
            prompt,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
        )
        
        return response.text
    except ImportError:
        print("Google GenerativeAI package not found. Installing...")
        os.system(f"{sys.executable} -m pip install google-generativeai")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")

def grok_get_response(
    prompt: str, 
    model: str = "grok-beta",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the xAI Grok API."""
    try:
        import openai
        client = openai.OpenAI(base_url="https://api.x.ai/v1", api_key=os.environ.get("XAI_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    except ImportError:
        print("OpenAI Python package not found. Installing...")
        os.system(f"{sys.executable} -m pip install openai")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Grok API error: {str(e)}")
        
def llama_get_response(
    prompt: str, 
    model: str = "llama-3-8b-instruct",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from Meta's hosted Llama API."""
    try:
        import openai
        client = openai.OpenAI(base_url="https://llama.meta.ai/v1", api_key=os.environ.get("META_AI_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    except ImportError:
        print("OpenAI Python package not found. Installing...")
        os.system(f"{sys.executable} -m pip install openai")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Meta Llama API error: {str(e)}")
        
def perplexity_get_response(
    prompt: str, 
    model: str = "llama-3.1-sonar-small-128k-online",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """Get a response from the Perplexity API."""
    try:
        import openai
        client = openai.OpenAI(base_url="https://api.perplexity.ai", api_key=os.environ.get("PERPLEXITY_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            search_domain_filter=["perplexity.ai"],
            search_recency_filter="month",
            frequency_penalty=1
        )
        
        return response.choices[0].message.content
    except ImportError:
        print("OpenAI Python package not found. Installing...")
        os.system(f"{sys.executable} -m pip install openai")
        print("Please run your code again.")
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Perplexity API error: {str(e)}")

#################################################
# CLI Interface
#################################################

if __name__ == "__main__":
    """Simple CLI interface when run directly."""
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        
        try:
            provider, model, reason, _ = recommend_model(prompt)
            print(f"Recommended model: {provider}:{model}")
            print(f"Reason: {reason}\n")
            
            # Check for task-specific recommendations
            task_recs = get_task_recommendations(prompt)
            if task_recs["task_recommendations"]:
                print("Task-specific recommendations:")
                for task in task_recs["task_recommendations"]:
                    print(f"- {task['task_description']}:")
                    for rec in task["recommendations"][:2]:  # Show top 2
                        print(f"  * {rec['provider'].capitalize()}'s {rec['model']}")
                print()
            
            print("Getting response...")
            response = get_response(prompt)
            print("\nResponse:")
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
            if "API key" in str(e):
                print("\nPlease set the required API key environment variables:")
                for provider, env_var in API_KEY_ENV_VARS.items():
                    print(f"- {env_var}: for {provider.capitalize()} access")
    else:
        print("GPToggle Enhanced - Intelligent AI Provider Selector")
        print("Usage: python gptoggle_enhanced.py \"Your prompt here\"")
        print("\nAvailable providers:")
        for provider in get_available_providers():
            print(f"- {provider.capitalize()}")