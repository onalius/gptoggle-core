# GPToggle Web Interface Guide

GPToggle includes a web interface that provides an easy-to-use GUI for interacting with multiple AI providers.

## Setting Up the Web Interface

### Option 1: Using Flask (Python)

1. Install the required packages:

```bash
pip install flask gptoggle-core
```

2. Create a file named `app.py` with the following content:

```python
import os
from flask import Flask, render_template, request, jsonify
from gptoggle import get_response, recommend_model, get_available_providers

app = Flask(__name__)

@app.route('/')
def index():
    providers = get_available_providers()
    return render_template('index.html', providers=providers)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    provider = data.get('provider') if data.get('provider') != 'auto' else None
    model = data.get('model') if data.get('model') != 'auto' else None
    
    try:
        response = get_response(prompt, provider, model)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    prompt = data.get('prompt')
    
    try:
        provider, model = recommend_model(prompt)
        return jsonify({'provider': provider, 'model': model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

3. Create a `templates` directory and add an `index.html` file:

```bash
mkdir templates
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/templates/index.html -o templates/index.html
```

4. Run the application:

```bash
python app.py
```

### Option 2: Pure HTML/JavaScript (No Server Required)

1. Download the standalone HTML file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle-web-example.html -o gptoggle-web-example.html
```

2. Download the GPToggle JavaScript file:

```bash
curl -sSL https://raw.githubusercontent.com/onalius/gptoggle-core/main/gptoggle.js -o gptoggle.js
```

3. Open the HTML file in your browser:

```bash
# If you have Python installed
python -m http.server 8000

# Then open http://localhost:8000/gptoggle-web-example.html in your browser
```

## Using the Web Interface

1. **Enter API Keys**: Input your API keys for the providers you want to use
2. **Enter Prompt**: Type your prompt in the text area
3. **Choose Provider**: Select a specific provider or use "Auto-select"
4. **Choose Model**: Select a specific model or use "Auto-select"
5. **Get Response**: Click "Get Response" to generate a response
6. **Recommend Model**: Alternatively, click "Recommend Model" to see which model is best for your prompt

## Customizing the Web Interface

You can customize the web interface by editing the HTML and CSS. The interface uses Bootstrap for styling and is designed to be responsive.

### Changing the Theme

The default theme is dark mode. To switch to light mode, change:

```html
<body data-bs-theme="dark">
```

to:

```html
<body data-bs-theme="light">
```

### Adding More Models

To add more models to the dropdown, edit the `<select id="model">` element:

```html
<select class="form-select" id="model">
  <option value="auto">Auto-select</option>
  <option value="openai:gpt-3.5-turbo">OpenAI: GPT-3.5 Turbo</option>
  <option value="openai:gpt-4o">OpenAI: GPT-4o</option>
  <!-- Add more models here -->
</select>
```

## Deploying the Web Interface

### On Replit

1. Create a new Repl with Flask
2. Upload the files or create them as described above
3. Replit will automatically detect the Flask app and run it

### On Vercel, Netlify, or GitHub Pages

For the pure HTML/JavaScript version:

1. Create a GitHub repository with the HTML and JS files
2. Deploy to your preferred platform

### With Docker

```bash
# Create a Dockerfile
echo 'FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install flask gptoggle-core
EXPOSE 5000
CMD ["python", "app.py"]' > Dockerfile

# Build and run the Docker container
docker build -t gptoggle-web .
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key-here gptoggle-web
```

## Security Considerations

- The pure HTML/JavaScript version stores API keys in the browser's localStorage
- For production use, consider implementing proper authentication and secure API key storage
- Never expose your API keys in client-side code in production environments