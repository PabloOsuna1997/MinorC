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
tableTmp = {}  #tabla en la que guardare el id y el $tn correspondiente
ultimaPos = 0

def execute(input, textEdit):
    tableTmp.clear()
    process(input)
    print(str(tableTmp))
    return augusTxt

def process(instructions):
    try:
        i = 0
        while i < len(instructions):
            #isinstance verificar tipos 
            b = instructions[i]

            if isinstance(b, Declaration):
                Declaration_(b.listId)
            i += 1
    except:
        pass

def Declaration_(b):
    global augusTxt, contadorT, tableTmp
    for i in b:
        if isinstance(i, SingleDeclaration):
            res = valueExpression(i.val)
            augusTxt += '$t'+ str(contadorT)
            augusTxt += ' = ' + str(res) + ' ;\n'
            tableTmp.setdefault(i.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif isinstance(i, IdentifierArray):
            augusTxt += '$t' + str(contadorT)
            augusTxt += ' = array();\n'
            if len(i.expressions) == 1:
                res = valueExpression(i.expressions[0])
                if res != None:
                    if isinstance(res, int):
                        for z in range(0,res):
                            augusTxt += '$t' + str(contadorT)
                            augusTxt += f'[{str(z)}] = 0;\n'
                    else:
                        augusTxt += '$t' + str(contadorT)
                        augusTxt += f'[{str(res)}] = 0;\n'
            
            tableTmp.setdefault(i.id, f'$t{str(contadorT)}')
            contadorT += 1
        elif isinstance(i, DeclarationArrayInit):
            dime = valueExpression(i.dimentions[0])
            if dime > len(i.val.val)-1 :
                augusTxt += '$t'+ str(contadorT)
                augusTxt += ' = array();\n'
                res = valueExpression(i.val)

                for v in range(ultimaPos, dime):
                    augusTxt += f'$t{str(contadorT)}[{str(v)}]'
                    augusTxt += ' = 0 ;\n'

            
                tableTmp.setdefault(i.id, f'$t{str(contadorT)}')
                contadorT += 1
            else:
                print("error de dimensiones")

def valueExpression(instruction):
    global contadorT, augusTxt, tableTmp
    if isinstance(instruction, BinaryExpression):      
        num1 = valueExpression(instruction.op1)
        num2 = valueExpression(instruction.op2)
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
        num1 = valueExpression(instruction.op1)
        num2 = valueExpression(instruction.op2)
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
        
        num1 = valueExpression(instruction.expression)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = !{str(num1)} ;\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, NegativeNumber):        
        num1 = valueExpression(instruction.expression)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = {str(num1)} * -1 ;\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, Identifier): return tableTmp.get(instruction.id)
    elif isinstance(instruction, Number): return instruction.val
    elif isinstance(instruction, Cast_):
        num1 = valueExpression(instruction.expression)
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
    elif isinstance(instruction, String_): return instruction.string
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
        num1 = valueExpression(instruction.op1)
        num2 = valueExpression(instruction.op2)
        
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
        num1 = valueExpression(instruction.expression)
        augusTxt += '$t'+ str(contadorT)
        augusTxt += f' = ~{str(num1)};\n'
        contadorT += 1
        return f'$t{str(contadorT-1)}'
    elif isinstance(instruction, ReferenceBit):
        num1 = valueExpression(instruction.expression)
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
            augusTxt += ' = ' + str(valueExpression(instruction.val[i])) + ' ;\n'