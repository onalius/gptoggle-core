/**
 * User Profile Service
 * 
 * Manages user profiles including loading, validation, caching, and updates.
 * Provides profile settings to the toggle() logic for personalized AI interactions.
 * 
 * @version 2.0.0
 */

import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { Logger } from './src/utils/logger';
import { ModuleService, ModuleUpdateContext } from './src/modules/moduleService';
import profileSchema from './userProfileSchema.json';

export interface UserProfile {
  userId: string;
  communicationStyle: {
    tone: 'formal' | 'casual' | 'friendly' | 'professional' | 'witty' | 'empathetic';
    verbosity: 'concise' | 'moderate' | 'detailed' | 'comprehensive';
    language: string;
    includeExplanations: boolean;
  };
  expertise: {
    domains: string[];
    skillLevel: Record<string, 'beginner' | 'intermediate' | 'advanced' | 'expert'>;
    interests: string[];
  };
  preferences: {
    prioritizeSpeed: boolean;
    adaptivePersonalization: boolean;
    contextualAwareness: boolean;
    privacyLevel: 'minimal' | 'standard' | 'enhanced' | 'maximum';
  };
  context: {
    recentInteractions: Array<{
      content: string;
      timestamp: string;
      category?: string;
      service?: string;
    }>;
    savedItems: Array<{
      content: string;
      type: string;
      timestamp: string;
      tags?: string[];
      metadata?: any;
    }>;
    learningPatterns: {
      commonTopics: Array<{
        topic: string;
        frequency: number;
        lastSeen: string;
      }>;
      timePatterns: Record<string, number>;
      contextualPreferences: Record<string, any>;
    };
    modules?: Record<string, {
      type: 'list' | 'planner' | 'calendar' | 'interest' | 'tracker' | 'goal';
      data: any;
      metadata: {
        createdAt: string;
        lastUpdated: string;
        lastAccessed?: string;
        priority?: number;
        tags?: string[];
        archived?: boolean;
      };
    }>;
  };
  serviceSpecific: Record<string, {
    enabled: boolean;
    configuration: any;
    preferences: any;
  }>;
  metadata: {
    createdAt: string;
    lastUpdated: string;
    version: string;
    source?: string;
    services: string[];
  };
}

export class UserProfileService {
  private ajv: Ajv;
  private profileCache: Map<string, UserProfile> = new Map();
  private logger: Logger;
  private storageAdapter: ProfileStorageAdapter;
  private moduleService: ModuleService;

  constructor(storageAdapter?: ProfileStorageAdapter) {
    this.ajv = new Ajv({ allErrors: true });
    addFormats(this.ajv);
    this.ajv.addSchema(profileSchema, 'userProfile');
    this.logger = new Logger('UserProfileService');
    this.storageAdapter = storageAdapter || new InMemoryStorageAdapter();
    this.moduleService = new ModuleService();
  }

  /**
   * Load a user profile by userId with caching
   */
  async loadProfile(userId: string): Promise<UserProfile> {
    // Check cache first
    if (this.profileCache.has(userId)) {
      const cachedProfile = this.profileCache.get(userId)!;
      this.logger.debug(`Profile loaded from cache for user: ${userId}`);
      return cachedProfile;
    }

    try {
      // Load from storage
      const profileData = await this.storageAdapter.loadProfile(userId);
      
      if (!profileData) {
        // Create default profile for new user
        const defaultProfile = this.createDefaultProfile(userId);
        await this.saveProfile(defaultProfile);
        return defaultProfile;
      }

      // Validate the loaded profile
      const validProfile = this.validateProfile(profileData);
      
      // Cache the valid profile
      this.profileCache.set(userId, validProfile);
      
      this.logger.debug(`Profile loaded for user: ${userId}`);
      return validProfile;

    } catch (error) {
      this.logger.error(`Failed to load profile for user ${userId}: ${error.message}`);
      // Return default profile as fallback
      return this.createDefaultProfile(userId);
    }
  }

  /**
   * Save a user profile
   */
  async saveProfile(profile: UserProfile): Promise<void> {
    try {
      // Validate before saving
      const validProfile = this.validateProfile(profile);
      
      // Update metadata
      validProfile.metadata = {
        ...validProfile.metadata,
        lastUpdated: new Date().toISOString(),
        version: '2.0.0'
      };

      // Save to storage
      await this.storageAdapter.saveProfile(validProfile);
      
      // Update cache
      this.profileCache.set(validProfile.userId, validProfile);
      
      this.logger.debug(`Profile saved for user: ${validProfile.userId}`);

    } catch (error) {
      this.logger.error(`Failed to save profile for user ${profile.userId}: ${error.message}`);
      throw error;
    }
  }

  /**
   * Update specific aspects of a user profile
   */
  async updateProfile(userId: string, updates: Partial<UserProfile>): Promise<UserProfile> {
    const existingProfile = await this.loadProfile(userId);
    
    const updatedProfile: UserProfile = {
      ...existingProfile,
      ...updates,
      userId, // Ensure userId cannot be changed
      metadata: {
        ...existingProfile.metadata,
        lastUpdated: new Date().toISOString()
      }
    };

    await this.saveProfile(updatedProfile);
    return updatedProfile;
  }

  /**
   * Update profile with module integration - automatically detects and manages modules
   */
  async updateProfileWithModules(
    userId: string, 
    query: string, 
    updates: Partial<UserProfile>,
    queryType?: string
  ): Promise<{
    profile: UserProfile;
    moduleActions: Array<{
      action: string;
      moduleKey?: string;
      moduleType?: string;
      success: boolean;
    }>;
  }> {
    const profile = await this.updateProfile(userId, updates);
    
    // Analyze query for module relevance
    const moduleAnalysis = await this.moduleService.analyzeQueryForModules(query, profile);
    const moduleActions: Array<{
      action: string;
      moduleKey?: string;
      moduleType?: string;
      success: boolean;
    }> = [];

    const updateContext: ModuleUpdateContext = {
      query,
      queryType,
      detectedIntent: this.detectIntent(query)
    };

    // Process suggested module actions
    for (const suggestion of moduleAnalysis.suggestedActions) {
      try {
        if (suggestion.action === 'create' && suggestion.moduleType) {
          const moduleKey = this.generateModuleKey(query, suggestion.moduleType);
          const initialData = this.extractInitialModuleData(query, suggestion.moduleType);
          
          await this.moduleService.createModule(
            profile,
            moduleKey,
            suggestion.moduleType,
            initialData,
            updateContext
          );
          
          moduleActions.push({
            action: 'create',
            moduleKey,
            moduleType: suggestion.moduleType,
            success: true
          });
        } else if (suggestion.action === 'update' && suggestion.moduleKey) {
          const updateData = this.extractModuleUpdateData(query, suggestion.moduleKey, profile);
          
          await this.moduleService.updateModule(
            profile,
            suggestion.moduleKey,
            updateData,
            updateContext
          );
          
          moduleActions.push({
            action: 'update',
            moduleKey: suggestion.moduleKey,
            success: true
          });
        }
      } catch (error) {
        this.logger.error(`Module ${suggestion.action} failed: ${error.message}`);
        moduleActions.push({
          action: suggestion.action,
          moduleKey: suggestion.moduleKey,
          moduleType: suggestion.moduleType,
          success: false
        });
      }
    }

    // Clean up stale modules periodically
    if (Math.random() < 0.1) { // 10% chance to run cleanup
      await this.moduleService.cleanupStaleModules(profile);
    }

    // Save profile with updated modules
    await this.saveProfile(profile);

    return { profile, moduleActions };
  }

  /**
   * Add an interaction to user's context
   */
  async addInteractionToContext(userId: string, content: string, category?: string, service?: string): Promise<void> {
    const profile = await this.loadProfile(userId);
    
    const interaction = {
      content,
      timestamp: new Date().toISOString(),
      category,
      service: service || 'gptoggle'
    };

    // Add new interaction and maintain limit
    profile.context.recentInteractions.unshift(interaction);
    profile.context.recentInteractions = profile.context.recentInteractions.slice(0, 100);

    // Update learning patterns
    if (category) {
      const existingTopic = profile.context.learningPatterns.commonTopics.find(t => t.topic === category);
      if (existingTopic) {
        existingTopic.frequency += 1;
        existingTopic.lastSeen = new Date().toISOString();
      } else {
        profile.context.learningPatterns.commonTopics.push({
          topic: category,
          frequency: 1,
          lastSeen: new Date().toISOString()
        });
      }

      // Sort by frequency and maintain limit
      profile.context.learningPatterns.commonTopics.sort((a, b) => b.frequency - a.frequency);
      profile.context.learningPatterns.commonTopics = profile.context.learningPatterns.commonTopics.slice(0, 20);
    }

    await this.saveProfile(profile);
  }

  /**
   * Add a saved item to user's context
   */
  async addSavedItem(userId: string, content: string, type: string, tags?: string[], metadata?: any): Promise<void> {
    const profile = await this.loadProfile(userId);
    
    const savedItem = {
      content,
      type,
      timestamp: new Date().toISOString(),
      tags: tags || [],
      metadata
    };

    // Add new saved item and maintain limit
    profile.context.savedItems.unshift(savedItem);
    profile.context.savedItems = profile.context.savedItems.slice(0, 200);

    await this.saveProfile(profile);
  }

  /**
   * Get personalized service recommendations based on user profile
   */
  getServiceRecommendations(profile: UserProfile, context: string): string[] {
    const recommendations: string[] = [];

    // Use service-specific preferred models if available
    const gptoggleConfig = profile.serviceSpecific['gptoggle'];
    if (gptoggleConfig?.configuration?.preferredModels) {
      recommendations.push(...gptoggleConfig.configuration.preferredModels);
    }

    // Domain expertise based recommendations
    const domainModelMap: Record<string, string[]> = {
      'technology': ['gpt-4o', 'claude-3-opus', 'gemini-1.5-pro'],
      'finance': ['claude-3-opus', 'gpt-4-turbo'],
      'health': ['claude-3-opus', 'gemini-1.5-pro'],
      'legal': ['claude-3-opus', 'gpt-4-turbo'],
      'science': ['gemini-1.5-pro', 'claude-3-opus', 'gpt-4o'],
      'arts': ['gpt-4o', 'claude-3-sonnet', 'gemini-1.5-flash'],
      'engineering': ['gpt-4o', 'claude-3-opus', 'gemini-1.5-pro']
    };

    profile.expertise.domains.forEach(domain => {
      if (domainModelMap[domain as keyof typeof domainModelMap]) {
        recommendations.push(...domainModelMap[domain as keyof typeof domainModelMap]);
      }
    });

    // Remove duplicates while preserving order
    return [...new Set(recommendations)];
  }

  /**
   * Analyze user patterns to provide insights
   */
  analyzeUserPatterns(profile: UserProfile): {
    commonTopics: Array<{ topic: string; frequency: number }>;
    preferredTimeSlots: string[];
    interactionEffectiveness: Record<string, number>;
  } {
    const analysis = {
      commonTopics: [] as Array<{ topic: string; frequency: number }>,
      preferredTimeSlots: [] as string[],
      interactionEffectiveness: {} as Record<string, number>
    };

    // Use the already computed common topics from learning patterns
    analysis.commonTopics = profile.context.learningPatterns.commonTopics.map(t => ({
      topic: t.topic,
      frequency: t.frequency
    }));

    // Analyze time patterns from recent interactions
    const timeSlotCounts: Record<string, number> = {};
    const serviceCounts: Record<string, number> = {};

    profile.context.recentInteractions.forEach(interaction => {
      // Count time slots
      const hour = new Date(interaction.timestamp).getHours();
      const timeSlot = this.getTimeSlot(hour);
      timeSlotCounts[timeSlot] = (timeSlotCounts[timeSlot] || 0) + 1;

      // Count service usage
      if (interaction.service) {
        serviceCounts[interaction.service] = (serviceCounts[interaction.service] || 0) + 1;
      }
    });

    analysis.preferredTimeSlots = Object.entries(timeSlotCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([slot]) => slot);

    // Simple effectiveness score based on usage
    const totalInteractions = profile.context.recentInteractions.length;
    analysis.interactionEffectiveness = Object.fromEntries(
      Object.entries(serviceCounts).map(([service, count]) => [
        service,
        totalInteractions > 0 ? count / totalInteractions : 0
      ])
    );

    return analysis;
  }

  /**
   * Get user modules summary using the ModuleService
   */
  getUserModulesSummary(userId: string): Promise<any> {
    return this.loadProfile(userId).then(profile => 
      this.moduleService.getUserModulesSummary(profile)
    );
  }

  /**
   * Detect intent from query for module context
   */
  private detectIntent(query: string): string {
    const queryLower = query.toLowerCase();
    
    if (queryLower.includes('add') || queryLower.includes('create') || queryLower.includes('make')) {
      return 'add';
    } else if (queryLower.includes('remove') || queryLower.includes('delete') || queryLower.includes('clear')) {
      return 'remove';
    } else if (queryLower.includes('update') || queryLower.includes('change') || queryLower.includes('modify')) {
      return 'update';
    } else if (queryLower.includes('show') || queryLower.includes('display') || queryLower.includes('list')) {
      return 'view';
    }
    
    return 'general';
  }

  /**
   * Generate a meaningful module key from query and type
   */
  private generateModuleKey(query: string, moduleType: string): string {
    const queryWords = query.toLowerCase().split(' ').filter(word => word.length > 2);
    const relevantWords = queryWords.slice(0, 3); // Take first 3 meaningful words
    
    const keyBase = relevantWords.join('');
    return `${keyBase}${moduleType.charAt(0).toUpperCase()}${moduleType.slice(1)}`;
  }

  /**
   * Extract initial data for new modules based on query content
   */
  private extractInitialModuleData(query: string, moduleType: string): any {
    const queryLower = query.toLowerCase();
    
    switch (moduleType) {
      case 'list':
        // Extract items from query like "add milk, eggs, bread to shopping list"
        const itemPattern = /(?:add|buy|get|need)\s+([^.!?]+?)(?:\s+to|\s+for|$)/i;
        const match = query.match(itemPattern);
        if (match) {
          const items = match[1].split(/[,;&]/).map(item => item.trim()).filter(item => item.length > 0);
          return items;
        }
        return [];
        
      case 'planner':
        return {
          date: this.extractDateFromQuery(query),
          tasks: this.extractTasksFromQuery(query),
          guests: this.extractGuestsFromQuery(query)
        };
        
      case 'calendar':
        const dateInfo = this.extractDateFromQuery(query);
        if (dateInfo) {
          return { [dateInfo]: query };
        }
        return {};
        
      case 'interest':
        return {
          keywords: this.extractKeywordsFromQuery(query),
          engagementLevel: 5
        };
        
      default:
        return {};
    }
  }

  /**
   * Extract update data for existing modules
   */
  private extractModuleUpdateData(query: string, moduleKey: string, profile: UserProfile): any {
    const module = profile.context.modules?.[moduleKey];
    if (!module) return {};

    const intent = this.detectIntent(query);
    
    switch (module.type) {
      case 'list':
        if (intent === 'add') {
          return this.extractItemsFromQuery(query);
        } else if (intent === 'remove') {
          return this.extractItemsToRemove(query, module.data);
        }
        break;
        
      case 'planner':
        return {
          tasks: this.extractTasksFromQuery(query),
          guests: this.extractGuestsFromQuery(query)
        };
        
      default:
        return {};
    }
    
    return {};
  }

  /**
   * Helper methods for data extraction
   */
  private extractDateFromQuery(query: string): string | null {
    // Simple date extraction - could be enhanced with a proper date parsing library
    const datePatterns = [
      /(\d{4}-\d{2}-\d{2})/,
      /(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}/i,
      /(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2}/i
    ];
    
    for (const pattern of datePatterns) {
      const match = query.match(pattern);
      if (match) return match[1];
    }
    
    return null;
  }

  private extractTasksFromQuery(query: string): string[] {
    const taskPatterns = [
      /(?:tasks?|todo|need to)\s*:?\s*([^.!?]+)/i,
      /(?:book|send|buy|get|organize)\s+([^.!?]+)/gi
    ];
    
    const tasks: string[] = [];
    for (const pattern of taskPatterns) {
      const matches = query.matchAll(pattern);
      for (const match of matches) {
        if (match[1]) {
          tasks.push(match[1].trim());
        }
      }
    }
    
    return tasks;
  }

  private extractGuestsFromQuery(query: string): string[] {
    const guestPattern = /(?:guests?|invite|attendees?)\s*:?\s*([^.!?]+)/i;
    const match = query.match(guestPattern);
    
    if (match) {
      return match[1].split(/[,;&]/).map(guest => guest.trim()).filter(guest => guest.length > 0);
    }
    
    return [];
  }

  private extractKeywordsFromQuery(query: string): string[] {
    // Extract meaningful keywords (nouns, adjectives)
    const words = query.toLowerCase().split(/\s+/);
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);
    
    return words.filter(word => 
      word.length > 3 && 
      !stopWords.has(word) && 
      /^[a-zA-Z]+$/.test(word)
    ).slice(0, 5); // Limit to 5 keywords
  }

  private extractItemsFromQuery(query: string): string[] {
    const itemPattern = /(?:add|include)\s+([^.!?]+)/i;
    const match = query.match(itemPattern);
    
    if (match) {
      return match[1].split(/[,;&]/).map(item => item.trim()).filter(item => item.length > 0);
    }
    
    return [];
  }

  private extractItemsToRemove(query: string, currentItems: string[]): string[] {
    const removePattern = /(?:remove|delete)\s+([^.!?]+)/i;
    const match = query.match(removePattern);
    
    if (match) {
      const itemsToRemove = match[1].split(/[,;&]/).map(item => item.trim());
      return currentItems.filter(item => 
        itemsToRemove.some(removeItem => 
          item.toLowerCase().includes(removeItem.toLowerCase())
        )
      );
    }
    
    return [];
  }

  /**
   * Validate profile against schema
   */
  private validateProfile(profileData: any): UserProfile {
    const valid = this.ajv.validate('userProfile', profileData);
    
    if (!valid) {
      const errors = this.ajv.errors?.map(err => `${err.instancePath}: ${err.message}`).join(', ');
      throw new Error(`Profile validation failed: ${errors}`);
    }

    return profileData as UserProfile;
  }

  /**
   * Create a default profile for new users
   */
  private createDefaultProfile(userId: string): UserProfile {
    return {
      userId,
      communicationStyle: {
        tone: 'casual',
        verbosity: 'moderate',
        language: 'en',
        includeExplanations: true
      },
      expertise: {
        domains: [],
        skillLevel: {},
        interests: []
      },
      preferences: {
        prioritizeSpeed: false,
        adaptivePersonalization: true,
        contextualAwareness: true,
        privacyLevel: 'standard'
      },
      context: {
        recentInteractions: [],
        savedItems: [],
        learningPatterns: {
          commonTopics: [],
          timePatterns: {},
          contextualPreferences: {}
        },
        modules: {}
      },
      serviceSpecific: {},
      metadata: {
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
        version: '2.0.0',
        source: 'api',
        services: []
      }
    };
  }

  /**
   * Get time slot for hour
   */
  private getTimeSlot(hour: number): string {
    if (hour >= 6 && hour < 12) return 'morning';
    if (hour >= 12 && hour < 18) return 'afternoon';
    if (hour >= 18 && hour < 22) return 'evening';
    return 'night';
  }

  /**
   * Clear cache for specific user or all users
   */
  clearCache(userId?: string): void {
    if (userId) {
      this.profileCache.delete(userId);
    } else {
      this.profileCache.clear();
    }
  }
}

/**
 * Storage adapter interface for different storage backends
 */
export interface ProfileStorageAdapter {
  loadProfile(userId: string): Promise<UserProfile | null>;
  saveProfile(profile: UserProfile): Promise<void>;
  deleteProfile(userId: string): Promise<void>;
}

/**
 * In-memory storage adapter for development/testing
 */
export class InMemoryStorageAdapter implements ProfileStorageAdapter {
  private profiles: Map<string, UserProfile> = new Map();

  async loadProfile(userId: string): Promise<UserProfile | null> {
    return this.profiles.get(userId) || null;
  }

  async saveProfile(profile: UserProfile): Promise<void> {
    this.profiles.set(profile.userId, profile);
  }

  async deleteProfile(userId: string): Promise<void> {
    this.profiles.delete(userId);
  }
}

/**
 * File-based storage adapter
 */
export class FileStorageAdapter implements ProfileStorageAdapter {
  constructor(private storageDirectory: string) {}

  async loadProfile(userId: string): Promise<UserProfile | null> {
    try {
      const fs = await import('fs/promises');
      const path = await import('path');
      
      const filePath = path.join(this.storageDirectory, `${userId}.json`);
      const data = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return null; // File doesn't exist
      }
      throw error;
    }
  }

  async saveProfile(profile: UserProfile): Promise<void> {
    const fs = await import('fs/promises');
    const path = await import('path');
    
    // Ensure directory exists
    await fs.mkdir(this.storageDirectory, { recursive: true });
    
    const filePath = path.join(this.storageDirectory, `${profile.userId}.json`);
    await fs.writeFile(filePath, JSON.stringify(profile, null, 2));
  }

  async deleteProfile(userId: string): Promise<void> {
    const fs = await import('fs/promises');
    const path = await import('path');
    
    const filePath = path.join(this.storageDirectory, `${userId}.json`);
    await fs.unlink(filePath);
  }
}