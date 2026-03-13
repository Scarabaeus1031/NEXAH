from ..base_adapter import NexahAdapter


class SupplyChainAdapter(NexahAdapter):

    def states(self):

        return [
            "normal_operation",
            "supply_delay",
            "inventory_shortage",
            "distribution_failure",
            "system_breakdown"
        ]

    def transitions(self):

        return {
            "normal_operation": ["supply_delay"],
            "supply_delay": ["inventory_shortage", "normal_operation"],
            "inventory_shortage": ["distribution_failure"],
            "distribution_failure": ["system_breakdown"],
            "system_breakdown": []
        }

    def regimes(self):

        return {
            "normal_operation": "STABLE",
            "supply_delay": "STRESS",
            "inventory_shortage": "CRITICAL",
            "distribution_failure": "FAILURE",
            "system_breakdown": "COLLAPSE"
        }

    def risk_targets(self):
        return ["system_breakdown"]

    def actions(self):
        return [
            "reroute_supply",
            "increase_inventory",
            "activate_backup_supplier"
        ]

    def metadata(self):
        return {
            "system": "Supply Chain",
            "domain": "logistics"
        }
