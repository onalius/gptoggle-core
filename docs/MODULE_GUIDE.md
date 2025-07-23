# Modular Adaptive Intelligence Guide

This comprehensive guide covers GPToggle's revolutionary Modular Adaptive Intelligence system - how it works, how to use it, and how to extend it for your applications.

## 🧠 Understanding Adaptive Modules

Adaptive modules are specialized knowledge containers that automatically emerge from user interactions. Unlike traditional static data structures, these modules:

- **Self-Create**: Automatically generate when patterns are detected
- **Evolve**: Adapt and grow based on continued usage
- **Cross-Reference**: Build relationships with other modules
- **Age Gracefully**: Archive and cleanup based on usage patterns

## 📊 Module Types Deep Dive

### 1. List Modules (`list`)

**Purpose**: Track collections of items, tasks, or inventory

**Auto-Created From**:
- "I need to buy milk, eggs, and bread"
- "Add to my shopping list"
- "My todo items are..."
- "Keep track of these books..."

**Data Structure**:
```python
{
  "type": "list",
  "data": ["item1", "item2", "item3"],
  "metadata": {
    "priority": 7,
    "tags": ["shopping", "groceries"],
    "contextKeywords": ["buy", "shopping", "groceries"]
  }
}
```

**Operations**:
- **Add**: "Also add cheese to my shopping list"
- **Remove**: "Remove eggs from the list" 
- **View**: "What's on my shopping list?"
- **Clear**: "Clear my shopping list"

**Example Usage**:
```python
# Creates shopping list module
response = gpt.query("I need to buy milk, eggs, bread, and bananas")

# Updates existing list
response = gpt.query("Add cheese and yogurt to my shopping list")

# Removes items
response = gpt.query("Remove eggs and bananas from my list")
```

### 2. Planner Modules (`planner`)

**Purpose**: Organize events, projects, and complex planning tasks

**Auto-Created From**:
- "I'm planning a birthday party for March 15th"
- "Organize a team meeting with Alice and Bob"
- "Plan my vacation to Japan"
- "Coordinate the product launch"

**Data Structure**:
```python
{
  "type": "planner",
  "data": {
    "title": "Birthday Party",
    "date": "March 15, 2025",
    "guests": ["Alice", "Bob", "Charlie"],
    "tasks": ["book venue", "order cake", "send invitations"],
    "status": "planning",
    "budget": 500,
    "location": "Community Center"
  }
}
```

**Operations**:
- **Add Guests**: "Invite David to the party"
- **Add Tasks**: "Add 'buy decorations' to the party tasks"
- **Update Status**: "The party planning is in progress"
- **Set Budget**: "Set party budget to $600"

**Example Usage**:
```python
# Creates party planning module
response = gpt.query("I'm planning Sarah's birthday party on March 15th with Alice and Bob")

# Adds tasks
response = gpt.query("Add tasks: book the restaurant, buy decorations, prepare playlist")

# Updates guest list
response = gpt.query("Also invite Charlie and Diana to the party")
```

### 3. Calendar Modules (`calendar`)

**Purpose**: Manage schedules, appointments, and time-based events

**Auto-Created From**:
- "I have a dentist appointment on July 10th"
- "Schedule gym session for tomorrow"
- "My summer schedule includes..."
- "Meeting with client at 3 PM Thursday"

**Data Structure**:
```python
{
  "type": "calendar",
  "data": {
    "2025-07-10": {
      "time": "14:00",
      "event": "Dentist Appointment",
      "duration": "1 hour",
      "location": "Downtown Dental",
      "reminders": ["1 day before", "2 hours before"]
    }
  }
}
```

**Operations**:
- **Add Event**: "Schedule lunch meeting for Friday at noon"
- **Update Event**: "Move the dentist appointment to 3 PM"
- **Remove Event**: "Cancel the gym session on Tuesday"
- **View Schedule**: "What's on my calendar this week?"

**Example Usage**:
```python
# Creates calendar module
response = gpt.query("I have soccer practice every Tuesday at 6 PM")

# Adds more events
response = gpt.query("Also schedule piano lessons on Thursdays at 4 PM")

# Updates existing event
response = gpt.query("Move soccer practice to 7 PM")
```

### 4. Interest Modules (`interest`)

**Purpose**: Track learning topics, hobbies, and areas of curiosity

**Auto-Created From**:
- "I'm fascinated by quantum physics"
- "I want to learn more about cooking"
- "Tell me about Virginia Woolf's writing"
- "I'm interested in sustainable energy"

**Data Structure**:
```python
{
  "type": "interest",
  "data": {
    "keywords": ["quantum", "physics", "mechanics", "entanglement"],
    "engagementLevel": 8,
    "relatedTopics": ["mathematics", "philosophy", "technology"],
    "learningGoals": ["understand basic principles", "read introductory book"],
    "resources": ["Wikipedia articles", "YouTube videos", "online courses"]
  }
}
```

**Operations**:
- **Deepen Interest**: "I want to understand quantum entanglement better"
- **Add Resources**: "Add this book to my quantum physics resources"
- **Connect Topics**: "How does quantum physics relate to computing?"
- **Set Goals**: "My goal is to read one quantum physics book this month"

**Example Usage**:
```python
# Creates interest module
response = gpt.query("I'm fascinated by Virginia Woolf and her stream of consciousness technique")

# Deepens the interest
response = gpt.query("Tell me more about modernist literature and the Bloomsbury Group")

# Adds learning goal
response = gpt.query("I want to read 'Mrs. Dalloway' this month")
```

### 5. Tracker Modules (`tracker`)

**Purpose**: Monitor progress, metrics, habits, and measurable goals

**Auto-Created From**:
- "Track my daily water intake"
- "Monitor my exercise progress"
- "Keep track of my reading habits"
- "Log my coding practice time"

**Data Structure**:
```python
{
  "type": "tracker",
  "data": {
    "metric": "water_intake",
    "unit": "glasses",
    "target": 8,
    "current": 6,
    "history": {
      "2025-07-23": 8,
      "2025-07-22": 6,
      "2025-07-21": 7
    },
    "streak": 5,
    "trend": "improving"
  }
}
```

**Operations**:
- **Log Progress**: "I drank 3 glasses of water today"
- **Update Target**: "Change my water goal to 10 glasses per day"
- **View Stats**: "How am I doing with my water intake?"
- **Set Reminders**: "Remind me to log my water intake daily"

**Example Usage**:
```python
# Creates habit tracker
response = gpt.query("I want to track my daily exercise - target is 30 minutes")

# Logs progress
response = gpt.query("I exercised for 45 minutes today")

# Views progress
response = gpt.query("How am I doing with my exercise goal this week?")
```

### 6. Goal Modules (`goal`)

**Purpose**: Manage long-term objectives, milestones, and achievements

**Auto-Created From**:
- "My goal is to learn Spanish this year"
- "I want to save $10,000 for vacation"
- "Achieve promotion to senior developer"
- "Run a marathon by December"

**Data Structure**:
```python
{
  "type": "goal",
  "data": {
    "title": "Learn Spanish",
    "description": "Achieve conversational fluency in Spanish",
    "deadline": "2025-12-31",
    "progress": 35,
    "milestones": [
      {"name": "Complete beginner course", "completed": True},
      {"name": "Hold 10-minute conversation", "completed": False},
      {"name": "Watch movie without subtitles", "completed": False}
    ],
    "strategies": ["daily practice", "conversation partner", "immersion weekends"],
    "obstacles": ["limited time", "pronunciation challenges"]
  }
}
```

**Operations**:
- **Update Progress**: "I completed the Spanish beginner course"
- **Add Milestone**: "Add milestone: read Spanish newspaper article"
- **Adjust Timeline**: "Extend Spanish goal deadline to June 2026"
- **Track Obstacles**: "Time management is challenging for language practice"

**Example Usage**:
```python
# Creates goal module
response = gpt.query("My goal is to learn Spanish and be conversational by the end of the year")

# Updates progress
response = gpt.query("I completed my Spanish beginner course today")

# Adds strategy
response = gpt.query("I found a Spanish conversation partner to practice with")
```

## 🔗 Module Relationships and Intelligence

### Cross-Module Connections

Modules can reference and enhance each other:

```python
# Shopping list connects to party planning
response = gpt.query("Add party supplies to my shopping list for Sarah's birthday")

# Interest module influences goal setting
response = gpt.query("Set a goal to read 5 books about quantum physics this year")

# Calendar integrates with habit tracking
response = gpt.query("Schedule my daily exercise for 7 AM every day")
```

### Smart Suggestions

The system provides intelligent suggestions based on module relationships:

```python
response = gpt.query("I'm planning a dinner party")

# GPToggle might suggest:
# - "Should I create a shopping list for dinner ingredients?"
# - "Would you like to track RSVPs from guests?"
# - "Set a reminder to prepare the menu?"
```

## 🆔 Universal Module Identifiers (UMID)

Every module receives a globally unique identifier for cross-platform compatibility.

### UMID Format
```
{service}.{type}.{contextHash}.{timestamp}.{random}
```

### Examples
```
gptoggle.list.a1b2c3d4.1721737200.x7z9        # Shopping list
gptoggle.planner.e5f6g7h8.1721737201.m3p5     # Birthday party  
chatgpt.interest.i9j0k1l2.1721737202.q8w2     # Learning topic
notion.tracker.n4o6p8r0.1721737203.t1u3       # Progress tracker
```

### Working with UMIDs

```python
from modules.umidGenerator import UMIDGenerator, UMIDParser

# Generate UMID for your service
generator = UMIDGenerator('my-app')
umid = generator.generate_umid('list', ['shopping', 'groceries'])

# Parse existing UMID
parser = UMIDParser()
parsed = parser.parse(umid)
print(f"Service: {parsed['service']}")
print(f"Type: {parsed['moduleType']}")
print(f"Created: {parsed['createdAt']}")
```

## 🔄 Module Lifecycle Management

### Automatic Aging

Modules follow intelligent aging policies:

1. **Active Phase** (0-30 days): Full functionality, frequent updates
2. **Archive Phase** (30-90 days): Preserved but less accessible
3. **Cleanup Phase** (90+ days): Removed unless high priority

### Priority-Based Retention

High-priority modules (priority 7-10) receive extended retention:
- Shopping lists with frequent updates
- Important project plans
- Active learning interests
- Critical goal tracking

### Manual Lifecycle Control

```python
# Get modules summary
summary = user_profile.get_modules_summary()

# Force cleanup of old modules
cleanup_result = module_service.cleanup_stale_modules(user_profile)
print(f"Archived: {cleanup_result['archived']}")
print(f"Removed: {cleanup_result['removed']}")

# Manually archive a module
module_service.archive_module(user_profile, umid)

# Restore archived module
module_service.restore_module(user_profile, umid)
```

## 🔧 Customizing Module Behavior

### Custom Module Types

Create your own module types for specialized needs:

```python
class CustomModuleService(EnhancedModuleService):
    def _detect_new_module_opportunities_umid(self, query):
        opportunities = super()._detect_new_module_opportunities_umid(query)
        
        # Add custom module detection
        if 'recipe' in query.lower():
            opportunities.append({
                'type': 'recipe',
                'keywords': ['cooking', 'recipe'] + self._extract_ingredients(query),
                'data': self._extract_recipe_data(query),
                'confidence': 0.9
            })
        
        return opportunities
```

### Module Schema Extensions

Extend the user profile schema for custom data:

```json
{
  "modules": {
    "custom-module-umid": {
      "type": "recipe",
      "data": {
        "title": "Chocolate Chip Cookies",
        "ingredients": ["flour", "sugar", "eggs"],
        "instructions": ["Mix ingredients", "Bake at 350°F"],
        "servings": 24,
        "cookTime": "25 minutes"
      }
    }
  }
}
```

## 📈 Analytics and Insights

### Module Usage Statistics

```python
# Get comprehensive module analytics
analytics = user_profile.get_module_analytics()

print(f"Most active module type: {analytics['most_active_type']}")
print(f"Average modules per user: {analytics['avg_modules_per_user']}")
print(f"Module creation rate: {analytics['creation_rate']} per day")

# Track module effectiveness
for module_type, stats in analytics['type_stats'].items():
    print(f"{module_type}: {stats['avg_interactions']} interactions")
```

### User Behavior Patterns

```python
# Analyze user patterns
patterns = user_profile.analyze_usage_patterns()

print(f"Peak usage time: {patterns['peak_hours']}")
print(f"Favorite module type: {patterns['preferred_type']}")
print(f"Module retention rate: {patterns['retention_rate']}%")
```

## 🚀 Advanced Module Operations

### Batch Module Operations

```python
# Process multiple queries efficiently
queries = [
    "Add milk and eggs to shopping list",
    "Schedule dentist appointment for Friday",
    "Track my daily reading progress"
]

results = gpt.batch_query_with_modules(queries)
for query, result in zip(queries, results):
    print(f"Query: {query}")
    print(f"Modules affected: {len(result['moduleActions'])}")
```

### Module Export and Import

```python
# Export modules for another platform
export_data = module_service.export_modules_for_service(
    user_profile, 
    target_service='notion'
)

# Import modules from another service
imported_modules = module_service.import_modules_from_service(
    export_data,
    current_service='gptoggle'
)
```

### Module Synchronization

```python
# Sync modules across multiple GPToggle instances
sync_manager = ModuleSyncManager(['gptoggle-web', 'gptoggle-mobile'])

# Push local changes
sync_manager.push_changes(user_profile)

# Pull remote changes  
sync_manager.pull_changes(user_profile)
```

## 🎯 Best Practices

### Query Optimization

**Good Queries** (create clear modules):
- "I need to buy milk, eggs, and bread for breakfast"
- "Plan my birthday party for March 15th with 10 friends"
- "Track my daily water intake goal of 8 glasses"

**Poor Queries** (unclear or too vague):
- "Buy stuff"
- "Plan something"
- "Track things"

### Module Organization

**Naming Conventions**:
- Use descriptive context keywords
- Include relevant details (dates, quantities, purposes)
- Avoid generic terms

**Priority Management**:
- High priority (8-10): Critical ongoing projects
- Medium priority (5-7): Regular activities and interests  
- Low priority (1-4): Occasional or experimental items

### Performance Optimization

**Efficient Module Usage**:
```python
# Good: Specific updates
response = gpt.query("Add organic apples to my grocery list")

# Better: Batch updates when possible
response = gpt.query("Add organic apples, whole grain bread, and Greek yogurt to my grocery list")

# Best: Context-aware updates
response = gpt.query("Add healthy breakfast items to my grocery list: organic apples, whole grain bread, and Greek yogurt")
```

## 🔍 Debugging Module Issues

### Common Problems and Solutions

**Module Not Created**:
```python
# Check if query was specific enough
response = gpt.query("I need to buy some things")  # Too vague
response = gpt.query("I need to buy milk and eggs")  # Specific enough

# Check module actions
for action in response.get('moduleActions', []):
    if not action['success']:
        print(f"Failed: {action.get('error', 'Unknown error')}")
```

**Module Not Updated**:
```python
# Verify module exists and is accessible
modules = user_profile.context.get('modules', {})
print(f"Current modules: {list(modules.keys())}")

# Use more explicit update language
response = gpt.query("Update my shopping list to include cheese")
```

**Module Cleanup Issues**:
```python
# Check module ages and priorities
for umid, module in modules.items():
    metadata = module.get('metadata', {})
    print(f"Module {umid}: Priority {metadata.get('priority', 5)}")
    print(f"Last accessed: {metadata.get('lastAccessed', 'Never')}")
```

## 🌟 Future Module Capabilities

### Planned Features

**v2.1 (Q4 2025)**:
- Voice-activated module creation
- Visual module planning with diagrams
- Team collaboration on shared modules
- Advanced pattern recognition

**v2.2 (Q1 2026)**:
- AI-powered module suggestions
- Custom module templates
- Integration with external tools
- Mobile-optimized module interfaces

### Experimental Features

**Emotional Intelligence Modules**:
- Mood tracking and correlation with activities
- Sentiment analysis of module interactions
- Adaptive responses based on emotional context

**Predictive Modules**:
- Automatic module creation based on usage patterns
- Predictive text for module updates
- Smart scheduling based on historical data

The Modular Adaptive Intelligence system represents a fundamental shift in how AI assistants understand and support user needs. By automatically creating and managing specialized knowledge containers, GPToggle v2.0 provides unprecedented personalization that grows and adapts with each interaction.