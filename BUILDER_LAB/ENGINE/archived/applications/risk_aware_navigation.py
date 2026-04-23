import heapq


class RiskAwareNavigator:
    """
    NEXAH Risk-Aware Navigation.

    Computes paths that minimize system risk.
    """

    def __init__(self, graph, risk_map):
        self.graph = graph
        self.risk_map = risk_map

    def risk(self, state):
        """Return risk value for a state."""
        return self.risk_map.get(state, 1)

    def safest_path(self, start, target):
        """
        Dijkstra-style search minimizing accumulated risk.
        """

        queue = []
        heapq.heappush(queue, (0, start, [start]))

        visited = {}

        while queue:
            total_risk, state, path = heapq.heappop(queue)

            if state == target:
                return path, total_risk

            if state in visited and visited[state] <= total_risk:
                continue

            visited[state] = total_risk

            for neighbor in self.graph.neighbors(state):
                risk = total_risk + self.risk(neighbor)
                heapq.heappush(queue, (risk, neighbor, path + [neighbor]))

        return None, None
