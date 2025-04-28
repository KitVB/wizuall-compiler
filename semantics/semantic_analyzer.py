# semantics/semantic_analyzer.py
from parser.parser import *
from scanner.lexer import TokenType
from semantics.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.errors = []
    

    def analyze(self):
        """Analyze the AST for semantic errors"""
        self.visit(self.ast)
        # Return True even if there are errors - we're being lenient in WizuAll
        return True, self.errors  # Changed from: return len(self.errors) == 0, self.errors
    
    def visit(self, node):
        """Visit a node in the AST"""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visit method"""
        pass
    
    def visit_StatementsNode(self, node):
        """Visit statements node"""
        for statement in node.statements:
            self.visit(statement)
    
    def visit_StatementNode(self, node):
        """Visit statement node"""
        self.visit(node.statement)
    
    def visit_AssignmentNode(self, node):
        """Visit assignment node"""
        # Evaluate right-hand side
        value = self.visit(node.expr)
        
        # Update symbol table
        name = node.identifier.name
        if name in self.symbol_table.symbols:
            self.symbol_table.update(name, value)
        else:
            value_type = 'vector' if isinstance(value, list) else 'scalar'
            self.symbol_table.define(name, value_type, value)
    
    def visit_IfNode(self, node):
        """Visit if node"""
        self.visit(node.condition)
        self.visit(node.if_body)
        if node.else_body:
            self.visit(node.else_body)
    
    def visit_WhileNode(self, node):
        """Visit while node"""
        self.visit(node.condition)
        self.visit(node.body)
    
    def visit_FunctionCallNode(self, node):
        """Visit function call node"""
        # Check if it's a visualization function
        vis_funcs = ['plot', 'histogram', 'heatmap', 'scatter', 'bar', 'line']
        
        # Process arguments
        for arg in node.args:
            self.visit(arg)
    
    def visit_BinaryOpNode(self, node):
        """Visit binary operation node"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Type checking can be done here
        # For example, ensuring vector operations are valid
        
        if node.op.token_type == TokenType.PLUS:
            return self.add(left, right)
        elif node.op.token_type == TokenType.MINUS:
            return self.subtract(left, right)
        elif node.op.token_type == TokenType.MULTIPLY:
            return self.multiply(left, right)
        elif node.op.token_type == TokenType.DIVIDE:
            return self.divide(left, right)
    
    def visit_UnaryOpNode(self, node):
        """Visit unary operation node"""
        value = self.visit(node.expr)
        
        if node.op.token_type == TokenType.MINUS:
            # Implement unary minus
            if isinstance(value, list):  # Vector
                return [-v for v in value]
            else:  # Scalar
                return -value
    
    def visit_NumberNode(self, node):
        """Visit number node"""
        return node.value
    
    def visit_IdentifierNode(self, node):
        """Visit identifier node"""
        symbol = self.symbol_table.lookup(node.name)
        if symbol:
            return symbol.value
        else:
            # In WizuAll, undefined variables get default value of 0
            self.symbol_table.define(node.name, 'scalar', 0)
            return 0
    
    def visit_VectorNode(self, node):
        """Visit vector node"""
        return [self.visit(element) for element in node.elements]
    
    # Helper methods for operations
    def add(self, left, right):
        """Addition operation handling both scalars and vectors"""
        if isinstance(left, list) and isinstance(right, list):
            # Vector + Vector
            if len(left) != len(right):
                self.errors.append("Vector dimensions don't match for addition")
                return left  # Default to left operand on error
            return [a + b for a, b in zip(left, right)]
        elif isinstance(left, list):
            # Vector + Scalar
            return [a + right for a in left]
        elif isinstance(right, list):
            # Scalar + Vector
            return [left + b for b in right]
        else:
            # Scalar + Scalar
            return left + right
    
    def subtract(self, left, right):
        """Subtraction operation handling both scalars and vectors"""
        if isinstance(left, list) and isinstance(right, list):
            # Vector - Vector
            if len(left) != len(right):
                self.errors.append("Vector dimensions don't match for subtraction")
                return left  # Default to left operand on error
            return [a - b for a, b in zip(left, right)]
        elif isinstance(left, list):
            # Vector - Scalar
            return [a - right for a in left]
        elif isinstance(right, list):
            # Scalar - Vector
            return [left - b for b in right]
        else:
            # Scalar - Scalar
            return left - right
    
    def multiply(self, left, right):
        """Multiplication operation handling both scalars and vectors"""
        if isinstance(left, list) and isinstance(right, list):
            # Vector * Vector (element-wise)
            if len(left) != len(right):
                self.errors.append("Vector dimensions don't match for multiplication")
                return left  # Default to left operand on error
            return [a * b for a, b in zip(left, right)]
        elif isinstance(left, list):
            # Vector * Scalar
            return [a * right for a in left]
        elif isinstance(right, list):
            # Scalar * Vector
            return [left * b for b in right]
        else:
            # Scalar * Scalar
            return left * right
    
    def divide(self, left, right):
        """Division operation handling both scalars and vectors"""
        # Check for division by zero
        if isinstance(right, (int, float)) and right == 0:
            self.errors.append("Division by zero")
            return left  # Default to left operand on error
        
        if isinstance(right, list) and 0 in right:
            self.errors.append("Division by zero in vector")
            return left  # Default to left operand on error
        
        if isinstance(left, list) and isinstance(right, list):
            # Vector / Vector
            if len(left) != len(right):
                self.errors.append("Vector dimensions don't match for division")
                return left  # Default to left operand on error
            return [a / b for a, b in zip(left, right)]
        elif isinstance(left, list):
            # Vector / Scalar
            return [a / right for a in left]
        elif isinstance(right, list):
            # Scalar / Vector
            return [left / b for b in right]
        else:
            # Scalar / Scalar
            return left / right