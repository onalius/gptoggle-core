/**
 * Module Service
 * 
 * Manages adaptive modules that track specialized areas of interest and intent per user.
 * These modules evolve as users interact with GPToggle-based platforms, enabling
 * intelligent support for recurring needs, personal goals, and contextual knowledge.
 * 
 * @version 2.0.0
 */

import { UserProfile } from '../profile/userProfileService';
import { Logger } from '../utils/logger';

export type ModuleType = 'list' | 'planner' | 'calendar' | 'interest' | 'tracker' | 'goal';

export interface ModuleMetadata {
  createdAt: string;
  lastUpdated: string;
  lastAccessed?: string;
  priority?: number; // 1-10 scale
  tags?: string[];
  archived?: boolean;
}

export interface BaseModule {
  type: ModuleType;
  data: any;
  metadata: ModuleMetadata;
}

export interface ListModule extends BaseModule {
  type: 'list';
  data: string[];
}

export interface PlannerModule extends BaseModule {
  type: 'planner';
  data: {
    date?: string;
    guests?: string[];
    tasks?: string[];
    budget?: number;
    location?: string;
    notes?: string;
    status?: 'planning' | 'in-progress' | 'completed' | 'cancelled';
  };
}

export interface CalendarModule extends BaseModule {
  type: 'calendar';
  data: Record<string, string>; // date -> event mapping
}

export interface InterestModule extends BaseModule {
  type: 'interest';
  data: {
    keywords: string[];
    engagementLevel: number; // 1-10 scale
    relatedTopics?: string[];
    lastEngagement?: string;
  };
}

export interface TrackerModule extends BaseModule {
  type: 'tracker';
  data: {
    metric: string;
    unit?: string;
    target?: number;
    currentValue?: number;
    history?: Array<{ date: string; value: number; notes?: string }>;
  };
}

export interface GoalModule extends BaseModule {
  type: 'goal';
  data: {
    title: string;
    description?: string;
    deadline?: string;
    milestones?: Array<{ title: string; completed: boolean; completedAt?: string }>;
    progress?: number; // 0-100 percentage
    category?: string;
  };
}

export type Module = ListModule | PlannerModule | CalendarModule | InterestModule | TrackerModule | GoalModule;

export interface ModuleUpdateContext {
  query: string;
  queryType?: string;
  detectedIntent?: string;
  extractedData?: any;
}

export class ModuleService {
  private logger: Logger;

  constructor() {
    this.logger = new Logger();
  }

  /**
   * Analyze a query to determine if it relates to existing modules or should create a new one
   */
  async analyzeQueryForModules(query: string, userProfile: UserProfile): Promise<{
    relevantModules: string[];
    suggestedActions: Array<{
      action: 'create' | 'update' | 'access';
      moduleKey?: string;
      moduleType?: ModuleType;
      confidence: number;
    }>;
  }> {
    const modules = userProfile.context.modules || {};
    const relevantModules: string[] = [];
    const suggestedActions: Array<{
      action: 'create' | 'update' | 'access';
      moduleKey?: string;
      moduleType?: ModuleType;
      confidence: number;
    }> = [];

    const queryLower = query.toLowerCase();

    // Check for existing module relevance
    for (const [key, module] of Object.entries(modules)) {
      if (this.isQueryRelevantToModule(query, key, module)) {
        relevantModules.push(key);
        
        // Determine if this should be an update or access
        const shouldUpdate = this.shouldUpdateModule(query, module);
        suggestedActions.push({
          action: shouldUpdate ? 'update' : 'access',
          moduleKey: key,
          confidence: this.calculateRelevanceConfidence(query, key, module)
        });
      }
    }

    // Check for new module creation opportunities
    const newModuleOpportunities = this.detectNewModuleOpportunities(query);
    suggestedActions.push(...newModuleOpportunities);

    return { relevantModules, suggestedActions };
  }

  /**
   * Create a new module based on query analysis
   */
  async createModule(
    userProfile: UserProfile,
    moduleKey: string,
    moduleType: ModuleType,
    initialData: any,
    context?: ModuleUpdateContext
  ): Promise<Module> {
    const now = new Date().toISOString();
    
    const newModule: Module = {
      type: moduleType,
      data: this.initializeModuleData(moduleType, initialData),
      metadata: {
        createdAt: now,
        lastUpdated: now,
        lastAccessed: now,
        priority: 5,
        tags: this.extractTagsFromContext(context),
        archived: false
      }
    } as Module;

    // Initialize modules object if it doesn't exist
    if (!userProfile.context.modules) {
      userProfile.context.modules = {};
    }

    userProfile.context.modules[moduleKey] = newModule;
    
    this.logger.debug(`Created new ${moduleType} module: ${moduleKey}`);
    return newModule;
  }

  /**
   * Update an existing module with new information
   */
  async updateModule(
    userProfile: UserProfile,
    moduleKey: string,
    updateData: any,
    context?: ModuleUpdateContext
  ): Promise<Module | null> {
    const modules = userProfile.context.modules || {};
    const existingModule = modules[moduleKey];

    if (!existingModule) {
      this.logger.warn(`Module ${moduleKey} not found for update`);
      return null;
    }

    const updatedModule = this.applyModuleUpdate(existingModule, updateData, context);
    modules[moduleKey] = updatedModule;

    this.logger.debug(`Updated module: ${moduleKey}`);
    return updatedModule;
  }

  /**
   * Remove or archive old modules based on aging rules
   */
  async cleanupStaleModules(userProfile: UserProfile): Promise<{
    archived: string[];
    removed: string[];
  }> {
    const modules = userProfile.context.modules || {};
    const archived: string[] = [];
    const removed: string[] = [];
    const now = new Date();

    for (const [key, module] of Object.entries(modules)) {
      const lastAccessed = new Date(module.metadata.lastAccessed || module.metadata.lastUpdated);
      const daysSinceAccess = Math.floor((now.getTime() - lastAccessed.getTime()) / (1000 * 60 * 60 * 24));

      // Archive modules not accessed in 30 days
      if (daysSinceAccess > 30 && !module.metadata.archived) {
        module.metadata.archived = true;
        archived.push(key);
      }

      // Remove archived modules not accessed in 90 days
      if (daysSinceAccess > 90 && module.metadata.archived) {
        delete modules[key];
        removed.push(key);
      }
    }

    return { archived, removed };
  }

  /**
   * Get a summary of all user modules for system awareness
   */
  getUserModulesSummary(userProfile: UserProfile): {
    totalModules: number;
    modulesByType: Record<ModuleType, number>;
    activeModules: Array<{ key: string; type: ModuleType; priority: number; lastAccessed: string }>;
    recentlyUpdated: Array<{ key: string; type: ModuleType; lastUpdated: string }>;
  } {
    const modules = userProfile.context.modules || {};
    const modulesByType: Record<ModuleType, number> = {
      list: 0, planner: 0, calendar: 0, interest: 0, tracker: 0, goal: 0
    };

    const activeModules: Array<{ key: string; type: ModuleType; priority: number; lastAccessed: string }> = [];
    const recentlyUpdated: Array<{ key: string; type: ModuleType; lastUpdated: string }> = [];

    for (const [key, module] of Object.entries(modules)) {
      if (!module.metadata.archived) {
        modulesByType[module.type]++;
        
        activeModules.push({
          key,
          type: module.type,
          priority: module.metadata.priority || 5,
          lastAccessed: module.metadata.lastAccessed || module.metadata.lastUpdated
        });

        // Consider recently updated if within last 7 days
        const lastUpdated = new Date(module.metadata.lastUpdated);
        const daysSinceUpdate = Math.floor((Date.now() - lastUpdated.getTime()) / (1000 * 60 * 60 * 24));
        if (daysSinceUpdate <= 7) {
          recentlyUpdated.push({
            key,
            type: module.type,
            lastUpdated: module.metadata.lastUpdated
          });
        }
      }
    }

    // Sort by priority and recent access
    activeModules.sort((a, b) => {
      const priorityDiff = b.priority - a.priority;
      if (priorityDiff !== 0) return priorityDiff;
      return new Date(b.lastAccessed).getTime() - new Date(a.lastAccessed).getTime();
    });

    recentlyUpdated.sort((a, b) => 
      new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime()
    );

    return {
      totalModules: Object.keys(modules).filter(key => !modules[key].metadata.archived).length,
      modulesByType,
      activeModules: activeModules.slice(0, 10), // Top 10 most relevant
      recentlyUpdated: recentlyUpdated.slice(0, 5) // Most recent 5
    };
  }

  /**
   * Check if a query is relevant to an existing module
   */
  private isQueryRelevantToModule(query: string, moduleKey: string, module: Module): boolean {
    const queryLower = query.toLowerCase();
    const keyLower = moduleKey.toLowerCase();

    // Check if module key is mentioned
    if (queryLower.includes(keyLower)) {
      return true;
    }

    // Check module-specific relevance
    switch (module.type) {
      case 'list':
        return this.isQueryRelevantToList(queryLower, module as ListModule);
      case 'planner':
        return this.isQueryRelevantToPlanner(queryLower, module as PlannerModule);
      case 'calendar':
        return this.isQueryRelevantToCalendar(queryLower, module as CalendarModule);
      case 'interest':
        return this.isQueryRelevantToInterest(queryLower, module as InterestModule);
      case 'tracker':
        return this.isQueryRelevantToTracker(queryLower, module as TrackerModule);
      case 'goal':
        return this.isQueryRelevantToGoal(queryLower, module as GoalModule);
      default:
        return false;
    }
  }

  private isQueryRelevantToList(query: string, module: ListModule): boolean {
    const listKeywords = ['add', 'remove', 'list', 'items', 'shopping', 'grocery', 'todo'];
    return listKeywords.some(keyword => query.includes(keyword)) ||
           module.data.some(item => query.includes(item.toLowerCase()));
  }

  private isQueryRelevantToPlanner(query: string, module: PlannerModule): boolean {
    const plannerKeywords = ['party', 'event', 'plan', 'guest', 'invite', 'celebration'];
    return plannerKeywords.some(keyword => query.includes(keyword)) ||
           (module.data.guests && module.data.guests.some(guest => query.includes(guest.toLowerCase())));
  }

  private isQueryRelevantToCalendar(query: string, module: CalendarModule): boolean {
    const calendarKeywords = ['schedule', 'calendar', 'appointment', 'meeting', 'date'];
    return calendarKeywords.some(keyword => query.includes(keyword)) ||
           Object.values(module.data).some(event => query.includes(event.toLowerCase()));
  }

  private isQueryRelevantToInterest(query: string, module: InterestModule): boolean {
    return module.data.keywords.some(keyword => query.includes(keyword.toLowerCase())) ||
           (module.data.relatedTopics && module.data.relatedTopics.some(topic => query.includes(topic.toLowerCase())));
  }

  private isQueryRelevantToTracker(query: string, module: TrackerModule): boolean {
    const trackerKeywords = ['track', 'progress', 'goal', 'target', 'metric'];
    return trackerKeywords.some(keyword => query.includes(keyword)) ||
           query.includes(module.data.metric.toLowerCase());
  }

  private isQueryRelevantToGoal(query: string, module: GoalModule): boolean {
    const goalKeywords = ['goal', 'achieve', 'progress', 'milestone', 'target'];
    return goalKeywords.some(keyword => query.includes(keyword)) ||
           query.includes(module.data.title.toLowerCase());
  }

  private shouldUpdateModule(query: string, module: Module): boolean {
    const updateKeywords = ['add', 'remove', 'update', 'change', 'modify', 'delete', 'complete'];
    return updateKeywords.some(keyword => query.toLowerCase().includes(keyword));
  }

  private calculateRelevanceConfidence(query: string, moduleKey: string, module: Module): number {
    let confidence = 0;

    // Base confidence for key mention
    if (query.toLowerCase().includes(moduleKey.toLowerCase())) {
      confidence += 0.8;
    }

    // Type-specific confidence boosters
    switch (module.type) {
      case 'list':
        if (['add', 'remove', 'list'].some(kw => query.toLowerCase().includes(kw))) {
          confidence += 0.6;
        }
        break;
      case 'planner':
        if (['party', 'event', 'plan'].some(kw => query.toLowerCase().includes(kw))) {
          confidence += 0.6;
        }
        break;
      // Add other types as needed
    }

    return Math.min(confidence, 1.0);
  }

  private detectNewModuleOpportunities(query: string): Array<{
    action: 'create';
    moduleType: ModuleType;
    confidence: number;
  }> {
    const opportunities: Array<{
      action: 'create';
      moduleType: ModuleType;
      confidence: number;
    }> = [];

    const queryLower = query.toLowerCase();

    // List detection
    if (['shopping list', 'grocery list', 'todo list', 'need to buy'].some(phrase => queryLower.includes(phrase))) {
      opportunities.push({ action: 'create', moduleType: 'list', confidence: 0.8 });
    }

    // Planner detection
    if (['party', 'birthday', 'celebration', 'event planning'].some(phrase => queryLower.includes(phrase))) {
      opportunities.push({ action: 'create', moduleType: 'planner', confidence: 0.7 });
    }

    // Calendar detection
    if (['schedule', 'calendar', 'appointments', 'meetings'].some(phrase => queryLower.includes(phrase))) {
      opportunities.push({ action: 'create', moduleType: 'calendar', confidence: 0.6 });
    }

    // Interest detection
    if (['interested in', 'learning about', 'studying', 'fascinated by'].some(phrase => queryLower.includes(phrase))) {
      opportunities.push({ action: 'create', moduleType: 'interest', confidence: 0.5 });
    }

    return opportunities;
  }

  private initializeModuleData(moduleType: ModuleType, initialData: any): any {
    switch (moduleType) {
      case 'list':
        return Array.isArray(initialData) ? initialData : [];
      case 'planner':
        return {
          date: null,
          guests: [],
          tasks: [],
          status: 'planning',
          ...initialData
        };
      case 'calendar':
        return typeof initialData === 'object' ? initialData : {};
      case 'interest':
        return {
          keywords: [],
          engagementLevel: 5,
          relatedTopics: [],
          ...initialData
        };
      case 'tracker':
        return {
          metric: 'unknown',
          history: [],
          ...initialData
        };
      case 'goal':
        return {
          title: 'New Goal',
          progress: 0,
          milestones: [],
          ...initialData
        };
      default:
        return initialData || {};
    }
  }

  private applyModuleUpdate(module: Module, updateData: any, context?: ModuleUpdateContext): Module {
    const updatedModule = { ...module };
    const now = new Date().toISOString();

    updatedModule.metadata = {
      ...updatedModule.metadata,
      lastUpdated: now,
      lastAccessed: now
    };

    switch (module.type) {
      case 'list':
        updatedModule.data = this.updateListData(module.data, updateData, context);
        break;
      case 'planner':
        updatedModule.data = { ...module.data, ...updateData };
        break;
      case 'calendar':
        updatedModule.data = { ...module.data, ...updateData };
        break;
      case 'interest':
        updatedModule.data = this.updateInterestData(module.data, updateData, context);
        break;
      case 'tracker':
        updatedModule.data = this.updateTrackerData(module.data, updateData, context);
        break;
      case 'goal':
        updatedModule.data = this.updateGoalData(module.data, updateData, context);
        break;
    }

    return updatedModule;
  }

  private updateListData(currentData: string[], updateData: any, context?: ModuleUpdateContext): string[] {
    if (context?.query) {
      const query = context.query.toLowerCase();
      
      if (query.includes('add') || query.includes('include')) {
        // Extract items to add
        if (Array.isArray(updateData)) {
          return [...new Set([...currentData, ...updateData])];
        } else if (typeof updateData === 'string') {
          return [...new Set([...currentData, updateData])];
        }
      } else if (query.includes('remove') || query.includes('delete')) {
        // Extract items to remove
        if (Array.isArray(updateData)) {
          return currentData.filter(item => !updateData.includes(item));
        } else if (typeof updateData === 'string') {
          return currentData.filter(item => item !== updateData);
        }
      }
    }

    // Default: replace if array, add if string
    if (Array.isArray(updateData)) {
      return updateData;
    } else if (typeof updateData === 'string') {
      return [...new Set([...currentData, updateData])];
    }

    return currentData;
  }

  private updateInterestData(currentData: any, updateData: any, context?: ModuleUpdateContext): any {
    const updated = { ...currentData };

    if (updateData.keywords) {
      updated.keywords = [...new Set([...updated.keywords, ...updateData.keywords])];
    }

    if (updateData.engagementLevel !== undefined) {
      updated.engagementLevel = updateData.engagementLevel;
    }

    if (context?.query) {
      updated.lastEngagement = new Date().toISOString();
    }

    return updated;
  }

  private updateTrackerData(currentData: any, updateData: any, context?: ModuleUpdateContext): any {
    const updated = { ...currentData };

    if (updateData.currentValue !== undefined) {
      if (!updated.history) updated.history = [];
      updated.history.push({
        date: new Date().toISOString(),
        value: updateData.currentValue,
        notes: context?.query
      });
      updated.currentValue = updateData.currentValue;
    }

    return { ...updated, ...updateData };
  }

  private updateGoalData(currentData: any, updateData: any, context?: ModuleUpdateContext): any {
    const updated = { ...currentData };

    if (updateData.milestones) {
      updated.milestones = updateData.milestones;
    }

    if (updateData.progress !== undefined) {
      updated.progress = Math.max(0, Math.min(100, updateData.progress));
    }

    return { ...updated, ...updateData };
  }

  private extractTagsFromContext(context?: ModuleUpdateContext): string[] {
    if (!context?.query) return [];

    const tags: string[] = [];
    const query = context.query.toLowerCase();

    // Extract common tags based on query content
    if (query.includes('urgent') || query.includes('important')) tags.push('urgent');
    if (query.includes('work') || query.includes('job')) tags.push('work');
    if (query.includes('personal') || query.includes('family')) tags.push('personal');
    if (query.includes('health') || query.includes('fitness')) tags.push('health');

    return tags;
  }
}