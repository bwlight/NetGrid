# tools/cyberkin/family_index.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FAM_JSON = BASE / "data" / "families"
INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"
OUT = BASE / "docs" / "lore" / "family_index.md"


def run():
    """
    Builds a global Family Index page.
    Includes:
    - All families
    - Their members (if any)
    - A stage listing sourced from the rebuilt cyberkin_index.json
    """

    # Load the rebuilt Cyberkin index
    try:
        index_data = json.load(open(INDEX, "r", encoding="utf-8"))
        ck_index = index_data.get("cyberkin", {})
    except Exception:
        ck_index = {}

    # Load all family JSON files
    families = []
    for fam_file in FAM_JSON.glob("*.json"):
        try:
            data = json.load(open(fam_file, "r", encoding="utf-8"))
        except Exception:
            continue

        families.append({
            "name": data.get("family", fam_file.stem),
            "members": data.get("members", []),
            "source": fam_file.as_posix()
        })

    # Sort families alphabetically
    families.sort(key=lambda f: f["name"].lower())

    # Build Markdown
    md = "# Family Index\n\n"
    md += "A complete index of all families and their known members.\n\n"

    for fam in families:
        md += f"## {fam['name']}\n\n"

        if fam["members"]:
            for m in fam["members"]:
                stage = ck_index.get(m, {}).get("stage", "unknown")
                md += f"- **{m}** — stage: {stage}\n"
            md += "\n"
        else:
            md += "_No registered members._\n\n"

    md += f"---\nThis file was created from → {FAM_JSON.as_posix()}"

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
