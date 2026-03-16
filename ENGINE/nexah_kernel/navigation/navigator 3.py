class Navigator:

    """
    Navigate through regime graphs.
    """

    def __init__(self, regime_graph):

        self.regime_graph = regime_graph


    def reachable_regimes(self, start_regime):

        visited = set()
        stack = [start_regime]

        reachable = []

        while stack:

            regime = stack.pop()

            if regime not in visited:

                visited.add(regime)
                reachable.append(regime)

                next_regimes = self.regime_graph.get_transitions(regime)

                stack.extend(next_regimes)

        return reachable
