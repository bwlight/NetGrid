import json
from pathlib import Path
from jsonschema import validate, ValidationError

CYBERKIN_ROOT = Path("data/cyberkin")
ABILITY_ROOT = Path("data/abilities")
SCHEMA_CYBERKIN = Path("schemas/cyberkin.schema.json")
SCHEMA_MASTER = Path("schemas/master_index.schema.json")
OUTPUT_FILE = CYBERKIN_ROOT / "cyberkin_index.json"

ELEMENTS = [
    "core", "root", "pulse", "archive", "cloud",
    "firewall", "dream", "echo", "void", "corrupt"
]


def load_schema(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


CYBERKIN_SCHEMA = load_schema(SCHEMA_CYBERKIN)
MASTER_SCHEMA = load_schema(SCHEMA_MASTER)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_ability_ids():
    ids = set()
    for path in ABILITY_ROOT.rglob("*.json"):
        try:
            data = load_json(path)
            if "ability" in data:
                ids.add(data["ability"]["id"])
        except Exception:
            continue
    return ids


def collect_passive_ids():
    ids = set()
    passive_dir = ABILITY_ROOT / "passive"
    if passive_dir.exists():
        for path in passive_dir.glob("*.json"):
            try:
                data = load_json(path)
                if "ability" in data:
                    ids.add(data["ability"]["id"])
            except Exception:
                continue
    return ids


ABILITY_IDS = collect_ability_ids()
PASSIVE_IDS = collect_passive_ids()


def validate_ability_refs(ck, file_path):
    errors = []

    ability_groups = [
        "basic", "advanced", "support", "disruptor"
    ]

    for group in ability_groups:
        for ability_id in ck["abilities"].get(group, []):
            if ability_id not in ABILITY_IDS:
                errors.append(f"Unknown ability ID '{ability_id}' in {group}")

    # Signature, mythic, ultimate
    for key in ["signature", "mythic", "ultimate"]:
        ability_id = ck["abilities"].get(key)
        if ability_id and ability_id not in ABILITY_IDS:
            errors.append(f"Unknown ability ID '{ability_id}' in {key}")

    # Passive
    passive_id = ck["abilities"].get("passive")
    if passive_id and passive_id not in PASSIVE_IDS:
        errors.append(f"Unknown passive ID '{passive_id}'")

    return errors


def scan_cyberkin_files():
    for path in CYBERKIN_ROOT.rglob("*.json"):
        if path.name == "cyberkin_index.json":
            continue
        if ".LEGACY" in path.parts:
            continue
        yield path


def build_index():
    index_entries = []
    element_groups = {e: [] for e in ELEMENTS}
    cyberkin_map = {}

    # First pass: validate Cyberkin schema + ability refs
    for file_path in scan_cyberkin_files():
        try:
            data = load_json(file_path)
            validate(instance=data, schema=CYBERKIN_SCHEMA)
            ck = data["cyberkin"]
        except ValidationError as e:
            print(f"[ERROR] Schema error in {file_path}: {e.message}")
            continue
        except Exception as e:
            print(f"[ERROR] Failed to load {file_path}: {e}")
            continue

        # Ability validation
        ability_errors = validate_ability_refs(ck, file_path)
        for err in ability_errors:
            print(f"[ERROR] {file_path}: {err}")
        if ability_errors:
            continue

        cyberkin_map[ck["id"]] = ck

    # Second pass: validate evolution targets
    for ck_id, ck in cyberkin_map.items():
        evo = ck.get("evolution", {})
        nxt = evo.get("next")
        if nxt and nxt not in cyberkin_map:
            print(f"[ERROR] Evolution target '{nxt}' for '{ck_id}' does not exist.")
            continue

    # Build index
    for ck_id, ck in cyberkin_map.items():
        entry = {
            "id": ck["id"],
            "name": ck["name"],
            "family": ck["family"],
            "sector": ck["sector"],
            "stage": ck["stage"],
            "element": ck["element"],
            "file": f"{ck['stage'].lower()}/{ck['id']}.json"
        }

        index_entries.append(entry)
        element_groups[ck["element"]].append(ck["id"])

    index_entries.sort(key=lambda x: x["id"])
    for e in element_groups:
        element_groups[e].sort()

    return {
        "index": index_entries,
        **element_groups
    }


def main():
    index_data = build_index()

    missing_abilities = set()
    missing_map = {}  # ability_id -> set of cyberkin names

    try:
        validate(instance=index_data, schema=MASTER_SCHEMA)
        print("[OK] Final index validated against master_index.schema.json")
    except ValidationError as e:
        print(f"[ERROR] Final index invalid: {e.message}")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)

    print(f"[OK] Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
