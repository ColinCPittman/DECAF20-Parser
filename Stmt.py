from ForStmt import ForStmt
from IfStmt import IfStmt
from WhileStmt import WhileStmt
from BreakStmt import BreakStmt
from ReturnStmt import ReturnStmt
from PrintStmt import PrintStmt
from Expressions import Expressions
from Basic import Basic
from Basic import SyntaxErr
import StmtBlock as stb

class Stmt(Basic, object):
    def __init__(self, tokens, tokenPosition):

        super(Stmt, self).__init__(tokens, tokenPosition)
        
        if tokens[tokenPosition].value == "{":
            self.stmtblock = stb.StmtBlock(tokens, tokenPosition)
            self.stmtType = "block"
            self.tokenPositionProcessed = self.stmtblock.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_If".lower():
            self.ifStmt = IfStmt(tokens, tokenPosition)
            self.stmtType = "if"
            self.tokenPositionProcessed = self.ifStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_While".lower():
            self.wStmt = WhileStmt(tokens, tokenPosition)
            self.stmtType = "while"
            self.tokenPositionProcessed = self.wStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_For".lower():
            self.fStmt = ForStmt(tokens, tokenPosition)
            self.stmtType = "for"
            self.tokenPositionProcessed = self.fStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_Break".lower():
            self.bStmt = BreakStmt(tokens, tokenPosition)
            self.stmtType = "break"
            self.tokenPositionProcessed = self.bStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_Return".lower():
            self.rStmt = ReturnStmt(tokens, tokenPosition)
            self.stmtType = "return"
            self.tokenPositionProcessed = self.rStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_Print".lower():
            self.pStmt = PrintStmt(tokens, tokenPosition)
            self.stmtType = "print"
            self.tokenPositionProcessed = self.pStmt.tokenPositionProcessed

        elif tokens[tokenPosition].type.lower() == "T_Else".lower():
            raise Exception(SyntaxErr, tokens[tokenPosition])

        else:
            # any other expression is treated as an expression statement
            self.exp = Expressions(tokens, tokenPosition)
            self.stmtType = "exp"
            self.tokenPositionProcessed = self.exp.tokenPositionProcessed
            if tokens[self.tokenPositionProcessed + 1].value != ";":
                raise Exception(SyntaxErr, tokens[self.tokenPositionProcessed + 1])
            self.tokenPositionProcessed += 1

    def print_tree(self, indent = 0, label = ""):
        if self.stmtType == "block":
            self.stmtblock.print_tree(indent)
        elif self.stmtType == "if":
            self.ifStmt.print_tree(indent)
        elif self.stmtType == "while":
            self.wStmt.print_tree(indent)
        elif self.stmtType == "for":
            self.fStmt.print_tree(indent, label) # label need to pass through (step) from ForStmt
        elif self.stmtType == "break":
            self.bStmt.print_tree(indent)
        elif self.stmtType == "return":
            self.rStmt.print_tree(indent)
        elif self.stmtType == "print":
            self.pStmt.print_tree(indent)
        elif self.stmtType == "exp":
            self.exp.print_tree(indent)