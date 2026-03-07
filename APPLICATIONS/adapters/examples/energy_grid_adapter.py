
"""
Example Energy Grid Adapter for NEXAH

This adapter demonstrates how a power grid simulator (e.g. pandapower, MATPOWER, PyPSA)
could expose its system dynamics as a finite state graph for the NEXAH framework.

This example is intentionally simple and illustrative.
"""

from base_adapter import NexahAdapter


class EnergyGridAdapter(NexahAdapter):
    """
    Minimal demonstration adapter translating a simple grid model
    into a NEXAH-compatible state graph.
    """

    def states(self):
        """
        Return possible system states.
        """
        return [
            "stable",
            "frequency_drop",
            "congestion",
            "failure",
            "collapse"
        ]

    def transitions(self):
        """
        Define possible transitions between states.
        """
        return {
            "stable": ["frequency_drop"],
            "frequency_drop": ["congestion", "stable"],
            "congestion": ["failure", "stable"],
            "failure": ["collapse", "stable"],
            "collapse": []
        }

    def regimes(self):
        """
        Regime classification of system states.
        """
        return {
            "stable": "STABLE",
            "frequency_drop": "STRESS",
            "congestion": "STRESS",
            "failure": "FAILURE",
            "collapse": "COLLAPSE"
        }

    def risk_targets(self):
        """
        Critical system states NEXAH should avoid.
        """
        return ["collapse"]

    def actions(self):
        """
        Example control actions available to policies.
        """
        return [
            "start_reserve",
            "shed_load",
            "redispatch",
            "reconfigure_grid"
        ]


if __name__ == "__main__":
    adapter = EnergyGridAdapter()

    print("States:", adapter.states())
    print("Transitions:", adapter.transitions())
    print("Regimes:", adapter.regimes())
    print("Risk Targets:", adapter.risk_targets())
    print("Actions:", adapter.actions())
