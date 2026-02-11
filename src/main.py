from netgrid.core.sectors import load_sectors

def main():
    sectors = load_sectors()
    print("Loaded sectors:")
    for s in sectors.values():
        print(f" - {s.name}: {s.description}")

if __name__ == "__main__":
    main()

from netgrid.core.nodes import load_nodes

def main():
    nodes = load_nodes()
    print("Loaded nodes:")
    for n in nodes.values():
        print(f" - {n.id} ({n.type}) connects to {n.connections}")

if __name__ == "__main__":
    main()

from netgrid.core.sectors import load_sectors, connect_sectors_to_nodes
from netgrid.core.nodes import load_nodes, connect_nodes_to_sectors

def main():
    sectors = load_sectors()
    nodes = load_nodes()

    connect_nodes_to_sectors(nodes, sectors)
    connect_sectors_to_nodes(sectors, nodes)

    print("Sectors and Nodes connected!\n")

    for sector in sectors.values():
        print(f"{sector.name} contains:")
        for n in sector.node_objs:
            print(f"  - {n.id} ({n.type})")

if __name__ == "__main__":
    main()
