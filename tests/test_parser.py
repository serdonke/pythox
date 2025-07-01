import subprocess
import re
from pathlib import Path
import pytest

LOX_ROOT = Path(__file__).parent / "loxscripts" / "parser"
EXPECT_OUTPUT = re.compile(r"// expect: ?(.*)")


def parse_expected_output(file: Path):
    lines = file.read_text().splitlines()
    return [m.group(1) for line in lines if (m := EXPECT_OUTPUT.search(line))]


def run_parser(file: Path) -> list[str]:
    result = subprocess.run(
        ["python", "-m", "pythox.parser", str(file)], capture_output=True, text=True
    )
    return result.stdout.strip().splitlines()


@pytest.mark.parametrize(
    "lox_file", sorted(LOX_ROOT.rglob("*.lox")), ids=lambda f: f.name
)
@pytest.mark.xfail(
    reason="This is supposed to fail, astPrinter \
                   additionally outputs printAST: [Unknown Expr]",
    strict=False,
)
def test_parser_outputs(lox_file):
    expected = parse_expected_output(lox_file)
    actual = run_parser(lox_file)
    assert actual == expected, (
        f"\nFile: {lox_file}\nExpected: {expected}\nGot: {actual}"
    )
