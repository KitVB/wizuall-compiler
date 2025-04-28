# tests/test_scanner.py
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.lexer import Lexer, TokenType, Token

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        source_code = "x = 10 + 20"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.IDENTIFIER,  # x
            TokenType.ASSIGN,      # =
            TokenType.NUMBER,      # 10
            TokenType.PLUS,        # +
            TokenType.NUMBER,      # 20
            TokenType.EOF          # End of file
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.token_type, expected_type)
    
    def test_vector_tokens(self):
        source_code = "v = [1, 2, 3]"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.IDENTIFIER,  # v
            TokenType.ASSIGN,      # =
            TokenType.LBRACKET,    # [
            TokenType.NUMBER,      # 1
            TokenType.COMMA,       # ,
            TokenType.NUMBER,      # 2
            TokenType.COMMA,       # ,
            TokenType.NUMBER,      # 3
            TokenType.RBRACKET,    # ]
            TokenType.EOF          # End of file
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.token_type, expected_type)
    
    def test_keywords(self):
        source_code = "if (x > 10) { y = 20 } else { y = 30 }"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Just check the keywords
        self.assertEqual(tokens[0].token_type, TokenType.IF)
        # Find the ELSE token
        else_token = None
        for token in tokens:
            if token.token_type == TokenType.ELSE:
                else_token = token
                break
        
        self.assertIsNotNone(else_token)
    
    def test_function_call(self):
        source_code = "plot(x, y)"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.IDENTIFIER,  # plot
            TokenType.LPAREN,      # (
            TokenType.IDENTIFIER,  # x
            TokenType.COMMA,       # ,
            TokenType.IDENTIFIER,  # y
            TokenType.RPAREN,      # )
            TokenType.EOF          # End of file
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.token_type, expected_type)

if __name__ == '__main__':
    unittest.main()