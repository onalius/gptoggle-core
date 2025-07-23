#!/usr/bin/env python3
"""
GPToggle Release Script

This script helps package GPToggle for distribution:
1. Cleans up build artifacts
2. Builds the Python package
3. Creates distribution archives

Usage:
    python release.py
"""

import os
import sys
import shutil
import subprocess

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    
    return True

def clean_build_artifacts():
    """Clean up build artifacts."""
    print("Cleaning up build artifacts...")
    
    # Directories to remove
    dirs_to_remove = [
        "build",
        "dist",
        "*.egg-info",
        "__pycache__",
        "**/__pycache__"
    ]
    
    for pattern in dirs_to_remove:
        command = f"find . -type d -name '{pattern}' -exec rm -rf {{}} + 2>/dev/null || true"
        run_command(command)
    
    # Files to remove
    files_to_remove = [
        "*.pyc",
        "**/*.pyc",
        "*.pyo",
        "**/*.pyo",
        "*.pyd",
        "**/*.pyd"
    ]
    
    for pattern in files_to_remove:
        command = f"find . -type f -name '{pattern}' -delete 2>/dev/null || true"
        run_command(command)
    
    print("Cleanup completed.")

def build_package():
    """Build the Python package."""
    print("\nBuilding Python package...")
    
    commands = [
        f"{sys.executable} -m pip install --upgrade pip setuptools wheel build",
        f"{sys.executable} -m build ."
    ]
    
    for command in commands:
        if not run_command(command):
            print("Building package failed.")
            return False
    
    print("Package built successfully.")
    return True

def main():
    """Main release function."""
    print("GPToggle Release Script")
    print("======================")
    
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Clean up build artifacts
    clean_build_artifacts()
    
    # Build the package
    if not build_package():
        return
    
    # Show output files
    print("\nCreated distribution files:")
    run_command("ls -l dist/")
    
    print("\nRelease process completed successfully!")
    print("\nTo upload to PyPI:")
    print("  python -m pip install --upgrade twine")
    print("  python -m twine upload dist/*")

if __name__ == "__main__":
    main()