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
import { Logger } from '../utils/logger';
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

  constructor(storageAdapter?: ProfileStorageAdapter) {
    this.ajv = new Ajv({ allErrors: true });
    addFormats(this.ajv);
    this.ajv.addSchema(profileSchema, 'userProfile');
    this.logger = new Logger();
    this.storageAdapter = storageAdapter || new InMemoryStorageAdapter();
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
        }
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