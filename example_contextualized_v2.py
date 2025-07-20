#!/usr/bin/env python3
"""
GPToggle v2.0 Contextualized Intelligence Example

This example demonstrates the new contextualized intelligence features
integrated directly into the GPToggle core system.
"""

from gptoggle_v2 import GPToggle, UserProfile
import json

def main():
    print("🚀 GPToggle v2.0 Contextualized Intelligence Demo")
    print("=" * 60)
    
    # Initialize GPToggle v2.0
    gptoggle = GPToggle()
    
    # Sample models for demonstration
    sample_models = [
        {
            "provider": "openai",
            "model_id": "gpt-4o",
            "display_name": "GPT-4o",
            "tiers": ["premium"],
            "capabilities": ["code", "reasoning", "vision"],
            "intelligence": 5,
            "speed": 4,
            "context_window": 128000,
            "pricing": {"input": 0.005, "output": 0.015}
        },
        {
            "provider": "anthropic", 
            "model_id": "claude-3-opus",
            "display_name": "Claude 3 Opus",
            "tiers": ["premium"],
            "capabilities": ["reasoning", "code", "creativity"],
            "intelligence": 5,
            "speed": 3,
            "context_window": 200000,
            "pricing": {"input": 0.015, "output": 0.075}
        },
        {
            "provider": "google",
            "model_id": "gemini-1.5-pro",
            "display_name": "Gemini 1.5 Pro",
            "tiers": ["standard"],
            "capabilities": ["reasoning", "math", "vision"],
            "intelligence": 4,
            "speed": 4,
            "context_window": 1000000,
            "pricing": {"input": 0.0035, "output": 0.0105}
        }
    ]
    
    # Register models
    gptoggle.register_models(sample_models)
    
    # Create different user profiles for demonstration
    profiles = {
        'developer': create_developer_profile(),
        'student': create_student_profile(),  
        'business': create_business_profile()
    }
    
    # Test queries
    test_queries = [
        "Write a Python function to sort a list",
        "Explain machine learning algorithms",
        "Create a marketing strategy for a new product",
        "How do I calculate compound interest?"
    ]
    
    # Demonstrate contextualized responses
    for query in test_queries:
        print(f"\n📝 Testing Query: \"{query}\"")
        print("-" * 50)
        
        for profile_type, profile in profiles.items():
            print(f"\n👤 Response for {profile_type}:")
            
            # Get contextualized recommendation
            recommendation = gptoggle.recommend_model(query)
            
            # Classify and enhance query
            classification = gptoggle.query_classifier.classify_query(query)
            enhancement = gptoggle.contextual_enhancer.enhance_query(
                query, classification['queryType'], profile
            )
            
            # Add interaction to profile
            profile.add_interaction(query, classification['queryType'])
            
            # Simulate response (would normally call actual API)
            response = simulate_ai_response(recommendation, enhancement)
            
            print(f"   Model: {recommendation['provider']}:{recommendation['model']}")
            print(f"   Type: {classification['queryType']}")
            print(f"   Enhancements: {', '.join(enhancement['enhancements'])}")
            print(f"   Response Preview: {response[:100]}...")
            
            # Show follow-up
            follow_up = gptoggle._generate_follow_up_suggestion(
                classification['queryType'], profile
            )
            print(f"   Follow-up: {follow_up}")
    
    # Show learning patterns
    print(f"\n🧠 Learning Patterns Analysis")
    print("-" * 50)
    
    for profile_type, profile in profiles.items():
        print(f"\n👤 {profile_type}:")
        analysis = analyze_profile_patterns(profile)
        for key, value in analysis.items():
            print(f"   {key}: {value}")
    
    print("\n✅ Demo completed! GPToggle v2.0 provides contextualized intelligence.")

def create_developer_profile() -> UserProfile:
    """Create a developer user profile"""
    profile = UserProfile.create_default("developer-alice")
    profile.communicationStyle['tone'] = 'casual'
    profile.communicationStyle['verbosity'] = 'detailed'
    profile.expertise['domains'] = ['technology', 'engineering']
    profile.expertise['skillLevel'] = {
        'javascript': 'expert',
        'python': 'advanced',
        'machine_learning': 'intermediate'
    }
    profile.expertise['interests'] = ['AI', 'web development', 'automation']
    return profile

def create_student_profile() -> UserProfile:
    """Create a student user profile"""
    profile = UserProfile.create_default("student-bob")
    profile.communicationStyle['tone'] = 'friendly'
    profile.communicationStyle['verbosity'] = 'moderate'
    profile.communicationStyle['includeExplanations'] = True
    profile.expertise['domains'] = ['education']
    profile.expertise['skillLevel'] = {
        'python': 'beginner',
        'math': 'intermediate'
    }
    profile.expertise['interests'] = ['learning', 'programming', 'science']
    return profile

def create_business_profile() -> UserProfile:
    """Create a business professional user profile"""
    profile = UserProfile.create_default("business-carol")
    profile.communicationStyle['tone'] = 'professional'
    profile.communicationStyle['verbosity'] = 'concise'
    profile.expertise['domains'] = ['business', 'finance']
    profile.expertise['skillLevel'] = {
        'business_strategy': 'expert',
        'marketing': 'advanced',
        'finance': 'expert'
    }
    profile.expertise['interests'] = ['strategy', 'growth', 'innovation']
    return profile

def simulate_ai_response(recommendation: dict, enhancement: dict) -> str:
    """Simulate an AI response based on recommendation and enhancement"""
    model_name = recommendation.get('model', 'unknown')
    enhancements = enhancement.get('enhancements', [])
    
    if 'GPT' in model_name:
        base = f"[Simulated Response from {model_name}]"
    elif 'claude' in model_name:
        base = f"[Simulated Response from Claude]"
    elif 'gemini' in model_name:
        base = f"[Simulated Response from Gemini]"
    else:
        base = f"[Simulated Response from {model_name}]"
    
    if enhancements:
        if 'detailed' in ' '.join(enhancements):
            return f"{base}\n\nThis is a comprehensive response to your query: \"{enhancement['original'][:50]}...\""
        elif 'concise' in ' '.join(enhancements):
            return f"{base}\n\nI've processed your request with consideration for your professional communication style."
        elif 'friendly' in ' '.join(enhancements):
            return f"{base}\n\nI've processed your request with consideration for your friendly communication style."
    
    return f"{base}\n\nThis is a standard response to your query."

def analyze_profile_patterns(profile: UserProfile) -> dict:
    """Analyze patterns in a user profile"""
    interactions = profile.context['recentInteractions']
    
    return {
        'Total Interactions': len(interactions),
        'Common Topics': ', '.join([f"{t['topic']} ({t['frequency']})" 
                                   for t in profile.context['learningPatterns']['commonTopics'][:3]]),
        'Communication Style': f"{profile.communicationStyle['tone']}, {profile.communicationStyle['verbosity']}",
        'Expertise': ', '.join(profile.expertise['domains'])
    }

if __name__ == "__main__":
    main()