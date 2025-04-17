#!/usr/bin/env python3
"""
GPToggle Installation Helper

This script helps install GPToggle in different environments, handling
environment-specific issues like Replit's self-dependency problems.

Usage:
    python install.py [options]

Options:
    --dev       Install in development mode
    --web       Install with web interface support
    --ui        Install with terminal UI support
    --all       Install all optional dependencies
    --no-deps   Install without dependencies
    --help      Show this help message
"""

import argparse
import os
import subprocess
import sys

# Determine if we're in a Replit environment
IN_REPLIT = 'REPL_ID' in os.environ or 'REPLIT_DEPLOYMENT' in os.environ

def run_command(cmd):
    """Run a command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def install_gptoggle(dev=False, web=False, ui=False, all_deps=False, no_deps=False):
    """Install GPToggle with the specified options."""
    
    # Base package name
    package_name = "gptoggle"
    extras = []
    
    # Add extras based on options
    if web:
        extras.append("web")
    if ui:
        extras.append("ui")
    if dev:
        extras.append("dev")
    if all_deps:
        extras = ["all"]
    
    # Build extras string
    extras_str = ""
    if extras:
        extras_str = f"[{','.join(extras)}]"
    
    # Special handling for Replit to avoid self-dependency issues
    if IN_REPLIT:
        package_name = "gptoggle-ai-wrapper-library-pkg"
        no_deps = True
        print("📝 Detected Replit environment, adjusting installation...")
        print("⚠️ Using distinctive package name to avoid self-dependency conflicts")
        print("⚠️ Using --no-deps flag to prevent dependency resolution issues")
    
    # Build installation command
    if dev:
        cmd = f"pip install -e .{extras_str}"
    else:
        # Assume package is installed from current directory
        cmd = f"pip install .{extras_str}"
    
    # Add --no-deps flag if specified
    if no_deps:
        cmd += " --no-deps"
    
    # Run the installation command
    print(f"Running: {cmd}")
    success, output = run_command(cmd)
    
    if success:
        print("✅ GPToggle package installed successfully")
    else:
        print(f"❌ Installation failed: {output}")
        return False
    
    # Install dependencies separately if --no-deps was used
    if no_deps:
        print("Installing core dependencies...")
        deps_cmd = "pip install openai>=1.0.0 anthropic>=0.5.0 google-generativeai>=0.3.0"
        success, output = run_command(deps_cmd)
        
        if success:
            print("✅ Core dependencies installed successfully")
        else:
            print(f"❌ Dependency installation failed: {output}")
            return False
        
        # Install additional dependencies based on extras
        if web or all_deps:
            print("Installing web dependencies...")
            web_cmd = "pip install flask>=2.0.0 flask-cors>=3.0.0"
            success, output = run_command(web_cmd)
            if not success:
                print(f"❌ Web dependency installation failed: {output}")
        
        if ui or all_deps:
            print("Installing UI dependencies...")
            ui_cmd = "pip install rich>=10.0.0"
            success, output = run_command(ui_cmd)
            if not success:
                print(f"❌ UI dependency installation failed: {output}")
        
        if dev:
            print("Installing development dependencies...")
            dev_cmd = "pip install pytest>=7.0.0 black>=22.0.0 isort>=5.0.0 flake8>=4.0.0"
            success, output = run_command(dev_cmd)
            if not success:
                print(f"❌ Development dependency installation failed: {output}")
    
    # Verify installation
    print("\nVerifying installation...")
    verify_cmd = "python -c \"import gptoggle; print(f'GPToggle version: {gptoggle.__version__}');\""
    success, output = run_command(verify_cmd)
    
    if success:
        print(output)
        print("✅ GPToggle imported successfully")
    else:
        print("❌ Failed to import GPToggle.")
        if IN_REPLIT:
            print("\n⚠️ Replit-Specific Troubleshooting:")
            print("1. Try using the REST API approach instead of direct import.")
            print("   See examples/rest_api.py for details")
            print("2. If you're developing a client application, use the client libraries:")
            print("   - examples/client_library.py (Python)")
            print("   - examples/client_library.js (JavaScript/Node.js)")
            print("3. If you still need direct import, try this manual installation:")
            print("   pip install -e . --no-deps")
            print("   pip install openai anthropic google-generativeai rich flask")
        else:
            print("This might be because of PATH issues.")
            print("Try starting a new terminal or Python session.")
        return False
    
    # Print environment info
    if IN_REPLIT:
        print("\n📝 Replit Environment Detected")
        print("For Replit-specific installation information, see REPLIT_INSTALLATION.md")
        print("⚠️ For optimal Replit compatibility:")
        print("1. Consider using the REST API example (examples/rest_api.py)")
        print("2. Or use the client libraries in examples/ directory")
        print("3. Avoid direct imports of the package in Replit environments")
    
    print("\n✨ Installation Complete!")
    print("To get started, run:")
    print("  python -c \"import gptoggle; print(gptoggle.get_response('Hello world'))\"")
    
    return True

def main():
    """Parse arguments and install GPToggle."""
    parser = argparse.ArgumentParser(description="Install GPToggle")
    parser.add_argument("--dev", action="store_true", help="Install in development mode")
    parser.add_argument("--web", action="store_true", help="Install with web interface support")
    parser.add_argument("--ui", action="store_true", help="Install with terminal UI support")
    parser.add_argument("--all", action="store_true", help="Install all optional dependencies")
    parser.add_argument("--no-deps", action="store_true", help="Install without dependencies")
    
    args = parser.parse_args()
    
    # Print information about the installation
    print("=" * 60)
    print("GPToggle Installation Helper")
    print("=" * 60)
    
    # Check if setup.py exists
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Please run this script from the root directory of the GPToggle package.")
        return False
    
    # Check for Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Error: GPToggle requires Python 3.8 or higher.")
        return False
    
    # Install GPToggle
    return install_gptoggle(
        dev=args.dev,
        web=args.web,
        ui=args.ui,
        all_deps=args.all,
        no_deps=args.no_deps
    )

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)