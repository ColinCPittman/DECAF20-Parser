from VariableDecl import VariableDecl
from FunctionDecl import FunctionDecl
from Basic import Basic
from Basic import SyntaxErr

# variable or function
class Decl(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(Decl, self).__init__(tokens, tokenPosition)
        self.variableDecl = None
        self.functionDecl = None
        self.isVariableDecl = False
        self.process()

    def process(self):
        nTok = self.tokens[self.tokenPosition]
        nnTok = self.tokens[self.tokenPosition + 1]
        nnnTok = self.tokens[self.tokenPosition + 2]
        if (nTok.value in ["int", "double", "string", "bool", "void"]):
            if (nnTok.type == "T_Identifier"):
                if (nnnTok.value == '('):
                    self.functionDecl = FunctionDecl(self.tokens, self.tokenPosition)
                    self.tokenPositionProcessed = self.functionDecl.tokenPositionProcessed
                else:
                    self.isVariableDecl = True
                    self.variableDecl = VariableDecl(self.tokens, self.tokenPosition)
                    self.tokenPositionProcessed = self.variableDecl.tokenPositionProcessed
            else:
                raise Exception(SyntaxErr, nnTok)
        else:
            raise Exception(SyntaxErr, nTok)

    def print_tree(self, indent = 0): 
        if self.isVariableDecl:
            self.variableDecl.print_tree(indent)
        else:
            self.functionDecl.print_tree(indent)