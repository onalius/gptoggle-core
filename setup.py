from setuptools import setup, find_packages
import re

# Read version from __init__.py to ensure single source of truth
with open('gptoggle/__init__.py', 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in gptoggle/__init__.py")

setup(
    name="gptoggle-package",  # Changed package name to avoid self-dependency issues
    version=version,
    author="GPToggle Team",
    author_email="lano@docdel.io",
    description="A multi-provider wrapper for AI model APIs with auto-model selection and comparison",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gptoggle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",  # For OpenAI and Grok providers
        "anthropic>=0.5.0",  # For Claude provider
        "google-generativeai>=0.3.0",  # For Gemini provider
        "rich>=10.0.0",  # For terminal formatting
        "flask>=2.0.0",  # For web interface
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ],
    },
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