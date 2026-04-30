from collections import defaultdict


class StateGraph:
    """
    Basic directed state graph used by the NEXAH framework.

    Nodes represent system states.
    Edges represent possible transitions between states.
    """

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_state(self, state):
        """Add a state node."""
        self.nodes.add(state)

    def add_transition(self, a, b):
        """Add a directed transition a → b."""
        self.nodes.add(a)
        self.nodes.add(b)
        self.edges[a].add(b)

    def neighbors(self, state):
        """Return reachable states from a given state."""
        return self.edges.get(state, set())

    def transitions(self):
        """Return all transitions."""
        for a in self.edges:
            for b in self.edges[a]:
                yield (a, b)

    def __repr__(self):
        return f"StateGraph(nodes={len(self.nodes)}, transitions={sum(len(v) for v in self.edges.values())})"
