import sys
from .scanner import Scanner

class Pythox():
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        if len(sys.argv) > 2:
            print("Usage: pythox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()

    def runFile(self, path: str) -> None:
        # TODO
        print("TODO")

    def runPrompt(self) -> None:
        while(True):
            try:
                print(">>> ", end='')
                line: str = input()
                if line == "": continue
                self.run(line)
            except KeyboardInterrupt:
                break

    def run(self, source: str) -> None:
        lexer  = Scanner(source)
        tokens = lexer.scanTokens()
        print(tokens)

if __name__ == "__main__":
    # Tests
    ...