"""
MEVA — Action Engine

The MEVA layer translates navigation insights into
simulated architectural interventions.

It allows the NEXAH system to test how small structural
changes influence system resilience.
"""

from .models import NavigationResult


class ActionEngine:

    def __init__(self, graph, landscape):

        self.graph = graph
        self.landscape = landscape

    # ---------------------------------------------------
    # ACTION SIMULATION
    # ---------------------------------------------------

    def simulate_action(self, action):

        """
        Simulate a structural modification.
        """

        modified_graph = self._apply_action(action)

        return modified_graph

    # ---------------------------------------------------

    def evaluate_action(self, action, resilience_analyzer):

        """
        Apply action and evaluate resilience change.
        """

        modified_graph = self._apply_action(action)

        new_resilience = resilience_analyzer(modified_graph)

        return {
            "action": action,
            "resilience": new_resilience
        }

    # ---------------------------------------------------

    def explore_actions(self, action_space, resilience_analyzer):

        """
        Test multiple structural actions.
        """

        results = []

        for action in action_space:

            result = self.evaluate_action(action, resilience_analyzer)

            results.append(result)

        return results

    # ---------------------------------------------------

    def _apply_action(self, action):

        """
        Internal function applying structural changes.
        """

        # shallow copy of graph structure
        nodes = dict(self.graph.nodes)
        edges = list(self.graph.edges)

        if action["type"] == "add_node":

            node_id = action["node"]
            nodes[node_id] = {}

        elif action["type"] == "remove_node":

            node_id = action["node"]
            nodes.pop(node_id, None)

            edges = [
                e for e in edges
                if node_id not in e
            ]

        elif action["type"] == "add_edge":

            edges.append(action["edge"])

        elif action["type"] == "remove_edge":

            if action["edge"] in edges:
                edges.remove(action["edge"])

        return {
            "nodes": nodes,
            "edges": edges
        }
