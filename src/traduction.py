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
tableGlobal = {}  #tabla en la que guardare el id y el $tn correspondiente   

def execute(input, textEdit): 
    global tableGlobal 
    tableGlobal.clear()   
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
                FunctionDeclaration_(b, ts)
            i += 1
    except:
        pass

def FunctionDeclaration_(b, ts):
    global augusTxt
    tsLocal = {}
    tsLocal.clear()
    augusTxt += f'{str(b.id)} :\n'
    #recorrer las listas de instrucciones
    i = 0
    while i < len(b.instructions):
        a = b.instructions[i]
        if isinstance(a, Declaration):
            Declaration_(a.listId, tsLocal)
        elif isinstance(a, Asignation):
            Asignation_(a, tsLocal)
        i += 1
    
    print(f"tsLocal: {str(tsLocal)}")

def Asignation_(b, ts):
    try:
        global contadorT, augusTxt
        res = valueExpression(b.expresion,ts)
        id = ts.get(b.id)
        if b.op == '=':
            #print(f"id: {id}")
            augusTxt += id
            augusTxt += ' = ' + str(res) + ' ;\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '+=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} + {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '-=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} - {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '*=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} * {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1    
        elif b.op == '/=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} / {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1  
        elif b.op == '%=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} % {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '<<=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} << {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '>>=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} >> {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '&=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} & {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '^=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} ^ {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif b.op == '|=':
            #print(f"id: {id}")
            augusTxt += f'{id} = {id} | {str(res)};\n'
            ts.setdefault(b.id, f'$t{str(contadorT)}')
            contadorT += 1
    except:
        print("Error semantico la varibale indicada no existe")

def Declaration_(b, ts):
    global augusTxt, contadorT
    for i in b:
        if isinstance(i, SingleDeclaration):
            res = valueExpression(i.val, ts)
            augusTxt += '$t'+ str(contadorT)
            augusTxt += ' = ' + str(res) + ' ;\n'
            ts.setdefault(i.id, f'$t{str(contadorT)}')
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
            ts.setdefault(i.id, f'$t{str(contadorT)}')
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
                    ts.setdefault(i.id, f'$t{str(contadorT)}')
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
                    ts.setdefault(i.id, f'$t{str(contadorT)}')
                contadorT += 1

def valueExpression(instruction, ts):
    global contadorT, augusTxt
    if isinstance(instruction, BinaryExpression):      
        num1 = valueExpression(instruction.op1, ts)
        num2 = valueExpression(instruction.op2, ts)
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
        #buscar en tabla local y en tabla global de lo contrario reportar error
        return ts.get(instruction.id)
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
        augusTxt += f' = {instruction.string} ;\n'
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

