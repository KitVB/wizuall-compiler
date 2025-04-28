# runtime/executor.py
import os
import subprocess
import tempfile

class RuntimeExecutor:
    def __init__(self, target_code, target_language='python'):
        self.target_code = target_code
        self.target_language = target_language
        
        # Define supported target languages and their execution commands
        self.language_configs = {
            'python': {
                'extension': '.py',
                'execute_cmd': ['python', '{}']
            },
            'c': {
                'extension': '.c',
                'compile_cmd': ['gcc', '{}', '-o', '{}.out', '-lm'],
                'execute_cmd': ['./{}']
            },
            'r': {
                'extension': '.R',
                'execute_cmd': ['Rscript', '{}']
            }
        }
    
    def execute(self):
        """Save, compile if needed, and execute the generated code"""
        if self.target_language not in self.language_configs:
            raise ValueError(f"Unsupported target language: {self.target_language}")
        
        config = self.language_configs[self.target_language]
        
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(suffix=config['extension'], delete=False) as temp:
            temp_filename = temp.name
            temp.write(self.target_code.encode('utf-8'))
        
        try:
            # Compile if needed (e.g., for C)
            if 'compile_cmd' in config:
                compile_cmd = [cmd.format(temp_filename) for cmd in config['compile_cmd']]
                result = subprocess.run(compile_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                
                if result.returncode != 0:
                    error_message = result.stderr.decode('utf-8')
                    raise Exception(f"Compilation error:\n{error_message}")
                
                # Set the execute command to the compiled binary
                execute_cmd = [cmd.format(temp_filename.replace(config['extension'], '.out')) for cmd in config['execute_cmd']]
            else:
                # For interpreted languages
                execute_cmd = [cmd.format(temp_filename) for cmd in config['execute_cmd']]
            
            # Execute the code
            result = subprocess.run(execute_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            
            if result.returncode != 0:
                error_message = result.stderr.decode('utf-8')
                raise Exception(f"Execution error:\n{error_message}")
            
            # Return the output
            return result.stdout.decode('utf-8')
        
        finally:
            # Clean up temporary files
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            
            # Clean up compiled binary for C
            if self.target_language == 'c':
                binary_path = temp_filename.replace(config['extension'], '.out')
                if os.path.exists(binary_path):
                    os.unlink(binary_path)