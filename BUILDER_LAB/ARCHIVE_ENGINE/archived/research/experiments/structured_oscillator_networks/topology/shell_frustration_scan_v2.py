import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# -----------------------------
# Kuramoto Dynamics
# -----------------------------
def kuramoto_step(theta, omega, A, K, dt):

    phase_diff = theta[:, None] - theta[None, :]
    coupling = np.sum(A * np.sin(-phase_diff), axis=1)

    dtheta = omega + (K / len(theta)) * coupling

    return theta + dt * dtheta


# -----------------------------
# Order Parameter
# -----------------------------
def order_parameter(theta):

    return np.abs(np.sum(np.exp(1j * theta)) / len(theta))


# -----------------------------
# Vortex / defect detection
# -----------------------------
def vortex_density(theta_ring):

    N = len(theta_ring)
    defects = 0

    for i in range(N):

        dphi = theta_ring[(i + 1) % N] - theta_ring[i]
        dphi = np.arctan2(np.sin(dphi), np.cos(dphi))

        if abs(dphi) > np.pi / 2:
            defects += 1

    return defects / N


# -----------------------------
# Graph generator
# -----------------------------
def build_hub_ring(N):

    G = nx.Graph()
    center = 0

    for i in range(1, N + 1):
        G.add_edge(center, i)

    for i in range(1, N + 1):
        G.add_edge(i, 1 + (i % N))

    return G


# -----------------------------
# Single Simulation
# -----------------------------
def run_single_simulation(N, steps=6000, dt=0.02, K=1.0):

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2 * np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    sync_time = None

    for t in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

        R = order_parameter(theta)

        if R > 0.95 and sync_time is None:
            sync_time = t

    if sync_time is None:
        sync_time = steps

    ring_theta = theta[1:]
    vortices = vortex_density(ring_theta)

    return sync_time, vortices


# -----------------------------
# Multi-trial experiment
# -----------------------------
def run_simulation(N, trials=5):

    sync_values = []
    vortex_values = []

    for _ in range(trials):

        s, v = run_single_simulation(N)

        sync_values.append(s)
        vortex_values.append(v)

    return np.mean(sync_values), np.mean(vortex_values)


# -----------------------------
# Shell scan
# -----------------------------
def shell_scan():

    shell_sizes = list(range(8, 120))

    sync_times = []
    vortex_densities = []

    for N in shell_sizes:

        print(f"Running shell size {N}")

        sync, vort = run_simulation(N)

        sync_times.append(sync)
        vortex_densities.append(vort)

    return shell_sizes, sync_times, vortex_densities


# -----------------------------
# Plot results
# -----------------------------
def plot_results(shell_sizes, sync_times, vortex_densities):

    plt.figure()

    plt.plot(shell_sizes, sync_times)

    plt.xlabel("Shell Size N")
    plt.ylabel("Synchronization Time")
    plt.title("Synchronization vs Shell Size")

    plt.savefig("sync_time_vs_shell_v2.png")

    plt.close()

    plt.figure()

    plt.plot(shell_sizes, vortex_densities)

    plt.xlabel("Shell Size N")
    plt.ylabel("Vortex Density")
    plt.title("Vortex Density vs Shell Size")

    plt.savefig("vortex_density_vs_shell_v2.png")

    plt.close()


# -----------------------------
# Main
# -----------------------------
def main():

    shell_sizes, sync_times, vortex_densities = shell_scan()

    plot_results(shell_sizes, sync_times, vortex_densities)

    print("Experiment 01 v2 completed")


if __name__ == "__main__":
    main()
