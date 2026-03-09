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
            debt=np.random.uniform(0.6,1.2),
            stability=np.random.uniform(0.4,0.7)
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):

        for j in range(i+1,len(nodes)):

            # financial exposure probability
            if np.random.random() < 0.04:

                exposure = np.random.uniform(0.2,1.0)

                G.add_edge(nodes[i],nodes[j],exposure=exposure)

    return G


# ---------------------------------------------------
# GLOBAL DRIFT
# ---------------------------------------------------

def financial_drift(G, year):

    # system fragility grows slowly over time
    fragility = (year - 2025) * 0.002

    for node in G.nodes:

        # rising debt
        G.nodes[node]["debt"] += np.random.normal(0.01 + fragility, 0.02)

        # partial recovery
        G.nodes[node]["debt"] *= np.random.uniform(0.97, 1.01)

        # clamp values
        G.nodes[node]["debt"] = max(0.3, G.nodes[node]["debt"])


# ---------------------------------------------------
# CLIMATE SHOCK
# ---------------------------------------------------

def climate_financial_shock(G):

    shock_nodes = []

    for node in G.nodes:

        if np.random.random() < 0.02:

            G.nodes[node]["debt"] += np.random.uniform(0.3,0.7)

            shock_nodes.append(node)

    return shock_nodes


# ---------------------------------------------------
# CONTAGION
# ---------------------------------------------------

def propagate_financial_shock(G):

    cascade = []

    for node in list(G.nodes):

        debt = G.nodes[node]["debt"]

        if debt > 1.6:

            cascade.append(node)

            for n in G.neighbors(node):

                exposure = G.edges[node,n]["exposure"]

                G.nodes[n]["debt"] += exposure * 0.15

    return cascade


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_financial_network(cities)

    year = 2025

    for step in range(50):

        year += 5

        # slow financial drift
        financial_drift(G, year)

        # climate-linked shock
        climate_shocks = climate_financial_shock(G)

        # cascade propagation
        cascades = propagate_financial_shock(G)

        total_events = len(climate_shocks) + len(cascades)

        print(
            "Year:",year,
            "Climate shocks:",len(climate_shocks),
            "Cascade events:",len(cascades),
            "Total financial stress:",total_events
        )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
