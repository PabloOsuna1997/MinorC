from enum import Enum

class Aritmetics(Enum):
    MAS     = 1
    MENOS   = 2
    POR     = 3
    DIV     = 4
    MODULO  = 5

class LogicsRelational(Enum):
    AND         = 1
    OR          = 2
    XOR         = 3
    IGUALQUE    = 4
    DIFERENTE   = 5
    MAYORIGUAL  = 6
    MENORIGUAL  = 7
    MAYORQUE    = 8
    MENORQUE    = 9

class BitToBit(Enum):
    ANDBIT  = 1
    ORBIT   = 2
    XORBIT  = 3
    SHIFTI = 4
    SHIFTD = 5

class Expretion:
     ''' this class represent an expresion'''

########--------------- declaration Section
class DeclarationExp:
    ''' this class represent an numeric expresion'''

class SingleDeclaration(DeclarationExp):
        def __init__(self, id, val, line, column):
            self.id = id
            self.val = val            
            self.line = line
            self.column = column


class Declaration_Array(DeclarationExp):
    def __init__(self, id, expresion, line, column):
            self.id = id
            self.expresion = expresion            
            self.line = line
            self.column = column

########--------------- Numeric Section
class NumericExpression:
    ''' this class represent an numeric expresion'''

class BinaryExpression(NumericExpression):
        def __init__(self, op1, op2, operator, line, column):
            self.op1 = op1
            self.op2 = op2
            self.operator = operator            
            self.line = line
            self.column = column

class Number(NumericExpression):
        def __init__(self, line, column, val=0):
            self.val = val
            self.line = line
            self.column = column
        
class Identifier(NumericExpression):
        def __init__(self, id, line, column):
            self.id = id
            self.line = line
            self.column = column

class NegativeNumber(NumericExpression):
        def __init__(self, expression, line, column):
            self.expression = expression
            self.line = line
            self.column = column

class Abs(NumericExpression):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

class IdentifierArray(NumericExpression):
    def __init__(self, id, expressions, line, column):
        self.id = id
        self.expressions = expressions
        self.line = line
        self.column = column

class SizeOf(NumericExpression):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

class Parentesis(NumericExpression):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

class AsignationArray(Expretion):
    def __init__(self, id, corchetes, expresion, line, column):
        self.expresion = expresion
        self.id = id
        self.corchetes = corchetes
        self.line = line
        self.column = column

######----------------Strings section
class StringExpression:
    '''this class represent an string expression'''

class String_(StringExpression):
    def __init__(self, string, line, column):
        self.string = string
        self.line = line
        self.column = column

######---------------- Logical Section
class LogicalExpression:
    '''this class represent an logical expresions'''

class LogicAndRelational(LogicalExpression):
    def __init__(self, op1, op2, operator, line , column):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator
        self.line = line
        self.column = column

class Not(LogicalExpression):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column



######----------------- bit-bit section
class Empty:
    ''' aslas '''
class empty(Empty):
    
    def __init__(self, val = ''):
        self.val = val

class BitBit:
    '''this class represent an bit to bit expressions'''

class NotBit(BitBit):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

class ReferenceBit(BitBit):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

class RelationalBit(BitBit):
    def __init__(self, op1, op2, operator, line, column):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator
        self.line = line
        self.column = column


###----------------------cast section
class Cast:
    'this class represent the diferents types of the cast'

class Cast_(Cast):
    def __init__(self, expression, type, line, column):
        self.expression = expression
        self.type = type
        self.line = line
        self.column = column


###------------------------read setcion
class Read:
    'this class represent the read to console'

class ReadConsole(Read):
    def __init__(self, line, column, read = 1):
        self.read = read
        self.line = line
        self.column = column

class Scanf(Read):
     def __init__(self, line, column, scan = 1):
        self.scan = scan
        self.line = line
        self.column = column



###-------------------------array section
class Array:
    'this class represent arrays'

class ExpressionsDeclarationArray(Array):
    def __init__(self, expressionIzq, expressionDer, line, column):
        self.expressionIzq = expressionIzq
        self.expressionDer = expressionDer
        self.line = line
        self.column = column

class InitializationArray(Expretion):
    def __init__(self, line, column, val = []):
        self.val = val
        self.line = line
        self.column = column

class DeclarationArrayInit(Expretion):
    def __init__(self, id, dimentions, val, line, column):
        self.id = id
        self.dimentions = dimentions
        self.val = val
        self.line = line
        self.column = column

class Param(Expretion):
    def __init__(self, type_, id, line, column):
        self.id = id
        self.type_ = type_
        self.line = line
        self.column = column


##----------------------------struct sections
class Struct:
    'this class represent an structs'

class DeclarationStruct(Struct):
    def __init__(self, id, atributos, line, column):
        self.id = id
        self.atributos = atributos
        self.line = line
        self.column = column

class puntoSimple():
    def __init__(self, id, line, column):
        self.id = id
        self.line = line
        self.column = column

class puntoArreglo():
    def __init__(self, id, expresion, line, column):
        self.id = id
        self.expresion = expresion
        self.line = line
        self.column = column