# tools/scan_tags.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CYBERKIN = BASE / "data" / "cyberkin"

def run():
    tags = set()

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
                    tags.add(t)

    print("Tags found across all Cyberkin:\n")
    for t in sorted(tags):
        print(f"- {t}")

if __name__ == "__main__":
    run()
