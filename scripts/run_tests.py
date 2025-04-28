# scripts/run_tests.py
import os
import sys
import unittest
import importlib
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def discover_and_run_tests(test_module=None):
    """Discover and run tests, optionally filtering by module name"""
    tests_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests')
    
    if test_module:
        # Run specific test module
        module_path = os.path.join(tests_dir, f"test_{test_module}.py")
        if not os.path.exists(module_path):
            print(f"Test module not found: {module_path}")
            return False
        
        # Import the module
        module_name = f"tests.test_{test_module}"
        try:
            module = importlib.import_module(module_name)
            suite = unittest.TestLoader().loadTestsFromModule(module)
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            return result.wasSuccessful()
        except ImportError as e:
            print(f"Error importing module {module_name}: {e}")
            return False
    else:
        # Run all tests
        suite = unittest.defaultTestLoader.discover(tests_dir, pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()

def main():
    parser = argparse.ArgumentParser(description='WizuAll Test Runner')
    parser.add_argument('--module', help='Specific test module to run (without the "test_" prefix)')
    
    args = parser.parse_args()
    
    success = discover_and_run_tests(args.module)
    
    if success:
        print("All tests passed successfully.")
        return 0
    else:
        print("Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())