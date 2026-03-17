#!/usr/bin/env python3
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
ABILITIES_ROOT = BASE / "data" / "abilities"
CYBERKIN_ROOT = BASE / "data" / "cyberkin"
OUTPUT_DIR = BASE / "data" / "indexes"

IGNORE_FOLDERS = {".LEGACY"}


def load_abilities():
    index = {}

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

            ability_id = ability.get("id")
            name = ability.get("name")

            if ability_id and name:
                index[ability_id] = name

    return dict(sorted(index.items()))


def load_cyberkin():
    index = {}
    family_map = {}

    for stage_folder in CYBERKIN_ROOT.iterdir():
        if not stage_folder.is_dir() or stage_folder.name in IGNORE_FOLDERS:
            continue

        stage = stage_folder.name.lower()

        for file in stage_folder.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            ck = data.get("cyberkin")
            if not ck:
                continue

            name = ck.get("name")
            element = ck.get("element")
            family = ck.get("family", "").lower()

            abilities = ck.get("abilities", {})
            flat_abilities = []

            for group in ["basic", "advanced", "signature", "ultimate"]:
                group_list = abilities.get(group)
                if isinstance(group_list, list):
                    flat_abilities.extend(group_list)
                elif isinstance(group_list, str):
                    flat_abilities.append(group_list)

            index[name] = {
                "stage": stage,
                "element": element,
                "family": family,
                "abilities": sorted(flat_abilities)
            }

            if family:
                family_map.setdefault(family, []).append(name)

    # Sort families alphabetically
    for fam in family_map:
        family_map[fam] = sorted(family_map[fam])

    return (
        dict(sorted(index.items())),
        dict(sorted(family_map.items()))
    )


def write_index(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote index: {path}")


def main():
    print("Building master indexes...")

    abilities = load_abilities()
    cyberkin, families = load_cyberkin()

    write_index(OUTPUT_DIR / "abilities_index.json", {"abilities": abilities})
    write_index(OUTPUT_DIR / "cyberkin_index.json", {"cyberkin": cyberkin})
    write_index(OUTPUT_DIR / "family_index1scheckme.json", {"families": families})

    print("Master index build complete.")


if __name__ == "__main__":
    main()
