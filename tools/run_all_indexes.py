#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
BUILDERS_DIR = BASE / "master_builders"
INDEX_BUILDERS = [
    "master_ability_stats.py",
    "master_index.py",
    "master_move_learnset.py",
    "master_element_index.py",
    "cyberkin_page.py",
    "family_index.py",
    "family_json.py",
    "family_markdown.py"
]


def run_builder(script_name):
    script_path = BUILDERS_DIR / script_name
    if not script_path.exists():
        print(f"[WARN] Missing builder: {script_path}")
        return 1

    print(f"\n=== Running {script_name} ===")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode


def main():
    print("======================================")
    print("  CYBERKIN MASTER INDEX BUILD SYSTEM")
    print("======================================\n")

    failures = 0

    for builder in INDEX_BUILDERS:
        code = run_builder(builder)
        if code != 0:
            failures += 1

    print("\n======================================")
    print("  FINAL INDEX BUILD SUMMARY")
    print("======================================\n")

    if failures == 0:
        print("✔ All index builders completed successfully.")
        return 0
    else:
        print(f"❌ {failures} builder(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
