class StrategicNavigator:
    """
    Computes multi-step stabilization strategies.

    Explores future state trajectories and selects the path
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
        Compute next state given an action.
        """

        if (state, action) in self.action_effect:
            return self.action_effect[(state, action)]

        return self.delta.get(state, state)


    def explore(self, state, depth, path, visited):
        """
        Recursively explore possible trajectories.
        """

        if depth == 0:
            return [(path, self.evaluate_path(path))]

        results = []

        for action in self.actions:

            next_state = self.next_state(state, action)

            if next_state in visited:
                continue

            new_path = path + [(action, next_state)]

            visited.add(next_state)

            results.extend(
                self.explore(
                    next_state,
                    depth - 1,
                    new_path,
                    visited
                )
            )

            visited.remove(next_state)

        return results


    def evaluate_path(self, path):
        """
        Score path based on stability values.
        """

        score = 0

        for action, state in path:

            score += self.risk_map.get(state, 0)

        return score


    def best_strategy(self, start_state):
        """
        Compute best stabilization strategy.
        """

        explored = self.explore(
            start_state,
            self.max_depth,
            [],
            {start_state}
        )

        best_path = None
        best_score = -float("inf")

        for path, score in explored:

            if score > best_score:
                best_score = score
                best_path = path

        return best_path, best_score
