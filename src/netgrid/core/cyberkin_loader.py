import json
from pathlib import Path

def load_cyberkin():
    data_dir = Path(__file__).parent.parent / "data" / "cyberkin"
    cyberkin = {}

    for file in data_dir.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            family_id = data["family_id"]
            cyberkin[family_id] = data

    return cyberkin
