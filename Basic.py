SyntaxErr = "syntax error"

class Basic:
    def __init__(self, tokens, tokenPosition):
        self.tokens = tokens
        self.tokenPosition = tokenPosition
        self.tokenPositionProcessed = tokenPosition
