# semantics/code_generator.py
from parser.parser import *
from semantics.symbol_table import SymbolTable
from visual_primitives.viz_functions import VisualizationPrimitives

class CodeGenerator:
    def __init__(self, ast, target_language='python'):
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.target_language = target_language
        self.viz_primitives = VisualizationPrimitives(target_language)
        self.code = []
        self.indentation = 0
        
        # Setup standard headers based on target language
        self.headers = {
            'python': [
                "import numpy as np",
                "import matplotlib.pyplot as plt",
                ""
            ],
            'c': [
                "#include <stdio.h>",
                "#include <stdlib.h>",
                "#include <math.h>",
                ""
            ],
            'r': [
                "# WizuAll generated R code",
                "library(ggplot2)",
                ""
            ]
        }
    
    def generate(self):
        """Generate target code from AST"""
        # Add headers
        self.code.extend(self.headers.get(self.target_language, []))
        
        # Generate code
        self.visit(self.ast)
        
        # Return complete code as string
        return '\n'.join(self.code)
    
    def indent(self):
        """Increase indentation level"""
        self.indentation += 4
    
    def dedent(self):
        """Decrease indentation level"""
        self.indentation = max(0, self.indentation - 4)
    
    def add_line(self, line):
        """Add a line of code with proper indentation"""
        self.code.append(' ' * self.indentation + line)
    
    def visit(self, node):
        """Visit a node in the AST"""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visit method"""
        return None
    
    def visit_StatementsNode(self, node):
        """Visit statements node"""
        for statement in node.statements:
            self.visit(statement)
        
        return None
    
    def visit_StatementNode(self, node):
        """Visit statement node"""
        return self.visit(node.statement)
    
    def visit_AssignmentNode(self, node):
        """Visit assignment node"""
        if self.target_language == 'python':
            var_name = node.identifier.name
            expr = self.visit(node.expr)
            self.add_line(f"{var_name} = {expr}")
        elif self.target_language == 'c':
            var_name = node.identifier.name
            expr = self.visit(node.expr)
            
            # Check if it's an array or scalar
            symbol = self.symbol_table.lookup(var_name)
            if symbol and symbol.type == 'vector':
                # It's a vector assignment
                # For simplicity, we just assume the vector is already defined
                self.add_line(f"// Vector assignment for {var_name}")
                self.add_line(f"// This needs to be expanded based on vector type")
            else:
                # Scalar assignment
                self.add_line(f"double {var_name} = {expr};")
        elif self.target_language == 'r':
            var_name = node.identifier.name
            expr = self.visit(node.expr)
            self.add_line(f"{var_name} <- {expr}")
        
        return None
    
    def visit_IfNode(self, node):
        """Visit if node"""
        condition = self.visit(node.condition)
        
        if self.target_language == 'python':
            self.add_line(f"if {condition}:")
            self.indent()
            self.visit(node.if_body)
            self.dedent()
            
            if node.else_body:
                self.add_line("else:")
                self.indent()
                self.visit(node.else_body)
                self.dedent()
        elif self.target_language == 'c':
            self.add_line(f"if ({condition}) {{")
            self.indent()
            self.visit(node.if_body)
            self.dedent()
            self.add_line("}")
            
            if node.else_body:
                self.add_line("else {")
                self.indent()
                self.visit(node.else_body)
                self.dedent()
                self.add_line("}")
        elif self.target_language == 'r':
            self.add_line(f"if ({condition}) {{")
            self.indent()
            self.visit(node.if_body)
            self.dedent()
            self.add_line("}")
            
            if node.else_body:
                self.add_line("else {")
                self.indent()
                self.visit(node.else_body)
                self.dedent()
                self.add_line("}")
        
        return None
    
    def visit_StringNode(self, node):
        """Visit string node"""
        return f'"{node.value}"'
    
    def visit_WhileNode(self, node):
        """Visit while node"""
        condition = self.visit(node.condition)
        
        if self.target_language == 'python':
            self.add_line(f"while {condition}:")
            self.indent()
            self.visit(node.body)
            self.dedent()
        elif self.target_language == 'c':
            self.add_line(f"while ({condition}) {{")
            self.indent()
            self.visit(node.body)
            self.dedent()
            self.add_line("}")
        elif self.target_language == 'r':
            self.add_line(f"while ({condition}) {{")
            self.indent()
            self.visit(node.body)
            self.dedent()
            self.add_line("}")
        
        return None
    
    def visit_FunctionCallNode(self, node):
        """Visit function call node"""
        function_name = node.identifier
        args = [self.visit(arg) for arg in node.args]
        
        # Check if it's a visualization function
        viz_functions = [
            'plot', 'histogram', 'heatmap', 'scatter', 'bar', 'line',
            'vec_average', 'vec_max', 'vec_min', 'vec_reverse',
            'vec_product', 'vec_compare', 'clustering', 'classification'
        ]
        
        if function_name in viz_functions:
            # Generate visualization code
            viz_code = self.viz_primitives.generate_code(function_name, args)
            # Add the visualization code directly
            for line in viz_code.split('\n'):
                if line.strip():  # Skip empty lines
                    self.add_line(line)
            return None
        
        # Regular function call
        args_str = ', '.join(args)
        if self.target_language == 'python':
            return f"{function_name}({args_str})"
        elif self.target_language == 'c':
            return f"{function_name}({args_str})"
        elif self.target_language == 'r':
            return f"{function_name}({args_str})"
    
    def visit_BinaryOpNode(self, node):
        """Visit binary operation node"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op.token_type == TokenType.PLUS:
            return f"({left} + {right})"
        elif node.op.token_type == TokenType.MINUS:
            return f"({left} - {right})"
        elif node.op.token_type == TokenType.MULTIPLY:
            return f"({left} * {right})"
        elif node.op.token_type == TokenType.DIVIDE:
            return f"({left} / {right})"
        elif node.op.token_type == TokenType.GREATER:
            return f"({left} > {right})"
        elif node.op.token_type == TokenType.LESS:
            return f"({left} < {right})"
        else:
            return f"({left} {node.op.value} {right})"  # Generic fallback"
    
    def visit_UnaryOpNode(self, node):
        """Visit unary operation node"""
        expr = self.visit(node.expr)
        
        if node.op.token_type == TokenType.MINUS:
            return f"(-{expr})"
    
    def visit_NumberNode(self, node):
        """Visit number node"""
        return str(node.value)
    
    def visit_IdentifierNode(self, node):
        """Visit identifier node"""
        return node.name
    
    def visit_VectorNode(self, node):
        """Visit vector node"""
        elements = [self.visit(element) for element in node.elements]
        elements_str = ', '.join(elements)
        
        if self.target_language == 'python':
            return f"np.array([{elements_str}])"
        elif self.target_language == 'c':
            # For C, we'd need to handle array allocation properly
            # This is just a placeholder
            return f"/* Array: {elements_str} */"
        elif self.target_language == 'r':
            return f"c({elements_str})"