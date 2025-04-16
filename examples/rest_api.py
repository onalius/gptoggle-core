#!/usr/bin/env python3
"""
GPToggle REST API Example

This script demonstrates how to create a simple REST API using Flask to serve AI responses
from GPToggle. This can be used by Node.js applications to interact with GPToggle without
needing to use Python child processes.

Usage:
    python rest_api.py

API endpoints:
    GET /providers - List all available providers
    GET /models - List all available models for a provider
    POST /recommend - Get a recommended model for a prompt
    POST /generate - Generate a response for a prompt
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

import gptoggle
from gptoggle import get_response, recommend_model, list_available_models, config

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set API keys from environment variables (best practice for deployment)
# For development, you can set them here
if "OPENAI_API_KEY" not in os.environ:
    print("Warning: OPENAI_API_KEY not set in environment")

# ======== API Routes ========

@app.route("/api/providers", methods=["GET"])
def get_providers():
    """Get a list of all available providers."""
    try:
        providers = config.get_enabled_providers()
        return jsonify({
            "success": True,
            "providers": providers
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/models", methods=["GET"])
def get_models():
    """Get a list of models for a specific provider."""
    provider = request.args.get("provider", "openai")
    try:
        models = list_available_models(provider)
        return jsonify({
            "success": True,
            "provider": provider,
            "models": models
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """Get a recommended model for a prompt."""
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({
            "success": False,
            "error": "Missing prompt in request body"
        }), 400

    try:
        prompt = data["prompt"]
        model = recommend_model(prompt)
        return jsonify({
            "success": True,
            "model": model
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/generate", methods=["POST"])
def generate():
    """Generate a response for a prompt."""
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({
            "success": False,
            "error": "Missing prompt in request body"
        }), 400

    try:
        prompt = data["prompt"]
        provider = data.get("provider")
        model = data.get("model")
        temperature = data.get("temperature", 0.7)
        max_tokens = data.get("max_tokens", 1000)

        response = get_response(
            prompt=prompt,
            provider_name=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return jsonify({
            "success": True,
            "response": response
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Main function
if __name__ == "__main__":
    # Print helpful information
    print("=" * 50)
    print("GPToggle REST API Example")
    print("=" * 50)
    print("\nAPI Endpoints:")
    print("  GET  /api/providers - List all available providers")
    print("  GET  /api/models    - List all available models for a provider")
    print("  POST /api/recommend - Get a recommended model for a prompt")
    print("  POST /api/generate  - Generate a response for a prompt")
    print("\nExample Node.js usage with fetch:")
    print("""
fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'What is the meaning of life?',
    provider: 'openai',
    model: 'gpt-4o'
  }),
})
.then(response => response.json())
.then(data => console.log(data));
    """)
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)