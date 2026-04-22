import os
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================

N_RUNS = 50
GRID_RES = 200

OUTPUT_DIR = "ENGINE/analysis/field_decomposition/outputs/extract_attractor_statistics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# =========================
# FIELD DEFINITION (copy aus deinem System)
# =========================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad_field(x, y, eps=1e-4):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2)

    r2 = p - clusters["C2"]
    d2 = np.linalg.norm(r2) + 1e-9
    v += 0.6 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2)/(2*1.6**2))

    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2)/(2*1.3**2))

    return v

def combined_field(x, y):
    return grad_field(x, y) + rotational_field(x, y)

# =========================
# FIXPOINT SEARCH (approx)
# =========================

def find_low_force_points(n_samples=500):
    points = []

    xs = np.random.uniform(8, 15, n_samples)
    ys = np.random.uniform(23, 29, n_samples)

    for x, y in zip(xs, ys):
        f = combined_field(x, y)
        mag = np.linalg.norm(f)

        if mag < 0.05:
            points.append([x, y])

    return np.array(points)

# =========================
# RUN SAMPLING
# =========================

all_points = []

for i in range(N_RUNS):
    pts = find_low_force_points()
    if len(pts) > 0:
        all_points.append(pts)

if len(all_points) == 0:
    print("No attractor points found.")
    exit()

all_points = np.vstack(all_points)

# =========================
# STATISTICS
# =========================

mean = np.mean(all_points, axis=0)
std = np.std(all_points, axis=0)

print("\n--- ATTRACTOR STATISTICS ---")
print(f"Samples: {len(all_points)}")
print(f"Mean: {mean}")
print(f"Std: {std}")

# =========================
# FRACTIONAL ANALYSIS
# =========================

frac_x = all_points[:, 0] % 1
frac_y = all_points[:, 1] % 1

print("\n--- FRACTIONAL PARTS ---")
print(f"Mean frac X: {np.mean(frac_x):.4f}")
print(f"Mean frac Y: {np.mean(frac_y):.4f}")

# =========================
# SAVE DATA
# =========================

np.save(os.path.join(OUTPUT_DIR, "all_points.npy"), all_points)

with open(os.path.join(OUTPUT_DIR, "stats.txt"), "w") as f:
    f.write(f"mean: {mean}\n")
    f.write(f"std: {std}\n")
    f.write(f"mean_frac_x: {np.mean(frac_x)}\n")
    f.write(f"mean_frac_y: {np.mean(frac_y)}\n")

# =========================
# PLOTS
# =========================

plt.figure(figsize=(6,6))
plt.scatter(all_points[:,0], all_points[:,1], s=10, alpha=0.4)
plt.scatter(mean[0], mean[1], c="red", s=100)
plt.title("Attractor Sampling")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig(os.path.join(OUTPUT_DIR, "attractor_cloud.png"), dpi=150)
plt.close()

plt.figure(figsize=(6,4))
plt.hist(frac_x, bins=50, alpha=0.6, label="frac x")
plt.hist(frac_y, bins=50, alpha=0.6, label="frac y")
plt.legend()
plt.title("Fractional Distribution")
plt.savefig(os.path.join(OUTPUT_DIR, "fractional_hist.png"), dpi=150)
plt.close()

print(f"\nSaved to: {OUTPUT_DIR}")
