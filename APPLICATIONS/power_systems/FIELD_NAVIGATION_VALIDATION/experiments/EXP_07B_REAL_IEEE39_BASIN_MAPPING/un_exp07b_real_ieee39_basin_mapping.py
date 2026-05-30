"""
run_exp07b_real_ieee39_basin_mapping.py

EXP_07B — REAL IEEE39 BASIN MAPPING

Goal:
Test whether IEEE39 graph communities correspond to dynamically discovered
state clusters / stability basins from real pandapower Monte-Carlo simulations.

Data:
- pandapower.networks.case39()

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

from networkx.algorithms.community import louvain_communities, modularity
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import normalized_mutual_info_score


warnings.filterwarnings("ignore")
np.random.seed(42)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_07B_REAL_IEEE39_BASIN_MAPPING"
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

print(f"Loaded IEEE39 with {len(bus_ids)} buses")


# ============================================================
# Build Real IEEE39 Graph
# ============================================================

G = nx.Graph()

for bus in bus_ids:
    G.add_node(int(bus))

for _, row in net0.line.iterrows():
    if row.in_service:
        G.add_edge(int(row.from_bus), int(row.to_bus))

if len(net0.trafo) > 0:
    for _, row in net0.trafo.iterrows():
        if row.in_service:
            G.add_edge(int(row.hv_bus), int(row.lv_bus))

pos = nx.spring_layout(G, seed=42)


# ============================================================
# Community Detection
# ============================================================

communities = louvain_communities(G, seed=42)
Q = modularity(G, communities)

community_map = {}

for cid, comm in enumerate(communities):
    for node in comm:
        community_map[node] = cid

n_communities = len(communities)

print(f"Louvain communities: {n_communities}")
print(f"Graph modularity: {Q:.6f}")


# ============================================================
# Monte-Carlo Simulation Settings
# ============================================================

N_RUNS = 1200

base_load_p = net0.load.p_mw.copy()
base_load_q = net0.load.q_mvar.copy()

records = []
state_vectors = []


# ============================================================
# Monte-Carlo Real Power Flow Runs
# ============================================================

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

    if converged:

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
                np.nanmax(net.res_line.loading_percent.values)
            )
            mean_loading = float(
                np.nanmean(net.res_line.loading_percent.values)
            )
        else:
            max_loading = 0.0
            mean_loading = 0.0

        risk_score = (
            (1.0 - min_vm)
            + 0.01 * max_loading
            + std_vm
            + 0.001 * angle_span
        )

        state_vector = [
            global_scale,
            min_vm,
            mean_vm,
            std_vm,
            angle_span,
            max_loading,            mean_loading
        ]

        state_vectors.append(state_vector)

        records.append({
            "run_id": run_id,
            "converged": 1,
            "global_scale": global_scale,
            "min_vm": min_vm,
            "mean_vm": mean_vm,
            "std_vm": std_vm,
            "angle_span": angle_span,
            "max_loading": max_loading,
            "mean_loading": mean_loading,
            "risk_score": risk_score
        })

    else:

        records.append({
            "run_id": run_id,
            "converged": 0,
            "global_scale": global_scale,
            "min_vm": np.nan,
            "mean_vm": np.nan,
            "std_vm": np.nan,
            "angle_span": np.nan,
            "max_loading": np.nan,
            "mean_loading": np.nan,
            "risk_score": np.nan
        })


# ============================================================
# DataFrames
# ============================================================

df = pd.DataFrame(records)

conv_df = df[
    df["converged"] == 1
].copy()

print()
print(
    f"Converged runs: "
    f"{len(conv_df)}"
)

print(
    f"Failed runs: "
    f"{len(df) - len(conv_df)}"
)


# ============================================================
# PCA State Space
# ============================================================

X = np.array(state_vectors)

pca = PCA(
    n_components=2,
    random_state=42
)

Z = pca.fit_transform(X)

conv_df["pca_x"] = Z[:, 0]
conv_df["pca_y"] = Z[:, 1]


# ============================================================
# DBSCAN State Clusters
# ============================================================

db = DBSCAN(
    eps=0.55,
    min_samples=12
)

clusters = db.fit_predict(Z)

conv_df["cluster"] = clusters

n_clusters = len(
    set(clusters)
    - {-1}
)

print(
    f"State clusters: "
    f"{n_clusters}"
)


# ============================================================
# Community Assignment
# ============================================================

community_sizes = []

for cid, comm in enumerate(communities):

    community_sizes.append(
        len(comm)
    )

community_sizes = np.array(
    community_sizes
)

community_prob = (
    community_sizes
    / community_sizes.sum()
)

scenario_community = np.random.choice(
    np.arange(n_communities),
    size=len(conv_df),
    p=community_prob
)

conv_df["community"] = scenario_community


# ============================================================
# Alignment Matrix
# ============================================================

cluster_ids = sorted(
    conv_df["cluster"].unique()
)

alignment = np.zeros(
    (
        n_communities,
        len(cluster_ids)
    )
)

purities = []

for cid in range(n_communities):

    tmp = conv_df[
        conv_df["community"] == cid
    ]

    if len(tmp) == 0:

        purities.append(0)

        continue

    counts = (
        tmp["cluster"]
        .value_counts(normalize=True)
    )

    purities.append(
        counts.max()
    )

    for j, cluster in enumerate(cluster_ids):

        alignment[cid, j] = (
            tmp["cluster"]
            .eq(cluster)
            .mean()
        )

mean_purity = float(
    np.mean(purities)
)

nmi = normalized_mutual_info_score(
    conv_df["community"],
    conv_df["cluster"]
)


# ============================================================
# Gate Scores
# ============================================================

gate_scores = []

for cid in range(n_communities):

    row = alignment[cid]

    row = row[row > 0]

    if len(row) <= 1:

        gate_scores.append(0)

    else:

        entropy = (
            -np.sum(
                row * np.log(row)
            )
        )

        entropy /= np.log(
            len(row)
        )

        gate_scores.append(
            float(entropy)
        )

gate_scores = np.array(
    gate_scores
)


# ============================================================
# Visual 1
# ============================================================

plt.figure(figsize=(9, 7))

plt.scatter(
    conv_df["pca_x"],
    conv_df["pca_y"],
    c=conv_df["cluster"],
    cmap="tab10",
    s=25
)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")

plt.title(
    "EXP_07B — Real IEEE39 State Space"
)

plt.grid(True)

plt.savefig(
    OUTPUT_DIR
    / "exp07b_real_state_map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
