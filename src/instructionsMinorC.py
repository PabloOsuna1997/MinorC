class Instruction:
    '''this is an abstractab class'''

class Print_(Instruction) :
    '''print statment, recieve a string'''
    
    def __init__(self, cadena, line, column):
         self.cadena = cadena
         self.line = line
         self.column = column

class Declaration(Instruction):
    '''variables declarations'''

    def __init__(self, type_, line, column, listId = []):
        self.type_ = type_
        self.listId = listId
        self.line = line
        self.column = column

class Unset(Instruction):
    '''variables destruction'''

    def __init__(self, id, line, column):
        self.id = id
        self.line = line
        self.column = column

class Exit(Instruction):
    def __init__(self, exit = 1):
        self.exit = exit

class If(Instruction):
    '''if statment, recieve a label for jump'''
    def __init__(self, expression, label, line, column):
        self.label = label
        self.expression = expression
        self.line = line
        self.column = column

class Goto(Instruction):
    '''label jump'''

    def __init__(self, label):
        self.label = label

class Label(Instruction):
    'destination label '
    def __init__(self, label, line, column):
        self.label = label
        self.line = line
        self.column = column

class DeclacionFunction(Instruction):
    'function'
    def __init__(self, type_, id, params, ret, line, column):
        self.type_ = type_
        self.id = id
        self.params = params
        self.ret = ret
        self.line = line
        self.column = column