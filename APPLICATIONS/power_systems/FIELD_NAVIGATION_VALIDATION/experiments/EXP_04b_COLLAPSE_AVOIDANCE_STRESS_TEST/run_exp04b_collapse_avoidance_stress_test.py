"""
run_exp04b_collapse_avoidance_stress_test.py

EXP_04B — Collapse Avoidance Stress Test

Goal:
Force the uncontrolled trajectory into a collapse basin
and evaluate whether a field-guided controller can
avoid collapse through corridor navigation.

NEXAH Field Navigation Validation
2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "..",
        "outputs",
        "EXP_04B_COLLAPSE_AVOIDANCE_STRESS_TEST"
    )
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CORRIDOR
# ============================================================

x_corridor = np.linspace(-8, 8, 800)

y_corridor = (
    np.sin(0.7 * x_corridor)
    + 0.5 * np.sin(1.8 * x_corridor)
)


# ============================================================
# COLLAPSE BASIN
# ============================================================

collapse_x = 5.5
collapse_y = -1.0
collapse_radius = 2.0


# ============================================================
# HELPERS
# ============================================================

def corridor_distance(x, y):

    dx = x_corridor - x
    dy = y_corridor - y

    d = np.sqrt(dx**2 + dy**2)

    idx = np.argmin(d)

    return d[idx], idx


def collapse_distance(x, y):

    return np.sqrt(
        (x - collapse_x) ** 2
        + (y - collapse_y) ** 2
    )


# ============================================================
# UNCONTROLLED
# ============================================================

def simulate_uncontrolled(n_steps=350):

    x = -7.0
    y = 4.9

    xs = []
    ys = []

    collapse_d = []
    entries = 0

    inside = False

    for _ in range(n_steps):

        x += 0.04

        # intentional drift toward collapse basin
        y -= 0.018

        y += np.random.normal(0, 0.03)

        d_col = collapse_distance(x, y)

        now_inside = d_col < collapse_radius

        if now_inside and not inside:
            entries += 1

        inside = now_inside

        xs.append(x)
        ys.append(y)

        collapse_d.append(d_col)

    return (
        np.array(xs),
        np.array(ys),
        np.array(collapse_d),
        entries
    )


# ============================================================
# GUIDED
# ============================================================

def simulate_guided(n_steps=350):

    x = -7.0
    y = 4.5

    xs = []
    ys = []

    collapse_d = []
    entries = 0

    inside = False

    gain = 0.22

    for _ in range(n_steps):

        _, idx = corridor_distance(x, y)

        target_y = y_corridor[idx]

        correction = gain * (target_y - y)

        x += 0.04

        y += correction

        y += np.random.normal(0, 0.02)

        d_col = collapse_distance(x, y)

        now_inside = d_col < collapse_radius

        if now_inside and not inside:
            entries += 1

        inside = now_inside

        xs.append(x)
        ys.append(y)

        collapse_d.append(d_col)

    return (
        np.array(xs),
        np.array(ys),
        np.array(collapse_d),
        entries
    )


# ============================================================
# RUN
# ============================================================

xu, yu, du, entries_u = simulate_uncontrolled()

xg, yg, dg, entries_g = simulate_guided()


# ============================================================
# METRICS
# ============================================================

min_u = np.min(du)
min_g = np.min(dg)

risk_reduction = (
    1.0 - (min_u / min_g)
) * 100

avoidance_success = (
    entries_u > entries_g
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(12, 8))

plt.plot(
    x_corridor,
    y_corridor,
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
    label="Guided"
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
    s=350,
    c="red",
    label="Collapse Basin"
)

plt.title(
    "EXP_04B — Collapse Avoidance Stress Test"
)

plt.xlabel("x")
plt.ylabel("y")

plt.grid(True)
plt.legend()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp04b_navigation.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    du,
    label="Uncontrolled"
)

plt.plot(
    dg,
    label="Guided"
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
        "exp04b_collapse_distance.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# VISUAL 3
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["Uncontrolled", "Guided"],
    [entries_u, entries_g]
)

plt.ylabel("Collapse Entries")

plt.title(
    "Collapse Basin Entries"
)

plt.grid(True, axis="y")

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp04b_basin_entries.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# VISUAL 4
# ============================================================

fig, ax = plt.subplots(
    3,
    1,
    figsize=(12, 15)
)

# navigation

ax[0].plot(
    x_corridor,
    y_corridor,
    linewidth=4
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

# distance

ax[1].plot(du)
ax[1].plot(dg)

ax[1].axhline(
    collapse_radius,
    linestyle="--"
)

ax[1].set_title(
    "Collapse Distance"
)

# entries

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
        "exp04b_summary_dashboard.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# TXT REPORT
# ============================================================

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp04b_results.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_04B COLLAPSE AVOIDANCE STRESS TEST\n"
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
        f"{'YES' if avoidance_success else 'NO'}\n"
    )


# ============================================================
# RESULTS
# ============================================================

print("\nEXP_04B RESULTS")
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
    f"{'YES' if avoidance_success else 'NO'}"
)

print(f"\nSaved to:\n{OUTPUT_DIR}")
