# This file contains all the subnodes for the expressions as outlined in the expected output for the 3rd deliverable

class Node():
    def print_tree(self, indent=0):
        pass

class AssignNode(Node):
    def __init__(self, lhs, operator, rhs):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
    
    def print_tree(self, indent=0, label = ""):
        line = self.operator.line

        # header
        print(f"{line} \t" + "\t" * indent + label + "AssignExpr:")
        
        # left print
        self.lhs.print_tree(indent + 1)
        
        # operator print
        print(f"{line} \t" + "\t" * (indent + 1) + "Operator: " + self.operator.value)
        
        # right print
        self.rhs.print_tree(indent + 1)

# ArithmeticExpr, RelationalExpr, and LogicalExpr all share similar node structures in the expected output
class BinaryExprNode(Node):
    def __init__(self, lhs, operator, rhs, expr_type):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
        self.expr_type = expr_type
    
    def print_tree(self, indent = 0, label = ""):
        line = self.operator.line
        # header
        print(f"{line} \t" + "\t" * indent + label + self.expr_type + ":")
        
        # left print
        self.lhs.print_tree(indent + 1) 
        
        # operator print
        print(f"{line} \t" + "\t" * (indent + 1) + "Operator: " + self.operator.value)
        
        # right print
        self.rhs.print_tree(indent + 1)

# UnaryExprNode is used for negation and logical not
class UnaryExprNode(Node):
    def __init__(self, operator, operand, expr_type):
        self.operator = operator
        self.operand = operand
        self.expr_type = expr_type

    def print_tree(self, indent=0, label = ""):
        line = self.operator.line

        # header print
        print(f"{line} \t" + "\t" * indent + label + self.expr_type + ":")
        
        # operator
        print(f"{line} \t" + "\t" * (indent + 1) + "Operator: " + self.operator.value)
        
        # operand
        self.operand.print_tree(indent + 1)

# function calls
class CallNode(Node):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def print_tree(self, indent = 0, label = ""):
        line = self.identifier.line
        
        # header 
        print(f"{line} \t" + "\t" * indent + label + "Call:")
        
        # identifer
        print(f"{line} \t" + "\t" * (indent + 1) + "Identifier: " + self.identifier.value)
        
        # arguments print
        for argument in self.arguments:
            argument.print_tree(indent + 1, label="(actuals) ")

# int, boolean, and string constants
class ConstantNode(Node):
    def __init__(self, token):
        self.token = token

    def print_tree(self, indent = 0, label = ""):
        line = self.token.line
        type_name = self.token.type[2:] # remove the 'T_' prefix to match expected output
        print(f"{line} \t" + "\t" * indent + label + type_name + ": " + self.token.value)

class FieldAccessNode(Node):
    def __init__(self, variable):
        self.variable = variable
    
    def print_tree(self, indent=0, label=""):
        line = self.variable.line
        print(f"{line} \t" + "\t" * indent + label + "FieldAccess:")
        print(f"{line} \t" + "\t" * (indent + 1) + "Identifier: " + self.variable.value)
