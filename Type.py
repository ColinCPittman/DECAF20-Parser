from Basic import SyntaxErr
# verifies that the type of a variable is valid
class Type:
    def __init__(self, token, isvoidallowed = False):
        self.token = token

        # only FunctionDecl passes true as third parameter to indicate 'void' type is allowed as a type
        self.isvoidallowed = isvoidallowed
        self.value = token.value 
        if self.value not in {"int", "string", "bool", "void", "double"}:
            raise Exception(SyntaxErr, self.token)
        if isvoidallowed == False and self.value == "void":
            raise Exception(SyntaxErr, self.token)
