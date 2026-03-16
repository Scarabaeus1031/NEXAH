from collections import deque


class NavigationEngine:
    """
    Basic navigation engine for NEXAH.

    Computes safe paths through a StateGraph.
    """

    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, target):
        """
        Breadth-first search to compute shortest path.
        """

        visited = set()
        queue = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()

            if node == target:
                return path

            if node in visited:
                continue

            visited.add(node)

            for neighbor in self.graph.neighbors(node):
                queue.append((neighbor, path + [neighbor]))

        return None
