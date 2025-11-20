from Basic import Basic
from Basic import SyntaxErr
from Expressions import Expressions
import Stmt as st

class WhileStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(WhileStmt, self).__init__(tokens, tokenPosition)
        # first token is "while", next checking for a '('
        if tokens[tokenPosition + 1].value != "(":
            raise Exception(SyntaxErr, tokens[tokenPosition + 1])
        
        # condition expression
        self.condition = Expressions(tokens, tokenPosition + 2)
        
        # ) 
        next_token_position = self.condition.tokenPositionProcessed + 1
        if tokens[next_token_position].value != ")":
            raise Exception(SyntaxErr, tokens[next_token_position])
        
        # body of the while statement
        self.body = st.Stmt(tokens, next_token_position + 1)
        self.tokenPositionProcessed = self.body.tokenPositionProcessed

