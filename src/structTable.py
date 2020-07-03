from enum import Enum

class d(Enum):
    INT = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    ARRAY = 5
    FUNCION = 6
    PROCEDIMIENTO = 7
    CONTROL = 8

class Symbol() :
    'this class represent a struct in our function table'
    def __init__(self, id, tipo, atributos = []) :
        self.id = id
        self.tipo = tipo
        self.atributos = atributos

class structTable() :
    'this class represent our symbol table'
    def __init__(self, symbols = {}):
        self.symbols = symbols
        self.symbols.clear();

    def add(self, symbol):
        self.symbols[symbol.id] = symbol
    
    def get(self, id):
        if not id in self.symbols:
            print("Error: struct "+ id + " not defiened." )
        return self.symbols[id]

    def exist(self, id):
        if id in self.symbols:
            return 1
        return 0
    
    def update(self, symbol):
        if not symbol.id in self.symbols:
            print("Error: struct "+ symbol.id + " not defiened." )
        else:
            self.symbols[symbol.id] = symbol
    
    def updateFunction(self, id, type_):
        if not id in self.symbols:
            print("Error: struct "+ id + " not defiened." )
        else:
            self.symbols[id].tipo = type_


    def delete(self, id):
        if id in self.symbols:
            del self.symbols[id]
            return 1            
        print(f"{id} not defiened.")
        return 0

