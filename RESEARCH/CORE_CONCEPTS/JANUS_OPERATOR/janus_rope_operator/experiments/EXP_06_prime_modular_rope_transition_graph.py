# ============================================================
# EXP_06 — PRIME MODULAR ROPE TRANSITION GRAPH
# JANUS Rope Operator
#
# Goal:
# Combine rope dynamics + splinter gates + prime residue graphs.
#
# Tests:
# - map rope phase into prime-modular states
# - extract transition matrix
# - separate cycle-core vs residual drift
# - detect dominant residue cycle
# - compare mod 17 / 19 / 23 / 31
#
# Output:
# outputs/EXP_06/
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

OUTPUT_DIR = Path(
    "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/"
    "symbolic_layer/janus_rope_operator/outputs/EXP_06"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

N = 30000
t = np.linspace(0, 260 * np.pi, N)

mods = [17, 19, 23, 31]

phi = (1 + np.sqrt(5)) / 2
root2 = np.sqrt(2)
pi = np.pi

pole = np.array([1.0, 0.0])

# ------------------------------------------------------------
# ROPE FIELD
# ------------------------------------------------------------

r1 = np.sin(2 * t / phi)
r2 = np.cos(3 * t / pi)
r3 = np.sin(5 * t / root2)
r4 = np.cos(7 * t / phi)

root_thread = (
    0.40 * np.sin(t / phi)
    + 0.35 * np.cos(t / root2)
    + 0.25 * np.sin(t / pi)
)

x = (
    0.48 * r1
    + 0.34 * r2
    + 0.16 * np.sin(11 * t / pi)
    + 0.12 * root_thread
)

y = (
    -0.36
    + 0.36 * r3
    + 0.28 * r4
    + 0.14 * np.cos(13 * t / root2)
)

# asymmetric bola compression
x *= 0.92 + 0.10 * np.sin(t / 180)
y *= 0.90 + 0.12 * np.cos(t / 210)

# ------------------------------------------------------------
# ANGLE AROUND OFFSET POLE
# ------------------------------------------------------------

dx = x - pole[0]
dy = y - pole[1]

theta = np.arctan2(dy, dx)
theta_unwrapped = np.unwrap(theta)
angle_deg = (np.degrees(theta) + 360) % 360

angular_velocity = np.abs(np.gradient(theta_unwrapped))
angular_velocity = gaussian_filter1d(angular_velocity, sigma=3)

# ------------------------------------------------------------
# SPLINTER SCORE
# ------------------------------------------------------------

bins = np.linspace(0, 360, 721)
hist, edges = np.histogram(angle_deg, bins=bins, density=True)
hist_smooth = gaussian_filter1d(hist, sigma=4)
centers = 0.5 * (edges[:-1] + edges[1:])

sector_idx = np.digitize(angle_deg, bins) - 1
sector_idx = np.clip(sector_idx, 0, len(hist_smooth) - 1)

local_density = hist_smooth[sector_idx]
splinter_score = angular_velocity * (1.0 - local_density / (local_density.max() + 1e-9))

splinter_threshold = np.percentile(splinter_score, 94)
splinter_mask = splinter_score >= splinter_threshold

# ------------------------------------------------------------
# PRIME MODULAR TRANSITION EXTRACTION
# ------------------------------------------------------------

results = {}

for mod in mods:
    state = np.floor(angle_deg / (360 / mod)).astype(int) % mod

    T = np.zeros((mod, mod))

    for a, b in zip(state[:-1], state[1:]):
        T[a, b] += 1

    row_sum = T.sum(axis=1, keepdims=True)
    P = np.divide(T, row_sum, out=np.zeros_like(T), where=row_sum > 0)

    # cycle component = strongest outgoing edge per node
    C = np.zeros_like(P)

    for i in range(mod):
        if P[i].sum() > 0:
            j = np.argmax(P[i])
            C[i, j] = P[i, j]

    R = np.maximum(P - C, 0)

    # graph
    G = nx.DiGraph()

    for i in range(mod):
        G.add_node(i)

    for i in range(mod):
        for j in range(mod):
            if P[i, j] > 0.01:
                G.add_edge(i, j, weight=P[i, j])

    # find dominant cycle
    cycles = list(nx.simple_cycles(G))

    best_cycle = []
    best_weight = 0.0

    for cyc in cycles:
        if len(cyc) < 3:
            continue

        w = 0.0
        valid = True

        for k in range(len(cyc)):
            a = cyc[k]
            b = cyc[(k + 1) % len(cyc)]
            if P[a, b] <= 0:
                valid = False
                break
            w += P[a, b]

        if valid:
            w = w / len(cyc)

            if w > best_weight:
                best_weight = w
                best_cycle = cyc

    results[mod] = {
        "state": state,
        "T": T,
        "P": P,
        "C": C,
        "R": R,
        "G": G,
        "cycle": best_cycle,
        "cycle_weight": best_weight,
    }

# ------------------------------------------------------------
# VISUAL 1 — ROPE FIELD WITH MODULAR STATES
# ------------------------------------------------------------

mod_show = 23
state = results[mod_show]["state"]

plt.figure(figsize=(10, 10))
plt.scatter(x, y, c=state, cmap="tab20", s=2, alpha=0.75)
plt.scatter(x[splinter_mask], y[splinter_mask], c="white", edgecolors="black", s=9, linewidths=0.25)
plt.scatter(pole[0], pole[1], marker="x", s=260, linewidths=4)
plt.axis("equal")
plt.title("EXP_06 — Rope Field Projected to Prime Residue States (mod 23)")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="residue state")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp06_rope_residue_projection_mod23.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# VISUAL 2 — MATRIX DECOMPOSITION
# ------------------------------------------------------------

P = results[mod_show]["P"]
C = results[mod_show]["C"]
R = results[mod_show]["R"]

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

for ax, mat, title in zip(
    axs,
    [P, C, R],
    ["Total Transition Flow", "Cycle-Core Component", "Residual / Drift Component"],
):
    im = ax.imshow(mat, cmap="magma")
    ax.set_title(title)
    ax.set_xlabel("to state")
    ax.set_ylabel("from state")
    plt.colorbar(im, ax=ax, fraction=0.046)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp06_transition_decomposition_mod23.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# VISUAL 3 — DOMINANT CYCLE GRAPH
# ------------------------------------------------------------

G = results[mod_show]["G"]
cycle = results[mod_show]["cycle"]

pos = nx.circular_layout(G)

plt.figure(figsize=(10, 10))

nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=700)
nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(
    G,
    pos,
    edge_color="gray",
    alpha=0.35,
    arrows=True,
    width=1
)

if cycle:
    cycle_edges = [
        (cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=cycle,
        node_color="red",
        node_size=850
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=cycle_edges,
        edge_color="red",
        width=3.5,
        arrows=True
    )

plt.title(
    f"EXP_06 — Dominant Prime Cycle Core (mod {mod_show})\n"
    f"len={len(cycle)} weight={results[mod_show]['cycle_weight']:.3f}"
)
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp06_dominant_cycle_core_mod23.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# VISUAL 4 — MULTI-MOD CYCLE COMPARISON
# ------------------------------------------------------------

cycle_lengths = []
cycle_weights = []
residual_energy = []

for mod in mods:
    cycle_lengths.append(len(results[mod]["cycle"]))
    cycle_weights.append(results[mod]["cycle_weight"])
    residual_energy.append(results[mod]["R"].sum() / (results[mod]["P"].sum() + 1e-9))

xpos = np.arange(len(mods))

plt.figure(figsize=(12, 6))
plt.plot(xpos, cycle_lengths, marker="o", linewidth=2, label="cycle length")
plt.plot(xpos, np.array(cycle_weights) * 20, marker="o", linewidth=2, label="cycle weight ×20")
plt.plot(xpos, np.array(residual_energy) * 20, marker="o", linewidth=2, label="residual energy ×20")
plt.xticks(xpos, [f"mod {m}" for m in mods])
plt.title("EXP_06 — Prime Mod Cycle / Drift Comparison")
plt.ylabel("scaled value")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp06_prime_mod_cycle_comparison.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# VISUAL 5 — SPLINTER STATE HITMAP
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

for mod in mods:
    s = results[mod]["state"]
    counts = np.bincount(s[splinter_mask], minlength=mod)
    counts = counts / (counts.sum() + 1e-9)
    plt.plot(np.arange(mod), counts, marker="o", linewidth=1.5, label=f"mod {mod}")

plt.title("EXP_06 — Splinter Events Across Prime Residue States")
plt.xlabel("residue state")
plt.ylabel("splinter probability")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp06_splinter_residue_hitmap.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print()
print("===================================")
print("EXP_06 — PRIME MODULAR ROPE TRANSITION GRAPH")
print("===================================")
print()

print(f"Samples: {N}")
print(f"Splinter events: {np.sum(splinter_mask)}")
print(f"Splinter threshold: {splinter_threshold:.6f}")
print()

print("Prime modular cycle summary:")
print("-----------------------------------")

for mod in mods:
    cyc = results[mod]["cycle"]
    print(
        f"mod {mod}: "
        f"cycle_len={len(cyc)}, "
        f"cycle_weight={results[mod]['cycle_weight']:.4f}, "
        f"residual_energy={results[mod]['R'].sum() / (results[mod]['P'].sum() + 1e-9):.4f}"
    )

print()
print("Generated visuals:")
print("-----------------------------------")
print("exp06_rope_residue_projection_mod23.png")
print("exp06_transition_decomposition_mod23.png")
print("exp06_dominant_cycle_core_mod23.png")
print("exp06_prime_mod_cycle_comparison.png")
print("exp06_splinter_residue_hitmap.png")

print()
print("DONE.")
print()
