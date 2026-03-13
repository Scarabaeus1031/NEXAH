from ..base_adapter import NexahAdapter


class TrafficAdapter(NexahAdapter):

    def states(self):

        return [
            "free_flow",
            "slow_traffic",
            "congestion",
            "gridlock"
        ]

    def transitions(self):

        return {
            "free_flow": ["slow_traffic"],
            "slow_traffic": ["congestion", "free_flow"],
            "congestion": ["gridlock", "slow_traffic"],
            "gridlock": []
        }

    def regimes(self):

        return {
            "free_flow": "STABLE",
            "slow_traffic": "STRESS",
            "congestion": "CRITICAL",
            "gridlock": "COLLAPSE"
        }

    def risk_targets(self):
        return ["gridlock"]

    def actions(self):
        return [
            "reroute_traffic",
            "adaptive_signal_control",
            "open_emergency_lane"
        ]

    def metadata(self):
        return {
            "system": "Traffic Network",
            "domain": "urban_transport"
        }
