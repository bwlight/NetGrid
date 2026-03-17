from pathlib import Path
import json
from tools.dependency_graph import update_cyberkin_entry, update_family_entry

FAMILY_DIR = Path(__file__).resolve().parents[2] / "data" / "families"

def update_family_file(family_path: Path, ck: dict):
    family_id = ck.get("family")
    cid = ck.get("id")

    # Load or create family file
    if not family_path.exists():
        family = {"id": family_id, "members": []}
    else:
        family = json.load(open(family_path, "r", encoding="utf-8"))

    # Update members
    members = set(family.get("members", []))
    members.add(cid)
    family["members"] = sorted(members)

    # Save updated family file
    family_path.write_text(json.dumps(family, indent=4), encoding="utf-8")
    print(f"Updated family file: {family_path}")

    # Update dependency graph
    update_cyberkin_entry(cid, family_id=family_id)
    update_family_entry(family_id, members=family["members"])


def run_for_cyberkin(cyberkin_path: Path):
    try:
        ck = json.load(open(cyberkin_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {cyberkin_path}: {e}")
        return

    family_id = ck.get("family")
    if not family_id:
        print(f"{cyberkin_path.name} has no family assigned.")
        return

    family_path = FAMILY_DIR / f"{family_id}.json"
    update_family_file(family_path, ck)
