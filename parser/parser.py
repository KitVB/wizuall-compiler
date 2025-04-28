# parser/parser.py
from scanner.lexer import TokenType, Token

class ASTNode:
    pass

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.op.value} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"({self.op.value}{self.expr})"

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __str__(self):
        return str(self.value)

class IdentifierNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.name = token.value
    
    def __str__(self):
        return self.name

class AssignmentNode(ASTNode):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr
    
    def __str__(self):
        return f"{self.identifier} = {self.expr}"

class StatementNode(ASTNode):
    def __init__(self, statement):
        self.statement = statement
    
    def __str__(self):
        return str(self.statement)

class StatementsNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements if statements else []
    
    def __str__(self):
        return '\n'.join(str(stmt) for stmt in self.statements)

class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
    
    def __str__(self):
        result = f"if ({self.condition}) {{\n{self.if_body}\n}}"
        if self.else_body:
            result += f" else {{\n{self.else_body}\n}}"
        return result

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __str__(self):
        return f"while ({self.condition}) {{\n{self.body}\n}}"

class FunctionCallNode(ASTNode):
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args
    
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.identifier}({args_str})"

class VectorNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    
    def __str__(self):
        elements_str = ', '.join(str(elem) for elem in self.elements)
        return f"[{elements_str}]"

class StringNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __str__(self):
        return f'"{self.value}"'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0]
    
    def error(self, expected):
        token = self.current_token
        raise Exception(f"Syntax error at {token.line}:{token.column}: Expected {expected}, but got {token.token_type.name} '{token.value}'")
    
    def eat(self, token_type):
        """Consume the current token if it matches the expected type"""
        if self.current_token.token_type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(token_type.name)
    
    def program(self):
        """Program -> Statements"""
        statements = self.statements()
        return statements
    
    def statements(self):
        """Statements -> Statement Statements | ε"""
        statements = []
        
        while (self.current_token.token_type != TokenType.EOF and 
               self.current_token.token_type != TokenType.RBRACE):
            statements.append(self.statement())
        
        return StatementsNode(statements)
    
    def statement(self):
        """Statement -> Assignment | ConditionalStatement | LoopStatement | FunctionCall"""
        if self.current_token.token_type == TokenType.IDENTIFIER:
            # Look ahead to check if it's an assignment or function call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].token_type == TokenType.ASSIGN:
                return self.assignment_statement()
            else:
                return StatementNode(self.function_call())
        elif self.current_token.token_type == TokenType.IF:
            return StatementNode(self.conditional_statement())
        elif self.current_token.token_type == TokenType.WHILE:
            return StatementNode(self.loop_statement())
        else:
            self.error("statement")
    
    def assignment_statement(self):
        """Assignment -> IDENTIFIER = Expression"""
        identifier = IdentifierNode(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return AssignmentNode(identifier, expr)
    
    def conditional_statement(self):
        """ConditionalStatement -> IF ( Expression ) { Statements } [ELSE { Statements }]"""
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.condition()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        if_body = self.statements()
        self.eat(TokenType.RBRACE)
        
        else_body = None
        if self.current_token.token_type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            else_body = self.statements()
            self.eat(TokenType.RBRACE)
        
        return IfNode(condition, if_body, else_body)
    
    def loop_statement(self):
        """LoopStatement -> WHILE ( Expression ) { Statements }"""
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.condition()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        body = self.statements()
        self.eat(TokenType.RBRACE)
        return WhileNode(condition, body)
    
    def function_call(self):
        """FunctionCall -> IDENTIFIER ( [Expression [, Expression]*] )"""
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        
        args = []
        if self.current_token.token_type != TokenType.RPAREN:
            # First check if it's a vector literal starting here
            if self.current_token.token_type == TokenType.LBRACKET:
                args.append(self.vector())
            else:
                args.append(self.expression())
                
            while self.current_token.token_type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                
                # Check again if it's a vector literal
                if self.current_token.token_type == TokenType.LBRACKET:
                    args.append(self.vector())
                else:
                    args.append(self.expression())
        
        self.eat(TokenType.RPAREN)
        return FunctionCallNode(identifier, args)
    
    def expression(self):
        """Expression -> Term ((PLUS | MINUS) Term)*"""
        node = self.term()
        
        while (self.current_token.token_type in 
               (TokenType.PLUS, TokenType.MINUS)):
            token = self.current_token
            if token.token_type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            
            node = BinaryOpNode(node, token, self.term())
        
        return node
    
    def condition(self):
        """Condition -> Expression (GREATER|LESS) Expression"""
        left = self.expression()
        
        if self.current_token.token_type in (TokenType.GREATER, TokenType.LESS):
            op = self.current_token
            
            if op.token_type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
            else:
                self.eat(TokenType.LESS)
            
            right = self.expression()
            return BinaryOpNode(left, op, right)
        
        return left
    
    def term(self):
        """Term -> Factor ((MULTIPLY | DIVIDE) Factor)*"""
        node = self.factor()
        
        while (self.current_token.token_type in 
               (TokenType.MULTIPLY, TokenType.DIVIDE)):
            token = self.current_token
            if token.token_type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            else:
                self.eat(TokenType.DIVIDE)
            
            node = BinaryOpNode(node, token, self.factor())
        
        return node
    
    def factor(self):
        """Factor -> NUMBER | IDENTIFIER | ( Expression ) | -Factor | FunctionCall | Vector"""
        token = self.current_token
        
        if token.token_type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token)
        
        elif token.token_type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token)
                
        elif token.token_type == TokenType.IDENTIFIER:
            # Look ahead to check if it's a function call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].token_type == TokenType.LPAREN:
                return self.function_call()
            else:
                self.eat(TokenType.IDENTIFIER)
                return IdentifierNode(token)
        
        elif token.token_type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        
        elif token.token_type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOpNode(token, self.factor())
        
        elif token.token_type == TokenType.LBRACKET:
            return self.vector()
        
        self.error("factor")
    
    def vector(self):
        """Vector -> [ [Expression [, Expression]*] ]"""
        self.eat(TokenType.LBRACKET)
        
        elements = []
        if self.current_token.token_type != TokenType.RBRACKET:
            elements.append(self.expression())
            
            while self.current_token.token_type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                elements.append(self.expression())
        
        self.eat(TokenType.RBRACKET)
        return VectorNode(elements)
    
    def parse(self):
        """Parse the tokens and return the abstract syntax tree"""
        return self.program()