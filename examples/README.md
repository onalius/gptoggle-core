# GPToggle Examples

This directory contains examples of how to use GPToggle in different ways.

## REST API Example

`rest_api.py` - A Flask-based REST API that exposes GPToggle functionality via HTTP endpoints.

### Running the REST API

```bash
python examples/rest_api.py
```

This will start a web server on port 5000 with the following endpoints:

- `GET /api/providers` - List all available providers
- `GET /api/models?provider=openai` - List all available models for a provider
- `POST /api/recommend` - Get a recommended model for a prompt
- `POST /api/generate` - Generate a response for a prompt

### Example API Calls

```bash
# Get available providers
curl http://localhost:5000/api/providers

# Get models for a specific provider
curl http://localhost:5000/api/models?provider=openai

# Get a recommended model for a prompt
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'

# Generate a response
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the meaning of life?", "provider": "openai", "model": "gpt-4o"}'
```

## Client Libraries

We provide client libraries to simplify connecting to the GPToggle REST API:

### Python Client

`client_library.py` - A Python client for the GPToggle REST API.

```python
from examples.client_library import GPToggleClient

# Create a client
client = GPToggleClient('http://localhost:5000')

# Get a response
response = client.generate_response('What is the meaning of life?')
print(response)
```

### Node.js Client

`client_library.js` - A Node.js client for the GPToggle REST API.

```javascript
const GPToggleClient = require('./examples/client_library');

// Create a client
const client = new GPToggleClient('http://localhost:5000');

// Use the client
async function example() {
  const response = await client.generateResponse({
    prompt: 'What is the meaning of life?'
  });
  console.log(response);
}

example().catch(console.error);
```

## Using in Different Environments

### Using in a Production Environment

When deploying to production, consider:

1. Setting up proper authentication for the API
2. Using environment variables for API keys
3. Implementing rate limiting
4. Setting up HTTPS

### Using in Replit

For Replit-specific setup, see [REPLIT_INSTALLATION.md](../REPLIT_INSTALLATION.md).