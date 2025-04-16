# GPToggle Core

GPToggle is a Python wrapper for the OpenAI API that provides automatic model selection and comparison capabilities.

## Features

- **Auto-triage Model Selection**: Automatically selects the most appropriate OpenAI model based on your prompt's characteristics
- **Model Comparison**: Compare responses from different models for the same prompt
- **Command Line Interface**: Use GPToggle directly from the command line
- **API Integration**: Import GPToggle into your Python projects

## Installation

### From PyPI (Coming Soon)

```bash
pip install gptoggle
```

### From GitHub

```bash
pip install git+https://github.com/gptoggle/gptoggle-core.git
```

### Development Installation

```bash
git clone https://github.com/gptoggle/gptoggle-core.git
cd gptoggle-core
pip install -e .
```

## Usage

### CLI Usage

#### Auto-select the best model for your prompt:

```bash
export OPENAI_API_KEY='your-api-key'
gptoggle "Write a short story about a robot learning to paint"
```

#### Specify a model manually:

```bash
gptoggle "Explain quantum computing in simple terms" --model gpt-4o
```

#### Compare responses from different models:

```bash
gptoggle "Solve this coding challenge: implement a function to reverse a linked list" --compare gpt-4o,gpt-3.5-turbo
```

#### List available models:

```bash
gptoggle --list-models
```

### Python API Usage

```python
import os
from gptoggle import get_response, choose_model, compare_models

# Set your API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Auto-select the best model
model, reason = choose_model("Write code to implement a binary search tree in Python")
print(f"Selected model: {model}")
print(f"Reason: {reason}")

# Get a response
response = get_response("Explain the theory of relativity", model)
print(response)

# Compare models
compare_models("Design a database schema for an e-commerce application", ["gpt-4o", "gpt-3.5-turbo"])
```

## How Model Selection Works

GPToggle uses a sophisticated triage algorithm to determine the most appropriate model based on:

1. **Prompt Length**: For very long prompts, models with longer context windows are preferred
2. **Code Keywords**: If your prompt contains programming-related keywords, code-optimized models are selected
3. **Creative Content**: For creative tasks like storytelling or content generation, models with better creative capabilities are chosen
4. **General Knowledge**: For standard informational queries, a balanced model is selected

## License

MIT License

## For More Information

Visit [GPToggle.com](https://gptoggle.com) for more information, documentation, and to explore our premium features.