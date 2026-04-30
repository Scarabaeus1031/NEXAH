class CascadeAnalysis:
    """
    Detect cascade paths in a StateGraph.

    Cascades occur when transitions move toward higher risk
    or deeper failure regimes.
    """

    def __init__(self, graph, distance_map):
        self.graph = graph
        self.distance_map = distance_map

    def cascade_sources(self):
        """
        Identify states that lead to higher risk states.
        """

        sources = []

        for node in self.graph.nodes:
            for neighbor in self.graph.neighbors(node):

                node_risk = self.distance_map.get(node, 0)
                neigh_risk = self.distance_map.get(neighbor, 0)

                if neigh_risk > node_risk:
                    sources.append(node)
                    break

        return sources

    def cascade_paths(self, start):
        """
        Follow transitions starting from a node.
        """

        path = [start]
        current = start

        while True:

            neighbors = list(self.graph.neighbors(current))

            if not neighbors:
                break

            next_node = neighbors[0]
            path.append(next_node)

            current = next_node

        return path
