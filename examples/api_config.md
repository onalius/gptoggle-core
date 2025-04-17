# GPToggle API Configuration

## Using GPToggle as a Library

When using GPToggle as a Python library directly in your application, you need API keys for the AI providers you want to use:

```python
import os
import gptoggle

# Set API keys for the providers you want to use
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"  # Optional
os.environ["GOOGLE_API_KEY"] = "your-google-key"        # Optional
os.environ["XAI_API_KEY"] = "your-xai-key"              # Optional

# Now you can use the library
response = gptoggle.get_response("Hello, world!")
```

## Using GPToggle as a Service

If you're using GPToggle as a service via its REST API:

1. Set the `GPTOGGLE_API_URL` environment variable in your application to point to the running GPToggle API server:

```javascript
// Node.js example
process.env.GPTOGGLE_API_URL = "https://your-gptoggle-api.domain.com/api";
```

```python
# Python example
import os
os.environ["GPTOGGLE_API_URL"] = "https://your-gptoggle-api.domain.com/api"
```

2. Make HTTP requests to the API endpoints:

```javascript
// Node.js fetch example
async function getResponse(prompt) {
  const response = await fetch(`${process.env.GPTOGGLE_API_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt
    }),
  });
  const data = await response.json();
  return data.response;
}
```

## API Endpoints

The GPToggle REST API provides the following endpoints:

- `GET /api/providers` - List all available providers
- `GET /api/models?provider=openai` - List all available models for a provider
- `POST /api/recommend` - Get a recommended model for a prompt
- `POST /api/generate` - Generate a response for a prompt

## API URL for the Replit Environment

If you're running GPToggle in a Replit environment, use the Replit domain as the API URL. For example:

```
GPTOGGLE_API_URL=https://gptoggle.yourusername.repl.co/api
```

You can get your Replit domain by looking at the URL in the browser when viewing your Repl, or by checking environment variables:

```python
import os
replit_domain = os.environ.get("REPLIT_DOMAIN")
api_url = f"https://{replit_domain}/api"
```