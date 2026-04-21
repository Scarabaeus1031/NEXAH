class RegimeDetector:

    def __init__(self, graph):
        self.graph = graph

    def detect_stable_states(self):
        stable = []
        for node in self.graph.nodes:
            if len(self.graph.neighbors(node)) == 0:
                stable.append(node)
        return stable
