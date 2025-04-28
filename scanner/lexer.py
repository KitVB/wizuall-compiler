# scanner/lexer.py
import re
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    GREATER = auto()
    LESS = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    
    # Others
    IDENTIFIER = auto()
    NUMBER = auto()
    EOF = auto()
    STRING = auto()

class Token:
    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.token_type}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source_code[0] if source_code else None
        
        # Define keyword mapping
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE
        }
    
    def advance(self):
        """Move to next character in source code"""
        self.position += 1
        if self.position < len(self.source_code):
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        """Skip spaces, tabs, and newlines"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """Parse a number from current position"""
        result = ''
        decimal_point_count = 0
        line = self.line
        column = self.column
        
        while (self.current_char is not None and 
               (self.current_char.isdigit() or self.current_char == '.')):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break
            result += self.current_char
            self.advance()
        
        return Token(TokenType.NUMBER, float(result), line, column)
    
    def string(self):
        """Parse a string literal"""
        result = ''
        line = self.line
        column = self.column
        
        # Skip the opening quote
        self.advance()
        
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        # Skip the closing quote
        if self.current_char == '"':
            self.advance()
        else:
            raise Exception(f"Unterminated string at {line}:{column}")
        
        return Token(TokenType.STRING, result, line, column)
    
    def identifier(self):
        """Parse an identifier or keyword from current position"""
        result = ''
        line = self.line
        column = self.column
        
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            result += self.current_char
            self.advance()
        
        # Check if identifier is a keyword
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, line, column)
    
    def skip_comment(self):
        """Skip comments (starting with #)"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        
        # Skip the newline character
        if self.current_char == '\n':
            self.advance()
    
    def get_next_token(self):
        """Tokenize the next element in the source code"""
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '>':
                token = Token(TokenType.GREATER, '>', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '<':
                token = Token(TokenType.LESS, '<', self.line, self.column)
                self.advance()
                return token
            
            # Identify tokens
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            
            # Operators and delimiters
            if self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '*':
                token = Token(TokenType.MULTIPLY, '*', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '/':
                token = Token(TokenType.DIVIDE, '/', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '=':
                token = Token(TokenType.ASSIGN, '=', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '{':
                token = Token(TokenType.LBRACE, '{', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '}':
                token = Token(TokenType.RBRACE, '}', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '[':
                token = Token(TokenType.LBRACKET, '[', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ']':
                token = Token(TokenType.RBRACKET, ']', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ',':
                token = Token(TokenType.COMMA, ',', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char == '"':
                return self.string()


            # Handle unknown characters
            raise Exception(f"Invalid character '{self.current_char}' at {self.line}:{self.column}")
        
        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self):
        """Convert the entire source code into tokens"""
        tokens = []
        token = self.get_next_token()
        
        while token.token_type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        
        tokens.append(token)  # Append EOF token
        return tokens