"""
EXP_01_STABILITY_SEEKING

Goal:
Test whether a simple field-aware controller can
reduce distance to the stability corridor (rift)
compared to an uncontrolled trajectory.

NEXAH Navigation Validation
2026
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Output Directory
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "EXP_01_STABILITY_SEEKING"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"\nOutputs -> {OUTPUT_DIR}")


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
# Plot 1 — Navigation Trajectory
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x_rift,
    y_rift,
    linewidth=3,
    label="Rift"
)

plt.plot(
    xu,
    yu,
    label="Uncontrolled"
)

plt.plot(
    xg,
    yg,
    label="Field Guided"
)

plt.xlabel("x")
plt.ylabel("y")

plt.title(
    "EXP_01 — Stability Seeking"
)

plt.legend()
plt.grid(True)

plt.savefig(
    OUTPUT_DIR / "exp01_navigation_trajectory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 2 — Distance Evolution
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    du,
    label="Uncontrolled"
)

plt.plot(
    dg,
    label="Field Guided"
)

plt.xlabel("Step")
plt.ylabel("Distance to Rift")

plt.title(
    "Distance Reduction"
)

plt.legend()
plt.grid(True)

plt.savefig(
    OUTPUT_DIR / "exp01_distance_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Metrics
# ============================================================

mean_u = np.mean(du)
mean_g = np.mean(dg)

improvement = (
    1 - mean_g / mean_u
) * 100


# ============================================================
# Plot 3 — Summary Dashboard
# ============================================================

fig, axes = plt.subplots(
    3,
    1,
    figsize=(10, 12)
)

# ------------------------------------------------------------
# Panel 1
# ------------------------------------------------------------

axes[0].plot(
    x_rift,
    y_rift,
    linewidth=3,
    label="Rift"
)

axes[0].plot(
    xu,
    yu,
    label="Uncontrolled"
)

axes[0].plot(
    xg,
    yg,
    label="Guided"
)

axes[0].set_title(
    "Trajectory Navigation"
)

axes[0].legend()
axes[0].grid(True)

# ------------------------------------------------------------
# Panel 2
# ------------------------------------------------------------

axes[1].plot(
    du,
    label="Uncontrolled"
)

axes[1].plot(
    dg,
    label="Guided"
)

axes[1].set_title(
    "Distance To Rift"
)

axes[1].legend()
axes[1].grid(True)

# ------------------------------------------------------------
# Panel 3
# ------------------------------------------------------------

axes[2].bar(
    ["Uncontrolled", "Guided"],
    [mean_u, mean_g]
)

axes[2].set_title(
    "Mean Distance Comparison"
)

axes[2].set_ylabel(
    "Distance"
)

axes[2].grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp01_navigation_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Results Report
# ============================================================

report_file = (
    OUTPUT_DIR
    / "exp01_results.txt"
)

with open(report_file, "w") as f:

    f.write(
        "EXP_01 STABILITY SEEKING\n"
    )

    f.write(
        "=" * 40 + "\n\n"
    )

    f.write(
        f"Mean distance uncontrolled: "
        f"{mean_u:.6f}\n"
    )

    f.write(
        f"Mean distance guided: "
        f"{mean_g:.6f}\n"
    )

    f.write(
        f"Distance reduction: "
        f"{improvement:.2f}%\n"
    )


# ============================================================
# Console Output
# ============================================================

print("\nEXP_01 RESULTS")
print("-" * 40)

print(
    f"Mean distance (uncontrolled): "
    f"{mean_u:.4f}"
)

print(
    f"Mean distance (guided): "
    f"{mean_g:.4f}"
)

print(
    f"Distance reduction: "
    f"{improvement:.2f}%"
)

print(
    f"\nSaved to: {OUTPUT_DIR}"
)
