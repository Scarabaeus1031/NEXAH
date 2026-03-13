from ..base_adapter import NexahAdapter


class PowerGridAdapter(NexahAdapter):

    def states(self):
        return [
            "stable",
            "frequency_drop",
            "line_overload",
            "failure",
            "blackout"
        ]

    def transitions(self):

        return {
            "stable": ["frequency_drop"],
            "frequency_drop": ["line_overload", "stable"],
            "line_overload": ["failure"],
            "failure": ["blackout"],
            "blackout": []
        }

    def regimes(self):

        return {
            "stable": "STABLE",
            "frequency_drop": "STRESS",
            "line_overload": "CRITICAL",
            "failure": "FAILURE",
            "blackout": "COLLAPSE"
        }

    def risk_targets(self):
        return ["failure", "blackout"]

    def actions(self):
        return [
            "shed_load",
            "activate_reserve",
            "reroute_power"
        ]

    def metadata(self):
        return {
            "system": "Power Grid",
            "domain": "energy_infrastructure"
        }
