#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

CYBERKIN_INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"
REFERENCE_DIR = BASE / "docs" / "reference"

REFERENCE_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    index = load_json(CYBERKIN_INDEX)

    families = set()
    for ck_name, ck_info in index["cyberkin"].items():
        families.add(ck_info.get("family", "none").lower())

    for family_id in families:
        json_path = REFERENCE_DIR / f"{family_id}.json"
        md_path = REFERENCE_DIR / f"{family_id}.md"

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

        if not md_path.exists():
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# {family_id.capitalize()} Family Lore\n\n")

    print("Reference folder initialized.")


if __name__ == "__main__":
    main()
