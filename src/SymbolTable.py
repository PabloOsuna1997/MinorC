from enum import Enum

class TypeData(Enum):
    INT = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    ARRAY = 5
    FUNCION = 6
    PROCEDIMIENTO = 7
    CONTROL = 8

class Symbol() :
    'this class represent a symbol in our symbol table'
    def __init__(self, id, tipo, valor = {}, declarada = 'main', parametros = [], dimension = 0, referencia = 0) :
        self.id = id
        self.tipo = tipo
        self.valor = valor        
        self.declarada = declarada
        self.dimension = dimension
        self.referencia = referencia
        self.parametros = parametros

class SymbolTable() :
    'this class represent our symbol table'
    def __init__(self, symbols = {}):
        self.symbols = symbols
        self.symbols.clear();

    def add(self, symbol):
        self.symbols[symbol.id] = symbol
    
    def get(self, id):
        if not id in self.symbols:
            print("Error: variable "+ id + " not defiened." )
        return self.symbols[id]

    def exist(self, id):
        if id in self.symbols:
            return 1
        return 0
    
    def update(self, symbol):
        if not symbol.id in self.symbols:
            print("Error: variable "+ symbol.id + " not defiened." )
        else:
            self.symbols[symbol.id] = symbol
    
    def updateFunction(self, id, type_):
        if not id in self.symbols:
            print("Error: function "+ id + " not defiened." )
        else:
            self.symbols[id].tipo = type_

    def updateReference(self, id, val):
        if not id in self.symbols:
            print("Error: variable "+ id + " not defiened." )
        else:
            self.symbols[id].valor = val

    def delete(self, id):
        if id in self.symbols:
            del self.symbols[id]
            return 1            
        print(f"{id} not defiened.")
        return 0


class SymbolTableDebug():
    'this class represent our symbol table'

    def __init__(self, symbols={}):
        self.symbols = symbols
        #self.symbols.clear();

    def add(self, symbol):
        self.symbols[symbol.id] = symbol

    def get(self, id):
        if not id in self.symbols:
            print("Error: variable " + id + " not defiened.")
        return self.symbols[id]

    def exist(self, id):
        if id in self.symbols:
            return 1
        return 0

    def update(self, symbol):
        if not symbol.id in self.symbols:
            print("Error: variable " + symbol.id + " not defiened.")
        else:
            self.symbols[symbol.id] = symbol

    def updateFunction(self, id, type_):
        if not id in self.symbols:
            print("Error: function " + id + " not defiened.")
        else:
            self.symbols[id].tipo = type_

    def updateReference(self, id, val):
        if not id in self.symbols:
            print("Error: variable " + id + " not defiened.")
        else:
            self.symbols[id].valor = val

    def delete(self, id):
        if id in self.symbols:
            del self.symbols[id]
            return 1
        print(f"{id} not defiened.")
        return 0

    def clearTable (self):
        self.symbols.clear()