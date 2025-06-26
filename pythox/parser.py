from .ttoken import Token, TokenType
from .expr import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        try:
            return self.expression()
        except ParseError as e:
            print(e)
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, 
                         TokenType.GREATER_EQUAL, 
                         TokenType.LESS, 
                         TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        print("BIG FUCCY WUCCY HAPPEN in pythox.parser.primary()")
        raise ParseError(f"[line {self.peek().line}] Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for ttype in types:
            if self.check(ttype):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        print("BIG FUCCY WUCCY HAPPEN in pythox.Parser.consume()")
        raise ParseError(f"[line {self.peek().line}] Error at '{self.peek().lexeme}': {message}")
        
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().tType == TokenType.SEMICOLON:
                return

            match self.peek().tType:
		        case TokenType.CLASS: return
		        case TokenType.FUN: return
		        case TokenType.VAR: return
		        case TokenType.FOR: return
		        case TokenType.IF: return
		        case TokenType.WHILE: return
		        case TokenType.PRINT: return
		        case TokenType.RETURN: return
		          
            self.advance()

    def check(self, ttype: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().tType == ttype

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().tType == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

class ParseError(Exception):
    pass

if __name__ in ("__main__"):
    import sys
    from .scanner import Scanner
    from .astPrinter import print_ast

    if len(sys.argv) < 2:
        print("Usage: python -m pythox.parser <file.lox>", file=sys.stderr)
        sys.exit(64)

    path = sys.argv[1]
    with open(path, "r") as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    parser = Parser(tokens)
    expr = parser.parse()

    if expr is not None:
        print(print_ast(expr))
