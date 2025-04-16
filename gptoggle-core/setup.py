#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gptoggle",
    version="0.1.0",
    author="GPToggle",
    author_email="lano@docdel.io",
    description="A Python wrapper for the OpenAI API with auto-model selection and comparison capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gptoggle/gptoggle-core",
    project_urls={
        "Bug Tracker": "https://github.com/gptoggle/gptoggle-core/issues",
        "Documentation": "https://github.com/gptoggle/gptoggle-core",
        "Source Code": "https://github.com/gptoggle/gptoggle-core",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gptoggle=gptoggle.chat:main",
        ],
    },
)