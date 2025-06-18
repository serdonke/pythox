from expr import *

from ttoken import TokenType

def print_ast(expr: Expr) -> str:
    match expr:
        case Binary(left, operator, right):
            return parenthesize(operator.lexeme, left, right)
        case Grouping(expression):
            return parenthesize("group", expression)
        case Literal(value):
            return str(value)
        case Unary(operator, right):
            return parenthesize(operator.lexeme, right)
        case Ternary(left, qmark, middle, colon, right):
            return parenthesize("?:", left, middle, right)
        case Logical(left, operator, right):
            return parenthesize(operator.lexeme, left, right)
        case Variable(name):
            return name.lexeme
        case Assign(name, value):
            return f"(assign {name.lexeme} {print_ast(value)})"
        case _:
            return "???"

def parenthesize(name: str, *exprs: Expr) -> str:
    parts = [print_ast(expr) for expr in exprs]
    return f"({name} {' '.join(parts)})"

if __name__ == "__main__":
    expr = Binary(
        left=Unary(
            operator=Token(TokenType.MINUS, "-", None, 1),
            right=Literal(123),
        ),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(
            expression=Literal(45.67),
        )
    )

    print(print_ast(expr))
