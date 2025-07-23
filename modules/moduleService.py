"""
Module Service - Python Implementation

Manages adaptive modules that track specialized areas of interest and intent per user.
These modules evolve as users interact with GPToggle-based platforms, enabling
intelligent support for recurring needs, personal goals, and contextual knowledge.

@version 2.0.0
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

MODULE_TYPES = ['list', 'planner', 'calendar', 'interest', 'tracker', 'goal']

@dataclass
class ModuleMetadata:
    createdAt: str
    lastUpdated: str
    lastAccessed: Optional[str] = None
    priority: Optional[int] = 5  # 1-10 scale
    tags: Optional[List[str]] = None
    archived: Optional[bool] = False

@dataclass
class Module:
    type: str
    data: Any
    metadata: ModuleMetadata

class ModuleService:
    """Service for managing adaptive user modules"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.ModuleService')
    
    def analyze_query_for_modules(self, query: str, user_profile: dict) -> Dict[str, Any]:
        """Analyze a query to determine if it relates to existing modules or should create a new one"""
        modules = user_profile.get('context', {}).get('modules', {})
        relevant_modules = []
        suggested_actions = []
        
        query_lower = query.lower()
        
        # Check for existing module relevance
        for key, module in modules.items():
            if self._is_query_relevant_to_module(query, key, module):
                relevant_modules.append(key)
                
                # Determine if this should be an update or access
                should_update = self._should_update_module(query, module)
                suggested_actions.append({
                    'action': 'update' if should_update else 'access',
                    'moduleKey': key,
                    'confidence': self._calculate_relevance_confidence(query, key, module)
                })
        
        # Check for new module creation opportunities
        new_module_opportunities = self._detect_new_module_opportunities(query)
        suggested_actions.extend(new_module_opportunities)
        
        return {
            'relevantModules': relevant_modules,
            'suggestedActions': suggested_actions
        }
    
    def create_module(self, user_profile: dict, module_key: str, module_type: str, 
                     initial_data: Any, context: Optional[Dict] = None) -> Module:
        """Create a new module based on query analysis"""
        now = datetime.now().isoformat()
        
        new_module = Module(
            type=module_type,
            data=self._initialize_module_data(module_type, initial_data),
            metadata=ModuleMetadata(
                createdAt=now,
                lastUpdated=now,
                lastAccessed=now,
                priority=5,
                tags=self._extract_tags_from_context(context),
                archived=False
            )
        )
        
        # Initialize modules object if it doesn't exist
        if 'context' not in user_profile:
            user_profile['context'] = {}
        if 'modules' not in user_profile['context']:
            user_profile['context']['modules'] = {}
        
        user_profile['context']['modules'][module_key] = asdict(new_module)
        
        self.logger.debug(f"Created new {module_type} module: {module_key}")
        return new_module
    
    def update_module(self, user_profile: dict, module_key: str, 
                     update_data: Any, context: Optional[Dict] = None) -> Optional[Module]:
        """Update an existing module with new information"""
        modules = user_profile.get('context', {}).get('modules', {})
        existing_module = modules.get(module_key)
        
        if not existing_module:
            self.logger.warning(f"Module {module_key} not found for update")
            return None
        
        updated_module = self._apply_module_update(existing_module, update_data, context)
        modules[module_key] = updated_module
        
        self.logger.debug(f"Updated module: {module_key}")
        return Module(**updated_module)
    
    def cleanup_stale_modules(self, user_profile: dict) -> Dict[str, List[str]]:
        """Remove or archive old modules based on aging rules"""
        modules = user_profile.get('context', {}).get('modules', {})
        archived = []
        removed = []
        now = datetime.now()
        
        for key, module in list(modules.items()):
            last_accessed = datetime.fromisoformat(
                module.get('metadata', {}).get('lastAccessed') or 
                module.get('metadata', {}).get('lastUpdated', now.isoformat())
            )
            days_since_access = (now - last_accessed).days
            
            # Archive modules not accessed in 30 days
            if days_since_access > 30 and not module.get('metadata', {}).get('archived'):
                module['metadata']['archived'] = True
                archived.append(key)
            
            # Remove archived modules not accessed in 90 days
            if days_since_access > 90 and module.get('metadata', {}).get('archived'):
                del modules[key]
                removed.append(key)
        
        return {'archived': archived, 'removed': removed}
    
    def get_user_modules_summary(self, user_profile: dict) -> Dict[str, Any]:
        """Get a summary of all user modules for system awareness"""
        modules = user_profile.get('context', {}).get('modules', {})
        modules_by_type = {mod_type: 0 for mod_type in MODULE_TYPES}
        active_modules = []
        recently_updated = []
        
        for key, module in modules.items():
            if not module.get('metadata', {}).get('archived'):
                mod_type = module.get('type')
                if mod_type in modules_by_type:
                    modules_by_type[mod_type] += 1
                
                active_modules.append({
                    'key': key,
                    'type': mod_type,
                    'priority': module.get('metadata', {}).get('priority', 5),
                    'lastAccessed': module.get('metadata', {}).get('lastAccessed') or 
                                  module.get('metadata', {}).get('lastUpdated')
                })
                
                # Consider recently updated if within last 7 days
                last_updated = datetime.fromisoformat(module.get('metadata', {}).get('lastUpdated'))
                days_since_update = (datetime.now() - last_updated).days
                if days_since_update <= 7:
                    recently_updated.append({
                        'key': key,
                        'type': mod_type,
                        'lastUpdated': module.get('metadata', {}).get('lastUpdated')
                    })
        
        # Sort by priority and recent access
        active_modules.sort(key=lambda x: (
            -x['priority'], 
            -(datetime.fromisoformat(x['lastAccessed']).timestamp() if x['lastAccessed'] else 0)
        ))
        
        recently_updated.sort(key=lambda x: -datetime.fromisoformat(x['lastUpdated']).timestamp())
        
        return {
            'totalModules': len([m for m in modules.values() if not m.get('metadata', {}).get('archived')]),
            'modulesByType': modules_by_type,
            'activeModules': active_modules[:10],  # Top 10 most relevant
            'recentlyUpdated': recently_updated[:5]  # Most recent 5
        }
    
    def _is_query_relevant_to_module(self, query: str, module_key: str, module: dict) -> bool:
        """Check if a query is relevant to an existing module"""
        query_lower = query.lower()
        key_lower = module_key.lower()
        
        # Check if module key is mentioned
        if key_lower in query_lower:
            return True
        
        # Check module-specific relevance
        module_type = module.get('type')
        if module_type == 'list':
            return self._is_query_relevant_to_list(query_lower, module)
        elif module_type == 'planner':
            return self._is_query_relevant_to_planner(query_lower, module)
        elif module_type == 'calendar':
            return self._is_query_relevant_to_calendar(query_lower, module)
        elif module_type == 'interest':
            return self._is_query_relevant_to_interest(query_lower, module)
        elif module_type == 'tracker':
            return self._is_query_relevant_to_tracker(query_lower, module)
        elif module_type == 'goal':
            return self._is_query_relevant_to_goal(query_lower, module)
        
        return False
    
    def _is_query_relevant_to_list(self, query: str, module: dict) -> bool:
        list_keywords = ['add', 'remove', 'list', 'items', 'shopping', 'grocery', 'todo']
        data = module.get('data', [])
        return (any(keyword in query for keyword in list_keywords) or
                any(item.lower() in query for item in data if isinstance(item, str)))
    
    def _is_query_relevant_to_planner(self, query: str, module: dict) -> bool:
        planner_keywords = ['party', 'event', 'plan', 'guest', 'invite', 'celebration']
        data = module.get('data', {})
        guests = data.get('guests', [])
        return (any(keyword in query for keyword in planner_keywords) or
                any(guest.lower() in query for guest in guests if isinstance(guest, str)))
    
    def _is_query_relevant_to_calendar(self, query: str, module: dict) -> bool:
        calendar_keywords = ['schedule', 'calendar', 'appointment', 'meeting', 'date']
        data = module.get('data', {})
        return (any(keyword in query for keyword in calendar_keywords) or
                any(event.lower() in query for event in data.values() if isinstance(event, str)))
    
    def _is_query_relevant_to_interest(self, query: str, module: dict) -> bool:
        data = module.get('data', {})
        keywords = data.get('keywords', [])
        related_topics = data.get('relatedTopics', [])
        return (any(keyword.lower() in query for keyword in keywords) or
                any(topic.lower() in query for topic in related_topics))
    
    def _is_query_relevant_to_tracker(self, query: str, module: dict) -> bool:
        tracker_keywords = ['track', 'progress', 'goal', 'target', 'metric']
        data = module.get('data', {})
        metric = data.get('metric', '')
        return (any(keyword in query for keyword in tracker_keywords) or
                metric.lower() in query)
    
    def _is_query_relevant_to_goal(self, query: str, module: dict) -> bool:
        goal_keywords = ['goal', 'achieve', 'progress', 'milestone', 'target']
        data = module.get('data', {})
        title = data.get('title', '')
        return (any(keyword in query for keyword in goal_keywords) or
                title.lower() in query)
    
    def _should_update_module(self, query: str, module: dict) -> bool:
        update_keywords = ['add', 'remove', 'update', 'change', 'modify', 'delete', 'complete']
        return any(keyword in query.lower() for keyword in update_keywords)
    
    def _calculate_relevance_confidence(self, query: str, module_key: str, module: dict) -> float:
        confidence = 0.0
        
        # Base confidence for key mention
        if module_key.lower() in query.lower():
            confidence += 0.8
        
        # Type-specific confidence boosters
        module_type = module.get('type')
        if module_type == 'list':
            if any(kw in query.lower() for kw in ['add', 'remove', 'list']):
                confidence += 0.6
        elif module_type == 'planner':
            if any(kw in query.lower() for kw in ['party', 'event', 'plan']):
                confidence += 0.6
        
        return min(confidence, 1.0)
    
    def _detect_new_module_opportunities(self, query: str) -> List[Dict[str, Any]]:
        opportunities = []
        query_lower = query.lower()
        
        # List detection
        if any(phrase in query_lower for phrase in ['shopping list', 'grocery list', 'todo list', 'need to buy']):
            opportunities.append({'action': 'create', 'moduleType': 'list', 'confidence': 0.8})
        
        # Planner detection
        if any(phrase in query_lower for phrase in ['party', 'birthday', 'celebration', 'event planning']):
            opportunities.append({'action': 'create', 'moduleType': 'planner', 'confidence': 0.7})
        
        # Calendar detection
        if any(phrase in query_lower for phrase in ['schedule', 'calendar', 'appointments', 'meetings']):
            opportunities.append({'action': 'create', 'moduleType': 'calendar', 'confidence': 0.6})
        
        # Interest detection
        if any(phrase in query_lower for phrase in ['interested in', 'learning about', 'studying', 'fascinated by']):
            opportunities.append({'action': 'create', 'moduleType': 'interest', 'confidence': 0.5})
        
        return opportunities
    
    def _initialize_module_data(self, module_type: str, initial_data: Any) -> Any:
        if module_type == 'list':
            return initial_data if isinstance(initial_data, list) else []
        elif module_type == 'planner':
            default = {'date': None, 'guests': [], 'tasks': [], 'status': 'planning'}
            return {**default, **(initial_data if isinstance(initial_data, dict) else {})}
        elif module_type == 'calendar':
            return initial_data if isinstance(initial_data, dict) else {}
        elif module_type == 'interest':
            default = {'keywords': [], 'engagementLevel': 5, 'relatedTopics': []}
            return {**default, **(initial_data if isinstance(initial_data, dict) else {})}
        elif module_type == 'tracker':
            default = {'metric': 'unknown', 'history': []}
            return {**default, **(initial_data if isinstance(initial_data, dict) else {})}
        elif module_type == 'goal':
            default = {'title': 'New Goal', 'progress': 0, 'milestones': []}
            return {**default, **(initial_data if isinstance(initial_data, dict) else {})}
        else:
            return initial_data or {}
    
    def _apply_module_update(self, module: dict, update_data: Any, context: Optional[Dict] = None) -> dict:
        updated_module = module.copy()
        now = datetime.now().isoformat()
        
        if 'metadata' not in updated_module:
            updated_module['metadata'] = {}
        
        updated_module['metadata'].update({
            'lastUpdated': now,
            'lastAccessed': now
        })
        
        module_type = module.get('type')
        if module_type == 'list':
            updated_module['data'] = self._update_list_data(module.get('data', []), update_data, context)
        elif module_type == 'planner':
            updated_module['data'] = {**module.get('data', {}), **update_data}
        elif module_type == 'calendar':
            updated_module['data'] = {**module.get('data', {}), **update_data}
        elif module_type == 'interest':
            updated_module['data'] = self._update_interest_data(module.get('data', {}), update_data, context)
        elif module_type == 'tracker':
            updated_module['data'] = self._update_tracker_data(module.get('data', {}), update_data, context)
        elif module_type == 'goal':
            updated_module['data'] = self._update_goal_data(module.get('data', {}), update_data, context)
        
        return updated_module
    
    def _update_list_data(self, current_data: List[str], update_data: Any, context: Optional[Dict] = None) -> List[str]:
        query = context.get('query', '') if context else ''
        query_lower = query.lower()
        
        if 'add' in query_lower or 'include' in query_lower:
            if isinstance(update_data, list):
                return list(set(current_data + update_data))
            elif isinstance(update_data, str):
                return list(set(current_data + [update_data]))
        elif 'remove' in query_lower or 'delete' in query_lower:
            if isinstance(update_data, list):
                return [item for item in current_data if item not in update_data]
            elif isinstance(update_data, str):
                return [item for item in current_data if item != update_data]
        
        # Default: replace if list, add if string
        if isinstance(update_data, list):
            return update_data
        elif isinstance(update_data, str):
            return list(set(current_data + [update_data]))
        
        return current_data
    
    def _update_interest_data(self, current_data: dict, update_data: dict, context: Optional[Dict] = None) -> dict:
        updated = current_data.copy()
        
        if 'keywords' in update_data:
            existing_keywords = updated.get('keywords', [])
            updated['keywords'] = list(set(existing_keywords + update_data['keywords']))
        
        if 'engagementLevel' in update_data:
            updated['engagementLevel'] = update_data['engagementLevel']
        
        if context and context.get('query'):
            updated['lastEngagement'] = datetime.now().isoformat()
        
        return updated
    
    def _update_tracker_data(self, current_data: dict, update_data: dict, context: Optional[Dict] = None) -> dict:
        updated = current_data.copy()
        
        if 'currentValue' in update_data:
            if 'history' not in updated:
                updated['history'] = []
            updated['history'].append({
                'date': datetime.now().isoformat(),
                'value': update_data['currentValue'],
                'notes': context.get('query') if context else None
            })
            updated['currentValue'] = update_data['currentValue']
        
        return {**updated, **update_data}
    
    def _update_goal_data(self, current_data: dict, update_data: dict, context: Optional[Dict] = None) -> dict:
        updated = current_data.copy()
        
        if 'milestones' in update_data:
            updated['milestones'] = update_data['milestones']
        
        if 'progress' in update_data:
            updated['progress'] = max(0, min(100, update_data['progress']))
        
        return {**updated, **update_data}
    
    def _extract_tags_from_context(self, context: Optional[Dict] = None) -> List[str]:
        if not context or 'query' not in context:
            return []
        
        tags = []
        query = context['query'].lower()
        
        # Extract common tags based on query content
        if 'urgent' in query or 'important' in query:
            tags.append('urgent')
        if 'work' in query or 'job' in query:
            tags.append('work')
        if 'personal' in query or 'family' in query:
            tags.append('personal')
        if 'health' in query or 'fitness' in query:
            tags.append('health')
        
        return tags