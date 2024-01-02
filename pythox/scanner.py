import sys

from .token import Token, TokenType

class Scanner():
    def __init__(self, source: str):
        self.tokens: list[Token] = []
        self.start: int   = 0
        self.current: int = 0
        self.line: int    = 1
        self.column: int  = 1
        self.source: str  = source.strip()
        self._keywords: dict[str, TokenType] = {
        'and'    : TokenType.AND,
        'class'  : TokenType.CLASS,
        'else'   : TokenType.ELSE,
        'false'  : TokenType.FALSE,
        'fun'    : TokenType.FUN,
        'for'    : TokenType.FOR,
        'if'     : TokenType.IF,
        'nil'    : TokenType.NIL,
        'or'     : TokenType.OR,
        'print'  : TokenType.PRINT,
        'return' : TokenType.RETURN,
        'super'  : TokenType.SUPER,
        'this'   : TokenType.THIS,
        'true'   : TokenType.TRUE,
        'var'    : TokenType.VAR,
        'while'  : TokenType.WHILE}
    
    def scanTokens(self) -> list:
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF,
                                 "",
                                 None,
                                 self.line))
        return self.tokens

    def scanToken(self) -> None:
        c: str = self.advance()
        match c:
            case '(': self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)
            case '!': self.addToken(TokenType.BANG_EQUAL
                                    if self.match('=')
                                    else TokenType.BANG)
            case '=': self.addToken(TokenType.EQUAL_EQUAL
                                    if self.match('=')
                                    else TokenType.EQUAL)
            case '<': self.addToken(TokenType.LESS_EQUAL
                                    if self.match('=')
                                    else TokenType.LESS)
            case '>': self.addToken(TokenType.GREATER_EQUAL
                                    if self.match('=')
                                    else TokenType.GREATER)
            case '?': self.addToken(TokenType.QUESTION)
            case ':': self.addToken(TokenType.COLON)
            case '/': 
                if self.match('/'):
                    while self.peek() != '\n' and not self.isAtEnd():
                        self.advance()
                # elif self.match('*'): # FIXME: Convoluted garbage..refactor
                #     self.blockComment()
                else:
                    self.addToken(TokenType.SLASH)
            case ' ' | '\r' | '\t': pass
            case '\n': 
                self.line += 1
                self.column = 1
            case '"' : self.string()
            case  _  : 
                if self.isDigit(c):
                    self.number()
                elif self.isAlpha(c):
                    self.identifier()
                else:
                    print(f"Unexpected token {c} on line: {self.line}",
                          file=sys.stderr)
                    
                    print(self.printScanError(),
                          file=sys.stderr) # FIXME: Set hadError
                
    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.isAtEnd():
            print("Unterminated String", file=sys.stderr)
            return
        
        # Consume closing "
        self.advance()

        value: str = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)
    
    def number(self) -> None:
        while self.isDigit(self.peek()):
            self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        
        self.addToken(TokenType.NUMBER,
                      float(self.source[self.start : self.current]))

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        
        text: str = self.source[self.start : self.current]
        try:
            type: TokenType = self._keywords[text]
            self.addToken(TokenType(type))
        except KeyError:
            self.addToken(TokenType.IDENTIFIER)
        
    def blockComment(self) -> None:
        while not self.isAtEnd() and (self.peek != '*'):
            self.advance()
            if self.peek() == '\n':
                self.line += 1
        
        if self.isAtEnd():
            return None
        
        if not self.isAtEnd() and self.peek() == '*':
            self.advance()
            if not self.isAtEnd() and self.peek() == '/':
                self.advance()
            else:
                print(f"Unterminated comment on line: {self.line}",
                      self.printScanError(), sep='\n', file=sys.stderr)
        else:
            print(f"Unterminated comment on line: {self.line}",
                  self.printScanError(), sep='\n', file=sys.stderr)

    def advance(self) -> str:
        self.current += 1
        self.column  += 1
        return self.source[self.current - 1]
    
    def addToken(self, type: TokenType, literal: object=None):
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(TokenType(type),
                                 text,
                                 literal,
                                 self.line))
        
    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def isDigit(self, char: str) -> bool:
        return char >= '0' and char <= '9'
    
    def isAlpha(self, char: str) -> bool:
        return (char >= 'a' and char <= 'z') or \
               (char >= 'A' and char <= 'Z') or \
                char == '_'

    def isAlphaNumeric(self, char: str):
        return self.isAlpha(char) or self.isDigit(char)
    
    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]
    
    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def printScanError(self) -> str:
        # NOTE(donke): This stinks...might bite in the arse later
        # NOTE(donke): Seems like adding a column var is much easier
        # than wutteva da fock I was tryin'... wow
        src: list = self.source.split('\n')
        srcLine: str = src[self.line - 1]
        # column: int = 0
        # if len(src) == 1 or self.line == 1:
        #     column = self.current
        # else:
        #     parsed: int = sum([len(x) for x in src[0: self.line - 1]])
        #     column = self.current - parsed - 1 # Count the newline
        return f"{srcLine}\n{'-' * (self.column - 2)}^"
        
if __name__ == "__main__":
    # Tests!
    ...