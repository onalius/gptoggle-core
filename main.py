"""
Flask web interface for the OpenAI CLI wrapper.
This provides a web UI for the same functionality available in the CLI.
"""
import os
from flask import Flask, render_template, request, jsonify
import config
import triage
import compare
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key")

@app.route('/')
def index():
    """Render the main page."""
    models = config.AVAILABLE_MODELS
    return render_template('index.html', models=models)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests from the web interface."""
    data = request.json
    prompt = data.get('prompt', '')
    selected_model = data.get('model', '')
    
    # Auto-select model if none provided
    if not selected_model:
        selected_model, reason = triage.choose_model(prompt)
    else:
        reason = "Manually selected by user"
    
    # Validate model
    if selected_model not in config.AVAILABLE_MODELS:
        return jsonify({'error': f'Invalid model: {selected_model}'}), 400
    
    # Get response from model
    try:
        client = OpenAI(api_key=config.openai_config.api_key)
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.openai_config.temperature,
            max_tokens=config.openai_config.max_tokens,
        )
        response_text = response.choices[0].message.content
        return jsonify({
            'response': response_text,
            'model': selected_model,
            'reason': reason
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_api():
    """Handle model comparison requests."""
    data = request.json
    prompt = data.get('prompt', '')
    models = data.get('models', [])
    
    # Validate models
    for model in models:
        if model not in config.AVAILABLE_MODELS:
            return jsonify({'error': f'Invalid model: {model}'}), 400
    
    # Ensure exactly two models
    if len(models) != 2:
        return jsonify({'error': 'Exactly two models must be selected for comparison'}), 400
    
    # Get responses
    try:
        responses = {}
        client = OpenAI(api_key=config.openai_config.api_key)
        
        for model in models:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.openai_config.temperature,
                max_tokens=config.openai_config.max_comparison_tokens,
            )
            responses[model] = response.choices[0].message.content
        
        return jsonify({
            'responses': responses,
            'models': models
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-rating', methods=['POST'])
def save_rating_api():
    """Save user rating from comparison."""
    data = request.json
    prompt = data.get('prompt', '')
    models = data.get('models', [])
    responses = data.get('responses', {})
    preferred = data.get('preferred', 0)
    
    if not prompt or not models or len(models) != 2 or not responses or preferred not in [1, 2]:
        return jsonify({'error': 'Invalid rating data'}), 400
    
    try:
        # Convert to 0-based index
        preferred_idx = preferred - 1
        
        # Map to model names
        preferred_model = models[preferred_idx]
        non_preferred_model = models[1 - preferred_idx]
        
        # Format for saving
        compare.save_rating(prompt, models, responses, preferred)
        
        return jsonify({'success': True, 'preferred_model': preferred_model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)