#!/usr/bin/env python3
"""
Setup script for GPToggle package.
"""

import os
import sys
from setuptools import setup, find_packages

# Check if running in Replit environment
IN_REPLIT = os.environ.get("REPL_ID") is not None
PACKAGE_NAME = "gptoggle-ai-wrapper-library-pkg" if IN_REPLIT else "gptoggle-core"

if IN_REPLIT:
    print("Detected Replit environment. Using alternative package name to avoid self-dependency issues.")

# Read the content of README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Check if standalone files exist - otherwise copy them from examples
standalone_files = ["gptoggle_minimal.py", "gptoggle_enhanced.py", "gptoggle.js", "gptoggle_enhanced.js"]
for file in standalone_files:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), file)):
        print(f"Warning: {file} not found in package root. Package may be incomplete.")

# Get all example files
example_files = []
examples_dir = os.path.join(os.path.dirname(__file__), "examples")
if os.path.isdir(examples_dir):
    for root, dirs, files in os.walk(examples_dir):
        for file in files:
            if file.endswith(".py") or file.endswith(".js"):
                example_files.append(os.path.join(root, file).replace(os.path.dirname(__file__) + os.sep, ""))

# Get all documentation files
docs_files = []
docs_dir = os.path.join(os.path.dirname(__file__), "docs")
if os.path.isdir(docs_dir):
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                docs_files.append(os.path.join(root, file).replace(os.path.dirname(__file__) + os.sep, ""))

setup(
    name=PACKAGE_NAME,
    version="1.0.3",
    description="Multi-provider AI model wrapper with intelligent model selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GPToggle Team",
    author_email="lano@docdel.io",
    url="https://github.com/onalius/gptoggle-core",
    py_modules=["gptoggle_minimal", "gptoggle_enhanced"],
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ("gptoggle/javascript", ["gptoggle.js", "gptoggle_enhanced.js"]),
        ("gptoggle/docs", docs_files),
        ("gptoggle/examples", example_files),
    ],
    scripts=["install.py", "release.py", "replit_install.sh"],
    install_requires=[
        # Core dependencies - minimal requirements
        "requests>=2.25.0",
    ],
    extras_require={
        # Optional dependencies for specific providers
        "openai": ["openai>=1.0.0"],
        "claude": ["anthropic>=0.5.0"],
        "gemini": ["google-generativeai>=0.3.0"],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "google-generativeai>=0.3.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords="ai, openai, claude, gemini, grok, gpt, chatgpt, api, wrapper, llm, multi-provider, gptoggle",
)