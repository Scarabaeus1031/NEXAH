from __future__ import annotations

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# BUILD FINANCIAL NETWORK
# ---------------------------------------------------

def build_financial_network(cities):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            debt=np.random.uniform(0.5,1.5),
            stability=0.33
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):

        for j in range(i+1,len(nodes)):

            if np.random.random() < 0.03:

                exposure = np.random.uniform(0.2,1.0)

                G.add_edge(nodes[i],nodes[j],exposure=exposure)

    return G


# ---------------------------------------------------
# FINANCIAL CONTAGION
# ---------------------------------------------------

def propagate_financial_shock(G):

    shocks = []

    for node in G.nodes:

        debt = G.nodes[node]["debt"]

        if debt > 1.3 and np.random.random() < 0.2:

            shocks.append(node)

            for n in G.neighbors(node):

                G.nodes[n]["debt"] += 0.1

    return shocks


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_financial_network(cities)

    year = 2025

    for step in range(40):

        year += 5

        shocks = propagate_financial_shock(G)

        print("Year:",year,"Financial shocks:",len(shocks))


if __name__ == "__main__":
    run()
