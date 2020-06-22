# ---------------------
# @Autor
# Juan Pablo Osuna de Leon 
# 201503911
#----------------------

reservadas = {
    'int': 'INT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'printf': 'PRINTF',
    'struct': 'STRUCT',
    'break': 'BREAK',
    'case': 'CASE',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'goto': 'GOTO',
    'return': 'RETURN',
    'sizeof': 'SIZEOF',
    'switch': 'SWITCH',
    'void': 'VOID',
    'scanf': 'SCANF',
    'malloc': 'MALLOC'
}

tokens = [
    'INCREMENTO',
    'DECREMENTO',
    'PUNTO',
    'FLECHA',
    'UNARIO',
    'COMA',
    'PUNTOCOMA',
    'DOSPUNTOS',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'NOTBIT',
    'ANDBIT',
    'ORBIT',
    'XORBIT',
    'SHIFTIZQ',
    'SHIFTDER',
    'NOTLOGICA',
    'MENOS',
    'MAS',
    'POR',
    'DIV',
    'MODULO',
    'AND',
    'OR',
    'IGUAL',
    'IGUALQUE',
    'DIFERENTE',
    'MAYORIGUAL',
    'MENORIGUAL',
    'MAYORQUE',
    'MENORQUE',
    'NUMERO',
    'ID',
    'CADENA',
    'CHAR_'
] + list(reservadas.values())

# er tokens
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'\-\-'
t_PUNTO     = r'\.'
t_FLECHA    = r'\-\>'
t_UNARIO    = r'\?'
t_COMA      = r'\,'
t_PUNTOCOMA  = r'\;'
t_DOSPUNTOS = r'\:'
t_LLAVEIZQ  = r'\{'
t_LLAVEDER  = r'\}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_NOTBIT    = r'\~'
t_ANDBIT    = r'\&'
t_ORBIT     = r'\|'
t_XORBIT    = r'\^'
t_SHIFTIZQ  = r'\<\<'
t_SHIFTDER  = r'\>\>'
t_NOTLOGICA = r'\!'
t_MENOS     = r'\-'
t_MAS       = r'\+'
t_POR       = r'\*'
t_DIV       = r'\/'
t_MODULO    = r'\%'
t_AND       = r'\&\&'
t_OR        = r'\|\|'
t_IGUAL     = r'\='
t_IGUALQUE  = r'\=\='
t_DIFERENTE = r'\!\='
t_MAYORIGUAL= r'\>\='
t_MENORIGUAL= r'\<\='
t_MAYORQUE  = r'\>'
t_MENORQUE  = r'\<'

import generator as g
import ply.lex as lex
import ply.yacc as yacc

from expressions import *
from instructions import *
from lexicalObject import *
from sintacticObject import *

grammarList = []
grammarList[:] = []
sintacticErroList = []
sintacticErroList[:] = []
LexicalErrosList = []
LexicalErrosList[:] =[]
aux = []
input_ = ''

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    try:
        x = t.value.split(".")
        if len(x) > 1:
            t.value = float(t.value)
        else: 
            t.value = int(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    #print(str(t.value))
    t.type = reservadas.get(t.value.lower(),'ID')
    return t

def t_CHAR_(t):
    r'\'[a-zA-Z_]\''
    print("char: " + str(t.value))
    t.value = t.value[1:-1]
    return t

def t_CADENA(t):
    r'(\'.+?\') | (\".+?\")'
    t.value = t.value[1:-1]
    return t

def t_COMENTARIO(t):
    r'\/\/.*\n'
    t.lexer.lineno += 1

#ignored characters 
t_ignore = " \t"

def t_newline(t):
    r'\n+' 
    t.lexer.lineno += t.value.count("\n")

# method for obtention the column
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
    
def t_error(t):
    global input_,LexicalErrosList
    lo = lexOb(t.value[0],find_column(input_,t),t.lexer.lineno)
    LexicalErrosList.append(lo)
    print("Illegal character '%s'" % t.value[0]+", linea: "+str(t.lexer.lineno))
    t.lexer.skip(1)


##---------------------------ANALISIS SINTACTICO------------------------
precedence = (
    
    #('right','UMENOS'),
    #('left', 'UNARIO'),    
    #('left','POR','DIV'),
    #('left', 'MODULO'),
    #('left','MAS','MENOS'),
    #('left', 'SHIFTIZQ', 'SHIFTDER'),
    #('left', 'AND'),
    #('left', 'OR'),
    #('left', 'NOTLOGICA'),
    #('left', 'ANDBIT'),
    #('left', 'ORBIT'),
    #('left', 'XORBIT'),
    #('right','NOTBIT'),
    #('left', 'INCREMENTO', 'DECREMENTO')

    
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'ORBIT'),
    ('left', 'XORBIT'),
    ('left', 'ANDBIT'),
    ('nonassoc', 'DIFERENTE','IGUALQUE'),
    ('nonassoc', 'MENORQUE','MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'SHIFTIZQ', 'SHIFTDER'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MODULO'),
    ('right', 'NOTLOGICA'),
    ('right', 'NOTBIT'),
    ('right', 'UMENOS'),
    ('right', 'UNARIO'),
    ('right', 'INT', 'FLOAT', 'CHAR'),
    ('left', 'PARIZQ'),
    ('left', 'CORIZQ')
)

#definition of grammar 
def p_init(t):
    'S : A'
    print("Se ha reconocido la cadena.")

def p_instruccionesGlobal(t):
    'A  :    INSTRUCCIONES_GLOBALES'

def p_listaInstrucciones(t):
    '''INSTRUCCIONES_GLOBALES : INSTRUCCIONES_GLOBALES DECLARACION_GLOBAL
                                | DECLARACION_GLOBAL'''

def p_declaracionGlobal(t):
    '''DECLARACION_GLOBAL :     DECLA_VARIABLES'''

def p_declaVariable(t):
    'DECLA_VARIABLES :  TIPO LISTA_ID PUNTOCOMA'

def p_tipo(t):
    '''TIPO :   INT
                | FLOAT
                | DOUBLE
                | VOID
                | CHAR
                | STRUCT '''

def p_listaId(t):
    '''LISTA_ID :   LISTA_ID COMA ASIGNA
                    | ASIGNA'''

def p_asigna(t):
    '''ASIGNA :     ID IGUAL EXPRESION
                    | ID CORCHETES
                    | ID CORCHETES IGUAL EXPRESION
                    | ID'''
   
def p_corchetes(t):
    '''CORCHETES :  CORCHETES CORCHETE
                    | CORCHETE '''

def p_corchete(t):
    'CORCHETE :     CORIZQ VALOR CORDER'

def p_valor(t):
    'VALOR :        EXPRESION'

def p_valorEmpty(t):
    'VALOR : '

def p_expresion(t):
    '''EXPRESION :  LOG'''
 
def p_log(t):
    '''LOG :    LOG OR LOG
                | LOG AND LOG
                | REL
                    '''

def p_rel(t):
    '''REL :    ARIT MAYORQUE ARIT
                | ARIT MENORQUE ARIT
                | ARIT MAYORIGUAL ARIT
                | ARIT MENORIGUAL ARIT
                | ARIT IGUALQUE ARIT
                | ARIT DIFERENTE ARIT
                | ARIT
    '''
def p_arit(t):
    '''ARIT :   ARIT POR ARIT
                | ARIT MAS ARIT
                | ARIT DIV ARIT
                | ARIT MENOS ARIT
                | PARIZQ EXPRESION PARDER
                | NUMERO
                | MENOS ARIT %prec UMENOS
                | ID                
                | NOTLOGICA LOG
                | CADENA
                | CHAR
    '''

def p_error(t):
    print("Error sintactico en '%s'" % t.value + "line: "+ str(t.lineno))
    global sintacticErroList
    so = sinOb(t.value, t.lineno, find_column(input_, t))
    sintacticErroList.append(so)


#def parse(input):
#global input_, sintacticErroList, LexicalErrosList

#sintacticErroList[:] = []
#LexicalErrosList[:] =[]

#input_ = input    
lexer = lex.lex()
parser = yacc.yacc()
#instructions = parser.parse(input)
#lexer.lineno = 1
#parser.restart()
#if len(LexicalErrosList) > 0 or len(sintacticErroList) > 0:
    #if instructions == None:
        #instructions = []
    #else:
        #instructions[:] = []
    #return instructions
#return instructions

f = open("./entrada.txt", "r")
input = f.read()
parser.parse(input)