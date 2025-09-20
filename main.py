import sys

class Token:
    def __init__(self, identifier, line, start_col, end_col, type, is_operator = False, is_constant = False):
        self.identifier = identifier
        self.line = line
        self.start_col = start_col
        self.end_col = end_col
        self.type = type
        self.is_operator = is_operator
        self.is_constant = type == 'T_CHARCONSTANT' or type == 'T_INTCONSTANT' or type == 'T_STRINGCONSTANT'

    def print_token(self):
        if not self.is_operator:
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type}")
        elif self.is_constant: 
            # the expected output shows that constant types repeat the value after the type (e.g. T_INTCONSTANT (value = 1))
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type} (value = {self.identifier})")
        else: 
            # the expected output shows that operators aren't printed with their type
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is '{self.identifier}'")

class Scanner:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.col = 1
        self.line = 1
        self.index = 0
        self.operators = {
            '{': 'T_LCB',
            '}': 'T_RCB', 
            '[': 'T_LSB',
            ']': 'T_RSB',
            ',': 'T_COMMA',
            ';': 'T_SEMICOLON',
            '(': 'T_LPAREN',
            ')': 'T_RPAREN',
            '=': 'T_ASSIGN',
            '-': 'T_MINUS',
            '!': 'T_NOT',
            '+': 'T_PLUS',
            '*': 'T_MULT',
            '/': 'T_DIV',
            '<<': 'T_LEFTSHIFT',
            '>>': 'T_RIGHTSHIFT',
            '<': 'T_LT',
            '>': 'T_GT',
            '<=': 'T_LEQ',
            '>=': 'T_GEQ',
            '==': 'T_EQ',
            '!=': 'T_NEQ',
            '&&': 'T_AND',
            '||': 'T_OR',
            '.': 'T_DOT'
        }
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
    def _char_isletter(self, char):
        return char.isalpha() or char == "_"

    def _is_start_of_hex(self):
        return (self.index + 1 < len(self.input) # not out of bounds 
                    and (self.input[self.index] == '0' and 
                    (self.input[self.index + 1] == 'x' or self.input[self.index + 1] == "X"))) # is 0x or 0X
       
    def tokenize(self):
        while self.index < len(self.input):
            if (self.input[self.index] == "'" 
                    or self.input[self.index] == '"'
                    or self.input[self.index].isdigit()):
                self._scan_literals()
            elif self._char_isletter(self.input[self.index]):
                self._scan_alphanum()
            elif self.input[self.index] in self.operators:
                self._scan_operators()
            elif self.input[self.index] == ' ':
                self.col += 1
                self.index += 1
            elif self.input[self.index] == '\n':
                self.line += 1
                self.col = 1
                self.index += 1
            else:
                print(f"Error: Unexpected character: {self.input[self.index]} at row {self.line}, column {self.col}")
                return

     
    # Integer Literals:
    # _______________________________________________________
    # int_lit     => decimal_lit | hex_lit .
    # decimal_lit => { decimal_digit }+ .
    # hex_lit     => "0" ( "x" | "X" ) { hex_digit }
    #
    # Character Literals:
    # _______________________________________________________
    # char_lit     => "'" ( char_lit_chars | escaped_char ) "'" .
    # escaped_char => "\" ( "n" | "r" | "t" | "v" | "f" | "a" | "b" | `\` | "'" | `"` )
    # 
    # String Literals:
    # _______________________________________________________
    # string_lit   => `"` { char | escaped_char } `"` .
    #
    def _scan_literals(self):
        initial_col = self.col
        identifier = ''

        if self._is_start_of_hex(): 
            identifier += self.input[self.index] + self.input[self.index + 1]
            self.index += 2
            self.col += 2
            while self.index < len(self.input) and self.input[self.index].isxdigit():
                identifier += self.input[self.index]
                self.index += 1
                self.col += 1
             self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_INTCONSTANT'))

        elif self.input[self.index].isdigit():
             while self.index < len(self.input) and self.input[self.index].isdigit():
                identifier += self.input[self.index]
                self.index += 1
                self.col += 1
            self.tokens.append(Token(identifier, self.line, initial_col, self.col -1, 'T_INTCONSTANT'))
            
        elif self.input[self.index] == '"':
            pass
        else: # starts with a "'"
            pass

        while self.index < len(self.input):
            identifier += self.input[self.index]
            self.index += 1
            self.col += 1
        
        self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'placeholder'))


    # this function generates tokens for identifiers and keywords
    # identifier => letter { letter | digit }
    def _scan_alphanum(self):
        initial_col = self.col
        identifier = ''
        while self.index < len(self.input) and (self._char_isletter(self.input[self.index]) or self.input[self.index].isdigit()):
            identifier += self.input[self.index]
            self.index += 1
            self.col += 1
        if identifier in self.keywords:
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, self.keywords[identifier]))
        else:
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_ID'))

    def _scan_operators(self):
        pass
    
    def print_tokens(self):
        for token in self.tokens:
            token.print_token()

def main():
    if len(sys.argv) != 2: 
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