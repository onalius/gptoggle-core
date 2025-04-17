# GPToggle REST API Documentation

This document provides detailed information about the GPToggle REST API endpoints, parameters, and response formats.

## Overview

The GPToggle REST API allows you to access multiple AI providers (OpenAI, Claude, Gemini, Grok) through a unified HTTP interface. This is especially useful in environments where direct Python package installation is challenging, such as Replit.

## Base URL

When self-hosting the API, the base URL is:
```
http://localhost:5000/api
```

For the public demo instance (if available):
```
https://gptoggle-api.onalius.repl.co/api
```

## API Endpoints

### 1. List Available Providers

**Endpoint:** `GET /providers`

**Description:** Returns a list of all available AI providers based on configured API keys.

**Example Request:**
```bash
curl https://gptoggle-api.onalius.repl.co/api/providers
```

**Example Response:**
```json
{
  "providers": ["openai", "claude", "gemini", "grok"]
}
```

### 2. List Models for a Provider

**Endpoint:** `GET /models`

**Parameters:**
- `provider` (query string): The provider name (e.g., "openai", "claude")

**Description:** Returns a list of available models for the specified provider.

**Example Request:**
```bash
curl https://gptoggle-api.onalius.repl.co/api/models?provider=openai
```

**Example Response:**
```json
{
  "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
}
```

### 3. Get Recommended Model

**Endpoint:** `POST /recommend`

**Request Body:**
```json
{
  "prompt": "Your prompt text here"
}
```

**Description:** Analyzes the prompt and recommends the most appropriate provider and model.

**Example Request:**
```bash
curl -X POST https://gptoggle-api.onalius.repl.co/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'
```

**Example Response:**
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "reason": "Advanced educational topic requiring detailed explanation"
}
```

### 4. Generate Response

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
  "prompt": "Your prompt text here",
  "provider": "openai",  // Optional, auto-selected if not provided
  "model": "gpt-4o",     // Optional, auto-selected if not provided
  "temperature": 0.7,    // Optional, defaults to 0.7
  "max_tokens": 1000     // Optional, defaults to 1000
}
```

**Description:** Generates a response from the specified (or auto-selected) model.

**Example Request:**
```bash
curl -X POST https://gptoggle-api.onalius.repl.co/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the meaning of life?",
    "provider": "claude",
    "model": "claude-3-opus-20240229"
  }'
```

**Example Response:**
```json
{
  "response": "The meaning of life is a profound philosophical question...",
  "provider": "claude",
  "model": "claude-3-opus-20240229"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Request was successful
- `400 Bad Request`: Invalid parameters or request body
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a descriptive message:

```json
{
  "error": "Invalid provider specified"
}
```

## Authentication

The REST API requires API keys for the underlying AI providers to be set as environment variables:

- `OPENAI_API_KEY`: For OpenAI models
- `ANTHROPIC_API_KEY`: For Claude models
- `GOOGLE_API_KEY`: For Gemini models
- `XAI_API_KEY`: For Grok models

These should be set on the server running the REST API, not in the client applications.

## Rate Limiting

The REST API implements basic rate limiting to prevent abuse:

- 60 requests per minute for the `/generate` endpoint
- 120 requests per minute for all other endpoints

## Client Libraries

We provide client libraries to simplify using the API:

- [Python Client](examples/client_library.py)
- [JavaScript/Node.js Client](examples/client_library.js)

## Node.js Usage Example

Here's an example of using the GPToggle API from a Node.js application:

```javascript
const axios = require('axios');

// Base URL of the GPToggle API
const API_URL = 'https://gptoggle-api.onalius.repl.co/api';

// Generate a response using the API
async function generateResponse(prompt, provider = null, model = null) {
  try {
    const response = await axios.post(`${API_URL}/generate`, {
      prompt,
      provider,
      model
    });
    
    return response.data.response;
  } catch (error) {
    console.error('Error generating response:', error.response?.data || error.message);
    throw error;
  }
}

// Example usage
async function main() {
  try {
    // Get a response with auto-selected model
    const response1 = await generateResponse('What is quantum computing?');
    console.log('Auto-selected model response:', response1);
    
    // Get a response with specific provider and model
    const response2 = await generateResponse(
      'Write a poem about AI',
      'openai',
      'gpt-4o'
    );
    console.log('Specific model response:', response2);
  } catch (error) {
    console.error('Failed to generate responses');
  }
}

main();
```

## Self-Hosting

To self-host the API:

1. Clone the GPToggle repository:
   ```bash
   git clone https://github.com/onalius/gptoggle-core.git
   cd gptoggle-core
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables for your API keys:
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export GOOGLE_API_KEY="your-google-key"
   export XAI_API_KEY="your-xai-key"
   ```

4. Start the API server:
   ```bash
   python examples/rest_api.py
   ```

The API will be available at `http://localhost:5000/api`.

## Security Considerations

When using the REST API:

1. **API Key Security**: Keep your AI provider API keys secure
2. **HTTPS**: Always use HTTPS in production environments
3. **CORS**: The API enables CORS for all origins by default
4. **Validation**: All inputs are validated before processing