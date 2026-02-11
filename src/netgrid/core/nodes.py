import json
from pathlib import Path

class Node:
    def __init__(self, node_id, node_type, sector, connections):
        self.id = node_id
        self.type = node_type
        self.sector = sector
        self.connections = connections

    def __repr__(self):
        return f"<Node {self.id} ({self.type}) in {self.sector}>"

def load_nodes():
    data_path = Path(__file__).parent.parent / "data" / "nodes.json"
    with open(data_path, "r") as f:
        raw = json.load(f)

    nodes = {}
    for entry in raw:
        node = Node(
            node_id=entry["id"],
            node_type=entry["type"],
            sector=entry["sector"],
            connections=entry["connections"]
        )
        nodes[node.id] = node

    return nodes

def connect_nodes_to_sectors(nodes, sectors):
    for node in nodes.values():
        if node.sector in sectors:
            node.sector_obj = sectors[node.sector]
        else:
            node.sector_obj = None
