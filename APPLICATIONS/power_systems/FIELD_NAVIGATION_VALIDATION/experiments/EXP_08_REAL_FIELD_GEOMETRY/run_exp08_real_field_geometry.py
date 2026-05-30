"""
EXP_08_REAL_FIELD_GEOMETRY

Goal:
Test whether real IEEE39 Monte-Carlo operating states form
a structured field geometry with corridors, density regions,
and bottleneck / gate candidates.

Data:
pandapower.networks.case39()

NEXAH Validation Program
2026
"""

from pathlib import Path
import copy
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

import pandapower as pp
import pandapower.networks as pn

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


warnings.filterwarnings("ignore")
np.random.seed(42)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print()
print(f"Outputs -> {OUTPUT_DIR}")
print()


# ============================================================
# Load IEEE39
# ============================================================

net0 = pn.case39()
bus_ids = list(net0.bus.index)

base_load_p = net0.load.p_mw.copy()
base_load_q = net0.load.q_mvar.copy()

print(f"Loaded IEEE39 with {len(bus_ids)} buses")


# ============================================================
# Monte Carlo Real Power Flow States
# ============================================================

N_RUNS = 1200

records = []
state_vectors = []

for run_id in range(N_RUNS):

    net = copy.deepcopy(net0)

    global_scale = np.random.uniform(0.75, 1.90)

    local_scale = np.random.normal(
        loc=1.0,
        scale=0.12,
        size=len(net.load)
    )

    local_scale = np.clip(local_scale, 0.65, 1.45)

    net.load.p_mw = base_load_p.values * global_scale * local_scale
    net.load.q_mvar = base_load_q.values * global_scale * local_scale

    converged = True

    try:
        pp.runpp(
            net,
            max_iteration=40,
            tolerance_mva=1e-6,
            init="auto"
        )
    except Exception:
        converged = False

    if not converged:        continue

    vm = net.res_bus.vm_pu.reindex(bus_ids).values
    va = net.res_bus.va_degree.reindex(bus_ids).values

    min_vm = float(np.nanmin(vm))
    mean_vm = float(np.nanmean(vm))
    std_vm = float(np.nanstd(vm))

    min_angle = float(np.nanmin(va))
    max_angle = float(np.nanmax(va))

    angle_span = max_angle - min_angle

    if len(net.res_line) > 0:

        max_loading = float(
            np.nanmax(
                net.res_line.loading_percent.values
            )
        )

        mean_loading = float(
            np.nanmean(
                net.res_line.loading_percent.values
            )
        )

    else:

        max_loading = 0.0
        mean_loading = 0.0

    state_vector = [
        global_scale,
        min_vm,
        mean_vm,
        std_vm,
        angle_span,
        max_loading,
        mean_loading
    ]

    state_vectors.append(state_vector)

    records.append({
        "run_id": run_id,
        "global_scale": global_scale,
        "min_vm": min_vm,
        "mean_vm": mean_vm,
        "std_vm": std_vm,
        "angle_span": angle_span,
        "max_loading": max_loading,
        "mean_loading": mean_loading
    })


# ============================================================
# DataFrame
# ============================================================

df = pd.DataFrame(records)

print(
    f"Converged runs: "
    f"{len(df)}"
)

X = np.array(state_vectors)


# ============================================================
# PCA Embedding
# ============================================================

pca = PCA(
    n_components=2,
    random_state=42
)

Z = pca.fit_transform(X)

df["pca_x"] = Z[:, 0]
df["pca_y"] = Z[:, 1]


# ============================================================
# kNN Graph Construction
# ============================================================

K = 12

nbrs = NearestNeighbors(
    n_neighbors=K
)

nbrs.fit(Z)

distances, indices = nbrs.kneighbors(Z)

G_field = nx.Graph()

for i in range(len(Z)):

    G_field.add_node(i)

for i in range(len(Z)):

    for j in indices[i][1:]:

        d = np.linalg.norm(
            Z[i] - Z[j]
        )

        G_field.add_edge(
            i,
            j,
            weight=d
        )

print(
    f"kNN nodes: {G_field.number_of_nodes()}"
)

print(
    f"kNN edges: {G_field.number_of_edges()}"
)


# ============================================================
# Density Estimate
# ============================================================

local_density = []

for row in distances:

    local_density.append(
        1.0 / (np.mean(row[1:]) + 1e-8)
    )

local_density = np.array(
    local_density
)

df["density"] = local_density


# ============================================================
# Betweenness Centrality
# ============================================================

print(
    "Computing betweenness..."
)

bet = nx.betweenness_centrality(
    G_field,
    normalized=True
)

betweenness = np.array(
    [
        bet[i]
        for i in range(len(Z))
    ]
)

df["betweenness"] = betweenness


# ============================================================
# Gate Candidates
# ============================================================

gate_threshold = np.percentile(
    betweenness,
    99
)

gate_mask = (
    betweenness >= gate_threshold
)

gate_nodes = np.where(
    gate_mask
)[0]

print(
    f"Gate candidates: "
    f"{len(gate_nodes)}"
)


# ============================================================
# Connected Components
# ============================================================

components = list(
    nx.connected_components(
        G_field
    )
)

print(
    f"Connected components: "
    f"{len(components)}"
)

largest_component = max(
    components,
    key=len
)

print(
    f"Largest component size: "
    f"{len(largest_component)}"
)
# ============================================================
# Visual 1
# Real State Space
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    s=25,
    alpha=0.8
)

plt.title(
    "EXP_08 — Real IEEE39 State Space"
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp08_real_state_space.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 2
# Density Map
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    c=local_density,
    cmap="viridis",
    s=30
)

plt.colorbar(label="Density")

plt.title(
    "EXP_08 — Density Structure"
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp08_density_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 3
# Betweenness Map
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    c=betweenness,
    cmap="plasma",
    s=30
)

plt.colorbar(label="Betweenness")

plt.title(
    "EXP_08 — Transport Structure"
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp08_betweenness_map.png",
    dpi=300
)

plt.close()


# ============================================================
# Visual 4
# Gate Candidates
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    Z[:, 0],
    Z[:, 1],
    color="lightgray",
    s=20,
    alpha=0.5
)

plt.scatter(
    Z[gate_nodes, 0],
    Z[gate_nodes, 1],
    color="red",
    s=120,
    label="Gate Candidates"
)

plt.legend()

plt.title(
    "EXP_08 — Gate Candidates"
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp08_gate_candidates.png",
    dpi=300
)

plt.close()


# ============================================================
# Save Tables
# ============================================================

df.to_csv(
    OUTPUT_DIR / "exp08_field_states.csv",
    index=False
)

report = f"""
EXP_08 REAL FIELD GEOMETRY
========================================

Converged runs: {len(df)}

kNN nodes: {G_field.number_of_nodes()}
kNN edges: {G_field.number_of_edges()}

Connected components: {len(components)}
Largest component size: {len(largest_component)}

Gate candidates: {len(gate_nodes)}

Mean density:
{local_density.mean():.6f}

Mean betweenness:
{betweenness.mean():.6f}
"""

with open(
    OUTPUT_DIR / "exp08_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_08 completed.")
print()
