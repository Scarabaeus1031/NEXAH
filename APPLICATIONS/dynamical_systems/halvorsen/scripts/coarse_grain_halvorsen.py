# ⚡ NEXAH — Coarse Graining (Halvorsen)
# ------------------------------------------------------------
# Groups fine-grained states into flow channels
#
# Idea:
# states with similar transition behavior → same macro-state
#
# Output:
# - coarse_transition_matrix.png
# - coarse_mapping.txt
# ------------------------------------------------------------

import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


# -----------------------------
# Load / define transitions
# -----------------------------
# 👉 hier einfach dein probs dict reinkopieren
# oder später aus Datei laden

def load_example():
    return {
        0: {0: 0.8, 1: 0.2},
        1: {1: 0.7, 2: 0.3},
        2: {2: 0.6, 3: 0.4},
        3: {3: 1.0}
    }


# -----------------------------
# Build transition vectors
# -----------------------------

def build_vectors(probs):
    states = list(probs.keys())
    state_index = {s: i for i, s in enumerate(states)}

    dim = len(states)
    vectors = {}

    for s in states:
        vec = np.zeros(dim)
        for t, p in probs[s].items():
            if t in state_index:
                vec[state_index[t]] = p
        vectors[s] = vec

    return vectors


# -----------------------------
# Similarity grouping (cosine)
# -----------------------------

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def cluster_states(vectors, threshold=0.95):
    clusters = []
    assigned = set()

    states = list(vectors.keys())

    for s in states:
        if s in assigned:
            continue

        cluster = [s]
        assigned.add(s)

        for t in states:
            if t in assigned:
                continue

            sim = cosine_similarity(vectors[s], vectors[t])

            if sim > threshold:
                cluster.append(t)
                assigned.add(t)

        clusters.append(cluster)

    return clusters


# -----------------------------
# Build coarse matrix
# -----------------------------

def build_coarse_matrix(probs, clusters):
    cluster_id = {}
    for i, cluster in enumerate(clusters):
        for s in cluster:
            cluster_id[s] = i

    coarse = defaultdict(lambda: defaultdict(float))

    for s, edges in probs.items():
        i = cluster_id[s]
        for t, p in edges.items():
            j = cluster_id.get(t, None)
            if j is not None:
                coarse[i][j] += p

    # normalize again (important)
    for i in coarse:
        total = sum(coarse[i].values())
        for j in coarse[i]:
            coarse[i][j] /= total

    return coarse, cluster_id


# -----------------------------
# Save mapping
# -----------------------------

def save_mapping(cluster_id, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(base_dir, f"coarse_mapping_{timestamp}.txt")

    with open(path, "w") as f:
        for k, v in sorted(cluster_id.items()):
            f.write(f"{k} -> cluster {v}\n")

    print(f"[✓] Mapping saved: {path}")


# -----------------------------
# Plot matrix
# -----------------------------

def plot_matrix(coarse, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    states = list(coarse.keys())
    n = len(states)

    matrix = np.zeros((n, n))

    for i, edges in coarse.items():
        for j, p in edges.items():
            matrix[i, j] = p

    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(matrix)

    plt.colorbar(im)
    ax.set_title("Coarse-Grained Transition Matrix")

    plt.tight_layout()

    path = os.path.join(base_dir, f"coarse_matrix_{timestamp}.png")
    fig.savefig(path, dpi=300)

    print(f"[✓] Matrix saved: {path}")


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    base_dir = os.path.join(
        "APPLICATIONS",
        "dynamical_systems",
        "halvorsen",
        "outputs"
    )
    os.makedirs(base_dir, exist_ok=True)

    print("→ load transitions")
    probs = load_example()  # 🔴 hier später echte probs rein

    print("→ build vectors")
    vectors = build_vectors(probs)

    print("→ cluster states")
    clusters = cluster_states(vectors, threshold=0.97)

    print(f"clusters: {len(clusters)}")

    print("→ build coarse matrix")
    coarse, mapping = build_coarse_matrix(probs, clusters)

    print("→ save")
    save_mapping(mapping, base_dir)
    plot_matrix(coarse, base_dir)

    print("✔ DONE")
