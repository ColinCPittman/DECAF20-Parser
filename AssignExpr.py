from Basic import Basic
from Expressions import Expressions
from Basic import SyntaxErr
class AssignExpr(Basic):
    def __init__(self, tokens, tokenPosition):
        super(AssignExpr, self).__init__(tokens, tokenPosition)

        # tokenPosition should point to an indentifier and the next token should be determined to be an "="
        self.expression = Expressions(tokens, tokenPosition + 2)
        token_position_after_expression = self.expression.tokenPositionProcessed
        
        if tokens[token_position_after_expression + 1].identifier != ";":
            raise Exception(SyntaxErr, tokens[token_position_after_expression + 1])
            
        self.tokenPositionProcessed = token_position_after_expression + 1
