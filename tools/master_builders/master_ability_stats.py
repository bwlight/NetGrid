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
            if not aid:
                continue

            element = ability.get("element")
            tier = aid.split(".")[1]

            abilities[aid] = {
                "element": element,
                "tier": tier,
                "power": ability.get("power", 0),
                "accuracy": ability.get("accuracy", 0),
                "cost": ability.get("cost", 0)
            }

    return abilities


def build_stats(abilities):
    tiers = {}
    elements = {}

    for aid, a in abilities.items():
        tier = a["tier"]
        element = a["element"]

        tiers.setdefault(tier, {"count": 0, "power": 0, "accuracy": 0, "cost": 0})
        elements.setdefault(element, {"count": 0, "power": 0, "accuracy": 0, "cost": 0})

        tiers[tier]["count"] += 1
        tiers[tier]["power"] += a["power"]
        tiers[tier]["accuracy"] += a["accuracy"]
        tiers[tier]["cost"] += a["cost"]

        elements[element]["count"] += 1
        elements[element]["power"] += a["power"]
        elements[element]["accuracy"] += a["accuracy"]
        elements[element]["cost"] += a["cost"]

    for group in [tiers, elements]:
        for key, stats in group.items():
            c = stats["count"]
            if c > 0:
                stats["avg_power"] = stats["power"] / c
                stats["avg_accuracy"] = stats["accuracy"] / c
                stats["avg_cost"] = stats["cost"] / c

            del stats["power"]
            del stats["accuracy"]
            del stats["cost"]

    return {"tiers": tiers, "elements": elements}


def write_index(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote index: {path}")


def main():
    print("Building ability stats index...")

    abilities = load_abilities()
    stats = build_stats(abilities)

    write_index(OUTPUT_DIR / "master_ability_stats.json", stats)

    print("Ability stats index complete.")


if __name__ == "__main__":
    main()
