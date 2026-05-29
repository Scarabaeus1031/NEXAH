"""
EXP_03_CORRIDOR_RETENTION

Goal:
Test whether a field-guided controller can
remain attached to a stability corridor under
repeated disturbances.

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
    / "EXP_03_CORRIDOR_RETENTION"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"\nOutputs -> {OUTPUT_DIR}")


# ============================================================
# Corridor
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
# Retention Controller
# ============================================================

def simulate_retention(n_steps=350):

    x = -7.0
    y = 5.5

    xs = []
    ys = []
    ds = []

    disturbance_steps = [
        100,
        180,
        260
    ]

    recovery_times = []

    recovering = False
    recovery_start = None

    for step in range(n_steps):

        d, idx = distance_to_corridor(x, y)

        target_y = y_corridor[idx]

        if d > 2.0:
            gain = 0.05
        elif d > 0.8:
            gain = 0.12
        else:
            gain = 0.20

        correction = gain * (
            target_y - y
        )

        x += 0.04

        y += (
            correction
            + np.random.normal(0, 0.015)
        )

        # --------------------------------
        # Disturbance Events
        # --------------------------------

        if step in disturbance_steps:

            y += np.random.choice(
                [-1.5, 1.5]
            )

            recovering = True
            recovery_start = step

        # --------------------------------
        # Recovery Tracking
        # --------------------------------

        d, _ = distance_to_corridor(x, y)

        if recovering and d < 0.30:

            recovery_times.append(
                step - recovery_start
            )

            recovering = False

        xs.append(x)
        ys.append(y)
        ds.append(d)

    return (
        np.array(xs),
        np.array(ys),
        np.array(ds),
        disturbance_steps,
        recovery_times
    )


# ============================================================
# Run
# ============================================================

(
    xg,
    yg,
    dg,
    disturbance_steps,
    recovery_times
) = simulate_retention()


# ============================================================
# Metrics
# ============================================================

mean_distance = np.mean(dg)

max_distance = np.max(dg)

occupancy = (
    np.sum(dg < 0.5)
    / len(dg)
) * 100

mean_recovery = (
    np.mean(recovery_times)
    if len(recovery_times) > 0
    else 0
)


# ============================================================
# Figure 1
# Corridor Retention
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x_corridor,
    y_corridor,
    linewidth=3,
    label="Corridor"
)

plt.plot(
    xg,
    yg,
    label="Guided Trajectory"
)

for step in disturbance_steps:

    if step < len(xg):

        plt.scatter(
            xg[step],
            yg[step],
            s=100,
            color="red"
        )

plt.title(
    "EXP_03 — Corridor Retention"
)

plt.xlabel("x")
plt.ylabel("y")

plt.legend()
plt.grid(True)

plt.savefig(
    OUTPUT_DIR
    / "exp03_corridor_retention.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Figure 2
# Distance Recovery
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    dg,
    label="Distance"
)

for step in disturbance_steps:

    plt.axvline(
        step,
        linestyle="--"
    )

plt.title(
    "Distance Recovery After Disturbances"
)

plt.xlabel("Step")
plt.ylabel("Distance")

plt.grid(True)

plt.legend()

plt.savefig(
    OUTPUT_DIR
    / "exp03_distance_recovery.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Figure 3
# Recovery Statistics
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    range(
        len(recovery_times)
    ),
    recovery_times
)

plt.title(
    "Recovery Time per Disturbance"
)

plt.xlabel(
    "Disturbance Event"
)

plt.ylabel(
    "Recovery Steps"
)

plt.grid(True)

plt.savefig(
    OUTPUT_DIR
    / "exp03_recovery_statistics.png",
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

axes[0].plot(
    x_corridor,
    y_corridor,
    linewidth=3
)

axes[0].plot(
    xg,
    yg
)

axes[0].set_title(
    "Corridor Retention"
)

axes[0].grid(True)

axes[1].plot(dg)

for step in disturbance_steps:

    axes[1].axvline(
        step,
        linestyle="--"
    )

axes[1].set_title(
    "Distance Recovery"
)

axes[1].grid(True)

axes[2].bar(
    [
        "Mean Dist",
        "Max Dist",
        "Recovery"
    ],
    [
        mean_distance,
        max_distance,
        mean_recovery
    ]
)

axes[2].set_title(
    "Retention Metrics"
)

axes[2].grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR
    / "exp03_summary_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# TXT Report
# ============================================================

with open(
    OUTPUT_DIR
    / "exp03_results.txt",
    "w"
) as f:

    f.write(
        "EXP_03 CORRIDOR RETENTION\n"
    )

    f.write(
        "=" * 40 + "\n\n"
    )

    f.write(
        f"Mean distance: "
        f"{mean_distance:.6f}\n"
    )

    f.write(
        f"Max distance: "
        f"{max_distance:.6f}\n"
    )

    f.write(
        f"Corridor occupancy: "
        f"{occupancy:.2f}%\n"
    )

    f.write(
        f"Mean recovery time: "
        f"{mean_recovery:.2f}\n"
    )


# ============================================================
# Console
# ============================================================

print("\nEXP_03 RESULTS")
print("-" * 40)

print(
    f"Mean distance: "
    f"{mean_distance:.4f}"
)

print(
    f"Max distance: "
    f"{max_distance:.4f}"
)

print(
    f"Corridor occupancy: "
    f"{occupancy:.2f}%"
)

print(
    f"Mean recovery time: "
    f"{mean_recovery:.2f}"
)

print(
    f"\nSaved to: {OUTPUT_DIR}"
)
