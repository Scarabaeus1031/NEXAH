"""
EXP_04_COLLAPSE_AVOIDANCE

Goal:
Test whether a field-guided controller can prevent
entry into a collapse basin by actively steering
the trajectory away from dangerous regions.

NEXAH Navigation Validation
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
    "outputs/EXP_04_COLLAPSE_AVOIDANCE"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# Corridor
# ============================================================

x_corr = np.linspace(-8, 8, 800)

y_corr = (
    np.sin(0.7 * x_corr)
    + 0.5 * np.cos(1.8 * x_corr)
)


# ============================================================
# Collapse Basin
# ============================================================

collapse_x = 6.0
collapse_y = -3.0
collapse_radius = 1.5


# ============================================================
# Helpers
# ============================================================

def distance_to_corridor(x, y):

    dx = x_corr - x
    dy = y_corr - y

    d = np.sqrt(dx**2 + dy**2)

    idx = np.argmin(d)

    return d[idx], idx


def distance_to_collapse(x, y):

    return np.sqrt(
        (x - collapse_x) ** 2
        + (y - collapse_y) ** 2
    )


# ============================================================
# Uncontrolled
# ============================================================

def simulate_uncontrolled():

    x = -7
    y = 5

    xs = []
    ys = []

    collapse_hits = 0
    min_dist = 999

    for _ in range(350):

        x += 0.04

        y += (
            -0.02
            + np.random.normal(0, 0.03)
        )

        dcol = distance_to_collapse(x, y)

        min_dist = min(min_dist, dcol)

        if dcol < collapse_radius:
            collapse_hits += 1

        xs.append(x)
        ys.append(y)

    return (
        np.array(xs),
        np.array(ys),
        collapse_hits,
        min_dist,
    )


# ============================================================
# Guided
# ============================================================

def simulate_guided():

    x = -7
    y = 5

    xs = []
    ys = []

    collapse_hits = 0
    min_dist = 999

    collapse_distances = []

    for _ in range(350):

        dcorr, idx = distance_to_corridor(x, y)

        target_y = y_corr[idx]

        corridor_force = (
            0.15 * (target_y - y)
        )

        dcol = distance_to_collapse(x, y)

        collapse_distances.append(dcol)

        repulsion = 0

        if dcol < 3.0:

            repulsion = (
                1.5
                * (3.0 - dcol)
                / 3.0
            )

        x += 0.04

        y += (
            corridor_force
            + repulsion
            + np.random.normal(0, 0.01)
        )

        min_dist = min(min_dist, dcol)

        if dcol < collapse_radius:
            collapse_hits += 1

        xs.append(x)
        ys.append(y)

    return (
        np.array(xs),
        np.array(ys),
        collapse_hits,
        min_dist,
        np.array(collapse_distances),
    )


# ============================================================
# Run
# ============================================================

xu, yu, hits_u, min_u = simulate_uncontrolled()

(
    xg,
    yg,
    hits_g,
    min_g,
    risk_g,
) = simulate_guided()


# ============================================================
# Visual 1
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.plot(
    x_corr,
    y_corr,
    linewidth=4,
    label="Corridor"
)

circle = plt.Circle(
    (collapse_x, collapse_y),
    collapse_radius,
    color="red",
    alpha=0.3,
)

ax.add_patch(circle)

ax.plot(
    xu,
    yu,
    label="Uncontrolled"
)

ax.plot(
    xg,
    yg,
    label="Guided"
)

ax.scatter(
    collapse_x,
    collapse_y,
    s=150,
    color="red",
    label="Collapse Basin"
)

ax.legend()
ax.grid(True)

ax.set_title(
    "EXP_04 — Collapse Avoidance"
)

plt.savefig(
    f"{OUTPUT_DIR}/exp04_collapse_navigation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Visual 2
# ============================================================

risk_u = [
    distance_to_collapse(
        xu[i],
        yu[i]
    )
    for i in range(len(xu))
]

plt.figure(figsize=(10, 5))

plt.plot(
    risk_u,
    label="Uncontrolled"
)

plt.plot(
    risk_g,
    label="Guided"
)

plt.axhline(
    collapse_radius,
    linestyle="--",
)

plt.title(
    "Distance To Collapse Basin"
)

plt.xlabel("Step")
plt.ylabel("Distance")

plt.legend()
plt.grid(True)

plt.savefig(
    f"{OUTPUT_DIR}/exp04_collapse_distance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Visual 3
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["Uncontrolled", "Guided"],
    [hits_u, hits_g]
)

plt.ylabel("Collapse Entries")

plt.title(
    "Collapse Basin Entries"
)

plt.savefig(
    f"{OUTPUT_DIR}/exp04_collapse_risk.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Visual 4
# ============================================================

fig, axs = plt.subplots(
    3,
    1,
    figsize=(10, 12)
)

axs[0].plot(
    x_corr,
    y_corr,
    linewidth=3
)
axs[0].plot(xu, yu)
axs[0].plot(xg, yg)
axs[0].set_title(
    "Navigation"
)

axs[1].plot(risk_u)
axs[1].plot(risk_g)
axs[1].axhline(
    collapse_radius,
    linestyle="--"
)
axs[1].set_title(
    "Collapse Distance"
)

axs[2].bar(
    ["Uncontrolled", "Guided"],
    [hits_u, hits_g]
)
axs[2].set_title(
    "Collapse Entries"
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/exp04_summary_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Results
# ============================================================

risk_reduction = 0

if min_u > 0:
    risk_reduction = (
        (min_g - min_u)
        / min_u
    ) * 100

with open(
    f"{OUTPUT_DIR}/exp04_results.txt",
    "w",
) as f:

    f.write(
        "EXP_04 COLLAPSE AVOIDANCE\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"Collapse entries uncontrolled: {hits_u}\n"
    )

    f.write(
        f"Collapse entries guided: {hits_g}\n"
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
        f"{'YES' if hits_g == 0 else 'NO'}\n"
    )

print("\nEXP_04 RESULTS")
print("-" * 40)

print(
    f"Collapse entries uncontrolled: {hits_u}"
)

print(
    f"Collapse entries guided: {hits_g}"
)

print(
    f"Minimum distance uncontrolled: "
    f"{min_u:.4f}"
)

print(
    f"Minimum distance guided: "
    f"{min_g:.4f}"
)

print(
    f"Avoidance success: "
    f"{'YES' if hits_g == 0 else 'NO'}"
)

print(f"\nSaved to: {OUTPUT_DIR}")
