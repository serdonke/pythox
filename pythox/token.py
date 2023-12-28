from enum import StrEnum

class TokenType(StrEnum):
    LEFT_PAREN='LEFT_PAREN' 
    RIGHT_PAREN='RIGHT_PAREN'
    LEFT_BRACE='LEFT_BRACE'
    RIGHT_BRACE='RIGHT_BRACE'
    COMMA='COMMA'
    DOT='DOT'
    MINUS='MINUS'
    PLUS='PLUS'
    SEMICOLON='SEMICOLON'
    SLASH='SLASH'
    STAR='STAR'
    QUESTION='QUESTION'
    COLON='COLON'

    BANG='BANG'
    BANG_EQUAL='BANG_EQUAL'
    EQUAL='EQUAL'
    EQUAL_EQUAL='EQUAL_EQUAL'
    GREATER='GREATER'
    GREATER_EQUAL='GREATER_EQUAL'
    LESS='LESS'
    LESS_EQUAL='LESS_EQUAL'

    IDENTIFIER='IDENTIFIER'
    STRING='STRING'
    NUMBER='NUMBER'
    
    AND='AND'
    CLASS='CLASS'
    ELSE='ELSE'
    FALSE='FALSE'
    FUN='FUN'
    FOR='FOR'
    IF='IF'
    NIL='NIL'
    OR='OR'
    PRINT='PRINT'
    RETURN='RETURN'
    SUPER='SUPER'
    THIS='THIS'
    TRUE='TRUE'
    VAR='VAR'
    WHILE='WHILE'

    EOF='EOF'

class Token:
    def __init__(self, tType: TokenType, lexeme: str, literal: object, line:int):
        self.tType   = tType
        self.lexeme  = lexeme
        self.literal = literal
        self.line    = line
        
    def __repr__(self) -> str:
        return f"{self.tType} {self.lexeme} {self.literal}"
    
    def __str__(self) -> str:
        return f"Type: {self.tType}\nLexeme: {self.lexeme}\nLiteral: {self.literal}"

if __name__ == "__main__":
    # Tests!
    token: TokenType = TokenType("SLASH")
    print(token)
    token1: Token = Token(TokenType("STAR"), '*', None, 1)
    print(token1)

# TokenType = Enum("TokenType", [
#             # Single-character tokens.
#             "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
#             "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",

#             # One or two character tokens.
#             "BANG", "BANG_EQUAL",
#             "EQUAL", "EQUAL_EQUAL",
#             "GREATER", "GREATER_EQUAL",
#             "LESS", "LESS_EQUAL",

#             # Literals.
#             "IDENTIFIER", "STRING", "NUMBER",

#             # Keywords.
#             "AND", "CLASS", "ELSE", "FALSE", "FUN", "FOR", "IF", "NIL", "OR",
#             "PRINT", "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE",

#             "EOF"])