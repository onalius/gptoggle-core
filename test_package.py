#!/usr/bin/env python3
"""
Test script to verify the gptoggle package installation.
"""
import sys
import os

def test_imports():
    """Test importing the gptoggle package."""
    try:
        sys.path.insert(0, os.path.abspath("gptoggle-core"))
        from gptoggle import choose_model, get_response, compare_models
        from gptoggle import OpenAIConfig, AVAILABLE_MODELS
        print("✓ Successfully imported gptoggle modules")
        return True
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        return False

def test_model_selection():
    """Test the model selection functionality."""
    try:
        from gptoggle import choose_model
        
        test_prompts = [
            "What is the capital of France?",
            "Write code to implement a binary search tree in Python",
            "Write a short story about a robot learning to paint"
        ]
        
        print("\nTesting model selection:")
        for prompt in test_prompts:
            model, reason = choose_model(prompt)
            print(f"  Prompt: '{prompt[:30]}...'")
            print(f"  Selected model: {model}")
            print(f"  Reason: {reason}\n")
        
        return True
    except Exception as e:
        print(f"✗ Model Selection Error: {e}")
        return False

def test_config():
    """Test the configuration module."""
    try:
        from gptoggle import OpenAIConfig, AVAILABLE_MODELS
        
        print("\nAvailable models:")
        for model in AVAILABLE_MODELS:
            print(f"  - {model}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration Error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing GPToggle Package Installation\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Model Selection Test", test_model_selection),
        ("Configuration Test", test_config)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if not test_func():
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed successfully!")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())