"""
NEXAH IEEE Test Systems Adapter
Connects standard IEEE power system test cases (14-bus, 30-bus, etc.)
to the NEXAH framework.
Uses pandapower for loading and simulation.
"""

import pandapower as pp
import networkx as nx
from APPLICATIONS.adapters.base_adapter import NexahAdapter
from typing import Dict, Any, List

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

    def _load_ieee_system(self):
        """Load standard IEEE test case via pandapower"""
        if self.system == "14":
            return pp.networks.case14()
        elif self.system == "30":
            return pp.networks.case30()
        elif self.system == "57":
            return pp.networks.case57()
        elif self.system == "118":
            return pp.networks.case118()
        else:
            raise ValueError(f"Unsupported IEEE system: {self.system}")

    def _build_initial_graph(self):
        """Convert pandapower network to NetworkX graph"""
        G = nx.Graph()
        # Add buses as nodes
        for idx, bus in self.net.bus.iterrows():
            G.add_node(int(bus.name), 
                       type="bus",
                       vn_kv=bus.vn_kv,
                       is_gen=idx in self.net.gen.bus.values)
        # Add lines as edges
        for _, line in self.net.line.iterrows():
            G.add_edge(int(line.from_bus), int(line.to_bus),
                       type="line",
                       length_km=line.length_km)
        return G

    # ===================================================================
    # REQUIRED NexahAdapter METHODS
    # ===================================================================

    def states(self) -> List[str]:
        """Return discrete states (we use a simple stability classification)"""
        return ["stable", "stressed", "critical", "unstable"]

    def transitions(self) -> Dict[str, List[str]]:
        """Define possible transitions between stability regimes"""
        return {
            "stable": ["stressed"],
            "stressed": ["stable", "critical"],
            "critical": ["stressed", "unstable"],
            "unstable": ["critical"]
        }

    def regimes(self) -> Dict[str, str]:
        """Map internal states to regime labels"""
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
            "graph": self.graph  # NetworkX graph for advanced use
        }

    # Optional dynamic methods (for future step-by-step simulation)
    def reset(self):
        return self.get_observation()

    def step(self, action=None):
        # Placeholder for dynamic load / generation changes
        return self.get_observation()

    def get_observation(self):
        return {
            "system": f"IEEE_{self.system}_bus",
            "num_buses": len(self.net.bus),
            "graph": self.graph
        }
