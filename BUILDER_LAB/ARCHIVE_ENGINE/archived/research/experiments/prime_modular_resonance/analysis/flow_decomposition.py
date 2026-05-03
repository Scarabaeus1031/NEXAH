# flow_decomposition.py

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

MOD = 23
N_PRIMES = 20000

TOP_EDGES = 2
MAX_CYCLE_LEN = 8
MAX_CYCLES = 200

OUTPUT_PATH = "output/plots"
DATA_PATH = "output/data"

os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)

# =========================
# PRIME RESIDUES
# =========================

primes = np.array(list(primerange(2, 300000)))[:N_PRIMES]
res = primes % MOD

# =========================
# TRANSITION MATRIX
# =========================

T = np.zeros((MOD, MOD))

for i in range(len(res) - 1):
    T[res[i], res[i + 1]] += 1

row_sums = T.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
P = T / row_sums

# =========================
# SPARSE GRAPH
# =========================

G = nx.DiGraph()

for i in range(MOD):
    top_idx = np.argsort(P[i])[-TOP_EDGES:]
    for j in top_idx:
        if P[i, j] > 0:
            G.add_edge(i, j, weight=P[i, j])

# =========================
# FIND SHORT CYCLES
# =========================

cycles = []

for c in nx.simple_cycles(G):
    if 2 <= len(c) <= MAX_CYCLE_LEN:
        cycles.append(c)

cycles = cycles[:MAX_CYCLES]

print(f"\n=== FLOW DECOMPOSITION — mod {MOD} ===")
print(f"cycles used: {len(cycles)}")

# =========================
# CYCLE COMPONENT MATRIX
# =========================

C = np.zeros_like(P)

for cycle in cycles:
    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[(i + 1) % len(cycle)]

        if P[a, b] > 0:
            C[a, b] += P[a, b]

# normalize cycle component to avoid double-count inflation
if C.max() > 0:
    C = C / C.max() * P.max()

# =========================
# RESIDUAL FLOW
# =========================

R = P - C
R[R < 0] = 0

# =========================
# METRICS
# =========================

total_flow = np.sum(P)
cycle_flow = np.sum(C)
residual_flow = np.sum(R)

cycle_fraction = cycle_flow / total_flow
residual_fraction = residual_flow / total_flow

print(f"total flow      = {total_flow:.4f}")
print(f"cycle flow      = {cycle_flow:.4f}")
print(f"residual flow   = {residual_flow:.4f}")
print(f"cycle fraction  = {cycle_fraction:.4f}")
print(f"residual frac.  = {residual_fraction:.4f}")

# =========================
# DRIFT METRICS
# =========================

def mean_modular_step(M):
    vals = []

    for i in range(MOD):
        for j in range(MOD):
            if M[i, j] > 0:
                step = (j - i) % MOD
                vals.append(step * M[i, j])

    if len(vals) == 0:
        return 0

    return np.sum(vals) / np.sum(M)

drift_total = mean_modular_step(P)
drift_cycle = mean_modular_step(C)
drift_resid = mean_modular_step(R)

print(f"\ndrift total     = {drift_total:.4f}")
print(f"drift cycle     = {drift_cycle:.4f}")
print(f"drift residual  = {drift_resid:.4f}")

# =========================
# SAVE DATA
# =========================

np.save(f"{DATA_PATH}/flow_total_mod{MOD}.npy", P)
np.save(f"{DATA_PATH}/flow_cycle_mod{MOD}.npy", C)
np.save(f"{DATA_PATH}/flow_residual_mod{MOD}.npy", R)

# =========================
# PLOT MATRIX DECOMPOSITION
# =========================

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

im0 = axes[0].imshow(P, cmap="viridis")
axes[0].set_title("Total Transition Flow")

im1 = axes[1].imshow(C, cmap="viridis")
axes[1].set_title("Cycle Component")

im2 = axes[2].imshow(R, cmap="magma")
axes[2].set_title("Residual / Drift Component")

for ax in axes:
    ax.set_xlabel("to state")
    ax.set_ylabel("from state")

fig.colorbar(im0, ax=axes[0])
fig.colorbar(im1, ax=axes[1])
fig.colorbar(im2, ax=axes[2])

plt.tight_layout()

save_path = f"{OUTPUT_PATH}/flow_decomposition_mod{MOD}.png"
plt.savefig(save_path, dpi=300)
plt.close()

print(f"\n[OK] saved → {save_path}")

# =========================
# GRAPH VIEW
# =========================

def graph_from_matrix(M, threshold=0.03):
    H = nx.DiGraph()

    for i in range(MOD):
        for j in range(MOD):
            if M[i, j] > threshold:
                H.add_edge(i, j, weight=M[i, j])

    return H

G_total = graph_from_matrix(P)
G_cycle = graph_from_matrix(C)
G_resid = graph_from_matrix(R)

pos = nx.circular_layout(G_total)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, H, title in zip(
    axes,
    [G_total, G_cycle, G_resid],
    ["Total Flow", "Cycle Flow", "Residual Flow"]
):
    weights = [H[u][v]["weight"] * 5 for u, v in H.edges]

    nx.draw(
        H,
        pos,
        ax=ax,
        node_size=300,
        node_color="lightblue",
        edge_color="gray",
        width=weights,
        arrows=True,
        with_labels=True,
        font_size=8
    )

    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()

save_path = f"{OUTPUT_PATH}/flow_decomposition_graph_mod{MOD}.png"
plt.savefig(save_path, dpi=300)
plt.close()

print(f"[OK] saved → {save_path}")

# =========================
# SUMMARY FILE
# =========================

summary_path = f"{DATA_PATH}/flow_decomposition_mod{MOD}.txt"

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"FLOW DECOMPOSITION — mod {MOD}\n\n")
    f.write(f"cycles used: {len(cycles)}\n")
    f.write(f"total flow: {total_flow:.6f}\n")
    f.write(f"cycle flow: {cycle_flow:.6f}\n")
    f.write(f"residual flow: {residual_flow:.6f}\n")
    f.write(f"cycle fraction: {cycle_fraction:.6f}\n")
    f.write(f"residual fraction: {residual_fraction:.6f}\n\n")
    f.write(f"drift total: {drift_total:.6f}\n")
    f.write(f"drift cycle: {drift_cycle:.6f}\n")
    f.write(f"drift residual: {drift_resid:.6f}\n")

print(f"[OK] saved → {summary_path}")

print("\n=== INTERPRETATION ===")
print("""
Cycle flow:
→ recurrent / loop-supported transition structure

Residual flow:
→ remaining directed transport after cycle extraction

If cycle fraction is high:
→ system is loop-dominated

If residual drift remains high:
→ system has transport beyond cycles

Key:
Flow = cycle structure + residual drift
""")
