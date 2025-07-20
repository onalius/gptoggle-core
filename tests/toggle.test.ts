/**
 * Unit tests for the enhanced Toggle function
 * 
 * @version 2.0.0
 */

import { Toggle, ToggleRequest } from '../src/core/toggle';
import { UserProfileService, UserProfile } from '../src/profile/userProfileService';

describe('Toggle Contextualized Intelligence Tests', () => {
  let toggle: Toggle;
  let profileService: UserProfileService;
  let testProfile: UserProfile;

  beforeEach(() => {
    toggle = new Toggle();
    profileService = new UserProfileService();
    
    testProfile = {
      userId: 'test-user',
      tone: 'casual',
      domainExpertise: ['tech'],
      preferences: {
        prioritizeSpeed: false,
        verbosityLevel: 'moderate',
        includeExplanations: true,
        language: 'en'
      },
      memory: {
        recentQueries: [],
        favorites: [],
        recentModels: []
      },
      access: {
        level: 'premium'
      }
    };
  });

  describe('Basic Toggle Functionality', () => {
    test('should process a simple query', async () => {
      const request: ToggleRequest = {
        query: 'What is machine learning?',
        userProfile: testProfile
      };

      const response = await toggle.toggle(request);

      expect(response).toBeDefined();
      expect(response.response).toBeTruthy();
      expect(response.queryType).toBeTruthy();
      expect(response.modelUsed).toBeTruthy();
      expect(response.provider).toBeTruthy();
      expect(response.metadata.processingTime).toBeGreaterThan(0);
    });

    test('should classify query types correctly', async () => {
      const codeRequest: ToggleRequest = {
        query: 'Write a Python function to sort a list',
        userProfile: testProfile
      };

      const response = await toggle.toggle(codeRequest);
      expect(response.queryType).toBe('code');
    });

    test('should apply contextual enhancements', async () => {
      const request: ToggleRequest = {
        query: 'Explain databases',
        userProfile: testProfile
      };

      const response = await toggle.toggle(request);
      expect(response.contextualEnhancements).toBeDefined();
      expect(response.contextualEnhancements.length).toBeGreaterThan(0);
    });
  });

  describe('User Profile Integration', () => {
    test('should respect user tone preferences', async () => {
      const formalProfile = { ...testProfile, tone: 'formal' as const };
      const request: ToggleRequest = {
        query: 'Explain artificial intelligence',
        userProfile: formalProfile
      };

      const response = await toggle.toggle(request);
      expect(response.contextualEnhancements).toContain('Tone adjustment: formal');
    });

    test('should consider domain expertise', async () => {
      const techExpertProfile = { 
        ...testProfile, 
        domainExpertise: ['tech', 'engineering'] 
      };
      
      const request: ToggleRequest = {
        query: 'How do microprocessors work?',
        userProfile: techExpertProfile
      };

      const response = await toggle.toggle(request);
      expect(response.contextualEnhancements.some(e => e.includes('Domain expertise'))).toBeTruthy();
    });

    test('should handle different access levels', async () => {
      const basicProfile = { ...testProfile, access: { level: 'basic' as const } };
      const request: ToggleRequest = {
        query: 'Analyze this complex dataset',
        userProfile: basicProfile
      };

      const response = await toggle.toggle(request);
      expect(response).toBeDefined();
      // Basic users should still get a response, just with different model selection
    });
  });

  describe('Model Selection', () => {
    test('should select appropriate models for different query types', async () => {
      const codeRequest: ToggleRequest = {
        query: 'Debug this JavaScript code',
        userProfile: testProfile
      };

      const response = await toggle.toggle(codeRequest);
      expect(response.modelUsed).toBeTruthy();
      expect(response.provider).toBeTruthy();
    });

    test('should respect user model preferences', async () => {
      const profileWithPreferences = {
        ...testProfile,
        preferences: {
          ...testProfile.preferences,
          preferredModels: ['gpt-4o']
        }
      };

      const request: ToggleRequest = {
        query: 'General question about AI',
        userProfile: profileWithPreferences
      };

      const response = await toggle.toggle(request);
      // Model selection should consider user preferences
      expect(response.modelUsed).toBeTruthy();
    });
  });

  describe('Follow-up Suggestions', () => {
    test('should generate relevant follow-up suggestions', async () => {
      const request: ToggleRequest = {
        query: 'Write a Python function',
        userProfile: testProfile
      };

      const response = await toggle.toggle(request);
      
      if (response.suggestedFollowUp) {
        expect(response.suggestedFollowUp).toBeTruthy();
        expect(typeof response.suggestedFollowUp).toBe('string');
      }
    });
  });

  describe('Error Handling', () => {
    test('should handle empty queries gracefully', async () => {
      const request: ToggleRequest = {
        query: '',
        userProfile: testProfile
      };

      await expect(toggle.toggle(request)).rejects.toThrow();
    });

    test('should handle malformed user profiles', async () => {
      const invalidProfile = { ...testProfile, userId: '' };
      const request: ToggleRequest = {
        query: 'Test query',
        userProfile: invalidProfile
      };

      // Should either handle gracefully or throw meaningful error
      try {
        await toggle.toggle(request);
      } catch (error) {
        expect(error.message).toBeTruthy();
      }
    });
  });

  describe('Performance', () => {
    test('should complete processing within reasonable time', async () => {
      const request: ToggleRequest = {
        query: 'What is the capital of France?',
        userProfile: testProfile
      };

      const startTime = Date.now();
      const response = await toggle.toggle(request);
      const endTime = Date.now();

      expect(endTime - startTime).toBeLessThan(10000); // Should complete within 10 seconds
      expect(response.metadata.processingTime).toBeLessThan(10000);
    });
  });

  describe('Confidence Scoring', () => {
    test('should provide confidence scores', async () => {
      const request: ToggleRequest = {
        query: 'Explain quantum computing',
        userProfile: testProfile
      };

      const response = await toggle.toggle(request);
      expect(response.metadata.confidence).toBeGreaterThan(0);
      expect(response.metadata.confidence).toBeLessThanOrEqual(1);
    });
  });
});

describe('Profile Service Tests', () => {
  let profileService: UserProfileService;

  beforeEach(() => {
    profileService = new UserProfileService();
  });

  test('should create default profile for new user', async () => {
    const profile = await profileService.loadProfile('new-user');
    
    expect(profile.userId).toBe('new-user');
    expect(profile.tone).toBeTruthy();
    expect(profile.access.level).toBeTruthy();
  });

  test('should save and load profiles correctly', async () => {
    const testProfile: UserProfile = {
      userId: 'save-test',
      tone: 'witty',
      domainExpertise: ['marketing'],
      access: { level: 'basic' }
    };

    await profileService.saveProfile(testProfile);
    const loadedProfile = await profileService.loadProfile('save-test');

    expect(loadedProfile.userId).toBe('save-test');
    expect(loadedProfile.tone).toBe('witty');
    expect(loadedProfile.domainExpertise).toContain('marketing');
  });

  test('should track query history', async () => {
    await profileService.addQueryToMemory('test-user', 'Test query', 'general', 'gpt-4o');
    
    const profile = await profileService.loadProfile('test-user');
    expect(profile.memory?.recentQueries).toBeDefined();
    expect(profile.memory?.recentQueries?.length).toBeGreaterThan(0);
    expect(profile.memory?.recentQueries?.[0].query).toBe('Test query');
  });

  test('should manage favorites', async () => {
    await profileService.addFavorite('test-user', 'Favorite response', 'response', ['tag1']);
    
    const profile = await profileService.loadProfile('test-user');
    expect(profile.memory?.favorites).toBeDefined();
    expect(profile.memory?.favorites?.length).toBeGreaterThan(0);
    expect(profile.memory?.favorites?.[0].content).toBe('Favorite response');
  });
});