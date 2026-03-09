from __future__ import annotations

import numpy as np
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# GEOPOLITICAL NETWORK
# ---------------------------------------------------

def build_geopolitical_network(cities):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            tension=np.random.uniform(0,0.2)
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):

        for j in range(i+1,len(nodes)):

            if np.random.random() < 0.05:

                G.add_edge(nodes[i],nodes[j])

    return G


# ---------------------------------------------------
# ESCALATION
# ---------------------------------------------------

def escalate_conflicts(G):

    conflicts = []

    for node in G.nodes:

        tension = G.nodes[node]["tension"]

        tension += np.random.normal(0,0.01)

        if tension > 0.4:

            conflicts.append(node)

            for n in G.neighbors(node):

                G.nodes[n]["tension"] += 0.05

        G.nodes[node]["tension"] = max(0,tension)

    return conflicts


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_geopolitical_network(cities)

    year = 2025

    for step in range(40):

        year += 5

        conflicts = escalate_conflicts(G)

        print("Year:",year,"Conflicts:",len(conflicts))


if __name__ == "__main__":
    run()
