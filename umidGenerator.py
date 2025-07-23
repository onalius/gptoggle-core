#!/usr/bin/env python3
"""
Universal Module Identifier (UMID) Generator

This module provides a standardized system for generating globally unique
identifiers for adaptive intelligence modules across any service or platform.

Format: {service}.{moduleType}.{contextHash}.{timestamp}.{random}
Example: gptoggle.list.a1b2c3d4.1721737200.x7z9
"""

import time
import hashlib
import random
import string
import re
from typing import Optional, Dict, List

class UMIDGenerator:
    """Generator for Universal Module Identifiers"""
    
    def __init__(self, service_id: str):
        """
        Initialize UMID generator for a specific service
        
        Args:
            service_id: Service identifier (3-20 chars, lowercase alphanumeric with hyphens)
        """
        if not self._validate_service_id(service_id):
            raise ValueError(f"Invalid service_id: {service_id}. Must be 3-20 chars, lowercase alphanumeric with hyphens")
        
        self.service_id = service_id.lower()
    
    def _validate_service_id(self, service_id: str) -> bool:
        """Validate service ID format"""
        pattern = r'^[a-z0-9-]{3,20}$'
        return bool(re.match(pattern, service_id))
    
    def generate_context_hash(self, keywords: List[str]) -> str:
        """
        Generate 8-character context hash from keywords
        
        Args:
            keywords: List of context keywords
            
        Returns:
            8-character hexadecimal hash
        """
        if not keywords:
            keywords = ['default']
        
        # Normalize and sort keywords for consistent hashing
        context_string = ' '.join(sorted(k.lower().strip() for k in keywords if k.strip()))
        
        # Generate SHA-256 hash and truncate to 8 characters
        hash_object = hashlib.sha256(context_string.encode('utf-8'))
        return hash_object.hexdigest()[:8]
    
    def generate_random_component(self) -> str:
        """
        Generate 4-character random component
        
        Returns:
            4-character random string (lowercase alphanumeric)
        """
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=4))
    
    def generate_umid(self, module_type: str, context_keywords: List[str]) -> str:
        """
        Generate complete Universal Module Identifier
        
        Args:
            module_type: Type of module (list, planner, calendar, interest, tracker, goal, etc.)
            context_keywords: Keywords describing the module context
            
        Returns:
            Complete UMID string
        """
        # Validate module type
        if not re.match(r'^[a-z]+$', module_type):
            raise ValueError(f"Invalid module_type: {module_type}. Must be lowercase alphabetic")
        
        # Generate components
        context_hash = self.generate_context_hash(context_keywords)
        timestamp = str(int(time.time()))
        random_component = self.generate_random_component()
        
        # Combine into UMID
        umid = f"{self.service_id}.{module_type}.{context_hash}.{timestamp}.{random_component}"
        return umid
    
    def generate_batch_umids(self, modules_data: List[Dict]) -> List[str]:
        """
        Generate multiple UMIDs efficiently
        
        Args:
            modules_data: List of dicts with 'type' and 'keywords' keys
            
        Returns:
            List of generated UMIDs
        """
        umids = []
        for module_data in modules_data:
            umid = self.generate_umid(
                module_data['type'], 
                module_data['keywords']
            )
            umids.append(umid)
        return umids

class UMIDParser:
    """Parser and validator for Universal Module Identifiers"""
    
    UMID_PATTERN = r'^([a-z0-9-]{3,20})\.([a-z]+)\.([a-f0-9]{8})\.(\d{10})\.([a-z0-9]{4})$'
    
    @classmethod
    def parse(cls, umid: str) -> Optional[Dict[str, any]]:
        """
        Parse UMID into components
        
        Args:
            umid: Universal Module Identifier string
            
        Returns:
            Dictionary with parsed components or None if invalid
        """
        match = re.match(cls.UMID_PATTERN, umid)
        if not match:
            return None
        
        timestamp = int(match.group(4))
        
        return {
            'service': match.group(1),
            'moduleType': match.group(2),
            'contextHash': match.group(3),
            'timestamp': timestamp,
            'createdAt': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
            'random': match.group(5),
            'full': umid
        }
    
    @classmethod
    def validate(cls, umid: str) -> bool:
        """
        Validate UMID format
        
        Args:
            umid: Universal Module Identifier string
            
        Returns:
            True if valid format, False otherwise
        """
        return bool(re.match(cls.UMID_PATTERN, umid))
    
    @classmethod
    def extract_service(cls, umid: str) -> Optional[str]:
        """Extract service ID from UMID"""
        parsed = cls.parse(umid)
        return parsed['service'] if parsed else None
    
    @classmethod
    def extract_type(cls, umid: str) -> Optional[str]:
        """Extract module type from UMID"""
        parsed = cls.parse(umid)
        return parsed['moduleType'] if parsed else None
    
    @classmethod  
    def extract_timestamp(cls, umid: str) -> Optional[int]:
        """Extract timestamp from UMID"""
        parsed = cls.parse(umid)
        return parsed['timestamp'] if parsed else None

class UMIDMigrator:
    """Utility for migrating existing module systems to UMID"""
    
    def __init__(self, service_id: str):
        self.generator = UMIDGenerator(service_id)
    
    def migrate_gptoggle_modules(self, existing_modules: Dict) -> Dict:
        """
        Migrate existing GPToggle modules to UMID format
        
        Args:
            existing_modules: Dictionary of existing modules
            
        Returns:
            Dictionary with new UMID keys
        """
        migrated = {}
        
        for old_key, module in existing_modules.items():
            # Extract context from module data
            context_keywords = self._extract_keywords_from_module(module, old_key)
            module_type = module.get('type', 'custom')
            
            # Generate new UMID
            new_umid = self.generator.generate_umid(module_type, context_keywords)
            
            # Preserve original data with new ID and migration info
            migrated[new_umid] = {
                **module,
                'umid': new_umid,
                'migrated_from': old_key,
                'migration_timestamp': int(time.time())
            }
        
        return migrated
    
    def _extract_keywords_from_module(self, module: Dict, old_key: str) -> List[str]:
        """Extract meaningful keywords from module for context hash"""
        keywords = []
        
        # Try to get keywords from module data
        if isinstance(module.get('data'), dict):
            data = module['data']
            # Look for common fields
            if 'title' in data:
                keywords.extend(data['title'].split())
            if 'name' in data:
                keywords.extend(data['name'].split())
            if 'tags' in data and isinstance(data['tags'], list):
                keywords.extend(data['tags'])
        
        # If no keywords found, use parts of old key
        if not keywords:
            # Remove common prefixes and suffixes
            clean_key = old_key.replace('List', '').replace('Planner', '').replace('Calendar', '')
            clean_key = re.sub(r'[^a-zA-Z\s]', ' ', clean_key)
            keywords = [word.lower() for word in clean_key.split() if len(word) > 2]
        
        # Ensure we have at least one keyword
        if not keywords:
            keywords = ['module']
        
        return keywords[:5]  # Limit to 5 keywords for reasonable hash

def demo_umid_generation():
    """Demonstrate UMID generation capabilities"""
    print("=" * 60)
    print("Universal Module Identifier (UMID) Generation Demo")
    print("=" * 60)
    
    # Create generators for different services
    gptoggle_gen = UMIDGenerator('gptoggle')
    chatgpt_gen = UMIDGenerator('chatgpt')
    notion_gen = UMIDGenerator('notion')
    custom_gen = UMIDGenerator('my-custom-app')
    
    # Generate various UMIDs
    examples = [
        (gptoggle_gen, 'list', ['shopping', 'groceries', 'weekly']),
        (gptoggle_gen, 'planner', ['birthday', 'party', 'alice']),
        (chatgpt_gen, 'interest', ['python', 'programming', 'learning']),
        (notion_gen, 'tracker', ['habit', 'exercise', 'daily']),
        (custom_gen, 'goal', ['career', 'promotion', 'manager']),
        (gptoggle_gen, 'calendar', ['meeting', 'standup', 'team'])
    ]
    
    print("\n📋 Generated UMIDs:")
    for generator, module_type, keywords in examples:
        umid = generator.generate_umid(module_type, keywords)
        print(f"   {umid}")
        
        # Parse and display components
        parsed = UMIDParser.parse(umid)
        if parsed:
            print(f"      → Service: {parsed['service']}")
            print(f"      → Type: {parsed['moduleType']}")
            print(f"      → Context: {parsed['contextHash']}")
            print(f"      → Created: {parsed['createdAt']}")
            print()
    
    # Demonstrate validation
    print("🔍 Validation Examples:")
    valid_umid = gptoggle_gen.generate_umid('list', ['test'])
    invalid_umid = "invalid.format.here"
    
    print(f"   Valid: {UMIDParser.validate(valid_umid)} - {valid_umid}")
    print(f"   Invalid: {UMIDParser.validate(invalid_umid)} - {invalid_umid}")
    
    # Demonstrate batch generation
    print("\n⚡ Batch Generation:")
    batch_data = [
        {'type': 'list', 'keywords': ['homework', 'assignments']},
        {'type': 'tracker', 'keywords': ['water', 'intake', 'health']},
        {'type': 'goal', 'keywords': ['fitness', 'marathon', 'training']}
    ]
    
    batch_umids = gptoggle_gen.generate_batch_umids(batch_data)
    for i, umid in enumerate(batch_umids):
        print(f"   {i+1}. {umid}")
    
    print("\n✅ UMID Generation Demo Complete!")
    print("   Ready for adoption by any service or platform!")

if __name__ == "__main__":
    demo_umid_generation()