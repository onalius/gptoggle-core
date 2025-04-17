#!/bin/bash
# GPToggle Replit Installation Script
# This script handles the installation of GPToggle in Replit environments

echo "==== GPToggle Replit Installation ===="
echo "Installing GPToggle with Replit-specific adjustments..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed. Please install pip first."
    exit 1
fi

# Install with --no-deps to avoid self-dependency issues
echo "📦 Installing package with --no-deps flag to avoid self-dependency conflicts..."
pip install git+https://github.com/onalius/gptoggle-core.git@main#egg=gptoggle-ai-wrapper-library-pkg --no-deps

# Install required core dependencies separately
echo "📦 Installing core dependencies..."
pip install openai>=1.0.0 anthropic>=0.5.0 google-generativeai>=0.3.0

# Optional: Install UI dependencies
if [[ "$*" == *"--ui"* ]]; then
    echo "📦 Installing UI dependencies..."
    pip install rich>=10.0.0
fi

# Optional: Install web dependencies
if [[ "$*" == *"--web"* ]] || [[ "$*" == *"--all"* ]]; then
    echo "📦 Installing web interface dependencies..."
    pip install flask>=2.0.0 flask-cors>=3.0.0
fi

# Verify installation
echo "🔍 Verifying installation..."
if python -c "import gptoggle; print(f'✅ GPToggle version {gptoggle.__version__} installed successfully')" 2>/dev/null; then
    echo "✨ Installation complete!"
else
    echo "⚠️ Installation may have partially succeeded, but importing failed."
    echo "📝 Try one of these alternative approaches:"
    echo "1. Use the REST API approach (see https://github.com/onalius/gptoggle-core#rest-api)"
    echo "2. Download the standalone Python file: gptoggle_minimal.py"
fi

echo "For more information, visit: https://github.com/onalius/gptoggle-core"