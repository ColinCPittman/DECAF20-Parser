from Basic import Basic
from Basic import SyntaxErr

class BreakStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        
        super(BreakStmt, self).__init__(tokens, tokenPosition)
  
        # break statement already matched by call from Stmt, next check for, next checking for semicolon
        if tokens[tokenPosition + 1].value != ";":
            raise Exception(SyntaxErr, tokens[tokenPosition + 1])
        
        self.tokenPositionProcessed = tokenPosition + 1

