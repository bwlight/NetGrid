class TravelSystem:
    def __init__(self, sectors, nodes):
        self.sectors = sectors
        self.nodes = nodes

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def neighbors(self, node_id):
        """Return all nodes directly connected to this one."""
        node = self.get_node(node_id)
        if not node:
            return []
        return [self.get_node(n) for n in node.connections]

    def can_travel(self, start_id, end_id):
        """Simple check: are they directly connected?"""
        start = self.get_node(start_id)
        return end_id in start.connections if start else False
