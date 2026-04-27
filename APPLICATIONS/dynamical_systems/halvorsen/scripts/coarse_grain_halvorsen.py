# ============================================================
# NEXAH — Coarse Graining (Halvorsen System)
# ============================================================
#
# Purpose:
# Reduce high-resolution transition graph into coarse basins
# via similarity clustering of transition probability vectors.
#
# Pipeline:
# probs → vector space → similarity clustering → coarse matrix
#
# Outputs:
# - cluster mapping (txt)
# - coarse transition matrix (png)
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ============================================================
# 🔹 LOAD REAL PROBABILITIES
# ============================================================

# 👉 WICHTIG:
# Erstelle Datei:
# APPLICATIONS/dynamical_systems/halvorsen/data/probs.py
#
# mit:
# PROBS = { ... dein dict ... }

from APPLICATIONS.dynamical_systems.halvorsen.data.probs import PROBS

# ============================================================
# 🔹 BUILD VECTORS
# ============================================================

def build_vectors(probs):
    states = sorted(probs.keys())
    index = {s: i for i, s in enumerate(states)}

    vectors = []
    for s in states:
        vec = np.zeros(len(states))
        for t, p in probs[s].items():
            if t in index:
                vec[index[t]] = p
        vectors.append(vec)

    return states, np.array(vectors)

# ============================================================
# 🔹 COSINE SIMILARITY
# ============================================================

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ============================================================
# 🔹 CLUSTERING
# ============================================================

def cluster_states(vectors, threshold=0.90):
    clusters = []
    assigned = set()

    for i in range(len(vectors)):
        if i in assigned:
            continue

        cluster = [i]
        assigned.add(i)

        for j in range(i + 1, len(vectors)):
            if j in assigned:
                continue

            sim = cosine_similarity(vectors[i], vectors[j])
            if sim > threshold:
                cluster.append(j)
                assigned.add(j)

        clusters.append(cluster)

    return clusters

# ============================================================
# 🔹 BUILD COARSE MATRIX
# ============================================================

def build_coarse_matrix(states, probs, clusters):
    n = len(clusters)
    matrix = np.zeros((n, n))

    state_to_cluster = {}
    for i, cluster in enumerate(clusters):
        for idx in cluster:
            state_to_cluster[states[idx]] = i

    for s, transitions in probs.items():
        i = state_to_cluster[s]

        for t, p in transitions.items():
            if t in state_to_cluster:
                j = state_to_cluster[t]
                matrix[i, j] += p

    # normalize rows
    for i in range(n):
        if matrix[i].sum() > 0:
            matrix[i] /= matrix[i].sum()

    return matrix, state_to_cluster

# ============================================================
# 🔹 SAVE OUTPUT
# ============================================================

def save_outputs(matrix, mapping):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_path = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base_path, exist_ok=True)

    # TXT mapping
    txt_path = f"{base_path}/coarse_mapping_{timestamp}.txt"
    with open(txt_path, "w") as f:
        for state, cluster in mapping.items():
            f.write(f"{state} -> cluster {cluster}\n")

    # PNG matrix
    fig = plt.figure(figsize=(6,5))
    plt.imshow(matrix)
    plt.title("Coarse-Grained Transition Matrix")
    plt.colorbar()
    plt.xlabel("to cluster j")
    plt.ylabel("from cluster i")

    png_path = f"{base_path}/coarse_matrix_{timestamp}.png"
    plt.savefig(png_path)
    plt.close()

    print(f"[✓] Mapping saved: {txt_path}")
    print(f"[✓] Matrix saved: {png_path}")

# ============================================================
# 🔹 MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load transitions")
    probs = PROBS

    print("→ build vectors")
    states, vectors = build_vectors(probs)

    print("→ cluster states")
    clusters = cluster_states(vectors, threshold=0.90)

    print(f"clusters: {len(clusters)}")

    print("→ build coarse matrix")
    matrix, mapping = build_coarse_matrix(states, probs, clusters)

    print("→ save")
    save_outputs(matrix, mapping)

    print("✔ DONE")
