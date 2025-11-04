import io
import re
from pathlib import Path

# Import your actual compiler components
from pythox.scanner import Scanner
from pythox.parser import Parser, ParseError
from pythox.interpreter import Interpreter, RuntimeError_
from pythox.astPrinter import print_ast

# --- 1. The Expectation Parser (Copied once) ---
def parse_expectations(source: str) -> tuple[list[str], str | None, str | None]:
    """Parses stdout, parse error, and runtime error expectations."""
    expected_stdout = []
    expected_parse_error = None
    expected_runtime_error = None
    
    # [line 2] Error at 'this': Expect variable name.
    PARSE_ERR_RE = re.compile(r"// \[line \d+\] Error at .+: (.+)")
    # expect runtime error: Undefined variable 'notDefined'.
    RUNTIME_ERR_RE = re.compile(r"// expect runtime error: (.+)")
    # expect: some output
    STDOUT_RE = re.compile(r"// expect: ?(.*)")

    for line in source.splitlines():
        if m := RUNTIME_ERR_RE.search(line):
            expected_runtime_error = m.group(1).strip()
        elif m := PARSE_ERR_RE.search(line):
            expected_parse_error = m.group(1).strip()
        elif m := STDOUT_RE.search(line):
            expected_stdout.append(m.group(1).lstrip())
            
    return expected_stdout, expected_parse_error, expected_runtime_error

# --- 2. The Interpreter (Full Pipeline) Test Runner ---
def run_interpreter_test(lox_file: Path):
    """Runs the full Scan -> Parse -> Interpret pipeline in-memory."""
    source = lox_file.read_text()
    expected_stdout, expect_parse_err, expect_runtime_err = parse_expectations(source)

    stdout_capture = io.StringIO()
    
    # 1. Scanner
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    # 2. Parser
    try:
        parser = Parser(tokens)
        statements = parser.parse()
    except ParseError as e:
        if expect_parse_err:
            assert expect_parse_err in str(e), f"Parse error mismatch.\nExpected: {expect_parse_err}\nGot: {e}"
            return # Test passed
        raise e # Unexpected parse error

    if expect_parse_err:
        assert False, f"Expected parse error '{expect_parse_err}' but got none."

    # 3. Interpreter
    try:
        interpreter = Interpreter(output_writer=stdout_capture.write)
        interpreter.interpret(statements)
    except RuntimeError_ as e:
        if expect_runtime_err:
            assert expect_runtime_err in str(e), f"Runtime error mismatch.\nExpected: {expect_runtime_err}\nGot: {e}"
            return # Test passed
        raise e # Unexpected runtime error

    if expect_runtime_err:
        assert False, f"Expected runtime error '{expect_runtime_err}' but got none."
        
    # 4. Assert Stdout
    actual_stdout = stdout_capture.getvalue().strip().splitlines()
    assert actual_stdout == expected_stdout, f"Stdout mismatch.\nGot: {actual_stdout}\nExpected: {expected_stdout}"

# --- 3. The Scanner-Only Test Runner ---
def run_scanner_test(lox_file: Path):
    """Runs *only* the scanner and compares token output."""
    source = lox_file.read_text()
    expected_stdout, _, _ = parse_expectations(source)

    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    
    actual_stdout = []
    for t in tokens:
        literal = "null" if t.literal is None else str(t.literal)
        actual_stdout.append(f"{t.tType.name} {t.lexeme} {literal}")

    assert actual_stdout == expected_stdout, f"Scanner output mismatch.\nGot: {actual_stdout}\nExpected: {expected_stdout}"

# --- 4. The Parser-Only (AST) Test Runner ---
def run_parser_test(lox_file: Path):
    """Runs Scan -> Parse and compares the AST print-out."""
    source = lox_file.read_text()
    expected_stdout, expect_parse_err, _ = parse_expectations(source)

    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    
    try:
        parser = Parser(tokens)
        statements = parser.parse()
    except ParseError as e:
        if expect_parse_err:
            assert expect_parse_err in str(e), f"Parse error mismatch.\nExpected: {expect_parse_err}\nGot: {e}"
            return # Test passed
        raise e

    if expect_parse_err:
        assert False, f"Expected parse error '{expect_parse_err}' but got none."

    # This part is tricky. The original test printed 'printAST: [Unknown Expr]'
    # We will just print the first statement for simplicity.
    # If you have multiple statements, you may need to adjust this.
    if statements:
        actual_stdout = [print_ast(statements[0].expression)]
    else:
        actual_stdout = []
        
    assert actual_stdout == expected_stdout, f"Parser AST output mismatch.\nGot: {actual_stdout}\nExpected: {expected_stdout}"
