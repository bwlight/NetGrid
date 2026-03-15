from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from jsonschema import validate, ValidationError


BASE_DIR = Path(__file__).resolve().parent.parent  # .../systems/party
DATA_DIR = BASE_DIR / "data"
SCHEMA_DIR = BASE_DIR / "schemas"


# Map data files → schema files
FILE_MAP = {
    "friendship_matrix.json": "friendship_matrix.schema.json",
    "synergy_rules.json": "synergy_rules.schema.json",
    "relationship_types.json": "relationship_types.schema.json",
    "party_events.json": "party_events.schema.json",
    "relationship_evolution_modifiers.json": "relationship_evolution_modifiers.schema.json",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(data_file: str, schema_file: str) -> None:
    data_path = DATA_DIR / data_file
    schema_path = SCHEMA_DIR / schema_file

    if not data_path.exists():
        print(f"❌ Missing data file: {data_path}")
        return

    if not schema_path.exists():
        print(f"❌ Missing schema file: {schema_path}")
        return

    data = load_json(data_path)
    schema = load_json(schema_path)

    try:
        validate(instance=data, schema=schema)
        print(f"✅ {data_file} is valid")
    except ValidationError as e:
        print(f"\n❌ Validation failed for {data_file}")
        print(f"   → {e.message}")
        print(f"   → Path: {'/'.join(map(str, e.path))}")
        print()


def main() -> None:
    print("🔍 Validating Netgrid Party System JSON files...\n")

    for data_file, schema_file in FILE_MAP.items():
        validate_file(data_file, schema_file)

    print("\n✨ Validation complete.")


if __name__ == "__main__":
    main()
