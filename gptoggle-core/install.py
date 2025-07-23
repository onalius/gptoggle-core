#!/usr/bin/env python3
"""
GPToggle Installation Helper

This script provides an easy installation experience for GPToggle
across different environments, including handling dependency issues
in Replit and other platforms.
"""

import os
import sys
import subprocess
import platform


def is_replit():
    """Check if running in a Replit environment."""
    return os.environ.get("REPL_ID") is not None


def install_package(package, upgrade=False):
    """Install a package using pip."""
    command = [sys.executable, "-m", "pip", "install"]
    if upgrade:
        command.append("--upgrade")
    command.append(package)
    
    print(f"Running: {' '.join(command)}")
    subprocess.check_call(command)


def main():
    """Main installation function."""
    print("GPToggle Installation Helper")
    print("===========================")
    
    # Detect environment
    if is_replit():
        print("Detected Replit environment!")
        # In Replit, we need to use a different package name to avoid self-dependency issues
        package_name = "gptoggle-ai-wrapper-library-pkg"
        # Install directly from the current directory
        install_package(".", upgrade=True)
    else:
        print(f"Detected regular environment: {platform.system()} {platform.release()}")
        package_name = "gptoggle-core"
        # Install from PyPI or current directory
        try:
            install_package(package_name, upgrade=True)
        except subprocess.CalledProcessError:
            print("Installing from current directory...")
            install_package(".", upgrade=True)
    
    # Check which provider libraries are already installed
    providers = {
        "openai": "OpenAI",
        "anthropic": "Anthropic Claude",
        "google-generativeai": "Google Gemini"
    }
    
    installed = []
    for pkg, name in providers.items():
        try:
            __import__(pkg.replace("-", "_") if "-" in pkg else pkg)
            installed.append(name)
        except ImportError:
            pass
    
    if installed:
        print(f"\nDetected libraries for: {', '.join(installed)}")
    
    # Ask if user wants to install optional provider libraries
    print("\nDo you want to install dependencies for specific providers?")
    print("1. OpenAI (for GPT models)")
    print("2. Claude (for Anthropic models)")
    print("3. Gemini (for Google models)")
    print("4. All providers")
    print("5. Skip (don't install any provider dependencies)")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    try:
        if choice == "1":
            install_package("openai>=1.0.0")
        elif choice == "2":
            install_package("anthropic>=0.5.0")
        elif choice == "3":
            install_package("google-generativeai>=0.3.0")
        elif choice == "4":
            install_package("openai>=1.0.0")
            install_package("anthropic>=0.5.0")
            install_package("google-generativeai>=0.3.0")
        elif choice == "5":
            print("Skipping provider dependencies.")
        else:
            print("Invalid choice. Skipping provider dependencies.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
    
    print("\nGPToggle installation completed!")
    print("\nUsage example:")
    print("```python")
    print("from gptoggle_enhanced import get_response")
    print("")
    print('response = get_response("What is quantum computing?")')
    print("print(response)")
    print("```")
    
    print("\nMake sure to set your API keys as environment variables:")
    print("- OPENAI_API_KEY for OpenAI")
    print("- ANTHROPIC_API_KEY for Claude")
    print("- GOOGLE_API_KEY for Gemini")
    print("- XAI_API_KEY for Grok")


if __name__ == "__main__":
    main()