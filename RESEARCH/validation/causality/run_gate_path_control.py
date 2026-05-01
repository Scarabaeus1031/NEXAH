import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ============================
# Lorenz system
# ============================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s*(y - x)
    dy = x*(r - z) - y
    dz = x*y - b*z
    return dx, dy, dz

def simulate_lorenz_control(steps=5000, dt=0.01, gate_region=None, target=None):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])

        # --- Gate intervention ---
        if gate_region is not None:
            x, y = xs[i], ys[i]
            x_min, x_max, y_min, y_max = gate_region

            if x_min < x < x_max and y_min < y < y_max:
                # small directional bias toward target
                if target is not None:
                    tx, ty = target
                    dx += 0.5 * (tx - x)
                    dy += 0.5 * (ty - y)

        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return np.stack([xs, ys, zs], axis=1)

# ============================
# Transition matrix
# ============================

def compute_transition_matrix(labels, k):
    T = np.zeros((k, k))

    for i in range(len(labels)-1):
        T[labels[i], labels[i+1]] += 1

    T /= T.sum(axis=1, keepdims=True) + 1e-8
    return T

# ============================
# Main experiment
# ============================

def run_path_control():

    print("⚡ NEXAH — Gate Path Control")

    # baseline
    data_base = simulate_lorenz_control()

    # gate + target
    gate_region = (-5, 5, -5, 5)
    target = (15, 15)

    data_ctrl = simulate_lorenz_control(
        gate_region=gate_region,
        target=target
    )

    # clustering
    k = 6
    km = KMeans(n_clusters=k, n_init=10)

    labels_base = km.fit_predict(data_base)
    labels_ctrl = km.fit_predict(data_ctrl)

    T_base = compute_transition_matrix(labels_base, k)
    T_ctrl = compute_transition_matrix(labels_ctrl, k)

    diff = np.mean(np.abs(T_base - T_ctrl))

    print(f"Mean transition difference: {diff:.6f}")

    # ============================
    # Plot trajectories
    # ============================

    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.plot(data_base[:,0], data_base[:,1], alpha=0.6)
    plt.title("Baseline")

    plt.subplot(1,2,2)
    plt.plot(data_ctrl[:,0], data_ctrl[:,1], alpha=0.6)
    plt.scatter(target[0], target[1], c='red', s=100, label='target')
    plt.legend()
    plt.title("Controlled")

    plt.savefig("RESEARCH/validation/causality/results/path_control.png")
    plt.close()

    print("✅ Saved: path_control.png")

# ============================
# Run
# ============================

if __name__ == "__main__":
    run_path_control()
