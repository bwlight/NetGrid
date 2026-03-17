#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

CYBERKIN_INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"
CYBERKIN_DIR = BASE / "data" / "cyberkin"

OUTPUT_DIR = BASE / "docs" / "cyberkin"


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def strip_id_from_name(name):
    if "(" in name and name.endswith(")"):
        return name[: name.rfind("(")].strip()
    return name


def render_resistance_block(title, data):
    lines = [f"**{title}**"]
    for key, value in data.items():
        lines.append(f"- {key.capitalize()} — {value}")
    return "\n".join(lines)


def render_abilities_block(abilities):
    categories = [
        "basic",
        "advanced",
        "support",
        "disruptor",
        "signature",
        "mythic",
        "ultimate",
        "passive",
    ]

    lines = ["**Abilities**"]
    for cat in categories:
        val = abilities.get(cat)
        if isinstance(val, list):
            lines.append(f"- {cat.capitalize()} — {', '.join(val) if val else 'None'}")
        else:
            lines.append(f"- {cat.capitalize()} — {val if val else 'None'}")

    return "\n".join(lines)


def render_evolution_block(evo):
    lines = ["**Evolution**"]
    lines.append(f"- next: {evo.get('next')}")
    lines.append(f"- method: {evo.get('method')}")

    req = evo.get("requirements")
    if req is None:
        lines.append("- requirements: null")
    else:
        lines.append("- requirements:")
        for key, value in req.items():
            lines.append(f"  - {key}: {value}")

    return "\n".join(lines)


def load_cyberkin_file(ck_name, stage):
    ck_path = CYBERKIN_DIR / stage.lower() / f"{ck_name}.json"
    if not ck_path.exists():
        return None
    return load_json(ck_path)["cyberkin"]


def generate_cyberkin_markdown(ck_name, ck_data):
    lines = []

    display_name = strip_id_from_name(ck_data["name"])
    title = ck_data.get("title")

    # Header
    if title and title.strip():
        lines.append(f"# {display_name} — *{title}*\n")
    else:
        lines.append(f"# {display_name}\n")

    # NEW: Show which JSON file generated this page
    source_path = f"data/cyberkin/{ck_data['stage'].lower()}/{ck_name}.json"
    lines.append(f"*Cyberkin was created from this file → `{source_path}`*\n")

    # Identity
    lines.append(f"- **ID:** {ck_name}")
    lines.append(f"- **Stage:** {ck_data['stage']}")
    lines.append(f"- **Element:** {ck_data['element'].capitalize()}")
    lines.append(f"- **Roles:** {', '.join(ck_data['role'])}")
    lines.append(f"- **Personality:** {', '.join(ck_data['personality'])}")
    lines.append(f"- **Tags:** {', '.join(ck_data['tags'])}\n")

    # Description
    desc = ck_data.get("description")
    lines.append("## Description")
    lines.append(desc if desc else "*Description coming soon.*")
    lines.append("")

    # Stats
    lines.append("## Stats")
    for key, value in ck_data["stats"].items():
        lines.append(f"- {key.capitalize()}: {value}")
    lines.append("")

    # Abilities
    lines.append("## Abilities")
    lines.append(render_abilities_block(ck_data["abilities"]))
    lines.append("")

    # Resistances
    lines.append("## Element Resistances")
    lines.append(render_resistance_block("Element Resistances", ck_data["element_resistances"]))
    lines.append("")

    lines.append("## Status Resistances")
    lines.append(render_resistance_block("Status Resistances", ck_data["status_resistances"]))
    lines.append("")

    # Evolution
    lines.append("## Evolution")
    lines.append(render_evolution_block(ck_data["evolution"]))
    lines.append("")

    # JSON File section
    lines.append("## Json File")
    pretty_json = json.dumps(ck_data, indent=2)
    lines.append(f"```json\n{pretty_json}\n```")
    lines.append("")

    lines.append("This file is auto-generated from NetGrid Cyberkin data.\n")

    return "\n".join(lines)


def main():
    print("Building Cyberkin markdown pages...")

    cyberkin_index = load_json(CYBERKIN_INDEX)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for ck_name, ck_info in cyberkin_index["cyberkin"].items():
        stage = ck_info["stage"]
        ck_data = load_cyberkin_file(ck_name, stage)

        if not ck_data:
            print(f"Missing JSON for {ck_name}")
            continue

        md = generate_cyberkin_markdown(ck_name, ck_data)

        out_path = OUTPUT_DIR / f"{ck_name}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"Wrote: {out_path}")

    print("Cyberkin markdown build complete.")


if __name__ == "__main__":
    main()
