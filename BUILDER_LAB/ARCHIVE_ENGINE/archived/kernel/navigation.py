from .models import NavigationResult


class NavigationEngine:

    def __init__(self, graph, landscape):

        self.graph = graph
        self.landscape = landscape

    def evaluate_paths(self):

        trajectories = []
        leverage_points = []

        # placeholder logic
        for node in self.graph.nodes:

            trajectories.append(node)

        return NavigationResult(
            trajectories=trajectories,
            leverage_points=leverage_points,
        )
