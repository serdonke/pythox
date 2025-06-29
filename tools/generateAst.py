from pathlib import Path
import sys

def main():
    outputDir = Path(__file__).resolve().parent.parent / "pythox"
    if outputDir.exists() and outputDir.is_dir():
        print(f"\033[32mOutputting in {outputDir}\033[0m")
    else:
        outputDir = Path(__file__).resolve().parent
        print(f"\033[31mOutputting to tools dir\033[0m", file=sys.stderr)
    
    expr: dict = {"Assign"   : "Token name, Expr value",
                  "Binary"   : "Expr left, Token operator, Expr right",
                  "Grouping" : "Expr expression",
                  "Literal"  : "object value",
                  "Logical"  : "Expr left, Token operator, Expr right",
                  "Unary"    : "Token operator, Expr right",
                  "Ternary"  : "Expr left, Token qmark, Expr middle, Token colon, Expr right",
                  "Variable" : "Token name"}
    defineAst(outputDir, "expr", expr)

    stmt: dict = {"Expression": "Expr expression", "Print": "Expr expression"}
    defineAst(outputDir, "stmt", stmt)

def defineAst(outputDir: Path, baseName: str, types: dict[str, str]):
    path = outputDir / f"{baseName}.py"
    with open(path, "w") as f:
        f.write("from dataclasses import dataclass\n\n")
        f.write("from .ttoken import Token\n\n")

        f.write(f"class {baseName.capitalize()}:\n")
        f.write("    pass\n\n")

        for className, fieldList in types.items():
            fields = [field.strip() for field in fieldList.split(',')]
            f.write(f"@dataclass(frozen=True, slots=True)\n")
            f.write(f"class {className}({baseName.capitalize()}):\n")
            for field in fields:
                tType, name = field.split(' ')
                if tType == "object":
                     f.write(f"    # Hmmm should we use {tType}?\n")
                     # Doing something similar in Token Class
                     # Kinda follows the spec methinks
                     f.write(f"    {name}: float | str | bool | None\n")
                     continue

                f.write(f"    {name}: {tType}\n")
            f.write("\n")

        print(f"\033[34mWrote {path.name}!\033[0m")

if __name__ == "__main__":
    main()
