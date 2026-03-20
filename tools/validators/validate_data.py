import json
import os
from jsonschema import validate, ValidationError

SCHEMA_DIR = "schemas"
DATA_DIR = "src/netgrid/data"

# Load schemas
with open(os.path.join(SCHEMA_DIR, "cyberkin.schema.json")) as f:
    CYBERKIN_SCHEMA = json.load(f)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def validate_file(path):
    data = load_json(path)

    # Determine which schema to use
    if "cyberkin" in data:
        schema = CYBERKIN_SCHEMA
    else:
        print(f"[SKIP] {path} (no matching schema yet)")
        return

    try:
        validate(instance=data, schema=schema)
        print(f"[OK]   {path}")
    except ValidationError as e:
        print(f"[ERR]  {path}")
        print(f"       {e.message}")

def walk_data():
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".json"):
                validate_file(os.path.join(root, file))

if __name__ == "__main__":
    walk_data()
