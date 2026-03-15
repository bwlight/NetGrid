#!/usr/bin/env python3
import subprocess
import sys
import os
import json
import time
import hashlib
from pathlib import Path

C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_BOLD = "\033[97;1m"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
VALIDATORS = BASE / "validators"

ABILITY_VALIDATOR = VALIDATORS / "validate_abilities.py"
CYBERKIN_VALIDATOR = VALIDATORS / "validate_cyberkin_abilities.py"

SUMMARY_JSON = BASE / "pipeline_summary.json"
PRECOMMIT_HOOK = ROOT / ".git" / "hooks" / "pre-commit"

WATCH_PATHS = [
    ROOT / "data" / "abilities",
    ROOT / "data" / "cyberkin",
    ROOT / "schemas"
]


def run_step(label, command_path):
    print(f"\n{C_BLUE}{C_BOLD}=== {label} ==={C_RESET}")
    print(f"{C_BOLD}Running:{C_RESET} {command_path}\n")

    result = subprocess.run(
        [sys.executable, str(command_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode, result.stdout


def hash_tree(paths):
    h = hashlib.sha256()
    for p in paths:
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "rb") as fh:
                        h.update(fh.read())
                except:
                    pass
    return h.hexdigest()


def install_precommit():
    hook = f"""#!/bin/sh
echo "Running Cyberkin content pipeline..."
python3 tools/pipeline.py
if [ $? -ne 0 ]; then
    echo "Commit blocked: pipeline failed."
    exit 1
fi
"""
    PRECOMMIT_HOOK.parent.mkdir(parents=True, exist_ok=True)
    with open(PRECOMMIT_HOOK, "w") as f:
        f.write(hook)
    os.chmod(PRECOMMIT_HOOK, 0o755)
    print(f"{C_GREEN}✔ Installed Git pre-commit hook.{C_RESET}")


def auto_fix_missing(stdout):
    lines = stdout.splitlines()
    in_block = False
    missing = []  # (name, tier, element)

    for line in lines:
        if "=== MISSING ABILITIES ===" in line:
            in_block = True
            continue
        if in_block:
            if not line.strip():
                break
            parts = line.split("—")
            if len(parts) >= 3:
                name = parts[0].strip()
                tier = parts[1].strip()
                element = parts[2].strip()
                missing.append((name, tier, element))

    if not missing:
        print(f"{C_YELLOW}No missing abilities to auto-fix.{C_RESET}")
        return

    print(f"\n{C_YELLOW}Auto-creating stubs for missing abilities:{C_RESET}")
    for name, tier, element in missing:
        print(f"  - {name} ({tier}, {element})")
        subprocess.run([
            sys.executable,
            str(BASE / "create_ability.py"),
            "--tier", tier,
            "--element", element,
            "--stub",
            name
        ])

    print(f"{C_GREEN}✔ Auto-fix complete.{C_RESET}")


def run_pipeline(auto_fix=False):
    print(f"{C_BOLD}{C_BLUE}======================================")
    print(" CYBERKIN CONTENT PIPELINE")
    print("======================================\n" + C_RESET)

    results = {}

    ability_status, _ = run_step("ABILITY VALIDATION", ABILITY_VALIDATOR)
    results["abilities"] = ability_status

    cyberkin_status, cyberkin_out = run_step("CYBERKIN VALIDATION", CYBERKIN_VALIDATOR)
    results["cyberkin"] = cyberkin_status

    if auto_fix and cyberkin_status != 0:
        auto_fix_missing(cyberkin_out)

    print(f"\n{C_BOLD}{C_BLUE}======================================")
    print(" FINAL PIPELINE SUMMARY")
    print("======================================\n" + C_RESET)

    for key, status in results.items():
        if status == 0:
            print(f"{C_GREEN}✔ {key.capitalize()} validation passed.{C_RESET}")
        else:
            print(f"{C_RED}❌ {key.capitalize()} validation failed.{C_RESET}")

    with open(SUMMARY_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n{C_GREEN}✔ Wrote summary to {SUMMARY_JSON}{C_RESET}")

    if any(status != 0 for status in results.values()):
        print(f"\n{C_RED}❌ PIPELINE FAILED — Fix errors and re-run.{C_RESET}")
        return 1

    print(f"\n{C_GREEN}✔ PIPELINE PASSED — All content validated successfully.{C_RESET}")
    return 0


def watch():
    print(f"{C_YELLOW}Watching for changes... (Ctrl+C to stop){C_RESET}")
    last_hash = hash_tree(WATCH_PATHS)

    while True:
        time.sleep(1)
        new_hash = hash_tree(WATCH_PATHS)
        if new_hash != last_hash:
            print(f"\n\n{C_YELLOW}{C_BOLD}=== CHANGE DETECTED ==={C_RESET}")
            run_pipeline()
            last_hash = new_hash


if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch()
    elif "--install-hook" in sys.argv:
        install_precommit()
    elif "--fix" in sys.argv:
        sys.exit(run_pipeline(auto_fix=True))
    else:
        sys.exit(run_pipeline())
