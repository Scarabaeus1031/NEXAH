class PolicyEngine:

    def decide(self, state, regimes):

        if state in regimes["failure"]:
            return "isolate_system"

        if state in regimes["stress"]:
            return "redispatch_resources"

        return "maintain"
