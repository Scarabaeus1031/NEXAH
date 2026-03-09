from __future__ import annotations

import numpy as np
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# BUILD FINANCIAL NETWORK
# ---------------------------------------------------

def build_financial_network(cities):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            debt=np.random.uniform(0.7, 1.1),
            stability=np.random.uniform(0.4, 0.7)
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            if np.random.random() < 0.03:

                exposure = np.random.uniform(0.1, 0.6)

                G.add_edge(nodes[i], nodes[j], exposure=exposure)

    return G


# ---------------------------------------------------
# FINANCIAL DRIFT
# ---------------------------------------------------

def financial_drift(G):

    for node in G.nodes:

        # slow increase of debt
        G.nodes[node]["debt"] += np.random.normal(0.01, 0.02)

        # partial recovery
        G.nodes[node]["debt"] *= np.random.uniform(0.98, 1.01)

        # clamp minimum
        G.nodes[node]["debt"] = max(0.3, G.nodes[node]["debt"])


# ---------------------------------------------------
# CONTAGION
# ---------------------------------------------------

def propagate_financial_shock(G):

    cascades = []

    for node in G.nodes:

        debt = G.nodes[node]["debt"]

        if debt > 1.4 and np.random.random() < 0.1:

            cascades.append(node)

            for n in G.neighbors(node):

                exposure = G.edges[node, n]["exposure"]

                G.nodes[n]["debt"] += exposure * 0.05

    return cascades


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_financial_network(cities)

    year = 2025

    for step in range(40):

        year += 5

        financial_drift(G)

        cascades = propagate_financial_shock(G)

        print(
            "Year:", year,
            "Financial cascade events:", len(cascades)
        )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
