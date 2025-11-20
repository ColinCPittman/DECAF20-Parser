# for a block of statements with { }

from VariableDecl import VariableDecl
from Basic import Basic
from Basic import SyntaxErr
import Stmt as st

class StmtBlock(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(StmtBlock, self).__init__(tokens, tokenPosition)
        self.variableDecls = []
        self.stmts = []

        varTokenPostion = self.tokenPosition + 1

        if self.tokens[self.tokenPosition].value == "{":
            
            while True:
                if self.tokens[varTokenPostion].value == "}":

                    self.tokenPositionProcessed = varTokenPostion
                    break
                
                current_token = self.tokens[varTokenPostion]
                next_token = self.tokens[varTokenPostion + 1]
                
                if (current_token.value in ["int", "double", "string", "bool"]) and (next_token.type == "T_Identifier"):
                    variableDecl = VariableDecl(self.tokens, varTokenPostion)
                    self.tokenPositionProcessed = variableDecl.tokenPositionProcessed
                    varTokenPostion = self.tokenPositionProcessed + 1
                    self.variableDecls.append(variableDecl)
                
                else:
                    stmt = st.Stmt(self.tokens, varTokenPostion)
                    self.tokenPositionProcessed = stmt.tokenPositionProcessed
                    varTokenPostion = self.tokenPositionProcessed + 1
                    self.stmts.append(stmt)
        else:
            raise Exception(SyntaxErr, self.tokens[self.tokenPosition])

    def print_tree(self, indent = 0, label = ""):
        line = self.tokens[self.tokenPosition].line

        # header
        print(f"{line} \t" + "\t" * indent + label + "StmtBlock:") # label can be (body)

        # variable declarations 
        for variableDecl in self.variableDecls:
            variableDecl.print_tree(indent + 1)

        # statements
        for stmt in self.stmts:
            stmt.print_tree(indent + 1)
