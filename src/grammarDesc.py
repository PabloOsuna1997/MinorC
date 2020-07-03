# ---------------------
# @Autor
# Juan Pablo Osuna de Leon 
# 201503911
#----------------------

reservadas = {
    'if': 'IF',
    'goto': 'GOTO',
    'print': 'PRINT',
    'unset': 'UNSET',
    'exit': 'EXIT',    
    'read': 'READ',
    'array': 'ARRAY',
    'abs': 'ABS',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'xor': 'XOR',
    'main': 'MAIN'
}

tokens = [
    'PUNTOCOMA',
    'DOSPUNTOS',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'DOLAR',
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
    'NUMERAL',
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
    'CHAR_',
    'LABEL'
] + list(reservadas.values())

# er tokens

t_PUNTOCOMA  = r'\;'
t_DOSPUNTOS = r'\:'
t_LLAVEIZQ  = r'\{'
t_LLAVEDER  = r'\}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_DOLAR     = r'\$'
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

from lexicalObject import *
from sintacticObject import *
import generator as g
grammarList = []
grammarList[:] = []
sintacticErroList = []
sintacticErroList[:] = []
LexicalErrosList = []
LexicalErrosList[:] =[ ]
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
    r'\$(t|a|v|ra|sp?)[0-9]*'
    #print(str(t.value))
    t.type = reservadas.get(t.value.lower(),'ID')
    return t

def t_LABEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(),'LABEL')
    #print(t)
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
    r'\#.*\n'
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
    print("Illegal character '%s'" % t.value[0]+", linea: "+str(t.lexer.lineno))
    lo = lexOb(t.value[0],find_column(input_,t),t.lexer.lineno)
    LexicalErrosList.append(lo)
    t.lexer.skip(1)

import ply.lex as lex



#sintactic
#construction the ast
from expressions import *
from instructions import *

primeravez = 0
treeList = [] #list for save nodes
contador = 0
contadorSente = 1
conNode = 1
senteList = [] #para guardar las sentencias y despues apuntarlas
senteList_ = []
corcheList = []
bandera = 0
corcheListaux = []
corcheListaux = []
csList = []
sentenciaHija = 0
bandera = 0
res = []
fgraph = ''

lisInstructions = []

#definition of grammar 
def p_init(t):
    'S : A'
    #code (sintetize result the A to S)
    t[0] = t[1]
    #region graph
    global fgraph,senteList, contador, conNode
    
    fgraph.write("n00"+str(conNode+1)+" [label=\"A\"] ;\n")
    for i in senteList:
        fgraph.write("n00"+str(conNode+1)+" -- "+"n00"+str(i)+";\n")
    senteList[:] = []
    contador += 1;
    fgraph.write("n00"+str(conNode+2)+" [label=\"S\"] ;\n")
    fgraph.write("n00"+str(conNode+2)+" -- "+"n00"+str(conNode+1)+";\n")
    conNode +=3
    #endregion
    
    fgraph.flush()
    fgraph.close()

    global grammarList
    grammarList.append(g.nodeGramatical('S  -> A', f'S.val = A.val'))
    grammarList.reverse()

    global lisInstructions
    tmp = flatten(lisInstructions)
    lisInstructions = tmp[:]
    #print(f"\n\nlista: {str(lisInstructions)}")
    #for i in grammarList:
        #print(f'production: {i.production}, rules: {i.rules}')

def p_main(t):
    'A : MAIN DOSPUNTOS SENTENCIAS'
    #solo agrego las sentencias 
    t[0] = t[3]
    #print(f'sentencias: {str(t[3])}')
    global grammarList
    grammarList.append(g.nodeGramatical('A  -> MAIN DOSPUNTOS SENTENCIAS', f'A.val = SENTENCIAS.val'))
   
def flatten(list_):
    try:
        head = list_[0]
    except IndexError:
        return []
    return ((flatten(head) if isinstance(head, list) else [head]) +
            flatten(list_[1:]))

def p_sentencias_lista(t):
    'SENTENCIAS   : SENTENCIA SENTENCIAS_'
    lists = []
    lists.append(t[1])
    lists.extend(t[2])
    tmp = flatten(lists)
    t[0] = tmp

    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIAS  -> SENTENCIA SENTENCIAS_ ', f'SENTENCIAS_.val.append(SENTENCIA.val) \n SENTENCIAS.val = SENTENCIAS_.val'))

def p_sentecncia__lista(t):
    'SENTENCIAS_   : SENTENCIA SENTENCIAS_'
    lists = []
    lists.append(t[1])
    lists.append(t[2])
    t[0] = lists
    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIAS_  -> SENTENCIA SENTENCIAS_ ', f'SENTENCIAS_1_.val.append(SENTENCIA.val) \n SENTENCIAS_.val = SENTENCIAS_1_.val'))

def p_sentencias__empty(t):
    'SENTENCIAS_   : '
    t[0] = empty()
    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIAS_  -> epsilon ', f'SENTENCIAS_.val = empty()'))

def p_sentencia_eti(t):
    'SENTENCIA    : ETIQUETA'

    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIA -> ETIQUETA', f'SENTENCIA.val = ETIQUETA.val'))
 
def p_sentencia_instr(t):
    'SENTENCIA    :  INSTRUCCIONES'

    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIA -> INSTRUCCIONES', f'SENTENCIA.val = INSTRUCCIONES.val'))
   
def p_sentencia_decla(t):
    'SENTENCIA    :  DECLARACIONES'

    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('SENTENCIA -> DECLARACIONES', f'SENTENCIA.val = DECLARACIONES.val'))
   
def p_etiqueta_error(t):
    'ETIQUETA   : LABEL error DOSPUNTOS' 
        
def p_etiqueta(t):
    # i call label to recognize the label
    'ETIQUETA   : LABEL DOSPUNTOS' 
    t[0] = Label(t[1], t.lineno(1), find_column(input_, t.slice[1]))
    global grammarList
    grammarList.append(g.nodeGramatical('ETIQUETA -> LABEL DOSPUNTOS', f'ETIQUETA.val = Label(LABEL.value)'))
  
def p_instrucciones_error(t):
    '''INSTRUCCIONES    : PRINT PARIZQ error PARDER PUNTOCOMA
                        | IF PARIZQ error PARDER GOTO LABEL PUNTOCOMA
                        | UNSET PARIZQ error PARDER PUNTOCOMA
                        | EXIT error PUNTOCOMA
                        | GOTO error  PUNTOCOMA'''

def p_instrucciones(t):
    '''INSTRUCCIONES    : PRINT PARIZQ EXPRESION PARDER PUNTOCOMA
                        | IF PARIZQ EXPRESION PARDER GOTO LABEL PUNTOCOMA
                        | UNSET PARIZQ ID PARDER PUNTOCOMA
                        | EXIT PUNTOCOMA
                        | GOTO LABEL PUNTOCOMA'''

    global contador, conNode, fgraph, senteList, input_, grammarList, lisInstructions
    if(t[1] == 'print'): 
        t[0] = Print_(t[3], t.lineno(2), find_column(input_, t.slice[2]))
        grammarList.append(g.nodeGramatical('INSTRUCCIONES -> PRINT ( EXPRESION ) PUNTOCOMA', f'INSTRUCCIONES.val = Print_(EXPRESION.val'))
    elif(t[1] == 'if'): 
        t[0] = If(t[3], t[6], t.lineno(2), find_column(input_, t.slice[2]))
        grammarList.append(g.nodeGramatical('INSTRUCCIONES -> IF ( EXPRESION ) GOTO LABEL PUNTOCOMA', f'INSTRUCCIONES.val = If(EXPRESION.val, LABEL.value'))
    elif(t[1] == 'unset'): 
        t[0] = Unset(t[3], t.lineno(3), t.lexpos(3))
        grammarList.append(g.nodeGramatical('INSTRUCCIONES -> UNSET ( ID ) PUNTOCOMA', f'INSTRUCCIONES.val = Unset(ID.value)'))
    elif(t[1] == 'goto'): 
        t[0] = Goto(t[2])
        grammarList.append(g.nodeGramatical('INSTRUCCIONES -> GOTO LABEL PUNTOCOMA', f'INSTRUCCIONES.val = Goto(LABEL.value)'))
    elif(t[1] == 'exit'): 
        t[0] = Exit()
        grammarList.append(g.nodeGramatical('INSTRUCCIONES -> EXIT PUNTOCOMA', f'INSTRUCCIONES.val = Exit( )'))

def p_declaraciones(t):
    'DECLARACIONES  : ID ARRAY_'
    t[0] = Declaration(t[1], t.lineno(1), t.lexpos(1),t[2])
    global grammarList
    grammarList.append(g.nodeGramatical('DECLARACIONES -> ID ARRAY', f'DECLARACIONES.val = Declaration(ID.value,ARRAY_.val'))

def p_array1_error(t):
    'ARRAY_    :  error IGUAL EXPRESION PUNTOCOMA'

def p_array_error(t):
    '''ARRAY_    :  CORCHETES IGUAL error PUNTOCOMA
                | IGUAL error PUNTOCOMA'''

def p_array(t):
    '''ARRAY_    :  CORCHETES IGUAL EXPRESION PUNTOCOMA
                | IGUAL EXPRESION PUNTOCOMA'''
    global grammarList
    if(t[1] == '='): 
        t[0] = t[2]  #if expresion is array, expression contain 'array'
        grammarList.append(g.nodeGramatical('ARRAY_ -> IGUAL EXPRESION PUNTOCOMA', f'ARRAY_.val = EXPRESION.val'))
    else: 
        t[0] = ExpressionsDeclarationArray(t[1], t[3], t.lineno(2), find_column(input_, t.slice[2]))
        grammarList.append(g.nodeGramatical('ARRAY_ -> CORCHETES IGUAL EXPRESION PUNTOCOMA', f'ARRAY_.val = ExpresionDeclarationArray(CORCHETES.val, EXPRESION.val)'))

def p_corchete_lista(t):
    'CORCHETES : CORCHETE CORCHETES_'
    if isinstance(t[2], list):
        t[2].append(t[1])
        #lista en esta posicion viene invertida, asi que se revierte
        t[2].reverse()
    t[0] = t[2]
    global grammarList
    grammarList.append(g.nodeGramatical('CORCHETES -> CORCHETES CORCHJETES_', f'CORCHETES_.val.append(CORCHETE.val) \n CORCHETES_.val.reverse() \n CORRCHETES.val = CORCHETES_.val'))
    
def p_corchetes__corchete(t):
    'CORCHETES_ : CORCHETE CORCHETES_'
    if isinstance(t[2], list):
        t[2].append(t[1])
    t[0] = t[2]
    global grammarList
    grammarList.append(g.nodeGramatical('CORCHETES_ -> CORCHETES CORCHETES_', f'CORCHETES_1_.val.append(CORCHETE.val) \n  CORRCHETES_.val = CORCHETES_1_.val'))

def p_corchetes__empty(t):
    'CORCHETES_  : '
    t[0] = []
    global grammarList
    grammarList.append(g.nodeGramatical('CORCHETES_ -> epsilon', f'CORCHETES_.val = empty()'))

def p_corchete(t):
    'CORCHETE : CORIZQ F CORDER'
    t[0] = t[2]
    global grammarList
    grammarList.append(g.nodeGramatical('CORCHETE -> CORQIZQ F CORDER', f'CORCHETE.val = F.val'))
  
def p_expresion_ato(t):
    'EXPRESION    :  ATOMICO'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION -> ATOMICO', f'EXPRESION.val = ATOMICO.val'))
   
def p_expresion_fun(t):
    'EXPRESION    :  FUNCION'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION -> FUNCION', f'EXPRESION.val = FUNCION.val'))
   
def p_expresion_ope(t):
    'EXPRESION    :  OPERACION'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('EXPRESION -> OPERACION', f'EXPRESION.val = OPERACION.val'))
    
def p_operacion_error(t):
    '''OPERACION    : F error F
                    | MENOS error
                    | NOTLOGICA error
                    | NOTBIT error
                    | ANDBIT error'''

def p_operacion(t):
    '''OPERACION    : F OPERADOR F
                    | MENOS F
                    | NOTLOGICA F
                    | NOTBIT F
                    | ANDBIT F'''

    #code
    #aritmetics
    global contador, conNode, fgraph,senteList,corcheList, grammarList, lisInstructions
    if(t[2] == '+'):        t[0] = BinaryExpression(t[1],t[3],Aritmetics.MAS, t.lineno(2), t.lexpos(2))
    elif(t[2] == '-'):        t[0] = BinaryExpression(t[1],t[3],Aritmetics.MENOS, t.lineno(2), t.lexpos(2))
    elif(t[2] == '*'):        t[0] = BinaryExpression(t[1],t[3],Aritmetics.POR, t.lineno(2), t.lexpos(2))
    elif(t[2] == '/'):        t[0] = BinaryExpression(t[1],t[3],Aritmetics.DIV, t.lineno(2), t.lexpos(2))
    elif(t[2] == '%'):        t[0] = BinaryExpression(t[1],t[3], Aritmetics.MODULO, t.lineno(2), t.lexpos(2))
    #unitaries
    elif(t[1] == '-'):        
        t[0] = NegativeNumber(t[2], t.lineno(2), t.lexpos(2))
        grammarList.append(g.nodeGramatical('OPERACION -> MENOS F', f'OPERACION.val = NegativeNumber(F.val)'))
    elif(t[1] == '!'): 
        t[0] = Not(t[2], t.lineno(2), t.lexpos(2))
        grammarList.append(g.nodeGramatical('OPERACION -> NOTLOGICA F', f'OPERACION.val = Not(F.val)'))
    elif(t[1] == '~'): 
        t[0] = NotBit(t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('OPERACION -> NOTBIT F', f'OPERACION.val = NotBit(F.val)'))
    elif(t[1] == '&'):
        t[0] = ReferenceBit(t[2], t.lineno(1), t.lexpos(1))
        grammarList.append(g.nodeGramatical('OPERACION -> ANDBIT F', f'OPERACION.val = ReferenceBit(F.val)'))
    #relational and logical
    elif(t[2] == '&&'):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.AND, t.lineno(2), t.lexpos(2))
    elif(t[2] == '||'):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.OR, t.lineno(2), t.lexpos(2))
    elif(t[2] == 'xor'):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.XOR, t.lineno(2), t.lexpos(2))
    elif(t[2] == '=='):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.IGUALQUE, t.lineno(2), t.lexpos(2))
    elif(t[2] == '!='):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.DIFERENTE, t.lineno(2), t.lexpos(2))
    elif(t[2] == '>='):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORIGUAL, t.lineno(2), t.lexpos(2))
    elif(t[2] == '<='):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORIGUAL, t.lineno(2), t.lexpos(2))
    elif(t[2] == '>'):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MAYORQUE, t.lineno(2), t.lexpos(2))
    elif(t[2] == '<'):        t[0] = LogicAndRelational(t[1],t[3], LogicsRelational.MENORQUE, t.lineno(2), t.lexpos(2))
    #bit to bit
    elif(t[2] == '|'):        t[0] = RelationalBit(t[1],t[3], BitToBit.ORBIT, t.lineno(1), t.lexpos(1))
    elif(t[2] == '^'):        t[0] = RelationalBit(t[1],t[3], BitToBit.XORBIT, t.lineno(1), t.lexpos(1))
    elif(t[2] == '<<'):        t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTI, t.lineno(1), t.lexpos(1))
    elif(t[2] == '>>'):        t[0] = RelationalBit(t[1],t[3], BitToBit.SHIFTD, t.lineno(1), t.lexpos(1))

def p_numero(t):
    'ATOMICO     : F'
    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('ATOMICO -> F', f'ATOMICO.val = F.val'))
  
def p_funcion(t):
    '''FUNCION      : ABS PARIZQ EXPRESION PARDER
                    | READ PARIZQ PARDER
                    | PARIZQ TIPO PARDER ID
                    | ARRAY PARIZQ PARDER'''
    
    global contador, conNode, fgraph, grammarList,lisInstructions
    if(t[1] == 'abs'):      
        t[0] = Abs(t[3], t.lineno(3), t.lexpos(3))
        grammarList.append((g.nodeGramatical('FUNCION -> ABS ( EXPRESION )', f'FUNCION.val = Abs(EXPRESION.val)')))
    elif(t[1] == 'read'):   
        t[0] = ReadConsole(t.lineno(1), t.lexpos(1))
        grammarList.append((g.nodeGramatical('FUNCION -> READ (  )', f'FUNCION.val = ReadConsole( )')))
    elif(t[1] == '('):
        t[0] = Cast_(Identifier(t[4], t.lineno(4), t.lexpos(4)),t[2], t.lineno(2), t.lexpos(2))
        grammarList.append((g.nodeGramatical('FUNCION -> ( TIPO )', f'FUNCION.val = Cast_(Identifier({t[4]}),{t[2]})')))
    elif(t[1] == 'array'):  
        t[0] = t[1]  #devolvemos la palabra array
        grammarList.append((g.nodeGramatical('FUNCION -> ARRAY (  )', f'FUNCION.val = \'array\'')))

def p_operador(t):
    '''OPERADOR     :   MAS
                        | MENOS
                        | DIV
                        | POR
                        | MODULO
                        | AND
                        | OR
                        | XOR
                        | IGUALQUE
                        | DIFERENTE
                        | MAYORIGUAL
                        | MENORIGUAL
                        | MAYORQUE
                        | MENORQUE
                        | ANDBIT
                        | ORBIT
                        | XORBIT
                        | SHIFTIZQ
                        | SHIFTDER'''

    t[0] = t[1]
    global grammarList
    grammarList.append(g.nodeGramatical('''OPERADOR -> MAS
                                                    | MENOS
                                                    | DIV
                                                    | POR
                                                    | MODULO
                                                    | AND
                                                    | OR
                                                    | XOR
                                                    | IGUALQUE
                                                    | DIFERENTE
                                                    | MAYORIGUAL
                                                    | MENORIGUAL
                                                    | MAYORQUE
                                                    | MENORQUE
                                                    | ANDBIT
                                                    | ORBIT
                                                    | XORBIT
                                                    | SHIFTIZQ
                                                    | SHIFTDER''', f'TIPO.val = NODE.value'))
    
def p_tipo(t):
    ''' TIPO    : INT
                | FLOAT
                | CHAR'''

    t[0] = t[1]
    global grammarList
    grammarList.append((g.nodeGramatical('TIPO -> INT | FLOAT | CHAR', f'TIPO.val = {t[1]}')))
    
def p_f_numero(t):
    'F  : NUMERO'
    global grammarList
    grammarList.append(g.nodeGramatical('F -> NUMERO', f'F.val = Number({t[1]})'))
    t[0] = Number(t.lineno(1), t.lexpos(1), t[1])

def p_f_id(t):
    'F  : ID'
    global grammarList
    grammarList.append((g.nodeGramatical('F -> ID', f'F.val = Identifier({t[1]})')))
    t[0] = Identifier(t[1], t.lineno(1), t.lexpos(1))
    
def p_f_idARRAY(t):
    'F  : ID CORCHETES'
    global grammarList
    grammarList.append((g.nodeGramatical('F -> ID CORCHETES', f'F.val = IdentifierArray(ID.value,CORCHETES.val)')))
    t[0] = IdentifierArray(t[1],t[2],t.lineno(1), find_column(input_, t.slice[1]))

def p_f_cadena(t):
    'F  : CADENA'
    global grammarList
    grammarList.append((g.nodeGramatical('F -> CADENA', f'F.val = String_({t[1]})')))
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))

def p_f_char(t):
    'F  : CHAR_'
    grammarList.append((g.nodeGramatical('F -> CHAR', f'F.val = Stirng_({t[1]})')))
    t[0] = String_(t[1], t.lineno(1), t.lexpos(1))

def p_error(t):
    print("Error sintactico en '%s'" % t.value + "line: "+ str(t.lineno))
    global sintacticErroList
    so = sinOb(t.value, t.lineno, find_column(input_, t))
    sintacticErroList.append(so)
   

import ply.yacc as yacc


def parse(input):
    global input_, fgraph, primeravez, treeList, contador, contadorSente, conNode, senteList, senteList_, corcheList, bandera
    global corcheListaux, csList, sentenciaHija, res, fgraph, sintacticErroList, LexicalErrosList
    primeravez = 0
    treeList = [] #list for save nodes
    contador = 0
    contadorSente = 1
    conNode = 1
    senteList = [] #para guardar las sentencias y despues apuntarlas
    senteList_ = []
    corcheList = []
    bandera = 0
    corcheListaux = []
    corcheListaux = []
    csList = []
    sentenciaHija = 0
    bandera = 0
    res = []
    fgraph = ''
    sintacticErroList[:] = []
    LexicalErrosList[:] =[]

    input_ = input
    fgraph = open('../reports/ast.dot','a') #creamos el archivo
    fgraph.write("\n") 
    #print(input_)
    lexer = lex.lex()
    parser = yacc.yacc()
    instructions = parser.parse(input)
    lexer.lineno = 1
    parser.restart()
    if len(LexicalErrosList) > 0 or len(sintacticErroList) > 0:
        if instructions == None:
            instructions = []
        else:
            instructions[:] = []
        return instructions
    return instructions