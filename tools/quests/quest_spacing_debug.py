import sys
from pathlib import Path

def debug_file(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")  # IMPORTANT: preserves blank lines

    print(f"\n=== DEBUG: {path.name} ===\n")

    for i, line in enumerate(lines):
        blank = "(blank)" if line.strip() == "" else ""
        print(f"{i:03d}: {repr(line)} {blank}")

    print("\n=== HEADER POSITIONS ===")
    for i, line in enumerate(lines):
        if line.startswith("## "):
            print(f"Header at line {i}: {line}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quest_spacing_debug.py <file>")
        sys.exit(1)

    debug_file(Path(sys.argv[1]))
