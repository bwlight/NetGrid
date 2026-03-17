# tools/cyberkin/index_rebuilder.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CYBERKIN = BASE / "data" / "cyberkin"
OUT = BASE / "data" / "indexes" / "cyberkin_index.json"


def run():
    """
    Rebuilds cyberkin_index.json using JSON files as the source of truth.
    The index is alphabetized and overwritten every run.
    """

    index = {}

    # Scan all stage folders
    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

    for ck_json in stage_dir.glob("*.json"):
        try:
            data = json.load(open(ck_json, "r", encoding="utf-8"))
        except Exception:
            # Skip malformed JSON — integrity checker will warn
            continue

        ck = data.get("cyberkin")
        if not ck:
            # Skip files missing the wrapper
            continue

        name = ck.get("id", ck_json.stem)
        stage = ck.get("stage", stage_dir.name)

        index[name] = {
            "stage": stage,
            "path": ck_json.as_posix()
        }



    # Alphabetize the index
    sorted_index = dict(sorted(index.items(), key=lambda x: x[0].lower()))

    # Wrap in top-level structure
    output = {
        "cyberkin": sorted_index,
        "_generated_from": "tools/cyberkin/index_rebuilder.py"
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
