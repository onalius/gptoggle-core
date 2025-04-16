# OpenAI CLI Wrapper

A Python-based command-line interface for interacting with OpenAI's models, featuring auto-model selection and comparison capabilities.

## Features

- **Model Discovery**: Automatically discovers and exposes available OpenAI models
- **Auto-Triage**: Intelligently selects the best model based on your prompt's characteristics
- **Comparison Mode**: Compare responses from different models side-by-side and save ratings
- **Simple CLI**: Easy-to-use command-line interface

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd openai-cli-wrapper
   ```

2. Install the required dependencies:
   ```bash
   pip install openai
   ```

3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

## Usage

### Basic Usage

Ask a question and let the tool automatically select the best model:

```bash
python chat.py "What is the capital of France?"
