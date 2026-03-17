from pathlib import Path
import json

INDEX_PATH = Path(__file__).resolve().parents[2] / "docs" / "family_index.json"

def update_family_index_entry(family: dict, index: dict):
    fid = family["id"]
    index[fid] = {
        "members": family.get("members", [])
    }


def run_for_family(family_path: Path):
    try:
        family = json.load(open(family_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {family_path}: {e}")
        return

    if INDEX_PATH.exists():
        index = json.load(open(INDEX_PATH, "r", encoding="utf-8"))
    else:
        index = {}

    update_family_index_entry(family, index)

    INDEX_PATH.write_text(json.dumps(index, indent=4), encoding="utf-8")
    print(f"Updated family index entry for {family_path.name}")
