# tools/update_allowed_tags.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CYBERKIN = BASE / "data" / "cyberkin"
SCHEMAS = BASE / "schemas"
ALLOWED_TAGS = SCHEMAS / "allowed_tags.json"


def run():
    tags_found = set()

    print("Looking in:", CYBERKIN)
    print("Exists:", CYBERKIN.exists())
    print("Dirs:", list(CYBERKIN.iterdir()) if CYBERKIN.exists() else "NOPE")


    # Scan Cyberkin files for tags
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

            tag_list = ck.get("tags", [])
            if isinstance(tag_list, list):
                for t in tag_list:
                    tags_found.add(t)

    # Load existing allowed tags if present
    if ALLOWED_TAGS.exists():
        try:
            existing = json.load(open(ALLOWED_TAGS, "r", encoding="utf-8"))
            if isinstance(existing, list):
                tags_found.update(existing)
        except Exception:
            pass

    # Sort and write updated list
    sorted_tags = sorted(tags_found)

    ALLOWED_TAGS.parent.mkdir(parents=True, exist_ok=True)
    with open(ALLOWED_TAGS, "w", encoding="utf-8") as f:
        json.dump(sorted_tags, f, indent=4)

    print(f"Updated allowed_tags.json with {len(sorted_tags)} tags.")

if __name__ == "__main__":
    run()
