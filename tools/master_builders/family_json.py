#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

CYBERKIN_INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"
REFERENCE_DIR = BASE / "docs" / "reference"
OUTPUT_DIR = BASE / "data" / "families"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    cyberkin_index = load_json(CYBERKIN_INDEX)

    families = {}
    for ck_name, ck_info in cyberkin_index["cyberkin"].items():
        family = ck_info.get("family", "none").lower()
        families.setdefault(family, []).append(ck_name)

    for family_id, members in families.items():
        ref_path = REFERENCE_DIR / f"{family_id}.json"
        ref_data = load_json(ref_path)

        family_json = {
            "family": family_id.capitalize(),
            "sector": ref_data.get("sector"),
            "type": ref_data.get("type"),
            "habitat": ref_data.get("habitat"),
            "themes": ref_data.get("themes", []),
            "evolution_requirements": ref_data.get("evolution_requirements", []),
            "quest_hooks": ref_data.get("quest_hooks", []),
            "example_abilities": ref_data.get("example_abilities", []),
            "members": members
        }

        out_path = OUTPUT_DIR / f"{family_id}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(family_json, f, indent=2)

    print("Family JSON generation complete.")


if __name__ == "__main__":
    main()
