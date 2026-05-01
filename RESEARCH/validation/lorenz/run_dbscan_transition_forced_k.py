import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
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
    k = len(np.unique(labels))
    T = np.zeros((k, k))

    for i in range(len(labels) - 1):
        T[labels[i], labels[i+1]] += 1

    T /= T.sum(axis=1, keepdims=True) + 1e-8
    return T

def matrix_distance(A, B):
    return np.mean(np.abs(A - B))

# -----------------------------
# Main experiment
# -----------------------------
data = simulate_lorenz()

eps_values = np.linspace(0.1, 0.4, 8)
k_fixed = 6

transition_matrices = {}

print("\n=== DBSCAN + Forced K Transition Test ===\n")

for eps in eps_values:
    db = DBSCAN(eps=eps, min_samples=10)
    db_labels = db.fit_predict(data)

    valid_mask = db_labels != -1
    valid_data = data[valid_mask]

    if len(valid_data) < 100:
        print(f"eps={eps:.3f} → too few points, skipped")
        continue

    # KMeans on valid region
    km = KMeans(n_clusters=k_fixed, n_init=10)
    km_labels = km.fit_predict(valid_data)

    # Rebuild full label sequence (only valid points)
    labels = km_labels

    T = compute_transition_matrix(labels)
    transition_matrices[eps] = T

    print(f"eps={eps:.3f} → valid_points={len(valid_data)}")

# -----------------------------
# Compare matrices
# -----------------------------
print("\nPairwise transition distances:\n")

eps_list = list(transition_matrices.keys())
distances = []

for i in range(len(eps_list)):
    for j in range(i+1, len(eps_list)):
        e1, e2 = eps_list[i], eps_list[j]
        T1, T2 = transition_matrices[e1], transition_matrices[e2]

        d = matrix_distance(T1, T2)
        distances.append(d)

        print(f"{e1:.2f} vs {e2:.2f} → {d:.6f}")

# -----------------------------
# Summary
# -----------------------------
mean_dist = np.mean(distances)

print("\n=== SUMMARY ===\n")
print(f"Mean transition difference: {mean_dist:.6f}")

# -----------------------------
# Save simple plot
# -----------------------------
plt.figure()
plt.hist(distances, bins=10)
plt.title("Transition Matrix Differences (Forced K)")
plt.xlabel("difference")
plt.ylabel("count")

plt.savefig("RESEARCH/validation/lorenz/results/dbscan_forced_k_transition_diff.png")
plt.close()

print("\nSaved: dbscan_forced_k_transition_diff.png")
