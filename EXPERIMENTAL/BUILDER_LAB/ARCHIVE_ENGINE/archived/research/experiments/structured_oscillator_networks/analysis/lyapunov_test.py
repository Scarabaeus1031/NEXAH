"""
NEXAH Experiment Tool
Lyapunov Test

Purpose
-------
Estimate whether the three-layer counterrotation system behaves more like

• a stable / periodic system
• a quasi-periodic system
• a weakly chaotic system

Method
------
Run two nearly identical simulations with a tiny perturbation in the initial phase state
and measure how their distance evolves over time.

Outputs
-------
output/lyapunov_distance_vs_time.png
output/lyapunov_log_distance_vs_time.png
output/lyapunov_report.txt

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python lyapunov_test.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def state_distance(theta_a, theta_b):
    d = wrap_angle(theta_a - theta_b)
    return np.sqrt(np.mean(d**2))


# ------------------------------------------------
# Graph builder
# ------------------------------------------------
def build_three_layer_graph(n_inner=16, n_middle=32, n_outer=16):
    G = nx.Graph()

    off_inner = 0
    off_middle = n_inner
    off_outer = n_inner + n_middle

    inner_nodes = list(range(off_inner, off_inner + n_inner))
    middle_nodes = list(range(off_middle, off_middle + n_middle))
    outer_nodes = list(range(off_outer, off_outer + n_outer))

    for layer_nodes in [inner_nodes, middle_nodes, outer_nodes]:
        m = len(layer_nodes)
        for i in range(m):
            G.add_edge(layer_nodes[i], layer_nodes[(i + 1) % m])

    for i, u in enumerate(inner_nodes):
        j = int(round(i * n_middle / n_inner)) % n_middle
        G.add_edge(u, middle_nodes[j])
        G.add_edge(u, middle_nodes[(j - 1) % n_middle])
        G.add_edge(u, middle_nodes[(j + 1) % n_middle])

    for i, u in enumerate(outer_nodes):
        j = int(round(i * n_middle / n_outer)) % n_middle
        G.add_edge(u, middle_nodes[j])
        G.add_edge(u, middle_nodes[(j - 1) % n_middle])
        G.add_edge(u, middle_nodes[(j + 1) % n_middle])

    return G, inner_nodes, middle_nodes, outer_nodes


# ------------------------------------------------
# Dynamics
# ------------------------------------------------
def kuramoto_step(theta, omega, A, K, dt):
    phase_diff = theta[:, None] - theta[None, :]
    coupling = np.sum(A * np.sin(-phase_diff), axis=1)
    dtheta = omega + (K / len(theta)) * coupling
    return theta + dt * dtheta


def build_system(n_inner=16, n_middle=32, n_outer=16, seed=1033):
    np.random.seed(seed)

    G, inner_nodes, middle_nodes, outer_nodes = build_three_layer_graph(
        n_inner=n_inner,
        n_middle=n_middle,
        n_outer=n_outer,
    )

    A = nx.to_numpy_array(G)
    n_total = A.shape[0]

    theta0 = np.random.uniform(0, 2 * np.pi, n_total)

    omega = np.zeros(n_total)
    omega[inner_nodes] = np.random.normal(+0.18, 0.03, len(inner_nodes))
    omega[middle_nodes] = np.random.normal(0.00, 0.02, len(middle_nodes))
    omega[outer_nodes] = np.random.normal(-0.18, 0.03, len(outer_nodes))

    return A, omega, theta0


# ------------------------------------------------
# Lyapunov run
# ------------------------------------------------
def run_perturbed_pair(
    steps=9600,
    dt=0.02,
    K=1.2,
    eps=1e-6,
    seed=1033,
    n_inner=16,
    n_middle=32,
    n_outer=16,
):
    A, omega, theta0 = build_system(
        n_inner=n_inner,
        n_middle=n_middle,
        n_outer=n_outer,
        seed=seed,
    )

    theta_ref = theta0.copy()
    theta_pert = theta0.copy()

    # tiny perturbation on one node
    theta_pert[0] += eps

    distances = np.zeros(steps)

    for t in range(steps):
        theta_ref = kuramoto_step(theta_ref, omega, A, K, dt)
        theta_pert = kuramoto_step(theta_pert, omega, A, K, dt)

        distances[t] = state_distance(theta_ref, theta_pert)

    return distances


# ------------------------------------------------
# Estimate exponent
# ------------------------------------------------
def estimate_lyapunov(distances, dt, fit_start=100, fit_end=2000):
    eps_floor = 1e-16
    y = np.log(np.maximum(distances, eps_floor))

    x = np.arange(len(y)) * dt

    fit_end = min(fit_end, len(y))
    fit_start = min(fit_start, fit_end - 2)

    xs = x[fit_start:fit_end]
    ys = y[fit_start:fit_end]

    coeffs = np.polyfit(xs, ys, 1)
    slope = coeffs[0]

    return slope, x, y, coeffs


# ------------------------------------------------
# Plotting
# ------------------------------------------------
def plot_distance(x, distances):
    plt.figure(figsize=(10, 4))
    plt.plot(x, distances)
    plt.xlabel("time")
    plt.ylabel("distance")
    plt.title("Lyapunov test: state distance vs time")
    plt.savefig("output/lyapunov_distance_vs_time.png", dpi=300)
    plt.show()


def plot_log_distance(x, log_dist, coeffs, fit_start_idx, fit_end_idx):
    plt.figure(figsize=(10, 4))
    plt.plot(x, log_dist, label="log distance")

    xs = x[fit_start_idx:fit_end_idx]
    fit_line = coeffs[0] * xs + coeffs[1]
    plt.plot(xs, fit_line, "--", label="linear fit")

    plt.xlabel("time")
    plt.ylabel("log distance")
    plt.title("Lyapunov test: log distance vs time")
    plt.legend()
    plt.savefig("output/lyapunov_log_distance_vs_time.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Report
# ------------------------------------------------
def write_report(lam, distances, dt, fit_start, fit_end):
    lines = []
    lines.append("Lyapunov Test Report")
    lines.append("--------------------")
    lines.append("")
    lines.append(f"Estimated exponent λ ≈ {lam:.8f}")
    lines.append(f"Initial distance     = {distances[0]:.12e}")
    lines.append(f"Final distance       = {distances[-1]:.12e}")
    lines.append(f"dt                   = {dt}")
    lines.append(f"fit window           = [{fit_start}, {fit_end}) steps")
    lines.append("")

    if lam > 1e-3:
        lines.append("Interpretation: positive exponent -> likely weak chaos.")
    elif lam > -1e-3:
        lines.append("Interpretation: near-zero exponent -> quasi-periodic / marginal behavior.")
    else:
        lines.append("Interpretation: negative exponent -> stable / contracting behavior.")

    with open("output/lyapunov_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():
    Path("output").mkdir(exist_ok=True)

    steps = 9600
    dt = 0.02
    K = 1.2
    eps = 1e-6
    fit_start = 100
    fit_end = 2000

    distances = run_perturbed_pair(
        steps=steps,
        dt=dt,
        K=K,
        eps=eps,
        seed=1033,
        n_inner=16,
        n_middle=32,
        n_outer=16,
    )

    lam, x, log_dist, coeffs = estimate_lyapunov(
        distances,
        dt=dt,
        fit_start=fit_start,
        fit_end=fit_end,
    )

    plot_distance(x, distances)
    plot_log_distance(x, log_dist, coeffs, fit_start, min(fit_end, len(x)))
    write_report(lam, distances, dt, fit_start, fit_end)

    print(f"Estimated Lyapunov exponent λ ≈ {lam:.8f}")
    print("Saved:")
    print("  output/lyapunov_distance_vs_time.png")
    print("  output/lyapunov_log_distance_vs_time.png")
    print("  output/lyapunov_report.txt")


if __name__ == "__main__":
    main()
