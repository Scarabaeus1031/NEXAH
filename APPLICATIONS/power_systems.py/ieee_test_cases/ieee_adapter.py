"""
NEXAH IEEE Test Systems Adapter
Connects standard IEEE power system test cases (14-bus, 30-bus, etc.)
to the NEXAH framework.
Uses pandapower for loading and simulation.
"""

import pandapower.networks as pn
import networkx as nx
from typing import Dict, Any, List

# Optional import (failsafe if adapter not present yet)
try:
    from APPLICATIONS.adapters.base_adapter import NexahAdapter
except ImportError:
    class NexahAdapter:
        def __init__(self, config=None):
            self.config = config or {}

class IEEEAdapter(NexahAdapter):
    """
    Adapter for IEEE Test Systems (14-bus, 30-bus, 57-bus, 118-bus, ...)
    Converts the power system into a NEXAH-compatible state graph.
    """

    def __init__(self, system: str = "14", config: Dict[str, Any] = None):
        super().__init__(config)
        self.system = system
        self.net = self._load_ieee_system()
        self.graph = self._build_initial_graph()

    # ===================================================================
    # LOAD IEEE SYSTEM
    # ===================================================================

    def _load_ieee_system(self):
        """Load standard IEEE test case via pandapower"""
        if self.system == "14":
            return pn.case14()
        elif self.system == "30":
            return pn.case30()
        elif self.system == "57":
            return pn.case57()
        elif self.system == "118":
            return pn.case118()
        else:
            raise ValueError(f"Unsupported IEEE system: {self.system}")

    # ===================================================================
    # GRAPH CONVERSION
    # ===================================================================

    def _build_initial_graph(self):
        """Convert pandapower network to NetworkX graph"""
        G = nx.Graph()

        # Generator buses
        gen_buses = set(self.net.gen["bus"].values) if len(self.net.gen) > 0 else set()

        # Add buses as nodes
        for idx, bus in self.net.bus.iterrows():
            G.add_node(
                int(idx),
                type="bus",
                vn_kv=bus.vn_kv,
                is_gen=int(idx) in gen_buses
            )

        # Add lines as edges
        for _, line in self.net.line.iterrows():
            G.add_edge(
                int(line.from_bus),
                int(line.to_bus),
                type="line",
                length_km=line.length_km
            )

        return G

    # ===================================================================
    # REQUIRED NexahAdapter METHODS
    # ===================================================================

    def states(self) -> List[str]:
        """Return discrete stability states"""
        return ["stable", "stressed", "critical", "unstable"]

    def transitions(self) -> Dict[str, List[str]]:
        """Define transitions between regimes"""
        return {
            "stable": ["stressed"],
            "stressed": ["stable", "critical"],
            "critical": ["stressed", "unstable"],
            "unstable": ["critical"]
        }

    def regimes(self) -> Dict[str, str]:
        """Map states to regime labels"""
        return {
            "stable": "STABLE",
            "stressed": "STRESS",
            "critical": "CRITICAL",
            "unstable": "UNSTABLE"
        }

    def initial_state(self) -> str:
        return "stable"

    def risk_targets(self) -> List[str]:
        return ["unstable"]

    def metadata(self) -> Dict[str, Any]:
        return {
            "system": f"IEEE_{self.system}_bus",
            "nodes": len(self.net.bus),
            "lines": len(self.net.line),
            "generator_count": len(self.net.gen),
            "adapter": "IEEEAdapter",
            "simulator": "pandapower"
        }

    def to_state_graph(self) -> Dict[str, Any]:
        """Export complete graph for NEXAH"""
        return {
            "states": self.states(),
            "transitions": self.transitions(),
            "regimes": self.regimes(),
            "initial_state": self.initial_state(),
            "risk_targets": self.risk_targets(),
            "actions": ["increase_load", "decrease_load", "shed_load"],
            "metadata": self.metadata(),
            "graph": self.graph
        }

    # ===================================================================
    # OPTIONAL (FUTURE DYNAMICS)
    # ===================================================================

    def reset(self):
        return self.get_observation()

    def step(self, action=None):
        # Placeholder for dynamic simulation
        return self.get_observation()

    def get_observation(self):
        return {
            "system": f"IEEE_{self.system}_bus",
            "num_buses": len(self.net.bus),
            "num_lines": len(self.net.line),
            "graph": self.graph
        }
