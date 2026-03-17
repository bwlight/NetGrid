# tools/data_integrity_checker.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CYBERKIN = BASE / "data" / "cyberkin"
FAMILIES = BASE / "data" / "families"
SCHEMAS = BASE / "schemas"
ALLOWED_TAGS_PATH = SCHEMAS / "allowed_tags.json"

def load_json(path):
    try:
        return json.load(open(path, "r", encoding="utf-8"))
    except Exception:
        return None


def run():
    grouped = {
        "Malformed Cyberkin JSON": [],
        "Missing Cyberkin Wrapper": [],
        "Missing Required Cyberkin Fields": [],
        "Stage Mismatches": [],
        "Missing Families": [],
        "Empty Families": [],
        "Invalid Family Members": [],
        "Unknown Family References": [],
        "Orphaned Family Files": [],
        "Invalid Tags": [],
        "Stat Errors": []
    }

    # Load allowed tags
    try:
        allowed_tags = set(json.load(open(ALLOWED_TAGS_PATH, "r", encoding="utf-8")))
    except Exception:
        allowed_tags = set()

    # Stage-based stat rules
    stage_stat_rules = {
        "Baby": {
            "hp": (20, 60),
            "attack": (5, 20),
            "defense": (5, 20),
            "speed": (5, 20),
            "stability": (5, 20)
        },
        "Rookie": {
            "hp": (50, 120),
            "attack": (15, 40),
            "defense": (15, 40),
            "speed": (15, 40),
            "stability": (15, 40)
        },
        "Champion": {
            "hp": (100, 200),
            "attack": (30, 70),
            "defense": (30, 70),
            "speed": (30, 70),
            "stability": (30, 70)
        },
        "Final": {
            "hp": (150, 300),
            "attack": (50, 100),
            "defense": (50, 100),
            "speed": (50, 100),
            "stability": (50, 100)
        }
    }

    # Collect all Cyberkin IDs for cross-reference
    all_cyberkin_ids = set()

    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        for ck_json in stage_dir.glob("*.json"):
            data = load_json(ck_json)
            if not data:
                grouped["Malformed Cyberkin JSON"].append(str(ck_json))
                continue

            ck = data.get("cyberkin")
            if not ck:
                grouped["Missing Cyberkin Wrapper"].append(str(ck_json))
                continue

            cid = ck.get("id")
            if cid:
                all_cyberkin_ids.add(cid)

    # Validate each Cyberkin
    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        stage_name = stage_dir.name.capitalize()

        for ck_json in stage_dir.glob("*.json"):
            data = load_json(ck_json)
            if not data:
                continue

            ck = data.get("cyberkin")
            if not ck:
                continue

            cid = ck.get("id", "UNKNOWN")

            # Required fields
            required_fields = [
                "id", "name", "family", "sector", "stage", "role",
                "personality", "element", "element_resistances",
                "status_resistances", "stats", "abilities",
                "evolution", "tags"
            ]

            for field in required_fields:
                if field not in ck:
                    grouped["Missing Required Cyberkin Fields"].append(f"{cid}: missing '{field}'")

            # Stage mismatch
            if ck.get("stage") != stage_name:
                grouped["Stage Mismatches"].append(f"{cid}: stage folder '{stage_name}' but JSON says '{ck.get('stage')}'")

            # Tag validation
            tags = ck.get("tags", [])

            if not isinstance(tags, list):
                grouped["Invalid Tags"].append(f"{cid}: tags must be a list")
            else:
                if len(tags) == 0:
                    grouped["Invalid Tags"].append(f"{cid}: has no tags")

                # Required stage tag
                required_stage_tag = stage_name.lower()
                if required_stage_tag not in tags:
                    grouped["Invalid Tags"].append(f"{cid}: missing required stage tag '{required_stage_tag}'")

                # Forbidden stage tags
                forbidden = {"baby", "rookie", "champion", "final"} - {required_stage_tag}
                for t in tags:
                    if t in forbidden:
                        grouped["Invalid Tags"].append(f"{cid}: forbidden tag '{t}' for stage {stage_name}")

                # Unknown tags
                for t in tags:
                    if t not in allowed_tags:
                        grouped["Invalid Tags"].append(f"{cid}: unknown tag '{t}'")

            # Stat validation
            stats = ck.get("stats", {})
            rules = stage_stat_rules.get(stage_name)

            if rules:
                for stat_name, (low, high) in rules.items():
                    value = stats.get(stat_name)

                    if value is None:
                        grouped["Stat Errors"].append(f"{cid}: missing stat '{stat_name}'")
                        continue

                    if not isinstance(value, int):
                        grouped["Stat Errors"].append(
                            f"{cid}: stat '{stat_name}' must be an integer, got {type(value).__name__}"
                        )
                        continue

                    if not (low <= value <= high):
                        grouped["Stat Errors"].append(
                            f"{cid}: {stat_name}={value} outside {stage_name} range {low}-{high}"
                        )

    # Validate families
    for fam_json in FAMILIES.glob("*.json"):
        fam = load_json(fam_json)
        if not fam:
            grouped["Malformed Cyberkin JSON"].append(str(fam_json))
            continue

        members = fam.get("members", [])
        if not members:
            grouped["Empty Families"].append(f"{fam_json.name}: no members")
            continue

        for m in members:
            if m not in all_cyberkin_ids:
                grouped["Invalid Family Members"].append(f"{fam_json.name}: unknown member '{m}'")

    # Orphaned family files
    for fam_json in FAMILIES.glob("*.json"):
        fam = load_json(fam_json)
        if not fam:
            continue

        if "members" not in fam:
            grouped["Orphaned Family Files"].append(str(fam_json))

    # Output
    output_path = BASE / "data" / "todo" / "integrity_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(grouped, f, indent=4)

    print("Integrity check complete. Report written to:", output_path)


if __name__ == "__main__":
    run()
