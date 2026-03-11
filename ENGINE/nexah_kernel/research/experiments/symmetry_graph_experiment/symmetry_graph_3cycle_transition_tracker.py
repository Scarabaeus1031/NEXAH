also das habe ich gesaved... """
NEXAH Symmetry Graph – 3 Cycle Transition Tracker
-------------------------------------------------

Tracks the dynamical transition structure of the

center + 17 spokes
C5 + C6 + C6

symmetry graph under Kuramoto dynamics.

Measured over time:
• global synchronization R(t)
• cycle windings
• vortex count
• final phase state

Interpretation:
Θ = random phase field
Τ = local clustering
Δ = domain locking
Ι = vortex collapse
Υ = global synchronization
"""

import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from core.symmetry_graph_vortex_detector import wrap_phase, phase_winding


# --------------------------------------------------
# Build graph
# --------------------------------------------------

def build_graph():
    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    pentagon = spokes[0:5]
    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i + 1) % 5])

    hexagon1 = spokes[5:11]
    for i in range(6):
        G.add_edge(hexagon1[i], hexagon1[(i + 1) % 6])

    hexagon2 = spokes[11:17]
    for i in range(6):
        G.add_edge(hexagon2[i], hexagon2[(i + 1) % 6])

    return G


# --------------------------------------------------
# Layout
# --------------------------------------------------

def layout_graph(G):
    pos = {}

    center = "center"
    pos[center] = (0.0, 0.0)

    radius = 3.0
    spokes = [n for n in G.nodes() if n != center]

    for i, node in enumerate(spokes):
        angle = 2 * math.pi * i / len(spokes)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        pos[node] = (x, y)

    return pos


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def ordered_nodes():
    return ["center"] + [f"s{i}" for i in range(17)]


def adjacency_matrix(G, nodes):
    n = len(nodes)

    index = {node: i for i, node in enumerate(nodes)}

    A = np.zeros((n, n))

    for u, v in G.edges():
        i = index[u]
        j = index[v]

        A[i, j] = 1
        A[j, i] = 1

    return A


def initial_phases(nodes, seed=1):

    rng = np.random.default_rng(seed)

    theta = rng.uniform(0, 2 * np.pi, len(nodes))

    return np.array([wrap_phase(x) for x in theta])


def intrinsic_frequencies(nodes):

    omega = np.zeros(len(nodes))

    for i, node in enumerate(nodes):

        if node == "center":
            omega[i] = 0.0

        else:
            k = int(node[1:])
            omega[i] = 0.1 * np.sin(2 * np.pi * k / 17)

    return omega


# --------------------------------------------------
# Kuramoto dynamics
# --------------------------------------------------

def kuramoto_step(theta, omega, A, K, dt):

    n = len(theta)

    dtheta = np.zeros(n)

    for i in range(n):

        coupling = 0.0

        for j in range(n):

            if A[i, j] != 0:
                coupling += np.sin(theta[j] - theta[i])

        dtheta[i] = omega[i] + K * coupling

    theta = theta + dt * dtheta

    theta = np.array([wrap_phase(x) for x in theta])

    return theta


def order_parameter(theta):

    z = np.mean(np.exp(1j * theta))

    return np.abs(z)


# --------------------------------------------------
# Cycle analysis
# --------------------------------------------------

def cycle_windings(G, nodes, theta):

    node_index = {n: i for i, n in enumerate(nodes)}

    cycles = nx.cycle_basis(G)

    results = []

    for cycle in cycles:

        phases = [theta[node_index[n]] for n in cycle]

        winding = phase_winding(phases, list(range(len(cycle))))

        results.append((cycle, winding))

    return results


def count_vortices(results):

    count = 0

    for cycle, w in results:

        if abs(w) > 0.5:
            count += 1

    return count


# --------------------------------------------------
# Simulation
# --------------------------------------------------

def simulate(G, steps=300, dt=0.04, K=0.3):

    nodes = ordered_nodes()

    A = adjacency_matrix(G, nodes)

    theta = initial_phases(nodes)

    omega = intrinsic_frequencies(nodes)

    history_R = []
    history_vortex = []

    for step in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

        R = order_parameter(theta)

        cycles = cycle_windings(G, nodes, theta)

        vortex_count = count_vortices(cycles)

        history_R.append(R)

        history_vortex.append(vortex_count)

    return nodes, theta, history_R, history_vortex


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def draw_graph(G, nodes, theta):

    pos = layout_graph(G)

    node_index = {n: i for i, n in enumerate(nodes)}

    colors = [theta[node_index[n]] for n in G.nodes()]

    plt.figure(figsize=(8, 8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500,
        node_color=colors,
        cmap="hsv"
    )

    nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_labels(G, pos)

    plt.title("Final Phase State")

    plt.axis("off")

    plt.show()


def plot_transition(history_R, history_vortex):

    plt.figure(figsize=(10, 4))

    plt.subplot(121)
    plt.plot(history_R)
    plt.title("Global synchronization R")

    plt.subplot(122)
    plt.plot(history_vortex)
    plt.title("Vortex count")

    plt.tight_layout()

    plt.show()


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":

    G = build_graph()

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    nodes, theta, history_R, history_vortex = simulate(G)

    draw_graph(G, nodes, theta)

    plot_transition(history_R, history_vortex)
