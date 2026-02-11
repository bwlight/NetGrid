import json
from pathlib import Path

class Sector:
    def __init__(self, sector_id, name, description, nodes):
        self.id = sector_id
        self.name = name
        self.description = description
        self.nodes = nodes

    def __repr__(self):
        return f"<Sector {self.id}: {self.name}>"

def load_sectors():
    data_path = Path(__file__).parent.parent / "data" / "sectors.json"
    with open(data_path, "r") as f:
        raw = json.load(f)

    sectors = {}
    for entry in raw:
        sector = Sector(
            sector_id=entry["id"],
            name=entry["name"],
            description=entry["description"],
            nodes=entry["nodes"]
        )
        sectors[sector.id] = sector

    return sectors

def connect_sectors_to_nodes(sectors, nodes):
    for sector in sectors.values():
        sector.node_objs = []
        for node_id in sector.nodes:
            if node_id in nodes:
                sector.node_objs.append(nodes[node_id])
