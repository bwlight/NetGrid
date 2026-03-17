#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

FAMILY_JSON_DIR = BASE / "data" / "families"
OUTPUT_DIR = BASE / "docs" / "families"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    index_entries = []

    for json_file in FAMILY_JSON_DIR.glob("*.json"):
        family_id = json_file.stem
        data = load_json(json_file)

        entry = {
            "id": family_id,
            "name": data.get("family", family_id.capitalize()),
            "sector": data.get("sector", "Unknown"),
            "type": data.get("type", "Unknown"),
            "habitat": data.get("habitat", "Unknown"),
            "count": len(data.get("members", [])),
        }

        index_entries.append(entry)

    # Sort alphabetically by family name
    index_entries.sort(key=lambda x: x["name"].lower())

    md = "# Cyberkin Family Index\n\n"
    md += "A complete index of all Cyberkin families, their sectors, and their members.\n\n"

    md += "## Families\n\n"

    for entry in index_entries:
        md += f"### [{entry['name']}](./{entry['id']}.md)\n"
        md += f"- **Sector:** {entry['sector']}\n"
        md += f"- **Type:** {entry['type']}\n"
        md += f"- **Habitat:** {entry['habitat']}\n"
        md += f"- **Members:** {entry['count']}\n\n"

    out_path = OUTPUT_DIR / "index.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print("Family index page generated.")


if __name__ == "__main__":
    main()
