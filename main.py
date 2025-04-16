"""
Flask web interface for the GPToggle multi-provider AI model wrapper.
This provides a web UI for the same functionality available in the CLI.
"""
import os
import sys
from flask import Flask, render_template, request, jsonify

# Try to import the package - this will work if installed
try:
    from gptoggle import (
        Config, 
        config,
        get_response, 
        choose_provider_and_model, 
        compare_models, 
        get_provider_instance
    )
except ImportError:
    # If not installed, try to import from local path
    sys.path.insert(0, ".")
    from gptoggle import (
        Config, 
        config,
        get_response, 
        choose_provider_and_model, 
        compare_models,
        get_provider_instance
    )

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key")

@app.route('/')
def index():
    """Render the main page."""
    # Get all provider configurations
    providers = config.get_enabled_providers()
    
    # Collect models from all providers
    all_models = []
    for provider_name in providers:
        provider = get_provider_instance(provider_name)
        if provider and provider.validate_api_key():
            provider_models = [f"{provider_name}:{model}" for model in provider.available_models]
            all_models.extend(provider_models)
        
    return render_template('index.html', models=all_models)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests from the web interface."""
    data = request.json
    prompt = data.get('prompt', '')
    selected_model_str = data.get('model', '')
    
    # Auto-select model if none provided
    if not selected_model_str:
        provider, model, reason = choose_provider_and_model(prompt)
        selected_provider = provider
        selected_model = model
    else:
        # Parse provider:model format
        if ":" in selected_model_str:
            selected_provider, selected_model = selected_model_str.split(":", 1)
            reason = "Manually selected by user"
        else:
            # Default to OpenAI if no provider specified
            selected_provider = "openai"
            selected_model = selected_model_str
            reason = "Manually selected by user"
    
    # Get response from model
    try:
        response_text = get_response(
            prompt, 
            provider_name=selected_provider, 
            model=selected_model
        )
        
        return jsonify({
            'response': response_text,
            'provider': selected_provider,
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
    model_pairs = data.get('models', [])
    
    # Parse model strings into provider:model pairs
    parsed_pairs = []
    for model_str in model_pairs:
        if ":" in model_str:
            provider, model = model_str.split(":", 1)
            parsed_pairs.append((provider, model))
        else:
            # Default to OpenAI if no provider specified
            parsed_pairs.append(("openai", model_str))
    
    # Ensure exactly two models
    if len(parsed_pairs) != 2:
        return jsonify({'error': 'Exactly two models must be selected for comparison'}), 400
    
    # Get responses
    try:
        # Prepare a dict to store responses
        responses = {}
        
        # Get response from each model
        for provider_name, model_name in parsed_pairs:
            response_text = get_response(
                prompt=prompt,
                provider_name=provider_name,
                model=model_name,
                max_tokens=config.get_provider_config(provider_name).max_comparison_tokens
            )
            
            # Store response with provider:model as key
            model_key = f"{provider_name}:{model_name}"
            responses[model_key] = response_text
        
        return jsonify({
            'responses': responses,
            'models': [f"{p}:{m}" for p, m in parsed_pairs]
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
        
        # Parse model strings into provider:model pairs
        model_pairs = []
        for model_str in models:
            if ":" in model_str:
                provider, model = model_str.split(":", 1)
                model_pairs.append((provider, model))
            else:
                # Default to OpenAI if no provider specified
                model_pairs.append(("openai", model_str))
        
        # Format for saving
        from gptoggle.compare import save_rating
        save_rating(prompt, model_pairs, responses, preferred)
        
        return jsonify({'success': True, 'preferred_model': preferred_model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)