from Basic import Basic
from Basic import SyntaxErr
from ExpressionSubnodes import AssignNode, BinaryExprNode, UnaryExprNode, CallNode, ConstantNode, FieldAccessNode

class Expressions(Basic):

    def __init__(self, tokens, tokenPosition):
        super(Expressions, self).__init__(tokens, tokenPosition)
        # top down recursive descent parsing
        self.expression_root = self._parse_assignment()
        self.tokenPositionProcessed = self.tokenPosition - 1 #Stmt throws error expecting to be after the seminicolon that an expression ends on, subtracting 1 here to account for this

    def _parse_assignment(self):
        # parse the left hand side of the assignment expression
        lhs = self._parse_logical_or()
        # check for assignment operator
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value == "=":
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_assignment()
            return AssignNode(lhs, operator, rhs)
        return lhs
    
    def _parse_logical_or(self):
        lhs = self._parse_logical_and()
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value == "||":
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_logical_or()
            return BinaryExprNode(lhs, operator, rhs, "LogicalExpr")
        return lhs

    def _parse_logical_and(self):
        lhs = self._parse_equality()
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value == "&&":
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_logical_and()
            return BinaryExprNode(lhs, operator, rhs, "LogicalExpr")
        return lhs
    
    def _parse_equality(self):
        lhs = self._parse_relational()
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value == "==":
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_equality()
            return BinaryExprNode(lhs, operator, rhs, "RelationalExpr")
        return lhs
    
    def _parse_relational(self):
        lhs = self._parse_arithmetic()
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value in ["<", ">", "<=", ">="]:
            operator = self.tokens[self.tokenPosition] 
            self.tokenPosition += 1
            rhs = self._parse_relational()
            return BinaryExprNode(lhs, operator, rhs, "RelationalExpr")
        return lhs
    
    # addition or subtraction
    def _parse_arithmetic(self):
        lhs = self._parse_multiplicative()
        if self.tokenPosition < len(self.tokens) and (self.tokens[self.tokenPosition].value == "+" or self.tokens[self.tokenPosition].value == "-"):
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_arithmetic()
            return BinaryExprNode(lhs, operator, rhs, "ArithmeticExpr")
        return lhs
    
    # multiplication or division
    def _parse_multiplicative(self):
        lhs = self._parse_unary()
        if self.tokenPosition < len(self.tokens) and (self.tokens[self.tokenPosition].value == "*" or self.tokens[self.tokenPosition].value == "/"):
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            rhs = self._parse_multiplicative()
            return BinaryExprNode(lhs, operator, rhs, "ArithmeticExpr")
        return lhs
    
    # logical not
    def _parse_unary(self):
        if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition].value == "!":
            operator = self.tokens[self.tokenPosition]
            self.tokenPosition += 1
            operand = self._parse_unary()
            return UnaryExprNode(operator, operand, "LogicalExpr")
        return self._parse_base()
    
    # at the base of the expression tree: could be a constant, an identifier, or a parentheses with an expression inside
    def _parse_base(self):
        current_token = self.tokens[self.tokenPosition]
        
        # literal value
        if current_token.is_constant:
            self.tokenPosition += 1
            variable = ConstantNode(current_token)
            return variable 

        # expression in parentheses
        elif current_token.value == "(":
            self.tokenPosition += 1 # skip '('
            expression = self._parse_assignment() 
            if self.tokens[self.tokenPosition].value != ")":
                raise Exception(SyntaxErr, self.tokens[self.tokenPosition])
            self.tokenPosition += 1 # skip ')'
            return expression 

        # identifier (variable name or function name)
        elif current_token.type == "T_Identifier":
            if self.tokenPosition < len(self.tokens) and self.tokens[self.tokenPosition + 1].value == "(":
                return self._parse_function_calls()
            else:
                self.tokenPosition += 1
                return FieldAccessNode(current_token)
            
        else:
            raise Exception(SyntaxErr, current_token)

    # function calls
    def _parse_function_calls(self):
        identifier = self.tokens[self.tokenPosition]
        self.tokenPosition += 2 # skip identifier and '('
        
        # no arguments
        if self.tokens[self.tokenPosition].value == ")":
            return CallNode(identifier, []) 
        
        arguments = [self._parse_assignment()]
        
        # parse additional arguments
        while self.tokens[self.tokenPosition].value == ",":
            self.tokenPosition += 1 # skip comma
            arguments.append(self._parse_assignment())

        # check for closing parenthesis
        if self.tokens[self.tokenPosition].value != ")":
            raise Exception(SyntaxErr, self.tokens[self.tokenPosition])
        self.tokenPosition += 1 # skip ')'

        return CallNode(identifier, arguments)
    
    def print_tree(self, indent = 0, label = ""):
        self.expression_root.print_tree(indent, label)