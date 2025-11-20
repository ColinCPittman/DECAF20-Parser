# handles "Print" statements
from Basic import Basic
from Basic import SyntaxErr
from Expressions import Expressions

class PrintStmt(Basic, object):
    def __init__(self, tokens, tokenPosition):
        super(PrintStmt, self).__init__(tokens, tokenPosition)
        self.expressions = []
        
        # print statement matched by call from Stmt, next check forchecking for a '('
        if tokens[tokenPosition + 1].value != "(":
            raise Exception(SyntaxErr, tokens[tokenPosition + 1])
        
        # parsing the first expression
        current_position = tokenPosition + 2 # first token in the parentheses
        self.expressions.append(Expressions(tokens, current_position))
        current_position = self.expressions[-1].tokenPositionProcessed + 1
        
        # parse any potential additional expressions separated by commas
        while tokens[current_position].value == ",":
            current_position += 1  # skip comma
            self.expressions.append(Expressions(tokens, current_position))

            #then update the current token position to the point after the positions advanced through the last expression
            current_position = self.expressions[-1].tokenPositionProcessed + 1
        
        # checking for a ')'
        if tokens[current_position].value != ")":
            raise Exception(SyntaxErr, tokens[current_position])
        
        # checking for a semicolon
        if tokens[current_position + 1].value != ";":
            raise Exception(SyntaxErr, tokens[current_position + 1])
        
        self.tokenPositionProcessed = current_position + 1

    def print_tree(self, indent = 0):
        line = self.tokens[self.tokenPosition].line
        print(f"{line} \t" + "\t" * indent + "PrintStmt:")
        for expression in self.expressions:
            expression.print_tree(indent + 1, label = "(args) ")