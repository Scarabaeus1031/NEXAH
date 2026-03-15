"""
NEXAH Experiment Tool
Three-Layer Counterrotation Long Run

Purpose
-------
Run a long-duration Kuramoto-style experiment on three coupled ring layers.

Model
-----
We use three shells:

    inner  -> positive drift
    middle -> near-neutral interface layer
    outer  -> negative drift

This creates a simple counter-rotation architecture with a transition zone
between the two opposite shells.

Goals
-----
Measure whether three-layer counterrotation produces:

• longer-lived defect structures
• stronger braid-like phase slips
• shell-specific synchronization patterns
• interface-layer turbulence / mediation

Outputs
-------
output/three_layer_global_order.png
output/three_layer_layer_orders.png
output/three_layer_defect_maps.png
output/three_layer_snapshot.png
output/three_layer_summary.txt

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python three_layer_counterrotation_longrun.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))


def phase_diff_ring(theta_ring):
    diffs = np.roll(theta_ring, -1) - theta_ring
    return wrap_angle(diffs)


def detect_defects(theta_ring, threshold=2.2):
    diffs = phase_diff_ring(theta_ring)
    idx = np.where(np.abs(diffs) > threshold)[0]
    return idx, diffs


# ------------------------------------------------
# Graph builder
# ------------------------------------------------
def build_three_layer_graph(n_inner=16, n_middle=32, n_outer=16):
    """
    Node layout:
        0 .. n_inner-1                      inner
        n_inner .. n_inner+n_middle-1      middle
        ...                                outer
    """

    G = nx.Graph()

    off_inner = 0
    off_middle = n_inner
    off_outer = n_inner + n_middle

    inner_nodes = list(range(off_inner, off_inner + n_inner))
    middle_nodes = list(range(off_middle, off_middle + n_middle))
    outer_nodes = list(range(off_outer, off_outer + n_outer))

    # ring edges inside each shell
    for layer_nodes in [inner_nodes, middle_nodes, outer_nodes]:
        m = len(layer_nodes)
        for i in range(m):
            G.add_edge(layer_nodes[i], layer_nodes[(i + 1) % m])

    # nearest-style inter-layer coupling by angular correspondence
    # inner <-> middle
    for i, u in enumerate(inner_nodes):
        j = int(round(i * n_middle / n_inner)) % n_middle
        G.add_edge(u, middle_nodes[j])
        G.add_edge(u, middle_nodes[(j - 1) % n_middle])
        G.add_edge(u, middle_nodes[(j + 1) % n_middle])

    # middle <-> outer
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


def simulate_three_layer(
    n_inner=16,
    n_middle=32,
    n_outer=16,
    steps=9600,
    dt=0.02,
    K=1.2,
    seed=1033,
):
    np.random.seed(seed)

    G, inner_nodes, middle_nodes, outer_nodes = build_three_layer_graph(
        n_inner=n_inner,
        n_middle=n_middle,
        n_outer=n_outer,
    )

    A = nx.to_numpy_array(G)
    n_total = A.shape[0]

    theta = np.random.uniform(0, 2 * np.pi, n_total)

    # counterrotation frequencies:
    # inner = positive drift
    # middle = near-neutral
    # outer = negative drift
    omega = np.zeros(n_total)

    omega[inner_nodes] = np.random.normal(loc=+0.18, scale=0.03, size=len(inner_nodes))
    omega[middle_nodes] = np.random.normal(loc=0.00, scale=0.02, size=len(middle_nodes))
    omega[outer_nodes] = np.random.normal(loc=-0.18, scale=0.03, size=len(outer_nodes))

    history = np.zeros((steps, n_total), dtype=float)

    global_R = np.zeros(steps, dtype=float)
    inner_R = np.zeros(steps, dtype=float)
    middle_R = np.zeros(steps, dtype=float)
    outer_R = np.zeros(steps, dtype=float)

    defect_inner = np.zeros((steps, len(inner_nodes)), dtype=float)
    defect_middle = np.zeros((steps, len(middle_nodes)), dtype=float)
    defect_outer = np.zeros((steps, len(outer_nodes)), dtype=float)

    for t in range(steps):
        theta = kuramoto_step(theta, omega, A, K, dt)
        history[t] = theta

        theta_inner = theta[inner_nodes]
        theta_middle = theta[middle_nodes]
        theta_outer = theta[outer_nodes]

        global_R[t] = order_parameter(theta)
        inner_R[t] = order_parameter(theta_inner)
        middle_R[t] = order_parameter(theta_middle)
        outer_R[t] = order_parameter(theta_outer)

        idx_i, _ = detect_defects(theta_inner)
        idx_m, _ = detect_defects(theta_middle)
        idx_o, _ = detect_defects(theta_outer)

        defect_inner[t, idx_i] = 1.0
        defect_middle[t, idx_m] = 1.0
        defect_outer[t, idx_o] = 1.0

    return {
        "history": history,
        "global_R": global_R,
        "inner_R": inner_R,
        "middle_R": middle_R,
        "outer_R": outer_R,
        "defect_inner": defect_inner,
        "defect_middle": defect_middle,
        "defect_outer": defect_outer,
        "inner_nodes": inner_nodes,
        "middle_nodes": middle_nodes,
        "outer_nodes": outer_nodes,
        "params": {
            "n_inner": n_inner,
            "n_middle": n_middle,
            "n_outer": n_outer,
            "steps": steps,
            "dt": dt,
            "K": K,
            "seed": seed,
        },
    }


# ------------------------------------------------
# Plotting
# ------------------------------------------------
def plot_global_order(global_R):
    plt.figure(figsize=(10, 4))
    plt.plot(global_R)
    plt.xlabel("time step")
    plt.ylabel("R")
    plt.title("Three-layer global synchronization")
    plt.savefig("output/three_layer_global_order.png", dpi=300)
    plt.show()


def plot_layer_orders(inner_R, middle_R, outer_R):
    plt.figure(figsize=(10, 4))
    plt.plot(inner_R, label="inner")
    plt.plot(middle_R, label="middle")
    plt.plot(outer_R, label="outer")
    plt.xlabel("time step")
    plt.ylabel("R")
    plt.title("Three-layer shell order parameters")
    plt.legend()
    plt.savefig("output/three_layer_layer_orders.png", dpi=300)
    plt.show()


def plot_defect_maps(defect_inner, defect_middle, defect_outer):
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    axes[0].imshow(defect_inner.T, aspect="auto", origin="lower", cmap="inferno")
    axes[0].set_ylabel("inner index")
    axes[0].set_title("Inner shell defects")

    axes[1].imshow(defect_middle.T, aspect="auto", origin="lower", cmap="inferno")
    axes[1].set_ylabel("middle index")
    axes[1].set_title("Middle shell defects")

    axes[2].imshow(defect_outer.T, aspect="auto", origin="lower", cmap="inferno")
    axes[2].set_ylabel("outer index")
    axes[2].set_xlabel("time step")
    axes[2].set_title("Outer shell defects")

    plt.tight_layout()
    plt.savefig("output/three_layer_defect_maps.png", dpi=300)
    plt.show()


def ring_coords(n, radius):
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return radius * np.cos(ang), radius * np.sin(ang)


def plot_snapshot(history, inner_nodes, middle_nodes, outer_nodes, t_index=None):
    if t_index is None:
        t_index = history.shape[0] - 1

    theta = history[t_index]
    theta_inner = theta[inner_nodes]
    theta_middle = theta[middle_nodes]
    theta_outer = theta[outer_nodes]

    xi, yi = ring_coords(len(inner_nodes), 0.7)
    xm, ym = ring_coords(len(middle_nodes), 1.1)
    xo, yo = ring_coords(len(outer_nodes), 1.5)

    plt.figure(figsize=(8, 8))
    plt.scatter(xi, yi, c=theta_inner, cmap="hsv", s=120, label="inner")
    plt.scatter(xm, ym, c=theta_middle, cmap="hsv", s=90, label="middle")
    plt.scatter(xo, yo, c=theta_outer, cmap="hsv", s=120, label="outer")

    # outline circles
    for r in [0.7, 1.1, 1.5]:
        circ = plt.Circle((0, 0), r, fill=False, color="black", alpha=0.3)
        plt.gca().add_patch(circ)

    plt.title(f"Three-layer phase snapshot t={t_index}")
    plt.axis("equal")
    plt.axis("off")
    plt.savefig("output/three_layer_snapshot.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Summary
# ------------------------------------------------
# Save defect arrays for further analysis
import numpy as np

np.save("output/inner_shell_defects.npy", results["defect_inner"])
np.save("output/middle_shell_defects.npy", results["defect_middle"])
np.save("output/outer_shell_defects.npy", results["defect_outer"])

plot_snapshot(
    results["history"],
    results["inner_nodes"],
    results["middle_nodes"],
    results["outer_nodes"],
    t_index=results["params"]["steps"] - 1,
)

# Save phase history for vortex analysis
np.save("output/phase_history.npy", results["history"])

print("Saved defect arrays and phase history.")

def save_summary(results):
    params = results["params"]

    global_R = results["global_R"]
    inner_R = results["inner_R"]
    middle_R = results["middle_R"]
    outer_R = results["outer_R"]

    defect_inner = results["defect_inner"]
    defect_middle = results["defect_middle"]
    defect_outer = results["defect_outer"]

    text = []
    text.append("Three-Layer Counterrotation Long Run")
    text.append("-----------------------------------")
    text.append("")
    text.append(f"n_inner  = {params['n_inner']}")
    text.append(f"n_middle = {params['n_middle']}")
    text.append(f"n_outer  = {params['n_outer']}")
    text.append(f"steps    = {params['steps']}")
    text.append(f"dt       = {params['dt']}")
    text.append(f"K        = {params['K']}")
    text.append(f"seed     = {params['seed']}")
    text.append("")
    text.append(f"Final global R  = {global_R[-1]:.6f}")
    text.append(f"Final inner R   = {inner_R[-1]:.6f}")
    text.append(f"Final middle R  = {middle_R[-1]:.6f}")
    text.append(f"Final outer R   = {outer_R[-1]:.6f}")
    text.append("")
    text.append(f"Mean defect density inner  = {defect_inner.mean():.6f}")
    text.append(f"Mean defect density middle = {defect_middle.mean():.6f}")
    text.append(f"Mean defect density outer  = {defect_outer.mean():.6f}")
    text.append("")

    with open("output/three_layer_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(text))


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():
    Path("output").mkdir(exist_ok=True)

    results = simulate_three_layer(
        n_inner=16,
        n_middle=32,
        n_outer=16,
        steps=9600,
        dt=0.02,
        K=1.2,
        seed=1033,
    )

    plot_global_order(results["global_R"])
    plot_layer_orders(results["inner_R"], results["middle_R"], results["outer_R"])
    plot_defect_maps(
        results["defect_inner"],
        results["defect_middle"],
        results["defect_outer"],
    )

    plot_snapshot(
        results["history"],
        results["inner_nodes"],
        results["middle_nodes"],
        results["outer_nodes"],
        t_index=results["params"]["steps"] - 1,
    )

    # 🔵 HIER EINFÜGEN
    np.save("output/inner_shell_defects.npy", results["defect_inner"])
    np.save("output/middle_shell_defects.npy", results["defect_middle"])
    np.save("output/outer_shell_defects.npy", results["defect_outer"])
    np.save("output/phase_history.npy", results["history"])

    print("Saved defect arrays and phase history.")

    save_summary(results)

    print("Three-layer counterrotation long run completed.")
