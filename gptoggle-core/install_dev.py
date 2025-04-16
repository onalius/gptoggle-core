#!/usr/bin/env python3
"""
Helper script to install the gptoggle package in development mode.
"""

import os
import subprocess
import sys

def main():
    """Install the package in development mode."""
    print("Installing GPToggle in development mode...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pip install in development mode
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=current_dir)
        print("\nInstallation successful!")
        print("\nTo use GPToggle, you need to set API keys for at least one provider:")
        print("  - OpenAI: export OPENAI_API_KEY='your-api-key'")
        print("  - Claude: export ANTHROPIC_API_KEY='your-api-key'")
        print("  - Gemini: export GOOGLE_API_KEY='your-api-key'")
        print("  - Grok: export XAI_API_KEY='your-api-key'")
        print("\nTest the installation with: python example.py")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()