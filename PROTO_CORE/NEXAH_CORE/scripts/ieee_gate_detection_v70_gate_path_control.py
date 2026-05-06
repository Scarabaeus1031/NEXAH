# ============================================================
# NEXAH — IEEE GATE DETECTION v70
# Gate-Path Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v70_gate_path_control.py
#
# PURPOSE:
# --------
# Use the v68/v69 basin-gate graph for control.
#
# Earlier control:
#   push directly toward target basin
#
# v70 control:
#   compute optimal basin path
#   steer toward the next gate on that path
#
# Example:
#   target transition B0 -> B1
#
# v69 says:
#   shortest path = B0 -> B3 -> B1
#
# Therefore v70 does:
#   Step 1: steer toward gate B0-B3
#   Step 2: steer toward gate B3-B1
#
# CORE IDEA:
# ----------
# Control should not aim at basin centroids.
# Control should aim at low-barrier gates.
#
# OUTPUTS:
# --------
# v70_gate_path_control_B0_to_B1.png
# v70_gate_path_control_deviation_B0_to_B1.png
# v70_gate_path_control_summary_B0_to_B1.txt
#
# ============================================================

import os
import sys
import heapq
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Utils
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


def circular_delta(a, b):
    return wrap_theta(a - b)


def unit_vector_to_target(s, target):
    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

    u = np.array([dr, dtheta])
    n = np.linalg.norm(u)

    if n > 1e-9:
        u = u / n

    return u


# ------------------------------------------------------------
# Build base data
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    return states


# ------------------------------------------------------------
# Potential grid
# ------------------------------------------------------------

def build_potential_grid(states, nr=140, nt=180):

    r_min = max(0.0, np.min(states[:, 0]) - 0.1)
    r_max = np.max(states[:, 0]) + 0.1

    theta_min = -np.pi
    theta_max = np.pi

    r_grid = np.linspace(r_min, r_max, nr)
    theta_grid = np.linspace(theta_min, theta_max, nt)

    R, T = np.meshgrid(r_grid, theta_grid, indexing="ij")

    data = np.vstack([states[:, 0], states[:, 1]])
    kde = gaussian_kde(data)

    points = np.vstack([R.ravel(), T.ravel()])
    rho = kde(points).reshape(R.shape)

    V = -np.log(rho + 1e-9)

    V = V - np.nanmin(V)
    if np.nanmax(V) > 1e-12:
        V = V / np.nanmax(V)

    return r_grid, theta_grid, R, T, rho, V


# ------------------------------------------------------------
# v68 fixed basin/gate data from last run
# ------------------------------------------------------------

def load_v68_graph():

    basins = {
        0: np.array([0.8715, 0.6494]),
        1: np.array([0.9310, -2.3343]),
        2: np.array([1.8223, 2.6151]),
        3: np.array([1.6242, -1.3514]),
        4: np.array([1.7431, 0.5090]),
    }

    gates = {
        (0, 1): {"pos": np.array([0.8913, -0.6143]), "barrier": 0.0482},
        (2, 3): {"pos": np.array([1.6638, -0.3686]), "barrier": 0.0401},
        (1, 2): {"pos": np.array([1.4460, 0.5090]), "barrier": 0.0341},
        (3, 4): {"pos": np.array([1.6836, -0.3686]), "barrier": 0.0253},
        (1, 4): {"pos": np.array([1.5648, -0.1229]), "barrier": 0.0191},
        (2, 4): {"pos": np.array([1.7629, 1.2461]), "barrier": 0.0190},
        (0, 2): {"pos": np.array([1.4856, 1.9481]), "barrier": 0.0171},
        (0, 3): {"pos": np.array([1.1488, -0.1580]), "barrier": 0.0150},
        (0, 4): {"pos": np.array([1.5252, 0.5090]), "barrier": 0.0104},
        (1, 3): {"pos": np.array([1.4856, -1.5620]), "barrier": 0.0017},
    }

    # symmetric access
    full_gates = {}
    for (a, b), g in gates.items():
        full_gates[(a, b)] = g
        full_gates[(b, a)] = g

    graph = {}
    for (a, b), g in gates.items():
        graph.setdefault(a, []).append((b, g["barrier"]))
        graph.setdefault(b, []).append((a, g["barrier"]))

    return basins, full_gates, graph


# ------------------------------------------------------------
# Shortest path
# ------------------------------------------------------------

def shortest_path(graph, start, end):

    q = [(0.0, start, [])]
    seen = set()

    while q:
        cost, node, path = heapq.heappop(q)

        if node in seen:
            continue

        seen.add(node)
        path = path + [node]

        if node == end:
            return cost, path

        for nb, w in graph.get(node, []):
            heapq.heappush(q, (cost + w, nb, path))

    return np.inf, []


# ------------------------------------------------------------
# Learned local flow
# ------------------------------------------------------------

def learn_local_flow(states, k=25):

    velocities = np.gradient(states, axis=0)

    def flow(s):

        dr = states[:, 0] - s[0]
        dtheta = np.array([wrap_theta(p[1] - s[1]) for p in states])

        dists = np.sqrt(dr**2 + dtheta**2)
        idx = np.argsort(dists)[:k]

        return np.mean(velocities[idx], axis=0)

    return flow


# ------------------------------------------------------------
# Stability field
# ------------------------------------------------------------

def build_stability_field(states):

    data = np.vstack([states[:, 0], states[:, 1]])
    kde = gaussian_kde(data)

    def density(s):
        return kde(np.array([[s[0]], [s[1]]]))[0]

    def potential(s):
        return -np.log(density(s) + 1e-8)

    def gradV(s, eps=1e-3):
        er = np.array([eps, 0.0])
        et = np.array([0.0, eps])

        dVr = (potential(s + er) - potential(s - er)) / (2 * eps)
        dVt = (potential(s + et) - potential(s - et)) / (2 * eps)

        return np.array([dVr, dVt])

    return potential, gradV


# ------------------------------------------------------------
# Gate path control simulation
# ------------------------------------------------------------

def simulate_gate_path_control(
    s0,
    local_flow,
    gradV,
    basins,
    gates,
    path,
    steps=360,
    dt=0.06,
    local_gain=1.0,
    stability_gain=0.18,
    gate_gain=0.16,
    gate_radius=0.16
):

    traj = [s0.copy()]
    active_gate_positions = []

    s = s0.copy()

    # path edges: [0,3,1] -> [(0,3),(3,1)]
    edges = list(zip(path[:-1], path[1:]))
    current_edge_index = 0

    for step in range(steps):

        v = local_gain * local_flow(s)
        v += -stability_gain * gradV(s)

        if current_edge_index < len(edges):

            edge = edges[current_edge_index]
            gate_pos = gates[edge]["pos"]

            u_gate = unit_vector_to_target(s, gate_pos)
            v += gate_gain * u_gate

            dist_to_gate = np.linalg.norm([
                s[0] - gate_pos[0],
                wrap_theta(s[1] - gate_pos[1])
            ])

            active_gate_positions.append(gate_pos.copy())

            if dist_to_gate < gate_radius:
                current_edge_index += 1

        s = s + dt * v
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())

    return np.array(traj), np.array(active_gate_positions), current_edge_index


def simulate_baseline(
    s0,
    local_flow,
    gradV,
    steps=360,
    dt=0.06,
    local_gain=1.0,
    stability_gain=0.18
):

    traj = [s0.copy()]
    s = s0.copy()

    for _ in range(steps):
        v = local_gain * local_flow(s)
        v += -stability_gain * gradV(s)

        s = s + dt * v
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())

    return np.array(traj)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states = build_pipeline()

    basins, gates, graph = load_v68_graph()

    source = 0
    target = 1

    cost, path = shortest_path(graph, source, target)

    local_flow = learn_local_flow(states, k=25)
    _, gradV = build_stability_field(states)

    s0 = basins[source].copy()

    baseline = simulate_baseline(
        s0,
        local_flow,
        gradV,
        steps=360
    )

    controlled, gate_targets, reached_edges = simulate_gate_path_control(
        s0,
        local_flow,
        gradV,
        basins,
        gates,
        path,
        steps=360
    )

    deviation = np.linalg.norm(controlled - baseline, axis=1)

    final_dist_to_target = np.linalg.norm([
        controlled[-1, 0] - basins[target][0],
        wrap_theta(controlled[-1, 1] - basins[target][1])
    ])

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(9, 8))

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=2,
        alpha=0.08,
        label="state field"
    )

    plt.plot(
        baseline[:, 1],
        baseline[:, 0],
        linewidth=2,
        label="baseline"
    )

    plt.plot(
        controlled[:, 1],
        controlled[:, 0],
        linewidth=2,
        label="gate-path controlled"
    )

    # basins
    for bid, b in basins.items():
        plt.scatter(
            b[1],
            b[0],
            s=80,
            marker="o",
            edgecolor="black",
            label=f"B{bid}" if bid in [source, target] else None
        )
        plt.text(b[1], b[0], f"B{bid}", fontsize=9)

    # gates on selected path
    for e in zip(path[:-1], path[1:]):
        g = gates[e]["pos"]
        plt.scatter(
            g[1],
            g[0],
            s=120,
            marker="x",
            color="red",
            label=f"gate {e[0]}->{e[1]}"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(
        f"NEXAH v70 — Gate-Path Control B{source}->B{target}\n"
        f"path={path}, cost={cost:.4f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v70_gate_path_control_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Deviation plot
    # --------------------------------------------------------

    plt.figure(figsize=(9, 4))

    plt.plot(deviation, linewidth=1.5)
    plt.xlabel("simulation step")
    plt.ylabel("controlled - baseline deviation")
    plt.title("NEXAH v70 — Gate-Path Control Deviation")
    plt.tight_layout()

    dev_path = os.path.join(
        OUT_DIR,
        f"v70_gate_path_control_deviation_B{source}_to_B{target}.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v70_gate_path_control_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v70 — Gate-Path Control\n")
        f.write("=============================\n\n")

        f.write(f"Source basin: B{source}\n")
        f.write(f"Target basin: B{target}\n")
        f.write(f"Shortest path: {path}\n")
        f.write(f"Path cost: {cost:.4f}\n")
        f.write(f"Reached path edges: {reached_edges}/{len(path)-1}\n\n")

        f.write("Path gates:\n")
        for e in zip(path[:-1], path[1:]):
            g = gates[e]
            f.write(
                f"  B{e[0]} -> B{e[1]}: "
                f"gate_r={g['pos'][0]:.4f}, "
                f"gate_theta={g['pos'][1]:.4f}, "
                f"barrier={g['barrier']:.4f}\n"
            )

        f.write("\nDeviation:\n")
        f.write(f"  final deviation: {deviation[-1]:.6f}\n")
        f.write(f"  max deviation:   {np.max(deviation):.6f}\n")
        f.write(f"  mean deviation:  {np.mean(deviation):.6f}\n\n")

        f.write(f"Final distance to target basin B{target}: {final_dist_to_target:.6f}\n")

    print("NEXAH v70 complete")
    print(f"Path: {path}")
    print(f"Path cost: {cost:.4f}")
    print(f"Reached edges: {reached_edges}/{len(path)-1}")
    print(f"Final distance to target B{target}: {final_dist_to_target:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {dev_path}")
    print(f"Saved: {summary_path}")
