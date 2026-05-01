import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cdist

# -----------------------------
# Lorenz system
# -----------------------------
def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

def simulate_lorenz(steps=5000, dt=0.01):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return np.stack([xs, ys, zs], axis=1)

# -----------------------------
# Transition matrix
# -----------------------------
def compute_transition_matrix(labels):
    valid = labels != -1
    labels = labels[valid]

    unique = np.unique(labels)
    k = len(unique)

    if k < 2:
        return None

    mapping = {u: i for i, u in enumerate(unique)}
    T = np.zeros((k, k))

    for i in range(len(labels) - 1):
        a = mapping[labels[i]]
        b = mapping[labels[i+1]]
        T[a, b] += 1

    T /= T.sum(axis=1, keepdims=True) + 1e-8
    return T

# -----------------------------
# Matrix distance (shape-aware)
# -----------------------------
def matrix_distance(A, B):
    if A.shape != B.shape:
        return None
    return np.mean(np.abs(A - B))

# -----------------------------
# Main experiment
# -----------------------------
data = simulate_lorenz()

eps_values = np.linspace(0.1, 0.4, 8)
transition_matrices = {}
cluster_counts = {}

print("\n=== DBSCAN Transition Invariance Test ===\n")

for eps in eps_values:
    db = DBSCAN(eps=eps, min_samples=10)
    labels = db.fit_predict(data)

    T = compute_transition_matrix(labels)
    k = len(set(labels)) - (1 if -1 in labels else 0)

    cluster_counts[eps] = k
    transition_matrices[eps] = T

    print(f"eps={eps:.3f} → clusters={k}")

# -----------------------------
# Compare matrices
# -----------------------------
print("\nPairwise transition distances:\n")

eps_list = list(eps_values)
distances = []

for i in range(len(eps_list)):
    for j in range(i+1, len(eps_list)):
        e1, e2 = eps_list[i], eps_list[j]
        T1, T2 = transition_matrices[e1], transition_matrices[e2]

        d = matrix_distance(T1, T2)

        if d is not None:
            distances.append(d)
            print(f"{e1:.2f} vs {e2:.2f} → {d:.6f}")

# -----------------------------
# Summary
# -----------------------------
valid_distances = [d for d in distances if d is not None]

mean_dist = np.mean(valid_distances) if valid_distances else None

print("\n=== SUMMARY ===\n")
print(f"Mean transition difference: {mean_dist}")

# -----------------------------
# Plot cluster count vs eps
# -----------------------------
plt.figure()
plt.plot(list(cluster_counts.keys()), list(cluster_counts.values()), marker='o')
plt.xlabel("eps")
plt.ylabel("number of clusters")
plt.title("DBSCAN cluster count vs eps")
plt.grid()
plt.savefig("RESEARCH/validation/lorenz/results/dbscan_transition_invariance_clusters.png")
plt.close()

print("\nSaved plot: dbscan_transition_invariance_clusters.png")
