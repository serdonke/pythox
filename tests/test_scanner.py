import pytest
from pathlib import Path
from tests.test_helper import run_scanner_test

LOX_ROOT = Path(__file__).parent / "loxscripts" / "scanning"
TEST_FILES = [p for p in LOX_ROOT.rglob("*.lox") if p.read_text().strip()]

@pytest.mark.parametrize("lox_file", TEST_FILES, ids=lambda f: f.name)
def test_scanner_outputs(lox_file: Path):
    run_scanner_test(lox_file)
