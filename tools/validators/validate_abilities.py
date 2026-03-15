import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[2]
ABILITIES_DIR = ROOT / "data" / "abilities"
SCHEMA_DIR = ROOT / "schemas"

ABILITY_SCHEMA = json.load(open(SCHEMA_DIR / "ability.schema.json", "r", encoding="utf-8"))
PASSIVE_SCHEMA = json.load(open(SCHEMA_DIR / "passive.schema.json", "r", encoding="utf-8"))


def is_passive(path: Path) -> bool:
    """Return True if the ability's category is 'passive'."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("ability", {}).get("category") == "passive"
    except Exception:
        # If unreadable or empty, treat as non-passive so validator reports the real error
        return False


def validate_file(path: Path, schema: dict):
    """Validate a single ability file against the given schema."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        validate(instance=data, schema=schema)
        print(f"[OK] {path}")
        return True

    except json.JSONDecodeError as e:
        print(f"[ERROR] {path}: Invalid JSON — {e.msg} at line {e.lineno}, column {e.colno}")
        return False

    except ValidationError as e:
        print(f"[ERROR] {path}: {e.message}")
        return False

    except Exception as e:
        print(f"[ERROR] {path}: Unexpected error — {e}")
        return False


def main():
    print("\n=== Validating Abilities ===\n")

    failures = 0

    for path in ABILITIES_DIR.rglob("*.json"):

        # Skip legacy folders
        if ".LEGACY" in path.parts:
            continue

        # Determine schema based on category
        if is_passive(path):
            ok = validate_file(path, PASSIVE_SCHEMA)
        else:
            ok = validate_file(path, ABILITY_SCHEMA)

        if not ok:
            failures += 1

    print(f"\n{failures} ability files failed validation.\n")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
