# variable declaration with semicolon
from Variable import Variable
from Basic import Basic
from Basic import SyntaxErr

class VariableDecl(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(VariableDecl, self).__init__(tokens, tokenPosition)
        self.variable = Variable(self.tokens, self.tokenPosition)
        
        if tokens[tokenPosition + 2].value == ";":
            self.semicolon = ";"
            self.tokenPositionProcessed = tokenPosition + 2
        else:
            raise Exception(SyntaxErr, tokens[tokenPosition + 2])

    def print_tree(self, indent = 0, label = ""):
        line = self.tokens[self.tokenPosition].line
        print(f"{line} \t" + "\t" * indent + label + "VarDecl:")  #label can be (formals)

        # type print
        # expected output omits some line numbers when printing some statements; printing line numbers here for consistency, though this breaks with the deliverable 3 output
        print(f"{line} \t" + "\t" * (indent + 1) + "Type: " + self.variable.type.value)

        # identifier print
        print(f"{line} \t" + "\t" * (indent + 1) + "Identifier: " + self.variable.identifier)


