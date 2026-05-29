"""
EXP_01_STABILITY_SEEKING

Goal:
Test whether a simple field-aware controller can
reduce distance to the stability corridor (rift)
compared to an uncontrolled trajectory.

NEXAH Navigation Validation
2026
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Synthetic Rift
# ============================================================

x_rift = np.linspace(-5, 5, 500)
y_rift = np.sin(x_rift)


# ============================================================
# Distance to Rift
# ============================================================

def distance_to_rift(x, y):

    dx = x_rift - x
    dy = y_rift - y

    d = np.sqrt(dx**2 + dy**2)

    idx = np.argmin(d)

    return d[idx], idx


# ============================================================
# Uncontrolled Trajectory
# ============================================================

def simulate_uncontrolled(n_steps=250):

    x = -4.0
    y = 1.5

    xs = []
    ys = []
    ds = []

    for _ in range(n_steps):

        x += 0.05
        y += 0.01 + np.random.normal(0, 0.02)

        d, _ = distance_to_rift(x, y)

        xs.append(x)
        ys.append(y)
        ds.append(d)

    return np.array(xs), np.array(ys), np.array(ds)


# ============================================================
# Field-Guided Trajectory
# ============================================================

def simulate_guided(n_steps=250):

    x = -4.0
    y = 1.5

    xs = []
    ys = []
    ds = []

    for _ in range(n_steps):

        d, idx = distance_to_rift(x, y)

        target_y = y_rift[idx]

        correction = 0.15 * (target_y - y)

        x += 0.05
        y += correction + np.random.normal(0, 0.01)

        d, _ = distance_to_rift(x, y)

        xs.append(x)
        ys.append(y)
        ds.append(d)

    return np.array(xs), np.array(ys), np.array(ds)


# ============================================================
# Run
# ============================================================

xu, yu, du = simulate_uncontrolled()
xg, yg, dg = simulate_guided()


# ============================================================
# Plot 1
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(x_rift, y_rift,
         linewidth=3,
         label="Rift")

plt.plot(xu, yu,
         label="Uncontrolled")

plt.plot(xg, yg,
         label="Field Guided")

plt.xlabel("x")
plt.ylabel("y")

plt.title("EXP_01 — Stability Seeking")

plt.legend()
plt.grid(True)

plt.savefig(
    "exp01_navigation_trajectory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 2
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(du,
         label="Uncontrolled")

plt.plot(dg,
         label="Field Guided")

plt.xlabel("Step")
plt.ylabel("Distance to Rift")

plt.title("Distance Reduction")

plt.legend()
plt.grid(True)

plt.savefig(
    "exp01_distance_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Metrics
# ============================================================

print("\nEXP_01 RESULTS")
print("-" * 40)

print(
    f"Mean distance (uncontrolled): "
    f"{np.mean(du):.4f}"
)

print(
    f"Mean distance (guided): "
    f"{np.mean(dg):.4f}"
)

improvement = (
    1 - np.mean(dg) / np.mean(du)
) * 100

print(
    f"Distance reduction: "
    f"{improvement:.2f}%"
)
