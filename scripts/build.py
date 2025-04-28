# scripts/build.py
import os
import sys
import subprocess
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    """Run all unit tests"""
    print("Running unit tests...")
    tests_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests')
    test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
    
    all_passed = True
    for test_file in test_files:
        print(f"Running {test_file}...")
        result = subprocess.run([sys.executable, os.path.join(tests_dir, test_file)], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            all_passed = False
            print(f"FAILED: {test_file}")
            print(result.stderr)
        else:
            print(f"PASSED: {test_file}")
    
    return all_passed

def build_project():
    """Build the project"""
    print("Building WizuAll compiler...")
    
    # Check if package directories exist
    required_dirs = [
        'preprocessor', 'scanner', 'parser', 'semantics', 
        'visual_primitives', 'runtime', 'tests', 'scripts'
    ]
    
    for directory in required_dirs:
        dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {directory}")
    
    # Create __init__.py files if they don't exist
    for directory in required_dirs:
        init_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Initialize package\n')
            print(f"Created __init__.py in {directory}")
    
    print("WizuAll compiler built successfully")
    return True

def compile_sample():
    """Compile the sample WizuAll program"""
    print("Compiling sample WizuAll program...")
    
    # Path to main.py and sample program
    main_py = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'main.py')
    sample_wzl = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sample.wzl')
    
    # Check if sample program exists
    if not os.path.exists(sample_wzl):
        print("Sample program not found. Creating it...")
        with open(sample_wzl, 'w') as f:
            f.write("""# sample.wzl - Sample WizuAll program

# Define data vectors
x = [1, 2, 3, 4, 5]
y = [5, 7, 9, 11, 13]

# Calculate some statistics
sum_x = vec_average(x)
max_y = vec_max(y)

# Perform vector operations
z = x + y

# Create a basic line plot
plot(x, y)

# Output the final result
print(z)
""")
        print("Sample program created at: sample.wzl")
    
    # Compile the sample program
    result = subprocess.run([sys.executable, main_py, sample_wzl, '--target', 'python', '--execute', '--verbose'],
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr)
        return False
    else:
        print("Compilation succeeded:")
        print(result.stdout)
        return True

def main():
    parser = argparse.ArgumentParser(description='WizuAll Build Script')
    parser.add_argument('--tests', action='store_true', help='Run unit tests')
    parser.add_argument('--build', action='store_true', help='Build the project')
    parser.add_argument('--sample', action='store_true', help='Compile the sample program')
    parser.add_argument('--all', action='store_true', help='Run tests, build, and compile sample')
    
    args = parser.parse_args()
    
    # If no arguments, run all
    if not (args.tests or args.build or args.sample):
        args.all = True
    
    success = True
    
    if args.tests or args.all:
        if not run_tests():
            success = False
            print("Some tests failed.")
    
    if args.build or args.all:
        if not build_project():
            success = False
            print("Build failed.")
    
    if args.sample or args.all:
        if not compile_sample():
            success = False
            print("Sample compilation failed.")
    
    if success:
        print("All operations completed successfully.")
        return 0
    else:
        print("Some operations failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())