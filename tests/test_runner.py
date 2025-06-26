import subprocess
import re
from pathlib import Path
import pytest

LOX_ROOT = Path(__file__).parent / "loxscripts"
EXPECT_OUTPUT = re.compile(r"// expect: ?(.*)")

def collect_lox_files(folder: str):
    """Return a list of .lox files under a given subfolder like 'scanning'."""
    return sorted((LOX_ROOT / folder).rglob("*.lox"))

def parse_expected_output(lox_file: Path):
    lines = lox_file.read_text().splitlines()
    return [m.group(1) for line in lines if (m := EXPECT_OUTPUT.search(line))]

def run_lox_file(lox_file: Path) -> list[str]:
    result = subprocess.run(
        ["python","-m" "pythox.scanner", str(lox_file)],
        capture_output=True, text=True
    )
    return result.stdout.strip().splitlines()

def run_test_for_file(lox_file: Path):
    expected = parse_expected_output(lox_file)
    actual = run_lox_file(lox_file)
    assert actual == expected, f"File: {lox_file}\nExpected: {expected}\nGot: {actual}"


@pytest.mark.parametrize("lox_file", 
                         collect_lox_files("scanning"), 
                         ids=lambda f: f.name)
def test_scanning_folder(lox_file):
    run_test_for_file(lox_file)

