from pathlib import Path
import json

INDEX_PATH = Path(__file__).resolve().parents[2] / "docs" / "cyberkin_index.json"

def update_index_entry(ck: dict, index: dict):
    cid = ck["id"]
    index[cid] = {
        "name": ck.get("name"),
        "stage": ck.get("stage"),
        "family": ck.get("family"),
        "tags": ck.get("tags", [])
    }


def run_single(cyberkin_path: Path):
    try:
        ck = json.load(open(cyberkin_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {cyberkin_path}: {e}")
        return

    if INDEX_PATH.exists():
        index = json.load(open(INDEX_PATH, "r", encoding="utf-8"))
    else:
        index = {}

    update_index_entry(ck, index)

    INDEX_PATH.write_text(json.dumps(index, indent=4), encoding="utf-8")
    print(f"Updated index entry for {cyberkin_path.name}")
