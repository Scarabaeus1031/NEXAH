import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import os

OUTPUT_DIR = "RESEARCH/validation/duffing/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================
# Duffing system
# ============================

def duffing(x, v, t, delta=0.2, alpha=-1.0, beta=1.0, gamma=0.3, omega=1.2):
    dxdt = v
    dvdt = -delta*v - alpha*x - beta*x**3 + gamma*np.cos(omega*t)
    return dxdt, dvdt

def simulate_duffing(steps=5000, dt=0.02, noise_init=0.01):
    x = np.zeros(steps)
    v = np.zeros(steps)

    # 🔥 random initial condition
    x[0] = 0.1 + noise_init * np.random.randn()
    v[0] = 0.0 + noise_init * np.random.randn()

    t = 0.0

    for i in range(steps - 1):
        dx, dv = duffing(x[i], v[i], t)
        x[i+1] = x[i] + dx * dt
        v[i+1] = v[i] + dv * dt
        t += dt

    return np.stack([x, v], axis=1)

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
# Multi-run
# ============================

def run_multirun(n_runs=10):
    endpoints = []
    trajectories = []

    for _ in range(n_runs):
        data = simulate_duffing()
        endpoints.append(data[-1])
        trajectories.append(data)

    endpoints = np.array(endpoints)

    D = cdist(endpoints, endpoints)
    mean_dist = np.mean(D)
    std_dist = np.std(D)

    print("\n=== DUFFING MULTI-RUN ===")
    print(f"Mean endpoint distance: {mean_dist:.4f}")
    print(f"Std: {std_dist:.4f}")

    plt.figure()
    for traj in trajectories:
        plt.plot(traj[:,0], traj[:,1], alpha=0.4)
    plt.title("Duffing Trajectory Overlay")
    plt.savefig(f"{OUTPUT_DIR}/trajectory_overlay.png")
    plt.close()

    return mean_dist, std_dist

# ============================
# Noise
# ============================

def run_noise_test(noise=1.0):
    clean = simulate_duffing()
    noisy = clean + noise * np.random.randn(*clean.shape)

    plt.figure()
    plt.plot(clean[:,0], clean[:,1], label="clean")
    plt.plot(noisy[:,0], noisy[:,1], alpha=0.5, label="noisy")
    plt.legend()
    plt.title("Duffing Noise Comparison")
    plt.savefig(f"{OUTPUT_DIR}/noise_comparison.png")
    plt.close()

# ============================
# Transition
# ============================

def run_transition():
    data = simulate_duffing()

    k = 6
    km = KMeans(n_clusters=k, n_init=10)
    labels = km.fit_predict(data)

    T = compute_transition_matrix(labels)

    plt.imshow(T)
    plt.title("Duffing Transition Matrix")
    plt.colorbar()
    plt.savefig(f"{OUTPUT_DIR}/transition_matrix.png")
    plt.close()

    return T

# ============================
# Partition invariance
# ============================

def run_partition():
    data = simulate_duffing()

    k = 6

    km1 = KMeans(n_clusters=k, n_init=10).fit(data)
    km2 = KMeans(n_clusters=k, n_init=10).fit(data[:, :1])  # projection

    T1 = compute_transition_matrix(km1.labels_)
    T2 = compute_transition_matrix(km2.labels_)

    d = matrix_distance(T1, T2)

    print("\n=== DUFFING PARTITION ===")
    print(f"Difference: {d:.6f}")

    return d

# ============================
# Main
# ============================

if __name__ == "__main__":

    print("⚡ NEXAH — Duffing Validation Suite")

    run_multirun()
    run_noise_test()
    run_transition()
    run_partition()

    print("\n✅ Duffing validation complete.")
