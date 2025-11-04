import sys

from .expr import *
from .stmt import *
from .ttoken import TokenType


class Interpreter:
    def __init__(self, output_writer=sys.stdout.write):
        self.output_writer = output_writer

    def interpret(self, statements: list[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError_ as e:
            print(e)

    def execute(self, stmt: Stmt):
        match stmt:
            case Expression():
                self.evaluate(stmt.expression)
                return None
            case Print():
                value = self.evaluate(stmt.expression)
                self.output_writer(self.stringify(value) + "\n")
                return None

    def evaluate(self, expr: Expr):
        match expr:
            case Literal():
                return expr.value

            case Grouping():
                return self.evaluate(expr.expression)

            case Unary():
                right = self.evaluate(expr.right)

                match expr.operator.tType:
                    case TokenType.BANG:
                        return not self.isTruthy(right)
                    case TokenType.MINUS:
                        return -float(right)
                # Should never come here
                print("reached unreachable branch in Unary during AST eval")
                return None

            case Binary():
                left = self.evaluate(expr.left)
                right = self.evaluate(expr.right)
                match expr.operator.tType:
                    case TokenType.GREATER:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) > float(right)
                    case TokenType.GREATER_EQUAL:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) >= float(right)
                    case TokenType.LESS:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) < float(right)
                    case TokenType.LESS_EQUAL:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) <= float(right)
                    case TokenType.BANG_EQUAL:
                        return not self.isEqual(left, right)
                    case TokenType.EQUAL_EQUAL:
                        return self.isEqual(left, right)
                    case TokenType.MINUS:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) - float(right)
                    case TokenType.PLUS:
                        if isinstance(left, float) and isinstance(right, float):
                            return float(left) + float(right)
                        if isinstance(left, str) and isinstance(right, str):
                            return left + right

                        # WARN: Do we even reach here?
                        # Python is much more forgiving than java
                        raise RuntimeError_(
                            expr.operator, "Operands must be two numbers or two strings"
                        )
                    case TokenType.SLASH:
                        self.check_number_operands(expr.operator, left, right)
                        # Python ftw?
                        # Auto converts all division
                        # to floats
                        if right == 0.0:
                            raise RuntimeError_(expr.operator, "Division by zero.")
                        return left / right
                    case TokenType.STAR:
                        self.check_number_operands(expr.operator, left, right)
                        return float(left) * float(right)
                # Should never come here
                raise AssertionError("Unreachable: unexpected binary operator")

    def isTruthy(self, objecta) -> bool:
        if objecta is None:
            return False
        if isinstance(objecta, bool):
            return bool(objecta)
        return True

    def isEqual(self, objecta, objectb) -> bool:
        if objecta is None and objectb is None:
            return True
        if objecta is None:
            return False
        return objecta == objectb

    def stringify(self, objecta) -> str:
        if objecta is None:
            return "nil"
        if isinstance(objecta, float):
            text = str(objecta)
            if text.endswith(".0"):
                text = text[0:-2]
            return text
        if isinstance(objecta, bool):
            return "true" if objecta else "false"
        return str(objecta)

    def check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        raise RuntimeError_(operator, "Operand must be a number.")

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError_(operator, "Operands must be numbers.")


class RuntimeError_(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

    def __str__(self):
        return f"[line {self.token.line}] RuntimeError: {self.args[0]}"


if __name__ in ("__main__"):
    import sys
    from .scanner import Scanner
    from .parser import Parser

    if len(sys.argv) < 2:
        print("Usage: python -m pythox.interpreter <file.lox>", file=sys.stderr)
        sys.exit(64)

    path = sys.argv[1]
    with open(path, "r") as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    parser = Parser(tokens)
    expr = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(expr)
