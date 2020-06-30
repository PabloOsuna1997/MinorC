class Instruction:
    '''this is an abstractab class'''

class PrintF_(Instruction) :
    '''print statment, recieve a string'''
    
    def __init__(self, expressions, line, column):
         self.expressions = expressions
         self.line = line
         self.column = column

class Declaration(Instruction):
    '''variables declarations'''

    def __init__(self, type_, line, column, listId = []):
        self.type_ = type_
        self.listId = listId
        self.line = line
        self.column = column

class FunctionDeclaration(Instruction):
    '''functions declarations'''

    def __init__(self, type_, id, params, instructions, line, column):
        self.type_ = type_
        self.id = id
        self.params = params
        self.instructions = instructions
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
    '''if statment'''
    def __init__(self, condition, instructions, ifElse, line, column):
        self.instructions = instructions
        self.condition = condition
        self.ifElse = ifElse
        self.line = line
        self.column = column

class IfElse(Instruction):
    '''else if statment'''
    def __init__(self,condition, instructions, line, column):
        self.condition = condition
        self.instructions = instructions
        self.line = line
        self.column = column

class Else(Instruction):
    '''else statment'''
    def __init__(self,instructions, line, column):
        self.instructions = instructions
        self.line = line
        self.column = column

class Switch_(Instruction):
    '''switch statment'''
    def __init__(self,expresion, listaCases, default, line, column):
        self.expresion = expresion
        self.listaCases = listaCases
        self.default = default
        self.line = line
        self.column = column

class Case_(Instruction):
    '''cases statment'''
    def __init__(self,expresion, instructions, break_, line, column):
        self.expresion = expresion
        self.instructions = instructions
        self.break_ = break_
        self.line = line
        self.column = column

class Default_(Instruction):
    '''default statment'''
    def __init__(self,instructions, break_, line, column):
        self.instructions = instructions
        self.break_ = break_
        self.line = line
        self.column = column

class CallFunction(Instruction):
    '''call function statment'''
    def __init__(self,id, params, line, column):
        self.id = id
        self.params = params
        self.line = line
        self.column = column

class For(Instruction):
    '''for statment'''
    def __init__(self,declaration,condition,increDecre,instructions, line, column):
        self.declaration = declaration
        self.condition = condition
        self.increDecre = increDecre
        self.instructions = instructions
        self.line = line
        self.column = column

class While_(Instruction):
    '''while statment'''
    def __init__(self,condition,instructions, line, column):
        self.condition = condition
        self.instructions = instructions
        self.line = line
        self.column = column

class DoWhile_(Instruction):
    '''do while statment'''
    def __init__(self,instructions,condition, line, column):
        self.condition = condition
        self.instructions = instructions
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

class IncreDecre_Pre(Instruction):
    'increment or decrement'
    def __init__(self, signo, id, line, column):
        self.signo = signo
        self.id = id
        self.line = line
        self.column = column

class IncreDecre_Post(Instruction):
    'increment or decrement'
    def __init__(self, signo, id, line, column):
        self.signo = signo
        self.id = id
        self.line = line
        self.column = column

class Asignation(Instruction):
    'asignation'
    def __init__(self, id, op, expresion, line, column):
        self.id = id
        self.op = op
        self.expresion = expresion
        self.line = line
        self.column = column

class DeclaStructIntr(Instruction):
    def __init__(self, type_, id, line, column):
        self.id = id
        self.type_ = type_
        self.line = line
        self.column = column

class AsignationStructExpre(Instruction):
    def __init__(self, expresionIzq, punto, expresion, line, column):
        self.id = id
        self.expresionIzq = expresionIzq
        self.punto = punto
        self.expresion = expresion
        self.line = line
        self.column = column



