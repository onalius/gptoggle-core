# Installing GPToggle in Replit

This guide provides special instructions for installing and using the GPToggle package specifically in Replit environments.

## Important: Installation Challenges in Replit

Replit environments have unique characteristics that can cause conflicts with Python package installation. The most common issue is **self-dependency errors**, which occur when Replit's project name conflicts with the package name.

To address this, we use a very distinctive package name (`gptoggle-ai-wrapper-library-pkg`) that's unlikely to conflict with any Replit project name.

## Option 1: Using the Installation Helper Script

The simplest approach is to use our installation helper script:

```bash
# Clone the repository
git clone https://github.com/yourusername/gptoggle.git
cd gptoggle

# Run the installation helper
python install.py
```

This script automatically detects the Replit environment and handles all the necessary adjustments.

## Option 2: Direct Installation (Core Functionality Only)

For basic usage in Replit, install the core package:

```bash
# Install with minimal dependencies to avoid conflicts
pip install gptoggle-ai-wrapper-library-pkg --no-deps
pip install openai anthropic google-generativeai
```

This installs only the essential AI provider libraries. You won't have the CLI formatting or web interface, but the core API functionality will work.

## Option 2: Installation with Specific Features

You can install specific optional components:

```bash
# Install with web interface support
pip install gptoggle-ai-wrapper-library-pkg[web] --no-deps
pip install openai anthropic google-generativeai flask flask-cors

# Install with terminal UI support
pip install gptoggle-ai-wrapper-library-pkg[ui] --no-deps
pip install openai anthropic google-generativeai rich
```

## Option 3: Using the Standalone File

If you're having trouble with package installation, use the standalone Python file:

```bash
# Download the standalone file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle_minimal.py -o gptoggle_minimal.py

# Use directly in your code
python -c "from gptoggle_minimal import get_response; print(get_response('Hello, world!'))"
```

The standalone file includes the core functionality of GPToggle without requiring installation.

## Option 4: Using the JavaScript Implementation

For web projects or if you prefer JavaScript, use our JavaScript implementation:

```bash
# Download the JavaScript file
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

In Node.js:
```javascript
const GPToggle = require('./gptoggle');
const gptoggle = new GPToggle({}, {
  openai: process.env.OPENAI_API_KEY,
  claude: process.env.ANTHROPIC_API_KEY
});

async function example() {
  const response = await gptoggle.getResponse('What is quantum computing?');
  console.log(response);
}

example().catch(console.error);
```

In a browser:
```html
<script src="gptoggle.js"></script>
<script>
  const gptoggle = new GPToggle({}, {
    openai: 'your-openai-key', // Be careful with API keys in frontend code!
    claude: 'your-claude-key'
  });
  
  async function askAI() {
    const response = await gptoggle.getResponse(
      document.getElementById('prompt').value
    );
    document.getElementById('response').textContent = response;
  }
</script>
```

## Option 5: Using GPToggle as a REST API Service

If you continue having issues with direct installation, you can use the REST API approach:

1. Clone and run the GPToggle REST API in one Repl:
   ```bash
   git clone https://github.com/onalius/gptoggle-core.git
   cd gptoggle-core
   python examples/rest_api.py
   ```

2. In your client Repl, use one of these client libraries:
   - For Python: [examples/client_library.py](examples/client_library.py)
   - For Node.js: [examples/client_library.js](examples/client_library.js)

3. Connect to the API using the Replit domain:
   ```python
   # Python example
   from client_library import GPToggleClient
   
   # Get the URL of the Repl running the GPToggle REST API
   client = GPToggleClient("https://gptoggle.yourusername.repl.co")
   
   # Use the client
   response = client.generate_response("What is the meaning of life?")
   print(response)
   ```

## Troubleshooting Replit-Specific Issues

### Self-Dependency Errors

If you see errors about self-dependencies:

```
error: Requirement name matches project name, but self-dependencies are not permitted without the `--dev` or `--optional` flags.
```

Try one of these approaches:

1. Install with the `--no-deps` flag as shown above

2. Use a different package name:
   ```bash
   pip install git+https://github.com/onalius/gptoggle-core.git@main#egg=gptoggle-ai-wrapper-library-pkg --no-deps
   ```

3. Clone the repository and use it without installation:
   ```bash
   git clone https://github.com/onalius/gptoggle-core.git
   cd gptoggle-core
   # Then import from this local directory
   ```

### Import Errors After Installation

If you installed successfully but see import errors:

1. Check that you installed all required dependencies:
   ```bash
   pip install openai anthropic google-generativeai
   ```

2. Verify the package is installed:
   ```bash
   pip list | grep gptoggle
   ```

3. Try importing specific modules instead of the whole package:
   ```python
   # Instead of 
   import gptoggle
   
   # Try
   from gptoggle import get_response, recommend_model
   ```

## Getting API Keys

Remember, you'll need API keys for whichever AI providers you want to use:

- OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
- Google API key from [makersuite.google.com](https://makersuite.google.com/)
- xAI API key (contact xAI directly)