import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ==========================================================
# EXP_05B — Multi Basin Navigation
# ==========================================================

steps = 350

# ----------------------------------------------------------
# Corridor
# ----------------------------------------------------------

x_corridor = np.linspace(-8, 8, steps)

y_corridor = (
    0.9*np.sin(0.7*x_corridor)
    + 0.5*np.sin(1.9*x_corridor)
)

# ----------------------------------------------------------
# Basins
# ----------------------------------------------------------

collapse_center = np.array([5.5, -1.0])
collapse_radius = 2.0

target = np.array([7.0, 1.5])

# ----------------------------------------------------------
# Uncontrolled trajectory
# ----------------------------------------------------------

x_un = np.linspace(-7.0, 7.0, steps)

y_un = (
    np.linspace(4.8, -2.0, steps)
    + 0.15*np.sin(np.linspace(0, 12, steps))
)

# ----------------------------------------------------------
# Guided trajectory
# ----------------------------------------------------------

guided_x = []
guided_y = []

corridor_choice = []

risk_history = []
distance_history = []

current_x = -7.0
current_y = 4.0

for i in range(steps):

    idx = min(i, steps-1)

    cx = x_corridor[idx]
    cy = y_corridor[idx]

    # ----------------------------------------------
    # Collapse distance
    # ----------------------------------------------

    dist = np.linalg.norm(
        np.array([current_x, current_y]) - collapse_center
    )

    distance_history.append(dist)

    # ----------------------------------------------
    # Risk
    # ----------------------------------------------

    risk = max(
        0.0,
        (collapse_radius + 1.5 - dist)
    )

    risk_history.append(risk)

    # ----------------------------------------------
    # Corridor A
    # ----------------------------------------------

    a_x = cx
    a_y = cy

    # ----------------------------------------------
    # Corridor B
    # alternative elevated route
    # ----------------------------------------------

    b_x = cx
    b_y = cy + 2.5

    # ----------------------------------------------
    # Choose safer corridor
    # ----------------------------------------------

    dist_a = np.linalg.norm(
        np.array([a_x, a_y]) - collapse_center
    )

    dist_b = np.linalg.norm(
        np.array([b_x, b_y]) - collapse_center
    )

    if dist_b > dist_a:
        chosen_x = b_x
        chosen_y = b_y
        corridor_choice.append(1)
    else:
        chosen_x = a_x
        chosen_y = a_y
        corridor_choice.append(0)

    # ----------------------------------------------
    # Move
    # ----------------------------------------------

    current_x += 0.25*(chosen_x-current_x)
    current_y += 0.25*(chosen_y-current_y)

    current_x += np.random.normal(0, 0.02)
    current_y += np.random.normal(0, 0.02)

    guided_x.append(current_x)
    guided_y.append(current_y)

guided_x = np.array(guided_x)
guided_y = np.array(guided_y)

# ----------------------------------------------------------
# Metrics
# ----------------------------------------------------------

collapse_entries_un = 0
collapse_entries_guided = 0

inside = False

for x, y in zip(x_un, y_un):

    d = np.linalg.norm(
        np.array([x, y]) - collapse_center
    )

    if d < collapse_radius and not inside:
        collapse_entries_un += 1
        inside = True

    if d >= collapse_radius:
        inside = False

inside = False

for x, y in zip(guided_x, guided_y):

    d = np.linalg.norm(
        np.array([x, y]) - collapse_center
    )

    if d < collapse_radius and not inside:
        collapse_entries_guided += 1
        inside = True

    if d >= collapse_radius:
        inside = False

mean_risk = np.mean(risk_history)
min_dist = np.min(distance_history)

# ----------------------------------------------------------
# Save results
# ----------------------------------------------------------

with open("results_exp05b.txt", "w") as f:

    f.write("EXP_05B MULTI BASIN NAVIGATION\n")
    f.write("========================================\n\n")

    f.write(f"Collapse entries uncontrolled: {collapse_entries_un}\n")
    f.write(f"Collapse entries guided: {collapse_entries_guided}\n")
    f.write(f"Minimum basin distance: {min_dist:.6f}\n")
    f.write(f"Mean risk: {mean_risk:.6f}\n")

    if collapse_entries_guided == 0:
        f.write("Navigation success: YES\n")
    else:
        f.write("Navigation success: NO\n")

# ----------------------------------------------------------
# Figure 1
# ----------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.plot(
    x_corridor,
    y_corridor,
    linewidth=5,
    label="Corridor A"
)

plt.plot(
    x_corridor,
    y_corridor + 2.5,
    linewidth=3,
    linestyle="--",
    label="Corridor B"
)

plt.plot(
    x_un,
    y_un,
    label="Uncontrolled"
)

plt.plot(
    guided_x,
    guided_y,
    label="Guided"
)

circle = plt.Circle(
    collapse_center,
    collapse_radius,
    alpha=0.3,
    color="red"
)

plt.gca().add_patch(circle)

plt.scatter(
    collapse_center[0],
    collapse_center[1],
    s=300,
    color="red",
    label="Collapse Basin"
)

plt.title("EXP_05B — Multi Basin Navigation")
plt.legend()
plt.grid(True)

plt.savefig(
    "exp05b_navigation.png",
    dpi=300,
    bbox_inches="tight"
)

# ----------------------------------------------------------
# Figure 2
# ----------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(distance_history)

plt.axhline(
    collapse_radius,
    linestyle="--"
)

plt.title("Distance To Collapse Basin")
plt.grid(True)

plt.savefig(
    "exp05b_basin_distance.png",
    dpi=300,
    bbox_inches="tight"
)

# ----------------------------------------------------------
# Figure 3
# ----------------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(corridor_choice)

plt.title("Corridor Selection")
plt.yticks([0, 1], ["A", "B"])

plt.grid(True)

plt.savefig(
    "exp05b_basin_selection.png",
    dpi=300,
    bbox_inches="tight"
)

# ----------------------------------------------------------
# Figure 4
# ----------------------------------------------------------

fig, axs = plt.subplots(3, 1, figsize=(12, 12))

axs[0].plot(guided_x, guided_y)
axs[0].set_title("Navigation")

axs[1].plot(distance_history)
axs[1].axhline(collapse_radius, linestyle="--")
axs[1].set_title("Collapse Distance")

axs[2].plot(risk_history)
axs[2].set_title("Risk Evolution")

for ax in axs:
    ax.grid(True)

plt.tight_layout()

plt.savefig(
    "exp05b_summary_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

print("EXP_05B finished.")
