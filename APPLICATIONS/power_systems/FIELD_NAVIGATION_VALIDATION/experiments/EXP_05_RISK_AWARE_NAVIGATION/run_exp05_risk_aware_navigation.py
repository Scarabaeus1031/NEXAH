"""
EXP_05_RISK_AWARE_NAVIGATION

Goal:
Navigate along the stability corridor while actively
avoiding collapse regions.

This extends EXP_04B by introducing a repulsive
force away from hazardous basins.

NEXAH Field Navigation Validation
2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Output Folder
# ============================================================

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/"
    "outputs/EXP_05_RISK_AWARE_NAVIGATION"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# Corridor
# ============================================================

x_corr = np.linspace(-8, 8, 800)

y_corr = (
    np.sin(0.8 * x_corr)
    + 0.5 * np.sin(2.2 * x_corr)
)


# ============================================================
# Collapse Basin
# ============================================================

collapse_x = 5.5
collapse_y = -1.0
collapse_radius = 2.0


# ============================================================
# Helpers
# ============================================================

def nearest_corridor(x):

    idx = np.argmin(np.abs(x_corr - x))

    return idx


def corridor_distance(x, y):

    idx = nearest_corridor(x)

    dx = x - x_corr[idx]
    dy = y - y_corr[idx]

    return np.sqrt(dx**2 + dy**2)


def collapse_distance(x, y):

    return np.sqrt(
        (x - collapse_x) ** 2
        + (y - collapse_y) ** 2
    )


# ============================================================
# Uncontrolled
# ============================================================

def simulate_uncontrolled():

    x = -7.0
    y = 4.8

    xs = []
    ys = []

    collapse_d = []

    entries = 0
    inside = False

    for _ in range(350):

        x += 0.04

        y += (
            -0.018
            + np.random.normal(0, 0.03)
        )

        d = collapse_distance(x, y)

        if d < collapse_radius and not inside:

            entries += 1
            inside = True

        if d >= collapse_radius:

            inside = False

        xs.append(x)
        ys.append(y)
        collapse_d.append(d)

    return (
        np.array(xs),
        np.array(ys),
        np.array(collapse_d),
        entries
    )


# ============================================================
# Risk-Aware Controller
# ============================================================

def simulate_risk_aware():

    x = -7.0
    y = 4.8

    xs = []
    ys = []

    collapse_d = []
    repulsion_log = []

    entries = 0
    inside = False

    for _ in range(350):

        idx = nearest_corridor(x)

        target_y = y_corr[idx]

        corridor_force = (
            0.16
            * (target_y - y)
        )

        d = collapse_distance(x, y)

        # ------------------------------------
        # Repulsion Force
        # ------------------------------------

        repulsion_force = 0.0

        if d < 4.0:

            repulsion_force = (
                1.6
                * (y - collapse_y)
                / (d**2 + 0.1)
            )

        control = (
            corridor_force
            + repulsion_force
        )

        x += 0.04

        y += (
            control
            + np.random.normal(0, 0.015)
        )

        d = collapse_distance(x, y)

        if d < collapse_radius and not inside:

            entries += 1
            inside = True

        if d >= collapse_radius:

            inside = False

        xs.append(x)
        ys.append(y)

        collapse_d.append(d)
        repulsion_log.append(repulsion_force)

    return (
        np.array(xs),
        np.array(ys),
        np.array(collapse_d),
        np.array(repulsion_log),
        entries
    )


# ============================================================
# Run
# ============================================================

xu, yu, du, entries_u = simulate_uncontrolled()

xg, yg, dg, repulsion, entries_g = (
    simulate_risk_aware()
)


# ============================================================
# Plot 1 Navigation
# ============================================================

plt.figure(figsize=(10, 7))

plt.plot(
    x_corr,
    y_corr,
    linewidth=5,
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
    label="Risk-Aware Guided"
)

circle = plt.Circle(
    (collapse_x, collapse_y),
    collapse_radius,
    color="red",
    alpha=0.25
)

plt.gca().add_patch(circle)

plt.scatter(
    collapse_x,
    collapse_y,
    s=500,
    c="red",
    label="Collapse Basin"
)

plt.title(
    "EXP_05 — Risk-Aware Navigation"
)

plt.xlabel("x")
plt.ylabel("y")

plt.grid(True)
plt.legend()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp05_navigation.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 2 Collapse Distance
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    du,
    label="Uncontrolled"
)

plt.plot(
    dg,
    label="Risk-Aware Guided"
)

plt.axhline(
    collapse_radius,
    linestyle="--",
    linewidth=3,
    label="Collapse Boundary"
)

plt.title(
    "Distance To Collapse Basin"
)

plt.xlabel("Step")
plt.ylabel("Distance")

plt.grid(True)
plt.legend()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp05_collapse_distance.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Plot 3 Repulsion Force
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(repulsion)

plt.title(
    "Repulsion Force Activation"
)

plt.xlabel("Step")
plt.ylabel("Repulsion Force")

plt.grid(True)

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp05_repulsion_force.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Dashboard
# ============================================================

fig, ax = plt.subplots(
    3,
    1,
    figsize=(12, 18)
)

# Navigation

ax[0].plot(
    x_corr,
    y_corr,
    linewidth=5
)

ax[0].plot(xu, yu)
ax[0].plot(xg, yg)

circle = plt.Circle(
    (collapse_x, collapse_y),
    collapse_radius,
    color="red",
    alpha=0.25
)

ax[0].add_patch(circle)

ax[0].set_title("Navigation")


# Distance

ax[1].plot(du)
ax[1].plot(dg)

ax[1].axhline(
    collapse_radius,
    linestyle="--"
)

ax[1].set_title(
    "Collapse Distance"
)


# Entries

ax[2].bar(
    ["Uncontrolled", "Guided"],
    [entries_u, entries_g]
)

ax[2].set_title(
    "Collapse Entries"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp05_summary_dashboard.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Metrics
# ============================================================

min_u = np.min(du)
min_g = np.min(dg)

risk_reduction = (
    (min_g - min_u)
    / min_u
) * 100

success = (
    entries_g < entries_u
)

# ============================================================
# TXT
# ============================================================

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp05_results.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_05 RISK AWARE NAVIGATION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Collapse entries uncontrolled: "
        f"{entries_u}\n"
    )

    f.write(
        f"Collapse entries guided: "
        f"{entries_g}\n"
    )

    f.write(
        f"Minimum collapse distance uncontrolled: "
        f"{min_u:.6f}\n"
    )

    f.write(
        f"Minimum collapse distance guided: "
        f"{min_g:.6f}\n"
    )

    f.write(
        f"Risk reduction: "
        f"{risk_reduction:.2f}%\n"
    )

    f.write(
        f"Avoidance success: "
        f"{'YES' if success else 'NO'}\n"
    )


# ============================================================
# Console
# ============================================================

print()
print("EXP_05 RESULTS")
print("-" * 40)

print(
    f"Collapse entries uncontrolled: "
    f"{entries_u}"
)

print(
    f"Collapse entries guided: "
    f"{entries_g}"
)

print(
    f"Minimum collapse distance uncontrolled: "
    f"{min_u:.4f}"
)

print(
    f"Minimum collapse distance guided: "
    f"{min_g:.4f}"
)

print(
    f"Risk reduction: "
    f"{risk_reduction:.2f}%"
)

print(
    f"Avoidance success: "
    f"{'YES' if success else 'NO'}"
)

print()
print(
    f"Saved to: {OUTPUT_DIR}"
)
