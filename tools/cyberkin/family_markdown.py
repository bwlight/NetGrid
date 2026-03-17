# tools/cyberkin/family_markdown.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FAM_JSON = BASE / "data" / "families"
OUT = BASE / "docs" / "lore" / "families"


def run():
    """
    Generates Markdown pages for each family based on their JSON files.
    The JSON files are created earlier by family_json.py.
    """

    OUT.mkdir(parents=True, exist_ok=True)

    for fam_file in FAM_JSON.glob("*.json"):
        try:
            data = json.load(open(fam_file, "r", encoding="utf-8"))
        except Exception:
            # Malformed JSON is handled by integrity checker
            continue

        family_name = data.get("family", fam_file.stem)
        members = data.get("members", [])

        out_path = OUT / f"{family_name}.md"

        md = f"# {family_name}\n\n"

        if members:
            md += "## Members\n\n"
            for m in members:
                md += f"- {m}\n"
            md += "\n"
        else:
            md += "_This family currently has no registered members._\n\n"

        md += f"---\nThis file was created from → {fam_file.as_posix()}"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
