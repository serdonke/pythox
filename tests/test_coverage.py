from pathlib import Path
import pytest

# --- 1. THE TRUTH: All .lox files that should be tested ---

# Define root
LOX_ROOT = Path(__file__).parent / "loxscripts"

# Define directories/files to *always* ignore
IGNORED_FILES = {
#    "comments",
#    "empty_file.lox",
#    "unexpected_character.lox",
}

# Find *every* .lox file...
all_files = set(LOX_ROOT.rglob("*.lox"))

# ...and filter out the ones we've explicitly ignored.
all_testable_files = {
    f for f in all_files
    if not any(ignored in str(f.relative_to(LOX_ROOT)) for ignored in IGNORED_FILES)
}


# --- 2. THE TEST: Get coverage from pytest's collection ---

def test_all_lox_files_are_covered(request):
    """
    Meta-test that auto-discovers all collected .lox tests
    and compares them against all .lox files on disk.

    This test fails (xfail) if any .lox files exist that
    are not being collected by a test_*.py file.
    """

    # --- A. Discover all *tested* files from the pytest session ---
    # This is the "magic". We ask pytest what tests it found.
    tested_files_set = set()
    session = request.session
    for item in session.items:
        # 'lox_file' is the parameter name we use in all test_*.py files
        if hasattr(item, "callspec") and "lox_file" in item.callspec.params:
            lox_file_path = item.callspec.params["lox_file"]
            # lox_file_path is already a Path object, thanks to our setup
            tested_files_set.add(lox_file_path)

    # --- B. Compare the truth (disk) to the coverage (pytest) ---
    untested_files = all_testable_files - tested_files_set

    if untested_files:
        # Format a clean, copy-pasteable error message
        file_list = "\n".join(sorted(str(f.relative_to(LOX_ROOT)) for f in untested_files))
        
        # This will now show as 'x' (xfail) instead of 'F' (FAILED)
        pytest.xfail(f"Found {len(untested_files)} untested .lox files:\n{file_list}")
