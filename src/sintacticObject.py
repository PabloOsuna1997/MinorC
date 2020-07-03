class sintacticObject:
    ''' this class represent an object sintactic'''

class sinOb(sintacticObject):
        def __init__(self, lexema, line, column):
            self.lexema = lexema
            self.column = column
            self.line = line