import json

def load_node_sector_map(path):
    with open(path, "r") as f:
        return json.load(f)
