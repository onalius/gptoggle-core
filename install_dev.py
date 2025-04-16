#!/usr/bin/env python3
"""
Helper script to install the gptoggle package in development mode.
"""
import os
import sys
import subprocess

def main():
    """Install the package in development mode."""
    print("Installing gptoggle package in development mode...")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.join(script_dir, "gptoggle-core")
    
    if not os.path.exists(package_dir):
        print(f"Error: Package directory not found: {package_dir}")
        return 1
    
    # Change to the package directory
    os.chdir(package_dir)
    
    # Run pip install -e .
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("\nInstallation successful!")
        print("\nYou can now import the gptoggle package or use the CLI:")
        print("  python -c 'from gptoggle import choose_model; print(choose_model(\"Hello\"))'")
        print("  python -m gptoggle.chat \"What is the capital of France?\"")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: Installation failed with code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())