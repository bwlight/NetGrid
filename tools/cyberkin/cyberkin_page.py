# tools/cyberkin/cyberkin_page.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CYBERKIN = BASE / "data" / "cyberkin"
OUT = BASE / "docs" / "cyberkin"


def run():
    """
    Generates Markdown pages for each Cyberkin based on their JSON files.
    JSON files are the source of truth for all Cyberkin data.
    """

    OUT.mkdir(parents=True, exist_ok=True)

    # Iterate through stage folders
    for stage_dir in CYBERKIN.iterdir():
        if not stage_dir.is_dir():
            continue

        # Iterate through Cyberkin JSON files
        for ck_json in stage_dir.glob("*.json"):
            try:
                data = json.load(open(ck_json, "r", encoding="utf-8"))
            except Exception:
                # Malformed JSON is handled by integrity checker
                continue

            ck = data.get("cyberkin", {})
            name = ck.get("name", ck_json.stem)
            stage = ck.get("stage", stage_dir.name)
            description = ck.get("description", "")


            out_path = OUT / f"{name}.md"

            md = f"# {name}\n\n"
            md += f"**Stage:** {stage}\n\n"

            if description:
                md += f"{description}\n\n"

            md += f"---\nThis file was created from → {ck_json.as_posix()}"

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md)
