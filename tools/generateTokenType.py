tokens = [
    # Single-character tokens.
    ["LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
    "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",
    "QUESTION", "COLON"],

    # One or two character tokens.
    ["BANG", "BANG_EQUAL",
    "EQUAL", "EQUAL_EQUAL",
    "GREATER", "GREATER_EQUAL",
    "LESS", "LESS_EQUAL"],

    # Literals.
    ["IDENTIFIER", "STRING", "NUMBER"],

    # Keywords.
    ["AND", "CLASS", "ELSE", "FALSE", "FUN", "FOR", "IF", "NIL", "OR",
    "PRINT", "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE"],

    ["EOF"]
]
# Generate keyword hashmap (dicts in python)
print("keywords={", *map(lambda x: f"         '{x.lower()}':TokenType('{x}'),", tokens[3]), "}",sep='\n')

# Generate the TokenType class
print("from enum import StrEnum\n")
print("class TokenType(StrEnum):")
for token in tokens:
    print(*map(lambda x: f"    {x}='{x}'", token), sep='\n', end='\n')
    print()