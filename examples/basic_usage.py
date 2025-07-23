#!/usr/bin/env python3
"""
GPToggle Basic Usage Examples

Demonstrates fundamental GPToggle operations including:
- Simple queries and responses
- Multi-provider usage
- Basic module creation
- Configuration options
"""

import sys
import os

# Add core directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from gptoggle_v2 import GPToggle

def basic_query_example():
    """Demonstrate basic query functionality"""
    print("=== Basic Query Example ===")
    
    # Initialize GPToggle
    gpt = GPToggle()
    
    # Simple query
    response = gpt.query("Explain the concept of machine learning in simple terms")
    
    print(f"Response: {response['response'][:200]}...")
    print(f"Provider used: {response.get('provider', 'auto-selected')}")
    print(f"Modules created: {len(response.get('moduleActions', []))}")

def multi_provider_example():
    """Demonstrate multi-provider functionality"""
    print("\n=== Multi-Provider Example ===")
    
    gpt = GPToggle()
    
    # Specify different providers
    providers_to_test = ['openai', 'claude', 'gemini']
    
    for provider in providers_to_test:
        try:
            response = gpt.query("What are the benefits of renewable energy?", provider=provider)
            print(f"\n{provider.upper()}: {response['response'][:100]}...")
        except Exception as e:
            print(f"{provider.upper()}: Not available - {str(e)}")

def module_creation_example():
    """Demonstrate automatic module creation"""
    print("\n=== Module Creation Example ===")
    
    gpt = GPToggle()
    
    # Queries that should create modules
    test_queries = [
        "I need to buy milk, eggs, and bread for this week",
        "I'm planning a birthday party for March 15th with Alice and Bob", 
        "I'm interested in learning about quantum computing",
        "I want to track my daily exercise - goal is 30 minutes"
    ]
    
    for query in test_queries:
        response = gpt.query(query)
        
        print(f"\nQuery: '{query[:50]}...'")
        print(f"Modules created: {len(response.get('moduleActions', []))}")
        
        for action in response.get('moduleActions', []):
            if action['success']:
                print(f"  → Created {action['moduleType']} module")

def configuration_example():
    """Demonstrate configuration options"""
    print("\n=== Configuration Example ===")
    
    # Custom provider priority
    gpt = GPToggle(provider_priority=['claude', 'openai', 'gemini'])
    
    response = gpt.query("Tell me about artificial intelligence")
    print(f"Provider used: {response.get('provider', 'auto-selected')}")
    
    # Get available providers
    available = gpt.get_available_providers()
    print(f"Available providers: {available}")

def module_management_example():
    """Demonstrate module management"""
    print("\n=== Module Management Example ===")
    
    gpt = GPToggle()
    
    # Create some modules
    gpt.query("I need to buy apples, bananas, and oranges")
    gpt.query("Plan weekend trip to San Francisco")
    
    # Get user profile with modules
    user_profile = gpt.get_user_profile()
    
    # Get modules summary
    summary = user_profile.get_modules_summary()
    print(f"Total modules: {summary['totalModules']}")
    print(f"Active modules: {len(summary['activeModules'])}")
    
    # Show modules by type
    for module_type, count in summary['modulesByType'].items():
        if count > 0:
            print(f"  {module_type.title()}: {count}")

def provider_comparison_example():
    """Demonstrate cross-provider comparison"""
    print("\n=== Provider Comparison Example ===")
    
    gpt = GPToggle()
    
    try:
        # Compare responses across multiple providers
        comparison = gpt.compare_providers(
            "Explain the benefits of solar energy",
            providers=['openai', 'claude']
        )
        
        for provider, response in comparison.items():
            print(f"\n{provider.upper()}:")
            print(f"{response[:150]}...")
            
    except Exception as e:
        print(f"Comparison not available: {e}")

def error_handling_example():
    """Demonstrate error handling"""
    print("\n=== Error Handling Example ===")
    
    gpt = GPToggle()
    
    # Test with invalid provider
    try:
        response = gpt.query("Hello", provider="invalid-provider")
    except Exception as e:
        print(f"Expected error with invalid provider: {type(e).__name__}")
    
    # Test with empty query
    try:
        response = gpt.query("")
        print("Empty query handled gracefully")
    except Exception as e:
        print(f"Error with empty query: {type(e).__name__}")

def main():
    """Run all basic usage examples"""
    print("GPToggle Basic Usage Examples")
    print("=" * 50)
    
    try:
        basic_query_example()
        multi_provider_example()
        module_creation_example()
        configuration_example()
        module_management_example()
        provider_comparison_example()
        error_handling_example()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        print("\nNext steps:")
        print("- Check out advanced_features.js for JavaScript examples")
        print("- See module_demos.py for detailed module system examples")
        print("- Read docs/QUICK_START.md for more information")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("- At least one AI provider API key set (OPENAI_API_KEY, etc.)")
        print("- GPToggle properly installed or core files available")

if __name__ == "__main__":
    main()