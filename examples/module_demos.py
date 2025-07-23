#!/usr/bin/env python3
"""
GPToggle v2.0 Modular Adaptive Intelligence Demo

This example demonstrates the new modular adaptive intelligence features
integrated into the GPToggle core system. It shows how modules automatically
track and evolve based on user interactions.

Examples include:
- Shopping lists that automatically organize items
- Birthday party planners with tasks and guest lists
- Summer schedules for ongoing events
- Interest tracking for topics like Virginia Woolf
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'modules'))

from gptoggle_v2 import GPToggle, UserProfile
from moduleService import ModuleService

def demo_shopping_list_module():
    """Demonstrate shopping list module creation and management"""
    print("=" * 60)
    print("DEMO: Shopping List Module")
    print("=" * 60)
    
    # Create user profile
    user_profile = UserProfile.create_default("user-123")
    user_profile.expertise['domains'] = ['cooking', 'health']
    
    # Simulate user queries that create and update a shopping list module
    queries = [
        "I need to buy milk, eggs, and bread for this week",
        "Add toothpaste and shampoo to my shopping list",
        "Remove eggs from the shopping list",
        "Don't forget to get organic apples and bananas"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. User Query: '{query}'")
        
        # Update profile with module integration
        result = user_profile.update_profile_with_modules(query, 'general')
        
        print(f"   Module Actions: {len(result['moduleActions'])}")
        for action in result['moduleActions']:
            if action['success']:
                print(f"   ✓ {action['action'].title()} {action.get('moduleType', '')} module: {action.get('moduleKey', 'N/A')}")
            else:
                print(f"   ✗ Failed to {action['action']} module")
    
    # Show final modules summary
    summary = user_profile.get_modules_summary()
    print(f"\n📊 Modules Summary:")
    print(f"   Total Active Modules: {summary['totalModules']}")
    print(f"   List Modules: {summary['modulesByType']['list']}")
    
    # Show the actual shopping list data
    shopping_lists = [k for k, v in user_profile.context['modules'].items() if v['type'] == 'list']
    if shopping_lists:
        list_key = shopping_lists[0]
        shopping_data = user_profile.context['modules'][list_key]['data']
        print(f"   Current Shopping List: {shopping_data}")
    
    return user_profile

def demo_birthday_party_planner():
    """Demonstrate birthday party planner module"""
    print("\n" + "=" * 60)
    print("DEMO: Birthday Party Planner Module")
    print("=" * 60)
    
    # Create user profile
    user_profile = UserProfile.create_default("user-456")
    
    # Simulate party planning queries
    queries = [
        "I'm planning a birthday party for September 14th with guests Alice and Ben",
        "Add tasks: book the cake and send invitations",
        "Invite Charlie to the birthday party too",
        "Need to organize decorations and buy party supplies"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. User Query: '{query}'")
        
        result = user_profile.update_profile_with_modules(query, 'business')
        
        for action in result['moduleActions']:
            if action['success']:
                print(f"   ✓ {action['action'].title()} {action.get('moduleType', '')} module: {action.get('moduleKey', 'N/A')}")
    
    # Show party planning details
    planners = [k for k, v in user_profile.context['modules'].items() if v['type'] == 'planner']
    if planners:
        planner_key = planners[0]
        planner_data = user_profile.context['modules'][planner_key]['data']
        print(f"\n🎉 Party Planning Details:")
        print(f"   Date: {planner_data.get('date', 'TBD')}")
        print(f"   Guests: {planner_data.get('guests', [])}")
        print(f"   Tasks: {planner_data.get('tasks', [])}")
        print(f"   Status: {planner_data.get('status', 'planning')}")
    
    return user_profile

def demo_interest_tracking():
    """Demonstrate interest tracking for Virginia Woolf"""
    print("\n" + "=" * 60)
    print("DEMO: Interest Tracking Module (Virginia Woolf)")
    print("=" * 60)
    
    # Create user profile
    user_profile = UserProfile.create_default("user-789")
    user_profile.expertise['domains'] = ['literature', 'education']
    
    # Simulate queries about Virginia Woolf
    queries = [
        "I'm fascinated by Virginia Woolf and her stream of consciousness writing technique",
        "Tell me about the Bloomsbury Group and Virginia Woolf's involvement",
        "I'm interested in learning more about modernist literature",
        "What are Virginia Woolf's most influential works?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. User Query: '{query}'")
        
        result = user_profile.update_profile_with_modules(query, 'educational')
        
        for action in result['moduleActions']:
            if action['success']:
                print(f"   ✓ {action['action'].title()} {action.get('moduleType', '')} module")
    
    # Show interest details
    interests = [k for k, v in user_profile.context['modules'].items() if v['type'] == 'interest']
    if interests:
        interest_key = interests[0]
        interest_data = user_profile.context['modules'][interest_key]['data']
        print(f"\n📚 Interest Tracking:")
        print(f"   Keywords: {interest_data.get('keywords', [])}")
        print(f"   Engagement Level: {interest_data.get('engagementLevel', 5)}/10")
        print(f"   Related Topics: {interest_data.get('relatedTopics', [])}")
    
    return user_profile

def demo_summer_schedule():
    """Demonstrate summer schedule calendar module"""
    print("\n" + "=" * 60)
    print("DEMO: Summer Schedule Calendar Module")
    print("=" * 60)
    
    # Create user profile
    user_profile = UserProfile.create_default("user-101")
    
    # Simulate schedule-related queries
    queries = [
        "I have soccer camp scheduled for July 5th",
        "Add swim lessons on July 10th to my calendar",
        "Schedule tennis practice for July 15th",
        "My summer schedule is getting busy!"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. User Query: '{query}'")
        
        result = user_profile.update_profile_with_modules(query, 'general')
        
        for action in result['moduleActions']:
            if action['success']:
                print(f"   ✓ {action['action'].title()} {action.get('moduleType', '')} module")
    
    # Show calendar details
    calendars = [k for k, v in user_profile.context['modules'].items() if v['type'] == 'calendar']
    if calendars:
        calendar_key = calendars[0]
        calendar_data = user_profile.context['modules'][calendar_key]['data']
        print(f"\n📅 Summer Schedule:")
        for date, event in calendar_data.items():
            print(f"   {date}: {event}")
    
    return user_profile

def demo_module_lifecycle():
    """Demonstrate module aging and cleanup"""
    print("\n" + "=" * 60)
    print("DEMO: Module Lifecycle and Cleanup")
    print("=" * 60)
    
    user_profile = UserProfile.create_default("user-lifecycle")
    module_service = ModuleService()
    
    # Create some modules
    profile_dict = user_profile.__dict__
    
    # Create an old module (simulate by setting old timestamp)
    old_module = {
        'type': 'list',
        'data': ['old item 1', 'old item 2'],
        'metadata': {
            'createdAt': '2024-01-01T00:00:00',
            'lastUpdated': '2024-01-01T00:00:00',
            'lastAccessed': '2024-01-01T00:00:00',
            'priority': 3,
            'archived': False
        }
    }
    
    # Create a recent module
    recent_module = {
        'type': 'planner',
        'data': {'date': '2025-08-01', 'guests': ['Alice'], 'tasks': ['Plan party']},
        'metadata': {
            'createdAt': datetime.now().isoformat(),
            'lastUpdated': datetime.now().isoformat(),
            'lastAccessed': datetime.now().isoformat(),
            'priority': 8,
            'archived': False
        }
    }
    
    # Add modules to profile
    user_profile.context['modules'] = {
        'oldShoppingList': old_module,
        'recentPartyPlanner': recent_module
    }
    
    print("Before cleanup:")
    summary = user_profile.get_modules_summary()
    print(f"   Total Modules: {summary['totalModules']}")
    print(f"   Active Modules: {len(summary['activeModules'])}")
    
    # Run cleanup
    cleanup_result = module_service.cleanup_stale_modules(profile_dict)
    user_profile.context = profile_dict['context']
    
    print(f"\nCleanup Results:")
    print(f"   Archived: {cleanup_result['archived']}")
    print(f"   Removed: {cleanup_result['removed']}")
    
    print("\nAfter cleanup:")
    summary = user_profile.get_modules_summary()
    print(f"   Total Modules: {summary['totalModules']}")
    print(f"   Active Modules: {len(summary['activeModules'])}")
    
    return user_profile

def demo_module_integration():
    """Demonstrate complete module integration workflow"""
    print("\n" + "=" * 60)
    print("DEMO: Complete Module Integration Workflow")
    print("=" * 60)
    
    user_profile = UserProfile.create_default("user-complete")
    
    # Complex queries that should trigger multiple module types
    complex_queries = [
        "I need to plan my mom's birthday party on March 15th, invite Sarah and Tom, and buy decorations, cake, and balloons",
        "Add grocery shopping to my schedule for this weekend: milk, bread, eggs, and party supplies",
        "I'm really interested in learning about sustainable cooking and zero-waste lifestyle",
        "Update my birthday party: also invite Mike and add task to book restaurant"
    ]
    
    for i, query in enumerate(complex_queries, 1):
        print(f"\n{i}. Complex Query: '{query}'")
        
        result = user_profile.update_profile_with_modules(query, 'business')
        
        print(f"   Actions Taken: {len(result['moduleActions'])}")
        for action in result['moduleActions']:
            if action['success']:
                action_type = action['action']
                module_type = action.get('moduleType', 'unknown')
                module_key = action.get('moduleKey', 'N/A')
                print(f"   ✓ {action_type.title()} {module_type} module: {module_key}")
        
        print(f"   Relevant Modules: {result['relevantModules']}")
    
    # Final comprehensive summary
    print(f"\n📋 Final Comprehensive Summary:")
    summary = user_profile.get_modules_summary()
    print(f"   Total Active Modules: {summary['totalModules']}")
    
    for module_type, count in summary['modulesByType'].items():
        if count > 0:
            print(f"   {module_type.title()} Modules: {count}")
    
    print(f"\n🎯 Most Active Modules:")
    for module in summary['activeModules'][:3]:
        print(f"   {module['key']} ({module['type']}) - Priority: {module['priority']}")
    
    print(f"\n🔄 Recently Updated:")
    for module in summary['recentlyUpdated']:
        print(f"   {module['key']} ({module['type']}) - {module['lastUpdated'][:10]}")
    
    return user_profile

def main():
    """Run all module demonstrations"""
    print("GPToggle v2.0 - Modular Adaptive Intelligence Demo")
    print("This demo shows how modules automatically track user interests and needs.")
    
    # Run all demos
    profile1 = demo_shopping_list_module()
    profile2 = demo_birthday_party_planner()
    profile3 = demo_interest_tracking()
    profile4 = demo_summer_schedule()
    profile5 = demo_module_lifecycle()
    profile6 = demo_module_integration()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE: Modular Adaptive Intelligence")
    print("=" * 60)
    print("✅ Successfully demonstrated:")
    print("   • Shopping list module creation and updates")
    print("   • Birthday party planning with tasks and guests")
    print("   • Interest tracking for educational topics")
    print("   • Calendar scheduling for summer activities")
    print("   • Module lifecycle and automatic cleanup")
    print("   • Complex query handling with multiple modules")
    print("\n📚 The modular system now provides:")
    print("   • Automatic module type detection")
    print("   • Context-aware data extraction")
    print("   • Intelligent module updates")
    print("   • Lifecycle management with aging")
    print("   • Cross-module relationships")
    print("\n🚀 Ready for integration into GPToggle.com and other platforms!")

if __name__ == "__main__":
    main()