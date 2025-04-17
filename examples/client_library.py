#!/usr/bin/env python3
"""
GPToggle Client Library for Python

This library provides a simple way to connect to a GPToggle REST API
from Python applications.
"""

import os
import json
import requests

class GPToggleClient:
    """Client for the GPToggle REST API."""
    
    def __init__(self, api_url=None):
        """
        Initialize the GPToggle client.
        
        Args:
            api_url (str, optional): The URL of the GPToggle API (without trailing slash).
                If not provided, will use the GPTOGGLE_API_URL environment variable.
        
        Raises:
            ValueError: If no API URL is provided and the GPTOGGLE_API_URL environment variable is not set.
        """
        # Use the provided API URL or check environment variable
        self.api_url = api_url or os.environ.get('GPTOGGLE_API_URL')
        
        if not self.api_url:
            raise ValueError('GPToggle API URL is required. Either provide it as a parameter or set the GPTOGGLE_API_URL environment variable.')
        
        # Remove trailing slash if present
        self.api_url = self.api_url.rstrip('/')
        
        # Add /api if not present
        if not self.api_url.endswith('/api'):
            self.api_url = f"{self.api_url}/api"
    
    def get_providers(self):
        """
        Get a list of available providers.
        
        Returns:
            list: A list of provider names.
            
        Raises:
            Exception: If the API request fails.
        """
        response = requests.get(f"{self.api_url}/providers")
        data = response.json()
        
        if not data.get('success'):
            raise Exception(data.get('error', 'Failed to get providers'))
        
        return data['providers']
    
    def get_models(self, provider='openai'):
        """
        Get a list of available models for a provider.
        
        Args:
            provider (str, optional): The provider name. Defaults to 'openai'.
            
        Returns:
            list: A list of model names.
            
        Raises:
            Exception: If the API request fails.
        """
        response = requests.get(f"{self.api_url}/models", params={'provider': provider})
        data = response.json()
        
        if not data.get('success'):
            raise Exception(data.get('error', f'Failed to get models for provider {provider}'))
        
        return data['models']
    
    def recommend_model(self, prompt):
        """
        Get a recommended model for a prompt.
        
        Args:
            prompt (str): The prompt to get a recommendation for.
            
        Returns:
            str: The recommended model in the format "provider:model".
            
        Raises:
            Exception: If the API request fails.
        """
        response = requests.post(
            f"{self.api_url}/recommend",
            json={'prompt': prompt}
        )
        data = response.json()
        
        if not data.get('success'):
            raise Exception(data.get('error', 'Failed to get recommendation'))
        
        return data['model']
    
    def generate_response(self, prompt, provider=None, model=None, temperature=0.7, max_tokens=1000):
        """
        Generate a response for a prompt.
        
        Args:
            prompt (str): The prompt to generate a response for.
            provider (str, optional): The provider to use. If not provided, will be auto-selected.
            model (str, optional): The model to use. If not provided, will be auto-selected.
            temperature (float, optional): The temperature to use. Defaults to 0.7.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1000.
            
        Returns:
            str: The generated response.
            
        Raises:
            Exception: If the API request fails.
        """
        response = requests.post(
            f"{self.api_url}/generate",
            json={
                'prompt': prompt,
                'provider': provider,
                'model': model,
                'temperature': temperature,
                'max_tokens': max_tokens
            }
        )
        data = response.json()
        
        if not data.get('success'):
            raise Exception(data.get('error', 'Failed to generate response'))
        
        return data['response']


# Example usage:
"""
# Create a client
client = GPToggleClient('https://your-gptoggle-api.domain.com')

# Get available providers
providers = client.get_providers()
print('Available providers:', providers)

# Get a recommended model
model = client.recommend_model('What is the meaning of life?')
print('Recommended model:', model)

# Generate a response
response = client.generate_response('What is the meaning of life?')
print('Response:', response)
"""

if __name__ == "__main__":
    # Only run this code if the script is run directly
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python client_library.py <api_url> <prompt>")
        sys.exit(1)
    
    api_url = sys.argv[1]
    prompt = sys.argv[2]
    
    try:
        client = GPToggleClient(api_url)
        response = client.generate_response(prompt)
        print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)