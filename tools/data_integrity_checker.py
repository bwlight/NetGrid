# tools/data_integrity_checker.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CYBERKIN = BASE / "data" / "cyberkin"
FAMILIES = BASE / "data" / "families"
INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"


def load_json(path: Path):
    try:
        return json.load(open(path, "r", encoding="utf-8"))
    except Exception:
        return None


def run_integrity_check():
    critical = []
    warnings = []
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
    }

    # -----------------------------
    # Load index (if exists)
    # -----------------------------
    index_data = load_json(INDEX)
    if not index_data:
        warnings.append("cyberkin_index.json missing or unreadable — will be rebuilt.")
        index = {}
    else:
        index = index_data.get("cyberkin", {})

    # -----------------------------
    # Scan Cyberkin JSON
    # -----------------------------
    cyberkin_families = {}  # family -> list of members
    cyberkin_seen = set()

    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        for ck_json in stage_dir.glob("*.json"):
            data = load_json(ck_json)
            name = ck_json.stem

            if not data:
                critical.append(f"{name}.json is unreadable or malformed.")
                grouped["Malformed Cyberkin JSON"].append(name)
                continue

            ck = data.get("cyberkin")
            if not ck:
                critical.append(f"{name}.json missing required 'cyberkin' wrapper.")
                grouped["Missing Cyberkin Wrapper"].append(name)
                continue

            # Required fields
            required = ["id", "name", "family", "stage"]
            missing = [f for f in required if f not in ck]
            if missing:
                critical.append(f"{name}.json missing required fields: {missing}")
                grouped["Missing Required Cyberkin Fields"].append(f"{name}: {missing}")
                continue

            cid = ck["id"]
            cyberkin_seen.add(cid)

            # Stage mismatch check
            json_stage = ck["stage"]
            index_stage = index.get(cid, {}).get("stage")
            if index_stage and index_stage != json_stage:
                warnings.append(
                    f"Stage mismatch for {cid}: index='{index_stage}', json='{json_stage}'."
                )
                grouped["Stage Mismatches"].append(
                    f"{cid}: index='{index_stage}', json='{json_stage}'"
                )

            # Family collection
            fam = ck["family"].lower()
            if fam not in cyberkin_families:
                cyberkin_families[fam] = []
            cyberkin_families[fam].append(cid)

    # -----------------------------
    # Validate Family JSON files
    # -----------------------------
    family_files = {f.stem.lower(): f for f in FAMILIES.glob("*.json")}

    # Families referenced by Cyberkin but missing JSON
    for fam in cyberkin_families:
        if fam not in family_files:
            warnings.append(f"Family '{fam}' referenced by Cyberkin but no JSON file exists.")
            grouped["Missing Families"].append(fam)

    # Validate existing family JSON files
    for fam_name, fam_file in family_files.items():
        data = load_json(fam_file)
        if not data:
            warnings.append(f"Family file '{fam_name}' is unreadable.")
            grouped["Orphaned Family Files"].append(fam_name)
            continue

        members = data.get("members", [])
        if not members:
            warnings.append(f"Family '{fam_name}' has no members.")
            grouped["Empty Families"].append(fam_name)

        # Members that don't exist as Cyberkin
        for m in members:
            if m not in cyberkin_seen:
                warnings.append(f"Family '{fam_name}' lists unknown Cyberkin '{m}'.")
                grouped["Invalid Family Members"].append(f"{fam_name}: {m}")

    # Cyberkin referencing families that don't exist
    for fam in cyberkin_families:
        if fam not in family_files:
            warnings.append(f"Cyberkin reference unknown family '{fam}'.")
            grouped["Unknown Family References"].append(fam)

    return {
        "critical": critical,
        "warnings": warnings,
        "grouped": grouped,
    }
