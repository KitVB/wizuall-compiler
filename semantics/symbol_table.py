# semantics/symbol_table.py
class Symbol:
    def __init__(self, name, type=None, value=None):
        self.name = name
        self.type = type  # 'scalar' or 'vector'
        self.value = value

class SymbolTable:
    def __init__(self):
        self.symbols = {}
    
    def define(self, name, type=None, value=None):
        """Add a symbol to the table"""
        self.symbols[name] = Symbol(name, type, value)
    
    def lookup(self, name):
        """Look up a symbol by name"""
        return self.symbols.get(name)
    
    def update(self, name, value):
        """Update a symbol's value"""
        if name in self.symbols:
            self.symbols[name].value = value
        else:
            # In WizuAll, undefined symbols get default value of 0
            self.define(name, 'scalar', 0)