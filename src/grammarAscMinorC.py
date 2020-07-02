# ---------------------
# @Autor
# Juan Pablo Osuna de Leon 
# 201503911
#----------------------

reservadas = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
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
    'C_INT',
    'C_CHAR',
    'C_FLOAT',
    'MASIGUAL',
    'MENOSIGUAL',
    'PORIGUAL',
    'DIVIGUAL',
    'MODIGUAL',
    'SIIGUAL',
    'SDIGUAL',
    'ANDIGUAL',
    'XORIGUAL',
    'ORIGUAL',
    'INCREMENTO',
    'DECREMENTO',
    'PUNTO',
    'FLECHA',
    'TERNARIO',
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
t_C_INT       = r'\(int\)'
t_C_CHAR      = r'\(char\)'
t_C_FLOAT      = r'\(float\)'
t_MASIGUAL = r'\+\='
t_MENOSIGUAL = r'\-\='
t_PORIGUAL  = r'\*\='
t_DIVIGUAL  = r'\/\='
t_MODIGUAL  = r'\%\='
t_SIIGUAL   = r'\<\<\='
t_SDIGUAL   = r'\>\>\='
t_ANDIGUAL  = r'\&\='
t_XORIGUAL  = r'\^\='
t_ORIGUAL   = r'\|\='
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'\-\-'
t_PUNTO     = r'\.'
t_FLECHA    = r'\-\>'
t_TERNARIO   = r'\?'
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

from expresionsMinorC import *
from instructionsMinorC import *
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
    ('left', 'COMA'),
    ('right','IGUAL','MASIGUAL','MENOSIGUAL','PORIGUAL','DIVIGUAL','MODIGUAL','SIIGUAL','SDIGUAL','ANDIGUAL','XORIGUAL','ORIGUAL'),
    ('right', 'TERNARIO'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'ORBIT'),
    ('left', 'XORBIT'),
    ('left', 'ANDBIT'),
    ('left', 'DIFERENTE','IGUALQUE'),
    ('left', 'MENORQUE','MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'SHIFTIZQ', 'SHIFTDER'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MODULO'),
    ('right', 'C_INT', 'C_FLOAT', 'C_CHAR', 'INCREMENTO', 'DECREMENTO', 'UMENOS','UANDBIT', 'NOTLOGICA', 'NOTBIT'),
    ('left', 'PARIZQ', 'CORIZQ') 
)

#definition of grammar 
def p_init(t):
    'S : A'
    t[0] = t[1]
    print("Se ha reconocido la cadena.")
    global grammarList
    grammarList.append(g.nodeGramatical('S  -> A', f'S.val = A.val'))
    grammarList.reverse()

def p_instruccionesGlobal(t):
    'A  :    INSTRUCCIONES_GLOBALES'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('A  -> INSTRUCCIONES_GLOBALES', f'A.val = INSTRUCCIONES_GLOBALES.val'))

def p_listaInstrucciones(t):
    '''INSTRUCCIONES_GLOBALES : INSTRUCCIONES_GLOBALES DECLARACION_GLOBAL
                                | DECLARACION_GLOBAL'''
    
    global grammarList
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('INSTRUCCIONES_GLOBALES  -> INSTRUCCIONES_GLOBALES DECLARACION_GLOBAL', f'INSTRUCCIONES_GLOBALES_1.val.append(DECLARACION_GLOBAL) \n INSTRUCCIONES_GLOBALES.val = INSTRUCCIONES_GLOBALES_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('INSTRUCCIONES_GLOBALES  -> DECLARACION_GLOBAL', f'INSTRUCCIONES_GLOBALES.val = = DECLARACION_GLOBAL.val'))

def p_declaracionGlobal(t):
    '''DECLARACION_GLOBAL :     DECLA_VARIABLES
                                | DECLA_FUNCIONES
                                | DECLA_STRUCTS'''

    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('DECLARACION_GLOBAL  -> DECLA_VARIABLES \n |DECLA_FUNCIONES \n |DECLA_STRUCTS', f'DECLARACION_GLOBAL.val = = t[1].val'))

##----------------------------------DECLARACION DE VARIABLES ------------------
def p_declaVariable_error(t):
    'DECLA_VARIABLES :  TIPO error PUNTOCOMA'
def p_declaVariable(t):
    'DECLA_VARIABLES :  TIPO LISTA_ID PUNTOCOMA'
    #print(f'tipo: {str(t[1])} valor: {str(t[2])}')
    t[0] = Declaration(t[1], t.lineno(1), t.lexpos(1), t[2])
    global grammarList
    grammarList.append(g.nodeGramatical('DECLA_VARIABLES  ->TIPO LISTA_ID PUNTOCOMA', f'DECLA_VARIABLES.val = Declaration(t[1], t.lineno(1), t.lexpos(1), t[2])'))

def p_tipo(t):
    '''TIPO :   INT
                | FLOAT
                | DOUBLE
                | VOID
                | CHAR '''
                #| STRUCT  -> quite el tipo struct 
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('TIPO  ->INT \n | FLOAT \n | DOUBLE \n | VOID \n | CHAR', f'TIPO.val = t[1]'))

def p_listaId_error(t):
    'LISTA_ID :   LISTA_ID error ASIGNA'
def p_listaId(t):
    '''LISTA_ID :   LISTA_ID COMA ASIGNA
                    | ASIGNA'''
   
    global grammarList
    if len(t) == 2:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('LISTA_ID  -> ASIGNA', f'LISTA_ID.val = ASIGNA.val'))
    else: 
        t[1].append(t[3])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('LISTA_ID  -> LISTA_ID COMA ASIGNA ', f' LISTA_ID_1.val.append(ASIGNA.val) \n LISTA_ID.val = LISTA_ID_1.val'))

def p_asigna_error(t):
    'ASIGNA :     ID error EXPRESION'
def p_asigna(t):
    '''ASIGNA :     ID IGUAL EXPRESION
                    | ID CORCHETES
                    | ID CORCHETES IGUAL EXPRESION
                    | ID'''
    global grammarList
    if len(t) == 4: 
        t[0] = SingleDeclaration(t[1], t[3], t.lineno(2), t.lexpos(2))
        grammarList.append(g.nodeGramatical('ASIGNA  -> ID IGUAL EXPRESION ', f' ASIGNA.val = SingleDeclaration(t[1], t[3], t.lineno(2), t.lexpos(2))'))
    elif len(t) == 3: 
        t[0] = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('ASIGNA  -> ID CORCHETES ', f' ASIGNA.val = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))'))
    elif len(t) == 2: 
        t[0] = SingleDeclaration(t[1], '#', t.lineno(1), t.lexpos(1)) #si mando numeral significa que no esta inicializada
        grammarList.append(g.nodeGramatical('ASIGNA  -> ID ', f' ASIGNA.val = SingleDeclaration(t[1], #, t.lineno(1), t.lexpos(1))'))
    else: 
        t[0] = DeclarationArrayInit(t[1], t[2], t[4], t.lineno(3), t.lexpos(3))
        grammarList.append(g.nodeGramatical('ASIGNA  -> ID ', f' ASIGNA.val = DeclarationArrayInit(t[1], t[2], t[4], t.lineno(3), t.lexpos(3))'))

def p_corchetes(t):
    '''CORCHETES :  CORCHETES CORCHETE
                    | CORCHETE '''
    global grammarList
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('CORCHETES  -> CORCHETES CORCHETE ', f' CORCHETES_1.val.append(CORCHETE.val) \n CORCHETES.val= CORCHETES_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('CORCHETES  ->  CORCHETE ', f' CORCHETES.val= CORCHETE.val'))

def p_corchete1_error(t):
    'CORCHETE :     CORIZQ VALOR error'
def p_corchete2_error(t):
    'CORCHETE :     error VALOR CORDER'
def p_corchete(t):
    'CORCHETE :     CORIZQ VALOR CORDER'
    t[0] = t[2]
    global grammarList
    grammarList.append(g.nodeGramatical('CORCHETE  ->  CORIZQ VALOR CORDER ', f' CORCHETE.val= VALOR.val'))

def p_valor(t):
    'VALOR :        EXPRESION'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('VALOR  ->  EXPRESION ', f' VALOR.val= EXPRESION.val'))

def p_valorEmpty(t):
    'VALOR : '
    t[0] = []
    global grammarList
    grammarList.append(g.nodeGramatical('VALOR  ->  empty ', f' VALOR.val= []'))

def p_expresion_error(t):
    'EXPRESION :  EXPRESION error EXPRESION'
def p_expresion(t):
    '''EXPRESION :  EXPRESION MAS EXPRESION
                    | EXPRESION MENOS EXPRESION
                    | EXPRESION POR EXPRESION
                    | EXPRESION DIV EXPRESION
                    | EXPRESION MODULO EXPRESION
                    | EXPRESION IGUALQUE EXPRESION
                    | EXPRESION DIFERENTE EXPRESION
                    | EXPRESION MENORQUE EXPRESION
                    | EXPRESION MAYORQUE EXPRESION
                    | EXPRESION MENORIGUAL EXPRESION
                    | EXPRESION MAYORIGUAL EXPRESION
                    | EXPRESION NOTBIT EXPRESION
                    | EXPRESION ANDBIT EXPRESION
                    | EXPRESION XORBIT EXPRESION
                    | EXPRESION ORBIT EXPRESION
                    | EXPRESION OR EXPRESION
                    | EXPRESION AND EXPRESION
                    | EXPRESION SHIFTIZQ EXPRESION
                    | EXPRESION SHIFTDER EXPRESION
                    | PARIZQ EXPRESION PARDER                    
                    | C_INT EXPRESION
                    | C_FLOAT EXPRESION
                    | C_CHAR EXPRESION                    
                    | SIZEOF PARIZQ EXPRESION PARDER                    
                    | NOTLOGICA EXPRESION
                    | MENOS EXPRESION %prec UMENOS
                    | NOTBIT EXPRESION
                    | ANDBIT EXPRESION %prec UANDBIT
                    | LLAMADA_FUNCION
                    | SCANF PARIZQ PARDER
                    | INCRE_DECRE'''
            #       | EXPRESION TERNARIO EXPRESION DOSPUNTOS EXPRESION'''

    global grammarList
    if len(t) == 4:
        #aritmetics
        if t[2] == '+': t[0] = BinaryExpression(t[1],t[3],Aritmetics.MAS, t.lineno(2), t.lexpos(2))        
        elif t[2] == '-': t[0] = BinaryExpression(t[1],t[3],Aritmetics.MENOS, t.lineno(2), t.lexpos(2))
        elif t[2] == '*': t[0] = BinaryExpression(t[1],t[3],Aritmetics.POR, t.lineno(2), t.lexpos(2))
        elif t[2] == '/': t[0] = BinaryExpression(t[1],t[3],Aritmetics.DIV, t.lineno(2), t.lexpos(2))
        elif t[2] == '%': t[0] = BinaryExpression(t[1],t[3], Aritmetics.MODULO, t.lineno(2), t.lexpos(2))
        #logics
        elif t[2] == '&&': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.AND, t.lineno(2), t.lexpos(2))
        elif t[2] == '||': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.OR, t.lineno(2), t.lexpos(2))
        elif t[2] == '==': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.IGUALQUE, t.lineno(2), t.lexpos(2))
        elif t[2] == '!=': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.DIFERENTE, t.lineno(2), t.lexpos(2))
        elif t[2] == '>=': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORIGUAL, t.lineno(2), t.lexpos(2))
        elif t[2] == '<=': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORIGUAL, t.lineno(2), t.lexpos(2))
        elif t[2] == '>': t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORQUE, t.lineno(2), t.lexpos(2))
        elif t[2] == '<': 
            print("menor que")
            t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORQUE, t.lineno(2), t.lexpos(2))
        #bits
        elif(t[2] == '|'): t[0] = RelationalBit(t[1],t[3], BitToBit.ORBIT, t.lineno(1), t.lexpos(1))
        elif(t[2] == '^'): t[0] = RelationalBit(t[1],t[3], BitToBit.XORBIT, t.lineno(1), t.lexpos(1))
        elif(t[2] == '<<'): t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTI, t.lineno(1), t.lexpos(1))
        elif(t[2] == '>>'): t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTD, t.lineno(1), t.lexpos(1))
        elif (t[2] == '&'): t[0] = RelationalBit(t[1], t[3], BitToBit.ANDBIT, t.lineno(1), t.lexpos(1))

        #grammarList.append(g.nodeGramatical('EXPRESION  ->  empty ', f' EXPRESION.val= BinaryExpression(t[1],t[3],Aritmetics.MAS, t.lineno(2), t.lexpos(2))'))
        
        elif t[1] == 'scanf': t[0] = Scanf(t.lineno(1), t.lexpos(1))
        elif t[1] == '(': t[0] = t[2]
    elif len(t) == 2:
        t[0] = t[1]
    else:
        if t[1] == '-' : t[0] = NegativeNumber(t[2], t.lineno(2), t.lexpos(2))
        elif t[1] == '~' : t[0] = NotBit(t[2], t.lineno(1), t.lexpos(1))
        elif t[1] == '&' :t[0] = ReferenceBit(t[2], t.lineno(1), t.lexpos(1))    
        elif t[1] == '!' : t[0] = Not(t[2], t.lineno(2), t.lexpos(2))
        elif t[1] == 'sizeof': t[0] = SizeOf(t[3], t.lineno(1), t.lexpos(1))
        elif t[1] == '(': t[0] = Parentesis(t[2], t.lineno(2), t.lexpos(2))
        elif t[1] == '(int)': t[0] = Cast_(t[2], 'int', t.lineno(1), t.lexpos(1))
        elif t[1] == '(float)': t[0] = Cast_(t[2], 'float', t.lineno(1), t.lexpos(1))
        elif t[1] == '(char)': t[0] = Cast_(t[2], 'char', t.lineno(1), t.lexpos(1))
        #print("aqui estoy");

def p_expresiones_numero(t):
    '''EXPRESION :    NUMERO'''
    t[0] = Number( t.lineno(1), t.lexpos(1), t[1])
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION  ->  NUMERO ', f' EXPRESION.val= Number( t.lineno(1), t.lexpos(1), t[1])'))

def p_expresiones_cadena(t):
    '''EXPRESION :    CADENA'''
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION  ->  CADENA ', f' EXPRESION.val= String_(t[1], t.lineno(1), t.lexpos(1))'))

def p_expresiones_char(t):
    '''EXPRESION :    CHAR_'''
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION  ->  CHAR_ ', f' EXPRESION.val= String_(t[1], t.lineno(1), t.lexpos(1))'))

def p_expresiones_id_error(t):
    'EXPRESION :    error CORCHETES'
def p_expresiones_id(t):
    '''EXPRESION :    ID CORCHETES
                        | ID 
        '''
        
    global grammarList
    if len(t) == 3: 
        t[0] = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('EXPRESION  ->  ID CORCHETES ', f' EXPRESION.val= IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))'))
    elif len(t) == 2: 
        t[0] =  Identifier(t[1], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('EXPRESION  ->  ID ', f' EXPRESION.val= Identifier(t[1], t.lineno(1), t.lexpos(1))'))

def p_expresiones_id_listapuntos(t):    #EXPRESION GET STRUCT
    '''EXPRESION :     ASISTRCUT LISTA_PUNTOS '''
    #ASISTRCUT me devuelve identiArray o identiofy
    #puntos me devuelve simple o compuesto
    print("aquiiiiiiiiii")
    t[0] = AccesStruct(t[1], t[2])
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION  ->  ASISTRCUT LISTA_PUNTOS ', f' EXPRESION.val= Accesos(t[1],t[2])'))
   
def p_expresiones_listaCorchetesInit(t):
    '''EXPRESION :   LISTA_INIT_CORCHETE'''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION  -> LISTA_INIT_CORCHETE ', f' EXPRESION.val= LISTA_INIT_CORCHETE.val'))

def p_listaInitCorchete(t):
    '''LISTA_INIT_CORCHETE :    LLAVEIZQ PARAMETROS LLAVEDER 
    '''
    t[0] = InitializationArray(t.lineno(1), t.lexpos(1), t[2])
    global grammarList
    grammarList.append(g.nodeGramatical('LISTA_INIT_CORCHETE  -> LLAVEIZQ PARAMETROS LLAVEDER  ', f' LISTA_INIT_CORCHETE.val= InitializationArray(t.lineno(1), t.lexpos(1), t[2])'))

def p_llamadaFuncion_error(t):
    '''LLAMADA_FUNCION :     ID PARIZQ error PARDER '''
def p_llamadaFuncion(t):
    '''LLAMADA_FUNCION :     ID PARIZQ PARAMETROS PARDER 
                            | ID PARIZQ PARDER'''
    global grammarList
    if len(t) == 5:
        t[0] = CallFunction(t[1], t[3], t.lineno(2), t.lexpos(2))
        grammarList.append(g.nodeGramatical('LLAMADA_FUNCION  -> LLAVEIZQ PARAMETROS LLAVEDER  ', f' LLAMADA_FUNCION.val= Call(t[1], t[3])'))
    else:
        t[0] = CallFunction(t[1], [] , t.lineno(2), t.lexpos(2))
        grammarList.append(g.nodeGramatical('LLAMADA_FUNCION  -> ID PARIZQ PARDER  ', f' LLAMADA_FUNCION.val= Call(t[1], [])'))

def p_parametros_error(t):
    'PARAMETROS :     PARAMETROS error EXPRESION'
def p_parametros(t):
    '''PARAMETROS :     PARAMETROS COMA EXPRESION
                        | EXPRESION '''
    global grammarList
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('PARAMETROS  -> PARAMETROS COMA EXPRESION  ', f' PARAMETROS_1.val.append(EXPRESION.val) \n PARAMETROS.val= PARAMETROS_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('PARAMETROS  -> EXPRESION ', f' PARAMETROS.val= [EXPRESION.val]'))


##----------------------DECLARACION DE FUNCIONES---------------------
def p_declaFuncion_error_2(t):
    'DECLA_FUNCIONES :    TIPO ID PARIZQ error PARDER LLAVEIZQ error LLAVEDER'
def p_declaFuncion_error(t):
    'DECLA_FUNCIONES :    TIPO ID PARIZQ RECEPCION_PARAMETROS PARDER LLAVEIZQ error LLAVEDER'
def p_declaFuncion(t):
    'DECLA_FUNCIONES :    TIPO ID PARIZQ RECEPCION_PARAMETROS PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'

    t[0] = FunctionDeclaration(t[1], t[2], t[4], t[7], t.lineno(2), t.lexpos(2))
    global grammarList
    grammarList.append(g.nodeGramatical('DECLA_FUNCIONES  ->  TIPO ID PARIZQ RECEPCION_PARAMETROS PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER ', f' DECLA_FUNCIONES.val= FunctionDeclaration(t[1], t[2], t[4], t[7], t.lineno(2), t.lexpos(2))'))

def p_recepcionParametros_error(t):
    'RECEPCION_PARAMETROS :   RECEPCION_PARAMETROS COMA error'
def p_recepcionParametros(t):
    '''RECEPCION_PARAMETROS :   RECEPCION_PARAMETROS COMA PARAM
                                | PARAM'''
    global grammarList
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('RECEPCION_PARAMETROS  ->  RECEPCION_PARAMETROS COMA PARAM ', f' RECEPCION_PARAMETROS_1.val.append(PARAM) \n RECEPCION_PARAMETROS.val= RECEPCION_PARAMETROS_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('RECEPCION_PARAMETROS  ->   PARAM ', f' RECEPCION_PARAMETROS.val= PARAM.val'))

def p_recepcionParametrosEmpty(t):
    'RECEPCION_PARAMETROS :  '
    t[0] = []
    global grammarList
    grammarList.append(g.nodeGramatical('RECEPCION_PARAMETROS  ->   empty ', f' RECEPCION_PARAMETROS.val= []'))

def p_param(t):
    'PARAM :    TIPO_FUN PUNT'

    t[0] = Param(t[1], t[2], t.lineno(2), t.lexpos(2))
    global grammarList
    grammarList.append(g.nodeGramatical('PARAM  ->   TIPO_FUN PUNT ', f' PARAM.val= Param(t[1], t[2], t.lineno(2), t.lexpos(2))'))

def p_tipoFuncion(t):
    '''TIPO_FUN :   TIPO
                    | STRUCT
    '''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('TIPO_FUN  -> TIPO \n | STRUCT ', f' TIPO_FUN.val= t[1]'))

def p_punt(t):
    '''PUNT :     ID ID
                | ID '''
    global grammarList
    if len(t) == 3:
        grammarList.append(g.nodeGramatical('PUNT  -> ID ID ', f' PUNT.val= Ids(t[1],t[2])'))
    else:
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('PUNT  -> ID  ', f' PUNT.val= ID.value'))

def p_instruccionesInternas(t):
    '''INSTRUCCIONES_INTERNAS :     INSTRUCCIONES_INTERNAS INSTR_IN
                                    | INSTR_IN'''
    global grammarList
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('INSTRUCCIONES_INTERNAS  -> INSTRUCCIONES_INTERNAS INSTR_IN ', f' INSTRUCCIONES_INTERNAS_1.val.append(INSTR_IN.val) \n INSTRUCCIONES_INTERNAS.val= INSTRUCCIONES_INTERNAS_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('INSTRUCCIONES_INTERNAS  -> INSTR_IN ', f'INSTRUCCIONES_INTERNAS.val= INSTR_IN.val'))

def p_instrIn_error(t):
    'INSTR_IN :   error'
def p_instrIn(t):
    '''INSTR_IN :   DECLA_VARIABLES
                    | DECLARACION_STRUCT_INTERNA
                    | ASIGNACIONES
                    | IF_
                    | FOR_
                    | WHILE_
                    | DO_
                    | SWITCH_
                    | LLAMADA_FUNCION PUNTOCOMA
                    | PRINTF PARIZQ PARAMETROS PARDER PUNTOCOMA
                    | RETURN EXPRESION PUNTOCOMA
                    | CONTINUE PUNTOCOMA
                    | BREAK PUNTOCOMA
                    | GOTO ID PUNTOCOMA
                    | PUNTOCOMA'''
    global grammarList
    if t[1] == 'printf':
        t[0] = PrintF_(t[3], t.lineno(1), t.lexpos(1))  
        grammarList.append(g.nodeGramatical('INSTR_IN  -> PRINTF PARIZQ PARAMETROS PARDER PUNTOCOMA ', f'INSTR_IN.val= PrintF_(t[3], t.lineno(1), t.lexpos(1)) ')) 
    elif t[1] == 'goto':
        t[0] = Goto(t[2])
        grammarList.append(g.nodeGramatical('INSTR_IN  -> GOTO ID PUNTOCOMA ', f'INSTR_IN.val= Goto(t[2])'))
    elif t[1] == 'for':
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('INSTR_IN  -> FOR_ ', f'INSTR_IN.val= FOR_.val'))
    else:
        print("llamadas desde instrucciones internas")
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('INSTR_IN  -> ..... ', f'INSTR_IN.val= t[1]'))

def p_instrInLabel(t):
    '''INSTR_IN :   ID DOSPUNTOS'''
    t[0] = Label(t[1], t.lineno(1), find_column(input_, t.slice[1]))
    global grammarList
    grammarList.append(g.nodeGramatical('INSTR_IN  -> ID DOSPUNTOS ', f'INSTR_IN.val= Label(t[1], t.lineno(1), find_column(input_, t.slice[1]))'))

def p_declaracionStructInterna_error(t):
    'DECLARACION_STRUCT_INTERNA : STRUCT ID ID IGUAL error PUNTOCOMA'
def p_declaracionStructIntern2_error(t):
    'DECLARACION_STRUCT_INTERNA : STRUCT ID error PUNTOCOMA'
def p_declaracionStructInterna(t):
    '''DECLARACION_STRUCT_INTERNA : STRUCT ID ASISTRCUT PUNTOCOMA
                                    | ID ASISTRCUT PUNTOCOMA
                                    | ASISTRCUT IGUAL EXPRESION PUNTOCOMA                                                
                                    | ASISTRCUT LISTA_PUNTOS OP_ASIGNACION EXPRESION PUNTOCOMA
    '''
    global grammarList
    if len(t) == 5 and t[1] == 'struct':
        #STRUCT ID ASISTRCUT PUNTOCOMA
        t[0] = DeclaStructIntr(t[2], t[3], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('DECLARACION_STRUCT_INTERNA  -> STRUCT ID ASISTRCUT PUNTOCOMA ', f'DECLARACION_STRUCT_INTERNA.val= AsignationStruct(t[2], t[3], t.lineno(1), t.lexpos(1))'))
    elif len(t) == 6:
        #ASISTRCUT ID IGUAL EXPRESION PUNTOCOMA
        a = 3
        t[0] = AsignationStructExpre(t[1], t[2], t[4], t.lineno(5), t.lexpos(5))
        grammarList.append(g.nodeGramatical('DECLARACION_STRUCT_INTERNA  -> ASISTRCUT LISTA_PUNTOS OP_ASIGNACION EXPRESION PUNTOCOMA ', f'DECLARACION_STRUCT_INTERNA.val= AsignationStructExpre(t[1], t[2], t[4], t.lineno(6), t.lexpos(6))'))

def p_asignaStructInterna(t):
    '''ASISTRCUT :  ID CORCHETES
                    | ID
    '''
    global grammarList
    if len(t) == 3:
        t[0] = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('ASISTRCUT  -> ID CORCHETES  ', f'ASISTRCUT.val= IdentifyArray(t[1],t[2])'))
    else:
        t[0] = Identifier(t[1], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('ASISTRCUT  -> ID  ', f'ASISTRCUT.val= ID.value)'))

def p_asignaciones_error(t):
    '''ASIGNACIONES :   error PUNTOCOMA
                        | ID error EXPRESION PUNTOCOMA
                        | ID CORCHETES error EXPRESION PUNTOCOMA'''
def p_asignaciones(t):
    '''ASIGNACIONES :   INCRE_DECRE PUNTOCOMA
                        | ID OP_ASIGNACION EXPRESION PUNTOCOMA
                        | ID CORCHETES OP_ASIGNACION EXPRESION PUNTOCOMA'''

    global grammarList
    if len(t) == 6:
        #asignacion de valor a arreglo;
        a = 3
        t[0] = AsignationArray(t[1], t[2], t[4], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('ASIGNACIONES  -> ID CORCHETES OP_ASIGNACION EXPRESION PUNTOCOMA', f'ASIGNACIONES.val= AsignationArray(t[1], t[2], t[4], t.lineno(1), t.lexpos(1))'))
    elif len(t) == 5:  #ID OP_ASIGNACION EXPRESION PUNTOCOMA
        t[0] = Asignation(t[1], t[2], t[3], t.lineno(1), t.lexpos(3))
        grammarList.append(g.nodeGramatical('ASIGNACIONES  -> ID OP_ASIGNACION EXPRESION PUNTOCOMA  ', f'ASIGNACIONES.val= Asignation(t[1], t[2], t[3], t.lineno(1), t.lexpos(3))'))
    elif len(t) == 3: #incremento o decremento
        t[0] = t[1]
        t[0] = Asignation(t[1].id, '=', t[1], t.lineno(2), t.lexpos(2))

def p_listaPuntos(t):
    '''LISTA_PUNTOS :   PUNTO ID
                        | PUNTO ID CORCHETES'''
    global grammarList
    if len(t) == 3:
        t[0] = puntoSimple(t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('LISTA_PUNTOS  -> PUNTO ID  ', f'LISTA_PUNTOS.val = puntoSimple(t[2], t.lineno(1), t.lexpos(1))'))
    else:
        t[0] = puntoArreglo(t[2], t[3], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('LISTA_PUNTOS  -> PUNTO ID  ', f'LISTA_PUNTOS.val = puntoArreglo(t[2], t[3], t.lineno(1), t.lexpos(1))'))

def p_if_error1(t):
    '''IF_ :  IF PARIZQ EXPRESION PARDER LLAVEIZQ error LLAVEDER ELSE_IF_'''
def p_if_error(t):
    '''IF_ :  IF error LLAVEDER ELSE_IF_'''
def p_if(t):
    # Si -> if (condicion) instrucciones ( else if (condicion) instrucciones) * ( else instrucciones)?

    '''IF_ :  IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER ELSE_IF_'''

    t[0] = If(t[3], t[6], t[8], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('IF_  -> IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER ELSE_IF_', f'IF_.val= If(t[3], t[6], t[8], t.lineno(1), t.lexpos(1))'))

def flatten(nested_list):
    try:
        head = nested_list[0]
    except IndexError:
        return []
    return ((flatten(head) if isinstance(head, list) else [head]) +
            flatten(nested_list[1:]))

def p_elseIf_(t):
    '''
    ELSE_IF_ :   ELSE_IF
                | ELSE_
                | ELSE_IF ELSE_
                | 
    '''
    global grammarList
    if len(t) == 2:
        t[1] = flatten(t[1])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('ELSE_IF_  -> ELSE_IF \n | ELSE_', f't[1] = flatten(t[1]) \n ELSE_IF_.val = t[1]'))
    elif len(t) == 3:
        t[1].append(t[2])
        t[1] = flatten(t[1])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('ELSE_IF_  -> ELSE_IF ELSE_', f't[1].append(t[2]) \n t[1] = flatten(t[1]) \n ELSE_IF_.val = t[1]'))
    else:
        t[0] = []
        grammarList.append(g.nodeGramatical('ELSE_IF_  -> ', f'ELSE_IF_.val = []'))

def p_elseIf(t):
    '''
    ELSE_IF :   ELSE_IF  ELIF
                | ELIF
    '''
    global grammarList
    if len(t) == 3:
        #t[1].append(t[2])
        t[1].extend(t[2])
        t[1] = flatten(t[1])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('ELSE_IF  -> ELSE_IF  ELIF', f't[1].extend(t[2]) \n t[1] = flatten(t[1]) \n ELSE_IF.val = t[1]'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('ELSE_IF  -> ELIF', f'ELSE_IF.val = ELIF.val'))

def p_elif(t):
    '''
    ELIF :  ELSE IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER
    '''
    t[0] = [IfElse(t[4], t[7], t.lineno(1), t.lexpos(1))]
    global grammarList
    grammarList.append(g.nodeGramatical('ELIF  -> ELSE IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER', f'ELIF.val = [IfElse(t[4], t[7], t.lineno(1), t.lexpos(1))]'))

def p_else(t):
    '''ELSE_ :  ELSE LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER 
    '''
    t[0] = [Else(t[3], t.lineno(1), t.lexpos(1))]
    global grammarList
    grammarList.append(g.nodeGramatical('ELSE_  -> ELSE LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER', f'ELSE_.val = [Else(t[3], t.lineno(1), t.lexpos(1))]'))

def p_for_error2(t): 
    'FOR_ :     FOR PARIZQ error EXPRESION PUNTOCOMA INCRE_DECRE PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER' 
def p_for_error1(t): 
    'FOR_ :     FOR PARIZQ DECLA_VARIABLES error PUNTOCOMA INCRE_DECRE PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER' 
def p_for_error0(t): 
    'FOR_ :     FOR PARIZQ DECLA_VARIABLES EXPRESION PUNTOCOMA error PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'              
def p_for(t):
    'FOR_ :     FOR PARIZQ DECLA_VARIABLES EXPRESION PUNTOCOMA INCRE_DECRE PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'
    t[0] = For(t[3], t[4], t[6], t[9], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('FOR_  -> FOR PARIZQ DECLA_VARIABLES EXPRESION PUNTOCOMA INCRE_DECRE PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER', f'FOR_.val = For(t[3], t[4], t[6], t[9], t.lineno(1), t.lexpos(1))'))

def p_while_error(t):
    'WHILE_ :   WHILE error LLAVEDER'
def p_while(t):
    'WHILE_ :   WHILE PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'
    t[0] = While_(t[3], t[6], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('WHILE_  -> WHILE PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER', f'WHILE_.val = While_(t[3], t[6], t.lineno(1), t.lexpos(1))'))

def p_doWhile_error(t):
    'DO_ :  DO error PUNTOCOMA'
def p_doWhile(t):
    'DO_ :  DO LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER WHILE PARIZQ EXPRESION PARDER PUNTOCOMA'
    t[0] = DoWhile_(t[3], t[7], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('DO_ -> DO LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER WHILE PARIZQ EXPRESION PARDER PUNTOCOMA', f'DO_.val = DoWhile_(t[3], t[7], t.lineno(1), t.lexpos(1))'))

def p_switch_error(t):
    'SWITCH_ :  SWITCH error LLAVEDER'
def p_switch(t):
    'SWITCH_ :  SWITCH PARIZQ EXPRESION PARDER LLAVEIZQ LISTA_CASES DEFAULT_ LLAVEDER'

    t[0] = Switch_(t[3], t[6], t[7], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('SWITCH_ -> SWITCH PARIZQ EXPRESION PARDER LLAVEIZQ LISTA_CASES DEFAULT_ LLAVEDER', f'SWITCH_.val = Switch_(t[3], t[6], t[7], t.lineno(1), t.lexpos(1))'))

def p_listaCases(t):
    '''LISTA_CASES :  LISTA_CASES CASE_
                    | CASE_'''
    global grammarList
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('LISTA_CASES -> LISTA_CASES CASE_', f'LISTA_CASES_1.val.append(CASE_.val) \n  LISTA_CASES_.val= LISTA_CASES_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('LISTA_CASES ->  CASE_', f'LISTA_CASES_.val= [CASE_.val]'))        

def p_case_error(t):
    'CASE_ :    CASE error BREAK_'
def p_case(t):
    'CASE_ :    CASE EXPRESION DOSPUNTOS INSTRUCCIONES_INTERNAS'
  
    t[0] = Case_(t[2], t[4], 0, t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('CASE_ -> CASE EXPRESION DOSPUNTOS INSTRUCCIONES_INTERNAS BREAK_', f'CASE_.val = Case_(t[2], t[4], 0, t.lineno(1), t.lexpos(1))'))

def p_break(t):
    '''BREAK_ : BREAK
                | '''
    
    #print("estoy entrando en break")
    global grammarList
    if len(t) == 2:
        t[0] = 1
        grammarList.append(g.nodeGramatical('BREAK_ -> BREAK', f'BREAK_.val = [BREAK.val]'))

    else:
        t[0] = 0
        grammarList.append(g.nodeGramatical('BREAK_ -> empty', f'BREAK_.val = []'))

def p_default(t):
    '''DEFAULT_ :   DEFAULT DOSPUNTOS INSTRUCCIONES_INTERNAS
                    | '''
    
    global grammarList
    if len(t) == 4:
        t[0] = Default_(t[3], 0, t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('DEFAULT_ -> empty', f'DEFAULT_.val = []'))
    else:
        t[0] = []
        grammarList.append(g.nodeGramatical('DEFAULT_ -> empty', f'DEFAULT_.val = []'))

def p_increDecre(t):
    '''INCRE_DECRE :    INCRE_DECRE_POST
                        | INCRE_DECRE_PRE'''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('INCRE_DECRE -> INCRE_DECRE_POST \n | INCRE_DECRE_PRE', f'INCRE_DECRE.val = t[1]'))

def p_increDecrePost(t):
    ' INCRE_DECRE_POST :    ID SIG'
    t[0] = IncreDecre_Post(t[2], t[1], t.lineno(2), t.lexpos(2))
    global grammarList
    grammarList.append(g.nodeGramatical('INCRE_DECRE_POST -> ID SIG', f'INCRE_DECRE_POST.val = IncreDecre_Post(t[2], t[1], t.lineno(2), t.lexpos(2))'))

def p_increDecrePre(t):
    ' INCRE_DECRE_PRE :    SIG ID'
    t[0] = IncreDecre_Pre(t[1], t[2], t.lineno(2), t.lexpos(2))
    global grammarList
    grammarList.append(g.nodeGramatical('INCRE_DECRE_PRE -> SIG ID', f'INCRE_DECRE_PRE.val = IncreDecre_Pre(t[1], t[2], t.lineno(2), t.lexpos(2))'))

def p_pre(t):
    '''SIG :   INCREMENTO
                | DECREMENTO'''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('SIG -> INCREMENTO \n | DECREMENTO', f'SIG.val = t[1]'))

def p_opAsignacion(t):
    '''OP_ASIGNACION :  IGUAL
                        | MASIGUAL
                        | MENOSIGUAL
                        | PORIGUAL
                        | DIVIGUAL
                        | MODIGUAL
                        | SIIGUAL
                        | SDIGUAL
                        | ANDIGUAL
                        | XORIGUAL
                        | ORIGUAL'''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('OP_ASIGNACION -> ', f'OP_ASIGNACION.val = t[1]'))
   
##---------------------------DECLARACION DE STRUCTS------------------------
def p_declaStructs_error(t):
    'DECLA_STRUCTS :  STRUCT ID LLAVEIZQ error LLAVEDER PUNTOCOMA'
def p_declaStructs(t):
    'DECLA_STRUCTS :  STRUCT ID LLAVEIZQ ATRIBUTOS LLAVEDER PUNTOCOMA'

    t[0] = DeclarationStruct(t[2], t[4], t.lineno(1), t.lexpos(1))
    global grammarList
    grammarList.append(g.nodeGramatical('DECLA_STRUCTS -> STRUCT ID LLAVEIZQ ATRIBUTOS LLAVEDER PUNTOCOMA', f'DECLA_STRUCTS.val = DeclarationStruct(t[2], t[4], t.lineno(1), t.lexpos(1))'))

def p_atributos(t):
    '''ATRIBUTOS :  ATRIBUTOS ATR
                    | ATR'''
    global grammarList
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
        grammarList.append(g.nodeGramatical('ATRIBUTOS -> ATRIBUTOS ATR', f' ATRIBUTOS_1.val.append(ATR); \n   ATRIBUTOS.val = ATRIBUTOS_1.val'))
    else:
        t[0] = [t[1]]
        grammarList.append(g.nodeGramatical('ATRIBUTOS -> ATR', f' ATRIBUTOS_1.val = ATR.val'))

def p_atr(t):
    '''ATR :    DECLA_VARIABLES'''
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('ATR -> DECLA_VARIABLES', f'ATR.val = DECLA_VARIABLES.val'))


def p_error(t):
    global sintacticErroList
    try:
        print("Error sintactico en '%s'" % t.value + "line: "+ str(t.lineno))
        so = sinOb(t.value, t.lineno, find_column(input_, t))
        sintacticErroList.append(so)
    except:
        print("Error sintactico Irrecuperable")
        
        so = sinOb('Error sintactico: Irrecuperable', 0, 0)
        sintacticErroList.append(so)

def parse(input):
    global input_, sintacticErroList, LexicalErrosList

    sintacticErroList[:] = []
    LexicalErrosList[:] =[]

    input_ = input    
    lexer = lex.lex()
    parser = yacc.yacc()
    instructions = parser.parse(input)
    print(str(instructions))
    lexer.lineno = 1
    parser.restart()
    if len(LexicalErrosList) > 0 or len(sintacticErroList) > 0:
        if instructions == None:
            instructions = []
        else:
            instructions[:] = []
        return instructions
    return instructions
"""    
lexer = lex.lex()
parser = yacc.yacc()
f = open("./entrada.txt", "r")
input = f.read()
parser.parse(input)"""