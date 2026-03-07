class CascadeAnalysis:
    """
    Detect potential cascade paths in a StateGraph.

    A cascade path is a sequence of transitions leading deeper
    into failure regions or away from stability.
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

                if self.distance_map.get(neighbor, 0) > self.distance_map.get(node, 0):
                    sources.append(node)
                    break

        return sources

    def cascade_paths(self, start, max_depth=5):
        """
        Explore possible cascade paths starting from a node.
        """

        paths = []

        def dfs(node, path, depth):

            if depth >= max_depth:
                return

            for neighbor in self.graph.neighbors(node):

                new_path = path + [neighbor]
                paths.append(new_path)

                dfs(neighbor, new_path, depth + 1)

        dfs(start, [start], 0)

        return paths
