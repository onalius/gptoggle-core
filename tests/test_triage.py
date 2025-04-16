"""
Tests for the triage module.
"""
import pytest
from gptoggle.chat import choose_provider_and_model

def test_choose_model_general():
    """Test provider and model selection for general queries."""
    prompt = "What is the capital of France?"
    provider, model, reason = choose_provider_and_model(prompt)
    assert provider is not None
    assert model is not None
    assert reason is not None
    assert "general" in reason.lower() or "simple" in reason.lower()

def test_choose_model_code():
    """Test model selection for code-related queries."""
    prompt = "Write a function in Python to find the greatest common divisor of two numbers"
    model, reason = choose_model(prompt)
    assert model is not None
    assert reason is not None
    assert "code" in reason.lower()

def test_choose_model_creative():
    """Test model selection for creative queries."""
    prompt = "Write a short story about a robot learning to paint"
    model, reason = choose_model(prompt)
    assert model is not None
    assert reason is not None
    assert "creative" in reason.lower() or "story" in reason.lower()

def test_choose_model_long():
    """Test model selection for long queries."""
    # Generate a long prompt
    prompt = "Explain " + "very " * 500 + "thoroughly how a computer works."
    model, reason = choose_model(prompt)
    assert model is not None
    assert reason is not None
    assert "long" in reason.lower()