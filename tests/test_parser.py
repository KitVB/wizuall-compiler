# tests/test_parser.py
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.lexer import Lexer
from parser.parser import Parser, NumberNode, IdentifierNode, BinaryOpNode, AssignmentNode

class TestParser(unittest.TestCase):
    def test_basic_expression(self):
        source_code = "10 + 20"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.expression()
        
        self.assertIsInstance(ast, BinaryOpNode)
        self.assertIsInstance(ast.left, NumberNode)
        self.assertIsInstance(ast.right, NumberNode)
        self.assertEqual(ast.left.value, 10)
        self.assertEqual(ast.right.value, 20)
    
    def test_assignment(self):
        source_code = "x = 10"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.assignment_statement()
        
        self.assertIsInstance(ast, AssignmentNode)
        self.assertIsInstance(ast.identifier, IdentifierNode)
        self.assertIsInstance(ast.expr, NumberNode)
        self.assertEqual(ast.identifier.name, "x")
        self.assertEqual(ast.expr.value, 10)
    
    def test_complex_expression(self):
        source_code = "a = 10 + 20 * 30"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.assignment_statement()
        
        self.assertIsInstance(ast, AssignmentNode)
        self.assertIsInstance(ast.identifier, IdentifierNode)
        self.assertIsInstance(ast.expr, BinaryOpNode)
        self.assertEqual(ast.identifier.name, "a")
        
        # Check that the expression follows operator precedence
        # It should be: a = (10 + (20 * 30))
        plus_node = ast.expr
        self.assertIsInstance(plus_node, BinaryOpNode)
        self.assertIsInstance(plus_node.left, NumberNode)
        self.assertIsInstance(plus_node.right, BinaryOpNode)
        self.assertEqual(plus_node.left.value, 10)
        
        mult_node = plus_node.right
        self.assertIsInstance(mult_node, BinaryOpNode)
        self.assertIsInstance(mult_node.left, NumberNode)
        self.assertIsInstance(mult_node.right, NumberNode)
        self.assertEqual(mult_node.left.value, 20)
        self.assertEqual(mult_node.right.value, 30)
    
    def test_program(self):
        source_code = """
        x = 10
        y = 20
        z = x + y
        """
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Verify we got a statements node with 3 statements
        self.assertEqual(len(ast.statements), 3)
        
        # Check each statement is an assignment
        for stmt in ast.statements:
            self.assertIsInstance(stmt, AssignmentNode)
        
        # Check the third assignment (z = x + y)
        z_assign = ast.statements[2]
        self.assertEqual(z_assign.identifier.name, "z")
        self.assertIsInstance(z_assign.expr, BinaryOpNode)
        self.assertEqual(z_assign.expr.left.name, "x")
        self.assertEqual(z_assign.expr.right.name, "y")

if __name__ == '__main__':
    unittest.main()