/**
 * Model Metadata Management for GPToggle
 * 
 * This file provides TypeScript definitions and helper functions for managing
 * AI model metadata including pricing, capabilities, and context windows.
 * 
 * @version 2.0.0
 */

export interface ModelMetadata {
  modelId: string;
  displayName: string;
  description: string;
  contextWindow: number;
  hasVision: boolean;
  inputCostPerMillionTokens: string;
  outputCostPerMillionTokens: string;
  provider: string;
  capabilities?: string[];
  intelligence?: number;
  speed?: number;
  tiers?: string[];
}

/**
 * Helper function to get display name from model ID
 */
export const getDisplayNameFromModelId = (modelId: string): string => {
  const displayNames: Record<string, string> = {
    // OpenAI models
    'gpt-3.5-turbo': 'GPT-3.5 Turbo',
    'gpt-4': 'GPT-4',
    'gpt-4o': 'GPT-4o',
    'gpt-4o-mini': 'GPT-4o Mini',
    'gpt-4-turbo': 'GPT-4 Turbo',
    'gpt-4-vision': 'GPT-4 Vision',
    
    // Anthropic models
    'claude-instant-1': 'Claude Instant',
    'claude-2': 'Claude 2',
    'claude-3-opus': 'Claude 3 Opus',
    'claude-3-sonnet': 'Claude 3 Sonnet',
    'claude-3-haiku': 'Claude 3 Haiku',
    'claude-3-5-sonnet': 'Claude 3.5 Sonnet',
    
    // Google models
    'gemini-1.0-pro': 'Gemini 1.0 Pro',
    'gemini-1.5-flash': 'Gemini 1.5 Flash',
    'gemini-1.5-pro': 'Gemini 1.5 Pro',
    'gemini-pro': 'Gemini Pro',
    'gemini-pro-vision': 'Gemini Pro Vision',
    
    // xAI models
    'grok-1': 'Grok 1',
    'grok-2': 'Grok 2',
    'grok-2-vision': 'Grok 2 Vision',
    'grok-beta': 'Grok Beta',
    'grok-2-1212': 'Grok 2 (Dec 2024)',
    'grok-2-vision-1212': 'Grok 2 Vision (Dec 2024)'
  };
  
  return displayNames[modelId] || modelId.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
};

/**
 * Helper function to get context window by model and provider
 */
export const getContextWindowByModel = (modelId: string, provider: string): number => {
  const contextWindows: Record<string, Record<string, number>> = {
    'openai': {
      'gpt-3.5-turbo': 16385,
      'gpt-4': 8192,
      'gpt-4o': 128000,
      'gpt-4o-mini': 128000,
      'gpt-4-turbo': 128000,
      'gpt-4-vision': 128000,
      'default': 8192
    },
    'anthropic': {
      'claude-instant-1': 100000,
      'claude-2': 100000,
      'claude-3-opus': 200000,
      'claude-3-sonnet': 200000,
      'claude-3-haiku': 200000,
      'claude-3-5-sonnet': 200000,
      'default': 100000
    },
    'google': {
      'gemini-1.0-pro': 32768,
      'gemini-1.5-flash': 1048576,
      'gemini-1.5-pro': 2097152,
      'gemini-pro': 32768,
      'gemini-pro-vision': 32768,
      'default': 32768
    },
    'xai': {
      'grok-1': 131072,
      'grok-2': 131072,
      'grok-2-vision': 131072,
      'grok-beta': 131072,
      'grok-2-1212': 131072,
      'grok-2-vision-1212': 131072,
      'default': 131072
    }
  };
  
  const providerWindows = contextWindows[provider] || {};
  return providerWindows[modelId] || providerWindows['default'] || 8192;
};

/**
 * Helper function to get model description
 */
export const getDescriptionByModel = (modelId: string, provider: string): string => {
  const descriptions: Record<string, Record<string, string>> = {
    'openai': {
      'gpt-3.5-turbo': 'Fast, cost-effective model for simple tasks',
      'gpt-4': 'Advanced reasoning and complex task handling',
      'gpt-4o': 'Latest multimodal model with vision and advanced reasoning',
      'gpt-4o-mini': 'Smaller, faster version of GPT-4o',
      'gpt-4-turbo': 'High-performance version of GPT-4',
      'gpt-4-vision': 'GPT-4 with image analysis capabilities',
      'default': 'OpenAI language model'
    },
    'anthropic': {
      'claude-instant-1': 'Fast, affordable model for simple tasks',
      'claude-2': 'Balanced model for complex reasoning',
      'claude-3-opus': 'Most capable model for complex tasks',
      'claude-3-sonnet': 'Balanced performance and speed',
      'claude-3-haiku': 'Fastest model for simple tasks',
      'claude-3-5-sonnet': 'Enhanced version with improved capabilities',
      'default': 'Anthropic Claude model'
    },
    'google': {
      'gemini-1.0-pro': 'Google\'s multimodal AI model',
      'gemini-1.5-flash': 'Fast, efficient model for quick tasks',
      'gemini-1.5-pro': 'Advanced model with large context window',
      'gemini-pro': 'General-purpose multimodal model',
      'gemini-pro-vision': 'Specialized for image understanding',
      'default': 'Google Gemini model'
    },
    'xai': {
      'grok-1': 'xAI\'s conversational AI model',
      'grok-2': 'Enhanced version with improved capabilities',
      'grok-2-vision': 'Multimodal version with image understanding',
      'grok-beta': 'Beta version of Grok',
      'grok-2-1212': 'December 2024 version of Grok 2',
      'grok-2-vision-1212': 'December 2024 version of Grok 2 Vision',
      'default': 'xAI Grok model'
    }
  };
  
  const providerDescriptions = descriptions[provider] || {};
  return providerDescriptions[modelId] || providerDescriptions['default'] || `${provider} AI model`;
};

/**
 * Get input cost per million tokens
 */
export const getInputCostByModel = (modelId: string, provider: string): string => {
  const costs: Record<string, Record<string, string>> = {
    'openai': {
      'gpt-3.5-turbo': '1.50',
      'gpt-4': '10.00',
      'gpt-4o': '10.00',
      'gpt-4o-mini': '5.00',
      'gpt-4-turbo': '10.00',
      'gpt-4-vision': '10.00',
      'default': '10.00'
    },
    'anthropic': {
      'claude-instant-1': '2.00',
      'claude-2': '8.00', 
      'claude-3-opus': '15.00',
      'claude-3-sonnet': '7.50',
      'claude-3-haiku': '3.00',
      'claude-3-5-sonnet': '8.00',
      'default': '8.00'
    },
    'google': {
      'gemini-1.0-pro': '2.50',
      'gemini-1.5-flash': '3.50',
      'gemini-1.5-pro': '10.00',
      'gemini-pro': '2.50',
      'gemini-pro-vision': '2.50',
      'default': '5.00'
    },
    'xai': {
      'grok-1': '5.00',
      'grok-2': '10.00',
      'grok-2-vision': '15.00',
      'grok-beta': '5.00',
      'grok-2-1212': '10.00',
      'grok-2-vision-1212': '15.00',
      'default': '10.00'
    }
  };
  
  const providerCosts = costs[provider] || {};
  return providerCosts[modelId] || providerCosts['default'] || '10.00';
};

/**
 * Get output cost per million tokens
 */
export const getOutputCostByModel = (modelId: string, provider: string): string => {
  const costs: Record<string, Record<string, string>> = {
    'openai': {
      'gpt-3.5-turbo': '2.00',
      'gpt-4': '30.00',
      'gpt-4o': '30.00',
      'gpt-4o-mini': '15.00',
      'gpt-4-turbo': '30.00',
      'gpt-4-vision': '30.00',
      'default': '30.00'
    },
    'anthropic': {
      'claude-instant-1': '6.00',
      'claude-2': '24.00',
      'claude-3-opus': '75.00',
      'claude-3-sonnet': '24.00',
      'claude-3-haiku': '15.00',
      'claude-3-5-sonnet': '24.00',
      'default': '24.00'
    },
    'google': {
      'gemini-1.0-pro': '7.50',
      'gemini-1.5-flash': '10.50',
      'gemini-1.5-pro': '30.00',
      'gemini-pro': '7.50',
      'gemini-pro-vision': '7.50',
      'default': '15.00'
    },
    'xai': {
      'grok-1': '15.00',
      'grok-2': '30.00',
      'grok-2-vision': '45.00',
      'grok-beta': '15.00',
      'grok-2-1212': '30.00',
      'grok-2-vision-1212': '45.00',
      'default': '30.00'
    }
  };
  
  const providerCosts = costs[provider] || {};
  return providerCosts[modelId] || providerCosts['default'] || '30.00';
};

/**
 * Provider-specific metadata fetchers
 */
export const fetchOpenAIModelMetadata = async (modelId: string): Promise<ModelMetadata | null> => {
  try {
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
    if (!OPENAI_API_KEY) {
      throw new Error('OpenAI API key not configured');
    }
    
    const modelData: ModelMetadata = {
      modelId,
      displayName: getDisplayNameFromModelId(modelId),
      contextWindow: getContextWindowByModel(modelId, 'openai'),
      hasVision: modelId.includes('vision') || modelId.includes('gpt-4o'),
      description: getDescriptionByModel(modelId, 'openai'),
      inputCostPerMillionTokens: getInputCostByModel(modelId, 'openai'),
      outputCostPerMillionTokens: getOutputCostByModel(modelId, 'openai'),
      provider: 'openai'
    };
    
    return modelData;
  } catch (error) {
    console.error('Error fetching OpenAI model metadata:', error);
    return null;
  }
};

export const fetchAnthropicModelMetadata = async (modelId: string): Promise<ModelMetadata | null> => {
  try {
    const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
    if (!ANTHROPIC_API_KEY) {
      throw new Error('Anthropic API key not configured');
    }
    
    const modelData: ModelMetadata = {
      modelId,
      displayName: getDisplayNameFromModelId(modelId),
      contextWindow: getContextWindowByModel(modelId, 'anthropic'),
      hasVision: modelId.includes('vision') || modelId.includes('opus') || modelId.includes('sonnet'),
      description: getDescriptionByModel(modelId, 'anthropic'),
      inputCostPerMillionTokens: getInputCostByModel(modelId, 'anthropic'),
      outputCostPerMillionTokens: getOutputCostByModel(modelId, 'anthropic'),
      provider: 'anthropic'
    };
    
    return modelData;
  } catch (error) {
    console.error('Error fetching Anthropic model metadata:', error);
    return null;
  }
};

export const fetchGoogleModelMetadata = async (modelId: string): Promise<ModelMetadata | null> => {
  try {
    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON) {
      throw new Error('Google AI credentials not configured');
    }
    
    const modelData: ModelMetadata = {
      modelId,
      displayName: getDisplayNameFromModelId(modelId),
      contextWindow: getContextWindowByModel(modelId, 'google'),
      hasVision: modelId.includes('vision') || modelId.includes('gemini'),
      description: getDescriptionByModel(modelId, 'google'),
      inputCostPerMillionTokens: getInputCostByModel(modelId, 'google'),
      outputCostPerMillionTokens: getOutputCostByModel(modelId, 'google'),
      provider: 'google'
    };
    
    return modelData;
  } catch (error) {
    console.error('Error fetching Google model metadata:', error);
    return null;
  }
};

export const fetchXAIModelMetadata = async (modelId: string): Promise<ModelMetadata | null> => {
  try {
    const XAI_API_KEY = process.env.XAI_API_KEY;
    if (!XAI_API_KEY) {
      throw new Error('xAI/Grok API key not configured');
    }
    
    const modelData: ModelMetadata = {
      modelId,
      displayName: getDisplayNameFromModelId(modelId),
      contextWindow: getContextWindowByModel(modelId, 'xai'),
      hasVision: modelId.includes('vision'),
      description: getDescriptionByModel(modelId, 'xai'),
      inputCostPerMillionTokens: getInputCostByModel(modelId, 'xai'),
      outputCostPerMillionTokens: getOutputCostByModel(modelId, 'xai'),
      provider: 'xai'
    };
    
    return modelData;
  } catch (error) {
    console.error('Error fetching xAI/Grok model metadata:', error);
    return null;
  }
};

/**
 * Generate default metadata for unknown models
 */
export const generateDefaultMetadata = (modelId: string, provider: string): ModelMetadata => {
  // Attempt to determine if it has vision capabilities
  const hasVision = modelId.toLowerCase().includes('vision') || 
                    modelId.toLowerCase().includes('gpt-4o') || 
                    modelId.toLowerCase().includes('claude-3') || 
                    modelId.toLowerCase().includes('gemini') ||
                    modelId.toLowerCase().includes('grok-vision');
                    
  // Estimate context window based on model name patterns
  let contextWindow = 8192; // Default conservative estimate
  if (modelId.includes('32k') || modelId.includes('32-k')) {
    contextWindow = 32768;
  } else if (modelId.includes('128k') || modelId.includes('128-k')) {
    contextWindow = 128000;
  } else if (modelId.includes('gpt-4') || modelId.includes('gpt4')) {
    contextWindow = 8192; // Default for GPT-4 series
  } else if (modelId.includes('gpt-4o') || modelId.includes('gpt4o')) {
    contextWindow = 128000; // Default for GPT-4o series
  } else if (modelId.includes('claude-3') || modelId.includes('claude3')) {
    contextWindow = 100000; // Default for Claude 3 series  
  } else if (modelId.includes('gemini-1.5-pro')) {
    contextWindow = 1000000; // Gemini 1.5 Pro's 1M context
  } else if (modelId.includes('gemini')) {
    contextWindow = 32000; // Default for other Gemini models
  }
  
  return {
    modelId,
    displayName: getDisplayNameFromModelId(modelId),
    description: `${provider.charAt(0).toUpperCase() + provider.slice(1)} AI model`,
    contextWindow,
    hasVision,
    inputCostPerMillionTokens: getInputCostByModel(modelId, provider),
    outputCostPerMillionTokens: getOutputCostByModel(modelId, provider),
    provider
  };
};