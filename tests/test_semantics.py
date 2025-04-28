# tests/test_semantic_analyzer.py
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.lexer import Lexer
from parser.parser import Parser
from semantics.semantic_analyzer import SemanticAnalyzer

class TestSemanticAnalyzer(unittest.TestCase):
    def test_basic_assignment(self):
        source_code = "x = 10"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
        
        # Check that x is in the symbol table
        self.assertIn('x', analyzer.symbol_table.symbols)
        self.assertEqual(analyzer.symbol_table.symbols['x'].value, 10)
    
    def test_undefined_variable(self):
        source_code = "x = y + 10"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        # In WizuAll, undefined variables should get default value 0
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
        
        # Check that y is in the symbol table with default value 0
        self.assertIn('y', analyzer.symbol_table.symbols)
        self.assertEqual(analyzer.symbol_table.symbols['y'].value, 0)
    
    def test_vector_operations(self):
        source_code = """
        v1 = [1, 2, 3]
        v2 = [4, 5, 6]
        v3 = v1 + v2
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
        
        # Check that v3 contains the sum of v1 and v2
        self.assertIn('v3', analyzer.symbol_table.symbols)
        expected = [1 + 4, 2 + 5, 3 + 6]  # [5, 7, 9]
        self.assertEqual(analyzer.symbol_table.symbols['v3'].value, expected)
    
    def test_vector_scalar_operations(self):
        source_code = """
        v = [1, 2, 3]
        s = 2
        result = v * s
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
        
        # Check that result contains v * s
        self.assertIn('result', analyzer.symbol_table.symbols)
        expected = [1 * 2, 2 * 2, 3 * 2]  # [2, 4, 6]
        self.assertEqual(analyzer.symbol_table.symbols['result'].value, expected)
    
    def test_vector_dimension_mismatch(self):
        source_code = """
        v1 = [1, 2, 3]
        v2 = [4, 5]
        v3 = v1 + v2
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        # This should produce an error but still be valid (using v1 as fallback)
        self.assertTrue(valid)  # We are being lenient in WizuAll
        self.assertEqual(len(errors), 1)  # But we record the error
        
        # Check the error message
        self.assertIn("dimension", errors[0].lower())
    
    def test_division_by_zero(self):
        source_code = "x = 10 / 0"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        valid, errors = analyzer.analyze()
        
        # This should produce an error but still be valid (using left operand as fallback)
        self.assertTrue(valid)  # We are being lenient in WizuAll
        self.assertEqual(len(errors), 1)  # But we record the error
        
        # Check the error message
        self.assertIn("division by zero", errors[0].lower())

if __name__ == '__main__':
    unittest.main()