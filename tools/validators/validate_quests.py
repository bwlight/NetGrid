import os
import json
from jsonschema import validate, ValidationError

SCHEMA_PATH = "quest.schema.json"
QUESTS_ROOT = "data/quests"

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_file(path, schema):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e

def main():
    schema = load_schema()
    errors = []

    for root, _, files in os.walk(QUESTS_ROOT):
        for file in files:
            if not file.endswith(".json"):
                continue

            json_path = os.path.join(root, file)
            ok, err = validate_file(json_path, schema)

            if ok:
                print(f"VALID:   {json_path}")
            else:
                print(f"INVALID: {json_path}")
                print(f"  → {err.message}")
                errors.append((json_path, err))

    if errors:
        print("\nValidation failed for one or more quest files.")
        exit(1)
    else:
        print("\nAll quest files are valid!")
        exit(0)

if __name__ == "__main__":
    main()
