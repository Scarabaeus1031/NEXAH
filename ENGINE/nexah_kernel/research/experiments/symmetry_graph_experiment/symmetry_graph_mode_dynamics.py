"""
NEXAH Symmetry Graph – Mode Dynamics
------------------------------------

Projects Kuramoto dynamics of the symmetry graph onto Laplacian eigenmodes.

Goal:
see which resonance modes are actually activated over time.

Outputs:
- global synchronization R(t)
- amplitudes of selected Laplacian modes over time
- final phase distribution
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx


# --------------------------------------------------
# Build symmetry graph
# --------------------------------------------------

def build_symmetry_graph():

    G = nx.Graph()

    # dual hubs
    G.add_node("hub_A")
    G.add_node("hub_B")
    G.add_edge("hub_A", "hub_B")

    # C5 ring
    C5 = [f"C5_{i}" for i in range(5)]
    for i in range(5):
        G.add_edge(C5[i], C5[(i + 1) % 5])

    # C6A ring
    C6A = [f"C6A_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6A[i], C6A[(i + 1) % 6])

    # C6B ring
    C6B = [f"C6B_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6B[i], C6B[(i + 1) % 6])

    # hub connections
    for n in C5:
        G.add_edge("hub_A", n)

    for n in C6A:
        G.add_edge("hub_A", n)

    for n in C6B:
        G.add_edge("hub_B", n)

    return G


# --------------------------------------------------
# Laplacian modes
# --------------------------------------------------

def compute_modes(G):

    nodes = list(G.nodes())
    L = nx.laplacian_matrix(G, nodelist=nodes).astype(float).todense()
    L = np.asarray(L)

    eigenvals, eigenvecs = np.linalg.eigh(L)

    return eigenvals, eigenvecs, nodes


# --------------------------------------------------
# Kuramoto dynamics with trajectory
# --------------------------------------------------

def run_kuramoto_trajectory(G, K=0.12, steps=2500, dt=0.05, omega_std=0.08):

    nodes = list(G.nodes())
    N = len(nodes)

    theta = np.random.uniform(0, 2 * np.pi, N)
    omega = np.random.normal(1.0, omega_std, N)

    adjacency = nx.to_numpy_array(G, nodelist=nodes)

    theta_series = []
    order_series = []

    for _ in range(steps):

        dtheta = np.zeros(N)

        for i in range(N):

            coupling_sum = 0.0

            for j in range(N):
                if adjacency[i, j] > 0:
                    coupling_sum += math.sin(theta[j] - theta[i])

            dtheta[i] = omega[i] + K * coupling_sum

        theta = theta + dtheta * dt
        theta = np.mod(theta, 2 * np.pi)

        theta_series.append(theta.copy())

        r = np.abs(np.sum(np.exp(1j * theta))) / N
        order_series.append(r)

    theta_series = np.array(theta_series)

    return theta_series, order_series, nodes


# --------------------------------------------------
# Mode projection
# --------------------------------------------------

def project_onto_modes(theta_series, eigenvecs, num_modes=6):
    """
    Project cosine phase state onto the first few nontrivial Laplacian modes.

    We skip mode 0 later in plotting because it is the trivial constant mode.
    """

    X = np.cos(theta_series)  # shape: (T, N)

    amplitudes = []

    for m in range(num_modes):
        v = np.asarray(eigenvecs[:, m]).reshape(-1)
        a = X @ v
        amplitudes.append(a)

    return np.array(amplitudes)  # shape: (num_modes, T)


# --------------------------------------------------
# Plotting
# --------------------------------------------------

def plot_mode_dynamics(order_series, mode_amplitudes, eigenvals, theta_final, nodes):

    fig, axs = plt.subplots(3, 1, figsize=(10, 10))

    # 1) global synchronization
    axs[0].plot(order_series)
    axs[0].set_title("Global Synchronization R(t)")
    axs[0].set_xlabel("time step")
    axs[0].set_ylabel("R")

    # 2) mode amplitudes
    # skip trivial mode 0 in visualization, start at mode 1
    for m in range(1, mode_amplitudes.shape[0]):
        axs[1].plot(
            mode_amplitudes[m],
            label=f"mode {m}  λ={eigenvals[m]:.3f}"
        )

    axs[1].set_title("Laplacian Mode Amplitudes")
    axs[1].set_xlabel("time step")
    axs[1].set_ylabel("projection amplitude")
    axs[1].legend(fontsize=8)

    # 3) final phase distribution
    x = np.cos(theta_final)
    y = np.sin(theta_final)

    axs[2].scatter(x, y, s=60)

    for i, node in enumerate(nodes):
        axs[2].text(x[i] * 1.05, y[i] * 1.05, node, fontsize=8)

    circle = plt.Circle((0, 0), 1, fill=False)
    axs[2].add_patch(circle)

    axs[2].set_title("Final Phase Distribution")
    axs[2].axis("equal")
    axs[2].set_xlim(-1.2, 1.2)
    axs[2].set_ylim(-1.2, 1.2)

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning Symmetry Graph Mode Dynamics...\n")

    G = build_symmetry_graph()
    eigenvals, eigenvecs, nodes = compute_modes(G)

    print("Nodes:", len(nodes))
    print("Edges:", len(G.edges()))
    print("\nLowest eigenvalues:")
    for i in range(min(6, len(eigenvals))):
        print(i, ":", float(eigenvals[i]))

    theta_series, order_series, nodes = run_kuramoto_trajectory(
        G,
        K=0.12,
        steps=2500,
        dt=0.05,
        omega_std=0.08
    )

    mode_amplitudes = project_onto_modes(
        theta_series,
        eigenvecs,
        num_modes=6
    )

    print("\nFinal synchronization:", float(order_series[-1]))

    plot_mode_dynamics(
        order_series,
        mode_amplitudes,
        eigenvals,
        theta_series[-1],
        nodes
    )
