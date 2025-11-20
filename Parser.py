from Decl import Decl
from Basic import SyntaxErr

class ProgramNode:
    def __init__(self):
        self.decls = []
    def print_tree(self):
        print("Program:\n")
        for declaration in self.decls:
            declaration.print_tree()
    
    def print_tree(self): #head of the print tree
        print("Program:")
        for declaration in self.decls:
            declaration.print_tree() # indent starts at 0; line number printing has an indent baked in,



def print_error(token, lines, error_type = "syntax error"): 
        print(f"*** Error line {token.line}")
        print(lines[token.line - 1])
        print(f'{" " * (token.start_col - 1)}{"^" * (token.end_col - token.start_col + 1)}')
        print(f"*** {error_type}")

# entry point of parser
def parseTokens(tokens, contents):
    lines = contents.splitlines()
    tokenLength = len(tokens)
    if tokenLength== 0:
        print("Empty program is syntactically incorrect because it is empty.")
        return
    try:
        progrmNode = ProgramNode()
        tokenposition = 0
        while True:
            if tokenLength <= tokenposition:
                break
            decl = Decl(tokens,tokenposition)
            tokenposition = decl.tokenPositionProcessed +1
            progrmNode.decls.append(decl)
        return progrmNode, False
    except Exception as error:

        print_error(error.args[1],lines, error.args[0])
        return None, True # entry code returned " '','', True ", not needed for this implemenation

