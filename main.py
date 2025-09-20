import sys

class Token:
    def __init__(self, identifier, line, start_col, end_col, type, is_operator = False, is_constant = False, const_value = None):
        self.identifier = identifier
        self.line = line
        self.start_col = start_col
        self.end_col = end_col
        self.type = type
        self.is_operator = is_operator
        if is_constant is not False:
            self.is_constant = type == 'T_CHARCONSTANT' or type == 'T_INTCONSTANT' or type == 'T_STRINGCONSTANT'
        self.const_value = const_value

    def print_token(self):
        if not self.is_operator:
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type}")
        elif self.is_constant: 
            # the expected output shows that constant types repeat the value after the type (e.g. T_INTCONSTANT (value = 1))
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type} (value = {self.identifier})")
        else: 
            # the expected output shows that operators have their identifier printed in the stead of their type
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
    def _char_isletter(self):
        return self.input[self.index].isalpha() or self.input[self.index] == "_"

    # hex_lit     => "0" ( "x" | "X" ) { hex_digit }
    def _is_start_of_hex(self):
        return (self.index + 1 < len(self.input) # not out of bounds 
                    and (self.input[self.index] == '0' and 
                    (self.input[self.index + 1] == 'x' or self.input[self.index + 1] == "X"))) # is 0x or 0X

    # escaped_char => "\" ( "n" | "r" | "t" | "v" | "f" | "a" | "b" | `\` | "'" | `"` )
    def _is_escaped_char(self):
        return (self.index + 1 < len(self.input) and 
                self.input[self.index] == '\' and 
                self.input[self.index + 1] in ['n', 'r', 't', 'v', 'f', 'a', 'b', '\', "'", '"'])
    
    # char => all ASCII characters from 7 ... 13 and 32 ... 126 except char 10 "\n", char 92 "\" and char 34: "
    def _is_char(self):
        char_ordinal = ord(self.input[self.index])
        return ((7 <= char_ordinal <= 13) or (32 <= char_ordinal <= 126)) and char_ordinal not in [10, 92, 34]
    
    # char_lit_chars => all ASCII characters from 7 ... 13 and 32 ... 126 except char 39 "'" and char 92 "\"
    def _is_char_lit_chars(self):
        char_ordinal = ord(self.input[self.index])
        return ((7 <= char_ordinal <= 13) or (32 <= char_ordinal <= 126)) and char_ordinal not in [39, 92]
    
    #consume char and advance pointers
    def _advance(self):
        temp_char = self.input[self.index]
        self.index += 1
        self.col += 1
        return temp_char
       
    # primary method intented for public use to convert input file to a set of tokens, dispatches to helper functions
    def tokenize(self):
        while self.index < len(self.input):
            if (self.input[self.index] == "'" 
                    or self.input[self.index] == '"'
                    or self.input[self.index].isdigit()):
                self._scan_literals()
            elif self._char_isletter():
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

        #hexadecimal literals
        if self._is_start_of_hex(): 
            identifier += self._advance() + self._advance()  # consume ('0' and ('x' or 'X'))
            while self.index < len(self.input) and self.input[self.index].isxdigit():
                identifier += self._advance()
             self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_INTCONSTANT', is_const = True))

        #decimal literals
        elif self.input[self.index].isdigit():
             while self.index < len(self.input) and self.input[self.index].isdigit():
                identifier += self._advance()
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_INTCONSTANT', is_const = True))
        
        #string literals
        elif self.input[self.index] == '"':
            identifier += self._advance()
            while self.index < len(self.input) and self.input[self.index] != '"':
                if self._is_char() or self._is_escaped_char():
                #TODO
        else: # starts with a "'"
            pass

        while self.index < len(self.input):
            identifier += self._advance()
        
        self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'placeholder'))


    # this function generates tokens for identifiers and keywords
    # identifier => letter { letter | digit }
    def _scan_alphanum(self):
        initial_col = self.col
        identifier = ''
        while self.index < len(self.input) and (self._char_isletter() or self.input[self.index].isdigit()):
            identifier += self._advance()
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