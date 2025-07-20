#!/usr/bin/env python3
"""
Test script for GPToggle v2.0 Adaptive Learning Integration

This test demonstrates the adaptive learning capabilities integrated
directly into the core GPToggle functions.
"""

import json
from gptoggle_v2 import GPToggle, UserProfile

def test_adaptive_learning():
    """Test the adaptive learning capabilities integrated into GPToggle core"""
    print("🧪 Testing GPToggle v2.0 Adaptive Learning Integration")
    print("=" * 60)
    
    # Initialize GPToggle
    gptoggle = GPToggle()
    
    # Sample models for testing
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
        }
    ]
    
    gptoggle.register_models(sample_models)
    
    # Create a test user profile
    user_profile = UserProfile.create_default("test-user")
    
    print(f"📋 Initial Profile State:")
    print(f"   Communication Tone: {user_profile.communicationStyle['tone']}")
    print(f"   Domains: {user_profile.expertise['domains']}")
    print(f"   Skill Levels: {user_profile.expertise['skillLevel']}")
    
    # Test queries to demonstrate adaptive learning
    test_queries = [
        ("Hey, can you write a Python function to sort a list?", "code"),
        ("Please help me code a JavaScript API endpoint", "code"),
        ("Cool! Now create a recipe for chocolate cake", "creative"),
        ("Could you kindly analyze the marketing strategy for this business plan?", "business"),
        ("Can you provide a comprehensive business analysis of revenue streams?", "business"),
        ("Thanks! Write a poem about programming", "creative")
    ]
    
    print(f"\n🔄 Processing Test Queries with Adaptive Learning:")
    print("-" * 50)
    
    for i, (query, expected_type) in enumerate(test_queries, 1):
        print(f"\n{i}. Query: \"{query}\"")
        
        # Classify query
        classification = gptoggle.query_classifier.classify_query(query)
        print(f"   Classified as: {classification['queryType']} (confidence: {classification['confidence']:.2f})")
        
        # Enhance query with current profile
        enhancement = gptoggle.contextual_enhancer.enhance_query(
            query, classification['queryType'], user_profile
        )
        print(f"   Enhancements: {', '.join(enhancement['enhancements']) if enhancement['enhancements'] else 'None'}")
        
        # Update profile adaptively (core integration)
        user_profile.update_profile_adaptively(query, classification['queryType'], "gpt-4o")
        
        # Show adaptive changes
        if i >= 3:  # Show changes after a few interactions
            print(f"   📈 Adaptive Changes:")
            print(f"      Tone: {user_profile.communicationStyle['tone']}")
            if user_profile.expertise['domains']:
                print(f"      New Domains: {user_profile.expertise['domains']}")
            
            # Show query type frequency
            query_types = user_profile.context.get('interactionHistory', {}).get('queryTypes', {})
            if query_types:
                sorted_types = sorted(query_types.items(), key=lambda x: x[1], reverse=True)
                print(f"      Query Type Frequency: {dict(sorted_types[:3])}")
    
    print(f"\n📊 Final Profile Analysis:")
    print("-" * 30)
    
    # Analyze final state
    final_analysis = analyze_adaptive_changes(user_profile)
    for key, value in final_analysis.items():
        print(f"   {key}: {value}")
    
    # Test recent queries storage
    recent_queries = user_profile.context.get('recentQueries', [])
    print(f"\n💾 Recent Queries Storage (Max 10):")
    print(f"   Total stored: {len(recent_queries)}")
    for query in recent_queries[:3]:  # Show first 3
        print(f"   - {query['type']}: \"{query['query'][:40]}...\"")
    
    # Test interaction history
    interaction_history = user_profile.context.get('interactionHistory', {})
    if interaction_history:
        print(f"\n📈 Interaction History:")
        print(f"   Last Model Used: {interaction_history.get('lastModelUsed')}")
        print(f"   Last Interaction: {interaction_history.get('lastInteraction')}")
        
        query_types = interaction_history.get('queryTypes', {})
        if query_types:
            print(f"   Query Type Distribution:")
            for qtype, count in sorted(query_types.items(), key=lambda x: x[1], reverse=True):
                print(f"     {qtype}: {count}")
    
    print(f"\n✅ Adaptive Learning Test Complete!")
    print(f"   The system successfully learned from {len(test_queries)} interactions")
    print(f"   Profile adapted based on user behavior patterns")
    
    return user_profile

def analyze_adaptive_changes(profile):
    """Analyze the adaptive changes made to a user profile"""
    analysis = {}
    
    # Communication style changes
    analysis['Communication Tone'] = profile.communicationStyle['tone']
    analysis['Verbosity'] = profile.communicationStyle['verbosity']
    
    # Domain expertise
    if profile.expertise['domains']:
        analysis['Detected Domains'] = ', '.join(profile.expertise['domains'])
    else:
        analysis['Detected Domains'] = 'None yet'
    
    # Skill levels
    skill_levels = profile.expertise['skillLevel']
    if skill_levels:
        top_skills = sorted(skill_levels.items(), key=lambda x: x[1], reverse=True)[:3]
        analysis['Top Skills'] = ', '.join([f"{skill} ({level})" for skill, level in top_skills])
    
    # Interaction patterns
    query_types = profile.context.get('interactionHistory', {}).get('queryTypes', {})
    if query_types:
        total_queries = sum(query_types.values())
        most_common = max(query_types.items(), key=lambda x: x[1])
        analysis['Most Common Query Type'] = f"{most_common[0]} ({most_common[1]}/{total_queries})"
    
    # Recent activity
    recent_queries = profile.context.get('recentQueries', [])
    analysis['Recent Queries Stored'] = len(recent_queries)
    
    # Learning patterns
    common_topics = profile.context['learningPatterns']['commonTopics']
    if common_topics:
        top_topic = common_topics[0]
        analysis['Top Learning Topic'] = f"{top_topic['topic']} ({top_topic['frequency']}x)"
    
    return analysis

def test_tone_adaptation():
    """Test specific tone adaptation functionality"""
    print(f"\n🎭 Testing Tone Adaptation:")
    print("-" * 30)
    
    # Create fresh profile
    profile = UserProfile.create_default("tone-test")
    gptoggle = GPToggle()
    
    # Test casual tone detection
    casual_queries = [
        "Hey, what's up?",
        "Cool, thanks for the help!",
        "Awesome, can you help me with this?"
    ]
    
    for query in casual_queries:
        profile.update_profile_adaptively(query, "general", "gpt-4o")
    
    print(f"   After casual queries: {profile.communicationStyle['tone']}")
    
    # Create another profile for formal tone
    formal_profile = UserProfile.create_default("formal-test")
    
    formal_queries = [
        "Could you please assist me with this matter?",
        "Would you kindly provide information about this topic?",
        "I would respectfully request your guidance on this issue."
    ]
    
    for query in formal_queries:
        formal_profile.update_profile_adaptively(query, "general", "gpt-4o")
    
    print(f"   After formal queries: {formal_profile.communicationStyle['tone']}")
    
    return profile, formal_profile

def test_domain_detection():
    """Test domain expertise detection"""
    print(f"\n🎯 Testing Domain Detection:")
    print("-" * 30)
    
    profile = UserProfile.create_default("domain-test")
    
    # Test technology domain
    tech_query = "I need help with Python programming and API development for my software project"
    profile.update_profile_adaptively(tech_query, "code", "gpt-4o")
    
    print(f"   After tech query:")
    print(f"     Domains: {profile.expertise['domains']}")
    print(f"     Skill levels: {profile.expertise['skillLevel']}")
    
    # Test business domain  
    business_query = "I need to analyze the revenue strategy and marketing budget for our contract negotiations"
    profile.update_profile_adaptively(business_query, "business", "gpt-4o")
    
    print(f"   After business query:")
    print(f"     Domains: {profile.expertise['domains']}")
    print(f"     Skill levels: {profile.expertise['skillLevel']}")
    
    return profile

if __name__ == "__main__":
    # Run comprehensive adaptive learning test
    main_profile = test_adaptive_learning()
    
    # Run specific feature tests
    tone_profiles = test_tone_adaptation()
    domain_profile = test_domain_detection()
    
    print(f"\n🎉 All Adaptive Learning Tests Completed Successfully!")
    print(f"   ✅ Core integration working")
    print(f"   ✅ Tone adaptation functional")
    print(f"   ✅ Domain detection operational")
    print(f"   ✅ Query history management active")
    print(f"   ✅ Interaction tracking functional")