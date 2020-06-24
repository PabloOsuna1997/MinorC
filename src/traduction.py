import grammar as g
import SymbolTable as TS
from semanticObject import *
from expresionsMinorC import *
from instructionsMinorC import *
import ast
import copy
import collections
import generator as g
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import time

augusTxt = 'main: \n'
contadorT = 0
semanticErrorList = []
ultimaPos = 0
tableGlobal = {}            #tabla en la que guardare el id y el $tn correspondiente
arrayTables = []            #guardare todas las tablas de simbolos, servira como una pila con append y pop
contadorEtiquetas = 0
contadorEtiquetasAux = 0
pasadas = 0

def execute(input, textEdit): 
    global tableGlobal 
    tableGlobal.clear()  
    arrayTables.append(tableGlobal) 
    process(input, tableGlobal)
    print(f"tsGlobal: {str(tableGlobal)}")
    return augusTxt

def process(instructions,ts):
    try:
        i = 0
        while i < len(instructions):
            #isinstance verificar tipos 
            b = instructions[i]

            if isinstance(b, Declaration):
                Declaration_(b.listId, ts)
            elif isinstance(b, FunctionDeclaration):
                if b.id == 'main':
                    FunctionDeclaration_(b, ts)
            i += 1
    except:
        pass

def FunctionDeclaration_(b, ts):   #ts siempre sera la tabla de simbolos del padre
    global augusTxt
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    if b.id != 'main':
        augusTxt += f'{str(b.id)} :\n'
    #recorrer las listas de instrucciones
    i = 0
    while i < len(b.instructions):
        a = b.instructions[i]
        if isinstance(a, Declaration):
            Declaration_(a.listId, tsLocal)
        elif isinstance(a, Asignation):
            Asignation_(a, tsLocal)
        elif isinstance(a, If):
            If_(a, tsLocal)
        elif isinstance(a, PrintF_):
            PrintF(a, tsLocal)
        elif isinstance(a, Label):
            augusTxt += f'{str(a.label)}:\n'
        elif isinstance(a, Goto):
           augusTxt += f'goto {str(a.label)};\n'
        elif isinstance(a, IncreDecre_Pre):
            increDecre(a, tsLocal, 1)
        elif isinstance(a, IncreDecre_Post):
            increDecre(a, tsLocal, 1)
        i += 1
    
    print(f"tsLocal: {str(tsLocal)}")
    arrayTables.pop()

def increDecre(b, ts, type_):
    global augusTxt, contadorT
    #type_ sera si es post o pre     
    if b.signo == '++':
        id = valueExpression(Identifier(b.id, 0, 0), ts)
        augusTxt += id
        augusTxt += f' = {str(id)} + 1;\n'
        arrayTables.pop()
        ts.setdefault(b.id, f'$t{str(id)}')
        arrayTables.append(ts)
        #contadorT += 1
    else:
        id = valueExpression(Identifier(b.id, 0, 0), ts)
        augusTxt += id
        augusTxt += f' = {str(id)} - 1;\n'
        arrayTables.pop()
        ts.setdefault(b.id, f'$t{str(id)}')
        arrayTables.append(ts)
        #contadorT += 1
    
def PrintF(b, ts):
    print("estoy en print")
    global contadorT, augusTxt
    #en la pos [0] siempre vendra la cadena "hola %d" etc..
    try:
        cadena = b.expressions[0].string
        cadena = cadena.split(' ')
        i = 0
        contadorValor = 1
        while i < len(cadena):
            if cadena[i] == '%d' or cadena[i] == '%s' or cadena[i] == '%f' or cadena[i] == '%c':
                cadena[i] = valueExpression(b.expressions[contadorValor], ts)
                contadorValor += 1
            i += 1
        #my_lst_str = ' '.join(map(str, cadena))        
        #print(f"printf: {my_lst_str}")
        for a in cadena:
            if a[0] == '$':
                augusTxt += f'print({str(a)});\n'       ## arreglar esto porque imprime ("$t8")
            else:
                augusTxt += f'print(\"{str(a)} \");\n'       ## arreglar esto porque imprime ("$t8")
    except:
        print("Error semantico en el print.")

def If_(b, tsPadre):
    global contadorT, augusTxt, contadorEtiquetas, contadorEtiquetasAux, arrayTables
    augusAuxAux = ''
    augusAux = ''
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    condition  = valueExpression(b.condition, tsPadre)
    augusTxt += f'if({str(condition)}) goto L{str(contadorEtiquetas)};\n'    
    augusAux += F'L{str(contadorEtiquetas)}:\n'                         #debajo del salto debo poner las instrucciones si son falsas
    augusAuxAux += augusTxt                                             #hacemos un backup de 
    augusTxt = ''
    contadorEtiquetas += 1
    i = 0                                                               #mandamos a hacer las instrucciones
    while i < len(b.instructions):
        a = b.instructions[i]
        if isinstance(a, Declaration):
            Declaration_(a.listId, tsLocal)
        elif isinstance(a, Asignation):
            Asignation_(a, tsLocal)
        elif isinstance(a, If):
            contadorEtiquetas += 1
            If_(a, tsLocal)
        elif isinstance(a, PrintF_):
            PrintF(a, tsLocal)
        elif isinstance(a, Label):
            augusTxt += f'{str(a.label)}:\n'
        elif isinstance(a, Goto):
           augusTxt += f'goto {str(a.label)};\n'
        elif isinstance(a, IncreDecre_Pre):
            increDecre(a, tsLocal, 1)
        elif isinstance(a, IncreDecre_Post):
            increDecre(a, tsLocal, 1)
        i += 1
    
                                                                       # termino de realizar etiquetas
    
    if len(b.ifElse) <= 0:
        contadorEtiquetasAux += 1

    augusTxt += f'goto L{len(b.ifElse) + contadorEtiquetasAux+1};\n'                             # termine de reconocer el FALSE Y INTERMACAMBIO LOS VALORES salto hasta la ultima etiquetas de if elses
    augusAux += augusTxt
    augusTxt = augusAuxAux                                              #le regresamos el contenido anterior
                                                                        #recorremos todos los ifelses
    if len(b.ifElse) > 0:                                               #hay if else's

        for a in b.ifElse:
            #if isinstance (a, list):                                    #aveces venia en lista dentro de listas
                #a = a[0]
            if isinstance(a, IfElse):
                condition  = valueExpression(a.condition, tsLocal)
                augusTxt += f'if({str(condition)}) goto L{str(contadorEtiquetas + contadorEtiquetasAux )};\n'
                #captura sus instrucciones
                augusAux += f'L{str(contadorEtiquetas + contadorEtiquetasAux)}:\n'
                augusAuxAux = ''
                augusAuxAux += augusTxt                                 #hacemos un backup de 
                augusTxt = ''
                contadorEtiquetas += 1
                                                                        #mandamos a hacer las instrucciones
                x = 0
                while x < len(a.instructions):
                    z = a.instructions[x]
                    if isinstance(z, Declaration):
                        Declaration_(z.listId, tsLocal)
                    elif isinstance(z, Asignation):
                        Asignation_(z, tsLocal)
                    elif isinstance(z, If):
                        contadorEtiquetas += 1
                        If_(a, tsLocal)
                    elif isinstance(z, PrintF_):
                        PrintF(z, tsLocal)
                    elif isinstance(z, Label):
                        augusTxt += f'{str(z.label)}:\n'
                    elif isinstance(z, Goto):
                        augusTxt += f'goto {str(z.label)};\n'
                    elif isinstance(z, IncreDecre_Pre):
                        increDecre(z, tsLocal, 1)
                    elif isinstance(z, IncreDecre_Post):
                        increDecre(z, tsLocal, 1)
        
                    x += 1
                                                                        # termino de realizar etiquetas
                
                augusAux += augusTxt
                augusAux += f'goto L{len(b.ifElse) + contadorEtiquetasAux+1};\n'                 #salto hasta la ultima etiquetas de if elses
                augusTxt = augusAuxAux                                  #le regresamos el contenido anterior 
            else:
                x = 0
                while x < len(a.instructions):
                    z = a.instructions[x]
                    if isinstance(z, Declaration):
                        Declaration_(z.listId, tsLocal)
                    elif isinstance(z, Asignation):
                        Asignation_(z, tsLocal)
                    elif isinstance(z, If):
                        If_(z, tsLocal)
                    elif isinstance(z, PrintF_):
                        PrintF(z, tsLocal)
                    elif isinstance(z, Label):
                        augusTxt += f'{str(z.label)}:\n'
                    elif isinstance(z, Goto):
                        augusTxt += f'goto {str(z.label)};\n'
                    elif isinstance(z, IncreDecre_Pre):
                        increDecre(z, tsLocal, 1)
                    elif isinstance(z, IncreDecre_Post):
                        increDecre(z, tsLocal, 1)
        
                    
                    x += 1
                augusTxt += f'goto L{len(b.ifElse) + contadorEtiquetasAux+1};\n'
        augusTxt += f'goto L{len(b.ifElse) + contadorEtiquetasAux + 1};\n'
        augusTxt += augusAux
        augusTxt += f'L{str(len(b.ifElse) + contadorEtiquetasAux+1)}:\n'
    else:        
        augusTxt += f'goto L{len(b.ifElse) + contadorEtiquetasAux+1};\n'
        augusTxt += augusAux
        augusTxt += f'L{str(len(b.ifElse) + contadorEtiquetasAux+1)}:\n'
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    arrayTables.pop()      #eliminamos la ts

def Asignation_(b, ts):
    try:
        if isinstance(b.expresion, IncreDecre_Post):
            increDecreAsignation(b.expresion, ts, valueExpression(Identifier(b.id,0,0), ts), b.id)
        elif isinstance(b.expresion, IncreDecre_Pre):
            increDecreAsignation(b.expresion, ts, valueExpression(Identifier(b.id,0,0), ts), b.id)
        else:
            global contadorT, augusTxt, arrayTables
            res = valueExpression(b.expresion,ts)
            id = valueExpression(Identifier(b.id,0,0), ts)
            if id != None:
                if b.op == '=':
                    #print(f"id: {id}")
                    augusTxt += id
                    augusTxt += ' = ' + str(res) + ' ;\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '+=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} + {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '-=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} - {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '*=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} * {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '/=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} / {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '%=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} % {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '<<=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} << {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '>>=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} >> {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '&=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} & {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '^=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} ^ {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                elif b.op == '|=':
                    #print(f"id: {id}")
                    augusTxt += f'{id} = {id} | {str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(b.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
            else:
                print("Error semantico la varibale indicada no existe asignacion")
    except:
        print("Error semantico la varibale indicada no existe except asignacion")

def Declaration_(b, ts):
    global augusTxt, contadorT, arrayTables
    for i in b:
        if isinstance(i, SingleDeclaration):
            if isinstance(i.val, IncreDecre_Post):
                increDecreAsignation(i.val, ts, f'$t{str(contadorT)}', i.id)
                contadorT+=1
            elif isinstance(i.val, IncreDecre_Pre):
                increDecreAsignation(i.val, ts, f'$t{str(contadorT)}', i.id)
                contadorT += 1
            else:
                res = valueExpression(i.val, ts)
                augusTxt += '$t'+ str(contadorT)
                augusTxt += ' = ' + str(res) + ' ;\n'
                arrayTables.pop()
                ts.setdefault(i.id, f'$t{str(contadorT)}')
                arrayTables.append(ts)
                contadorT += 1
        elif isinstance(i, IdentifierArray):
            augusTxt += '$t' + str(contadorT)
            augusTxt += ' = array();\n'
            if len(i.expressions) == 1:
                res = valueExpression(i.expressions[0],ts)
                if res != None:
                    if isinstance(res, int):
                        for z in range(0,res):
                            augusTxt += '$t' + str(contadorT)
                            augusTxt += f'[{str(z)}] = 0;\n'
                    else:
                        augusTxt += '$t' + str(contadorT)
                        augusTxt += f'[{str(res)}] = 0;\n'
            arrayTables.pop()
            ts.setdefault(i.id, f'$t{str(contadorT)}')
            arrayTables.append(ts)
            contadorT += 1
        elif isinstance(i, DeclarationArrayInit):
            dime = valueExpression(i.dimentions[0], ts)
            if dime != None:
                if dime > len(i.val.val)-1 :
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += ' = array();\n'
                    res = valueExpression(i.val, ts)
                    for v in range(ultimaPos, dime):
                        augusTxt += f'$t{str(contadorT)}[{str(v)}]'
                        augusTxt += ' = 0 ;\n'            
                    arrayTables.pop()
                    ts.setdefault(i.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                    contadorT += 1
                
                else:
                    print("Error semantico, dimensiones incorrectas")
            else:
                augusTxt += '$t'+ str(contadorT)
                augusTxt += ' = array();\n'
                res = valueExpression(i.val, ts)
                if isinstance(res, str):
                    ts.setdefault(i.id, f'{str(res)}')
                else:
                    arrayTables.pop()
                    ts.setdefault(i.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                contadorT += 1

def valueExpression(instruction, ts):
    global contadorT, augusTxt, arrayTables
    if isinstance(instruction, BinaryExpression):      
        num1 = valueExpression(instruction.op1, ts)
        num2 = valueExpression(instruction.op2, ts)
        if num1 != None and num2 != None:
            try:
                if instruction.operator == Aritmetics.MAS:
                    
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = {str(num1)} + {str(num2)} ;\n'
                    contadorT += 1
                    return f'$t{str(contadorT-1)}'

                elif instruction.operator == Aritmetics.MENOS: 
                    
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = {str(num1)} - {str(num2)} ;\n'
                    contadorT += 1
                    return f'$t{str(contadorT-1)}'

                elif instruction.operator == Aritmetics.POR:
                    
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = {str(num1)} * {str(num2)} ;\n'
                    contadorT += 1
                    return f'$t{str(contadorT-1)}'

                elif instruction.operator == Aritmetics.DIV: 
                    
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = {str(num1)} / {str(num2)} ;\n'
                    contadorT += 1
                    return f'$t{str(contadorT-1)}'

                elif instruction.operator == Aritmetics.MODULO: 
                    
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = {str(num1)} % {str(num2)} ;\n'
                    contadorT += 1
                    return f'$t{str(contadorT-1)}'

            except:
                print("trono")
                seob = seOb('Error Semantico: Tipos de datos en operacion aritmetica.', 0, 0)
                semanticErrorList.append(seob)
                return '#'
        else:
            #retornar alfgo para que no traduzca mas 
            print("Error semantico la varibale indicada no existe suma NONE")
    elif isinstance(instruction, LogicAndRelational):
        num1 = valueExpression(instruction.op1, ts)
        num2 = valueExpression(instruction.op2, ts)
        try:
            if instruction.operator == LogicsRelational.MAYORQUE: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} > {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.MENORQUE: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} < {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.MAYORIGUAL: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} >= {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.MENORIGUAL: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} <= {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.IGUALQUE: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} == {str(num2)} ;\n'
                contadorT += 1

                return f'$t{str(contadorT-1)}'
            elif instruction.operator == LogicsRelational.AND: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} && {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.OR: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} || {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'

            elif instruction.operator == LogicsRelational.XOR: 
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} ^ {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'
                
            elif instruction.operator == LogicsRelational.DIFERENTE:
                augusTxt += '$t'+ str(contadorT)
                augusTxt += f' = {str(num1)} != {str(num2)} ;\n'
                contadorT += 1
                return f'$t{str(contadorT-1)}'
        
            return 0
        except:
            se = seOb('Error : Tipos de datos en operacion relacional.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, Not):
        
        num1 = valueExpression(instruction.expression, ts)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = !{str(num1)} ;\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, NegativeNumber):        
        num1 = valueExpression(instruction.expression, ts)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = {str(num1)} * -1 ;\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, Identifier): 
        #si no encuentra la variable en la ts actual, buscarla en las demas ts que estan en la pila
        tablesAux = arrayTables[:]
        tablesAux.reverse()
        for i in tablesAux:
            if instruction.id in i:
                return i.get(instruction.id)
        return None
    elif isinstance(instruction, Number): return instruction.val
    elif isinstance(instruction, Cast_):
        num1 = valueExpression(instruction.expression, ts)
        if instruction.type == 'float':  
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = (float){str(num1)};\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.type == 'char':
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = (char){str(num1)};\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.type == 'int': 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = (int){str(num1)};\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        else:
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = (otro){str(num1)};\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, String_):
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = \"{instruction.string}\" ;\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, ExpressionsDeclarationArray): return 'array'
    elif instruction == 'array': return 'array'
    elif isinstance(instruction, IdentifierArray):
        #hacer un for para recorrer las expresiones -> entiendase los arreglos
        print(f'{str(instruction.id)}')
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = array();\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, ReadConsole): print("scanf")
    elif isinstance(instruction, RelationalBit):
        num1 = valueExpression(instruction.op1, ts)
        num2 = valueExpression(instruction.op2, ts)
        
        if instruction.operator == BitToBit.ANDBIT: 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = {str(num1)} & {str(num2)} ;\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.operator == BitToBit.ORBIT: 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = {str(num1)} | {str(num2)} ;\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.operator == BitToBit.XORBIT: 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = {str(num1)} ^ {str(num2)} ;\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.operator == BitToBit.SHIFTI: 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = {str(num1)} << {str(num2)} ;\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
        elif instruction.operator == BitToBit.SHIFTD: 
            augusTxt += '$t'+ str(contadorT)
            augusTxt += f' = {str(num1)} >> {str(num2)} ;\n'
            contadorT += 1
            return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, NotBit):
        num1 = valueExpression(instruction.expression, ts)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = ~{str(num1)};\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, ReferenceBit):
        num1 = valueExpression(instruction.expression, ts)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = &{str(num1)};\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif instruction == '#': return 0   #ssirve para las declaraciones globales que no son inicializadas
    elif isinstance(instruction, InitializationArray):
        print("recorrer la inicializacion")
        global ultimaPos
        for i in range(0, len(instruction.val)):
            ultimaPos += 1
            augusTxt += f'$t{str(contadorT)}[{str(i)}]'
            augusTxt += ' = ' + str(valueExpression(instruction.val[i], ts)) + ' ;\n'
    elif isinstance(instruction, Scanf):
        augusTxt += f'$t{str(contadorT)} = read();\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'

def increDecreAsignation(instruction, ts, idPadre, VariableAlto):
    global augusTxt,arrayTables,contadorT
    if isinstance(instruction, IncreDecre_Post):
        #primero lo agrego
        id = valueExpression(Identifier(instruction.id, 0, 0), ts)  ##id de variable afectada   -> a++;  -> $t0
        augusTxt += f'{idPadre}'
        augusTxt += f' = {str(id)};\n'
        arrayTables.pop()
        ts.setdefault(VariableAlto, f'{idPadre}')
        arrayTables.append(ts)
        #ahora incremento
        augusTxt += id
        if instruction.signo == '++':
            augusTxt += f' = {str(id)} + 1;\n'
        else:
            augusTxt += f' = {str(id)} - 1;\n'
        arrayTables.pop()
        ts.setdefault(instruction.id, f'{id}')
        arrayTables.append(ts)
    else:
        #primero incremento        
        id = valueExpression(Identifier(instruction.id, 0, 0), ts)
        augusTxt += id
        if instruction.signo == '++':
            augusTxt += f' = {str(id)} + 1;\n'
        else:
            augusTxt += f' = {str(id)} - 1;\n'
        arrayTables.pop()
        ts.setdefault(instruction.id, f'{id}')
        arrayTables.append(ts)
        #despues lo agrego
        augusTxt += f'{idPadre}'
        augusTxt += f' = {str(id)};\n'
        arrayTables.pop()
        ts.setdefault(VariableAlto, f'{idPadre}')
        arrayTables.append(ts)

        