from Variable import Variable
from StmtBlock import StmtBlock
from Basic import SyntaxErr

class FunctionDecl(Variable, object):
    def __init__(self, tokens, tokenPosition):
        super(FunctionDecl, self).__init__(tokens, tokenPosition, True)
        self.formals = [] #variable objects
        self.hasFormals = False
        self.processFormals(self.tokenPosition + 3)
        self.stmtBlock = StmtBlock(tokens, self.tokenPositionProcessed + 1)
        self.tokenPositionProcessed = self.stmtBlock.tokenPositionProcessed
        self.type = tokens[tokenPosition].value
        self.identifier = tokens[tokenPosition + 1].value

    def processFormals(self, tokPosToProcess):
        variableList = []
        
        #there are no formals, closes immediately
        if self.tokens[tokPosToProcess].value == ")":
            self.tokenPositionProcessed = tokPosToProcess
            return variableList

        #process first formal
        variableList.append(Variable(self.tokens, tokPosToProcess))
        
        # process additional formals if present 
        while self.tokens[tokPosToProcess + 2].value == ",":
            tokPosToProcess += 3
            variableList.append(Variable(self.tokens, tokPosToProcess))

        # check if closing parentheses are after the formals
        if self.tokens[tokPosToProcess + 2].value != ")":
            raise Exception(SyntaxErr, self.tokens[tokPosToProcess + 2])

        self.formals = variableList
        self.hasFormals = len(variableList) != 0
        self.tokenPositionProcessed = tokPosToProcess + 2 # originally was "+= (tokPosToProcess + 2)"" but this was throwing errors because the tokenPositionProcessed was effectively doubling instead of incrementing
    
    # print tree can have return type, identifier, formals, and body
    def print_tree(self, indent = 0):
        line = self.tokens[self.tokenPosition].line
        
        # header
        print(f"{line} \t" + "\t" * indent  + "FnDecl:")

        # return type
        print(f"{line} \t" + "\t" * (indent + 1) + "(return type) Type: " + self.type)

        # identifier
        print(f"{line} \t" + "\t" * (indent + 1) + "Identifier: " + self.identifier)

        # formals are variables, so they need to be hard coded to print VarDecl to follow implementation and expected output
        for formal in self.formals:
            print(f"{line} \t" + "\t" * (indent + 1) + "(formals) VarDecl:")
            print(f"{line} \t" + "\t" * (indent + 2) + "Type: " + formal.type.value)
            print(f"{line} \t" + "\t" * (indent + 2) + "Identifier: " + formal.identifier)

        # body
        self.stmtBlock.print_tree(indent + 1, label = "(body) ")
