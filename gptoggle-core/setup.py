from setuptools import setup, find_packages

setup(
    name="gptoggle",
    version="0.1.0",
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
    ],
    entry_points={
        "console_scripts": [
            "gptoggle=gptoggle.chat:main",
        ],
    },
)