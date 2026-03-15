#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
ABILITIES_ROOT = BASE / "data" / "abilities"
CYBERKIN_ROOT = BASE / "data" / "cyberkin"
OUTPUT_DIR = BASE / "data" / "indexes"

IGNORE_FOLDERS = {".LEGACY"}


def load_ability_names():
    names = {}

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

            name = ability.get("name")
            if name:
                names[name] = True

    return list(sorted(names.keys()))


def load_cyberkin():
    ck_map = {}

    for stage_folder in CYBERKIN_ROOT.iterdir():
        if not stage_folder.is_dir() or stage_folder.name in IGNORE_FOLDERS:
            continue

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
            abilities = ck.get("abilities", {})

            flat = []
            for group in ["basic", "advanced", "signature", "ultimate"]:
                g = abilities.get(group)
                if isinstance(g, list):
                    flat.extend(g)
                elif isinstance(g, str):
                    flat.append(g)

            ck_map[name] = flat

    return ck_map


def build_learnset(ability_names, cyberkin):
    learnset = {}

    for ability in ability_names:
        learnset[ability] = []

        for ck_name, moves in cyberkin.items():
            if ability in moves:
                learnset[ability].append(ck_name)

        learnset[ability].sort()

    return learnset


def write_index(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote index: {path}")


def main():
    print("Building move learnset index...")

    ability_names = load_ability_names()
    cyberkin = load_cyberkin()

    learnset = build_learnset(ability_names, cyberkin)

    write_index(OUTPUT_DIR / "master_move_learnset.json", learnset)

    print("Move learnset index complete.")


if __name__ == "__main__":
    main()
