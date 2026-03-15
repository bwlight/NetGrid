import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[2]
CYBERKIN_DIR = ROOT / "data" / "cyberkin"
SCHEMA_DIR = ROOT / "schemas"

CYBERKIN_SCHEMA = json.load(open(SCHEMA_DIR / "cyberkin.schema.json", "r", encoding="utf-8"))

def validate_file(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        validate(instance=data, schema=CYBERKIN_SCHEMA)
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
    print("\n=== Validating Cyberkin ===\n")

    failures = 0

    for path in CYBERKIN_DIR.rglob("*.json"):

        if ".LEGACY" in path.parts:
            continue

        if not validate_file(path):
            failures += 1

    print(f"\n{failures} Cyberkin files failed validation.\n")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
