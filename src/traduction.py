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


augusTxt = ''
contadorT = 0
semanticErrorList = []

def execute(input, textEdit):
    process(input)
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
    global augusTxt, contadorT
    for i in b:
        if isinstance(i, SingleDeclaration):
            res = valueExpression(i.val)
            augusTxt += '$t'+ str(contadorT)
            augusTxt += ' = ' + str(res) + '\n'
            contadorT += 1
 
def valueExpression(instruction):
    if isinstance(instruction, BinaryExpression):      
        num1 = valueExpression(instruction.op1)
        num2 = valueExpression(instruction.op2)
        try:
            if instruction.operator == Aritmetics.MAS:
                #augusTxt += '$t'+ str(contadorT)
                #augusTxt += ' = ' + str(res) + '\n'
                #contadorT += 1
                if isinstance((num1 + num2), str):
                    return str(num1 + num2)
                else:
                    return (num1 + num2)
            elif instruction.operator == Aritmetics.MENOS: return num1 - num2
            elif instruction.operator == Aritmetics.POR: return num1 * num2
            elif instruction.operator == Aritmetics.DIV: 
                if num2 != 0:
                    return num1 / num2
                else:
                    seob = seOb('Error Semantico: Division entre 0.', la, co)
                    semanticErrorList.append(seob)
                    return '#'
            elif instruction.operator == Aritmetics.MODULO: return num1 % num2
        except:
            print("trono")
            seob = seOb('Error Semantico: Tipos de datos en operacion aritmetica.', la, co)
            semanticErrorList.append(seob)
            return '#'
    elif isinstance(instruction, LogicAndRelational):
        val1 = valueExpression(instruction.op1)
        val2 = valueExpression(instruction.op2)
        try:
            if instruction.operator == LogicsRelational.MAYORQUE: 
                if val1 > val2: return 1
            elif instruction.operator == LogicsRelational.MENORQUE: 
                if val1 < val2: return 1
            elif instruction.operator == LogicsRelational.MAYORIGUAL: 
                if val1 >= val2: return 1
            elif instruction.operator == LogicsRelational.MENORIGUAL: 
                if val1 <= val2: return 1
            elif instruction.operator == LogicsRelational.IGUALQUE: 
                if val1 == val2: return 1
            elif instruction.operator == LogicsRelational.AND: 
                if val1 == 1 and val2 == 1: return 1
            elif instruction.operator == LogicsRelational.OR: 
                if val1 == 1 or val2 == 1: return 1
            elif instruction.operator == LogicsRelational.XOR: 
                if val1 == 1 ^ val2 == 1: return 1
            elif instruction.operator == LogicsRelational.DIFERENTE:
                if val1 != val2: return 1
        
            return 0
        except:
            se = seOb('Error : Tipos de datos en operacion relacional.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, Not):
        try:
            num1 = valueExpression(instruction.expression)
            if num1 >= 1: return 0
            else: return 1
        except:
            se = seOb(f'Error: Tipos de datos en la operacion Not {valueExpression(instruction.expression)}.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, Abs):
        try:
            return abs(valueExpression(instruction.expression))
        except:
            se = seOb(f'Error: Tipos de datos en la operacion Abs {valueExpression(instruction.expression)}.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, NegativeNumber):
        try:
            num1 = valueExpression(instruction.expression)
            if isinstance(num1, int) or isinstance(num1, float):
                return -1 * num1
            else:
                se = seOb(f'Error: No se puede aplicar negativo a {num1}.', instruction.line, instruction.column)
                semanticErrorList.append(se)
                return '#'
        except:
            se = seOb(f'Error: No se puede aplicar negativo a {num1}.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, Identifier):
        if ts.exist(instruction.id) == 1:
            return ts.get(instruction.id).valor
        else:
            se = seOb(f'Error Semantico: Variable  {instruction.id} no existe.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, Number):
        return instruction.val
    elif isinstance(instruction, Cast_):
        num1 = valueExpression(instruction.expression)
        #validations if num1 is array
        if isinstance(num1, int):
            if instruction.type == 'float':  return float(num1)
            elif instruction.type == 'char': return chr(num1)
            elif instruction.type == 'int': return num1

        elif isinstance(num1, float):
            if instruction.type == 'int':  return int(num1)
            elif instruction.type == 'char': return chr(int(num1))
            elif instruction.type == 'float': return num1               

        elif isinstance(num1, str):
            if instruction.type == 'int':  return ord(num1[0])
            elif instruction.type == 'float': return float(ord(num1[0]))
            elif instruction.type == 'char': return num1[0]
            else: return num1
    elif isinstance(instruction, String_):
        return instruction.string
    elif isinstance(instruction, ExpressionsDeclarationArray): return 'array'
    elif instruction == 'array': return 'array'
    elif isinstance(instruction, IdentifierArray):
        try:

            if ts.exist(instruction.id) == 0:
                se = seOb(f'Error Semantico: Variable  {instruction.id} no existe.', instruction.line,
                          instruction.column)
                semanticErrorList.append(se)
                return '#'
            sym = ts.get(instruction.id).valor
            if isinstance(sym, str):
                #print("es string")
                #es un string pero con posiciones
                if len(instruction.expressions) > 1:
                    #es decir que trar mas de un indice es decir  $t1[0][4]
                    #lo cual es error en un string 
                    #print(f"tamaño: {len(instruction.expressions)}")
                    se = seOb(f'Error: Indice {sym} del arreglo no existe.', instruction.line, instruction.column)
                    semanticErrorList.append(se)
                    return '#'
                else:
                    #print(f"valor del indice: {str(sym[valueExpression(instruction.expressions[0], ts,textEdit)])}")
                    return sym[valueExpression(instruction.expressions[0])]
            else:
                #print("no es  string")
                #manejo normal de array
                d = ast.literal_eval(str(sym))
                tmp = d
                i = 0
                while i < len(instruction.expressions)-1:
                    value = valueExpression(instruction.expressions[i])
                    tmp = tmp.setdefault(value, ts)
                    if tmp == None:
                        se = seOb(f'Error: Indice {value} del arreglo no existe.', instruction.line, instruction.column)
                        semanticErrorList.append(se)
                        return '#'
                    i += 1

                result = tmp.get(valueExpression(instruction.expressions[len(instruction.expressions)-1]))
                #print("Resultado de la consulta: " + str(result))
                return result
        except:
            se = seOb(f'Error: Indice {value} del arreglo no existe.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, ReadConsole):
        entrada = ''
        textoInicial = textEdit.toPlainText()
        textEdit.setFocus()
        cursorTemp = textEdit.textCursor()
        cursorTemp.setPosition(len(textoInicial))
        textEdit.setTextCursor(cursorTemp)
        while True:
            QtGui.QGuiApplication.processEvents()
            textoAct = textEdit.toPlainText()
            time.sleep(0.050)
            if len(textoAct) < len(textoInicial):  #verifico que el usuario no borre de ser asi vuelvo a setear todo como antes
                textoInicial.setPlainText(textoInicial)
                cursorTemp = textEdit.textCursor()
                cursorTemp.setPosition(len(textoInicial))
            elif len(textoAct) > len(textoInicial):    #si ya escribio verifico si ya tiene salto de linea
                if textoInicial == textoAct[0:len(textoInicial)]:
                    if textoAct[len(textoAct)-1] == "\n":
                        #print(f'textoInicial: {textoInicial}, textoAct: {textoAct}')
                        entrada = textoAct[len(textoInicial): len(textoAct)-1]
                        break
        
        #print(entrada)
        flo = entrada.split('.')
        if len(flo) > 1:
            return float(entrada)
        else:
            try:
                return int(flo[0])
            except:
                return entrada
    elif isinstance(instruction, RelationalBit):
        val1 = valueExpression(instruction.op1)
        val2 = valueExpression(instruction.op2)
        
        try:
            if instruction.operator == BitToBit.ANDBIT: 
                return (val1 & val2)
            elif instruction.operator == BitToBit.ORBIT: 
                return (val1 | val2)
            elif instruction.operator == BitToBit.XORBIT: 
                return (val1 ^ val2)
            elif instruction.operator == BitToBit.SHIFTI: 
                return (val1 << val2)
            elif instruction.operator == BitToBit.SHIFTD: 
                return (val1 >> val2)
        
            return 0
        except:
            se = seOb('Error : Tipos de datos en operacion bit a bit.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, NotBit):
        num1 = valueExpression(instruction.expression)
        if isinstance(num1, int) or isinstance(num1, float):
            return  ~num1
        else:
            se = seOb(f'Error: No se puede aplicar not bit  a {num1}.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif isinstance(instruction, ReferenceBit):
        val = valueExpression(instruction.expression)
        if val != '#':
            return val
        else:
            se = seOb(f'Error Referencia: variable {instruction.expression.id} no existe.', instruction.line, instruction.column)
            semanticErrorList.append(se)
            return '#'
    elif instruction == '#': return 0