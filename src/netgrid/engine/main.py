from netgrid.core.sectors import load_sectors, connect_sectors_to_nodes
from netgrid.core.nodes import load_nodes, connect_nodes_to_sectors
from netgrid.core.travel import TravelSystem
from pathlib import Path

def main():
    sectors = load_sectors()
    nodes = load_nodes()
    
    connect_nodes_to_sectors(nodes, sectors)
    connect_sectors_to_nodes(sectors, nodes)
    
    travel_map_path = Path(__file__).parent.parent.parent.parent / "data" / "world" / "travel_map.json"
    travel = TravelSystem(travel_map_path)
    
    print("Neighbors of root-gate:")
    # Get neighbors from the graph
    if "root-gate" in travel.graph:
        for edge in travel.graph["root-gate"]:
            print(" -", edge["to"])

if __name__ == "__main__":
    main()
