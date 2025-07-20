"""
GPToggle v2.0 - Model-Agnostic Implementation with Contextualized Intelligence

This module implements a model-agnostic version of GPToggle that features:
- Dynamic model registry
- Capability-based model selection
- Rich attribute scoring system
- Provider-agnostic interface
- Universal user profiles for personalization
- Query classification and contextual enhancement
- Adaptive learning from user interactions

This implementation allows for:
- Runtime registration of models and providers
- Detailed model metadata and capabilities
- Sophisticated scoring and selection algorithms
- Clear explanation of model selection
- Contextualized AI interactions based on user profiles
- Cross-service compatible user profiling

Usage:
    from gptoggle_v2 import GPToggle, UserProfile
    
    # Initialize with API keys
    gptoggle = GPToggle(api_keys={
        "openai": "your-openai-key",
        "anthropic": "your-anthropic-key"
    })
    
    # Register models
    gptoggle.register_models(sample_models)
    
    # Create or load user profile
    user_profile = UserProfile.create_default("user-123")
    user_profile.expertise['domains'] = ['technology']
    
    # Get contextualized response
    response = gptoggle.get_response(
        "Create a Python function...", 
        user_profile=user_profile
    )
"""

import os
import sys
import re
import json
from typing import List, Dict, Any, Tuple, Callable, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """Universal User Profile for contextualized AI interactions"""
    userId: str
    communicationStyle: Dict[str, Any]
    expertise: Dict[str, Any] 
    preferences: Dict[str, Any]
    context: Dict[str, Any]
    serviceSpecific: Dict[str, Any]
    metadata: Dict[str, Any]
    
    @classmethod
    def create_default(cls, user_id: str):
        """Create a default universal user profile"""
        return cls(
            userId=user_id,
            communicationStyle={
                'tone': 'casual',
                'verbosity': 'moderate', 
                'language': 'en',
                'includeExplanations': True
            },
            expertise={
                'domains': [],
                'skillLevel': {},
                'interests': []
            },
            preferences={
                'prioritizeSpeed': False,
                'adaptivePersonalization': True,
                'contextualAwareness': True,
                'privacyLevel': 'standard'
            },
            context={
                'recentInteractions': [],
                'savedItems': [],
                'learningPatterns': {
                    'commonTopics': [],
                    'timePatterns': {},
                    'contextualPreferences': {}
                }
            },
            serviceSpecific={
                'gptoggle': {
                    'enabled': True,
                    'configuration': {'accessLevel': 'basic'},
                    'preferences': {}
                }
            },
            metadata={
                'createdAt': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat(),
                'version': '2.0.0',
                'services': ['gptoggle']
            }
        )
    
    def add_interaction(self, content: str, category: str = None, service: str = 'gptoggle'):
        """Add an interaction to user context"""
        interaction = {
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'service': service
        }
        
        self.context['recentInteractions'].insert(0, interaction)
        self.context['recentInteractions'] = self.context['recentInteractions'][:100]
        
        # Update learning patterns
        if category:
            common_topics = self.context['learningPatterns']['commonTopics']
            existing = next((t for t in common_topics if t['topic'] == category), None)
            
            if existing:
                existing['frequency'] += 1
                existing['lastSeen'] = datetime.now().isoformat()
            else:
                common_topics.append({
                    'topic': category,
                    'frequency': 1,
                    'lastSeen': datetime.now().isoformat()
                })
            
            # Sort by frequency and limit
            common_topics.sort(key=lambda x: x['frequency'], reverse=True)
            self.context['learningPatterns']['commonTopics'] = common_topics[:20]
        
        self.metadata['lastUpdated'] = datetime.now().isoformat()
    
    def update_profile_adaptively(self, query: str, query_type: str, model_used: str = None):
        """Adaptively update user profile based on interaction patterns"""
        timestamp = datetime.now().isoformat()
        
        # Add to recent queries (FIFO with max 10)
        if 'recentQueries' not in self.context:
            self.context['recentQueries'] = []
        self.context['recentQueries'].insert(0, {
            'query': query,
            'type': query_type,
            'timestamp': timestamp
        })
        self.context['recentQueries'] = self.context['recentQueries'][:10]
        
        # Update interaction history
        if 'interactionHistory' not in self.context:
            self.context['interactionHistory'] = {
                'queryTypes': {},
                'lastModelUsed': None,
                'lastInteraction': None
            }
        
        # Increment query type counter
        self.context['interactionHistory']['queryTypes'][query_type] = \
            self.context['interactionHistory']['queryTypes'].get(query_type, 0) + 1
        
        # Update last used model and interaction time
        if model_used:
            self.context['interactionHistory']['lastModelUsed'] = model_used
        self.context['interactionHistory']['lastInteraction'] = timestamp
        
        # Adaptive domain expertise detection
        self._update_domain_expertise(query)
        
        # Adaptive tone analysis
        self._update_communication_tone(query)
        
        # Update metadata
        self.metadata['lastUpdated'] = timestamp
    
    def _update_domain_expertise(self, query: str):
        """Update domain expertise based on query content"""
        query_lower = query.lower()
        
        # Domain keyword mapping
        domain_keywords = {
            'technology': ['code', 'programming', 'software', 'api', 'database', 'javascript', 'python', 'algorithm'],
            'business': ['contract', 'revenue', 'strategy', 'marketing', 'sales', 'finance', 'budget', 'roi'],
            'creative': ['design', 'art', 'story', 'creative', 'poem', 'music', 'melody', 'composition'],
            'education': ['learn', 'teach', 'study', 'lesson', 'tutorial', 'course', 'homework', 'assignment'],
            'science': ['research', 'experiment', 'data', 'analysis', 'hypothesis', 'theory', 'scientific'],
            'health': ['medical', 'health', 'nutrition', 'exercise', 'wellness', 'therapy', 'treatment'],
            'cooking': ['recipe', 'cook', 'ingredient', 'food', 'meal', 'kitchen', 'bake', 'prepare']
        }
        
        # Count domain matches
        for domain, keywords in domain_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in query_lower)
            if matches > 0:
                if domain not in self.expertise['domains']:
                    # Add new domain if multiple keywords detected
                    if matches >= 2:
                        self.expertise['domains'].append(domain)
                
                # Update skill level based on frequency
                current_level = self.expertise['skillLevel'].get(domain, 0)
                self.expertise['skillLevel'][domain] = min(current_level + matches, 10)
    
    def _update_communication_tone(self, query: str):
        """Adaptively update communication tone based on query style"""
        query_lower = query.lower()
        
        # Casual indicators
        casual_indicators = ['hey', 'hi', 'thanks', 'cool', 'awesome', 'lol', 'btw', 'gonna', 'wanna']
        casual_count = sum(1 for indicator in casual_indicators if indicator in query_lower)
        
        # Formal indicators  
        formal_indicators = ['please', 'would you', 'could you', 'kindly', 'respectfully', 'sincerely']
        formal_count = sum(1 for indicator in formal_indicators if indicator in query_lower)
        
        # Professional indicators
        professional_indicators = ['analyze', 'evaluate', 'assess', 'provide', 'demonstrate', 'implement']
        professional_count = sum(1 for indicator in professional_indicators if indicator in query_lower)
        
        # Adaptive tone adjustment
        total_interactions = sum(self.context.get('interactionHistory', {}).get('queryTypes', {}).values())
        if total_interactions >= 3:  # Only adjust after sufficient interactions
            if casual_count > formal_count + professional_count:
                self.communicationStyle['tone'] = 'casual'
            elif professional_count > casual_count:
                self.communicationStyle['tone'] = 'professional'
            elif formal_count > casual_count:
                self.communicationStyle['tone'] = 'formal'

class QueryClassifier:
    """Intelligent query classification system"""
    
    def __init__(self):
        self.patterns = {
            'code': {
                'keywords': ['code', 'program', 'function', 'debug', 'javascript', 'python', 'html', 'css', 'sql', 'api'],
                'phrases': ['write a function', 'debug this', 'how to code', 'programming help'],
            },
            'creative': {
                'keywords': ['write', 'create', 'imagine', 'story', 'poem', 'brainstorm', 'design', 'creative'],
                'phrases': ['write a story', 'create content', 'brainstorm ideas'],
            },
            'factual': {
                'keywords': ['what', 'when', 'where', 'who', 'how', 'explain', 'define', 'information', 'facts'],
                'phrases': ['what is', 'explain to me', 'tell me about'],
            },
            'analytical': {
                'keywords': ['analyze', 'compare', 'evaluate', 'assess', 'examine', 'review', 'study'],
                'phrases': ['compare and contrast', 'analyze this', 'evaluate the'],
            },
            'business': {
                'keywords': ['business', 'strategy', 'marketing', 'sales', 'profit', 'revenue', 'company'],
                'phrases': ['business plan', 'marketing strategy', 'increase sales'],
            },
            'educational': {
                'keywords': ['learn', 'teach', 'explain', 'lesson', 'tutorial', 'course', 'study'],
                'phrases': ['teach me', 'learn about', 'tutorial on'],
            }
        }
    
    def classify_query(self, query: str) -> Dict[str, Any]:
        """Classify a query and return type with confidence"""
        query_lower = query.lower()
        scores = {}
        
        for query_type, config in self.patterns.items():
            score = 0
            
            # Keyword matching
            keyword_matches = sum(1 for keyword in config['keywords'] if keyword in query_lower)
            score += keyword_matches * 2
            
            # Phrase matching  
            phrase_matches = sum(1 for phrase in config['phrases'] if phrase in query_lower)
            score += phrase_matches * 3
            
            scores[query_type] = score
        
        # Find best match
        best_type = max(scores.items(), key=lambda x: x[1])
        
        return {
            'queryType': best_type[0] if best_type[1] > 0 else 'general',
            'confidence': min(best_type[1] / 10, 1.0) if best_type[1] > 0 else 0.5,
            'scores': scores
        }

class ContextualEnhancer:
    """Contextual query enhancement system"""
    
    def enhance_query(self, query: str, query_type: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Enhance query based on context and user profile"""
        enhancements = []
        enhanced_query = query
        
        # Apply query type enhancement
        type_enhancement = self._get_type_enhancement(query_type)
        if type_enhancement:
            enhanced_query = f"{type_enhancement} {enhanced_query}"
            enhancements.append(f"Query type: {query_type}")
        
        # Apply communication style
        style = user_profile.communicationStyle
        if style['tone'] != 'casual':
            tone_instruction = self._get_tone_instruction(style['tone'])
            enhanced_query = f"{tone_instruction} {enhanced_query}"
            enhancements.append(f"Tone: {style['tone']}")
        
        if style['verbosity'] != 'moderate':
            verbosity_instruction = self._get_verbosity_instruction(style['verbosity'])
            enhanced_query = f"{verbosity_instruction} {enhanced_query}"
            enhancements.append(f"Verbosity: {style['verbosity']}")
        
        # Apply domain expertise
        if user_profile.expertise['domains']:
            expertise_context = f"Context: User has expertise in {', '.join(user_profile.expertise['domains'])}. "
            enhanced_query = expertise_context + enhanced_query
            enhancements.append('Domain expertise')
        
        # Apply recent context
        recent_topics = self._extract_recent_topics(user_profile.context['recentInteractions'])
        if recent_topics:
            topics_str = ', '.join([f"{topic[0]} ({topic[1]}x)" for topic in recent_topics])
            context_note = f"Recent discussion topics: {topics_str}. "
            enhanced_query = context_note + enhanced_query
            enhancements.append('Recent context')
        
        return {
            'enhanced': enhanced_query,
            'enhancements': enhancements,
            'original': query
        }
    
    def _get_type_enhancement(self, query_type: str) -> str:
        enhancements = {
            'code': 'You are a programming expert. Provide working code with best practices.',
            'creative': 'You are a creative assistant. Think imaginatively and provide original content.',
            'factual': 'Provide accurate, well-sourced factual information.',
            'analytical': 'Provide structured, logical analysis with clear reasoning.',
            'business': 'You are a business consultant. Provide practical, actionable advice.',
            'educational': 'You are a patient educator. Explain concepts clearly with examples.'
        }
        return enhancements.get(query_type, '')
    
    def _get_tone_instruction(self, tone: str) -> str:
        instructions = {
            'formal': 'Please respond in a professional, formal tone.',
            'friendly': 'Please respond in a warm, friendly manner.',
            'professional': 'Please respond professionally and concisely.',
            'witty': 'Please respond with appropriate wit and clever insights.',
            'empathetic': 'Please respond with empathy and understanding.'
        }
        return instructions.get(tone, '')
    
    def _get_verbosity_instruction(self, verbosity: str) -> str:
        instructions = {
            'concise': 'Please provide a brief, focused response.',
            'detailed': 'Please provide a comprehensive, detailed response with examples.',
            'comprehensive': 'Please provide an exhaustive response covering all aspects.'
        }
        return instructions.get(verbosity, '')
    
    def _extract_recent_topics(self, interactions: List[Dict]) -> List[Tuple[str, int]]:
        topic_counts = {}
        for interaction in interactions[:10]:
            if 'category' in interaction and interaction['category']:
                topic = interaction['category']
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]


class ModelRegistry:
    """
    Registry for storing and retrieving model information.
    """
    
    def __init__(self):
        """Initialize an empty model registry."""
        self.models = {}
    
    def register_model(self, model_info: Dict[str, Any]) -> 'ModelRegistry':
        """
        Register a model with its capabilities and attributes.
        
        Args:
            model_info: Dictionary containing model information
            
        Returns:
            Self for method chaining
        """
        provider = model_info.get("provider")
        model_id = model_info.get("model_id")
        
        if not provider or not model_id:
            raise ValueError("Model must have both provider and model_id attributes")
        
        model_key = f"{provider}:{model_id}"
        self.models[model_key] = model_info
        return self
    
    def register_models_from_list(self, models_list: List[Dict[str, Any]]) -> 'ModelRegistry':
        """
        Register multiple models at once from a list.
        
        Args:
            models_list: List of model information dictionaries
            
        Returns:
            Self for method chaining
        """
        for model in models_list:
            self.register_model(model)
        return self
    
    def get_all_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of all registered models.
        
        Returns:
            List of all model information dictionaries
        """
        return list(self.models.values())
    
    def get_models_by_tier(self, tier: str) -> List[Dict[str, Any]]:
        """
        Get models filtered by tier (e.g., "free", "standard").
        
        Args:
            tier: Tier to filter by
            
        Returns:
            List of models in the specified tier
        """
        return [
            model for model in self.get_all_models()
            if model.get("tiers") and tier in model.get("tiers", [])
        ]
    
    def get_models_by_provider(self, provider: str) -> List[Dict[str, Any]]:
        """
        Get models filtered by provider (e.g., "openai", "anthropic").
        
        Args:
            provider: Provider to filter by
            
        Returns:
            List of models from the specified provider
        """
        return [
            model for model in self.get_all_models()
            if model.get("provider") == provider
        ]
    
    def get_models_by_capability(self, capability: str) -> List[Dict[str, Any]]:
        """
        Get models filtered by capability (e.g., "vision", "code").
        
        Args:
            capability: Capability to filter by
            
        Returns:
            List of models with the specified capability
        """
        return [
            model for model in self.get_all_models()
            if model.get("capabilities") and capability in model.get("capabilities", [])
        ]
    
    def has_model(self, provider: str, model_id: str) -> bool:
        """
        Check if a model exists in the registry.
        
        Args:
            provider: Provider name
            model_id: Model ID
            
        Returns:
            Whether the model exists
        """
        return f"{provider}:{model_id}" in self.models
    
    def get_model(self, provider: str, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific model by provider and ID.
        
        Args:
            provider: Provider name
            model_id: Model ID
            
        Returns:
            The model or None if not found
        """
        return self.models.get(f"{provider}:{model_id}")


class InputAnalyzer:
    """
    Analyzer for determining requirements from a prompt.
    """
    
    def __init__(self):
        """Initialize analyzer with keyword lists for detection."""
        # Keywords for detecting specific requirements
        self.VISION_KEYWORDS = [
            'image', 'picture', 'photo', 'diagram', 'chart', 'screenshot', 'graph',
            'infographic', 'illustration', 'visual', 'look at this', 'analyze this image'
        ]
        
        self.CODE_KEYWORDS = [
            'code', 'programming', 'function', 'algorithm', 'javascript', 'python', 'java',
            'c++', 'typescript', 'html', 'css', 'react', 'node', 'express', 'coding',
            'bug', 'debug', 'script', 'implementation', 'software', 'developer', 'compile'
        ]
        
        self.MATH_KEYWORDS = [
            'math', 'calculation', 'equation', 'formula', 'calculus', 'algebra', 'statistics',
            'probability', 'numerical', 'computation', 'solve', 'geometric', 'matrix', 'vector'
        ]
        
        self.CREATIVE_KEYWORDS = [
            'creative', 'story', 'poem', 'fiction', 'narrative', 'script', 'screenplay',
            'artistic', 'imaginative', 'design', 'invent', 'create', 'novel', 'write'
        ]
        
        self.REASONING_KEYWORDS = [
            'explain', 'reasoning', 'logic', 'rationale', 'justify', 'argument', 'analyze',
            'deduce', 'infer', 'step-by-step', 'step by step', 'breakdown', 'systematic'
        ]
    
    def count_words(self, text: str) -> int:
        """
        Count the number of words in a text string.
        
        Args:
            text: Input text
            
        Returns:
            Word count
        """
        return len(re.findall(r'\b\w+\b', text))
    
    def contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """
        Check if text contains any of the specified keywords.
        
        Args:
            text: Input text
            keywords: List of keywords to check
            
        Returns:
            True if any keyword is found
        """
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the text.
        A rough estimate is that 1 token ≈ 4 characters or 0.75 words for English text.
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        return max(
            round(len(text) / 4),
            round(self.count_words(text) * 0.75)
        )
    
    def assess_complexity(self, text: str) -> int:
        """
        Assess the complexity of a prompt on a scale of 1-5.
        
        Args:
            text: Input text
            
        Returns:
            Complexity rating (1-5)
        """
        word_count = self.count_words(text)
        token_count = self.estimate_tokens(text)
        
        # Base complexity on length
        complexity = 1
        
        if word_count > 500 or token_count > 750:
            complexity += 1
        if word_count > 1000 or token_count > 1500:
            complexity += 1
        
        # Increase complexity for combined requirements
        requirement_count = 0
        if self.contains_keywords(text, self.CODE_KEYWORDS):
            requirement_count += 1
        if self.contains_keywords(text, self.MATH_KEYWORDS):
            requirement_count += 1
        if self.contains_keywords(text, self.REASONING_KEYWORDS):
            requirement_count += 1
        
        if requirement_count >= 2:
            complexity += 1
        if requirement_count >= 3:
            complexity += 1
        
        # Cap at 5
        return min(complexity, 5)
    
    def analyze_requirements(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze input requirements from the prompt.
        
        Args:
            prompt: User prompt
            
        Returns:
            Dictionary of requirements
        """
        token_count = self.estimate_tokens(prompt)
        word_count = self.count_words(prompt)
        needs_vision = self.contains_keywords(prompt, self.VISION_KEYWORDS)
        needs_code = self.contains_keywords(prompt, self.CODE_KEYWORDS)
        needs_math = self.contains_keywords(prompt, self.MATH_KEYWORDS)
        needs_creativity = self.contains_keywords(prompt, self.CREATIVE_KEYWORDS)
        needs_reasoning = self.contains_keywords(prompt, self.REASONING_KEYWORDS)
        complexity = self.assess_complexity(prompt)
        
        # Context window requirement is a multiple of the input length plus room for response
        min_context_window = max(token_count * 4, 1000)
        
        # Detect domains/categories from the prompt
        domains = []
        if needs_code:
            domains.append('code')
        if needs_math:
            domains.append('math')
        if needs_creativity:
            domains.append('creative')
        if needs_reasoning:
            domains.append('reasoning')
        if not domains:
            domains.append('general')
        
        return {
            "token_count": token_count,
            "word_count": word_count,
            "needs_vision": needs_vision,
            "needs_code": needs_code,
            "needs_math": needs_math,
            "needs_creativity": needs_creativity,
            "needs_reasoning": needs_reasoning,
            "complexity": complexity,
            "min_context_window": min_context_window,
            "is_multimodal": needs_vision,
            "domains": domains
        }


class ModelScorer:
    """
    Scorer for ranking models based on requirements.
    """
    
    def __init__(self):
        """Initialize scorer with scoring weights."""
        # Scoring weights for different attributes
        self.weights = {
            "vision": 50,
            "context_window": 20,
            "intelligence": 10,
            "code": 25,
            "math": 25,
            "reasoning": 30,
            "creativity": 15,
            "speed": 15,
            "provider": {
                'openai': {'code': 10},
                'anthropic': {'reasoning': 10, 'creativity': 10},
                'vertex': {'math': 5},
                'xai': {'reasoning': 5}
            }
        }
    
    def score_model(self, model: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate a score for a model based on requirements.
        
        Args:
            model: Model object with attributes
            requirements: Requirements from input analysis
            
        Returns:
            Dictionary with score and reasons
        """
        score = 0
        reasons = []
        
        # Critical capabilities check - automatic disqualification
        if requirements.get("needs_vision") and "vision" not in model.get("capabilities", []):
            return {
                "score": -9999,
                "reasons": ['lacks required vision capability']
            }
        
        # Context window check
        if model.get("context_window") and model.get("context_window") >= requirements.get("min_context_window", 0):
            score += self.weights["context_window"]
        elif model.get("context_window") and model.get("context_window") < requirements.get("min_context_window", 0):
            score -= self.weights["context_window"] * 1.5
            reasons.append('limited context window')
        
        # Vision capability
        if requirements.get("needs_vision") and "vision" in model.get("capabilities", []):
            score += self.weights["vision"]
            reasons.append('supports image analysis')
        
        # Intelligence match for complexity
        if model.get("intelligence"):
            intelligence_match = model["intelligence"] - requirements.get("complexity", 0)
            if intelligence_match >= 0:
                score += intelligence_match * self.weights["intelligence"] + 20
                if intelligence_match > 1:
                    reasons.append(f"high intelligence rating ({model['intelligence']}/5)")
            else:
                score -= abs(intelligence_match) * self.weights["intelligence"] * 1.5
                reasons.append(f"lower intelligence rating ({model['intelligence']}/5)")
        
        # Task-specific capability bonuses
        if requirements.get("needs_code") and "code" in model.get("capabilities", []):
            score += self.weights["code"]
            reasons.append('strong code capabilities')
        
        if requirements.get("needs_math") and model.get("intelligence") and model["intelligence"] >= 4:
            score += self.weights["math"]
            reasons.append('strong math capabilities')
        
        if requirements.get("needs_reasoning") and "reasoning" in model.get("capabilities", []):
            score += self.weights["reasoning"]
            reasons.append('specialized reasoning capabilities')
        
        if requirements.get("needs_creativity") and "creativity" in model.get("capabilities", []):
            score += self.weights["creativity"]
            reasons.append('creative capabilities')
        
        # Speed bonus for less complex tasks
        if requirements.get("complexity", 5) <= 3 and model.get("speed") and model["speed"] >= 4:
            score += self.weights["speed"]
            reasons.append(f"fast response times ({model['speed']}/5)")
        
        # Provider-specific bonuses based on observed strengths
        provider = model.get("provider")
        for domain in requirements.get("domains", []):
            if (provider in self.weights["provider"] and 
                domain in self.weights["provider"][provider]):
                score += self.weights["provider"][provider][domain]
                reasons.append(f"{provider}'s strength in {domain}")
        
        return {"score": score, "reasons": reasons}
    
    def generate_explanation(self, model: Dict[str, Any], reasons: List[str]) -> str:
        """
        Generate a human-readable explanation for model selection.
        
        Args:
            model: Selected model
            reasons: Reasons for selection
            
        Returns:
            Human-readable explanation
        """
        display_name = model.get("display_name") or model.get("model_id")
        explanation = f"Selected {display_name} because it "
        
        if reasons:
            # Convert list to comma-separated string with "and" before the last item
            if len(reasons) == 1:
                explanation += reasons[0]
            else:
                last_reason = reasons[-1]
                other_reasons = reasons[:-1]
                explanation += ", ".join(other_reasons) + f" and {last_reason}"
        else:
            explanation += "is well-suited for general tasks"
        
        return explanation + "."


class GPToggle:
    """
    Main GPToggle v2.0 class with model-agnostic implementation and contextualized intelligence.
    
    New in v2.0:
    - Universal user profiles for personalization
    - Query classification and contextual enhancement
    - Adaptive learning from user interactions
    - Cross-service compatible profiling system
    """
    
    def __init__(self, config: Dict[str, Any] = None, api_keys: Dict[str, str] = None):
        """
        Initialize GPToggle v2.0 with API keys, configuration, and contextualized intelligence.
        
        Args:
            config: Configuration dictionary
            api_keys: Dictionary of API keys for different providers
        """
        self.api_keys = api_keys or {}
        self.config = config or {}
        self.registry = ModelRegistry()
        self.analyzer = InputAnalyzer()
        self.scorer = ModelScorer()
        self.provider_handlers = {}
        
        # Contextualized Intelligence v2.0 components
        self.query_classifier = QueryClassifier()
        self.contextual_enhancer = ContextualEnhancer()
        self.user_profiles = {}  # Store user profiles in memory
        
        # Version info
        self.version = "2.0.0"
        
        # Register built-in fallback models
        self.register_fallback_models()
    
    def register_fallback_models(self):
        """Register minimal fallback models for emergency cases."""
        self.registry.register_model({
            "provider": "openai",
            "model_id": "gpt-3.5-turbo",
            "display_name": "GPT-3.5 Turbo",
            "capabilities": ["text", "code"],
            "strengths": {"general": 3, "code": 3},
            "tiers": ["free"],
            "context_window": 16000,
            "intelligence": 3,
            "speed": 4
        })
        
        # Only register if we have the API key
        if "anthropic" in self.api_keys:
            self.registry.register_model({
                "provider": "anthropic",
                "model_id": "claude-instant-1",
                "display_name": "Claude Instant",
                "capabilities": ["text", "reasoning"],
                "strengths": {"general": 3, "reasoning": 3},
                "tiers": ["free"],
                "context_window": 16000,
                "intelligence": 3,
                "speed": 4
            })
    
    def register_provider_handler(self, provider: str, handler: Callable) -> 'GPToggle':
        """
        Register an API handler for a provider.
        
        Args:
            provider: Provider name
            handler: API handler function
            
        Returns:
            Self for method chaining
        """
        self.provider_handlers[provider] = handler
        return self
    
    def register_model(self, model: Dict[str, Any]) -> 'GPToggle':
        """
        Register a model in the registry.
        
        Args:
            model: Model information dictionary
            
        Returns:
            Self for method chaining
        """
        self.registry.register_model(model)
        return self
    
    def register_models(self, models: List[Dict[str, Any]]) -> 'GPToggle':
        """
        Register multiple models at once.
        
        Args:
            models: List of model information dictionaries
            
        Returns:
            Self for method chaining
        """
        self.registry.register_models_from_list(models)
        return self
    
    def recommend_model(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Recommend the best model for a prompt.
        
        Args:
            prompt: User prompt
            options: Options dictionary (tier, etc.)
            
        Returns:
            Recommendation with provider, model and reason
        """
        options = options or {}
        
        # Get input requirements
        requirements = self.analyzer.analyze_requirements(prompt)
        
        # Get eligible models based on tier
        models = (self.registry.get_models_by_tier(options["tier"]) 
                  if "tier" in options 
                  else self.registry.get_all_models())
        
        if not models:
            return {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "reason": "No eligible models found, using fallback"
            }
        
        # Score each model
        scored_models = []
        for model in models:
            result = self.scorer.score_model(model, requirements)
            scored_models.append({
                "model": model,
                "score": result["score"],
                "reasons": result["reasons"]
            })
        
        # Sort by score (descending)
        scored_models.sort(key=lambda x: x["score"], reverse=True)
        
        # Select the highest-scoring model
        selected = scored_models[0]
        
        # Generate explanation
        reason = self.scorer.generate_explanation(
            selected["model"],
            selected["reasons"]
        )
        
        return {
            "provider": selected["model"]["provider"],
            "model": selected["model"]["model_id"],
            "reason": reason,
            "requirements": requirements,
            "score": selected["score"]
        }
    
    def get_or_create_user_profile(self, user_id: str) -> UserProfile:
        """
        Get an existing user profile or create a new one.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            UserProfile instance
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile.create_default(user_id)
        return self.user_profiles[user_id]
    
    def save_user_profile(self, user_profile: UserProfile) -> None:
        """
        Save a user profile.
        
        Args:
            user_profile: UserProfile instance to save
        """
        self.user_profiles[user_profile.userId] = user_profile
    
    def _generate_follow_up_suggestion(self, query_type: str, user_profile: UserProfile) -> str:
        """
        Generate follow-up suggestions based on query type and user profile.
        
        Args:
            query_type: Type of the original query
            user_profile: User's profile for personalization
            
        Returns:
            Follow-up suggestion string
        """
        follow_ups = {
            'code': "Would you like me to explain how this code works or help you test it?",
            'creative': "Would you like me to expand on this idea or create variations?",
            'factual': "Is there anything else you'd like to explore about this topic?",
            'analytical': "Would you like me to dive deeper into any specific aspect?",
            'business': "Would you like me to help with implementation strategies or risk analysis?",
            'educational': "Would you like me to provide examples or practice exercises?",
            'general': "How else can I help you with this topic?"
        }
        
        base_suggestion = follow_ups.get(query_type, follow_ups['general'])
        
        # Personalize based on user's common topics
        common_topics = user_profile.context['learningPatterns']['commonTopics']
        if common_topics:
            most_common = common_topics[0]['topic']
            if most_common != query_type:
                base_suggestion += f" Or would you like to explore how this relates to {most_common}?"
        
        return base_suggestion

    def get_task_recommendations(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get recommendations for specific tasks within a prompt.
        
        Args:
            prompt: User prompt
            options: Options dictionary (tier, etc.)
            
        Returns:
            Overall and task-specific recommendations
        """
        options = options or {}
        
        # Get overall recommendation
        overall = self.recommend_model(prompt, options)
        
        # Get all eligible models
        models = (self.registry.get_models_by_tier(options["tier"]) 
                  if "tier" in options 
                  else self.registry.get_all_models())
        
        # Get requirements
        requirements = self.analyzer.analyze_requirements(prompt)
        
        # Score each model
        scored_models = []
        for model in models:
            result = self.scorer.score_model(model, requirements)
            scored_models.append({
                "model": model,
                "score": result["score"],
                "reasons": result["reasons"]
            })
        
        # Sort by score (descending)
        scored_models.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top 3 models for recommendations
        top_models = scored_models[:3]
        
        # Format recommendations
        recommendations = []
        for scored in top_models:
            rec = {
                "provider": scored["model"]["provider"],
                "model": scored["model"]["model_id"],
                "reason": self.scorer.generate_explanation(scored["model"], scored["reasons"]),
            }
            
            if "intelligence" in scored["model"]:
                rec["strength"] = f"Intelligence: {scored['model']['intelligence']}/5"
                
            recommendations.append(rec)
        
        return {
            "overall": overall,
            "recommendations": recommendations
        }
    
    async def get_response(self, prompt: str, provider_name: str = None, model_name: str = None, 
                     params: Dict[str, Any] = None) -> str:
        """
        Get a response from any provider.
        
        Args:
            prompt: User prompt
            provider_name: Provider name (auto-selected if not provided)
            model_name: Model name (auto-selected if not provided)
            params: Generation parameters
            
        Returns:
            Generated response
        """
        params = params or {}
        
        # Auto-select model if not specified
        if not provider_name or not model_name:
            recommendation = self.recommend_model(prompt, params)
            provider_name = provider_name or recommendation["provider"]
            model_name = model_name or recommendation["model"]
        
        # Check if API key is available
        if provider_name not in self.api_keys:
            raise ValueError(f"API key for {provider_name} not found")
        
        # Use registered provider handler if available
        if provider_name in self.provider_handlers:
            return await self.provider_handlers[provider_name](
                prompt, model_name, self.api_keys[provider_name], params
            )
        
        # Fallback to built-in handlers based on provider
        if provider_name == 'openai':
            return await self.openai_get_response(prompt, model_name, params)
        elif provider_name == 'anthropic':
            return await self.anthropic_get_response(prompt, model_name, params)
        else:
            raise ValueError(f"Provider {provider_name} not implemented and no custom handler registered")
    
    async def openai_get_response(self, prompt: str, model: str, params: Dict[str, Any] = None) -> str:
        """
        Get a response using the OpenAI API.
        
        Args:
            prompt: User prompt
            model: Model name
            params: Generation parameters
            
        Returns:
            Generated response
        """
        # Import openai here to avoid dependency if not used
        from openai import OpenAI
        
        try:
            client = OpenAI(api_key=self.api_keys.get("openai"))
            
            # Set up parameters
            temperature = params.get("temperature", 0.7)
            max_tokens = params.get("max_tokens", 1000)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def anthropic_get_response(self, prompt: str, model: str, params: Dict[str, Any] = None) -> str:
        """
        Get a response using the Anthropic Claude API.
        
        Args:
            prompt: User prompt
            model: Model name
            params: Generation parameters
            
        Returns:
            Generated response
        """
        # Import anthropic here to avoid dependency if not used
        from anthropic import Anthropic
        
        try:
            client = Anthropic(api_key=self.api_keys.get("anthropic"))
            
            # Set up parameters
            temperature = params.get("temperature", 0.7)
            max_tokens = params.get("max_tokens", 1000)
            
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")


# Example model registry definition
sample_models = [
    {
        "provider": "openai",
        "model_id": "gpt-4o",
        "display_name": "GPT-4o",
        "capabilities": ["text", "vision", "code", "reasoning", "creativity"],
        "strengths": {"general": 5, "code": 5, "math": 4, "creativity": 4, "reasoning": 5},
        "weaknesses": ["hallucination"],
        "context_window": 128000,
        "intelligence": 5,
        "speed": 4,
        "tiers": ["standard"],
        "pricing": {
            "input_tokens": 0.00005,
            "output_tokens": 0.00015
        },
        "knowledge_cutoff": "2023-04",
        "released": "2023-05-13",
        "deprecated": False
    },
    {
        "provider": "anthropic",
        "model_id": "claude-3-opus",
        "display_name": "Claude 3 Opus",
        "capabilities": ["text", "vision", "reasoning", "creativity"],
        "strengths": {"general": 5, "reasoning": 5, "math": 4, "creativity": 5},
        "weaknesses": ["code"],
        "context_window": 200000,
        "intelligence": 5,
        "speed": 3,
        "tiers": ["standard"],
        "pricing": {
            "input_tokens": 0.00005,
            "output_tokens": 0.00015
        },
        "knowledge_cutoff": "2023-08",
        "released": "2024-03-04",
        "deprecated": False
    },
    {
        "provider": "anthropic",
        "model_id": "claude-3-sonnet",
        "display_name": "Claude 3 Sonnet",
        "capabilities": ["text", "vision", "reasoning", "creativity"],
        "strengths": {"general": 4, "reasoning": 4, "math": 3, "creativity": 4},
        "weaknesses": ["code"],
        "context_window": 200000,
        "intelligence": 4,
        "speed": 4,
        "tiers": ["standard"],
        "pricing": {
            "input_tokens": 0.00003,
            "output_tokens": 0.00010
        },
        "knowledge_cutoff": "2023-08",
        "released": "2024-03-04",
        "deprecated": False
    },
    # Example of adding a model from a new provider
    {
        "provider": "xai",
        "model_id": "grok-2",
        "display_name": "Grok 2",
        "capabilities": ["text", "code", "reasoning"],
        "strengths": {"general": 4, "reasoning": 4, "code": 3},
        "context_window": 130000,
        "intelligence": 4,
        "speed": 4,
        "tiers": ["standard"],
        "pricing": {
            "input_tokens": 0.00003,
            "output_tokens": 0.00010
        },
        "knowledge_cutoff": "2023-12",
        "released": "2024-04-11",
        "deprecated": False
    }
]


# Example usage
async def example():
    """Example usage of GPToggle."""
    # Initialize with API keys
    gptoggle = GPToggle(api_keys={
        "openai": os.environ.get("OPENAI_API_KEY"),
        "anthropic": os.environ.get("ANTHROPIC_API_KEY"),
        "xai": os.environ.get("XAI_API_KEY")
    })
    
    # Register example models
    gptoggle.register_models(sample_models)
    
    # Register a custom provider handler
    async def xai_handler(prompt, model, api_key, params):
        # Custom implementation for XAI/Grok API would go here
        return f"This is a custom XAI handler responding to: {prompt}"
    
    gptoggle.register_provider_handler("xai", xai_handler)
    
    # Get recommendation for a prompt
    recommendation = gptoggle.recommend_model(
        "Create a Python function that analyzes images to detect objects"
    )
    
    print("Recommendation:", recommendation)
    
    # Get task-specific recommendations
    task_recs = gptoggle.get_task_recommendations(
        "Create a Python function that analyzes images to detect objects"
    )
    
    print("Task Recommendations:", task_recs)
    
    # Get a response (would call the API in a real implementation)
    response = await gptoggle.get_response(
        "Create a Python function that analyzes images to detect objects"
    )
    
    print("Response:", response)


# Run the example if executed directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(example())