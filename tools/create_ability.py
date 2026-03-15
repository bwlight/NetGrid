import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ABILITIES_ROOT = BASE / "data" / "abilities"


def normalize(name: str) -> str:
    return name.lower().replace(" ", "_")


parser = argparse.ArgumentParser()
parser.add_argument("--tier", type=str, help="Tier for stub generation")
parser.add_argument("--element", type=str, help="Element for stub generation")
parser.add_argument("--stub", action="store_true", help="Auto-generate a stub ability")
parser.add_argument("name", nargs="?")
args = parser.parse_args()


if args.stub:
    name = args.name
    tier = args.tier
    element = args.element

    if not name or not tier or not element:
        print("Stub generation requires: --tier <tier> --element <element> <name>")
        exit(1)

    norm = normalize(name)
    ability_id = f"{element}.{tier}.{norm}"

    ability = {
        "ability": {
            "id": ability_id,
            "name": name,
            "element": element,
            "category": "NEW",
            "power": 0,
            "accuracy": 100,
            "cost": 0,
            "priority": 0,
            "target": "self",
            "animation": norm,
            "description": "[TODO: Fill in description]",
            "tags": ["auto-generated", "stub"]
        }
    }

    out_dir = ABILITIES_ROOT / tier
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{norm}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ability, f, indent=2)

    print(f"Created stub ability: {out_path}")
    exit(0)


print("Interactive mode is disabled for this regenerated version.")
print("Use --stub for auto-generation.")
