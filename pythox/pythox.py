import os
import sys

from .scanner import Scanner
from .parser import Parser
from .astPrinter import print_ast, parenthesize

fancyPrompt: bool = True
try:
    # This is real Prompt engineering
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from rich.console import Console
    import os
except ModuleNotFoundError:
    fancyPrompt = False

class Pythox():
    def __init__(self) -> None:
        self.hadError: bool = False
    
    def main(self) -> None:
        if len(sys.argv) > 2:
            print("Usage: pythox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
        elif fancyPrompt:
            self.runFancyPrompt()
        else:
            self.runPrompt()

    def runFile(self, filepath: str) -> None:
        # TODO: Add error handling
        with open(filepath, 'r') as file:
            src = file.read()
            self.run(src)
            if self.hadError: 
                sys.exit(65)

    def runPrompt(self) -> None:
        while(True):
            try:
                try:
                    line: str = input(">>> ")
                except EOFError:
                    continue
                if line == "":
                    continue
                self.run(line)
                self.hadError = False
            except KeyboardInterrupt:
                break

    def runFancyPrompt(self) -> None:
        console = Console()
        history_path = os.path.expanduser("./.pythox_history")
        session = PromptSession(">>> ", history=FileHistory(history_path))

        while True:
            try:
                line: str = session.prompt()
                if line.strip() == "":
                    continue
                self.run(line)
                self.hadError = False
            except KeyboardInterrupt:
                console.print("[bold red]Why you do that?[/bold red]")
                continue
            except EOFError:
                console.print("[bold cyan]Goodbye.[/bold cyan]")
                break
            except Exception as e:
                console.print(f"[bold red]Unhandled Error:[/bold red] {e}")

    def run(self, source: str) -> None:
        lexer  = Scanner(source)
        tokens = lexer.scanTokens()

        parser = Parser(tokens)
        expression = parser.parse()

        print(print_ast(expression))
        #print(*tokens, sep='\n---xxx---\n\n')

    def error(self, line: int, message: str):
        self.report(line, "", message)
    
    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where} : {message}", 
              file=sys.stderr)
        self.hadError = True

if __name__ == "__main__":
    # Tests
    ...
