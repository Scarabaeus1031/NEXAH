import os
import numpy as np
import matplotlib.pyplot as plt

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

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    val = 0.0
    val += gaussian(x, y, clusters["C2"], 3.0)
    val += gaussian(x, y, clusters["C1"], 2.0)
    val += gaussian(x, y, clusters["C0"], 1.5)
    val += gaussian(x, y, clusters["C3"], -2.0)
    return val

def grad_scalar_field(x, y, eps=1e-3):
    dx = (scalar_field(x+eps, y) - scalar_field(x-eps, y)) / (2*eps)
    dy = (scalar_field(x, y+eps) - scalar_field(x, y-eps)) / (2*eps)
    return np.array([dx, dy])

# ============================================================
# 3. CONTROL COST (simplified proxy)
# ============================================================

def control_cost(x, y):
    # distance + barrier penalty
    d = np.linalg.norm(np.array([x, y]) - clusters["C2"])
    
    barrier = np.exp(-((x - 11)**2 + (y - 29)**2) / 2.5)
    
    return d + 8 * barrier

# ============================================================
# 4. ROBUSTNESS (noise stability)
# ============================================================

def simulate_noise_stability(x, y, steps=20, noise=0.15):
    p = np.array([x, y], dtype=float)
    
    success = 0
    
    for _ in range(5):
        p_sim = p.copy()
        
        for _ in range(steps):
            v = grad_scalar_field(p_sim[0], p_sim[1])
            v = v / (np.linalg.norm(v) + 1e-9)
            p_sim += 0.2 * v
            p_sim += noise * np.random.randn(2)
        
        if np.linalg.norm(p_sim - clusters["C2"]) < 1.5:
            success += 1
    
    return success / 5.0

# ============================================================
# 5. GRID
# ============================================================

x = np.linspace(6, 17, 120)
y = np.linspace(22, 31, 120)
X, Y = np.meshgrid(x, y)

cost_field = np.zeros_like(X)
robust_field = np.zeros_like(X)

print("Computing V35 fields...")

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        cost_field[i, j] = control_cost(X[i, j], Y[i, j])
        robust_field[i, j] = simulate_noise_stability(X[i, j], Y[i, j])

# normalize cost
cost_norm = (cost_field - cost_field.min()) / (cost_field.max() - cost_field.min() + 1e-9)

# ============================================================
# 6. PHASE MAP
# ============================================================

phase_map = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        
        c = cost_norm[i, j]
        r = robust_field[i, j]
        
        if r > 0.7 and c < 0.4:
            phase_map[i, j] = 0  # optimal
        elif r > 0.7:
            phase_map[i, j] = 1  # robust but expensive
        elif c < 0.4:
            phase_map[i, j] = 2  # fragile but cheap
        else:
            phase_map[i, j] = 3  # bad region

# ============================================================
# 7. PLOT
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Q1 — Control Cost
im1 = axs[0, 0].contourf(X, Y, cost_norm, levels=30)
axs[0, 0].set_title("Q1 — Control Cost (normalized)")
plt.colorbar(im1, ax=axs[0, 0])

# Q2 — Robustness
im2 = axs[0, 1].contourf(X, Y, robust_field, levels=30)
axs[0, 1].set_title("Q2 — Robustness")
plt.colorbar(im2, ax=axs[0, 1])

# Q3 — Phase Map
cmap = plt.cm.get_cmap("Set1", 4)
im3 = axs[1, 0].imshow(
    phase_map,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap=cmap,
    alpha=0.85,
)
axs[1, 0].set_title("Q3 — Control × Robustness Phase Map")

# Q4 — Overlay
im4 = axs[1, 1].contourf(X, Y, scalar_field(X, Y), levels=30)
axs[1, 1].set_title("Q4 — Field + Phase Overlay")

for ax in axs.flat:
    for c, pos in clusters.items():
        ax.scatter(pos[0], pos[1], color=cluster_colors[c], s=80)
        ax.text(pos[0]+0.2, pos[1]+0.2, c)

plt.tight_layout()

outfile = os.path.join(OUTPUT_DIR, "v35_control_robustness_phase.png")
plt.savefig(outfile, dpi=200)
plt.close()

print(f"Saved: {outfile}")
