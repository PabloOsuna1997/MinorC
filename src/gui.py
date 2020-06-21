# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import os
import sys

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import execute
import grammar
import grammarDesc
import re
import reportGenerator as rg
import SymbolTable as TS
from expressions import *
from instructions import *
from semanticObject import *

contadorVentanas = 0
data = []
dataS = []
dataSema = []
dataTs = []
pasadas = 0

tsDebug = TS.SymbolTable()
printListDebug = []
instructionsDebug = []
printPases = []
conttadorIns = 0
instructionsList = []
banderaDescAsc = True
textCopy = ''

class pintar(QtGui.QSyntaxHighlighter):

    expresiones = []
    expresiones.append((r"\d+(\.\d+)?", QtGui.QColor(198,209,101)))
    expresiones.append((r"\bmain", QtGui.QColor(152,81,164)))
    expresiones.append((r"[a-zA-Z_][a-zA-Z_0-9]*", QtGui.QColor(161,81,164)))        
    expresiones.append((r'\".+\"', QtGui.QColor(185,185,112)))
    expresiones.append((r'\'.+\'', QtGui.QColor(185,185,112)))
    expresiones.append((r"#.*", QtGui.QColor(68,146,92)))
    expresiones.append((r"\$(t|a|v|ra|sp?)[0-9]*", QtGui.QColor(119,193,230)))

    def highlightBlock(self, text):
        formato = QtGui.QTextCharFormat()
        for i in self.expresiones:
            #print(expresion[0])
            formato.setForeground(QtGui.QColor(i[1]))
            tmp = QtCore.QRegExp(i[0])
            indice = tmp.indexIn(text,0)
            while indice >= 0:
                length = tmp.matchedLength()
                QtGui.QSyntaxHighlighter.setFormat(self, indice, length, formato)
                indice = tmp.indexIn(text,indice + length)

class Ui_Augus(object):
    
    def setupUi(self, Augus):        
        Augus.setObjectName("Augus")
        Augus.resize(980, 616)
        Augus.setStyleSheet('QMainWindow{background-color: yellow; border: 1px solid black;}')
        self.centralwidget = QtWidgets.QWidget(Augus)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(33,33,33);")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 471, 541))
        self.tabWidget.setObjectName("tabWidget")
        self.textEditConsole = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditConsole.setGeometry(QtCore.QRect(510, 20, 461, 541))
        self.textEditConsole.setObjectName("textEditConsole")
        self.textEditConsole.setStyleSheet('''background-color: rgb(33, 33, 33);
                                            border-color: rgb(18, 18, 18);
                                            color: rgb(223, 213, 213);
                                            font: 12pt \"consolas\";''' )
        self.textEditConsole.setPlainText("CONSOLE:\n")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(985, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Next")
        self.textDebug = QtWidgets.QTextEdit(self.centralwidget)
        self.textDebug.setGeometry(QtCore.QRect(985, 50, 480, 510))
        self.textDebug.setObjectName("textDebug")
        self.textDebug.setStyleSheet('''background-color: rgb(33, 33, 33);
                                            border-color: rgb(18, 18, 18);
                                            color: rgb(0, 255, 60);
                                            font: 12pt \"consolas\";''' )
        self.textDebug.setPlainText("DEBUG:\n")
        Augus.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Augus)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuEjecutar = QtWidgets.QMenu(self.menubar)
        self.menuEjecutar.setObjectName("menuEjecutar")
        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuReportes = QtWidgets.QMenu(self.menubar)
        self.menuReportes.setObjectName("menuReportes")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        Augus.setMenuBar(self.menubar)
       
        self.statusbar = QtWidgets.QStatusBar(Augus)
        self.statusbar.setObjectName("statusbar")
        Augus.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(Augus)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionReporteLexico = QtWidgets.QAction(Augus)
        self.actionReporteLexico.setObjectName("actionReporteLexico")
        self.actionReporteSintactico = QtWidgets.QAction(Augus)
        self.actionReporteSintactico.setObjectName("actionReporteSintactico")
        self.actionReporteSemantico = QtWidgets.QAction(Augus)
        self.actionReporteSemantico.setObjectName("actionReporteSemantico")
        self.actionReporteAST = QtWidgets.QAction(Augus)
        self.actionReporteAST.setObjectName("actionReporteAST")
        self.actionReporteGramatical = QtWidgets.QAction(Augus)
        self.actionReporteGramatical.setObjectName("actionReporteGramatical")
        self.actionAST = QtWidgets.QAction(Augus)
        self.actionAST.setObjectName("actionAST")
        self.actionReporteTS = QtWidgets.QAction(Augus)
        self.actionReporteTS.setObjectName("actionReporteTS")
        self.actionAbrir = QtWidgets.QAction(Augus)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionGuardar = QtWidgets.QAction(Augus)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_Como = QtWidgets.QAction(Augus)
        self.actionGuardar_Como.setObjectName("actionGuardar_Como")
        self.actionCerrar = QtWidgets.QAction(Augus)
        self.actionCerrar.setObjectName("actionCerrar")
        self.actionSalir = QtWidgets.QAction(Augus)
        self.actionSalir.setObjectName("actionSalir")
        self.actionCopiar = QtWidgets.QAction(Augus)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(Augus)
        self.actionPegar.setObjectName("actionPegar")
        self.actionCortar = QtWidgets.QAction(Augus)
        self.actionCortar.setObjectName("actionCortar")
        self.actionBuscar = QtWidgets.QAction(Augus)
        self.actionBuscar.setObjectName("actionBuscar")
        self.actionAscendente = QtWidgets.QAction(Augus)
        self.actionAscendente.setObjectName("actionAscendente")
        self.actionDescendente = QtWidgets.QAction(Augus)
        self.actionDescendente.setObjectName("actionDescendente")
        self.actionDebuguer = QtWidgets.QAction(Augus)
        self.actionDebuguer.setObjectName("actionDebuguer")
        self.actionCambiar_color_de_fondo = QtWidgets.QAction(Augus)
        self.actionCambiar_color_de_fondo.setObjectName("actionCambiar_color_de_fondo")
        self.actionLigth = QtWidgets.QAction(Augus)
        self.actionLigth.setObjectName("actionLigth")
        self.actionMat = QtWidgets.QAction(Augus)
        self.actionMat.setObjectName("actionMat")
        self.actionAyuda = QtWidgets.QAction(Augus)
        self.actionAyuda.setObjectName("actionAyuda")
        self.actionAcerca = QtWidgets.QAction(Augus)
        self.actionAcerca.setObjectName("actionAcerca")
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuReportes.addAction(self.actionReporteLexico)
        self.menuReportes.addAction(self.actionReporteSintactico)
        self.menuReportes.addAction(self.actionReporteSemantico)
        self.menuReportes.addAction(self.actionReporteGramatical)
        self.menuReportes.addAction(self.actionReporteAST)
        self.menuReportes.addAction(self.actionAST)
        self.menuReportes.addAction(self.actionReporteTS)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addAction(self.actionCortar)
        self.menuEditar.addAction(self.actionBuscar)
        self.menuEjecutar.addAction(self.actionAscendente)
        self.menuEjecutar.addAction(self.actionDescendente)
        self.menuEjecutar.addAction(self.actionDebuguer)
        self.menuOpciones.addAction(self.actionCambiar_color_de_fondo)
        self.menuOpciones.addAction(self.actionLigth)
        self.menuOpciones.addAction(self.actionMat)
        self.menuAyuda.addAction(self.actionAyuda)
        self.menuAyuda.addAction(self.actionAcerca)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuEjecutar.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuReportes.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(Augus)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Augus)

        #actions
        self.actionNuevo.triggered.connect(lambda : self.fn_Nuevo())
        self.actionAbrir.triggered.connect(lambda : self.fn_Abrir())
        self.actionAscendente.triggered.connect(lambda : self.fn_Ejecutar_Ascendente())
        self.actionDescendente.triggered.connect(lambda : self.fn_Ejecutar_Descendente())
        self.actionDebuguer.triggered.connect(lambda : self.fn_Ejecutar_Debuguer())
        self.actionGuardar.triggered.connect(lambda : self.fn_Guardar())
        self.actionGuardar_Como.triggered.connect(lambda : self.fn_Guardar_Como())
        self.actionCerrar.triggered.connect(lambda : self.fn_Cerrar())
        self.actionSalir.triggered.connect(lambda : self.fn_Salir())
        self.actionReporteLexico.triggered.connect(lambda : self.fn_repLexico())
        self.actionReporteSintactico.triggered.connect(lambda : self.fn_repSintactico())
        self.actionReporteSemantico.triggered.connect(lambda : self.fn_repSemantico())
        self.actionReporteGramatical.triggered.connect(lambda : self.fn_repGramatical())
        self.actionReporteAST.triggered.connect(lambda : self.fn_repAST())
        self.actionAST.triggered.connect(lambda : self.fn_repASTGeneral())
        self.actionReporteTS.triggered.connect(lambda : self.fn_repTS())
        self.pushButton.clicked.connect(lambda : self.fn_Next())
        self.actionCambiar_color_de_fondo.triggered.connect(lambda : self.fn_cambiaColor())
        self.actionLigth.triggered.connect(lambda : self.fn_cambiaColorLigth())
        self.actionMat.triggered.connect(lambda : self.fn_cambiaColorMaterial())
        self.actionBuscar.triggered.connect(lambda : self.fn_buscarReemplazar())
        self.actionAyuda.triggered.connect(lambda : self.fn_ayuda())
        self.actionAcerca.triggered.connect(lambda : self.fn_acerca())
        self.actionCopiar.triggered.connect(lambda : self.fn_copiar())
        self.actionPegar.triggered.connect(lambda : self.fn_pegar())
        self.actionCortar.triggered.connect(lambda : self.fn_cortar())

    def retranslateUi(self, Augus):
        _translate = QtCore.QCoreApplication.translate
        Augus.setWindowTitle(_translate("Augus", "Augus"))
        self.menuArchivo.setTitle(_translate("Augus", "Archivo"))
        self.menuEditar.setTitle(_translate("Augus", "Editar"))
        self.menuEjecutar.setTitle(_translate("Augus", "Ejecutar"))
        self.menuOpciones.setTitle(_translate("Augus", "Opciones"))
        self.menuReportes.setTitle(_translate("Augus", "Reportes"))
        self.menuAyuda.setTitle(_translate("Augus", "Ayuda"))
        self.actionNuevo.setText(_translate("Augus", "Nuevo"))
        self.actionReporteLexico.setText(_translate("Augus", "Reporte Lexico"))
        self.actionReporteSintactico.setText(_translate("Augus", "Reporte Sintactico"))
        self.actionReporteSemantico.setText(_translate("Augus", "Reporte Semantico"))
        self.actionReporteTS.setText(_translate("Augus", "Reporte Tabla de Simbolos"))
        self.actionReporteAST.setText(_translate("Augus", "Reporte AST ascendente"))
        self.actionReporteGramatical.setText(_translate("Augus", "Reporte Gramatical"))
        self.actionAST.setText(_translate("Augus", "Reporte AST"))
        self.actionAbrir.setText(_translate("Augus", "Abrir"))
        self.actionGuardar.setText(_translate("Augus", "Guardar"))
        self.actionGuardar_Como.setText(_translate("Augus", "Guardar Como"))
        self.actionCerrar.setText(_translate("Augus", "Cerrar"))
        self.actionSalir.setText(_translate("Augus", "Salir"))
        self.actionCopiar.setText(_translate("Augus", "Copiar"))
        self.actionPegar.setText(_translate("Augus", "Pegar"))
        self.actionCortar.setText(_translate("Augus", "Cortar"))
        self.actionBuscar.setText(_translate("Augus", "Buscar y Reemplazar"))
        self.actionAscendente.setText(_translate("Augus", "Ascendente"))
        self.actionDescendente.setText(_translate("Augus","Descendente"))
        self.actionDebuguer.setText(_translate("Augus","Debuguer"))
        self.actionCambiar_color_de_fondo.setText(_translate("Augus", "Tema Dark"))
        self.actionLigth.setText(_translate("Augus", "Tema Light"))
        self.actionMat.setText(_translate("Augus", "Tema Material"))
        self.actionAyuda.setText(_translate("Augus", "Ayuda"))
        self.actionAcerca.setText(_translate("Augus", "Acerca de"))

    def fn_copiar(self):
        try:
            global textCopy
            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            content += '\n'
            textCopy = content
        except:
            pass
    
    def fn_pegar(self):
        try:
            global textCopy
            self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").setPlainText(textCopy)
        except:
            pass

    def fn_cortar(self):
        try:
            global textCopy
            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            content += '\n'
            textCopy = content
        except:
            pass

    def fn_ayuda(self):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setText("Lenguaje Augus\nSi presentas algun inconveniente comunicate al correo 2472932372001@ingenieria.usac.edu.gt\nDesarrollador Juan Pablo Osuna de Leon\nLicencia: https://github.com/PabloOsuna1997/Proyecto_Augus/blob/master/LICENSE\nReporitorio de Github: https://github.com/PabloOsuna1997/Proyecto_Augus ")
        self.msgBox.exec()

    def fn_acerca(self):
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setText("Lenguaje Augus. \nCreado con fines academicos basado en PHP y MIPDS.\nDesarrollador en Python 3.8\nDesarrollador: Juan Pablo Osuna de Leon estudiante de la Universidad de San Carlos de Guatemala, carnet 201503911")
        self.msgBox.exec()

    def fn_buscarReemplazar(self):
        import read
        import re
        a = read.Read()
        find = a.buscar("Buscar:")
        replace = a.buscar("Reemplazar:")        
        content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
        incidences = re.findall(find, content, flags=re.IGNORECASE)
        cont = re.sub(find, replace, content, flags=re.IGNORECASE)
        cont += '\n'
        self.textEdit.setPlainText(cont)
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setText(f"Se han reemplazado {str(len(incidences))} incidencias.")
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.exec()

    def fn_cambiaColorLigth(self):
        try:
            self.textEdit.setStyleSheet('''background-color: rgb(255, 255, 255);
                                        border-color: rgb(18, 18, 18);
                                        color: rgb(0, 0, 0);
                                        font: 12pt \"consolas\";
                                        ''')
            self.textEditConsole.setStyleSheet('''background-color: rgb(255, 255, 255);
                                                border-color: rgb(18, 18, 18);
                                                color: rgb(0, 0, 0);
                                                font: 12pt \"consolas\";''')

            self.centralwidget.setStyleSheet("background-color: rgb(255,255,255);")
        except:
            pass

    def fn_cambiaColor(self):
        try:
            self.textEdit.setStyleSheet('''background-color: rgb(33, 33, 33);
                                                border-color: rgb(18, 18, 18);
                                                color: rgb(255, 255, 255);
                                                font: 12pt \"consolas\";
                                        ''')
            self.textEditConsole.setStyleSheet('''background-color: rgb(33, 33, 33);
                                                border-color: rgb(18, 18, 18);
                                                color: rgb(51, 252, 255);
                                                font: 12pt \"consolas\";''')
            self.centralwidget.setStyleSheet("background-color: rgb(33,33,33);");
        except:
            pass

    def fn_cambiaColorMaterial(self):
        try:
            self.textEdit.setStyleSheet('''background-color: rgb(159, 161, 159);
                                                border-color: rgb(18, 18, 18);
                                                color: rgb(0, 34, 255);
                                                font: 12pt \"consolas\";''')

            self.textEditConsole.setStyleSheet('''background-color: rgb(159, 161, 159);
                                                border-color: rgb(18, 18, 18);
                                                color: rgb(119, 0, 255);
                                                font: 12pt \"consolas\";''')
            self.centralwidget.setStyleSheet("background-color: (159, 161, 159);");
        except:
            pass
    
    def fn_Nuevo(self):
        global contadorVentanas
        contadorVentanas += 1
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setGeometry(QtCore.QRect(0,0,460,520))
        self.textEdit.setStyleSheet('''background-color: rgb(33, 33, 33);
                                            border-color: rgb(18, 18, 18);
                                            color: rgb(255, 255, 255);
                                            font: 12pt \"consolas\";''' )
        self.textEdit.setObjectName("textEdit")
        self.pintar = pintar(self.textEdit.document())
        self.tabWidget.addTab(
            self.tab,"Tab "+ str(contadorVentanas)
        )
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)    #para poner el focus en la nueva pestaña
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setText("New area.")
        self.msgBox.exec()

    def fn_Abrir(self):
        try:
            filename = QFileDialog.getOpenFileName(None,' Open document',r"c:\\Users\\", "All Files (*)")
            path = filename[0]
            print(path)
            with open(path, 'r') as f:
                data = f.read()
                            
                #creating a new tab
                self.tab = QtWidgets.QWidget()
                self.tab.setObjectName("tab")
                self.textEdit = QtWidgets.QTextEdit(self.tab)
                self.textEdit.setGeometry(QtCore.QRect(0,0,460,520))
                self.textEdit.setStyleSheet('''background-color: rgb(33, 33, 33);
                                            border-color: rgb(18, 18, 18);
                                            color: rgb(255, 255, 255);
                                            font: 12pt \"consolas\";''' )
                self.textEdit.setObjectName("textEdit")
                self.pintar = pintar(self.textEdit.document())
                self.textEdit.setPlainText(data)
                self.tabWidget.addTab(
                    self.tab,path
                )
                self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)    #para poner el focus en la nueva pestaña

                #close the file
                f.close()
        except:
            print("closing file dialog.")

    def fn_repASTGeneral(self):
        try:  
            fgraph = open('../reports/astG.dot','w+') #creamos el archivo
            fgraph.write("graph \"\" { node [shape=box];")
            fgraph.close()

            #llamar a metodo de dibujo en execute
            global instructionsList
            execute.grafo(instructionsList,self.textEditConsole)

            fgraph = open('../reports/astG.dot','a') #agregamos al archivo '}'
            fgraph.write("}")
            fgraph.flush()
            fgraph.close()
            os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
            #os.system('dot -Tpng  ../reports/ast.dot  -o  ../reports/ast.png')
            os.system('dot -Tsvg  ../reports/astG.dot  -o  ../reports/astG.svg')
            os.startfile('..\\reports\\astG.svg')
            #ruta = ("../reports/ast.png")
            #im = Image.open(ruta)
            #im.show()
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Error al crear reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()

    def fn_repAST(self):
        try:
            os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
            #os.system('dot -Tpng  ../reports/ast.dot  -o  ../reports/ast.png')
            os.system('dot -Tsvg  ../reports/ast.dot  -o  ../reports/ast.svg')
            os.startfile('..\\reports\\ast.svg')
            #ruta = ("../reports/ast.png")
            #im = Image.open(ruta)
            #im.show()
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Error al crear reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()

    def fn_repTS(self):
        print("reporte de tabla de simbolos")
        try:
            fgraph = open('../reports/tsReport.dot','w+') #creamos el archivo
            fgraph.write("digraph H { parent [ shape=plaintext label=< <table border=\'1\' cellborder=\'1\'>")                    
            fgraph.write("<tr><td colspan=\"3\">REPORTE DE TABLA DE SIMBOLOS</td></tr>")
            fgraph.write("<tr><td port=\'port_one\'>ID</td><td port=\'port_two\'>TIPO</td><td port=\'port_three\'>VALOR</td><td port=\'port_four\'>DECLARADA EN</td><td port=\'port_five\'>DIMENSION</td><td port=\'port_six\'>REFERENCIA</td><td port=\'port_seven\'>PARAMETROS</td></tr>")
            
            for key, val in execute.tsGlobal.symbols.items():
                fgraph.write(f"<tr><td port=\'port_one\'>{str(key)}</td><td port=\'port_two\'>{str(val.tipo)}</td><td port=\'port_three\'>{str(val.valor)}</td><td port=\'port_four\'>{str(val.declarada)}</td><td port=\'port_five\'>{str(val.dimension)}</td><td port=\'port_six\'>{str(val.referencia)}</td><td port=\'port_seven\'>{str(val.parametros)}</td></tr>")
                        
            fgraph.write("</table> >]; }")
            fgraph.close()

            os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
            os.system('dot -Tpng ../reports/tsReport.dot -o ../reports/tsReport.png')    

            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Reporte creado.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()

            ruta = ("../reports/tsReport.png")
            im = Image.open(ruta)
            im.show()

            execute.tsGlobal = {}
        except:
            print("error")
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Error al crear el reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()

    def fn_repGramatical(self):
        print("reporte gramatical")
        try:
            fgraph = open('../reports/gramaticalReport.dot','w+') #creamos el archivo
            fgraph.write("digraph H { parent [ shape=plaintext label=< <table border=\'1\' cellborder=\'1\'>\n")                    
            fgraph.write("<tr><td colspan=\"3\">REPORTE GRAMATICAL</td></tr>\n")
            fgraph.write("<tr><td port=\'port_one\'>PRODUCCION</td><td port=\'port_two\'>REGLAS SEMANTICAS</td></tr>\n")
            
            global banderaDescAsc  #true = se analizo ascendente y 0 se analizao descendente
            if banderaDescAsc:
                for i in grammar.grammarList:
                    fgraph.write(f"<tr><td align=\"left\" port=\'port_one\'>{str(i.production.replace('<', '&lt;').replace('>', '&gt;').replace('|', '<BR/>|').replace('<<','&lt&lt;').replace('>>','&gt&gt;'))}</td><td align=\"left\" port=\'port_two\'>{str(i.rules)}</td></tr>\n")
            else:
                for i in grammarDesc.grammarList:
                    fgraph.write(f"<tr><td align=\"left\" port=\'port_one\'>{str(i.production.replace('<', '&lt;').replace('>', '&gt;').replace('|', '<BR/>|').replace('<<','&lt&lt;').replace('>>','&gt&gt;'))}</td><td align=\"left\" port=\'port_two\'>{str(i.rules)}</td></tr>\n")
            
            fgraph.write("</table> >]; \n}")
            fgraph.close()

            os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
            os.system('dot -Tpng ../reports/gramaticalReport.dot -o ../reports/gramaticalReport.png')    

            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Reporte creado.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()

            grammar.grammarList[:] = []

            ruta = ("../reports/gramaticalReport.png")
            im = Image.open(ruta)
            im.show()

        except:
            print("error")
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Error al crear el reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()
    
    def fn_repSemantico(self):
        print("reportando semantico")
        global dataSema
        try:
            rg.export_to_pdf(dataSema,3)
            dataSema[:] = []
            execute.semanticErrorList[:] = []         

            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Despelgando reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()
            import os
            os.startfile('..\\reports\\semanticReport.pdf')
        except:
            print("error")
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Porfavor cierre el reporte de errores semanticos.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()

    def fn_repSintactico(self):
        print("reportando sintactico")
        global dataS
        try:
            rg.export_to_pdf(dataS,2)
            dataS[:] = []
            grammar.sintacticErroList[:] = []           

            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Despelgando reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()
            import os
            os.startfile('..\\reports\\sintacticReport.pdf')
        except:
            print("error")
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Porfavor cierre el reporte sintactico.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()
    
    def fn_repLexico(self):
        print("reportando lexico")
        global data
        try:
            rg.export_to_pdf(data,1)
            data[:] = []
            grammar.LexicalErrosList[:] = []           

            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Despelgando reporte.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()
            import os
            os.startfile('..\\reports\\lexicalReport.pdf')
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("please close report lexical.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.exec()

    def fn_Next(self):
        global tsDebug, printListDebug, instructionsDebug, conttadorIns, printPases
        if conttadorIns < len(instructionsDebug):
            if isinstance(instructionsDebug[conttadorIns], If):
                result = execute.valueExpression(instructionsDebug[conttadorIns].expression, execute.tsGlobal, self.textEditConsole)                
                self.textDebug.append(f'if: {result} ->')                
                if result == 1:
                    self.textDebug.append('true')
                    tmp = conttadorIns
                    conttadorIns = execute.goto(conttadorIns + 1, instructionsDebug, instructionsDebug[conttadorIns].label)
                    if conttadorIns != 0:
                        execute.pasadas = 0
                        # print("realizando salto a: "+ str(b.label))
                    else:
                        conttadorIns = tmp
                        # print("error semantico, etiqueta no existe")
                        se = seOb(f"Error: etiqueta {instructionsDebug[conttadorIns].label} no existe", instructionsDebug[conttadorIns].line, instructionsDebug[conttadorIns].column)
                        execute.semanticErrorList.append(se)
                elif result == '#':
                    se = seOb(f"Error: Condicion no valida", instructionsDebug[conttadorIns].line, instructionsDebug[conttadorIns].column)
                    execute.semanticErrorList.append(se)
                else:
                    self.textDebug.append('false\n')
            elif isinstance(instructionsDebug[conttadorIns], Goto):
                # seteamos la instruccion anterior como la llamada al goto
                tmp = conttadorIns
                conttadorIns = execute.goto(conttadorIns, instructionsDebug,instructionsDebug[conttadorIns].label)
                if conttadorIns != 0:
                    execute.pasadas = 0
                    # print("realizando salto a: "+ str(b.label))
                else:
                    conttadorIns = tmp
                    # print("error semantico, etiqueta no existe")
                    se = seOb(f"Error: etiqueta {instructionsDebug[conttadorIns].label} no existe", instructionsDebug[conttadorIns].line, instructionsDebug[conttadorIns].column)
                    execute.semanticErrorList.append(se)
            else:
                execute.executeDebug(instructionsDebug[conttadorIns],self.textEditConsole)
            conttadorIns += 1

        self.textDebug.setText("")
        self.textDebug.setPlainText("DEBUG:\n")
        for key, val in execute.tsGlobal.symbols.items():
            self.textDebug.append(f'id: {str(key)} valor: {str(val.valor)} \n')

        if conttadorIns == len(instructionsDebug)-1:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Analisis correcto.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()
            Augus.resize(980, 616)

        elif len(execute.semanticErrorList) != 0:                              
            dataSema = [("DESCRIPCION", "COLUMNA", "LINEA")]
            for i in execute.semanticErrorList:
                dataSema.append((str(i.description), str(i.column), str(i.line)))
                    
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Existen errores semanticos.")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.exec()
        
    def fn_Ejecutar_Debuguer(self):
        print("ejecutando debuguer")
        global tsDebug, printListDebug, instructionsDebug, conttadorIns, printPases
        Augus.resize(1500, 616)        
        #print(str(execute.tsGlobal.symbols))
        ts = TS.SymbolTableDebug()
        ts.symbols.clear()
        
        try:
            execute.contador = 4  #for grapho   
            execute.currentAmbit = 'main'   #current ambit
            execute.currentParams = []  #list of parameters that the current function will have
            execute.semanticErrorList = []
            execute.tsGlobal = {}
            execute.lecturasRead = []       #sera modificada desde gui
            execute.la = 0
            execute.co = 0 
            execute.pasadas = 0
            self.textDebug.setPlainText("")
            tsDebug = {}
            printListDebug[:] = []
            instructionsDebug[:] = []
            conttadorIns = 0
            printPases[:] = []
            self.textEditConsole.setText("CONSOLE:\n")

            #region creations of reports
            fgraph = open('../reports/ast.dot','w+') #creamos el archivo
            fgraph.write("graph \"\"{ node [shape=box];\n")          
            fgraph.close()

            fgraph = open('../reports/graph.dot','w+') #creamos el archivo
            fgraph.write("graph \"\" {")
            fgraph.close()
            #endregion

            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            content += '\n'
            content.encode('utf-8')  #validation utf8
            result = grammar.parse(content)
            instructionsDebug = result[:]   #copio las instrucciones a la lista global

            # si exists errores lexicos o sintacticos traera una lista vacia            
            global data, dataS, dataSema, dataTs
            if len(result) == 0:
                Augus.setStyleSheet('QMainWindow{background-color: red; border: 1px solid black;}')
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setText("Este archivo contiene errores lexicos o sintacticos.")
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.exec()

                if len(grammar.LexicalErrosList) > 0:                    
                    data = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammar.LexicalErrosList:
                        data.append((str(i.lexema), str(i.column), str(i.line)))
                
                if len(grammar.sintacticErroList) > 0:                    
                    dataS = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammar.sintacticErroList:
                        dataS.append((str(i.lexema), str(i.column), str(i.line)))
            else:
                Augus.setStyleSheet('QMainWindow{background-color: green; border: 1px solid black;}')
             
            #region end to report
            fgraph = open('../reports/ast.dot','a') #agregamos al archivo '}'
            fgraph.write("}")
            fgraph.flush() 
            fgraph.close()

            fgraph = open('../reports/graph.dot','a') #agregamos al archivo '}'
            fgraph.write("}")
            fgraph.flush()
            fgraph.close()
          
            sys.stdout.flush()
            #endregion
            
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("Area Vacia.")
            self.msgBox.exec()

    def fn_Ejecutar_Ascendente(self):
        try:
            #region initialization
            global banderaDescAsc
            banderaDescAsc = True
            self.textEditConsole.setText("CONSOLE:\n")
            execute.contador = 4  #for grapho   
            execute.currentAmbit = 'main'   #current ambit
            execute.currentParams = []  #list of parameters that the current function will have
            execute.semanticErrorList = []
            execute.tsGlobal = {}
            execute.lecturasRead = []       #sera modificada desde gui
            execute.la = 0
            execute.co = 0 
            execute.pasadas = 0
            self.textDebug.setPlainText("")
            fgraph = open('../reports/ast.dot','w+') #creamos el archivo
            fgraph.write("graph \"\"{ node [shape=box];\n")          
            fgraph.close()
            #endregion

            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            content += '\n'  
            
            #obser = unicode(content)
            #content = content.decode('utf-8')
            content.encode('utf-8')

            result = grammar.parse(content)
            global instructionsList
            instructionsList = result[:]

            # si exists errores lexicos o sintacticos traera una lista vacia            
            global data, dataS, dataSema, dataTs
            if len(result) == 0:
                Augus.setStyleSheet('QMainWindow{background-color: red; border: 1px solid black;}')
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setText("Este archivo contiene errores lexicos o sintacticos.")
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.exec()

                if len(grammar.LexicalErrosList) > 0:                    
                    data = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammar.LexicalErrosList:
                        data.append((str(i.lexema), str(i.column), str(i.line)))
                
                if len(grammar.sintacticErroList) > 0:                    
                    dataS = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammar.sintacticErroList:
                        dataS.append((str(i.lexema), str(i.column), str(i.line)))
            else:
                Augus.setStyleSheet('QMainWindow{background-color: green; border: 1px solid black;}')
                #not exist errors                            
                execute.execute(result, self.textEditConsole)
                
                if len(execute.semanticErrorList) == 0:
                    
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText("Analisis Ascendente correcto.")
                    self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                    self.msgBox.exec()
                
                else:   
                    Augus.setStyleSheet('QMainWindow{background-color: red; border: 1px solid black;}')                
                    dataSema = [("DESCRIPCION", "COLUMNA", "LINEA")]
                    for i in execute.semanticErrorList:
                        dataSema.append((str(i.description), str(i.column), str(i.line)))
                    
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText("Existen errores semanticos.")
                    self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                    self.msgBox.exec()

            #region end to report
            fgraph = open('../reports/ast.dot','a') #agregamos al archivo '}'
            fgraph.write("}")
            fgraph.flush() 
            fgraph.close()
          
            sys.stdout.flush()
            #endregion
            
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("Area Vacia.")
            self.msgBox.exec()
    
    def fn_Ejecutar_Descendente(self):
        try:
            #region initialization
            global banderaDescAsc
            banderaDescAsc = False
            self.textEditConsole.setText("CONSOLE:\n")
            execute.contador = 4  #for grapho   
            execute.currentAmbit = 'main'   #current ambit
            execute.currentParams = []  #list of parameters that the current function will have
            execute.semanticErrorList = []
            execute.tsGlobal = {}
            execute.lecturasRead = []       #sera modificada desde gui
            execute.la = 0
            execute.co = 0 
            execute.pasadas = 0
            self.textDebug.setPlainText("")
            #endregion
            
            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            content += '\n'
            content.encode('utf-8')  #validation utf8
            result = grammarDesc.parse(content)
            global instructionsList  #save a all instructions for posterior use in graph astGenreal
            instructionsList = result[:]

            global data, dataS, dataSema, dataTs
            if len(result) == 0:
                Augus.setStyleSheet('QMainWindow{background-color: red; border: 1px solid black;}')
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setText("Este archivo contiene errores lexicos o sintacticos.")
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.exec()

                if len(grammarDesc.LexicalErrosList) > 0:                    
                    data = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammarDesc.LexicalErrosList:
                        data.append((str(i.lexema), str(i.column), str(i.line)))
                
                if len(grammarDesc.sintacticErroList) > 0:                    
                    dataS = [("LEXEMA", "COLUMNA", "LINEA")]
                    for i in grammarDesc.sintacticErroList:
                        dataS.append((str(i.lexema), str(i.column), str(i.line)))
            else:
                Augus.setStyleSheet('QMainWindow{background-color: green; border: 1px solid black;}')
                #not exist errors   
                execute.execute(result, self.textEditConsole)
                grammarDesc.lisInstructions[:] = []  
                
                if len(execute.semanticErrorList) == 0:
                    
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText("Analisis Descendente correcto.")
                    self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                    self.msgBox.exec()
                
                else:   
                    Augus.setStyleSheet('QMainWindow{background-color: red; border: 1px solid black;}')                
                    dataSema = [("DESCRIPCION", "COLUMNA", "LINEA")]
                    for i in execute.semanticErrorList:
                        dataSema.append((str(i.description), str(i.column), str(i.line)))
                    
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText("Existen errores semanticos.")
                    self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                    self.msgBox.exec()
  
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Empty Area.")
            self.msgBox.exec()

    def fn_Guardar(self):
        try:
            #content to save
            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            path = self.tabWidget.tabText(self.tabWidget.currentIndex())
            #print(path)
            print("writing to file.")
            f=open(path,"w")
            f.write(content)
            f.close()
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Archivo Guardado.")
            self.msgBox.exec()
        except:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Empty Area.")
            self.msgBox.exec()
    
    def fn_Guardar_Como(self):
        try:
            content = self.tabWidget.currentWidget().findChild(QtWidgets.QTextEdit,"textEdit").toPlainText()
            filename = QFileDialog.getSaveFileName(None)
            path = filename[0]
            
            print("writing to file.")
            f=open(path,"w+")
            f.write(content)
            f.close()

            #updating title on the tab
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), path)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Archivo Guardado.")
            self.msgBox.exec()
        except:
            print("closing file dialog")
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Empty Area.")
            self.msgBox.exec()

    def fn_Cerrar(self):
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        self.msg = QtWidgets.QMessageBox()
        self.msg.setText("Closed Table.")
        self.msg.exec()

    def fn_Salir(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setText("¡Good Bye!")
        self.msg.exec()
        sys.exit(1)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Augus = QtWidgets.QMainWindow()
    ui = Ui_Augus()
    ui.setupUi(Augus)
    Augus.show()
    sys.exit(app.exec_())
