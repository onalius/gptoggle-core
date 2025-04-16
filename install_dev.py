#!/usr/bin/env python3
"""
Helper script to install the gptoggle package in development mode.
"""

import os
import subprocess
import sys


def main():
    """Install the package in development mode."""
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Install the package in development mode
    print("Installing GPToggle package in development mode...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=script_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    
    if result.returncode == 0:
        print("Installation successful!")
        print("You can now import gptoggle in your Python scripts or run 'gptoggle' from the command line.")
    else:
        print("Installation failed!")
        print(f"Error: {result.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    main()