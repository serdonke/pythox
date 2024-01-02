import sys
from .scanner import Scanner

class Pythox():
    def __init__(self) -> None:
        self.hadError: bool = False
    
    def main(self) -> None:
        if len(sys.argv) > 2:
            print("Usage: pythox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
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

    def run(self, source: str) -> None:
        lexer  = Scanner(source)
        tokens = lexer.scanTokens()
        print(*tokens, sep='\n---xxx---\n\n')

    def error(self, line: int, message: str):
        self.report(line, "", message)
    
    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where} : {message}", 
              file=sys.stderr)
        self.hadError = True

if __name__ == "__main__":
    # Tests
    ...