"""
NEXAH Base Adapter Interface

Adapters connect external simulators or system models to the NEXAH
navigation engine.

They translate external system dynamics into a finite state graph
representation that can be analyzed by NEXAH.

Architecture:

    External System / Simulator
              ↓
            Adapter
              ↓
        State Graph
              ↓
             NEXAH
              ↓
            Policy
              ↓
            Actions

This adapter supports two modes:

1) Graph Mode
   Systems already defined as discrete state graphs.

2) Dynamic Mode (optional extension)
   Continuous dynamical systems that are projected into
   a state graph representation.
"""


class NexahAdapter:
    """
    Base adapter interface for connecting external systems to the NEXAH framework.

    Implementations translate external simulator states into a NEXAH-compatible
    finite state graph representation.
    """

    # -----------------------------------------------------------
    # REQUIRED METHODS (GRAPH STRUCTURE)
    # -----------------------------------------------------------

    def states(self):
        """
        Return the list or set of system states.

        Example:
            ["stable", "stress", "failure"]
        """
        raise NotImplementedError("states() must be implemented by the adapter.")

    def transitions(self):
        """
        Return system transitions.

        Expected format:
        {
            "state_a": ["state_b", "state_c"],
            "state_b": ["state_c"]
        }
        """
        raise NotImplementedError("transitions() must be implemented by the adapter.")

    # -----------------------------------------------------------
    # OPTIONAL GRAPH METHODS
    # -----------------------------------------------------------

    def regimes(self):
        """
        Optional regime classification for states.

        Example:
        {
            "stable": "STABLE",
            "stress": "STRESS",
            "failure": "FAILURE"
        }
        """
        return None

    def initial_state(self):
        """
        Optional starting state for navigation.

        Example:
            "stable"
        """
        return None

    def risk_targets(self):
        """
        Optional list of states representing failure or collapse conditions.

        Example:
            ["failure", "collapse"]
        """
        return []

    def actions(self):
        """
        Optional list of control actions that policies may apply.

        Example:
            ["shed_load", "reroute_power", "restart_node"]
        """
        return []

    def transition_probabilities(self):
        """
        Optional transition probability structure.

        Example:
        {
            "stable": {"stable": 0.7, "stress": 0.3},
            "stress": {"failure": 0.5, "stable": 0.5}
        }
        """
        return None

    def metadata(self):
        """
        Optional metadata describing the system model.

        Example:
        {
            "system_type": "power_grid",
            "nodes": 120,
            "simulator": "pandapower"
        }
        """
        return {}

    # -----------------------------------------------------------
    # OPTIONAL DYNAMIC SYSTEM INTERFACE
    # -----------------------------------------------------------

    def reset(self):
        """
        Optional method for dynamic systems.

        Reset simulation state.
        """
        return None

    def step(self, action=None):
        """
        Optional simulation step.

        Advance system dynamics by one time step.
        """
        return None

    def observe(self):
        """
        Optional observation for dynamic systems.

        Return current system state.

        Example:
            {"x": 1.2, "y": 0.4, "z": 2.1}
        """
        return None

    # -----------------------------------------------------------
    # GRAPH EXPORT
    # -----------------------------------------------------------

    def to_state_graph(self):
        """
        Export adapter data as a unified NEXAH state graph.

        This ensures that all adapters produce a consistent format
        for the navigation engine.
        """

        graph = {
            "states": self.states(),
            "transitions": self.transitions(),
            "regimes": self.regimes(),
            "initial_state": self.initial_state(),
            "risk_targets": self.risk_targets(),
            "actions": self.actions(),
            "transition_probabilities": self.transition_probabilities(),
            "metadata": self.metadata(),
        }

        return graph
