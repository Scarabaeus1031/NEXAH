class RiskMinimizingPolicy:
    """
    Chooses actions that minimize risk distance to target.
    """

    def __init__(self, delta, action_effect, risk_map, actions):
        self.delta = delta
        self.action_effect = action_effect
        self.risk_map = risk_map
        self.actions = actions

    def evaluate_action(self, state, action):
        """
        Compute next state under action.
        """

        if (state, action) in self.action_effect:
            return self.action_effect[(state, action)]

        return self.delta[state]

    def choose(self, state):
        """
        Choose action minimizing risk distance.
        """

        best_action = None
        best_risk = float("inf")

        for a in self.actions:

            next_state = self.evaluate_action(state, a)

            risk = self.risk_map.get(next_state, float("inf"))

            if risk < best_risk:
                best_risk = risk
                best_action = a

        return best_action
