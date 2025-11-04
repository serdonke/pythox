import pytest
from pathlib import Path
from tests.test_helper import run_interpreter_test

LOX_ROOT = Path(__file__).parent / "loxscripts" / "precedence"
TEST_FILES = [p for p in LOX_ROOT.rglob("*.lox") if p.read_text().strip()]

@pytest.mark.parametrize("lox_file", TEST_FILES, ids=lambda f: f.name)
def test_precedence_scripts(lox_file: Path):
    run_interpreter_test(lox_file)
