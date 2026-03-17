from pathlib import Path
import json
from tools.dependency_graph import update_cyberkin_entry

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "cyberkin"

def generate_markdown(ck: dict):
    name = ck.get("name", "Unknown")
    cid = ck.get("id", "Unknown")
    stage = ck.get("stage", "Unknown")
    family = ck.get("family", "Unknown")
    tags = ", ".join(ck.get("tags", []))
    stats = ck.get("stats", {})

    md = []
    md.append(f"# {name} ({cid})")
    md.append("")
    md.append(f"**Stage:** {stage}")
    md.append(f"**Family:** {family}")
    md.append(f"**Tags:** {tags}")
    md.append("")
    md.append("## Stats")
    for key, value in stats.items():
        md.append(f"- **{key.capitalize()}** — {value}")
    md.append("")

    return "\n".join(md)


def save_markdown(ck: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cid = ck["id"]
    path = OUTPUT_DIR / f"{cid}.md"
    path.write_text(generate_markdown(ck), encoding="utf-8")

    # Update dependency graph
    update_cyberkin_entry(cid, markdown_path=str(path))

    print(f"Saved markdown: {path}")


def run_single(cyberkin_path: Path):
    try:
        ck = json.load(open(cyberkin_path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {cyberkin_path}: {e}")
        return

    save_markdown(ck)
