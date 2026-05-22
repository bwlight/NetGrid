import json
from pathlib import Path

class Sector:
    def __init__(self, sector_id, name, description):
        self.id = sector_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Sector {self.id}: {self.name}>"

def load_sectors():
    data_path = Path(__file__).parent.parent.parent.parent / "data" / "world" / "sectors.json"
    with open(data_path, "r") as f:
        raw = json.load(f)

    sectors = {}
    for sector_id, entry in raw.items():
        sector = Sector(
            sector_id=entry["id"],
            name=entry["name"],
            description=entry["description"]
        )
        sectors[sector.id] = sector

    return sectors

def connect_sectors_to_nodes(sectors, nodes):
    pass
