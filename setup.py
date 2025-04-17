from setuptools import setup, find_packages
import os
import re
import sys

# Determine if we're in a Replit environment
IN_REPLIT = 'REPL_ID' in os.environ or 'REPLIT_DEPLOYMENT' in os.environ

# Read version from __init__.py to ensure single source of truth
try:
    with open('gptoggle/__init__.py', 'r') as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            version = version_match.group(1)
        else:
            raise RuntimeError("Unable to find version string in gptoggle/__init__.py")
except FileNotFoundError:
    version = "0.0.0"  # Fallback version if file not found

# Determine which requirements approach to use based on environment
# In Replit, we'll make Flask, rich, and other UI dependencies optional
install_requires = [
    "openai>=1.0.0",  # For OpenAI and Grok providers
    "anthropic>=0.5.0",  # For Claude provider
    "google-generativeai>=0.3.0",  # For Gemini provider
]

if not IN_REPLIT:
    # These are needed for the full experience but can cause issues in Replit
    install_requires.extend([
        "rich>=10.0.0",  # For terminal formatting
        "flask>=2.0.0",  # For web interface
    ])

# Optional dependencies for different use cases
extras_require = {
    "dev": [
        "pytest>=7.0.0",
        "black>=22.0.0",
        "isort>=5.0.0",
        "flake8>=4.0.0",
    ],
    "web": [
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
    ],
    "ui": [
        "rich>=10.0.0",
    ],
    "all": [
        "rich>=10.0.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "pytest>=7.0.0",
    ]
}

# Get long description from README.md if available
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "GPToggle: A multi-provider wrapper for AI model APIs"

# Package naming to avoid conflicts with Replit environment
# Use a very distinctive name that won't conflict with any Replit project name
package_name = "gptoggle" if not IN_REPLIT else "gptoggle-ai-wrapper-library-pkg"

setup(
    name=package_name,
    version=version,
    author="GPToggle Team",
    author_email="lano@docdel.io",
    description="A multi-provider wrapper for AI model APIs with auto-model selection and comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onalius/gptoggle-core",
    project_urls={
        "Bug Tracker": "https://github.com/onalius/gptoggle-core/issues",
        "Documentation": "https://github.com/onalius/gptoggle-core/blob/main/README.md",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "gptoggle=gptoggle.chat:main",
        ],
    },
    # Make sure package data is included
    include_package_data=True,
    # Include templates, static files, etc.
    package_data={
        "gptoggle": ["templates/*", "static/**/*"],
    },
)