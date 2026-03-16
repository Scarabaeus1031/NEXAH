import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class StabilityAttractorNetwork:

    def __init__(self, flow_engine, attractor_radius=0.3):

        self.flow = flow_engine
        self.radius = attractor_radius

    def _cluster(self, endpoints):

        clusters = []

        for p in endpoints:

            assigned = False

            for c in clusters:

                if np.linalg.norm(p - c) < self.radius:
                    assigned = True
                    break

            if not assigned:
                clusters.append(p)

        return np.array(clusters)

    def compute(self, starts):

        trajectories = self.flow.simulate_many(starts)

        endpoints = np.array([traj[-1] for traj in trajectories])

        attractors = self._cluster(endpoints)

        edges = []

        for i, start in enumerate(starts):

            end = endpoints[i]

            idx = np.argmin(np.linalg.norm(attractors - end, axis=1))

            edges.append((tuple(start), idx))

        return attractors, edges

    def plot(self, attractors, edges):

        G = nx.Graph()

        for i, a in enumerate(attractors):
            G.add_node(i, pos=a)

        for s, a in edges:
            G.add_edge(str(s), a)

        pos = {}

        for node in G.nodes():

            if isinstance(node, int):
                pos[node] = attractors[node]
            else:
                pos[node] = eval(node)

        plt.figure(figsize=(8,6))

        nx.draw(G, pos, with_labels=True, node_size=300)

        plt.title("Attractor Network")

        plt.show()
