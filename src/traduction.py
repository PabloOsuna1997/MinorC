import grammar as g
import SymbolTable as TS
import functionTable as fTS
from semanticObject import *
from expresionsMinorC import *
from instructionsMinorC import *
import ast
import copy
import collections
import generatorMinorC as g
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import time

tsFunciones = {}
augusTxt = 'main: \n'
augusTxtAuxVar = ''
augusTxtAuxJUMPS  = '\n'
augusTxtCalls = ''      #texto auxiliar para las llamadas
contadorT = 0
semanticErrorList = []
ultimaPos = 0
tableGlobal = {}            #tabla en la que guardare el id y el $tn correspondiente
arrayTables = []            #guardare todas las tablas de simbolos, servira como una pila con append y pop
contadorEtiquetas = 0
contadorEtiquetasAux = 0
pasadas = 0
caseAnt = None
contadorCalls = 0       #para nombrar etiquetas de salto
contadorParams = 0      #variables $a0

def execute(input, textEdit):
    global tableGlobal, contadorParams, contadorT, contadorEtiquetas, contadorEtiquetasAux, contadorCalls, tsFunciones, augusTxtAuxJUMPS
    tableGlobal.clear()
    tsFunciones = {}
    tsFunciones = fTS.functionsTable()
    contadorParams = 0
    contadorT = 0
    contadorEtiquetas = 0
    contadorEtiquetasAux = 0
    contadorCalls = 0
    arrayTables.append(tableGlobal)

    augusTxtAuxJUMPS = ''
    augusTxtAuxJUMPS += 'manejador:\n'
    augusTxtAuxJUMPS += '$s5 = $s0[$ra];\n'
    augusTxtAuxJUMPS += '$ra = $ra - 1;\n'
    process(input, tableGlobal)
    print(f"tsGlobal: {str(tableGlobal)}")
    return augusTxt

def process(instructions,ts):
    #try:
        global augusTxt, augusTxtCalls, augusTxtAuxVar, contadorParams, augusTxtAuxJUMPS
        #primera pasada capturando las funciones, metodos y variables globales
        contadorParams = 0
        i = 0
        while i < len(instructions):
            #isinstance verificar tipos
            b = instructions[i]

            if isinstance(b, Declaration):
                Declaration_(b.listId, ts)
            elif isinstance(b, FunctionDeclaration):
                if b.id != 'main':                    
                    augusTxtAuxVar = augusTxt       #back de augutxt
                    augusTxt = ''
                    getFunctions(b, ts)
                    augusTxt += 'goto manejador;\n'
                    augusTxtCalls += augusTxt
                    augusTxt = augusTxtAuxVar
            elif isinstance(b, DeclarationStruct):
                DeclarationStruct_(b, ts)
            i += 1

        #capturo instrucciones del main  
        augusTxt += '$ra = -1;  #apuntador de pila de llamadas\n'
        augusTxt += '$s0 = array(); #pila de llamadas\n'
        #en mi etiqueta manejoador siempre restara tope de pila
        i = 0
        while i < len(instructions):
            #isinstance verificar tipos
            b = instructions[i]

            if isinstance(b, FunctionDeclaration):
                if b.id == 'main':
                    contadorParams = 0
                    FunctionDeclaration_(b, ts)
                    augusTxt += 'goto FINAL_AUGUS;\n'
                    #demas funciones
                    augusTxt += augusTxtCalls
                    augusTxt += '\n\n'
                    augusTxt += augusTxtAuxJUMPS
                    augusTxt += 'FINAL_AUGUS:'

            i += 1
            
    #except:
        #pass

def DeclarationStruct_(b, ts):
    id = valueExpression(Identifier(b.id, 0, 0), ts)
    print("declaracion de structs")

def getFunctions(b, ts):    #POSEE INSTRUCCIONES INTERNAS ACTUALIZAR CON TODAS           #seteo los parametros dentro de la funcion y capturo sus instrucciones
    global augusTxt, contadorParams, contadorT
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    parametros = []
    #debo guardar la funcion en la tabla de simbolos asi cada vez que la llame le asigno el valor a la misva variable
    # guardar en ts mi funcion
    if isinstance(b.params, list):
        parametros[:] = []
        for param in b.params:
            parametros.append((f'$a{str(contadorParams)}', param.id))
            contadorParams += 1

        #insertar en mi tabla de simbolos de funciones
        funcion = fTS.Symbol(b.id, b.type_, parametros)
        tsFunciones.add(funcion)
    #recorrer las listas de instrucciones
    else:
        parametros[:] = []
        #insertar en mi tabla de simbolos de funciones
        funcion = fTS.Symbol(b.id, b.type_, parametros)
        tsFunciones.add(funcion)

    #asignacion del valor a mi parametro
    if b.id != 'main':
        augusTxt += f'{str(b.id)} :\n'              #etiqueta de nombre de mi funcion
        if isinstance(b.params, list):
            i = 0
            while i < len(b.params):
                #conforme el contador de parametros
                augusTxt += '$t'+ str(contadorT)
                augusTxt += ' = ' + str(f'{parametros[i][0]}') + ' ;\n'
                arrayTables.pop()
                tsLocal.setdefault(parametros[i][1], f'$t{str(contadorT)}')         #agrego a mi tabla de simbolos local de cada metodo los parametros correspondientes
                arrayTables.append(tsLocal)
                contadorT += 1          #aumento contador de tmp   
                i += 1

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
        elif isinstance(a, For):
            For_(a, tsLocal)
        elif isinstance(a, While_):
            While__(a, tsLocal)
        elif isinstance(a, DoWhile_):
            DoW(a, tsLocal)
        elif isinstance(a, Switch_):
            Switch(a, tsLocal)
        elif isinstance(a, CallFunction):
            CallF(a, tsLocal)
        elif isinstance(a, AsignationArray):
            AsignationArray_(a, tsLocal)
        i += 1

    print(f"tsLocal funcion {b.id}: {str(tsLocal)}")
    #antes de sacar la tabla inserto todo el demas texto de las funciones.
    #capturar las instrucciones de los demas metodos
    if (b.id == 'main'):
        contadorParams = 0  #reestablezco el valor de los parametros
    arrayTables.pop()

def FunctionDeclaration_(b, ts): #POSEE INSTRUCCIONES INTERNAS ACTUALIZAR CON TODAS    #ts siempre sera la tabla de simbolos del padre
    global augusTxt, contadorParams, contadorT
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
        elif isinstance(a, For):
            For_(a, tsLocal)
        elif isinstance(a, While_):
            While__(a, tsLocal)
        elif isinstance(a, DoWhile_):
            DoW(a, tsLocal)
        elif isinstance(a, Switch_):
            Switch(a, tsLocal)
        elif isinstance(a, CallFunction):
            CallF(a, tsLocal)
        elif isinstance(a, AsignationArray):
            AsignationArray_(a, tsLocal)
        i += 1

    print(f"tsLocal funcion {b.id}: {str(tsLocal)}")
    if (b.id == 'main'):
        contadorParams = 0  #reestablezco el valor de los parametros
    arrayTables.pop()

def CallF(b, ts):                   #consulto los parametros de cada funcion y los asigno
    global augusTxtCalls, contadorCalls, augusTxt, contadorParams, arrayTables, augusTxtAuxJUMPS
    try:
        if len(b.params) != 0:  #parametros del metodo a llamar
            #debemos crear las variable $an correspondientes
            #mando a traer sus parametros a mi tabla de simbolos
            parametros = tsFunciones.get(b.id).parametros
            i = 0
            while i < len(b.params):
                a = b.params[i]
                res = valueExpression(a, ts)
                augusTxt += f'{parametros[i][0]}'
                augusTxt += ' = ' + str(res) + ' ;\n'
                # paso por referencia
                if isinstance(a, ReferenceBit):
                    augusTxt += f'{str(res)} = &{str(parametros[i][0])};\n'
                i += 1

        #creo las instrucciones de la funcion
        augusTxt += f'$ra = $ra + 1;\n'
        augusTxt += f'$s0[$ra] = {contadorCalls};\n'
        augusTxt += f'goto {str(b.id)};\n'        #etiqueta al metodo para ejecutar ej: goto suma;
        #declaro una etiqueta para que el metodo regrese
        augusTxt += f'regreso{str(contadorCalls)}:\n'           #lacaionamos el ra con la etiqueta de regreso
        #if contadorCalls > 0:
            #augusTxt += f'$ra = $ra + {str(contadorCalls)};\n'
        #else:
            #augusTxt += f'$ra = $ra + {str(contadorCalls+1)};\n'

        #agregamos a nuestro manejador de saltos
        augusTxtAuxJUMPS += f'if ( $s5 == {str(contadorCalls)}) goto regreso{str(contadorCalls)};\n'
        contadorCalls += 1
    except:
        print("Error Semantico: No existe el metodo indicado.")

def Switch(b, ts):
    global contadorT, augusTxt, arrayTables, contadorEtiquetas, contadorEtiquetasAux, caseAnt
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    #valuar la expresion
    contadorCase = 0
    caseAnt = None
    for i in b.listaCases:
        if contadorCase > 0:
            #if caseAnt.break_ != 0:
            exp = valueExpression(LogicAndRelational(b.expresion, i.expresion, LogicsRelational.IGUALQUE, 0, 0), ts)
            augusTxt += f'if({str(exp)}) goto sL{str(contadorEtiquetas)};\n'
            augusTxt += f'goto sL{str(contadorEtiquetas + 1)};\n'
        else:
            exp = valueExpression(LogicAndRelational(b.expresion, i.expresion, LogicsRelational.IGUALQUE, 0, 0), ts)
            augusTxt += f'if({str(exp)}) goto sL{str(contadorEtiquetas)};\n'
            augusTxt += f'goto sL{str(contadorEtiquetas + 1)};\n'

        contaAux = contadorEtiquetas + 1
        augusTxt += F'sL{str(contadorEtiquetas)}:\n'
        contadorEtiquetas += 2
        processInstructions(i.instructions, tsLocal)
        #if i.break_ != 0:
        augusTxt += '##--##\n'        #salto hacia el final
        augusTxt += F'sL{str(contaAux)}:\n'
        contadorCase += 1
        caseAnt = i                 #guardo en case anterior

    if isinstance(b.default, Default_):
        #existe default
        augusTxt += F'sLDefault:\n'
        #contadorEtiquetas += 2
        processInstructions(b.default.instructions, tsLocal)
        augusTxt += '##--##\n'        #salto hacia el final
        #augusTxt += F'sL{str(contaAux)}:\n'


    import re
    augusTxt = re.sub('##--##', f'goto sL{str(contadorEtiquetas)};\n', augusTxt, flags=re.IGNORECASE)
    augusTxt += f'sL{str(contadorEtiquetas)}:\n'
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    arrayTables.pop()

def DoW(b, ts):
    print("do while")
    global contadorT, augusTxt, arrayTables, contadorEtiquetas, contadorEtiquetasAux
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    augusTxt += F'dwL{str(contadorEtiquetas)}:\n'
    contaAuxAUx = contadorEtiquetas
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    processInstructions(b.instructions, tsLocal)
    condition = valueExpression(b.condition, tsLocal)
    augusTxt += f'if({str(condition)}) goto dwL{str(contadorEtiquetas)};\n'   #$Tn
    augusTxt += f'goto dwL{str(contadorEtiquetas + 1)};\n'  # $Tn+1
    augusTxt += F'dwL{str(contadorEtiquetas)}:\n'
    augusTxt += f'goto dwL{str(contaAuxAUx)};\n'
    augusTxt += f'dwL{str(contadorEtiquetas + 1)}:\n'
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    arrayTables.pop()

def While__(b, ts):
    global contadorT, augusTxt, arrayTables, contadorEtiquetas, contadorEtiquetasAux

    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    augusTxt += F'wL{str(contadorEtiquetas)}:\n'
    contaAuxAUx = contadorEtiquetas
    contadorEtiquetas += 1
    condition = valueExpression(b.condition, tsLocal)
    augusTxt += f'if({str(condition)}) goto wL{str(contadorEtiquetas)};\n'   #$Tn
    augusTxt += f'goto wL{str(contadorEtiquetas+1)};\n'                      #$Tn+1
    augusTxt += F'wL{str(contadorEtiquetas)}:\n'                             #Tn:
    contaAux = contadorEtiquetas+1
    contadorEtiquetas += 2
    processInstructions(b.instructions, tsLocal)
    augusTxt += f'goto wL{str(contaAuxAUx)};\n'                  #contador del goto inicial
    contadorEtiquetas = contadorEtiquetas + 1
    contadorEtiquetasAux = contadorEtiquetas
    augusTxt += F'wL{str(contaAux)}:\n'
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    arrayTables.pop()

def For_(b, ts):
    global contadorT, augusTxt, arrayTables, contadorEtiquetas, contadorEtiquetasAux

    #creamos una nueva tabla de simbolos
    tsLocal = {}
    tsLocal.clear()
    arrayTables.append(tsLocal)
    Declaration_(b.declaration.listId, tsLocal)
    augusTxt += F'fL{str(contadorEtiquetas)}:\n'
    contaAuxAUx = contadorEtiquetas
    contadorEtiquetas += 1
    condition = valueExpression(b.condition, tsLocal)
    augusTxt += f'if({str(condition)}) goto fL{str(contadorEtiquetas)};\n'   #$Tn
    augusTxt += f'goto fL{str(contadorEtiquetas+1)};\n'                      #$Tn+1
    augusTxt += F'fL{str(contadorEtiquetas)}:\n'                             #Tn:
    contaAux = contadorEtiquetas+1                                          #aux = Tn+1
    #instrucciones verdaderas
    #b.instructions
    contadorEtiquetas += 2 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
    processInstructions(b.instructions, tsLocal)
    #incremento
    if isinstance(b.increDecre, IncreDecre_Post):
        increDecreAsignation(b.increDecre, tsLocal, valueExpression(Identifier(b.increDecre.id, 0, 0), ts), b.increDecre.id)
    elif isinstance(b.increDecre, IncreDecre_Pre):
        increDecreAsignation(b.expresion, tsLocal, valueExpression(Identifier(b.increDecre.id, 0, 0), ts), b.increDecre.id)
    augusTxt += f'goto fL{str(contaAuxAUx)};\n'                  #contador del goto inicial
    contadorEtiquetas = contadorEtiquetas + 1
    contadorEtiquetasAux = contadorEtiquetas
    augusTxt += F'fL{str(contaAux)}:\n'
    contadorEtiquetas += 1
    contadorEtiquetasAux = contadorEtiquetas
    arrayTables.pop()

def processInstructions(b, tsLocal):    #POSEE INSTRUCCIONES INTERNAS ACTUALIZAR CON TODAS 
    global augusTxt
    i = 0
    while i < len(b):
        a = b[i]
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
        elif isinstance(a, For):
            For_(a, tsLocal)
        elif isinstance(a, While_):
            While__(a, tsLocal)
        elif isinstance(a, DoWhile_):
            DoW(a, tsLocal)
        elif isinstance(a, Switch_):
            Switch(a, tsLocal)
        elif isinstance(a, CallFunction):
            CallF(a, tsLocal)
        elif isinstance(a, AsignationArray):
            AsignationArray_(a, tsLocal)
        i += 1

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
    #print("estoy en print")
    global contadorT, augusTxt
    #en la pos [0] siempre vendra la cadena "hola %d" etc..
    try:
        cadena = b.expressions[0].string
        cadena = cadena.replace('%d', '%d ')
        cadena = cadena.replace('%c', '%c ')
        cadena = cadena.replace('%f', '%f ')
        cadena = cadena.replace('%s', '%s ')
        cadena = cadena.replace('%i', '%i ')
        cadena = cadena.replace('\\n', ' \\n ')

        cadena = cadena.split(' ')
        i = 0
        contadorValor = 1
        while i < len(cadena):
            if cadena[i] == '%d' or cadena[i] == '%s' or cadena[i] == '%f' or cadena[i] == '%c'  or cadena[i] == '%i'  :
                cadena[i] = valueExpression(b.expressions[contadorValor], ts)
                contadorValor += 1
            i += 1
        #my_lst_str = ' '.join(map(str, cadena))
        #print(f"printf: {my_lst_str}")
        for a in cadena:
            if a != '':
                if a[0] == '$':
                    augusTxt += f'print({str(a)});\n'       ## arreglar esto porque imprime ("$t8")
                else:
                    if a != '\\n':
                        augusTxt += f'print(\" {str(a)} \");\n'       ## arreglar esto porque imprime ("$t8")
                    else:
                        augusTxt += f'print(\"\\n\");\n'  ## para no sumarle el espacio en el \n
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
    augusTxt += f'if({str(condition)}) goto iL{str(contadorEtiquetas)};\n'
    if len(b.ifElse) == 0:
        #es solo un if
        augusTxt += f'goto iL{str(contadorEtiquetas+1)};\n'
        augusTxt += f'iL{str(contadorEtiquetas)}:\n'
        contaAux = contadorEtiquetas+1
        contadorEtiquetas += 2 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
        processInstructions(b.instructions, tsLocal)
        augusTxt += f'iL{str(contaAux)}:\n'
        contadorEtiquetas += 1
        contadorEtiquetasAux = contadorEtiquetas
        arrayTables.pop()
    elif len(b.ifElse) == 1:
        if isinstance(b.ifElse[0],Else):
            #else
            augusTxt += f'goto iL{str(contadorEtiquetas+1)};\n'
            augusTxt += f'iL{str(contadorEtiquetas)}:\n'
            contaAux = contadorEtiquetas+1
            contadorEtiquetas += 2 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
            processInstructions(b.instructions, tsLocal)
            #########################################################
            augusAuxAux = augusTxt          #guardo lo que llevo
            augusTxt = ''
            #empiezo a almacenar el else en  una tmp
            augusAux += f'iL{str(contaAux)}:\n'
            #etiquetas falsas
            contaAux = contadorEtiquetas
            processInstructions(b.ifElse[0].instructions, tsLocal)
            augusTxt += f'goto iL{str(contadorEtiquetas)};\n'
            augusTxt += f'iL{str(contadorEtiquetas)}:\n'
            augusAux += augusTxt
            #########################################################
            #cuando regreso de todas las instruccionies del else ya lo incorporo a mi texto original pero antes pongo goto del if verdadero
            augusTxt = augusAuxAux
            augusTxt += f'goto iL{str(contadorEtiquetas)};\n'
            augusTxt += augusAux
            contadorEtiquetas += 1
            contadorEtiquetasAux = contadorEtiquetas
            arrayTables.pop()
        else:
            # viene un unico else if
            condition  = valueExpression(b.ifElse[0].condition, tsPadre)
            augusTxt += f'if({str(condition)}) goto iL{str(contadorEtiquetas+1)};\n'
            augusAuxAux = augusTxt                  #guardo contenido actual
            contaAux = contadorEtiquetas+1          #etiqueta a donde debo saltar de ser falsa el segundo if
            augusAuxIf = f'iL{str(contadorEtiquetas)}:\n'
            augusTxt = ''
            contadorEtiquetas += 2 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
            processInstructions(b.instructions, tsLocal)  #ejecutar instrucciones verdaderas
            augusAuxIf += augusTxt

            augusAux_Else = f'iL{str(contaAux)}:\n'         #instrucciones del elseif
            augusTxt = ''
            processInstructions(b.ifElse[0].instructions, tsLocal)  #ejecutar instrucciones verdaderas
            augusAux_Else += augusTxt
            augusAux_Else += f'goto iL{str(contadorEtiquetas)};\n'
            augusTxt = augusAuxAux

            augusTxt += f'goto iL{str(contadorEtiquetas)};\n'   ### si ninguna se cumple se sale

            augusTxt += augusAuxIf
            augusTxt += f'goto iL{str(contadorEtiquetas)};\n'
            augusTxt += augusAux_Else
            augusTxt += f'iL{str(contadorEtiquetas)}:\n'
            contadorEtiquetas += 1
            contadorEtiquetasAux = contadorEtiquetas
            arrayTables.pop()
    else:
        #vienen if else a morir y else
        #1 traigo las instrucciones verdaderas del primer if
        augusAuxAux = augusTxt
        augusTxt = ''
        augusTxt += f'iL{str(contadorEtiquetas)}:\n'
        contaAux = contadorEtiquetas
        contadorEtiquetas += 1 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
        processInstructions(b.instructions, tsLocal)  #ejecutar instrucciones verdaderas
        augusAuxIf1 = augusTxt      #pendiente salto de fin
        augusAuxIf1 += '##--##\n'     #posteriormente reemplazare eso por el ultimo salto
        augusTxt = augusAuxAux
        for a in b.ifElse:
            if isinstance(a, IfElse):
                condition  = valueExpression(a.condition, tsPadre)
                augusTxt += f'if({str(condition)}) goto iL{str(contadorEtiquetas)};\n'
                augusAuxIf1 += f'iL{str(contadorEtiquetas)}:\n'
                augusAuxAux = augusTxt
                augusTxt = ''
                contadorEtiquetas += 1 #aumentamos porque las demas instrucciones tambien crearan etiquetas si no sobre escribiran la que ya tenia
                processInstructions(a.instructions, tsLocal)
                augusAuxIf1 += augusTxt      #pendiente salto de fin
                augusAuxIf1 += '##--##'     #posteriormente reemplazare eso por el ultimo salto
                augusTxt = augusAuxAux
            else:
                augusTxt += f'goto iL{str(contadorEtiquetas)};\n'
                augusTxt += f'iL{str(contadorEtiquetas)}:\n'
                contadorEtiquetas += 1
                processInstructions(a.instructions, tsLocal)
                augusTxt += f'goto iL{str(contadorEtiquetas)};\n'

        import re
        augusAuxIf1 = re.sub('##--##', f'goto iL{str(contadorEtiquetas)};\n', augusAuxIf1, flags=re.IGNORECASE)
        augusTxt += augusAuxIf1
        augusTxt += f'iL{str(contadorEtiquetas)}:\n'
        contadorEtiquetas += 1
        contadorEtiquetasAux = contadorEtiquetas
        arrayTables.pop()

def AsignationArray_(b, ts):
    global contadorT, augusTxt
    print("asignacion de valor a array")
    id = valueExpression(Identifier(b.id, 0, 0), ts)
    #contateno los corchetes
    aux = ''
    aux += id
    for i in b.corchetes:
        aux += f'[{str(valueExpression(i,ts))}]'
    aux += f' = {str(valueExpression(b.expresion, ts))};\n'
    augusTxt += aux
    arrayTables.pop()
    ts.setdefault(b.id, f'{str(id)}')
    arrayTables.append(ts)
    contadorT += 1

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
                    ts.setdefault(b.id, f'{str(id)}')
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
            elif isinstance(i.val, IdentifierArray):
                res = valueExpression(i.val, ts)
                augusTxt += '$t' + str(contadorT)
                augusTxt += f' = {str(res)};\n'
                arrayTables.pop()
                ts.setdefault(i.id, f'$t{str(contadorT)}')
                arrayTables.append(ts)
                contadorT += 1
            else:
                if isinstance(i.val, ReferenceBit):
                    res = valueExpression(i.val, ts)
                    augusTxt += '$t'+ str(contadorT)
                    augusTxt += f' = &{str(res)};\n'
                    arrayTables.pop()
                    ts.setdefault(i.id, f'$t{str(contadorT)}')
                    arrayTables.append(ts)
                else:
                    res = valueExpression(i.val, ts)
                    augusTxt += '$t' + str(contadorT)
                    augusTxt += f' = {str(res)};\n'
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
        augusTxt += f' = -1 ;\n'
        #contadorT += 1
        augusTxt += '$t'+ str(contadorT+1)
        augusTxt += f' = {str(num1)} * $t{str(contadorT)} ;\n'
        contadorT += 2
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
        id = valueExpression(Identifier(instruction.id, 0, 0), ts)
        aux = ''
        aux += str(id)         #$t0
        for i in instruction.expressions:
            aux += f'[{str(valueExpression(i,ts))}]'
        return aux
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
        #augusTxt += '$t'+ str(contadorT)
        #augusTxt += f' = &{str(num1)};\n'
        #contadorT += 1
        return f'{str(num1)}'
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


contador = 0
########################################## GRAPHO
def grafo(instrucciones):
    global contador
    node = g.node(contador, contador, 'S')
    ge = g.genera()
    ge.add(node)
    node = g.node(contador, contador+1, 'A')
    ge.add(node)
    contador += 1  #el nuevo padre
    instruccionesGlobales(instrucciones, ge, contador)

def instruccionesGlobales(instructions, ge, padre):
    global contador
    i = 0
    while i < len(instructions):
        #isinstance verificar tipos
        b = instructions[i]
        if isinstance(b, Declaration):
            node = g.node(padre, contador+1, 'INSTRUCCIONES GLOBALES')
            ge.add(node)
            node = g.node(contador+1, contador+2, 'DECLA_VARIABLES')
            ge.add(node)
            contador += 2
            padreLocal = contador
            node = g.node(contador, contador+1, 'TIPO')
            ge.add(node)
            node = g.node(contador+1, contador+2, f'{str(b.type_)}')
            ge.add(node)
            contador += 2       #despues restar 2 cuando termine
            #lista de id separador por coma
            for a in b.listId:
                if isinstance(a, SingleDeclaration):    #a es de tipo singleDeclaration
                    node = g.node(padreLocal, contador+1, f'{str(a.id)}')   
                    ge.add(node)
                    if a.val != '#':    #significa que si trae valor
                        node = g.node(padreLocal, contador+2, f'ASIGN')   
                        ge.add(node)
                        node = g.node(contador+2, contador+3, f'=')   
                        ge.add(node)
                        node = g.node(contador+2, contador+4, f'EXPRESION')   
                        ge.add(node)
                        contador += 4
                        padretmp = contador                        
                        #graficar esxpresion
                        drawExpresiones(a.val, ge, padretmp)
                    else:
                        node = g.node(padreLocal, contador + 2, f'ASIGN')
                        ge.add(node)
                        node = g.node(contador + 2, contador + 3, f'=')
                        ge.add(node)
                        node = g.node(contador + 2, contador + 4, f'EXPRESION')
                        ge.add(node)
                        contador += 4
                        padretmp = contador
                        # graficar esxpresion
                        node = g.node(contador, contador + 1, f'0')
                        ge.add(node)
                        contador += 1

                node = g.node(padreLocal, contador+1, ',')
                ge.add(node)
                contador += 1
        elif isinstance(b, FunctionDeclaration):
            node = g.node(padre, contador+1, 'INSTRUCCIONES GLOBALES')
            ge.add(node)
            node = g.node(contador+1, contador+2, 'DECLA_FUNCIONES')
            ge.add(node)
            node = g.node(contador+2, contador+3, 'TIPO')
            ge.add(node)
            node = g.node(contador+3, contador+4, f'{str(b.type_)}')
            ge.add(node)
            node = g.node(contador+2, contador+5, f'{str(b.id)}')
            ge.add(node)
            node = g.node(contador+2, contador+6, f'(')
            ge.add(node)
            node = g.node(contador+2, contador + 7, 'PARAMETROS')
            ge.add(node)
            auxPadre_ = contador+2
            contador += 7
            auxPadre = contador
            for z in b.params:
                drawExpresiones(z, ge, auxPadre)
                node = g.node(auxPadre, contador + 1, ',')
                ge.add(node)
                contador += 1
            node = g.node(auxPadre_, contador+1, f'INSTRUCCIONES_INTERNAS')
            ge.add(node)
            contador += 1
            #llamo a las instrucciones internas
            drawInstruccionesInternas(b.instructions, ge, contador)
            node = g.node(auxPadre_, contador+1, f')')
            ge.add(node)
            contador += 1
            a = 3
        i += 1

def drawInstruccionesInternas(instrucciones, ge, padre):
    global contador
    i = 0
    while i < len(instrucciones):
        #isinstance verificar tipos 
        a = instrucciones[i]      
        if isinstance(a, Declaration):
            node = g.node(padre, contador+1, 'DECLA_VARIABLES')
            ge.add(node)
            contador += 1
            padreLocal = contador
            node = g.node(contador, contador+1, 'TIPO')
            ge.add(node)
            node = g.node(contador+1, contador+2, f'{str(a.type_)}')
            ge.add(node)
            contador += 2       #despues restar 2 cuando termine
            #lista de id separador por coma
            for b in a.listId:
                if isinstance(b, SingleDeclaration):    #a es de tipo singleDeclaration
                    node = g.node(padreLocal, contador+1, f'{str(b.id)}')   
                    ge.add(node)
                    if b.val != '#':    #significa que si trae valor
                        node = g.node(padreLocal, contador+2, f'ASIGN')   
                        ge.add(node)
                        node = g.node(contador+2, contador+3, f'=')   
                        ge.add(node)
                        node = g.node(contador+2, contador+4, f'EXPRESION')   
                        ge.add(node)
                        contador += 4
                        padretmp = contador                        
                        #graficar esxpresion
                        drawExpresiones(b.val, ge, padretmp)
                    else:
                        node = g.node(padreLocal, contador + 2, f'ASIGN')
                        ge.add(node)
                        node = g.node(contador + 2, contador + 3, f'=')
                        ge.add(node)
                        node = g.node(contador + 2, contador + 4, f'EXPRESION')
                        ge.add(node)
                        contador += 4
                        padretmp = contador
                        # graficar esxpresion
                        node = g.node(contador, contador + 1, f'0')
                        ge.add(node)
                        contador += 1
                node = g.node(padreLocal, contador+1, ',')
                ge.add(node)
                contador += 1
        elif isinstance(a, Asignation):
            node = g.node(padre, contador + 1, 'ASIGNACIONES')
            ge.add(node)
            contador += 1
            node = g.node(contador, contador+1, a.id)
            ge.add(node)
            node = g.node(contador, contador + 2, a.op)
            ge.add(node)
            node = g.node(contador, contador + 3, f'EXPRESION')
            ge.add(node)
            contador += 3
            padretmp = contador
            # graficar esxpresion
            drawExpresiones(a.expresion, ge, padretmp)
        elif isinstance(a, If):
            node = g.node(padre, contador + 1, 'IF')
            ge.add(node)
            contador += 1
            node = g.node(contador, contador + 1, 'if')
            ge.add(node)
            node = g.node(contador, contador + 2, '(')
            ge.add(node)
            node = g.node(contador, contador + 3, f'EXPRESION')
            ge.add(node)
            padretmp = contador
            contador += 3
            # graficar esxpresion
            drawExpresiones(a.condition, ge, contador)
            node = g.node(padretmp, contador + 1, ')')
            ge.add(node)
            contador += 1
        elif isinstance(a, PrintF_):
            node = g.node(padre, contador + 1, 'PRINTF_')
            ge.add(node)
            contador += 1
            node = g.node(contador, contador + 1, 'print')
            ge.add(node)
            node = g.node(contador, contador + 2, '(')
            ge.add(node)
            node = g.node(contador, contador + 3, 'LISTA_PRINT')
            ge.add(node)
            padretmp = contador
            contador += 3
            paAuX = contador
            #grafica de lista de prints
            for b in a.expressions:
                node = g.node(paAuX, contador + 1, f'{str(drawValueExpression(b))}')
                ge.add(node)
                node = g.node(paAuX, contador + 2, f',')
                ge.add(node)
                contador += 2

            node = g.node(padretmp, contador + 1, ')')
            ge.add(node)
            contador += 1
        elif isinstance(a, Label):
            node = g.node(padre, contador + 1, 'LABEL')
            ge.add(node)
            node = g.node(contador+1, contador + 2, f'str{a.label}')
            ge.add(node)
            contador += 2
        elif isinstance(a, Goto):
            node = g.node(padre, contador + 1, 'GOTO')
            ge.add(node)
            node = g.node(contador+1, contador+2, 'goto')
            ge.add(node)
            node = g.node(contador+1, contador+3, f'{str(a.label)}')
            ge.add(node)
            contador += 3
        elif isinstance(a, IncreDecre_Pre):
            node = g.node(padre, contador + 1, 'INCREMENTO_DECREMENTO')
            ge.add(node)
            node = g.node(contador + 1, contador + 2, f'{str(a.signo)}')
            ge.add(node)
            node = g.node(contador + 1, contador + 3, f'{str(a.id)}')
            ge.add(node)
            contador += 3
        elif isinstance(a, IncreDecre_Post):
            node = g.node(padre, contador + 1, 'INCREMENTO_DECREMENTO')
            ge.add(node)
            node = g.node(contador + 1, contador + 2, f'{str(a.id)}')
            ge.add(node)
            node = g.node(contador + 1, contador + 3, f'{str(a.signo)}')
            ge.add(node)
            contador += 3
        elif isinstance(a, For):
            node = g.node(padre, contador + 1, 'FOR')
            ge.add(node)
            node = g.node(contador + 1, contador + 2, f'for')
            ge.add(node)
            node = g.node(contador + 1, contador + 3, f'DECLARACION')
            ge.add(node)
            auxPadre = contador+1
            contador += 3
            drawInstruccionesInternas([a.declaration], ge, contador)
            node = g.node(auxPadre, contador +1, f'CONDICION')
            ge.add(node)
            contador += 1
            drawExpresiones(a.condition, ge, contador)
            node = g.node(auxPadre, contador +1, f'INSTRUCCIONES_INTERNAS')
            ge.add(node)
            contador += 1
            drawInstruccionesInternas(a.instructions, ge, contador)
            node = g.node(auxPadre, contador + 1, f'INCREMENTO_DECREMENTO')
            ge.add(node)
            contador += 1
            drawInstruccionesInternas([a.increDecre], ge, contador)
        elif isinstance(a, While_):
            node = g.node(padre, contador + 1, 'WHILE')
            ge.add(node)
            padreTmp = contador + 1
            node = g.node(padreTmp, contador + 1, 'while')
            ge.add(node)
            node = g.node(padreTmp, contador + 2, '(')
            ge.add(node)
            node = g.node(padreTmp, contador + 3, 'CONDICION')
            ge.add(node)
            contador += 3
            drawExpresiones(a.condition, ge, contador)
            node = g.node(padreTmp, contador + 1, ')')
            ge.add(node)
            contador += 1
            #instrucciones internas
            drawInstruccionesInternas(a.instructions, ge, contador)
        elif isinstance(a, DoWhile_):
            node = g.node(padre, contador + 1, 'DO_WHILE')
            ge.add(node)
            contador +=1 
            auxPadre = contador
            node = g.node(auxPadre, contador + 1, 'do')
            ge.add(node)
            contador += 1            
            #instrucciones internas
            drawInstruccionesInternas(a.instructions, ge, contador)
            node = g.node(auxPadre, contador + 1, 'while')
            ge.add(node)
            node = g.node(auxPadre, contador + 2, 'CONDICION')
            ge.add(node)
            contador += 2
            drawExpresiones(a.condition, ge, contador)
        elif isinstance(a, Switch_):
            node = g.node(padre, contador + 1, 'SWITCH')
            ge.add(node)
            contador +=1
            auxPadre = contador
            node = g.node(auxPadre, contador + 1, 'switch')
            ge.add(node)
            node = g.node(auxPadre, contador + 2, 'EXPRESION')
            ge.add(node)
            contador += 2
            drawExpresiones(a.expresion, ge, contador)
            #lista de cases
            node = g.node(auxPadre, contador + 1, 'LISTA_CASES')
            ge.add(node)
            contador += 1 
            padreList = contador
            for z in a.listaCases:
                node = g.node(padreList, contador + 1, 'CASE')
                ge.add(node)
                contador += 1
                auxPa = contador
                node = g.node(auxPa, contador + 1, 'case')
                ge.add(node)
                node = g.node(auxPa, contador + 2, 'EXPRESION')
                ge.add(node)
                contador += 2
                drawExpresiones(z.expresion, ge, contador)
                node = g.node(auxPa, contador + 1, 'INSTRUCCIONES_INTERNAS')
                ge.add(node)
                contador += 1
                drawInstruccionesInternas(z.instructions, ge, contador)
        elif isinstance(a, CallFunction):
            node = g.node(padre, contador + 1, 'CALL_FUNCTION')
            ge.add(node)
            pa = contador+1
            node = g.node(contador + 1, contador + 2, f'{str(a.id)}')
            ge.add(node)
            node = g.node(contador + 1, contador+3 , '(')
            ge.add(node)
            node = g.node(contador + 1, contador + 4, 'PARAMETROS')
            ge.add(node)
            contador += 4
            auxPadre = contador
            for z in a.params:
                drawExpresiones(z, ge, auxPadre)
                node = g.node(auxPadre, contador + 1, ',')
                ge.add(node)
                contador += 1
            node = g.node(pa, contador + 1, ')')
            ge.add(node)
            contador += 1
        elif isinstance(a, AsignationArray):
            node = g.node(padre, contador + 1, 'ASIGNATION_ARRAY')
            ge.add(node)
            padreAux = contador+1
            contador += 1
            node = g.node(padreAux, contador + 1, f'{a.id}')
            ge.add(node)
            contador += 1
            #recorrer los corchetes
            for z in a.corchetes:
                node = g.node(padreAux, contador + 1, f'[  EXPRESION  ]')
                ge.add(node)
                contador += 1
                node = g.node(contador, contador + 1, f'EXPRESION')
                ge.add(node)
                contador += 1
                drawExpresiones(z, ge, contador)
                contador += 1
            node = g.node(padreAux, contador + 1, f'=')
            ge.add(node)
            contador += 1
            node = g.node(contador, contador + 1, f'EXPRESION')
            ge.add(node)
            contador += 1
            drawExpresiones(z, ge, contador)
            contador += 1


        i += 1

def drawExpresiones(instruction, ge, padre):
    global contador
    #print(f'ahshas: {str(instruction)}') 
    if isinstance(instruction, BinaryExpression):
        num1 = drawValueExpression(instruction.op1)
        num2 = drawValueExpression(instruction.op2)
        try:
            if instruction.operator == Aritmetics.MAS: 
               node = g.node(padre, contador+1, str(num1))
               ge.add(node)
               node = g.node(padre, contador+2, '+')
               ge.add(node)
               node = g.node(padre, contador+3, str(num2))
               ge.add(node)
               contador +=3
            elif instruction.operator == Aritmetics.MENOS:
                node = g.node(padre, contador+1, str(num1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '-')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(num2))
                ge.add(node)
                contador +=1
            elif instruction.operator == Aritmetics.POR:
                node = g.node(padre, contador+1, str(num1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '*')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(num2))
                ge.add(node)
                contador +=1
            elif instruction.operator == Aritmetics.DIV: 
                node = g.node(padre, contador+1, str(num1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '/')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(num2))
                ge.add(node)
                contador +=1
            elif instruction.operator == Aritmetics.MODULO:
                node = g.node(padre, contador+1, str(num1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '%')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(num2))
                ge.add(node)
                contador +=1
        except:
            pass
    elif isinstance(instruction, LogicAndRelational):
        val1 = drawValueExpression(instruction.op1)
        val2 = drawValueExpression(instruction.op2)
        try:
            if instruction.operator == LogicsRelational.MAYORQUE: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '>')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.MENORQUE: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '<')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.MAYORIGUAL: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '>=')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.MENORIGUAL: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '<=')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.IGUALQUE: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '==')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.AND: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '&&')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.OR: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '||')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.XOR: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '^')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == LogicsRelational.DIFERENTE:
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '!=')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
        
        except:
            pass
    elif isinstance(instruction, Not):
        try:
            num1 = drawValueExpression(instruction.expression)
            node = g.node(padre, contador+1, str(num1))
            ge.add(node)
            contador +=1
            node = g.node(padre, contador+1, '!')
            ge.add(node)
            contador +=1
        except:
            pass
    elif isinstance(instruction, Abs):
        try:
            node = g.node(padre, contador+1, 'abs')
            ge.add(node)
            contador +=1
            node = g.node(padre, contador+1, str(drawValueExpression(instruction.expression)))
            ge.add(node)
            contador +=1
        except:
            pass
    elif isinstance(instruction, NegativeNumber):
        try:
            num1 = drawValueExpression(instruction.expression)
            node = g.node(padre, contador+1, '-')
            ge.add(node)
            contador +=1
            node = g.node(padre, contador+1, str(num1))
            ge.add(node)
            contador +=1
        except:
            pass
    elif isinstance(instruction, Identifier):
        node = g.node(padre, contador+1, str(instruction.id))
        ge.add(node)
        contador +=1
    elif isinstance(instruction, Number):
        node = g.node(padre, contador+1, str(instruction.val))
        ge.add(node)
        contador +=1
    elif isinstance(instruction, Cast_):
        num1 = drawValueExpression(instruction.expression)

        node = g.node(padre, contador+1, str(instruction.type))
        ge.add(node)
        contador +=1
        node = g.node(padre, contador+1, str(num1))
        ge.add(node)
        contador +=1
    elif isinstance(instruction, String_):
        node = g.node(padre, contador+1, str(instruction.string))
        ge.add(node)
        contador +=1
    elif isinstance(instruction, ExpressionsDeclarationArray):
        #print(f'ahshas: {str(instruction.expressionDer)}') 
        for i in instruction.expressionIzq:
            node = g.node(padre, contador+1, f'[{str(drawValueExpression(i))}]')
            ge.add(node)
            contador +=1
        node = g.node(padre, contador+1, f'=')
        ge.add(node)
        contador +=1

        drawExpresiones(instruction.expressionDer, ge, padre)
    elif instruction == 'array': 
        node = g.node(padre, contador+1, f'array ( )')
        ge.add(node)
        contador +=1
    elif isinstance(instruction, IdentifierArray):
        try:
            #print(str(instruction))
            node = g.node(padre, contador+1, str(instruction.id))
            ge.add(node)
            contador +=1
            sym = ts.get(instruction.id).valor            
            i = 0
            while i < len(instruction.expressions):
                node = g.node(padre, contador+1, f'[{str(drawValueExpression(instruction.op2))}]')
                ge.add(node)
                contador +=1
                i += 1
        except:
            pass
    elif isinstance(instruction, ReadConsole):
        #lectura de consola
       
        node = g.node(padre, contador+1, 'read ( ) ')
        ge.add(node)
        contador +=1
    elif isinstance(instruction, RelationalBit):
        val1 = drawValueExpression(instruction.op2)
        val2 = drawValueExpression(instruction.op2)       
        try:
            if instruction.operator == BitToBit.ANDBIT: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '&')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == BitToBit.ORBIT: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '|')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == BitToBit.XORBIT: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '^')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == BitToBit.SHIFTI: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '<<')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
            elif instruction.operator == BitToBit.SHIFTD: 
                node = g.node(padre, contador+1, str(val1))
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, '>>')
                ge.add(node)
                contador +=1
                node = g.node(padre, contador+1, str(val2))
                ge.add(node)
                contador +=1
        except:
            pass
    elif isinstance(instruction, NotBit):
        num1 = drawValueExpression(instruction.expression)
        node = g.node(padre, contador+1, '~')
        ge.add(node)
        contador +=1
        node = g.node(padre, contador+1, str(num1))
        ge.add(node)
        contador +=1
    elif isinstance(instruction, ReferenceBit):
        num1 = drawValueExpression(instruction.expression)
        node = g.node(padre, contador+1, '&')
        ge.add(node)
        contador +=1
        node = g.node(padre, contador+1, str(num1))
        ge.add(node)
        contador +=1

def drawValueExpression(instruction):
    if isinstance(instruction, Identifier):
        return instruction.id
    elif isinstance(instruction, Number):
        return instruction.val
    elif isinstance(instruction, String_):
        return instruction.string