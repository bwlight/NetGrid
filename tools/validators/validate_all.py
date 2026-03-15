"""
NetGrid — Master Validation Runner

This script automatically discovers and runs every validator script in this
directory whose filename starts with 'validate_'.

Why this design works well:
- You never need to edit this file when adding new validators.
- Any new validator (e.g., validate_maps.py, validate_quests.py) is picked up
  automatically as long as it follows the naming pattern.
- Each validator runs in its own subprocess, so failures don't break the runner.
- Output is grouped and readable.

To add a new validator:
1. Create a file named validate_<something>.py in this folder.
2. That's it — the master script will run it automatically.
"""

import argparse
import subprocess
import sys
import time
import json
from pathlib import Path

# ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def color(text, code, enabled):
    return f"{code}{text}{RESET}" if enabled else text


def run_validator(path):
    start = time.time()
    proc = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True
    )
    end = time.time()
    return proc.returncode, proc.stdout + proc.stderr, end - start


def main():
    parser = argparse.ArgumentParser(description="NetGrid Master Validator")

    # Short flags for common actions
    parser.add_argument("-v", "--validator", help="Run only a specific validator")
    parser.add_argument("-s", "--skip", nargs="*", help="Skip specific validators")
    parser.add_argument("-e", "--only-errors", action="store_true", help="Show only errors")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress live output")
    parser.add_argument("-c", "--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("-f", "--fail-fast", action="store_true", help="Stop on first failure")
    parser.add_argument("-t", "--timing", action="store_true", help="Show timing for each validator")

    # Long‑form flags for advanced behavior
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--summary-only", action="store_true", help="Only show summary")
    parser.add_argument("--errors-only", action="store_true", help="Only show final error report")
    parser.add_argument("--list", action="store_true", help="List all validators and exit")
    parser.add_argument("--root", help="Override project root")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without executing")
    parser.add_argument("--ci", action="store_true", help="CI mode: quiet + fail-fast + json")
    parser.add_argument("--exit-zero", action="store_true", help="Always exit with code 0")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--no-legacy-skip", action="store_true", help="Validate .LEGACY folders")

    args = parser.parse_args()

    # CI mode overrides
    if args.ci:
        args.quiet = True
        args.fail_fast = True
        args.json = True

    use_color = not args.no_color

    # Determine root
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    validator_dir = root / "validators"

    # Collect validators
    validators = sorted(
        p for p in validator_dir.glob("validate_*.py")
        if p.name != "validate_all.py"
        and (args.no_legacy_skip or ".LEGACY" not in p.parts)
    )

    # List mode
    if args.list:
        for v in validators:
            print(v.name)
        return

    # Filter by --validator
    if args.validator:
        validators = [v for v in validators if v.name == args.validator]

    # Skip list
    if args.skip:
        validators = [v for v in validators if v.name not in args.skip]

    # Dry run
    if args.dry_run:
        print("Would run:")
        for v in validators:
            print(" -", v.name)
        return

    results = []
    error_log = []

    if not args.summary_only:
        print(color("\n=== NetGrid Full Validation ===\n", YELLOW, use_color))

    # Run validators
    for v in validators:
        if not args.quiet and not args.summary_only:
            print(color(f"--- Running {v.name} ---", YELLOW, use_color))

        code, output, duration = run_validator(v)

        # Live output
        if not args.quiet and not args.summary_only:
            for line in output.splitlines():
                if args.only_errors and not line.startswith("[ERROR]"):
                    continue
                if line.startswith("[ERROR]"):
                    print(color(line, RED, use_color))
                elif line.startswith("[OK]"):
                    print(color(line, GREEN, use_color))
                else:
                    print(line)

        # Collect errors
        for line in output.splitlines():
            if line.startswith("[ERROR]"):
                error_log.append(f"{v.name}: {line}")

        results.append({
            "name": v.name,
            "returncode": code,
            "output": output,
            "duration": duration
        })

        if args.fail_fast and code != 0:
            break

        if not args.quiet and not args.summary_only:
            if code == 0:
                print(color(f"[OK] {v.name} passed.\n", GREEN, use_color))
            else:
                print(color(f"[FAIL] {v.name} failed.\n", RED, use_color))

    # Summary
    failed = [r for r in results if r["returncode"] != 0]

    if not args.errors_only:
        print(color("=== Validation Summary ===", YELLOW, use_color))
        print(f"{len(results) - len(failed)} / {len(results)} validators passed.\n")

    # JSON output
    if args.json:
        print(json.dumps({"results": results, "errors": error_log}, indent=2))
        sys.exit(0 if args.exit_zero else (1 if failed else 0))

    # Error report
    if error_log:
        print(color("=== Error Report ===", RED, use_color))
        for err in error_log:
            print(color(err, RED, use_color))
        print()
        sys.exit(0 if args.exit_zero else 1)

    print(color("All validators passed successfully.", GREEN, use_color))
    sys.exit(0)


if __name__ == "__main__":
    main()
