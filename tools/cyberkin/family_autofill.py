# tools/cyberkin/family_autofill.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CYBERKIN = BASE / "data" / "cyberkin"
FAM_JSON = BASE / "data" / "families"


def run():
    """
    Auto-populates family JSON files based on Cyberkin JSON data.
    Reads each Cyberkin's 'family' field and assigns them to the correct family.
    This replaces the old family_json.py behavior entirely.
    """

    FAM_JSON.mkdir(parents=True, exist_ok=True)

    # Build a dictionary: family_name -> list of members
    families = {}

    # Scan all Cyberkin JSON files
    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        for ck_json in stage_dir.glob("*.json"):
            try:
                data = json.load(open(ck_json, "r", encoding="utf-8"))
            except Exception:
                continue

            ck = data.get("cyberkin")
            if not ck:
                continue

            name = ck.get("id") or ck.get("name") or ck_json.stem
            family = ck.get("family")

            if not family:
                continue

            family = family.lower()

            if family not in families:
                families[family] = []

            families[family].append(name)

    # Write out family JSON files based on Cyberkin data
    for family_name, members in families.items():
        out_path = FAM_JSON / f"{family_name}.json"

        data = {
            "family": family_name,
            "members": sorted(members),
            "_generated_from": "tools/cyberkin/family_autofill.py"
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # Preserve existing families with no members
    for fam_file in FAM_JSON.glob("*.json"):
        try:
            data = json.load(open(fam_file, "r", encoding="utf-8"))
        except Exception:
            continue

        name = data.get("family", fam_file.stem).lower()

        if name not in families:
            data["members"] = []
            with open(fam_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
