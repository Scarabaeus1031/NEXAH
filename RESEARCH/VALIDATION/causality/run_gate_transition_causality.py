import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ============================
# Setup
# ============================

OUTPUT_DIR = "RESEARCH/validation/causality/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================
# Lorenz System
# ============================

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

# ============================
# Transition Matrix
# ============================

def compute_transition_matrix(labels, k):
    T = np.zeros((k, k))

    for i in range(len(labels) - 1):
        T[labels[i], labels[i+1]] += 1

    T /= (T.sum(axis=1, keepdims=True) + 1e-8)
    return T

def matrix_distance(A, B):
    return np.mean(np.abs(A - B))

# ============================
# Gate Intervention
# ============================

def apply_gate_intervention(data, strength=2.0):
    """
    Boost points in transition region (center of Lorenz attractor)
    """

    modified = data.copy()

    # Gate heuristic: near origin (center switching region)
    gate_mask = np.linalg.norm(data[:, :2], axis=1) < 5.0

    # amplify motion in that region
    modified[gate_mask] += strength * np.random.randn(*modified[gate_mask].shape)

    return modified, gate_mask

# ============================
# Main Experiment
# ============================

def run_experiment():
    print("⚡ NEXAH — Gate Transition Causality Test")

    data = simulate_lorenz()

    k = 6
    km = KMeans(n_clusters=k, n_init=10)
    labels = km.fit_predict(data)

    T_base = compute_transition_matrix(labels, k)

    # Apply intervention
    data_mod, gate_mask = apply_gate_intervention(data)

    labels_mod = km.predict(data_mod)
    T_mod = compute_transition_matrix(labels_mod, k)

    # Compare
    diff = matrix_distance(T_base, T_mod)

    print("\n=== RESULT ===")
    print(f"Mean transition difference: {diff:.6f}")

    # ============================
    # Visuals
    # ============================

    # Transition matrices
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.imshow(T_base, cmap="viridis")
    plt.title("Baseline")

    plt.subplot(1,2,2)
    plt.imshow(T_mod, cmap="viridis")
    plt.title("After Gate Intervention")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/gate_transition_comparison.png")
    plt.close()

    # Difference map
    plt.figure()
    plt.imshow(np.abs(T_base - T_mod), cmap="inferno")
    plt.title("Transition Difference Map")
    plt.colorbar()
    plt.savefig(f"{OUTPUT_DIR}/gate_transition_difference.png")
    plt.close()

    # Gate region visualization
    plt.figure()
    plt.scatter(data[:,0], data[:,1], c="lightgray", s=1)
    plt.scatter(data[gate_mask,0], data[gate_mask,1], c="red", s=1)
    plt.title("Gate Intervention Region")
    plt.savefig(f"{OUTPUT_DIR}/gate_region.png")
    plt.close()

    # Save summary
    with open(f"{OUTPUT_DIR}/causality_summary.txt", "w") as f:
        f.write("NEXAH — Gate Transition Causality\n\n")
        f.write(f"Mean transition difference: {diff:.6f}\n")

    print("✅ Saved results to:", OUTPUT_DIR)


# ============================
# Run
# ============================

if __name__ == "__main__":
    run_experiment()
