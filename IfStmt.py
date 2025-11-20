from Basic import Basic
from Basic import SyntaxErr
from Expressions import Expressions
import Stmt as st

# this class is called in Stmt, used after an if statement is encountered
# deliverable 3 stores the condition of the if statement, the then statement, and 
# the else statement. They are printed sequentially (in present) in t4.out
class IfStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(IfStmt, self).__init__(tokens, tokenPosition)
        self.withElse = False
        
        # if statement matched by a call from Stmt, next check for "("
        if tokens[tokenPosition + 1].value != "(":
            raise Exception(SyntaxErr, tokens[tokenPosition + 1])
        
        # condition expr
        self.condition = Expressions(tokens, tokenPosition + 2)
        
        #  )
        next_token_position = self.condition.tokenPositionProcessed + 1
        if tokens[next_token_position].value != ")":
            raise Exception(SyntaxErr, tokens[next_token_position])
        
        # 'then' statement
        self.thenStmt = st.Stmt(tokens, next_token_position + 1)
        
        self.tokenPositionProcessed = self.thenStmt.tokenPositionProcessed
        
        #  else clause could optionally appear
        if (self.tokenPositionProcessed + 1 < len(tokens) and 
            tokens[self.tokenPositionProcessed + 1].type.lower() == "T_Else".lower()):
            self.withElse = True
            self.elseStmt = st.Stmt(tokens, self.tokenPositionProcessed + 2)
            self.tokenPositionProcessed = self.elseStmt.tokenPositionProcessed

    def print_tree(self, indent = 0):
        line = self.tokens[self.tokenPosition].line
        print(f"{line} \t" + "\t" * indent + "IfStmt:")
        
        # condition print
        self.condition.print_tree(indent + 1, label = "(test) ")

        # then statement
        self.thenStmt.print_tree(indent + 1)

        # else statement
        if self.withElse:
            self.elseStmt.print_tree(indent + 1)