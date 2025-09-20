import sys

class Scanner:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.col = 1
        self.line = 1
        self.index = 0
        self.operators = {'{', '}', '[', ']', ',', ';', '(', ')', 
                            '=', '-', '!', '+', '*', '/', '<<', '>>', '<',
                            '>', '<=', '>=', '==', '!=', '&&', '||', '.'}
        self.keywords = {
            'bool': 'T_BOOLTYPE',
            'break': 'T_BREAK',
            'continue': 'T_CONTINUE',
            'else': 'T_ELSE',
            'extern': 'T_EXTERN',
            'false': 'T_FALSE',
            'for': 'T_FOR',
            'func': 'T_FUNC',
            'if': 'T_IF',
            'int': 'T_INTTYPE',
            'null': 'T_NULL',
            'package': 'T_PACKAGE',
            'return': 'T_RETURN',
            'string': 'T_STRINGTYPE',
            'true': 'T_TRUE',
            'var': 'T_VAR',
            'void': 'T_VOID',
            'while': 'T_WHILE'
        }
        
    
    # letter => "A" ... "Z" | "a" ... "z" | "_"
    def _isletter(self, char):
        return char.isalpha or char == "_"

    def tokenize(self):
        while index < len(self.input):
            if self.input[self.index].isdigit():
                self._scan_literals()
            elif self.input[self.index].isalpha() or self.input[index] == '_':
                #scanning for identifers takes precedence over literals
                #scan_identifiers will hand over to _scan_keywords if it's a match
                self._scan_identifiers() 
            elif self.input[self.index] in self.operators:
                self._scan_operators()
            elif self.input[self.index] == ' ':
                self.col += 1
                index += 1
            elif self.input[self.index] == '\n':
                self.line += 1
                self.col = 1
                self.index += 1
            else:
                print(f"Error: Unexpected character: {self.input[self.index]} at row {self.line}, column {self.col}")
                return


    def _scan_literals(self):
        pass

    # identifier => letter { letter | digit }
    def _scan_identifiers(self):
        initial_col = self.col
        identifier = ''
        while self.index < len(self.input) and self._isletter(self.input[self.index]) or self.input[self.index].isdigit():
            identifier += input[self.index]
            self.index += 1
            self.col += 1
        if identifier in self.keywords:
            self._scan_keywords(identifier, initial_col)
        tokens += (identifier, self.line, initial_col, self.col, 'T_ID')

    def _scan_operators(self):
        pass
    
    def _scan_keywords(self, keyword = None, initial_col = None):
        if keyword is not None and initial_col  is not None:
            tokens += (keyword, self.line, initial_col, self.col, self.keywords[keyword])

    def print_tokens(self):
        for token in self.tokens:
            print(token)

def main():
    if len(sys.argv) != 2: #only 2 arguments should be provided
        print("Expected input: python main.py <input_file>")
        return
    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            contents = file.read()
            scanner = Scanner(contents)
            scanner.tokenize()
            scanner.print_tokens()
    except FileNotFoundError:
        print(f"{input_file} not found")