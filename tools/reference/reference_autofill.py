# tools/reference/reference_autofill.py

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
REF_DATA = BASE / "data" / "reference"
OUT = BASE / "docs" / "reference"


def run():
    """
    Converts reference JSON files into Markdown pages.
    Each output file includes a provenance footer.
    """
    OUT.mkdir(parents=True, exist_ok=True)

    for ref_json in REF_DATA.glob("*.json"):
        try:
            data = json.load(open(ref_json, "r", encoding="utf-8"))
        except Exception:
            # If a reference JSON is malformed, skip it.
            continue

        name = data.get("name", ref_json.stem)
        description = data.get("description", "")

        out_path = OUT / f"{ref_json.stem}.md"

        md = f"# {name}\n\n"
        md += f"{description}\n\n"
        md += f"---\nThis file was created from → {ref_json.as_posix()}"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
