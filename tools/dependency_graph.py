from pathlib import Path
import json

GRAPH_PATH = Path(__file__).resolve().parents[1] / "data" / "dependency_graph.json"

def load_graph():
    if GRAPH_PATH.exists():
        return json.load(open(GRAPH_PATH, "r", encoding="utf-8"))
    return {"cyberkin": {}, "families": {}}

def save_graph(graph):
    GRAPH_PATH.write_text(json.dumps(graph, indent=4), encoding="utf-8")

def update_cyberkin_entry(cid, family_id=None, markdown_path=None):
    graph = load_graph()
    entry = graph["cyberkin"].setdefault(cid, {})

    if family_id is not None:
        entry["family"] = family_id

    if markdown_path is not None:
        entry["markdown"] = markdown_path

    save_graph(graph)

def update_family_entry(fid, members=None, markdown_path=None):
    graph = load_graph()
    entry = graph["families"].setdefault(fid, {})

    if members is not None:
        entry["members"] = sorted(list(set(members)))

    if markdown_path is not None:
        entry["markdown"] = markdown_path

    save_graph(graph)
