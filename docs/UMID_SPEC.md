# Universal Module Identifier (UMID) Specification

This document defines the Universal Module Identifier (UMID) specification - a standardized system for creating globally unique identifiers for adaptive intelligence modules across any service or platform.

## 🎯 Overview

The Universal Module Identifier (UMID) provides a cross-platform standard for identifying and managing adaptive intelligence modules. It enables seamless module portability between different services while ensuring collision-free identification in distributed systems.

## 📐 Specification Format

### Schema Structure
```
{service}.{moduleType}.{contextHash}.{timestamp}.{random}
```

### Example
```
gptoggle.list.a1b2c3d4.1721737200.x7z9
```

## 🧩 Component Specifications

### 1. Service Identifier (`service`)

**Purpose**: Identifies the originating service, platform, or application

**Format Requirements**:
- Length: 3-20 characters
- Character set: Lowercase letters (a-z), numbers (0-9), hyphens (-)
- Pattern: `^[a-z0-9-]{3,20}$`

**Valid Examples**:
- `gptoggle`
- `chatgpt`
- `claude`
- `notion`
- `slack`
- `my-custom-app`
- `ai-assistant-v2`

**Invalid Examples**:
- `GP` (too short)
- `MyApp` (uppercase letters)
- `my_app` (underscore not allowed)
- `very-long-service-name-here` (too long)

### 2. Module Type (`moduleType`)

**Purpose**: Categorizes the module's functional purpose

**Format Requirements**:
- Length: 1-20 characters
- Character set: Lowercase letters (a-z) only
- Pattern: `^[a-z]{1,20}$`

**Standard Types**:
- `list` - Item collections, shopping lists, todo lists
- `planner` - Event planning, project coordination
- `calendar` - Schedule management, appointments
- `interest` - Learning topics, hobbies, research areas
- `tracker` - Progress monitoring, metrics, habits
- `goal` - Long-term objectives, milestones
- `note` - Knowledge capture, documentation
- `contact` - People management, relationships
- `location` - Places, addresses, travel information
- `custom` - Service-specific module types

**Custom Types**: Services can define custom module types following the format requirements.

### 3. Context Hash (`contextHash`)

**Purpose**: Represents the semantic context of the module for grouping and identification

**Format Requirements**:
- Length: Exactly 8 characters
- Character set: Lowercase hexadecimal (a-f, 0-9)
- Pattern: `^[a-f0-9]{8}$`

**Generation Algorithm**:
1. Collect context keywords from module creation
2. Normalize keywords (lowercase, trim whitespace)
3. Sort keywords alphabetically for consistency
4. Join keywords with spaces
5. Generate SHA-256 hash of the string
6. Take first 8 characters of hexadecimal representation

**Example Generation**:
```python
import hashlib

keywords = ['shopping', 'groceries', 'weekly']
context_string = ' '.join(sorted(keywords))  # 'groceries shopping weekly'
hash_object = hashlib.sha256(context_string.encode('utf-8'))
context_hash = hash_object.hexdigest()[:8]  # 'a1b2c3d4'
```

### 4. Timestamp (`timestamp`)

**Purpose**: Records creation time for chronological ordering and lifecycle management

**Format Requirements**:
- Length: Exactly 10 characters
- Character set: Numbers (0-9) only
- Pattern: `^\d{10}$`
- Value: Unix timestamp (seconds since epoch)

**Generation**:
```python
import time
timestamp = str(int(time.time()))  # '1721737200'
```

**Validation Range**:
- Minimum: `1000000000` (September 9, 2001)
- Maximum: `9999999999` (November 20, 2286)

### 5. Random Component (`random`)

**Purpose**: Ensures uniqueness even when other components are identical

**Format Requirements**:
- Length: Exactly 4 characters
- Character set: Lowercase letters (a-z) and numbers (0-9)
- Pattern: `^[a-z0-9]{4}$`

**Generation**:
```python
import random
import string

chars = string.ascii_lowercase + string.digits
random_component = ''.join(random.choices(chars, k=4))  # 'x7z9'
```

## ✅ Validation Rules

### Complete UMID Validation

**Full Pattern**:
```regex
^[a-z0-9-]{3,20}\.[a-z]{1,20}\.[a-f0-9]{8}\.\d{10}\.[a-z0-9]{4}$
```

**Validation Function**:
```python
import re

def validate_umid(umid: str) -> bool:
    pattern = r'^[a-z0-9-]{3,20}\.[a-z]{1,20}\.[a-f0-9]{8}\.\d{10}\.[a-z0-9]{4}$'
    return bool(re.match(pattern, umid))
```

### Component Validation

```python
def validate_components(service, module_type, context_hash, timestamp, random):
    # Service validation
    if not re.match(r'^[a-z0-9-]{3,20}$', service):
        return False, "Invalid service identifier"
    
    # Module type validation  
    if not re.match(r'^[a-z]{1,20}$', module_type):
        return False, "Invalid module type"
    
    # Context hash validation
    if not re.match(r'^[a-f0-9]{8}$', context_hash):
        return False, "Invalid context hash"
    
    # Timestamp validation
    if not re.match(r'^\d{10}$', timestamp):
        return False, "Invalid timestamp format"
    
    timestamp_int = int(timestamp)
    if timestamp_int < 1000000000 or timestamp_int > 9999999999:
        return False, "Timestamp out of valid range"
    
    # Random component validation
    if not re.match(r'^[a-z0-9]{4}$', random):
        return False, "Invalid random component"
    
    return True, "Valid UMID"
```

## 🏗️ Implementation Guidelines

### Reference Implementation (Python)

```python
import time
import hashlib
import random
import string
import re
from typing import List, Optional, Dict, Any

class UMIDGenerator:
    def __init__(self, service_id: str):
        if not self._validate_service_id(service_id):
            raise ValueError(f"Invalid service_id: {service_id}")
        self.service_id = service_id.lower()
    
    def _validate_service_id(self, service_id: str) -> bool:
        return bool(re.match(r'^[a-z0-9-]{3,20}$', service_id))
    
    def generate_context_hash(self, keywords: List[str]) -> str:
        if not keywords:
            keywords = ['default']
        
        context_string = ' '.join(sorted(k.lower().strip() for k in keywords if k.strip()))
        hash_object = hashlib.sha256(context_string.encode('utf-8'))
        return hash_object.hexdigest()[:8]
    
    def generate_random_component(self) -> str:
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=4))
    
    def generate_umid(self, module_type: str, context_keywords: List[str]) -> str:
        if not re.match(r'^[a-z]{1,20}$', module_type):
            raise ValueError(f"Invalid module_type: {module_type}")
        
        context_hash = self.generate_context_hash(context_keywords)
        timestamp = str(int(time.time()))
        random_component = self.generate_random_component()
        
        return f"{self.service_id}.{module_type}.{context_hash}.{timestamp}.{random_component}"
```

### Reference Implementation (JavaScript/TypeScript)

```typescript
import crypto from 'crypto';

export class UMIDGenerator {
  private serviceId: string;

  constructor(serviceId: string) {
    if (!/^[a-z0-9-]{3,20}$/.test(serviceId)) {
      throw new Error(`Invalid service_id: ${serviceId}`);
    }
    this.serviceId = serviceId.toLowerCase();
  }

  generateContextHash(keywords: string[]): string {
    if (!keywords || keywords.length === 0) {
      keywords = ['default'];
    }

    const contextString = keywords
      .map(k => k.toLowerCase().trim())
      .filter(k => k.length > 0)
      .sort()
      .join(' ');

    return crypto
      .createHash('sha256')
      .update(contextString, 'utf8')
      .digest('hex')
      .substring(0, 8);
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
    if (!/^[a-z]{1,20}$/.test(moduleType)) {
      throw new Error(`Invalid module_type: ${moduleType}`);
    }

    const contextHash = this.generateContextHash(contextKeywords);
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const randomComponent = this.generateRandomComponent();

    return `${this.serviceId}.${moduleType}.${contextHash}.${timestamp}.${randomComponent}`;
  }
}
```

## 🗄️ Storage Recommendations

### Database Schema (SQL)

```sql
CREATE TABLE modules (
    umid VARCHAR(255) PRIMARY KEY,
    service_id VARCHAR(20) NOT NULL,
    module_type VARCHAR(20) NOT NULL,
    context_hash CHAR(8) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    random_component CHAR(4) NOT NULL,
    
    -- Module payload
    data JSONB NOT NULL,
    metadata JSONB NOT NULL,
    
    -- Indexes for efficient querying
    INDEX idx_service_type (service_id, module_type),
    INDEX idx_context_hash (context_hash),
    INDEX idx_created_at (created_at),
    
    -- Constraints
    CONSTRAINT chk_service_format CHECK (service_id REGEXP '^[a-z0-9-]{3,20}$'),
    CONSTRAINT chk_type_format CHECK (module_type REGEXP '^[a-z]{1,20}$'),
    CONSTRAINT chk_context_format CHECK (context_hash REGEXP '^[a-f0-9]{8}$'),
    CONSTRAINT chk_random_format CHECK (random_component REGEXP '^[a-z0-9]{4}$')
);
```

### NoSQL Schema (MongoDB)

```javascript
{
  "_id": "gptoggle.list.a1b2c3d4.1721737200.x7z9",
  "umid": "gptoggle.list.a1b2c3d4.1721737200.x7z9",
  "components": {
    "service": "gptoggle",
    "moduleType": "list", 
    "contextHash": "a1b2c3d4",
    "timestamp": 1721737200,
    "randomComponent": "x7z9"
  },
  "data": {
    // Module-specific data
  },
  "metadata": {
    "createdAt": "2025-07-23T12:00:00Z",
    "lastUpdated": "2025-07-23T12:00:00Z",
    "priority": 8,
    "tags": ["shopping", "groceries"]
  }
}
```

## 🔄 Migration Strategies

### From Legacy Systems

```python
def migrate_legacy_modules(legacy_modules: Dict, service_id: str) -> Dict:
    generator = UMIDGenerator(service_id)
    migrated = {}
    
    for old_key, module in legacy_modules.items():
        # Extract context from legacy data
        context_keywords = extract_keywords_from_legacy(module, old_key)
        module_type = infer_module_type(module)
        
        # Generate new UMID
        umid = generator.generate_umid(module_type, context_keywords)
        
        # Preserve legacy reference
        module['migration'] = {
            'legacy_key': old_key,
            'migrated_at': time.time(),
            'umid': umid
        }
        
        migrated[umid] = module
    
    return migrated
```

### Cross-Service Migration

```python
def export_for_service(modules: Dict, target_service: str) -> Dict:
    export_data = {
        'source_service': 'gptoggle',
        'target_service': target_service,
        'export_timestamp': time.time(),
        'modules': {}
    }
    
    for umid, module in modules.items():
        # Create portable format
        export_data['modules'][umid] = {
            'original_umid': umid,
            'type': module['type'],
            'data': module['data'],
            'metadata': module['metadata'],
            'context_keywords': module['metadata'].get('contextKeywords', [])
        }
    
    return export_data
```

## 📊 Analytics and Insights

### UMID-Based Analytics

```python
def analyze_umid_patterns(umids: List[str]) -> Dict[str, Any]:
    analysis = {
        'services': {},
        'module_types': {},
        'creation_timeline': {},
        'context_clusters': {}
    }
    
    for umid in umids:
        parsed = UMIDParser.parse(umid)
        if not parsed:
            continue
        
        # Service distribution
        service = parsed['service']
        analysis['services'][service] = analysis['services'].get(service, 0) + 1
        
        # Module type distribution
        module_type = parsed['moduleType']
        analysis['module_types'][module_type] = analysis['module_types'].get(module_type, 0) + 1
        
        # Timeline analysis
        timestamp = parsed['timestamp']
        date = datetime.fromtimestamp(timestamp).date()
        analysis['creation_timeline'][str(date)] = analysis['creation_timeline'].get(str(date), 0) + 1
        
        # Context clustering
        context_hash = parsed['contextHash']
        analysis['context_clusters'][context_hash] = analysis['context_clusters'].get(context_hash, 0) + 1
    
    return analysis
```

## 🔒 Security Considerations

### Privacy Protection

- **No Personal Data**: UMIDs contain no personally identifiable information
- **Context Hashing**: Keywords are hashed, not stored in plain text
- **Service Isolation**: Service identifiers prevent cross-contamination

### Collision Resistance

- **Cryptographic Hashing**: SHA-256 provides strong collision resistance
- **Temporal Uniqueness**: Timestamp component ensures time-based uniqueness
- **Random Component**: 4-character random string provides 1.6M additional combinations

### Validation Requirements

```python
def secure_umid_validation(umid: str) -> bool:
    # Format validation
    if not validate_umid(umid):
        return False
    
    # Timestamp validation (prevent future timestamps)
    parsed = UMIDParser.parse(umid)
    if parsed['timestamp'] > int(time.time()) + 300:  # Allow 5 minutes clock skew
        return False
    
    # Service whitelist (if applicable)
    allowed_services = ['gptoggle', 'chatgpt', 'claude', 'notion']
    if parsed['service'] not in allowed_services:
        return False
    
    return True
```

## 🌍 Interoperability Standards

### Cross-Platform Exchange Format

```json
{
  "format_version": "1.0",
  "exchange_timestamp": "2025-07-23T12:00:00Z",
  "source_service": "gptoggle",
  "target_service": "notion",
  "modules": [
    {
      "umid": "gptoggle.list.a1b2c3d4.1721737200.x7z9",
      "type": "list",
      "context_keywords": ["shopping", "groceries"],
      "data": ["milk", "eggs", "bread"],
      "metadata": {
        "priority": 8,
        "created_at": "2025-07-23T12:00:00Z",
        "tags": ["shopping"]
      }
    }
  ]
}
```

### Import/Export APIs

```python
class UMIDExchangeAPI:
    def export_modules(self, service_filter: Optional[str] = None) -> Dict:
        """Export modules in standard exchange format"""
        pass
    
    def import_modules(self, exchange_data: Dict, conflict_resolution: str = 'skip') -> Dict:
        """Import modules from standard exchange format"""
        pass
    
    def validate_exchange_format(self, data: Dict) -> bool:
        """Validate exchange format compliance"""
        pass
```

## 📋 Compliance Checklist

### For Implementation

- [ ] UMID format validation implemented
- [ ] All components follow specification requirements
- [ ] Context hash generation uses SHA-256
- [ ] Timestamp uses Unix epoch seconds
- [ ] Random component uses specified character set
- [ ] Migration support for legacy systems
- [ ] Export/import functionality for interoperability
- [ ] Security validation for timestamps and services
- [ ] Analytics support for UMID-based insights
- [ ] Documentation and examples provided

### For Services Adopting UMID

- [ ] Service identifier registered and validated
- [ ] Standard module types supported
- [ ] Custom module types follow naming conventions
- [ ] Database schema supports UMID structure
- [ ] Migration path from existing identifiers
- [ ] Cross-service export capabilities
- [ ] Proper error handling for invalid UMIDs
- [ ] Analytics integration for usage insights

The Universal Module Identifier specification provides a robust foundation for cross-platform module interoperability, enabling the next generation of truly portable adaptive intelligence systems.