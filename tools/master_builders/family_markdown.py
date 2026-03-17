#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

REFERENCE_DIR = BASE / "docs" / "reference"
FAMILY_JSON_DIR = BASE / "data" / "families"
OUTPUT_DIR = BASE / "docs" / "families"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    for json_file in FAMILY_JSON_DIR.glob("*.json"):
        family_id = json_file.stem
        data = load_json(json_file)

        md = f"# {data['family']} Family\n\n"

        md += "## Summary\n"
        md += f"- **Sector:** {data['sector']}\n"
        md += f"- **Type:** {data['type']}\n"
        md += f"- **Habitat:** {data['habitat']}\n"
        md += f"- **Themes:** {', '.join(data['themes'])}\n"
        md += f"- **Evolution Requirements:** {', '.join(data['evolution_requirements'])}\n"
        md += f"- **Quest Hooks:** {', '.join(data['quest_hooks'])}\n"
        md += f"- **Example Abilities:** {', '.join(data['example_abilities'])}\n\n"

        md += "## Members\n"
        for m in data["members"]:
            md += f"- {m}\n"

        md += "\n## Lore\n"
        md += "Auto-generated baseline lore. Expand as needed.\n"

        out_path = OUTPUT_DIR / f"{family_id}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

    print("Family Markdown generation complete.")


if __name__ == "__main__":
    main()
