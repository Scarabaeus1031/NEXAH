import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class StabilityAttractorNetwork:

    def __init__(self, flow, radius=0.4):

        self.flow = flow
        self.radius = radius

    def _cluster(self, points):

        clusters = []

        for p in points:

            found = False

            for c in clusters:

                if np.linalg.norm(p-c) < self.radius:
                    found=True

            if not found:
                clusters.append(p)

        return np.array(clusters)

    def compute(self, starts):

        traj = self.flow.simulate_many(starts)

        ends = np.array([t[-1] for t in traj])

        attractors = self._cluster(ends)

        edges=[]

        for i,s in enumerate(starts):

            e = ends[i]

            idx = np.argmin(np.linalg.norm(attractors-e,axis=1))

            edges.append((i,idx))

        return attractors, edges

    def plot(self, attractors, edges):

        G = nx.Graph()

        for i,a in enumerate(attractors):
            G.add_node(i,pos=a)

        for s,a in edges:
            G.add_edge(s,a)

        pos = nx.get_node_attributes(G,"pos")

        nx.draw(G,pos,with_labels=True,node_size=300)

        plt.title("Attractor Network")

        plt.show()
