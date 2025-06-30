from dataclasses import dataclass

from .expr import Expr


class Stmt:
    pass


@dataclass(frozen=True, slots=True)
class Expression(Stmt):
    expression: Expr


@dataclass(frozen=True, slots=True)
class Print(Stmt):
    expression: Expr
