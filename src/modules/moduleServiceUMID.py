#!/usr/bin/env python3
"""
GPToggle Modular Adaptive Intelligence - Enhanced Module Service with UMID

This enhanced version of the module service integrates Universal Module Identifiers (UMID)
for cross-platform module identification and interoperability. All modules now receive
globally unique identifiers that can be adopted by any service or platform.

Features:
- Universal unique module identification
- Cross-platform module portability
- Service-agnostic module schema
- Automatic UMID generation and management
- Migration support from legacy module keys

@version 2.0.0
"""

import re
import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

# Import UMID generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from umidGenerator import UMIDGenerator, UMIDParser, UMIDMigrator

class EnhancedModuleService:
    """Enhanced Module Service with Universal Module Identifier support"""
    
    def __init__(self, service_id: str = 'gptoggle'):
        """
        Initialize the enhanced module service
        
        Args:
            service_id: Identifier for this service (e.g., 'gptoggle', 'chatgpt', 'notion')
        """
        self.service_id = service_id
        self.umid_generator = UMIDGenerator(service_id)
        self.umid_parser = UMIDParser()
    
    def create_module_with_umid(self, module_type: str, context_keywords: List[str], 
                               initial_data: Any, priority: int = 5) -> Dict[str, Any]:
        """
        Create a new module with UMID
        
        Args:
            module_type: Type of module (list, planner, calendar, interest, tracker, goal)
            context_keywords: Keywords describing the module context
            initial_data: Initial data for the module
            priority: Priority level (1-10)
            
        Returns:
            Dictionary containing the new module with UMID
        """
        # Generate UMID
        umid = self.umid_generator.generate_umid(module_type, context_keywords)
        
        # Create module structure
        module = {
            'umid': umid,
            'type': module_type,
            'data': initial_data,
            'metadata': {
                'createdAt': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat(),
                'lastAccessed': datetime.now().isoformat(),
                'priority': priority,
                'tags': context_keywords[:3],  # Use first 3 keywords as tags
                'archived': False,
                'contextKeywords': context_keywords
            }
        }
        
        return {umid: module}
    
    def update_module_by_umid(self, user_profile: Dict, umid: str, 
                             new_data: Any, query_context: str = '') -> bool:
        """
        Update an existing module by its UMID
        
        Args:
            user_profile: User profile containing modules
            umid: Universal Module Identifier
            new_data: New data to update the module with
            query_context: Context of the query that triggered the update
            
        Returns:
            True if update successful, False otherwise
        """
        modules = user_profile.get('context', {}).get('modules', {})
        
        if umid not in modules:
            return False
        
        module = modules[umid]
        
        # Update based on module type
        if module['type'] == 'list':
            module['data'] = self._update_list_data(module['data'], new_data, query_context)
        elif module['type'] == 'planner':
            module['data'] = self._update_planner_data(module['data'], new_data, query_context)
        elif module['type'] == 'calendar':
            module['data'] = self._update_calendar_data(module['data'], new_data, query_context)
        elif module['type'] == 'interest':
            module['data'] = self._update_interest_data(module['data'], new_data, query_context)
        elif module['type'] == 'tracker':
            module['data'] = self._update_tracker_data(module['data'], new_data, query_context)
        elif module['type'] == 'goal':
            module['data'] = self._update_goal_data(module['data'], new_data, query_context)
        
        # Update metadata
        module['metadata']['lastUpdated'] = datetime.now().isoformat()
        module['metadata']['lastAccessed'] = datetime.now().isoformat()
        
        return True
    
    def migrate_legacy_modules(self, user_profile: Dict) -> Dict[str, Any]:
        """
        Migrate existing modules without UMIDs to the new UMID system
        
        Args:
            user_profile: User profile with existing modules
            
        Returns:
            Migration results with statistics
        """
        modules = user_profile.get('context', {}).get('modules', {})
        migrated_modules = {}
        migration_stats = {
            'total_modules': len(modules),
            'migrated': 0,
            'skipped': 0,
            'mapping': {}  # old_key -> new_umid mapping
        }
        
        for old_key, module in modules.items():
            # Skip if already has UMID
            if 'umid' in module and self.umid_parser.validate(module['umid']):
                migrated_modules[module['umid']] = module
                migration_stats['skipped'] += 1
                continue
            
            # Extract context keywords for UMID generation
            context_keywords = self._extract_context_keywords(old_key, module)
            module_type = module.get('type', 'custom')
            
            # Generate new UMID
            umid = self.umid_generator.generate_umid(module_type, context_keywords)
            
            # Add UMID to module
            module['umid'] = umid
            module['metadata'] = module.get('metadata', {})
            module['metadata']['migratedFrom'] = old_key
            module['metadata']['migrationTimestamp'] = datetime.now().isoformat()
            
            migrated_modules[umid] = module
            migration_stats['migrated'] += 1
            migration_stats['mapping'][old_key] = umid
        
        # Update user profile
        user_profile['context']['modules'] = migrated_modules
        
        return migration_stats
    
    def analyze_query_for_modules_umid(self, query: str, user_profile: Dict) -> Dict[str, Any]:
        """
        Enhanced query analysis with UMID support
        
        Args:
            query: User query to analyze
            user_profile: User profile with modules
            
        Returns:
            Analysis results with UMID-based module actions
        """
        modules = user_profile.get('context', {}).get('modules', {})
        relevant_modules = []
        module_actions = []
        
        query_lower = query.lower()
        
        # Check existing modules for relevance
        for umid, module in modules.items():
            relevance_score = self._calculate_module_relevance(query, module)
            
            if relevance_score > 0.3:  # Relevance threshold
                relevant_modules.append(umid)
                
                # Determine action type
                action_type = self._determine_action_type(query, module)
                module_actions.append({
                    'action': action_type,
                    'umid': umid,
                    'moduleType': module['type'],
                    'confidence': relevance_score,
                    'success': True
                })
        
        # Check for new module creation opportunities
        new_module_opportunities = self._detect_new_module_opportunities_umid(query)
        
        for opportunity in new_module_opportunities:
            # Create new module
            context_keywords = opportunity['keywords']
            module_type = opportunity['type']
            initial_data = opportunity['data']
            
            new_module = self.create_module_with_umid(
                module_type, context_keywords, initial_data
            )
            
            umid = list(new_module.keys())[0]
            
            # Add to user profile
            if 'context' not in user_profile:
                user_profile['context'] = {}
            if 'modules' not in user_profile['context']:
                user_profile['context']['modules'] = {}
            
            user_profile['context']['modules'].update(new_module)
            
            module_actions.append({
                'action': 'create',
                'umid': umid,
                'moduleType': module_type,
                'confidence': opportunity['confidence'],
                'success': True
            })
        
        return {
            'relevantModules': relevant_modules,
            'moduleActions': module_actions
        }
    
    def get_modules_by_service(self, user_profile: Dict, service_id: str) -> Dict[str, Any]:
        """Get all modules created by a specific service"""
        modules = user_profile.get('context', {}).get('modules', {})
        service_modules = {}
        
        for umid, module in modules.items():
            parsed = self.umid_parser.parse(umid)
            if parsed and parsed['service'] == service_id:
                service_modules[umid] = module
        
        return service_modules
    
    def get_modules_by_type(self, user_profile: Dict, module_type: str) -> Dict[str, Any]:
        """Get all modules of a specific type"""
        modules = user_profile.get('context', {}).get('modules', {})
        type_modules = {}
        
        for umid, module in modules.items():
            if module.get('type') == module_type:
                type_modules[umid] = module
        
        return type_modules
    
    def cleanup_stale_modules_umid(self, user_profile: Dict, 
                                   archive_days: int = 30, 
                                   remove_days: int = 90) -> Dict[str, Any]:
        """
        Enhanced cleanup with UMID tracking
        
        Args:
            user_profile: User profile with modules
            archive_days: Days before archiving inactive modules
            remove_days: Days before removing archived modules
            
        Returns:
            Cleanup statistics with UMIDs
        """
        modules = user_profile.get('context', {}).get('modules', {})
        now = datetime.now()
        
        archived_umids = []
        removed_umids = []
        
        for umid, module in list(modules.items()):
            metadata = module.get('metadata', {})
            last_accessed = metadata.get('lastAccessed')
            
            if not last_accessed:
                continue
            
            try:
                last_access_date = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
            except:
                continue
            
            days_since_access = (now - last_access_date).days
            
            # Archive logic
            if not metadata.get('archived', False) and days_since_access >= archive_days:
                priority = metadata.get('priority', 5)
                if priority < 7:  # Don't archive high priority modules
                    metadata['archived'] = True
                    metadata['archivedAt'] = now.isoformat()
                    archived_umids.append(umid)
            
            # Remove logic
            elif metadata.get('archived', False) and days_since_access >= remove_days:
                del modules[umid]
                removed_umids.append(umid)
        
        return {
            'archived': archived_umids,
            'removed': removed_umids,
            'total_remaining': len(modules)
        }
    
    def export_modules_for_service(self, user_profile: Dict, 
                                  target_service: str) -> Dict[str, Any]:
        """
        Export modules in a format suitable for another service
        
        Args:
            user_profile: User profile with modules
            target_service: Target service identifier
            
        Returns:
            Exportable module data with service attribution
        """
        modules = user_profile.get('context', {}).get('modules', {})
        exported_data = {
            'source_service': self.service_id,
            'target_service': target_service,
            'export_timestamp': datetime.now().isoformat(),
            'modules': {}
        }
        
        for umid, module in modules.items():
            # Parse UMID to verify it's from our service
            parsed = self.umid_parser.parse(umid)
            if not parsed or parsed['service'] != self.service_id:
                continue
            
            # Create portable module format
            exported_data['modules'][umid] = {
                'original_umid': umid,
                'type': module['type'],
                'data': module['data'],
                'metadata': {
                    **module['metadata'],
                    'exported_from': self.service_id,
                    'export_timestamp': datetime.now().isoformat()
                },
                'context_keywords': module['metadata'].get('contextKeywords', [])
            }
        
        return exported_data
    
    # Helper methods
    def _extract_context_keywords(self, old_key: str, module: Dict) -> List[str]:
        """Extract meaningful keywords from existing module for UMID generation"""
        keywords = []
        
        # Try module data first
        if 'data' in module and isinstance(module['data'], dict):
            data = module['data']
            for field in ['title', 'name', 'description']:
                if field in data and isinstance(data[field], str):
                    keywords.extend(data[field].split()[:3])
        
        # Try metadata tags
        metadata = module.get('metadata', {})
        if 'tags' in metadata and isinstance(metadata['tags'], list):
            keywords.extend(metadata['tags'])
        
        # Fall back to old key
        if not keywords:
            clean_key = re.sub(r'[^a-zA-Z\s]', ' ', old_key)
            keywords = [word.lower() for word in clean_key.split() if len(word) > 2][:3]
        
        return keywords or ['module']
    
    def _calculate_module_relevance(self, query: str, module: Dict) -> float:
        """Calculate how relevant a query is to a specific module"""
        query_lower = query.lower()
        relevance_score = 0.0
        
        # Check context keywords
        context_keywords = module.get('metadata', {}).get('contextKeywords', [])
        for keyword in context_keywords:
            if keyword.lower() in query_lower:
                relevance_score += 0.3
        
        # Check module data
        data = module.get('data', {})
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, str) and value.lower() in query_lower:
                    relevance_score += 0.2
        
        # Check tags
        tags = module.get('metadata', {}).get('tags', [])
        for tag in tags:
            if tag.lower() in query_lower:
                relevance_score += 0.2
        
        return min(relevance_score, 1.0)
    
    def _determine_action_type(self, query: str, module: Dict) -> str:
        """Determine what action should be taken on a module based on query"""
        query_lower = query.lower()
        
        # Update indicators
        update_keywords = ['add', 'update', 'change', 'modify', 'include', 'remove', 'delete']
        if any(keyword in query_lower for keyword in update_keywords):
            return 'update'
        
        # View/access indicators
        view_keywords = ['show', 'display', 'list', 'what', 'tell', 'view']
        if any(keyword in query_lower for keyword in view_keywords):
            return 'view'
        
        return 'access'
    
    def _detect_new_module_opportunities_umid(self, query: str) -> List[Dict[str, Any]]:
        """Detect opportunities to create new modules from query"""
        opportunities = []
        query_lower = query.lower()
        
        # Shopping list detection
        if any(indicator in query_lower for indicator in ['buy', 'shopping', 'purchase', 'need to get']):
            items = self._extract_list_items(query)
            if items:
                opportunities.append({
                    'type': 'list',
                    'keywords': ['shopping', 'groceries'] + items[:2],
                    'data': items,
                    'confidence': 0.8
                })
        
        # Party planning detection
        if any(indicator in query_lower for indicator in ['party', 'celebration', 'event', 'planning']):
            planning_data = self._extract_planning_data(query)
            opportunities.append({
                'type': 'planner',
                'keywords': ['party', 'planning'] + list(planning_data.keys())[:2],
                'data': planning_data,
                'confidence': 0.7
            })
        
        # Interest detection
        if any(indicator in query_lower for indicator in ['interested', 'learning', 'fascinated', 'studying']):
            interest_data = self._extract_interest_data(query)
            opportunities.append({
                'type': 'interest',
                'keywords': interest_data.get('keywords', ['learning'])[:3],
                'data': interest_data,
                'confidence': 0.6
            })
        
        return opportunities
    
    def _extract_list_items(self, query: str) -> List[str]:
        """Extract list items from query"""
        # Simple extraction - look for comma-separated items or common patterns
        query_clean = re.sub(r'(buy|need|get|purchase)', '', query.lower()).strip()
        
        # Split by common separators
        items = []
        for separator in [',', ' and ', '&']:
            if separator in query_clean:
                parts = query_clean.split(separator)
                items.extend([item.strip() for item in parts if item.strip()])
                break
        
        if not items:
            # Look for individual words that might be items
            words = query_clean.split()
            common_items = ['milk', 'eggs', 'bread', 'butter', 'cheese', 'apples', 'bananas']
            items = [word for word in words if word in common_items]
        
        return items[:10]  # Limit to 10 items
    
    def _extract_planning_data(self, query: str) -> Dict[str, Any]:
        """Extract planning data from query"""
        planning_data = {
            'date': '',
            'guests': [],
            'tasks': [],
            'status': 'planning'
        }
        
        # Extract date patterns
        date_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'(today|tomorrow|next week|this weekend)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, query.lower())
            if match:
                planning_data['date'] = match.group(0)
                break
        
        # Extract names (simple pattern)
        name_pattern = r'\b([A-Z][a-z]+)\b'
        names = re.findall(name_pattern, query)
        planning_data['guests'] = names[:5]  # Limit to 5 guests
        
        return planning_data
    
    def _extract_interest_data(self, query: str) -> Dict[str, Any]:
        """Extract interest data from query"""
        # Extract keywords and topics
        query_words = query.lower().split()
        
        # Filter out common words
        stop_words = {'i', 'am', 'is', 'the', 'in', 'to', 'and', 'or', 'but', 'about', 'by', 'for'}
        keywords = [word for word in query_words if word not in stop_words and len(word) > 3]
        
        return {
            'keywords': keywords[:5],
            'engagementLevel': 5,
            'relatedTopics': []
        }
    
    # Data update methods (simplified versions)
    def _update_list_data(self, current_data: List, new_data: Any, context: str) -> List:
        """Update list module data"""
        if isinstance(new_data, list):
            # Merge lists, avoiding duplicates
            combined = list(set(current_data + new_data))
            return combined
        elif isinstance(new_data, str):
            if new_data not in current_data:
                current_data.append(new_data)
        return current_data
    
    def _update_planner_data(self, current_data: Dict, new_data: Any, context: str) -> Dict:
        """Update planner module data"""
        if isinstance(new_data, dict):
            current_data.update(new_data)
        return current_data
    
    def _update_calendar_data(self, current_data: Dict, new_data: Any, context: str) -> Dict:
        """Update calendar module data"""
        if isinstance(new_data, dict):
            current_data.update(new_data)
        return current_data
    
    def _update_interest_data(self, current_data: Dict, new_data: Any, context: str) -> Dict:
        """Update interest module data"""
        if isinstance(new_data, dict) and 'keywords' in new_data:
            existing_keywords = current_data.get('keywords', [])
            new_keywords = new_data['keywords']
            current_data['keywords'] = list(set(existing_keywords + new_keywords))
        return current_data
    
    def _update_tracker_data(self, current_data: Dict, new_data: Any, context: str) -> Dict:
        """Update tracker module data"""
        if isinstance(new_data, dict):
            current_data.update(new_data)
        return current_data
    
    def _update_goal_data(self, current_data: Dict, new_data: Any, context: str) -> Dict:
        """Update goal module data"""
        if isinstance(new_data, dict):
            current_data.update(new_data)
        return current_data


def demo_umid_module_service():
    """Demonstrate the enhanced module service with UMID support"""
    print("=" * 60)
    print("Enhanced Module Service with UMID Demo")
    print("=" * 60)
    
    # Create service instance
    service = EnhancedModuleService('gptoggle')
    
    # Create sample user profile
    user_profile = {
        'userId': 'demo-user',
        'context': {
            'modules': {}
        }
    }
    
    # Demo 1: Create modules with UMID
    print("\n1. Creating modules with UMID:")
    
    # Shopping list
    shopping_module = service.create_module_with_umid(
        'list', 
        ['shopping', 'groceries', 'weekly'],
        ['milk', 'eggs', 'bread']
    )
    user_profile['context']['modules'].update(shopping_module)
    
    # Party planner
    party_module = service.create_module_with_umid(
        'planner',
        ['birthday', 'party', 'alice'],
        {'date': 'March 15', 'guests': ['Alice', 'Bob'], 'tasks': ['book venue']}
    )
    user_profile['context']['modules'].update(party_module)
    
    for umid in list(user_profile['context']['modules'].keys()):
        parsed = service.umid_parser.parse(umid)
        print(f"   Created: {parsed['service']}.{parsed['moduleType']} - {umid}")
    
    # Demo 2: Query analysis with UMID
    print(f"\n2. Query analysis with UMID:")
    queries = [
        "Add toothpaste to my shopping list",
        "Invite Charlie to Alice's birthday party",
        "I'm interested in learning about machine learning"
    ]
    
    for query in queries:
        result = service.analyze_query_for_modules_umid(query, user_profile)
        print(f"   Query: '{query}'")
        print(f"   Actions: {len(result['moduleActions'])}")
        for action in result['moduleActions']:
            print(f"     → {action['action']} {action['moduleType']} ({action['umid'][:20]}...)")
    
    # Demo 3: Service filtering
    print(f"\n3. Service-specific module filtering:")
    gptoggle_modules = service.get_modules_by_service(user_profile, 'gptoggle')
    print(f"   GPToggle modules: {len(gptoggle_modules)}")
    
    list_modules = service.get_modules_by_type(user_profile, 'list')
    print(f"   List modules: {len(list_modules)}")
    
    # Demo 4: Export capability
    print(f"\n4. Module export for interoperability:")
    export_data = service.export_modules_for_service(user_profile, 'chatgpt')
    print(f"   Exported {len(export_data['modules'])} modules for ChatGPT")
    print(f"   Export timestamp: {export_data['export_timestamp'][:19]}")
    
    print(f"\n✅ Enhanced Module Service Demo Complete!")
    print(f"   All modules now have universal unique identifiers")
    print(f"   Ready for cross-platform adoption and interoperability")


if __name__ == "__main__":
    demo_umid_module_service()