class StabilityMaximizingPolicy:
    """
    Chooses actions that maximize distance from collapse
    (i.e. maximize risk distance).
    """

    def __init__(self, delta, action_effect, risk_map, actions):
        self.delta = delta
        self.action_effect = action_effect
        self.risk_map = risk_map
        self.actions = actions

    def evaluate_action(self, state, action):
        """
        Determine resulting state after applying action.
        """

        if (state, action) in self.action_effect:
            return self.action_effect[(state, action)]

        return self.delta.get(state, state)

    def choose(self, state):
        """
        Choose action that maximizes distance from collapse.
        """

        best_action = None
        best_score = -float("inf")

        for action in self.actions:

            next_state = self.evaluate_action(state, action)

            score = self.risk_map.get(next_state, -float("inf"))

            if score > best_score:
                best_score = score
                best_action = action

        return best_action
