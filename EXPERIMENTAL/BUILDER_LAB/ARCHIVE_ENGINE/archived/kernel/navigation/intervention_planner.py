class InterventionPlanner:

    """
    Select actions that move system toward desired regimes.
    """

    def __init__(self, actions):

        self.actions = actions


    def plan(self, current_regime, target_regime):

        for action in self.actions:

            if action.get("from") == current_regime and action.get("to") == target_regime:
                return action

        return None
