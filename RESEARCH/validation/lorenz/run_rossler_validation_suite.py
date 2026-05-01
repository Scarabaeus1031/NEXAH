import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

# ============================
# Rössler system
# ============================

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return dx, dy, dz

def simulate_rossler(steps=5000, dt=0.01):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = rossler(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return np.stack([xs, ys, zs], axis=1)

# ============================
# Transition matrix
# ============================

def compute_transition_matrix(labels):
    k = len(np.unique(labels))
    T = np.zeros((k, k))

    for i in range(len(labels) - 1):
        T[labels[i], labels[i+1]] += 1

    T /= T.sum(axis=1, keepdims=True) + 1e-8
    return T

def matrix_distance(A, B):
    return np.mean(np.abs(A - B))

# ============================
# Multi-run simulation
# ============================

def run_multirun(n_runs=10):
    endpoints = []
    trajectories = []

    for _ in range(n_runs):
        data = simulate_rossler()
        endpoints.append(data[-1])
        trajectories.append(data)

    endpoints = np.array(endpoints)

    mean_dist = np.mean(cdist(endpoints, endpoints))
    std_dist = np.std(cdist(endpoints, endpoints))

    print("\n=== MULTI-RUN ===")
    print(f"Mean endpoint distance: {mean_dist:.4f}")
    print(f"Std: {std_dist:.4f}")

    # Plot
    plt.figure()
    for traj in trajectories:
        plt.plot(traj[:,0], traj[:,1], alpha=0.5)
    plt.title("Rössler Trajectory Overlay")
    plt.savefig("RESEARCH/validation/rossler/results/trajectory_overlay.png")
    plt.close()

    return mean_dist, std_dist

# ============================
# Noise test
# ============================

def run_noise_test(n_runs=10, noise=1.0):
    clean_data = simulate_rossler()
    noisy_data = clean_data + noise * np.random.randn(*clean_data.shape)

    plt.figure()
    plt.plot(clean_data[:,0], clean_data[:,1], label="clean")
    plt.plot(noisy_data[:,0], noisy_data[:,1], alpha=0.6, label="noisy")
    plt.legend()
    plt.title("Noise Comparison")
    plt.savefig("RESEARCH/validation/rossler/results/noise_comparison.png")
    plt.close()

    print("\n=== NOISE TEST ===")
    print("Noise applied, structure visually inspectable")

# ============================
# Transition stability
# ============================

def run_transition_test():
    data = simulate_rossler()

    k = 6
    km = KMeans(n_clusters=k, n_init=10)
    labels = km.fit_predict(data)

    T = compute_transition_matrix(labels)

    print("\n=== TRANSITION TEST ===")
    print("Transition matrix computed")

    plt.imshow(T, cmap="viridis")
    plt.title("Transition Matrix")
    plt.colorbar()
    plt.savefig("RESEARCH/validation/rossler/results/transition_matrix.png")
    plt.close()

    return T

# ============================
# Partition invariance (simple)
# ============================

def run_partition_invariance():
    data = simulate_rossler()

    k = 6

    km1 = KMeans(n_clusters=k, n_init=10).fit(data)
    km2 = KMeans(n_clusters=k, n_init=10).fit(data[:, :2])  # projection

    T1 = compute_transition_matrix(km1.labels_)
    T2 = compute_transition_matrix(km2.labels_)

    d = matrix_distance(T1, T2)

    print("\n=== PARTITION INVARIANCE ===")
    print(f"Difference: {d:.6f}")

    plt.figure(figsize=(8,4))
    plt.subplot(1,2,1)
    plt.imshow(T1)
    plt.title("Full")

    plt.subplot(1,2,2)
    plt.imshow(T2)
    plt.title("Projected")

    plt.savefig("RESEARCH/validation/rossler/results/partition_invariance.png")
    plt.close()

    return d

# ============================
# Main
# ============================

if __name__ == "__main__":

    print("⚡ NEXAH — Rössler Validation Suite")

    run_multirun()
    run_noise_test()
    run_transition_test()
    run_partition_invariance()

    print("\n✅ Rössler validation complete.")
