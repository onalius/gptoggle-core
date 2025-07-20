/**
 * Configuration utilities for GPToggle
 * 
 * @version 2.0.0
 */

export interface GPToggleConfig {
  defaultTemperature: number;
  defaultMaxTokens: number;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  cacheProfiles: boolean;
  profileStorageType: 'memory' | 'file' | 'database';
  profileStorageOptions?: {
    directory?: string;
    connectionString?: string;
  };
}

export const defaultConfig: GPToggleConfig = {
  defaultTemperature: 0.7,
  defaultMaxTokens: 1000,
  logLevel: 'info',
  cacheProfiles: true,
  profileStorageType: 'memory'
};

export class Config {
  private config: GPToggleConfig;

  constructor(config: Partial<GPToggleConfig> = {}) {
    this.config = { ...defaultConfig, ...config };
  }

  get<K extends keyof GPToggleConfig>(key: K): GPToggleConfig[K] {
    return this.config[key];
  }

  set<K extends keyof GPToggleConfig>(key: K, value: GPToggleConfig[K]): void {
    this.config[key] = value;
  }

  getAll(): GPToggleConfig {
    return { ...this.config };
  }

  update(updates: Partial<GPToggleConfig>): void {
    this.config = { ...this.config, ...updates };
  }
}