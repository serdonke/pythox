import subprocess
import json
import sys
import re
import os
from pathlib import Path

def get_total_lox_files() -> int:
    """Gets the total number of testable .lox files."""
    lox_root = Path(__file__).parent.parent / "tests" / "loxscripts"
    
    # We are not ignoring any files, per your request
    ignored = {}

    all_files = set(lox_root.rglob("*.lox"))
    testable = {
        f for f in all_files
        if not any(ign in str(f.relative_to(lox_root)) for ign in ignored)
    }
    return len(testable)

def get_passing_tests_count() -> int:
    """
    Runs pytest quietly and parses the summary line for 'passed'.
    """
    print("Running pytest to count passing tests...")
    
    try:
        # We run 'pytest -q' and capture stdout.
        # We use 'check=False' because we don't care if it fails
        # (e.g., from the xfail), we just want the summary.
        result = subprocess.run(
            ["pytest", "-q"],
            capture_output=True,
            text=True,
            check=False,
        )
        
        output = result.stdout
        
        # Regex to find: "9 passed, 1 xfailed"
        match = re.search(r"(\d+) passed", output)
        
        if match:
            return int(match.group(1))
        else:
            # If no "passed" line is found, 0 tests passed.
            return 0
            
    except Exception as e:
        print(f"Error running pytest: {e}", file=sys.stderr)
        return 0

def main():
    """
    Generates the 'progress.json' file for the badge.
    """
    total_files = get_total_lox_files()
    passing_count = get_passing_tests_count()
    
    try:
        percentage = (passing_count / total_files) * 100
    except ZeroDivisionError:
        percentage = 0.0

    # Determine badge color
    color = "red"
    if percentage == 100:
        color = "success"
    elif percentage > 50:
        color = "yellow"
    elif percentage > 10:
        color = "orange"
        
    # Prepare JSON output for shields.io
    stats_json = {
        "schemaVersion": 1,
        "label": "Test Progress",
        "message": f"{passing_count} / {total_files} ({percentage:.1f}%)",
        "color": color,
    }

    # Write the *badge* JSON file
    output_path = Path(__file__).parent.parent / ".tests" / "progress.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(stats_json, f, indent=2)
        
    print(f"Stats successfully written to {output_path}")
    print(f"Summary: {passing_count} / {total_files} passing")

if __name__ == "__main__":
    main()
