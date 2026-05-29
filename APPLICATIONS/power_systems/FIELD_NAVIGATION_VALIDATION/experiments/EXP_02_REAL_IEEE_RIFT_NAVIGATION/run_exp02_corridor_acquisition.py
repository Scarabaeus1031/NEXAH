"""
EXP_02_CORRIDOR_ACQUISITION

Goal:
Test whether a field-aware controller can
discover, acquire, and lock onto a stability corridor
when starting far away from the structure.

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
    / "EXP_02_CORRIDOR_ACQUISITION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"\nOutputs -> {OUTPUT_DIR}")


# ============================================================
# Synthetic Stability Corridor
# ============================================================

x_corridor = np.linspace(-8, 8, 800)

y_corridor = (
    1.2 * np.sin(0.6 * x_corridor)
    + 0.3 * np.cos(2.0 * x_corridor)
)


# ============================================================
# Distance Function
# ============================================================

def distance_to_corridor(x, y):

    dx = x_corridor - x
    dy = y_corridor - y

    d = np.sqrt(dx**2 + dy**2)

    idx = np.argmin(d)

    return d[idx], idx


# ============================================================
# Uncontrolled Search
# ============================================================

def simulate_uncontrolled(n_steps=350):

    x = -7.0
    y = 6.0

    xs = []
    ys = []
    ds = []

    for _ in range(n_steps):

        x += 0.04

        y += (
            0.015
            + np.random.normal(0, 0.03)
        )

        d, _ = distance_to_corridor(x, y)

        xs.append(x)
        ys.append(y)
        ds.append(d)

    return (
        np.array(xs),
        np.array(ys),
        np.array(ds)
    )


# ============================================================
# Corridor Acquisition Controller
# ============================================================

def simulate_guided(n_steps=350):

    x = -7.0
    y = 6.0

    xs = []
    ys = []
    ds = []

    acquisition_step = None

    for step in range(n_steps):

        d, idx = distance_to_corridor(x, y)

        target_y = y_corridor[idx]

        # -------------------------
        # Search Phase
        # -------------------------

        if d > 2.0:

            gain = 0.05

        # -------------------------
        # Acquisition Phase
        # -------------------------

        elif d > 0.8:

            gain = 0.12

        # -------------------------
        # Corridor Following
        # -------------------------

        else:

            gain = 0.20

            if acquisition_step is None:
                acquisition_step = step

        correction = gain * (
            target_y - y
        )

        x += 0.04

        y += (
            correction
            + np.random.normal(0, 0.015)
        )

        d, _ = distance_to_corridor(x, y)

        xs.append(x)
        ys.append(y)
        ds.append(d)

    return (
        np.array(xs),
        np.array(ys),
        np.array(ds),
        acquisition_step
    )


# ============================================================
# Run
# ============================================================

xu, yu, du = simulate_uncontrolled()

xg, yg, dg, acquisition_step = (
    simulate_guided()
)


# ============================================================
# Distance Field
# ============================================================

grid_x = np.linspace(-8, 8, 120)

grid_y = np.linspace(-8, 8, 120)

Z = np.zeros(
    (len(grid_y), len(grid_x))
)

for iy, yy in enumerate(grid_y):

    for ix, xx in enumerate(grid_x):

        d, _ = distance_to_corridor(
            xx,
            yy
        )

        Z[iy, ix] = d


# ============================================================
# Figure 1
# Corridor Acquisition
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x_corridor,
    y_corridor,
    linewidth=3,
    label="Corridor"
)

plt.plot(
    xu,
    yu,
    label="Uncontrolled"
)

plt.plot(
    xg,
    yg,
    label="Guided"
)

plt.scatter(
    [xg[0]],
    [yg[0]],
    s=100,
    label="Start"
)

plt.title(
    "EXP_02 — Corridor Acquisition"
)

plt.xlabel("x")
plt.ylabel("y")

plt.legend()
plt.grid(True)

plt.savefig(
    OUTPUT_DIR
    / "exp02_corridor_acquisition.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Figure 2
# Distance Evolution
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    du,
    label="Uncontrolled"
)

plt.plot(
    dg,
    label="Guided"
)

if acquisition_step is not None:

    plt.axvline(
        acquisition_step,
        linestyle="--",
        label="Acquisition"
    )

plt.title(
    "Distance Evolution"
)

plt.xlabel("Step")
plt.ylabel("Distance")

plt.legend()
plt.grid(True)

plt.savefig(
    OUTPUT_DIR
    / "exp02_distance_evolution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Figure 3
# Distance Field
# ============================================================

plt.figure(figsize=(10, 8))

plt.imshow(
    Z,
    extent=[
        grid_x.min(),
        grid_x.max(),
        grid_y.min(),
        grid_y.max()
    ],
    origin="lower",
    aspect="auto"
)

plt.colorbar(
    label="Distance to Corridor"
)

plt.plot(
    x_corridor,
    y_corridor,
    linewidth=2
)

plt.plot(
    xg,
    yg,
    linewidth=2
)

plt.title(
    "Corridor Acquisition in Distance Field"
)

plt.xlabel("x")
plt.ylabel("y")

plt.savefig(
    OUTPUT_DIR
    / "exp02_distance_field.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Figure 4
# Summary Dashboard
# ============================================================

fig, axes = plt.subplots(
    3,
    1,
    figsize=(10, 12)
)

# --------------------------

axes[0].plot(
    x_corridor,
    y_corridor,
    linewidth=3,
    label="Corridor"
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

axes[0].legend()
axes[0].grid(True)

axes[0].set_title(
    "Corridor Acquisition"
)

# --------------------------

axes[1].plot(
    du,
    label="Uncontrolled"
)

axes[1].plot(
    dg,
    label="Guided"
)

axes[1].legend()
axes[1].grid(True)

axes[1].set_title(
    "Distance Evolution"
)

# --------------------------

axes[2].bar(
    ["Uncontrolled", "Guided"],
    [
        np.mean(du),
        np.mean(dg)
    ]
)

axes[2].set_title(
    "Mean Distance Comparison"
)

axes[2].grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp02_summary_dashboard.png",
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
# Report
# ============================================================

report_file = (
    OUTPUT_DIR
    / "exp02_results.txt"
)

with open(report_file, "w") as f:

    f.write(
        "EXP_02 CORRIDOR ACQUISITION\n"
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

    if acquisition_step is not None:

        f.write(
            f"Acquisition step: "
            f"{acquisition_step}\n"
        )


# ============================================================
# Console Output
# ============================================================

print("\nEXP_02 RESULTS")
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

if acquisition_step is not None:

    print(
        f"Acquisition step: "
        f"{acquisition_step}"
    )

print(
    f"\nSaved to: {OUTPUT_DIR}"
)
