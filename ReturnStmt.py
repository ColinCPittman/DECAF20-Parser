# return statement can inlcude an expression optionally 
from Basic import Basic
from Basic import SyntaxErr
from Expressions import Expressions

class ReturnStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(ReturnStmt, self).__init__(tokens, tokenPosition)
        self.withExpression = False
        
        # first token determined to be a return by the call from Stmt
        #  next, checking for an expression before semicolon
        if tokens[tokenPosition + 1].value != ";":
            self.expression = Expressions(tokens, tokenPosition + 1)
            self.withExpression = True
            self.tokenPositionProcessed = self.expression.tokenPositionProcessed
            
            # semicolon after expression
            if tokens[self.tokenPositionProcessed + 1].value != ";":
                raise Exception(SyntaxErr, tokens[self.tokenPositionProcessed + 1])
            
            self.tokenPositionProcessed += 1
        else:
            # just a return statement with a semicolon
            self.tokenPositionProcessed = tokenPosition + 1
        
    def print_tree(self, indent = 0):
        line = self.tokens[self.tokenPosition].line
        print(f"{line} \t" + "\t" * indent + "ReturnStmt:")
        
        if self.withExpression:
            self.expression.print_tree(indent + 1, label = "(args) ")
