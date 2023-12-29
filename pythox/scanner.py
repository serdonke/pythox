import sys
from .token import Token, TokenType

class Scanner():
    def __init__(self, source: str):
        self.tokens: list = []
        self.start: int   = 0
        self.current: int = 0
        self.line: int    = 1
        self.source: str  = source.strip()
    
    def scanTokens(self) -> list:
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType("EOF"),
                                 "",
                                 None,
                                 self.line))
        return self.tokens

    def scanToken(self) -> None:
        c: str = self.advance()
        match c:
            case '(': self.addToken(TokenType("LEFT_PAREN"))
            case ')': self.addToken(TokenType("RIGHT_PAREN"))
            case '{': self.addToken(TokenType("LEFT_BRACE"))
            case '}': self.addToken(TokenType("RIGHT_BRACE"))
            case ',': self.addToken(TokenType("COMMA"))
            case '.': self.addToken(TokenType("DOT"))
            case '-': self.addToken(TokenType("MINUS"))
            case '+': self.addToken(TokenType("PLUS"))
            case ';': self.addToken(TokenType("SEMICOLON"))
            case '*': self.addToken(TokenType("STAR"))
            case '!': self.addToken(TokenType("BANG_EQUAL")
                                    if self.match('=')
                                    else TokenType("BANG"))
            case '=': self.addToken(TokenType("EQUAL_EQUAL")
                                    if self.match('=')
                                    else TokenType("EQUAL"))
            case '<': self.addToken(TokenType("LESS_EQUAL")
                                    if self.match('=')
                                    else TokenType("LESS"))
            case '>': self.addToken(TokenType("GREATER_EQUAL")
                                    if self.match('=')
                                    else TokenType("GREATER"))
            case '?': self.addToken(TokenType("QUESTION"))
            case ':': self.addToken(TokenType("COLON"))
            case '/': 
                if self.match('/'):
                    while self.peek() != '\n' and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType("SLASH"))
            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1
            case  _ : print(f"Unexpected token {c} on line: {self.line}:{self.current}\n",
                            f"{self.source}\n", # FIXME: Not fool-proof, defer to a method
                            "-" * (self.current - 1), "^\n",
                            file=sys.stderr, sep='') # FIXME: Set hadError

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    
    # def addToken(self, type: TokenType):
    #     self.addToken(type, None)
    
    def addToken(self, type: TokenType, literal: object=None):
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(TokenType(type),
                                 text,
                                 literal,
                                 self.line))
        
    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def match(self, expected: str) -> bool:
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]
    
if __name__ == "__main__":
    # Tests!
    ...