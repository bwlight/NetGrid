# tools/data_integrity_checker.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
CYBERKIN = DATA / "cyberkin"
FAMILIES = DATA / "families"
INDEXES = DATA / "indexes"


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def run_integrity_check():
    critical = []
    warnings = []
    grouped = {
        "Missing Cyberkin JSON Files": [],
        "Malformed Cyberkin JSON Files": [],
        "Index Stage Mismatches": [],
        "Missing Family JSON Files": [],
        "Malformed Family JSON Files": [],
        "Families With No Members": [],
    }

    # Load index (if missing, warn but do not fail — index_rebuilder will fix it)
    index_path = INDEXES / "cyberkin_index.json"
    index = load_json(index_path)
    if not index:
        warnings.append("cyberkin_index.json missing or unreadable — will be rebuilt.")
        index = {"cyberkin": {}}

    index = index.get("cyberkin", {})

    # Validate Cyberkin JSON files (source of truth)
    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        for ck_json in stage_dir.glob("*.json"):
            data = load_json(ck_json)
            name = ck_json.stem

            if not data:
                critical.append(f"{name}.json is unreadable or malformed.")
                grouped["Malformed Cyberkin JSON Files"].append(name)
                continue

            ck = data.get("cyberkin")
            if not ck:
                critical.append(f"{name}.json missing required 'cyberkin' wrapper.")
                grouped["Malformed Cyberkin JSON Files"].append(name)
                continue

            if "stage" not in ck:
                critical.append(f"{name}.json missing required field 'stage'.")
                grouped["Malformed Cyberkin JSON Files"].append(name)
                continue

            json_stage = ck["stage"]
            index_stage = index.get(name, {}).get("stage")

            if index_stage and index_stage != json_stage:
                warnings.append(
                    f"Index stage mismatch for {name}: index='{index_stage}', json='{json_stage}'."
                )
                grouped["Index Stage Mismatches"].append(
                    f"{name}: index='{index_stage}', json='{json_stage}'"
                )


    # Validate family JSON files
    for fam_json in FAMILIES.glob("*.json"):
        fam = load_json(fam_json)
        name = fam_json.stem

        if not fam:
            warnings.append(f"{name}.json unreadable or malformed.")
            grouped["Malformed Family JSON Files"].append(name)
            continue

        if "members" not in fam:
            warnings.append(f"{name}.json missing 'members' list.")
            grouped["Malformed Family JSON Files"].append(name)
            continue

        if not fam["members"]:
            warnings.append(f"Family '{name}' has no members.")
            grouped["Families With No Members"].append(name)

    return {
        "critical": critical,
        "warnings": warnings,
        "grouped": grouped,
    }
