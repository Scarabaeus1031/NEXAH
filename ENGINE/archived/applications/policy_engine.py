class PolicyEngine:
    """
    Basic rule-based policy engine for NEXAH.

    Maps system states and regime classifications
    to stabilization actions.
    """

    def __init__(self, regimes):
        self.regimes = regimes

    def decide(self, state):
        """
        Decide which action to apply based on regime class.
        """

        if state in self.regimes.get("failure", []):
            return "start_reserve"

        if state in self.regimes.get("stress", []):
            return "reconfigure_grid"

        if state in self.regimes.get("stable", []):
            return "maintain"

        return "monitor"
