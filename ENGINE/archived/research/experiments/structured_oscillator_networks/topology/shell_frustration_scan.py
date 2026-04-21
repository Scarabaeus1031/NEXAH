"""
NEXAH Experiment 01
Shell Frustration Scan

Investigates how shell size N influences synchronization time
and vortex density in hub–ring oscillator networks.

Output:
- sync_time_vs_shell.png
- vortex_density_vs_shell.png
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------
# Kuramoto Simulation
# ----------------------------

def kuramoto_step(theta, omega, A, K, dt):

    N = len(theta)
    dtheta = np.zeros(N)

    for i in range(N):

        coupling = 0.0

        for j in range(N):
            if A[i, j] > 0:
                coupling += np.sin(theta[j] - theta[i])

        dtheta[i] = omega[i] + (K / N) * coupling

    theta = theta + dt * dtheta

    return theta


# ----------------------------
# Order Parameter
# ----------------------------

def order_parameter(theta):

    return np.abs(np.mean(np.exp(1j * theta)))


# ----------------------------
# Vortex Detection
# ----------------------------

def vortex_count(theta_ring):

    """
    Detect phase winding along ring.
    """

    N = len(theta_ring)

    winding = 0.0

    for i in range(N):

        dphi = theta_ring[(i + 1) % N] - theta_ring[i]

        dphi = np.arctan2(np.sin(dphi), np.cos(dphi))

        winding += dphi

    winding_number = winding / (2 * np.pi)

    return abs(winding_number)


# ----------------------------
# Build Hub-Ring Graph
# ----------------------------

def build_hub_ring(N):

    """
    1 center node
    N ring nodes
    """

    G = nx.Graph()

    center = 0

    for i in range(1, N + 1):
        G.add_edge(center, i)

    for i in range(1, N + 1):
        G.add_edge(i, 1 + (i % N))

    return G


# ----------------------------
# Run Simulation
# ----------------------------

def run_simulation(N, K=1.0, steps=4000, dt=0.01):

    G = build_hub_ring(N)

    A = nx.to_numpy_array(G)

    num_nodes = len(A)

    omega = np.random.normal(0, 0.1, num_nodes)

    theta = np.random.uniform(0, 2*np.pi, num_nodes)

    sync_time = None

    for t in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

        R = order_parameter(theta)

        if R > 0.95 and sync_time is None:
            sync_time = t

    if sync_time is None:
        sync_time = steps

    ring_phases = theta[1:]  # exclude center

    vortices = vortex_count(ring_phases)

    return sync_time, vortices


# ----------------------------
# Shell Scan
# ----------------------------

def shell_scan():

    shell_sizes = list(range(8, 120))

    sync_times = []
    vortex_densities = []

    for N in shell_sizes:

        print(f"Running shell size {N}")

        sync_time, vortices = run_simulation(N)

        sync_times.append(sync_time)

        vortex_densities.append(vortices)

    return shell_sizes, sync_times, vortex_densities


# ----------------------------
# Plot Results
# ----------------------------

def plot_results(shell_sizes, sync_times, vortex_densities):

    plt.figure()

    plt.plot(shell_sizes, sync_times)

    plt.xlabel("Shell Size N")
    plt.ylabel("Synchronization Time")

    plt.title("Synchronization vs Shell Size")

    plt.savefig("sync_time_vs_shell.png")

    plt.close()

    plt.figure()

    plt.plot(shell_sizes, vortex_densities)

    plt.xlabel("Shell Size N")
    plt.ylabel("Vortex Density")

    plt.title("Vortex Density vs Shell Size")

    plt.savefig("vortex_density_vs_shell.png")

    plt.close()


# ----------------------------
# Main
# ----------------------------

def main():

    shell_sizes, sync_times, vortex_densities = shell_scan()

    plot_results(shell_sizes, sync_times, vortex_densities)

    print("Experiment completed.")


if __name__ == "__main__":
    main()
