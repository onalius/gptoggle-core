/**
 * Universal Module Identifier (UMID) Generator - TypeScript Implementation
 * 
 * This module provides a standardized system for generating globally unique
 * identifiers for adaptive intelligence modules across any service or platform.
 * 
 * Format: {service}.{moduleType}.{contextHash}.{timestamp}.{random}
 * Example: gptoggle.list.a1b2c3d4.1721737200.x7z9
 */

import crypto from 'crypto';

export interface ParsedUMID {
  service: string;
  moduleType: string;
  contextHash: string;
  timestamp: number;
  createdAt: string;
  random: string;
  full: string;
}

export interface ModuleData {
  type: string;
  keywords: string[];
}

export class UMIDGenerator {
  private serviceId: string;
  private static readonly SERVICE_PATTERN = /^[a-z0-9-]{3,20}$/;
  private static readonly MODULE_TYPE_PATTERN = /^[a-z]+$/;

  constructor(serviceId: string) {
    if (!this.validateServiceId(serviceId)) {
      throw new Error(`Invalid service_id: ${serviceId}. Must be 3-20 chars, lowercase alphanumeric with hyphens`);
    }
    this.serviceId = serviceId.toLowerCase();
  }

  private validateServiceId(serviceId: string): boolean {
    return UMIDGenerator.SERVICE_PATTERN.test(serviceId);
  }

  /**
   * Generate 8-character context hash from keywords
   */
  generateContextHash(keywords: string[]): string {
    if (!keywords || keywords.length === 0) {
      keywords = ['default'];
    }

    // Normalize and sort keywords for consistent hashing
    const contextString = keywords
      .map(k => k.toLowerCase().trim())
      .filter(k => k.length > 0)
      .sort()
      .join(' ');

    // Generate SHA-256 hash and truncate to 8 characters
    return crypto
      .createHash('sha256')
      .update(contextString, 'utf8')
      .digest('hex')
      .substring(0, 8);
  }

  /**
   * Generate 4-character random component
   */
  generateRandomComponent(): string {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 4; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * Generate complete Universal Module Identifier
   */
  generateUMID(moduleType: string, contextKeywords: string[]): string {
    // Validate module type
    if (!UMIDGenerator.MODULE_TYPE_PATTERN.test(moduleType)) {
      throw new Error(`Invalid module_type: ${moduleType}. Must be lowercase alphabetic`);
    }

    // Generate components
    const contextHash = this.generateContextHash(contextKeywords);
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const randomComponent = this.generateRandomComponent();

    // Combine into UMID
    return `${this.serviceId}.${moduleType}.${contextHash}.${timestamp}.${randomComponent}`;
  }

  /**
   * Generate multiple UMIDs efficiently
   */
  generateBatchUMIDs(modulesData: ModuleData[]): string[] {
    return modulesData.map(moduleData => 
      this.generateUMID(moduleData.type, moduleData.keywords)
    );
  }
}

export class UMIDParser {
  private static readonly UMID_PATTERN = /^([a-z0-9-]{3,20})\.([a-z]+)\.([a-f0-9]{8})\.(\d{10})\.([a-z0-9]{4})$/;

  /**
   * Parse UMID into components
   */
  static parse(umid: string): ParsedUMID | null {
    const match = umid.match(this.UMID_PATTERN);
    if (!match) {
      return null;
    }

    const timestamp = parseInt(match[4]);
    const createdAt = new Date(timestamp * 1000).toISOString();

    return {
      service: match[1],
      moduleType: match[2],
      contextHash: match[3],
      timestamp,
      createdAt,
      random: match[5],
      full: umid
    };
  }

  /**
   * Validate UMID format
   */
  static validate(umid: string): boolean {
    return this.UMID_PATTERN.test(umid);
  }

  /**
   * Extract service ID from UMID
   */
  static extractService(umid: string): string | null {
    const parsed = this.parse(umid);
    return parsed ? parsed.service : null;
  }

  /**
   * Extract module type from UMID
   */
  static extractType(umid: string): string | null {
    const parsed = this.parse(umid);
    return parsed ? parsed.moduleType : null;
  }

  /**
   * Extract timestamp from UMID
   */
  static extractTimestamp(umid: string): number | null {
    const parsed = this.parse(umid);
    return parsed ? parsed.timestamp : null;
  }
}

export class UMIDMigrator {
  private generator: UMIDGenerator;

  constructor(serviceId: string) {
    this.generator = new UMIDGenerator(serviceId);
  }

  /**
   * Migrate existing GPToggle modules to UMID format
   */
  migrateGPToggleModules(existingModules: Record<string, any>): Record<string, any> {
    const migrated: Record<string, any> = {};

    for (const [oldKey, module] of Object.entries(existingModules)) {
      // Extract context from module data
      const contextKeywords = this.extractKeywordsFromModule(module, oldKey);
      const moduleType = module.type || 'custom';

      // Generate new UMID
      const newUMID = this.generator.generateUMID(moduleType, contextKeywords);

      // Preserve original data with new ID and migration info
      migrated[newUMID] = {
        ...module,
        umid: newUMID,
        migratedFrom: oldKey,
        migrationTimestamp: Math.floor(Date.now() / 1000)
      };
    }

    return migrated;
  }

  private extractKeywordsFromModule(module: any, oldKey: string): string[] {
    const keywords: string[] = [];

    // Try to get keywords from module data
    if (module.data && typeof module.data === 'object') {
      const data = module.data;
      
      // Look for common fields
      if (data.title && typeof data.title === 'string') {
        keywords.push(...data.title.split(/\s+/));
      }
      if (data.name && typeof data.name === 'string') {
        keywords.push(...data.name.split(/\s+/));
      }
      if (Array.isArray(data.tags)) {
        keywords.push(...data.tags.filter(tag => typeof tag === 'string'));
      }
    }

    // If no keywords found, use parts of old key
    if (keywords.length === 0) {
      // Remove common suffixes
      let cleanKey = oldKey.replace(/(List|Planner|Calendar|Interest|Tracker|Goal)$/i, '');
      // Remove non-alphabetic characters and split
      cleanKey = cleanKey.replace(/[^a-zA-Z\s]/g, ' ');
      const keyWords = cleanKey
        .split(/\s+/)
        .map(word => word.toLowerCase())
        .filter(word => word.length > 2);
      keywords.push(...keyWords);
    }

    // Ensure we have at least one keyword
    if (keywords.length === 0) {
      keywords.push('module');
    }

    // Limit to 5 keywords for reasonable hash
    return keywords.slice(0, 5);
  }
}

// Demo and testing functions
export function demoUMIDGeneration(): void {
  console.log('='.repeat(60));
  console.log('Universal Module Identifier (UMID) Generation Demo');
  console.log('='.repeat(60));

  // Create generators for different services
  const gptoggleGen = new UMIDGenerator('gptoggle');
  const chatgptGen = new UMIDGenerator('chatgpt');
  const notionGen = new UMIDGenerator('notion');
  const customGen = new UMIDGenerator('my-custom-app');

  // Generate various UMIDs
  const examples: Array<[UMIDGenerator, string, string[]]> = [
    [gptoggleGen, 'list', ['shopping', 'groceries', 'weekly']],
    [gptoggleGen, 'planner', ['birthday', 'party', 'alice']],
    [chatgptGen, 'interest', ['python', 'programming', 'learning']],
    [notionGen, 'tracker', ['habit', 'exercise', 'daily']],
    [customGen, 'goal', ['career', 'promotion', 'manager']],
    [gptoggleGen, 'calendar', ['meeting', 'standup', 'team']]
  ];

  console.log('\n📋 Generated UMIDs:');
  examples.forEach(([generator, moduleType, keywords]) => {
    const umid = generator.generateUMID(moduleType, keywords);
    console.log(`   ${umid}`);
    
    // Parse and display components
    const parsed = UMIDParser.parse(umid);
    if (parsed) {
      console.log(`      → Service: ${parsed.service}`);
      console.log(`      → Type: ${parsed.moduleType}`);
      console.log(`      → Context: ${parsed.contextHash}`);
      console.log(`      → Created: ${parsed.createdAt}`);
      console.log();
    }
  });

  // Demonstrate validation
  console.log('🔍 Validation Examples:');
  const validUMID = gptoggleGen.generateUMID('list', ['test']);
  const invalidUMID = 'invalid.format.here';

  console.log(`   Valid: ${UMIDParser.validate(validUMID)} - ${validUMID}`);
  console.log(`   Invalid: ${UMIDParser.validate(invalidUMID)} - ${invalidUMID}`);

  // Demonstrate batch generation
  console.log('\n⚡ Batch Generation:');
  const batchData: ModuleData[] = [
    { type: 'list', keywords: ['homework', 'assignments'] },
    { type: 'tracker', keywords: ['water', 'intake', 'health'] },
    { type: 'goal', keywords: ['fitness', 'marathon', 'training'] }
  ];

  const batchUMIDs = gptoggleGen.generateBatchUMIDs(batchData);
  batchUMIDs.forEach((umid, index) => {
    console.log(`   ${index + 1}. ${umid}`);
  });

  console.log('\n✅ UMID Generation Demo Complete!');
  console.log('   Ready for adoption by any service or platform!');
}

// Browser-compatible version (when crypto module is not available)
export class BrowserUMIDGenerator {
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

    // Simple hash function for browser environments
    let hash = 0;
    for (let i = 0; i < contextString.length; i++) {
      const char = contextString.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    
    // Convert to hex and pad to 8 characters
    return Math.abs(hash).toString(16).padStart(8, '0').substring(0, 8);
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
    if (!/^[a-z]+$/.test(moduleType)) {
      throw new Error(`Invalid module_type: ${moduleType}`);
    }

    const contextHash = this.generateContextHash(contextKeywords);
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const randomComponent = this.generateRandomComponent();

    return `${this.serviceId}.${moduleType}.${contextHash}.${timestamp}.${randomComponent}`;
  }
}

export default {
  UMIDGenerator,
  UMIDParser,
  UMIDMigrator,
  BrowserUMIDGenerator,
  demoUMIDGeneration
};