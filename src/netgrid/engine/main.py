from netgrid.core.sectors import load_sectors, connect_sectors_to_nodes
from netgrid.core.nodes import load_nodes, connect_nodes_to_sectors
from netgrid.core.travel import TravelSystem

def main():
    sectors = load_sectors()
    nodes = load_nodes()

    connect_nodes_to_sectors(nodes, sectors)
    connect_sectors_to_nodes(sectors, nodes)

    travel = TravelSystem(sectors, nodes)

    print("Neighbors of root-gate:")
    for n in travel.neighbors("root-gate"):
        print(" -", n.id)

if __name__ == "__main__":
    main()
