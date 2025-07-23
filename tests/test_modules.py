#!/usr/bin/env python3
"""
GPToggle Module System Tests

Test suite for the modular adaptive intelligence system including:
- Module creation and detection
- UMID generation and parsing
- Module lifecycle management
- Cross-service export/import
"""

import unittest
import sys
import os
import time
from unittest.mock import Mock, patch

# Add modules directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

try:
    from umidGenerator import UMIDGenerator, UMIDParser, UMIDMigrator
    from moduleServiceUMID import EnhancedModuleService
except ImportError:
    UMIDGenerator = None
    UMIDParser = None 
    UMIDMigrator = None
    EnhancedModuleService = None

class TestUMIDGenerator(unittest.TestCase):
    """Test UMID generation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if UMIDGenerator is None:
            self.skipTest("UMID system not available for testing")
            
        self.generator = UMIDGenerator('test-service')
    
    def test_initialization(self):
        """Test UMID generator initialization"""
        self.assertEqual(self.generator.service_id, 'test-service')
        
        # Test invalid service ID
        with self.assertRaises(ValueError):
            UMIDGenerator('InvalidService')  # Uppercase not allowed
    
    def test_context_hash_generation(self):
        """Test context hash generation"""
        keywords = ['shopping', 'groceries', 'weekly']
        hash1 = self.generator.generate_context_hash(keywords)
        hash2 = self.generator.generate_context_hash(keywords)
        
        # Same keywords should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Hash should be 8 characters
        self.assertEqual(len(hash1), 8)
        
        # Should be lowercase hex
        self.assertTrue(all(c in '0123456789abcdef' for c in hash1))
    
    def test_random_component_generation(self):
        """Test random component generation"""
        random1 = self.generator.generate_random_component()
        random2 = self.generator.generate_random_component()
        
        # Should be different
        self.assertNotEqual(random1, random2)
        
        # Should be 4 characters
        self.assertEqual(len(random1), 4)
        self.assertEqual(len(random2), 4)
        
        # Should be lowercase alphanumeric
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        self.assertTrue(all(c in allowed_chars for c in random1))
    
    def test_umid_generation(self):
        """Test complete UMID generation"""
        umid = self.generator.generate_umid('list', ['shopping', 'groceries'])
        
        # Should have correct format
        parts = umid.split('.')
        self.assertEqual(len(parts), 5)
        
        # Check each component
        self.assertEqual(parts[0], 'test-service')  # service
        self.assertEqual(parts[1], 'list')          # module type
        self.assertEqual(len(parts[2]), 8)          # context hash
        self.assertEqual(len(parts[3]), 10)         # timestamp
        self.assertEqual(len(parts[4]), 4)          # random
    
    def test_umid_validation(self):
        """Test UMID format validation"""
        # Valid UMID
        valid_umid = self.generator.generate_umid('list', ['test'])
        self.assertTrue(self.generator.validate_umid(valid_umid))
        
        # Invalid UMIDs
        invalid_umids = [
            'invalid',
            'too.few.parts',
            'too.many.parts.in.this.umid.here',
            'UPPERCASE.list.12345678.1234567890.abcd',
            'test.INVALID.12345678.1234567890.abcd',
            'test.list.invalid.1234567890.abcd',
        ]
        
        for invalid in invalid_umids:
            with self.subTest(umid=invalid):
                self.assertFalse(self.generator.validate_umid(invalid))


class TestUMIDParser(unittest.TestCase):
    """Test UMID parsing functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if UMIDParser is None:
            self.skipTest("UMID system not available for testing")
            
        self.parser = UMIDParser()
        self.generator = UMIDGenerator('test-service')
    
    def test_umid_parsing(self):
        """Test UMID parsing"""
        # Generate a test UMID
        umid = self.generator.generate_umid('list', ['shopping', 'groceries'])
        
        # Parse it
        parsed = self.parser.parse(umid)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['service'], 'test-service')
        self.assertEqual(parsed['moduleType'], 'list')
        self.assertEqual(len(parsed['contextHash']), 8)
        self.assertIsInstance(parsed['timestamp'], int)
        self.assertEqual(len(parsed['randomComponent']), 4)
        self.assertIsInstance(parsed['createdAt'], str)  # ISO format
    
    def test_invalid_umid_parsing(self):
        """Test parsing of invalid UMIDs"""
        invalid_umids = [
            'invalid-format',
            'too.few.parts',
            None,
            '',
            123
        ]
        
        for invalid in invalid_umids:
            with self.subTest(umid=invalid):
                result = self.parser.parse(invalid)
                self.assertIsNone(result)
    
    def test_validation(self):
        """Test UMID validation"""
        # Valid UMID
        valid_umid = self.generator.generate_umid('tracker', ['exercise'])
        self.assertTrue(self.parser.validate(valid_umid))
        
        # Invalid UMID
        self.assertFalse(self.parser.validate('invalid-umid'))


class TestEnhancedModuleService(unittest.TestCase):
    """Test enhanced module service functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if EnhancedModuleService is None:
            self.skipTest("Enhanced module service not available for testing")
            
        self.service = EnhancedModuleService('test-service')
        self.user_profile = {
            'userId': 'test-user',
            'context': {
                'modules': {}
            }
        }
    
    def test_service_initialization(self):
        """Test service initialization"""
        self.assertEqual(self.service.service_id, 'test-service')
        self.assertIsNotNone(self.service.umid_generator)
        self.assertIsNotNone(self.service.umid_parser)
    
    def test_module_creation_with_umid(self):
        """Test module creation with UMID"""
        module_data = self.service.create_module_with_umid(
            'list',
            ['shopping', 'groceries'],
            ['milk', 'eggs', 'bread'],
            priority=8
        )
        
        # Should have one module
        self.assertEqual(len(module_data), 1)
        
        # Get the UMID and module
        umid = list(module_data.keys())[0]
        module = module_data[umid]
        
        # Validate UMID format
        self.assertTrue(self.service.umid_parser.validate(umid))
        
        # Validate module structure
        self.assertEqual(module['type'], 'list')
        self.assertEqual(module['data'], ['milk', 'eggs', 'bread'])
        self.assertEqual(module['metadata']['priority'], 8)
        self.assertIn('createdAt', module['metadata'])
    
    def test_module_update_by_umid(self):
        """Test updating modules by UMID"""
        # Create a module first
        module_data = self.service.create_module_with_umid(
            'list',
            ['shopping'],
            ['milk', 'eggs']
        )
        
        # Add to user profile
        self.user_profile['context']['modules'].update(module_data)
        
        # Update the module
        umid = list(module_data.keys())[0]
        success = self.service.update_module_by_umid(
            self.user_profile,
            umid,
            ['milk', 'eggs', 'bread', 'cheese']
        )
        
        self.assertTrue(success)
        
        # Check if module was updated
        updated_module = self.user_profile['context']['modules'][umid]
        self.assertIn('bread', updated_module['data'])
        self.assertIn('cheese', updated_module['data'])
    
    def test_query_analysis_for_modules(self):
        """Test query analysis for module operations"""
        # Create a shopping list module
        module_data = self.service.create_module_with_umid(
            'list',
            ['shopping', 'groceries'],
            ['milk', 'eggs']
        )
        self.user_profile['context']['modules'].update(module_data)
        
        # Analyze query that should update the list
        result = self.service.analyze_query_for_modules_umid(
            "Add bread and cheese to my shopping list",
            self.user_profile
        )
        
        self.assertIn('moduleActions', result)
        self.assertGreater(len(result['moduleActions']), 0)
        
        # Should have detected update action
        update_actions = [a for a in result['moduleActions'] if a['action'] == 'update']
        self.assertGreater(len(update_actions), 0)
    
    def test_module_export(self):
        """Test module export for cross-service compatibility"""
        # Create test modules
        module1 = self.service.create_module_with_umid('list', ['shopping'], ['milk'])
        module2 = self.service.create_module_with_umid('tracker', ['exercise'], {'target': 30})
        
        self.user_profile['context']['modules'].update(module1)
        self.user_profile['context']['modules'].update(module2)
        
        # Export modules
        export_data = self.service.export_modules_for_service(
            self.user_profile,
            'target-service'
        )
        
        self.assertEqual(export_data['source_service'], 'test-service')
        self.assertEqual(export_data['target_service'], 'target-service')
        self.assertEqual(len(export_data['modules']), 2)
        
        # Check export format
        for umid, exported_module in export_data['modules'].items():
            self.assertIn('original_umid', exported_module)
            self.assertIn('type', exported_module)
            self.assertIn('data', exported_module)
            self.assertIn('metadata', exported_module)
    
    def test_module_cleanup(self):
        """Test module lifecycle cleanup"""
        # Create modules with different ages
        old_module = self.service.create_module_with_umid('list', ['old'], ['item'])
        recent_module = self.service.create_module_with_umid('tracker', ['recent'], {})
        
        # Manually set old timestamp
        old_umid = list(old_module.keys())[0]
        old_time = time.time() - (35 * 24 * 60 * 60)  # 35 days ago
        old_module[old_umid]['metadata']['lastAccessed'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(old_time))
        
        self.user_profile['context']['modules'].update(old_module)
        self.user_profile['context']['modules'].update(recent_module)
        
        # Run cleanup
        cleanup_result = self.service.cleanup_stale_modules_umid(self.user_profile, archive_days=30)
        
        self.assertIn('archived', cleanup_result)
        self.assertIn('removed', cleanup_result)
        
        # Old module should be archived
        archived_module = self.user_profile['context']['modules'][old_umid]
        self.assertTrue(archived_module['metadata'].get('archived', False))


class TestModuleIntegration(unittest.TestCase):
    """Test integration between modules and main system"""
    
    def setUp(self):
        """Set up test fixtures"""
        if EnhancedModuleService is None:
            self.skipTest("Module system not available for testing")
            
        self.service = EnhancedModuleService('integration-test')
    
    def test_shopping_list_workflow(self):
        """Test complete shopping list workflow"""
        user_profile = {'context': {'modules': {}}}
        
        # Step 1: Create shopping list
        result1 = self.service.analyze_query_for_modules_umid(
            "I need to buy milk, eggs, and bread",
            user_profile
        )
        
        # Should create a list module
        create_actions = [a for a in result1['moduleActions'] if a['action'] == 'create']
        self.assertGreater(len(create_actions), 0)
        
        list_actions = [a for a in create_actions if a['moduleType'] == 'list']
        self.assertGreater(len(list_actions), 0)
        
        # Step 2: Add items to existing list
        result2 = self.service.analyze_query_for_modules_umid(
            "Also add cheese and yogurt to my shopping list",
            user_profile
        )
        
        # Should update existing list
        update_actions = [a for a in result2['moduleActions'] if a['action'] == 'update']
        self.assertEqual(len(update_actions), 1)  # Should find and update existing list
    
    def test_party_planning_workflow(self):
        """Test party planning workflow"""
        user_profile = {'context': {'modules': {}}}
        
        # Create party planning module
        result = self.service.analyze_query_for_modules_umid(
            "I'm planning a birthday party for March 15th with Alice, Bob, and Charlie",
            user_profile
        )
        
        # Should create planner module
        create_actions = [a for a in result['moduleActions'] if a['action'] == 'create']
        planner_actions = [a for a in create_actions if a['moduleType'] == 'planner']
        
        self.assertGreater(len(planner_actions), 0)
    
    def test_cross_module_intelligence(self):
        """Test intelligence across multiple module types"""
        user_profile = {'context': {'modules': {}}}
        
        # Create multiple modules
        queries = [
            "I need to buy party supplies",
            "Plan Sarah's birthday party for next weekend", 
            "I'm interested in party planning techniques"
        ]
        
        for query in queries:
            self.service.analyze_query_for_modules_umid(query, user_profile)
        
        # Should have created different types of modules
        modules = user_profile['context']['modules']
        module_types = set()
        
        for module in modules.values():
            module_types.add(module['type'])
        
        # Should have multiple module types
        self.assertGreater(len(module_types), 1)


def run_module_tests():
    """Run all module tests with detailed output"""
    unittest.TestLoader.sortTestMethodsUsing = None
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestUMIDGenerator,
        TestUMIDParser,
        TestEnhancedModuleService,
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
    print(f"Module Tests Summary")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All module tests passed!' if success else '❌ Some module tests failed!'}")
    
    return success


if __name__ == '__main__':
    run_module_tests()