from .token import Token, TokenType

class Scanner():
    def __init__(self, source: str):
        self.tokens: list = []
        self.start: int   = 0
        self.current: int = 0
        self.line: int    = 1
        self.source: str  = source
    
    def scanTokens(self) -> list:
        return self.tokens

if __name__ == "__main__":
    # Tests!
    ...