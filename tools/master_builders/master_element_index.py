#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
ABILITIES_ROOT = BASE / "data" / "abilities"
OUTPUT_DIR = BASE / "data" / "indexes"

IGNORE_FOLDERS = {".LEGACY"}


def load_abilities():
    abilities = {}

    for tier_folder in ABILITIES_ROOT.iterdir():
        if not tier_folder.is_dir() or tier_folder.name in IGNORE_FOLDERS:
            continue

        for file in tier_folder.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            ability = data.get("ability")
            if not ability:
                continue

            aid = ability.get("id")
            element = ability.get("element")

            if aid and element:
                abilities.setdefault(element, []).append(aid)

    for e in abilities:
        abilities[e].sort()

    return abilities


def write_index(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote index: {path}")


def main():
    print("Building element index...")

    element_index = load_abilities()

    write_index(OUTPUT_DIR / "master_element_index.json", element_index)

    print("Element index complete.")


if __name__ == "__main__":
    main()
