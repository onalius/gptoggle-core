#!/bin/bash
# GPToggle Quick Start Script
# This script helps users quickly test the GPToggle package

echo "GPToggle Quick Start Script"
echo "=========================="
echo ""
echo "This script will guide you through testing GPToggle with your API keys."
echo ""

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 not found. Please install Python 3 to use GPToggle."
    exit 1
fi

# Prompt for API keys
read -p "Enter OpenAI API Key (leave blank to skip): " OPENAI_API_KEY
read -p "Enter Anthropic API Key (leave blank to skip): " ANTHROPIC_API_KEY
read -p "Enter Google API Key (leave blank to skip): " GOOGLE_API_KEY
read -p "Enter xAI API Key (leave blank to skip): " XAI_API_KEY

# Temporarily set environment variables
export OPENAI_API_KEY=$OPENAI_API_KEY
export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
export GOOGLE_API_KEY=$GOOGLE_API_KEY
export XAI_API_KEY=$XAI_API_KEY

# Prompt for testing mode
echo ""
echo "Select a testing mode:"
echo "1. Python Test"
echo "2. JavaScript Test (requires Node.js)"
echo "3. Run examples"
echo "4. Skip testing"
read -p "Enter your choice (1-4): " CHOICE

case $CHOICE in
    1)
        # Python Test
        echo "Running Python test..."
        python3 examples/test_installation.py
        ;;
    2)
        # JavaScript Test
        if ! command -v node &>/dev/null; then
            echo "Node.js not found. Please install Node.js to run JavaScript tests."
            exit 1
        fi
        
        echo "Running JavaScript test..."
        node -e "
        const { GPToggle } = require('./gptoggle_enhanced');
        
        // Setup API keys
        const apiKeys = {
            openai: process.env.OPENAI_API_KEY,
            claude: process.env.ANTHROPIC_API_KEY,
            gemini: process.env.GOOGLE_API_KEY,
            grok: process.env.XAI_API_KEY
        };
        
        // Create a GPToggle instance
        const gptoggle = new GPToggle({}, apiKeys);
        
        // Check available providers
        const providers = gptoggle.getAvailableProviders();
        console.log('Available providers:', providers);
        
        if (providers.length > 0) {
            // Test model recommendation
            const testPrompt = 'What is quantum computing?';
            const recommendation = gptoggle.recommendModel(testPrompt);
            console.log('Recommended model for:', testPrompt);
            console.log('Provider:', recommendation.provider);
            console.log('Model:', recommendation.model);
            console.log('Reason:', recommendation.reason);
        } else {
            console.log('No API keys found. Please set at least one of the API key environment variables.');
        }
        "
        ;;
    3)
        # Run examples
        echo "Available examples:"
        echo "1. Python - GPToggle Follow-up Example"
        echo "2. JavaScript - GPToggle Follow-up Example (requires Node.js)"
        echo "3. JavaScript - Browser Example (opens in browser)"
        read -p "Enter your choice (1-3): " EXAMPLE_CHOICE
        
        case $EXAMPLE_CHOICE in
            1)
                echo "Running Python Follow-up Example..."
                python3 examples/python/gptoggle_followup_example.py
                ;;
            2)
                if ! command -v node &>/dev/null; then
                    echo "Node.js not found. Please install Node.js to run JavaScript examples."
                    exit 1
                fi
                
                echo "Running JavaScript Follow-up Example..."
                node examples/javascript/gptoggle-followup-example.js
                ;;
            3)
                echo "Opening Browser Example..."
                # Try different commands to open a browser
                if command -v xdg-open &>/dev/null; then
                    xdg-open examples/javascript/browser-example.html
                elif command -v open &>/dev/null; then
                    open examples/javascript/browser-example.html
                elif command -v start &>/dev/null; then
                    start examples/javascript/browser-example.html
                else
                    echo "Could not open browser automatically. Please open this file manually:"
                    echo "$(pwd)/examples/javascript/browser-example.html"
                fi
                ;;
            *)
                echo "Invalid choice."
                ;;
        esac
        ;;
    4)
        # Skip testing
        echo "Skipping tests."
        ;;
    *)
        echo "Invalid choice."
        ;;
esac

echo ""
echo "Quick Start Completed!"
echo ""
echo "For more examples and documentation, see:"
echo "- examples/python/ - Python examples"
echo "- examples/javascript/ - JavaScript examples"
echo "- docs/ - Documentation files"
echo ""
echo "Thank you for using GPToggle!"