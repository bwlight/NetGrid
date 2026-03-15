#!/usr/bin/env python3
import os
import json
from pathlib import Path

# ============================================================
#  EXCLUSION SETTINGS
#  Add or remove paths here. These are matched as substrings.
# ============================================================

EXCLUDE_PATHS = [
    "node_modules",
    ".github",
    ".pytest_cache",
    ".vscode",
    ".git",
    ".venv",
    "__pycache__",
    "tools/",  # example: skip builders if desired
]

EXCLUDE_FILES = [
    "README.md",
    "LICENSE",
]

# ============================================================
#  FILE TYPES TO SCAN
#  Add or remove extensions as needed.
# ============================================================

SCAN_EXTENSIONS = {
    ".py", ".json", ".md", ".txt", ".js", ".ts", ".yaml", ".yml"
}

# ============================================================
#  PROJECT ROOT
# ============================================================

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "data" / "indexes" / "todo_report.json"


def should_exclude(path: Path) -> bool:
    """Return True if the file or folder should be excluded."""
    path_str = str(path).replace("\\", "/")

    for excl in EXCLUDE_PATHS:
        if excl in path_str:
            return True

    if path.name in EXCLUDE_FILES:
        return True

    return False


def scan_file(path: Path):
    """Return list of (line_number, line_text) for TODOs in a file."""
    todos = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if "TODO" in line:
                    todos.append((i, line.rstrip()))
    except Exception:
        return []
    return todos


def main():
    print(f"Scanning for TODOs under: {BASE}\n")

    results = {}

    for root, dirs, files in os.walk(BASE):
        root_path = Path(root)

        # Skip excluded directories
        if should_exclude(root_path):
            continue

        for file in files:
            file_path = root_path / file

            # Skip excluded files
            if should_exclude(file_path):
                continue

            # Skip non-target extensions
            if file_path.suffix.lower() not in SCAN_EXTENSIONS:
                continue

            todos = scan_file(file_path)
            if todos:
                results[str(file_path)] = [
                    {"line": ln, "text": text} for ln, text in todos
                ]

    # Write JSON report
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Console summary
    if not results:
        print("✔ No TODOs found in the project.")
        return

    print("=== TODO REPORT SUMMARY ===")
    print(f"Files with TODOs: {len(results)}")
    total = sum(len(v) for v in results.values())
    print(f"Total TODO entries: {total}")
    print(f"\nReport written to: {OUTPUT}")


if __name__ == "__main__":
    main()
