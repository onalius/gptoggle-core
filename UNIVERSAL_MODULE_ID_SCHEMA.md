# Universal Module Identifier Schema (UMID)

## Overview

The Universal Module Identifier Schema (UMID) provides a standardized, globally unique identification system for adaptive intelligence modules across any service, platform, or project. This schema ensures module portability, interoperability, and collision-free identification in distributed systems.

## Schema Structure

### Format
```
{service}.{moduleType}.{contextHash}.{timestamp}.{random}
```

### Components

#### 1. Service Identifier (`service`)
- **Purpose**: Identifies the originating service/project/platform
- **Format**: Lowercase alphanumeric with optional hyphens
- **Length**: 3-20 characters
- **Examples**: 
  - `gptoggle` - GPToggle platform
  - `chatgpt` - ChatGPT service
  - `claude` - Anthropic Claude
  - `notion` - Notion workspace
  - `slack` - Slack workspace
  - `my-app` - Custom application

#### 2. Module Type (`moduleType`)
- **Purpose**: Categorizes the module functionality
- **Format**: Lowercase single word
- **Standard Types**:
  - `list` - Item collections, shopping lists, todo lists
  - `planner` - Event planning, project coordination
  - `calendar` - Schedule management, appointments
  - `interest` - Learning topics, hobbies, research areas
  - `tracker` - Progress monitoring, metrics, habits
  - `goal` - Long-term objectives, milestones
  - `note` - Knowledge capture, documentation
  - `contact` - People management, relationships
  - `location` - Places, addresses, travel
  - `custom` - Service-specific module types

#### 3. Context Hash (`contextHash`)
- **Purpose**: Represents the semantic context of the module
- **Format**: 8-character hexadecimal hash
- **Generation**: SHA-256 hash of primary context keywords, truncated
- **Examples**:
  - Shopping list for "groceries" → `a1b2c3d4`
  - Birthday party for "Alice" → `e5f6g7h8`
  - Learning about "Python" → `i9j0k1l2`

#### 4. Timestamp (`timestamp`)
- **Purpose**: Creation time for ordering and aging
- **Format**: Unix timestamp (seconds since epoch)
- **Example**: `1721737200` (July 23, 2025)

#### 5. Random Component (`random`)
- **Purpose**: Ensures uniqueness even with identical context/time
- **Format**: 4-character alphanumeric (base36)
- **Example**: `x7z9`, `m3p5`, `q8w2`

## Complete Examples

```
gptoggle.list.a1b2c3d4.1721737200.x7z9
chatgpt.planner.e5f6g7h8.1721737201.m3p5
notion.tracker.i9j0k1l2.1721737202.q8w2
slack.goal.n4o6p8r0.1721737203.t1u3
my-app.custom.s2v4x6z8.1721737204.y5a7
```

## Implementation Guide

### Context Hash Generation

```python
import hashlib

def generate_context_hash(keywords):
    """Generate 8-character context hash from keywords"""
    context_string = ' '.join(sorted(keywords)).lower()
    hash_object = hashlib.sha256(context_string.encode())
    return hash_object.hexdigest()[:8]

# Examples
generate_context_hash(['shopping', 'groceries', 'weekly']) → 'a1b2c3d4'
generate_context_hash(['birthday', 'party', 'alice']) → 'e5f6g7h8'
```

### Random Component Generation

```python
import random
import string

def generate_random_component():
    """Generate 4-character random component"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=4))

# Examples
generate_random_component() → 'x7z9'
generate_random_component() → 'm3p5'
```

### Complete UMID Generation

```python
import time
import hashlib
import random
import string

class UMIDGenerator:
    def __init__(self, service_id):
        self.service_id = service_id.lower()
    
    def generate_umid(self, module_type, context_keywords):
        """Generate complete UMID"""
        # Context hash
        context_string = ' '.join(sorted(context_keywords)).lower()
        context_hash = hashlib.sha256(context_string.encode()).hexdigest()[:8]
        
        # Timestamp
        timestamp = str(int(time.time()))
        
        # Random component
        chars = string.ascii_lowercase + string.digits
        random_component = ''.join(random.choices(chars, k=4))
        
        # Combine components
        umid = f"{self.service_id}.{module_type}.{context_hash}.{timestamp}.{random_component}"
        return umid

# Usage examples
generator = UMIDGenerator('gptoggle')
umid1 = generator.generate_umid('list', ['shopping', 'groceries'])
umid2 = generator.generate_umid('planner', ['birthday', 'party', 'alice'])
```

### TypeScript Implementation

```typescript
import crypto from 'crypto';

class UMIDGenerator {
  private serviceId: string;

  constructor(serviceId: string) {
    this.serviceId = serviceId.toLowerCase();
  }

  generateContextHash(keywords: string[]): string {
    const contextString = keywords.sort().join(' ').toLowerCase();
    return crypto.createHash('sha256').update(contextString).digest('hex').substring(0, 8);
  }

  generateRandomComponent(): string {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 4; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  generateUMID(moduleType: string, contextKeywords: string[]): string {
    const contextHash = this.generateContextHash(contextKeywords);
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const randomComponent = this.generateRandomComponent();
    
    return `${this.serviceId}.${moduleType}.${contextHash}.${timestamp}.${randomComponent}`;
  }
}

// Usage
const generator = new UMIDGenerator('gptoggle');
const umid1 = generator.generateUMID('list', ['shopping', 'groceries']);
const umid2 = generator.generateUMID('planner', ['birthday', 'party', 'alice']);
```

## Parsing and Validation

### UMID Parser

```python
import re
from typing import Optional, Dict

class UMIDParser:
    UMID_PATTERN = r'^([a-z0-9-]{3,20})\.([a-z]+)\.([a-f0-9]{8})\.(\d{10})\.([a-z0-9]{4})$'
    
    @classmethod
    def parse(cls, umid: str) -> Optional[Dict[str, str]]:
        """Parse UMID into components"""
        match = re.match(cls.UMID_PATTERN, umid)
        if not match:
            return None
        
        return {
            'service': match.group(1),
            'moduleType': match.group(2),
            'contextHash': match.group(3),
            'timestamp': int(match.group(4)),
            'random': match.group(5),
            'full': umid
        }
    
    @classmethod
    def validate(cls, umid: str) -> bool:
        """Validate UMID format"""
        return bool(re.match(cls.UMID_PATTERN, umid))

# Usage
parser = UMIDParser()
parsed = parser.parse('gptoggle.list.a1b2c3d4.1721737200.x7z9')
is_valid = parser.validate('gptoggle.list.a1b2c3d4.1721737200.x7z9')
```

## Database Schema

### SQL Schema
```sql
CREATE TABLE modules (
    umid VARCHAR(255) PRIMARY KEY,
    service_id VARCHAR(20) NOT NULL,
    module_type VARCHAR(50) NOT NULL,
    context_hash CHAR(8) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    random_component CHAR(4) NOT NULL,
    
    -- Module data
    data JSONB NOT NULL,
    metadata JSONB NOT NULL,
    
    -- Indexes for efficient querying
    INDEX idx_service_type (service_id, module_type),
    INDEX idx_context_hash (context_hash),
    INDEX idx_created_at (created_at)
);
```

### NoSQL Schema (MongoDB)
```javascript
{
  _id: "gptoggle.list.a1b2c3d4.1721737200.x7z9",
  umid: "gptoggle.list.a1b2c3d4.1721737200.x7z9",
  service: "gptoggle",
  moduleType: "list",
  contextHash: "a1b2c3d4",
  timestamp: 1721737200,
  randomComponent: "x7z9",
  
  data: {
    items: ["milk", "eggs", "bread"],
    completed: []
  },
  
  metadata: {
    priority: 8,
    tags: ["grocery", "weekly"],
    archived: false,
    lastAccessed: "2025-07-23T12:00:00Z"
  }
}
```

## Benefits

### Collision Avoidance
- **Service Namespace**: Prevents conflicts between different platforms
- **Context Differentiation**: Similar modules have different context hashes
- **Temporal Uniqueness**: Timestamp ensures chronological uniqueness
- **Random Guarantee**: Final random component eliminates any remaining collision risk

### Interoperability
- **Cross-Platform**: Modules can be transferred between services
- **Standardized Format**: Consistent parsing across implementations
- **Backward Compatibility**: Schema can evolve without breaking existing IDs

### Analytics and Insights
- **Service Attribution**: Track module origins and usage patterns
- **Type Analysis**: Understand module type popularity and effectiveness
- **Temporal Patterns**: Analyze creation and usage trends
- **Context Clustering**: Group similar modules for recommendations

### Scalability
- **Distributed Generation**: No central authority required
- **High Throughput**: Fast generation without database lookups
- **Storage Efficient**: Compact representation with rich information

## Migration Guide

### From Existing Systems

#### GPToggle Current → UMID
```python
def migrate_gptoggle_modules(existing_modules):
    """Migrate existing GPToggle modules to UMID format"""
    generator = UMIDGenerator('gptoggle')
    migrated = {}
    
    for old_key, module in existing_modules.items():
        # Extract context from old key or module data
        context_keywords = extract_keywords_from_module(module)
        module_type = module.get('type', 'custom')
        
        # Generate new UMID
        new_umid = generator.generate_umid(module_type, context_keywords)
        
        # Preserve original data with new ID
        migrated[new_umid] = {
            **module,
            'umid': new_umid,
            'legacy_key': old_key
        }
    
    return migrated
```

#### Generic Migration
```python
def migrate_to_umid(service_id, modules, key_extractor, type_extractor):
    """Generic migration function for any service"""
    generator = UMIDGenerator(service_id)
    migrated = {}
    
    for module in modules:
        context_keywords = key_extractor(module)
        module_type = type_extractor(module)
        
        new_umid = generator.generate_umid(module_type, context_keywords)
        migrated[new_umid] = {
            **module,
            'umid': new_umid
        }
    
    return migrated
```

## Adoption Examples

### Notion Integration
```typescript
const notionGenerator = new UMIDGenerator('notion');

// Create module for a database
const databaseModuleId = notionGenerator.generateUMID('tracker', ['habit', 'exercise']);

// Create module for a page
const pageModuleId = notionGenerator.generateUMID('note', ['meeting', 'quarterly', 'review']);
```

### Slack Integration
```python
slack_generator = UMIDGenerator('slack')

# Create module for channel topic
channel_module = slack_generator.generate_umid('interest', ['javascript', 'learning'])

# Create module for recurring event
event_module = slack_generator.generate_umid('calendar', ['standup', 'daily'])
```

### Custom Application
```javascript
const myAppGenerator = new UMIDGenerator('my-custom-app');

// Create domain-specific modules
const userPrefsId = myAppGenerator.generateUMID('custom', ['user', 'preferences']);
const workflowId = myAppGenerator.generateUMID('custom', ['automation', 'workflow']);
```

## Future Extensions

### Hierarchical Extensions
- **Parent-Child Relationships**: `parent.child` format for sub-modules
- **Version Management**: Append version numbers for module evolution
- **Geographical Context**: Optional geo-coding for location-aware modules

### Federation Support
- **Cross-Service References**: Standardized linking between services
- **Shared Modules**: Collaborative modules across platforms
- **Synchronization Protocols**: Real-time updates across services

The Universal Module Identifier Schema provides a robust foundation for the next generation of adaptive intelligence systems, enabling seamless interoperability and unlimited scalability across any platform or service.