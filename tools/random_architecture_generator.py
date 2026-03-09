"""
Random Architecture Generator for NEXAH

Creates diverse network topologies for resilience exploration.
"""

import random
import networkx as nx


def generate_random_architecture():

    topology = random.choice([
        "erdos_renyi",
        "scale_free",
        "small_world"
    ])

    n = random.randint(5, 40)

    if topology == "erdos_renyi":

        p = random.uniform(0.1, 0.4)
        G = nx.erdos_renyi_graph(n, p, directed=True)

    elif topology == "scale_free":

        m = random.randint(1, 4)
        G = nx.barabasi_albert_graph(n, m).to_directed()

    elif topology == "small_world":

        k = random.randint(2, 6)
        p = random.uniform(0.1, 0.3)
        G = nx.watts_strogatz_graph(n, k, p).to_directed()

    else:

        G = nx.gnp_random_graph(n, 0.2, directed=True)

    architecture = {
        "graph": G,
        "topology": topology,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges()
    }

    return architecture
