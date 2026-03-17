from pathlib import Path
import json
from tools.dependency_graph import update_family_entry

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "families"

def generate_family_markdown(family: dict):
    fid = family.get("id", "Unknown")
    members = family.get("members", [])

    md = []
    md.append(f"# Family: {fid}")
    md.append("")
    md.append("## Members")
    for m in members:
        md.append(f"- {m}")
    md.append("")

    return "\n".join(md)


def save_family_markdown(family: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fid = family["id"]
    path = OUTPUT_DIR / f"{fid}.md"
    path.write_text(generate_family_markdown(family), encoding="utf-8")

    # Update dependency graph
    update_family_entry(fid, markdown_path=str(path))

    print(f"Saved family markdown: {path}")


def run_for_family(family_path: Path):
    try:
        family = json.load(open(family_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {family_path}: {e}")
        return

    save_family_markdown(family)
