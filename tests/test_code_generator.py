# tests/test_code_generator.py
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.lexer import Lexer
from parser.parser import Parser
from semantics.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def test_basic_python_generation(self):
        source_code = """
        x = 10
        y = 20
        z = x + y
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'python')
        generated_code = code_generator.generate()
        
        # Check that generated code contains the expected Python code
        self.assertIn("import numpy", generated_code)
        self.assertIn("x = 10.0", generated_code)
        self.assertIn("y = 20.0", generated_code)
        self.assertIn("z = (x + y)", generated_code)
    
    def test_conditional_generation(self):
        source_code = """
        x = 10
        if (x > 5) {
            y = 20
        } else {
            y = 30
        }
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'python')
        generated_code = code_generator.generate()
        
        # Check that generated code contains the expected Python conditional
        self.assertIn("if (x > 5.0):", generated_code)
        self.assertIn("y = 20.0", generated_code)
        self.assertIn("else:", generated_code)
        self.assertIn("y = 30.0", generated_code)
    
    def test_loop_generation(self):
        source_code = """
        i = 0
        while (i < 10) {
            j = i * 2
            i = i + 1
        }
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'python')
        generated_code = code_generator.generate()
        
        # Check that generated code contains the expected Python loop
        self.assertIn("i = 0", generated_code)
        self.assertIn("while (i < 10.0):", generated_code)
        self.assertIn("j = (i * 2.0)", generated_code)
        self.assertIn("i = (i + 1.0)", generated_code)
    
    def test_vector_generation(self):
        source_code = """
        v = [1.0, 2.0, 3.0]
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'python')
        generated_code = code_generator.generate()
        
        # Check that generated code creates a numpy array
        self.assertIn("v = np.array([1.0, 2.0, 3.0])", generated_code)
    
    def test_visualization_function_generation(self):
        source_code = """
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [10.0, 20.0, 30.0, 40.0, 50.0]
        plot(x, y)
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'python')
        generated_code = code_generator.generate()
        
        # Check that generated code includes visualization code
        self.assertIn("x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])", generated_code)
        self.assertIn("y = np.array([10.0, 20.0, 30.0, 40.0, 50.0])", generated_code)
        self.assertIn("plt.plot", generated_code)
        self.assertIn("plt.show", generated_code)
    
    def test_c_code_generation(self):
        source_code = """
        x = 10
        y = 20
        z = x + y
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'c')
        generated_code = code_generator.generate()
        
        # Check that generated code contains C-style variable declarations
        self.assertIn("#include <stdio.h>", generated_code)
        self.assertIn("double x = 10.0", generated_code)
        self.assertIn("double y = 20.0", generated_code)
        self.assertIn("double z = (x + y)", generated_code)
    
    def test_r_code_generation(self):
        source_code = """
        x = 10
        y = 20
        z = x + y
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        code_generator = CodeGenerator(ast, 'r')
        generated_code = code_generator.generate()
        
        # Check that generated code contains R-style assignment
        self.assertIn("library(ggplot2)", generated_code)
        self.assertIn("x <- 10.0", generated_code)
        self.assertIn("y <- 20.0", generated_code)
        self.assertIn("z <- (x + y)", generated_code)

if __name__ == '__main__':
    unittest.main()