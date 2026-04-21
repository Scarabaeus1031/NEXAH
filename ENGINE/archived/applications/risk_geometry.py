from collections import deque


class RiskGeometry:

    def __init__(self, graph):
        self.graph = graph

    def distance_to_target(self, target):
        """
        Compute distance from every node to target state.
        """

        distances = {target: 0}
        queue = deque([target])

        while queue:
            current = queue.popleft()

            for node in self.graph.nodes:
                if current in self.graph.neighbors(node):

                    if node not in distances:
                        distances[node] = distances[current] + 1
                        queue.append(node)

        return distances
