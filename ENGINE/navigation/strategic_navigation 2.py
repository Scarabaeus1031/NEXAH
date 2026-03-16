class StrategicNavigator:
    """
    Computes multi-step stabilization strategies.

    Explores possible future trajectories and selects the path
    that maximizes stability (distance from collapse).
    """

    def __init__(self, delta, action_effect, risk_map, actions, max_depth=5):
        self.delta = delta
        self.action_effect = action_effect
        self.risk_map = risk_map
        self.actions = actions
        self.max_depth = max_depth


    def next_state(self, state, action):
        """
        Determine next state under action.
        """

        if (state, action) in self.action_effect:
            return self.action_effect[(state, action)]

        return self.delta.get(state, state)


    def explore(self, state, depth):
        """
        Explore future trajectories.
        """

        if depth == 0:
            return [[state]]

        paths = []

        for action in self.actions:

            next_state = self.next_state(state, action)

            subpaths = self.explore(next_state, depth - 1)

            for sp in subpaths:
                paths.append([state] + sp)

        return paths


    def evaluate_path(self, path):
        """
        Compute stability score for a path.
        """

        score = 0

        for state in path:
            score += self.risk_map.get(state, 0)

        return score


    def best_strategy(self, start_state):
        """
        Compute best stabilization trajectory.
        """

        paths = self.explore(start_state, self.max_depth)

        best_path = None
        best_score = -float("inf")

        for p in paths:

            score = self.evaluate_path(p)

            if score > best_score:
                best_score = score
                best_path = p

        return best_path, best_score
