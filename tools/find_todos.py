# tools/find_todos.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TODO_DIR = BASE / "data" / "todo"
REPORT_PATH = TODO_DIR / "integrity_report.json"
OUTPUT_PATH = TODO_DIR / "todo_list.md"


def run():
    print("Generating TODO list...\n")

    if not REPORT_PATH.exists():
        print("No integrity report found. Run the integrity checker first.")
        return

    try:
        report = json.load(open(REPORT_PATH, "r", encoding="utf-8"))
    except Exception as e:
        print("Error reading integrity report:", e)
        return

    # Build markdown output
    lines = []
    lines.append("# NetGrid TODO List\n")
    lines.append("Generated from integrity_report.json\n")
    lines.append("---\n")

    total_issues = 0

    for group, items in report.items():
        if not items:
            continue

        total_issues += len(items)

        lines.append(f"## {group} ({len(items)})\n")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")  # blank line

    if total_issues == 0:
        lines.append("🎉 **No issues found!** The dataset is clean.\n")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"TODO list written to: {OUTPUT_PATH}")
    print(f"Total issues: {total_issues}\n")


if __name__ == "__main__":
    run()
