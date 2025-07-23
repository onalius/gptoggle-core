#!/bin/bash
# GPToggle Replit Installation Script
# This script installs GPToggle in Replit environments with proper handling
# of self-dependency issues.

echo "GPToggle Replit Installation Script"
echo "===================================="

# Check if running in Replit
if [ -n "$REPL_ID" ]; then
    echo "Detected Replit environment!"
else
    echo "Warning: Not running in a Replit environment."
    echo "This script is optimized for Replit. It may work in other environments, but is not tested."
fi

# Install the package from the current directory
echo "Installing GPToggle..."
python -m pip install --upgrade .

# Verify installation
echo "Verifying installation..."
if python -c "import gptoggle_enhanced" 2>/dev/null; then
    echo "✓ GPToggle successfully installed!"
else
    echo "× Installation verification failed. Please check for errors above."
    exit 1
fi

# Prompt for provider selection
echo ""
echo "Do you want to install dependencies for specific providers?"
echo "1. OpenAI (for GPT models)"
echo "2. Claude (for Anthropic models)"
echo "3. Gemini (for Google models)"
echo "4. All providers"
echo "5. Skip (don't install any provider dependencies)"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Installing OpenAI dependencies..."
        python -m pip install openai>=1.0.0
        ;;
    2)
        echo "Installing Claude dependencies..."
        python -m pip install anthropic>=0.5.0
        ;;
    3)
        echo "Installing Gemini dependencies..."
        python -m pip install google-generativeai>=0.3.0
        ;;
    4)
        echo "Installing all provider dependencies..."
        python -m pip install openai>=1.0.0 anthropic>=0.5.0 google-generativeai>=0.3.0
        ;;
    5)
        echo "Skipping provider dependencies."
        ;;
    *)
        echo "Invalid choice. Skipping provider dependencies."
        ;;
esac

echo ""
echo "GPToggle installation completed!"
echo ""
echo "Usage example:"
echo "```python"
echo "from gptoggle_enhanced import get_response"
echo ""
echo "response = get_response(\"What is quantum computing?\")"
echo "print(response)"
echo "```"
echo ""
echo "Make sure to set your API keys as environment variables:"
echo "- OPENAI_API_KEY for OpenAI"
echo "- ANTHROPIC_API_KEY for Claude"
echo "- GOOGLE_API_KEY for Gemini"
echo "- XAI_API_KEY for Grok"
echo ""
echo "You can set these in the Replit Secrets tab in the Tools panel."