from dataclasses import dataclass

from .ttoken import Token

class Expr:
    pass

@dataclass(frozen=True, slots=True)
class Assign(Expr):
    name: Token
    value: Expr

@dataclass(frozen=True, slots=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(frozen=True, slots=True)
class Grouping(Expr):
    expression: Expr

@dataclass(frozen=True, slots=True)
class Literal(Expr):
    # Hmmm should we use object?
    value: float | str | bool | None

@dataclass(frozen=True, slots=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(frozen=True, slots=True)
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass(frozen=True, slots=True)
class Ternary(Expr):
    left: Expr
    qmark: Token
    middle: Expr
    colon: Token
    right: Expr

@dataclass(frozen=True, slots=True)
class Variable(Expr):
    name: Token

