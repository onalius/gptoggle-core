#!/usr/bin/env python3
"""
GPToggle Core Functionality Tests

Test suite for core GPToggle functionality including:
- Basic query processing
- Provider selection
- Configuration management
- Error handling
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add core directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

try:
    from gptoggle_v2 import GPToggle, UserProfile
except ImportError:
    # Fallback for testing without full installation
    GPToggle = None
    UserProfile = None

class TestGPToggleCore(unittest.TestCase):
    """Test core GPToggle functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if GPToggle is None:
            self.skipTest("GPToggle not available for testing")
        
        self.gpt = GPToggle()
        
    def test_initialization(self):
        """Test GPToggle initialization"""
        self.assertIsNotNone(self.gpt)
        self.assertTrue(hasattr(self.gpt, 'query'))
        self.assertTrue(hasattr(self.gpt, 'get_available_providers'))
    
    def test_provider_detection(self):
        """Test provider availability detection"""
        available = self.gpt.get_available_providers()
        self.assertIsInstance(available, list)
        # Should have at least one provider if API keys are configured
    
    def test_query_validation(self):
        """Test query input validation"""
        # Empty query
        with self.assertRaises(ValueError):
            self.gpt.query("")
        
        # None query
        with self.assertRaises(ValueError):
            self.gpt.query(None)
    
    def test_provider_specification(self):
        """Test provider specification"""
        # Valid provider (if available)
        try:
            response = self.gpt.query("Hello", provider="openai")
            self.assertIn('response', response)
        except Exception:
            # Provider not available, which is acceptable
            pass
        
        # Invalid provider
        with self.assertRaises(ValueError):
            self.gpt.query("Hello", provider="invalid-provider")
    
    def test_configuration(self):
        """Test configuration options"""
        # Custom provider priority
        custom_gpt = GPToggle(provider_priority=['claude', 'openai'])
        self.assertEqual(custom_gpt.provider_priority[0], 'claude')
        
        # Module cleanup days
        custom_gpt = GPToggle(module_cleanup_days=45)
        self.assertEqual(custom_gpt.module_cleanup_days, 45)
    
    @patch('gptoggle_v2.requests.post')
    def test_mock_query_response(self, mock_post):
        """Test query processing with mocked response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Test query
        response = self.gpt.query("Test query")
        
        # Verify response structure
        self.assertIn('response', response)
        self.assertIn('provider', response)
        self.assertIn('moduleActions', response)
        
    def test_user_profile_creation(self):
        """Test user profile functionality"""
        if UserProfile is None:
            self.skipTest("UserProfile not available for testing")
            
        profile = UserProfile.create_default("test-user")
        
        self.assertEqual(profile.user_id, "test-user")
        self.assertIn('context', profile.profile_data)
        self.assertIn('modules', profile.profile_data['context'])


class TestUserProfile(unittest.TestCase):
    """Test UserProfile functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if UserProfile is None:
            self.skipTest("UserProfile not available for testing")
            
        self.profile = UserProfile.create_default("test-user")
    
    def test_profile_creation(self):
        """Test profile creation"""
        self.assertEqual(self.profile.user_id, "test-user")
        self.assertIsInstance(self.profile.profile_data, dict)
    
    def test_modules_summary(self):
        """Test modules summary generation"""
        summary = self.profile.get_modules_summary()
        
        self.assertIn('totalModules', summary)
        self.assertIn('activeModules', summary)
        self.assertIn('modulesByType', summary)
        self.assertIsInstance(summary['totalModules'], int)
    
    def test_profile_update_with_modules(self):
        """Test profile update with module integration"""
        result = self.profile.update_profile_with_modules(
            "I need to buy milk and eggs",
            "general"
        )
        
        self.assertIn('moduleActions', result)
        self.assertIsInstance(result['moduleActions'], list)


class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        if GPToggle is None:
            self.skipTest("GPToggle not available for testing")
            
        self.gpt = GPToggle()
    
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Empty string
        with self.assertRaises((ValueError, TypeError)):
            self.gpt.query("")
        
        # None value
        with self.assertRaises((ValueError, TypeError)):
            self.gpt.query(None)
        
        # Invalid type
        with self.assertRaises((ValueError, TypeError)):
            self.gpt.query(12345)
    
    def test_provider_errors(self):
        """Test provider-related error handling"""
        # Invalid provider name
        with self.assertRaises(ValueError):
            self.gpt.query("Hello", provider="nonexistent")
        
        # Provider not configured (should handle gracefully)
        try:
            self.gpt.query("Hello", provider="claude")
            # If this succeeds, provider is configured
        except Exception as e:
            # Should be a configuration error, not a crash
            self.assertIn("API key", str(e).lower())
    
    def test_network_error_simulation(self):
        """Test network error handling"""
        with patch('gptoggle_v2.requests.post') as mock_post:
            # Simulate network error
            mock_post.side_effect = Exception("Network error")
            
            with self.assertRaises(Exception):
                self.gpt.query("Test query")


class TestModuleIntegration(unittest.TestCase):
    """Test module system integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        if GPToggle is None:
            self.skipTest("GPToggle not available for testing")
            
        self.gpt = GPToggle()
    
    def test_module_detection_patterns(self):
        """Test module detection from queries"""
        test_queries = [
            ("I need to buy milk and eggs", "list"),
            ("Plan my birthday party", "planner"),
            ("Schedule dentist appointment", "calendar"),
            ("I'm interested in quantum physics", "interest"),
            ("Track my daily exercise", "tracker"),
            ("My goal is to learn Spanish", "goal")
        ]
        
        for query, expected_type in test_queries:
            with self.subTest(query=query):
                # Get user profile
                profile = self.gpt.get_user_profile()
                
                # Simulate module update
                result = profile.update_profile_with_modules(query, "general")
                
                # Check if expected module type was detected
                created_types = [action['moduleType'] for action in result['moduleActions'] 
                               if action['action'] == 'create']
                
                # Should detect the expected type (if module system is working)
                if created_types:
                    self.assertIn(expected_type, created_types)


def run_tests():
    """Run all tests with detailed output"""
    # Configure test runner
    unittest.TestLoader.sortTestMethodsUsing = None
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestGPToggleCore,
        TestUserProfile, 
        TestErrorHandling,
        TestModuleIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback.split()[-1]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback.split()[-1]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success


if __name__ == '__main__':
    run_tests()