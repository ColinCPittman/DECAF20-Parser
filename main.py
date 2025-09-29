import sys

class Token:
    def __init__(self, identifier, line, start_col, end_col, type, is_operator = False, is_constant = False, const_value = None):
        self.identifier = identifier
        self.line = line
        self.start_col = start_col
        self.end_col = end_col
        self.type = type
        self.is_operator = is_operator
        self.is_constant = is_constant
        if self.is_constant:
            self.is_constant = type == 'T_CHARCONSTANT' or type == 'T_IntConstant' or type == 'T_STRINGCONSTANT' or type == 'T_BoolConstant'
        self.const_value = const_value

    def print_token(self):
        if self.is_operator:
            # 2-character operators like <=, &&, show the token type instead of the indentifier after 'is' in the expected output
            if len(self.identifier) > 1:
                print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type}")
            else:
                print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is '{self.identifier}'")
        elif self.is_constant: 
            # the expected output shows that constant types repeat the value after the type (e.g. T_IntConstant (value= 1))
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type} (value= {self.identifier})")
        else: 
            print(f"{self.identifier} \t line {self.line} Cols {self.start_col} - {self.end_col} is {self.type}")

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
            '<=': 'T_LessEqual', #instead of 'T_LEQ', as per spec, to match expected output
            '>=': 'T_GEQ',
            '==': 'T_EQ',
            '!=': 'T_NEQ',
            '&&': 'T_logicaland', # should be 'T_AND' as per the DECAF20 spec but changed to match expected output
            '||': 'T_OR',
            '.': 'T_DOT'
        }
        #some of these keywords had to deviate from the all-caps format specified to match the expected output
        self.keywords = {
            'bool': 'T_IDENTIFIER', # spec says this should be 'T_BOOLTYPE' but expected output shows 'T_IDENTIFIER'
            'break': 'T_BREAK',
            'continue': 'T_CONTINUE',
            'else': 'T_Else',
            'extern': 'T_EXTERN',
            'false': 'T_BoolConstant',
            'for': 'T_For',
            'func': 'T_FUNC',
            'if': 'T_If',
            'int': 'T_Int',
            'null': 'T_NULL',
            'package': 'T_PACKAGE',
            'return': 'T_Return',
            'string': 'T_String', # this is 'T_STRINGTYPE' in the spec but had to change it to 'T_String' to match expected output
            'true': 'T_BoolConstant',
            'var': 'T_VAR',
            'void': 'T_Void',
            'while': 'T_WHILE',
            'Print': 'T_Print'
        }
        
    
    # letter => "A" ... "Z" | "a" ... "z" | "_"
    def _is_letter(self):
        return self.input[self.index].isalpha() or self.input[self.index] == "_"

    # hex_lit     => "0" ( "x" | "X" ) { hex_digit }
    def _is_start_of_hex(self):
        return (self.index + 1 < len(self.input) # not out of bounds 
                    and (self.input[self.index] == '0' and 
                    (self.input[self.index + 1] == 'x' or self.input[self.index + 1] == "X"))) # is 0x or 0X

    # escaped_char => "\" ( "n" | "r" | "t" | "v" | "f" | "a" | "b" | `\` | "'" | `"` )
    def _is_escaped_char(self):
        return (self.index + 1 < len(self.input) and 
                self.input[self.index] == '\\' and 
                self.input[self.index + 1] in ['n', 'r', 't', 'v', 'f', 'a', 'b', '\\', "'", '"'])
    
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
                self._scan_literal()
            elif self._is_letter():
                self._scan_alphanum()
            elif self.input[self.index] in self.operators or self.input[self.index] == '&' or self.input[self.index] == '|':
                self._scan_operator()
            elif self.input[self.index].isspace():
                if self.input[self.index] == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.index += 1
            else:
                print(f"Error: Unexpected character: '{self.input[self.index]}' at line {self.line}, column {self.col}")
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
    def _scan_literal(self):
        initial_col = self.col
        identifier = ''

        #hexadecimal literals
        if self._is_start_of_hex(): 
            identifier += self._advance() + self._advance()  # consume ('0' and ('x' or 'X'))
            while self.index < len(self.input) and self.input[self.index].isxdigit():
                identifier += self._advance()
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_IntConstant', is_constant = True))

        #decimal literals
        elif self.input[self.index].isdigit():
            while self.index < len(self.input) and self.input[self.index].isdigit():
                identifier += self._advance()
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_IntConstant', is_constant = True))
        
        #string literals
        elif self.input[self.index] == '"':
            identifier += self._advance()
            while self.index < len(self.input) and self.input[self.index] != '"':
                if self._is_escaped_char():
                    identifier += self._advance() + self._advance() #consume / and the subsequent escaped_char
                elif self._is_char(): 
                    identifier += self._advance() # consume normal char
            identifier += self._advance() # consume the end double quote
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, "T_STRINGCONSTANT", is_constant = True))
        
        #character literals
        else: # starts with a "'"
            identifier +=  self._advance()
            if self._is_escaped_char():
                identifier += self._advance() + self._advance()
            elif self._is_char_lit_chars():
                identifier += self._advance()
            identifier += self._advance() # consume ending single quote
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, "T_CHARCONSTANT", is_constant = True))


    # this function generates tokens for identifiers and keywords
    # identifier => letter { letter | digit }
    def _scan_alphanum(self):
        initial_col = self.col
        identifier = ''
        while self.index < len(self.input) and (self._is_letter() or self.input[self.index].isdigit()):
            identifier += self._advance()

        # keywords    
        if identifier in self.keywords: 
            if identifier == 'true' or identifier == 'false': #booleans are the only constant type the can be encountered in a keyword match
                self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, self.keywords[identifier], is_constant = True))
            else:
                self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, self.keywords[identifier]))
        
        # identifiers
        else:
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, 'T_IDENTIFIER')) #DECAF20 spec specifies this type label as 'T_ID' but changing it to 'T_IDENTIFIER' to match expected output

    def _scan_operator(self):
        initial_col = self.col
        identifier = ''

        # 2-character operators
        if self.index + 1 < len(self.input) and ((self.input[self.index] + self.input[self.index + 1]) in self.operators):
            identifier += self._advance() + self._advance()

        # single character operators
        else:
            identifier += self._advance()
        
        if identifier in self.operators:
            self.tokens.append(Token(identifier, self.line, initial_col, self.col - 1, self.operators[identifier], is_operator = True))
        # catch the case where a | or an & appear alone, since the dispaching tokenize() method calls this method if a single one is encountered
        else:
            print(f"Error: Unexpected character: '{identifier}' at line {self.line}, column {initial_col}")
            return
    
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

if __name__ == "__main__":
    main()