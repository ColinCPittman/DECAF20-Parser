from Basic import Basic
from Basic import SyntaxErr
from Expressions import Expressions
import Stmt as st

# currently unmodified aside from correcting the typo "tokenPostion" in entry code
class ForStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(ForStmt, self).__init__(tokens, tokenPosition)
        self.hasFirstExp = False
        self.hasLastExp = False
        self.check_left_par()
        self.check_first_exp()
        self.check_middle_exp()
        self.check_last_exp()
        self.set_stmt()

    def check_left_par(self):
        ntok = self.tokens[self.tokenPosition + 1]
        if ntok.value != "(":
            raise Exception(SyntaxErr, ntok)
        self.tokenPositionProcessed = self.tokenPosition + 1

    def check_first_exp(self):
        ntok = self.tokens[self.tokenPositionProcessed + 1]
        if ntok.value != ";":
            firstexp = Expressions(self.tokens, self.tokenPositionProcessed + 1)
            self.firstexp = firstexp
            self.hasFirstExp = True
            self.tokenPositionProcessed = firstexp.tokenPositionProcessed

        self.tokenPositionProcessed += 1

    def check_middle_exp(self):
        ntok = self.tokens[self.tokenPositionProcessed + 1]
        if ntok.value != ";":
            middleexp = Expressions(self.tokens, self.tokenPositionProcessed + 1)
            self.middleexp = middleexp
            self.tokenPositionProcessed = middleexp.tokenPositionProcessed
        else:
            raise Exception(SyntaxErr, ntok)
        self.tokenPositionProcessed += 1

    def check_last_exp(self):
        ntok = self.tokens[self.tokenPositionProcessed + 1]
        if ntok.value != ")":
            lastexp = Expressions(self.tokens, self.tokenPositionProcessed + 1)
            self.lastexp = lastexp
            self.hasLastExp = True
            self.tokenPositionProcessed = lastexp.tokenPositionProcessed
        self.tokenPositionProcessed += 1

    def set_stmt(self):
        stmt = st.Stmt(self.tokens, self.tokenPositionProcessed + 1)
        self.tokenPositionProcessed = stmt.tokenPositionProcessed
        self.stmt = stmt

    def print_tree(self, indent = 0, label = ""):
        line = self.tokens[self.tokenPosition].line
        print(f"{line} \t" + "\t" * indent + label + "ForStmt:")

        # first expression
        if self.hasFirstExp:
            self.firstexp.print_tree(indent + 1, label = "(init) ")

        # condition expression
        self.middleexp.print_tree(indent + 1, label = "(test) ")
        
        # fori increment
        if self.hasLastExp:
            self.lastexp.print_tree(indent + 1, label = "(step) ")
        
        self.stmt.print_tree(indent + 1)