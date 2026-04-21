import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v7.2 — Stability Map + Chaos Detection
# ============================================================

# ------------------------------------------------------------
# FIELD DEFINITION
# ------------------------------------------------------------
def field(x, y):
    """
    Same field family as v7.1
    radial + rotation
    """
    r = np.sqrt(x**2 + y**2) + 1e-9

    fx = x * (1 - r)
    fy = y * (1 - r)

    fx += -0.5 * y
    fy +=  0.5 * x

    return fx, fy


# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate(x0, y0, steps=200, dt=0.05):
    x, y = x0, y0
    traj = np.zeros((steps, 2), dtype=float)

    for k in range(steps):
        fx, fy = field(x, y)
        x += fx * dt
        y += fy * dt
        traj[k] = (x, y)

    return traj


# ------------------------------------------------------------
# LOCAL INSTABILITY / LYAPUNOV-LIKE SCORE
# ------------------------------------------------------------
def local_instability(x, y, eps=1e-4, steps=200, dt=0.05):
    """
    Compare two nearby trajectories and estimate sensitivity.
    Returns:
        instability_score  ~ log(final_dist / initial_dist)
        final_dist
    """
    traj1 = simulate(x, y, steps=steps, dt=dt)
    traj2 = simulate(x + eps, y + eps, steps=steps, dt=dt)

    d0 = np.sqrt((eps)**2 + (eps)**2)
    d1 = np.linalg.norm(traj1[-1] - traj2[-1])

    score = np.log((d1 + 1e-12) / d0)
    return score, d1


# ------------------------------------------------------------
# TRAJECTORY CLASSIFICATION
# ------------------------------------------------------------
def classify_stability(score):
    """
    Simple threshold-based interpretation.
    """
    if score < -0.5:
        return 0   # very stable
    elif score < 0.5:
        return 1   # stable / neutral
    elif score < 1.5:
        return 2   # sensitive
    else:
        return 3   # chaotic / strongly divergent


# ------------------------------------------------------------
# GRID SETUP
# ------------------------------------------------------------
N = 80
x_vals = np.linspace(-1.5, 1.5, N)
y_vals = np.linspace(-1.5, 1.5, N)

stability_map = np.zeros((N, N))
final_distance_map = np.zeros((N, N))
class_map = np.zeros((N, N))

# optional: representative trajectories
sample_trajs = []

# ------------------------------------------------------------
# COMPUTE MAPS
# ------------------------------------------------------------
for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        score, d1 = local_instability(x, y, eps=1e-4, steps=200, dt=0.05)

        stability_map[j, i] = score
        final_distance_map[j, i] = d1
        class_map[j, i] = classify_stability(score)

# representative trajectories from a few points
sample_points = [
    (-1.2, -1.2),
    (-1.2,  1.2),
    ( 1.2, -1.2),
    ( 1.2,  1.2),
    ( 0.0,  0.0),
    ( 0.4,  0.0),
    ( 0.0,  0.4),
]
for pt in sample_points:
    sample_trajs.append(simulate(pt[0], pt[1], steps=250, dt=0.05))

# ------------------------------------------------------------
# PLOT 1: STABILITY MAP
# ------------------------------------------------------------
plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
im1 = plt.imshow(stability_map, cmap="coolwarm")
plt.title("Stability Map (Lyapunov-like)")
plt.colorbar(im1, label="log(final_dist / initial_dist)")

plt.subplot(2, 2, 2)
im2 = plt.imshow(final_distance_map, cmap="magma")
plt.title("Final Distance Map")
plt.colorbar(im2, label="final trajectory separation")

plt.subplot(2, 2, 3)
im3 = plt.imshow(class_map, cmap="viridis")
plt.title("Stability Classes")
plt.colorbar(im3, label="0=very stable ... 3=chaotic")

plt.subplot(2, 2, 4)
for traj in sample_trajs:
    plt.plot(traj[:, 0], traj[:, 1], alpha=0.8)
plt.title("Representative Trajectories")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.grid(True)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 2: OVERLAY
# ------------------------------------------------------------
plt.figure(figsize=(7, 7))
plt.imshow(stability_map, cmap="coolwarm", origin="lower")
for traj in sample_trajs:
    plt.plot(
        (traj[:, 0] - x_vals.min()) / (x_vals.max() - x_vals.min()) * (N - 1),
        (traj[:, 1] - y_vals.min()) / (y_vals.max() - y_vals.min()) * (N - 1),
        color="white",
        linewidth=1.0,
        alpha=0.8
    )
plt.title("Stability Map with Trajectory Overlay")
plt.colorbar(label="instability score")
plt.show()

# ------------------------------------------------------------
# PRINT SUMMARY
# ------------------------------------------------------------
print("\n=== NEXAH v7.2 Summary ===")
print("stability min:", np.min(stability_map))
print("stability max:", np.max(stability_map))
print("stability mean:", np.mean(stability_map))

unique, counts = np.unique(class_map.astype(int), return_counts=True)
print("\nClass counts:")
for u, c in zip(unique, counts):
    print(f"class {u}: {c}")
