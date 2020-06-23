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
    ('nonassoc', 'DIFERENTE','IGUALQUE'),
    ('nonassoc', 'MENORQUE','MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
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

def p_instruccionesGlobal(t):
    'A  :    INSTRUCCIONES_GLOBALES'
    t[0] = t[1]

def p_listaInstrucciones(t):
    '''INSTRUCCIONES_GLOBALES : INSTRUCCIONES_GLOBALES DECLARACION_GLOBAL
                                | DECLARACION_GLOBAL'''

    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_declaracionGlobal(t):
    '''DECLARACION_GLOBAL :     DECLA_VARIABLES
                                | DECLA_FUNCIONES
                                | DECLA_STRUCTS'''

    t[0] = t[1]

##----------------------------------DECLARACION DE VARIABLES ------------------
def p_declaVariable(t):
    'DECLA_VARIABLES :  TIPO LISTA_ID PUNTOCOMA'
    #print(f'tipo: {str(t[1])} valor: {str(t[2])}')
    t[0] = Declaration(t[1], t.lineno(1), t.lexpos(1), t[2])

def p_tipo(t):
    '''TIPO :   INT
                | FLOAT
                | DOUBLE
                | VOID
                | CHAR '''
                #| STRUCT  -> quite el tipo struct 
    t[0] = t[1]

def p_listaId(t):
    '''LISTA_ID :   LISTA_ID COMA ASIGNA
                    | ASIGNA'''

    if len(t) == 2:
        t[0] = [t[1]]
    else: 
        t[1].append(t[3])
        t[0] = t[1]

def p_asigna(t):
    '''ASIGNA :     ID IGUAL EXPRESION
                    | ID CORCHETES
                    | ID CORCHETES IGUAL EXPRESION
                    | ID'''

    if len(t) == 4: t[0] = SingleDeclaration(t[1], t[3], t.lineno(2), t.lexpos(2))
    elif len(t) == 3: t[0] = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))
    elif len(t) == 2: t[0] = SingleDeclaration(t[1], '#', t.lineno(1), t.lexpos(1)) #si mando numeral significa que no esta inicializada
    else: t[0] = DeclarationArrayInit(t[1], t[2], t[4], t.lineno(3), t.lexpos(3))

def p_corchetes(t):
    '''CORCHETES :  CORCHETES CORCHETE
                    | CORCHETE '''

    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_corchete(t):
    'CORCHETE :     CORIZQ VALOR CORDER'
    t[0] = t[2]

def p_valor(t):
    'VALOR :        EXPRESION'
    t[0] = t[1]

def p_valorEmpty(t):
    'VALOR : '
    t[0] = []

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
                    | SIZEOF PARIZQ EXPRESION PARDER
                    | NOTLOGICA EXPRESION
                    | EXPRESION SHIFTIZQ EXPRESION
                    | EXPRESION SHIFTDER EXPRESION
                    | PARIZQ EXPRESION PARDER                    
                    | C_INT EXPRESION
                    | C_FLOAT EXPRESION
                    | C_CHAR EXPRESION
                    | MENOS EXPRESION %prec UMENOS
                    | NOTBIT EXPRESION
                    | ANDBIT EXPRESION %prec UANDBIT
                    | LLAMADA_FUNCION'''
        # | EXPRESION TERNARIO EXPRESION DOSPUNTOS EXPRESION'''


    if len(t) == 4:
        #aritmetics
        if(t[2] == '+'): t[0] = BinaryExpression(t[1],t[3],Aritmetics.MAS, t.lineno(2), t.lexpos(2))        
        elif(t[2] == '-'): t[0] = BinaryExpression(t[1],t[3],Aritmetics.MENOS, t.lineno(2), t.lexpos(2))
        elif(t[2] == '*'): t[0] = BinaryExpression(t[1],t[3],Aritmetics.POR, t.lineno(2), t.lexpos(2))
        elif(t[2] == '/'): t[0] = BinaryExpression(t[1],t[3],Aritmetics.DIV, t.lineno(2), t.lexpos(2))
        elif(t[2] == '%'): t[0] = BinaryExpression(t[1],t[3], Aritmetics.MODULO, t.lineno(2), t.lexpos(2))
        #logics
        elif(t[2] == '&&'): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.AND, t.lineno(2), t.lexpos(2))
        elif(t[2] == '||'): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.OR, t.lineno(2), t.lexpos(2))
        elif(t[2] == '=='): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.IGUALQUE, t.lineno(2), t.lexpos(2))
        elif(t[2] == '!='): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.DIFERENTE, t.lineno(2), t.lexpos(2))
        elif(t[2] == '>='): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORIGUAL, t.lineno(2), t.lexpos(2))
        elif(t[2] == '<='): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORIGUAL, t.lineno(2), t.lexpos(2))
        elif(t[2] == '>'): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORQUE, t.lineno(2), t.lexpos(2))
        elif(t[2] == '<'): t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORQUE, t.lineno(2), t.lexpos(2))
        #bits
        elif(t[2] == '|'): t[0] = RelationalBit(t[1],t[3], BitToBit.ORBIT, t.lineno(1), t.lexpos(1))
        elif(t[2] == '^'): t[0] = RelationalBit(t[1],t[3], BitToBit.XORBIT, t.lineno(1), t.lexpos(1))
        elif(t[2] == '<<'): t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTI, t.lineno(1), t.lexpos(1))
        elif(t[2] == '>>'): t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTD, t.lineno(1), t.lexpos(1))
        elif (t[2] == '&'): t[0] = RelationalBit(t[1], t[3], BitToBit.ANDBIT, t.lineno(1), t.lexpos(1))
    else:
        if(t[1] == '-'): t[0] = NegativeNumber(t[2], t.lineno(2), t.lexpos(2))
        elif(t[1] == '~'): t[0] = NotBit(t[2], t.lineno(1), t.lexpos(1))
        elif(t[1] == '&'):t[0] = ReferenceBit(t[2], t.lineno(1), t.lexpos(1))    
        elif t[1] == '!' : t[0] = Not(t[2], t.lineno(2), t.lexpos(2))
        elif t[1] == 'sizeof': t[0] = SizeOf(t[3], t.lineno(1), t.lexpos(1))
        elif t[1] == '(': t[0] = Parentesis(t[2], t.lineno(2), t.lexpos(2))
        elif t[1] == '(int)': t[0] = Cast_(t[2], 'int', t.lineno(1), t.lexpos(1))
        elif t[1] == '(float)': t[0] = Cast_(t[2], 'float', t.lineno(1), t.lexpos(1))
        elif t[1] == '(char)': t[0] = Cast_(t[2], 'char', t.lineno(1), t.lexpos(1))

def p_expresiones_numero(t):
    '''EXPRESION :    NUMERO'''
    t[0] = Number( t.lineno(1), t.lexpos(1), t[1])

def p_expresiones_cadena(t):
    '''EXPRESION :    CADENA'''
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))

def p_expresiones_char(t):
    '''EXPRESION :    CHAR_'''
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))

def p_expresiones_id(t):
    '''EXPRESION :    ID CORCHETES
                        | ID CORCHETES LISTA_PUNTOS
                        | ID 
        '''
    if len(t) == 3: t[0] = IdentifierArray(t[1], t[2], t.lineno(1), t.lexpos(1))
    elif len(t) == 2: t[0] =  Identifier(t[1], t.lineno(1), t.lexpos(1))
    else: print("lista id-> corchetes-> listaPuntos")

def p_expresiones_id_listapuntos(t):
    '''EXPRESION :     ID LISTA_PUNTOS '''
   
def p_expresiones_listaCorchetesInit(t):
    '''EXPRESION :   LISTA_INIT_CORCHETE'''
    t[0] = t[1]

def p_listaInitCorchete(t):
    '''LISTA_INIT_CORCHETE :    LLAVEIZQ PARAMETROS LLAVEDER 
    '''
    t[0] = InitializationArray(t.lineno(1), t.lexpos(1), t[2])

def p_llamadaFuncion(t):
    '''LLAMADA_FUNCION :     ID PARIZQ PARAMETROS PARDER 
                            | ID PARIZQ PARDER'''

def p_parametros(t):
    '''PARAMETROS :     PARAMETROS COMA EXPRESION
                        | EXPRESION '''

    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

##----------------------DECLARACION DE FUNCIONES---------------------
def p_declaFuncion(t):
    'DECLA_FUNCIONES :    TIPO ID PARIZQ RECEPCION_PARAMETROS PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'

def p_recepcionParametros(t):
    '''RECEPCION_PARAMETROS :   RECEPCION_PARAMETROS COMA PARAM
                                | PARAM'''

def p_recepcionParametrosEmpty(t):
    'RECEPCION_PARAMETROS :  '

def p_param(t):
    'PARAM :    TIPO_FUN ID'

def p_tipoFuncion(t):
    '''TIPO_FUN :   TIPO
                    | STRUCT
    '''

def p_punt(t):
    '''PUNT :     ID PUNTERO
                | ID '''

def p_instruccionesInternas(t):
    '''INSTRUCCIONES_INTERNAS :     INSTRUCCIONES_INTERNAS INSTR_IN
                                    | INSTR_IN'''

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
                    | ID DOSPUNTOS
                    | PRINTF PARIZQ PARAMETROS PARDER PUNTOCOMA
                    | RETURN EXPRESION PUNTOCOMA
                    | CONTINUE PUNTOCOMA
                    | BREAK PUNTOCOMA
                    | GOTO ID PUNTOCOMA
                    | PUNTOCOMA'''

def p_declaracionStructInterna(t):
    '''DECLARACION_STRUCT_INTERNA : STRUCT ID PUNTERO IGUAL EXPRESION PUNTOCOMA
                                    | STRUCT ID PUNTERO IGUAL PARIZQ STRUCT PUNTERO PARDER MALLOC PARIZQ SIZEOF PARIZQ STRUCT PUNTERO PARDER PARDER PUNTOCOMA
                                    | STRUCT ID PUNTERO PUNTOCOMA
                                    | ID ASISTRCUT PUNTOCOMA
    '''

def p_asignaStructInterna(t):
    '''ASISTRCUT :  ID CORCHETES
                    | ID
    '''

def p_asignaciones(t):
    '''ASIGNACIONES :   INCRE_DECRE PUNTOCOMA
                        | ID OP_ASIGNACION EXPRESION PUNTOCOMA
                        | ID CORCHETES OP_ASIGNACION EXPRESION PUNTOCOMA
                        | ID CORCHETES LISTA_PUNTOS OP_ASIGNACION EXPRESION PUNTOCOMA
                        | ID LISTA_PUNTOS OP_ASIGNACION EXPRESION PUNTOCOMA'''

def p_listaPuntos(t):
    '''LISTA_PUNTOS :   LISTA_PUNTOS ACCES ID
                        | LISTA_PUNTOS ACCES ID CORCHETES
                        | ACCES ID
                        | ACCES ID CORCHETES'''

def p_listaFlechas(t):
    '''ACCES :   PUNTO
                | FLECHA'''

def p_if(t):
    '''IF_ :  IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER ELSE_
            | IF PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'''

def p_else(t):
    '''ELSE_ :  ELSE IF_
                | ELSE LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'''
                
def p_for(t):
    'FOR_ :     FOR PARIZQ DECLA_VARIABLES EXPRESION PUNTOCOMA INCRE_DECRE PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'

def p_while(t):
    'WHILE_ :   WHILE PARIZQ EXPRESION PARDER LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER'

def p_doWhile(t):
    'DO_ :  DO LLAVEIZQ INSTRUCCIONES_INTERNAS LLAVEDER WHILE PARIZQ EXPRESION PARDER PUNTOCOMA'

def p_switch(t):
    'SWITCH_ :  SWITCH PARIZQ EXPRESION PARDER LLAVEIZQ LISTA_CASES DEFAULT_ LLAVEDER'

def p_listaCases(t):
    '''LISTA_CASES :  LISTA_CASES CASE_
                    | CASE_'''

def p_case(t):
    'CASE_ :    CASE EXPRESION DOSPUNTOS INSTRUCCIONES_INTERNAS BREAK_'

def p_break(t):
    '''BREAK_ : BREAK
                | '''

def p_default(t):
    '''DEFAULT_ :   DEFAULT DOSPUNTOS INSTRUCCIONES_INTERNAS BREAK_
                    | '''

def p_increDecre(t):
    '''INCRE_DECRE :    INCRE_DECRE_POST
                        | INCRE_DECRE_PRE'''

def p_increDecrePost(t):
    ' INCRE_DECRE_POST :    ID SIG'

def p_increDecrePre(t):
    ' INCRE_DECRE_PRE :    SIG ID'

def p_pre(t):
    '''SIG :   INCREMENTO
                | DECREMENTO'''

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

   
##---------------------------DECLARACION DE STRUCTS------------------------
def p_declaStructs(t):
    'DECLA_STRUCTS :  STRUCT ID LLAVEIZQ ATRIBUTOS LLAVEDER PUNTOCOMA'

def p_atributos(t):
    '''ATRIBUTOS :  ATRIBUTOS ATR
                    | ATR'''

def p_atr(t):
    '''ATR :    DECLA_VARIABLES
                | STRUCT ID PUNTERO ASIGNA_STRUCT PUNTOCOMA
                | STRUCT ID PUNTERO CORCHETES ASIGNA_STRUCT PUNTOCOMA'''

def p_asignaStruct(t):
    '''ASIGNA_STRUCT :    IGUAL EXPRESION
                        | '''

def p_puntero(t):
    '''PUNTERO :    LISTA_ASTERISCOS ID
                    | ID LISTA_ASTERISCOS
                    | ID '''
    if len(t) == 3:
        if isinstance(t[1], list):
            t[1].append(t[2])
            t[0] = t[1]
        else:
            t[2].append(t[1])
            t[0] = t[1]
    else:
        t[0] = t[1]

def p_listaAsteriscos(t):
    '''LISTA_ASTERISCOS :   LISTA_ASTERISCOS POR
                            | POR '''

    if len(t) == 2: t[0] = [t[1]]
    else: 
        t[1].append(t[2])
        t[0] = t[1]

def p_error(t):
    print("Error sintactico en '%s'" % t.value + "line: "+ str(t.lineno))
    global sintacticErroList
    so = sinOb(t.value, t.lineno, find_column(input_, t))
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