# ============================================================
# NEXAH — IEEE GATE DETECTION v71
# Barrier-Aware Gate Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v71_barrier_aware_gate_control.py
#
# PURPOSE:
# --------
# Upgrade v70 gate-path control.
#
# v70:
#   steer toward gate position
#
# Problem:
#   system remains trapped in stability basin
#
# v71:
#   use barrier-aware control:
#
#       control strength depends on
#       ΔV = V_gate - V_current
#
# CORE IDEA:
# ----------
# Gates are not targets.
# Gates are barrier crossings.
#
# Control must inject enough directional energy to cross the
# local potential barrier.
#
# OUTPUTS:
# --------
# v71_barrier_aware_gate_control_B0_to_B1.png
# v71_barrier_aware_gate_control_deviation_B0_to_B1.png
# v71_barrier_aware_gate_control_summary_B0_to_B1.txt
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


def state_distance(a, b):
    return np.linalg.norm([
        a[0] - b[0],
        wrap_theta(a[1] - b[1])
    ])


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
# Fixed v68/v69 graph data
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

    full_gates = {}
    graph = {}

    for (a, b), g in gates.items():
        full_gates[(a, b)] = g
        full_gates[(b, a)] = g

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
# Stability potential
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
# Nearest basin assignment
# ------------------------------------------------------------

def assign_nearest_basin(s, basins):

    best_id = None
    best_dist = np.inf

    for bid, b in basins.items():
        d = state_distance(s, b)

        if d < best_dist:
            best_dist = d
            best_id = bid

    return best_id, best_dist


# ------------------------------------------------------------
# Baseline simulation
# ------------------------------------------------------------

def simulate_baseline(
    s0,
    local_flow,
    gradV,
    steps=420,
    dt=0.06,
    local_gain=1.0,
    stability_gain=0.16
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
# Barrier-aware gate path control
# ------------------------------------------------------------

def simulate_barrier_aware_control(
    s0,
    local_flow,
    potential,
    gradV,
    basins,
    gates,
    path,
    steps=420,
    dt=0.06,
    local_gain=1.0,
    stability_gain=0.14,
    base_gate_gain=0.22,
    barrier_gain=2.8,
    max_gate_gain=0.95,
    gate_radius=0.18,
    basin_radius=0.22
):

    traj = [s0.copy()]
    boost_history = []
    edge_history = []
    basin_history = []

    s = s0.copy()

    edges = list(zip(path[:-1], path[1:]))
    current_edge_index = 0
    reached_edges = 0

    for step in range(steps):

        current_basin, basin_dist = assign_nearest_basin(s, basins)
        basin_history.append(current_basin)

        v = local_gain * local_flow(s)
        v += -stability_gain * gradV(s)

        boost = 0.0
        active_edge = None

        if current_edge_index < len(edges):

            active_edge = edges[current_edge_index]
            gate = gates[active_edge]
            gate_pos = gate["pos"]

            V_current = potential(s)
            V_gate = potential(gate_pos)

            barrier_delta = max(0.0, V_gate - V_current)

            # barrier-aware boost
            boost = base_gate_gain + barrier_gain * barrier_delta
            boost = min(boost, max_gate_gain)

            u_gate = unit_vector_to_target(s, gate_pos)

            # inject directional energy toward barrier crossing
            v += boost * u_gate

            dist_to_gate = state_distance(s, gate_pos)

            # edge is counted reached when the simulated state comes near the gate
            if dist_to_gate < gate_radius:
                current_edge_index += 1
                reached_edges = current_edge_index

        s = s + dt * v
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())
        boost_history.append(boost)
        edge_history.append(active_edge)

        # optional early stop if target basin reached
        target_basin = path[-1]
        if state_distance(s, basins[target_basin]) < basin_radius:
            break

    return (
        np.array(traj),
        reached_edges,
        boost_history,
        edge_history,
        basin_history
    )


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
    potential, gradV = build_stability_field(states)

    s0 = basins[source].copy()

    baseline = simulate_baseline(
        s0,
        local_flow,
        gradV
    )

    controlled, reached_edges, boost_history, edge_history, basin_history = (
        simulate_barrier_aware_control(
            s0,
            local_flow,
            potential,
            gradV,
            basins,
            gates,
            path
        )
    )

    n = min(len(controlled), len(baseline))
    deviation = np.linalg.norm(controlled[:n] - baseline[:n], axis=1)

    final_dist_to_target = state_distance(controlled[-1], basins[target])
    final_basin, final_basin_dist = assign_nearest_basin(controlled[-1], basins)

    tag = f"B{source}_to_B{target}"

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
        label="barrier-aware control"
    )

    for bid, b in basins.items():
        plt.scatter(
            b[1],
            b[0],
            s=80,
            marker="o",
            edgecolor="black"
        )
        plt.text(b[1], b[0], f"B{bid}", fontsize=9)

    for e in zip(path[:-1], path[1:]):
        g = gates[e]["pos"]
        plt.scatter(
            g[1],
            g[0],
            s=130,
            marker="x",
            color="red"
        )
        plt.text(g[1], g[0], f"G{e[0]}->{e[1]}", fontsize=8, color="red")

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(
        f"NEXAH v71 — Barrier-Aware Gate Control {tag}\n"
        f"path={path}, cost={cost:.4f}, reached={reached_edges}/{len(path)-1}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v71_barrier_aware_gate_control_{tag}.png"
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
    plt.title("NEXAH v71 — Barrier-Aware Control Deviation")
    plt.tight_layout()

    dev_path = os.path.join(
        OUT_DIR,
        f"v71_barrier_aware_gate_control_deviation_{tag}.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Boost plot
    # --------------------------------------------------------

    plt.figure(figsize=(9, 4))

    plt.plot(boost_history, linewidth=1.5)
    plt.xlabel("simulation step")
    plt.ylabel("gate boost")
    plt.title("NEXAH v71 — Barrier-Aware Gate Boost")
    plt.tight_layout()

    boost_path = os.path.join(
        OUT_DIR,
        f"v71_barrier_aware_gate_boost_{tag}.png"
    )

    plt.savefig(boost_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v71_barrier_aware_gate_control_summary_{tag}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v71 — Barrier-Aware Gate Control\n")
        f.write("======================================\n\n")

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

        f.write("\nFinal state:\n")
        f.write(f"  final r: {controlled[-1, 0]:.6f}\n")
        f.write(f"  final theta: {controlled[-1, 1]:.6f}\n")
        f.write(f"  nearest basin: B{final_basin}\n")
        f.write(f"  nearest basin distance: {final_basin_dist:.6f}\n")
        f.write(f"  distance to target B{target}: {final_dist_to_target:.6f}\n\n")

        f.write("Deviation:\n")
        f.write(f"  final deviation: {deviation[-1]:.6f}\n")
        f.write(f"  max deviation:   {np.max(deviation):.6f}\n")
        f.write(f"  mean deviation:  {np.mean(deviation):.6f}\n\n")

        if len(boost_history) > 0:
            f.write("Boost:\n")
            f.write(f"  max boost:  {np.max(boost_history):.6f}\n")
            f.write(f"  mean boost: {np.mean(boost_history):.6f}\n")

    print("NEXAH v71 complete")
    print(f"Path: {path}")
    print(f"Path cost: {cost:.4f}")
    print(f"Reached edges: {reached_edges}/{len(path)-1}")
    print(f"Final nearest basin: B{final_basin}")
    print(f"Final distance to target B{target}: {final_dist_to_target:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {dev_path}")
    print(f"Saved: {boost_path}")
    print(f"Saved: {summary_path}")
