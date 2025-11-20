from Basic import Basic
from Type import Type
from Basic import SyntaxErr

class Variable(Basic, object):
    def __init__(self, tokens, tokenPosition, isvoidallowed = False):
        super(Variable, self).__init__(tokens, tokenPosition)
        self.type = Type(tokens[tokenPosition], isvoidallowed)
        if tokens[tokenPosition + 1].type == "T_Identifier":
            self.identifier = tokens[tokenPosition + 1].value
        else:
            raise Exception(SyntaxErr, tokens[tokenPosition + 1])

