# navigator_v34_noise_robustness.py

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

cluster_order = ["C0", "C1", "C2", "C3"]

# ============================================================
# 2. FIELD (same as before)
# ============================================================

def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x - center[0])**2 + (y - center[1])**2)/(2*sigma**2))

def envelope(t):
    return 1.0 + 0.4*np.sin(0.03*t)

def attractor_strengths(t):
    e = envelope(t)
    return {
        "C0": 1.5 * e,
        "C1": 2.0 * (1.0 + 0.4*np.sin(0.03*t + np.pi/2)),
        "C2": 3.0 * (1.0 + 0.3*np.sin(0.03*t)),
        "C3": -2.0,
    }

def scalar_field(x, y, t):
    val = 0.0
    strengths = attractor_strengths(t)
    for k, pos in clusters.items():
        val += gaussian(x, y, pos, strengths[k])
    return val

def grad_scalar_field(x, y, t, eps=1e-3):
    dx = (scalar_field(x+eps, y, t) - scalar_field(x-eps, y, t))/(2*eps)
    dy = (scalar_field(x, y+eps, t) - scalar_field(x, y-eps, t))/(2*eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x,y])
    v = np.zeros(2)

    for c in ["C2","C3"]:
        r = p - clusters[c]
        d = np.linalg.norm(r) + 1e-9
        if c=="C2":
            v += 0.8*np.array([r[1], -r[0]])*np.exp(-(d**2)/(2*1.4**2))
        else:
            v += 1.1*np.array([-r[1], r[0]])*np.exp(-(d**2)/(2*1.1**2))
    return v

def combined_field(x,y,t):
    return grad_scalar_field(x,y,t) + 0.65*rotational_field(x,y)

# ============================================================
# 3. SIMULATION WITH NOISE
# ============================================================

def simulate_endpoint(start, noise_level=0.0, steps=120, dt=0.08):
    x = np.array(start)

    for k in range(steps):
        v = combined_field(x[0], x[1], k)
        v = v/(np.linalg.norm(v)+1e-9)

        noise = noise_level * np.random.randn(2)

        x = x + dt*(v + noise)

    return x

def nearest_cluster(x):
    return min(clusters, key=lambda k: np.linalg.norm(x-clusters[k]))

# ============================================================
# 4. ROBUSTNESS MAP
# ============================================================

def compute_robustness(noise_level=0.1, trials=6, nx=60, ny=60):
    xs = np.linspace(6,17,nx)
    ys = np.linspace(22,31,ny)

    stability = np.zeros((ny,nx))

    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            results = []
            for _ in range(trials):
                end = simulate_endpoint([x,y], noise_level=noise_level)
                results.append(nearest_cluster(end))

            # fraction of dominant outcome
            dominant = max(set(results), key=results.count)
            stability[j,i] = results.count(dominant)/len(results)

    return xs, ys, stability

# ============================================================
# 5. PLOT
# ============================================================

def plot_v34():

    print("Running V34 Noise Robustness...")

    xs, ys, stab_low = compute_robustness(noise_level=0.05)
    _, _, stab_high = compute_robustness(noise_level=0.2)

    fig, axes = plt.subplots(1,2, figsize=(12,5))

    # low noise
    im1 = axes[0].contourf(xs, ys, stab_low, levels=30, cmap="viridis")
    axes[0].set_title("Low Noise Stability")
    plt.colorbar(im1, ax=axes[0])

    # high noise
    im2 = axes[1].contourf(xs, ys, stab_high, levels=30, cmap="magma")
    axes[1].set_title("High Noise Stability")
    plt.colorbar(im2, ax=axes[1])

    for ax in axes:
        for k,c in clusters.items():
            ax.scatter(c[0],c[1], c=cluster_colors[k], s=100, edgecolor='black')
            ax.text(c[0], c[1]+0.2, k, color="white", ha="center")

        ax.set_xlabel("α")
        ax.set_ylabel("β")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "v34_noise_robustness.png")
    plt.savefig(path, dpi=200)
    plt.close()

    print(f"Saved: {path}")

if __name__ == "__main__":
    plot_v34()
