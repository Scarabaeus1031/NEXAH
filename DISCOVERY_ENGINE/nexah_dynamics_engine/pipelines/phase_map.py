import numpy as np
import matplotlib.pyplot as plt

from pipelines.real_pipeline import run_pipeline

# 🔥 META ANALYSIS IMPORTS
from analysis.phase_transition_detector import analyze_phase_space
from analysis.phase_gradient import compute_phase_gradient
from analysis.topology_diversity import compute_diversity

# 🔥 FLOW FIELD
from analysis.flow_field import compute_flow_field, normalize_flow

# 🔥 TRANSITION OVERLAY
from analysis.transition_overlay import compute_transition_overlay

# 🔥 BASIN DETECTOR
from analysis.basin_detector import detect_basins, compute_basin_strength

# 🔥 META FIELD
from analysis.meta_field import compute_meta_field, extract_meta_zones


# --------------------------------------------------
# PARAM GRID
# --------------------------------------------------

orbit_values = np.linspace(0.1, 0.5, 8)
helix_values = np.linspace(0.0, 0.5, 8)


# --------------------------------------------------
# RUN GRID
# --------------------------------------------------

results = []
phase_grid = []

rotation_grid = []
strength_grid = []
angle_grid = []

for i, orbit in enumerate(orbit_values):

    row = []
    rot_row = []
    strength_row = []
    angle_row = []

    for j, helix in enumerate(helix_values):

        params = {
            "orbit": float(orbit),
            "helix": float(helix)
        }

        print(f"\n--- GRID {i},{j} ---")
        res = run_pipeline(params, run_id=f"grid_v2_{i}_{j}", visualize=False)

        results.append(res)

        # -----------------------------
        # CLASSIFICATION
        # -----------------------------

        label = res["classification"]

        if "Loop" in label:
            row.append(0)
        elif "Network" in label:
            row.append(1)
        else:
            row.append(2)

        # -----------------------------
        # ROTATION
        # -----------------------------

        rot = res.get("rotation", "NONE")
        strength = res.get("rotation_strength", 0.0)

        if rot == "CCW":
            rot_row.append(1)
        elif rot == "CW":
            rot_row.append(-1)
        else:
            rot_row.append(0)

        strength_row.append(float(strength))

        # -----------------------------
        # ANGLE
        # -----------------------------

        angle_data = res.get("angle_data", {})
        dominant_angle = angle_data.get("dominant_angle", 0.0)

        angle_row.append(float(dominant_angle))

    phase_grid.append(row)
    rotation_grid.append(rot_row)
    strength_grid.append(strength_row)
    angle_grid.append(angle_row)


# --------------------------------------------------
# TO NUMPY
# --------------------------------------------------

phase_grid = np.array(phase_grid)
rotation_grid = np.array(rotation_grid)
strength_grid = np.array(strength_grid)
angle_grid = np.array(angle_grid)


# --------------------------------------------------
# META ANALYSIS
# --------------------------------------------------

print("\n==============================")
print("PHASE TRANSITION ANALYSIS")
print("==============================")

transitions = analyze_phase_space(results)

gradient = compute_phase_gradient(phase_grid)
diversity = compute_diversity(results, phase_grid.shape)


# --------------------------------------------------
# FLOW FIELD
# --------------------------------------------------

flow_x, flow_y = compute_flow_field(phase_grid)
flow_x, flow_y = normalize_flow(flow_x, flow_y)


# --------------------------------------------------
# BASINS
# --------------------------------------------------

basins = detect_basins(flow_x, flow_y)
basin_strength = compute_basin_strength(flow_x, flow_y)


# --------------------------------------------------
# TRANSITION OVERLAY
# --------------------------------------------------

transition_overlay = compute_transition_overlay(
    phase_grid,
    rotation_grid,
    angle_grid
)


# --------------------------------------------------
# META FIELD (MASTER)
# --------------------------------------------------

meta_field = compute_meta_field(
    gradient,
    transition_overlay,
    basin_strength,
    flow_x,
    flow_y,
    rotation_grid
)

hot_zones, stable_zones = extract_meta_zones(meta_field)


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def setup_axes(title):
    plt.xticks(range(len(helix_values)), [round(v, 2) for v in helix_values])
    plt.yticks(range(len(orbit_values)), [round(v, 2) for v in orbit_values])
    plt.xlabel("helix")
    plt.ylabel("orbit")
    plt.title(title)


# 1 Phase Map
plt.figure(figsize=(8, 6))
plt.imshow(phase_grid, origin="lower", aspect="auto")
setup_axes("Topology Phase Map")
plt.colorbar()

# 2 Rotation
plt.figure(figsize=(8, 6))
plt.imshow(rotation_grid, origin="lower", aspect="auto")
setup_axes("Rotation Field")
plt.colorbar()

# 3 Strength
plt.figure(figsize=(8, 6))
plt.imshow(strength_grid, origin="lower", aspect="auto")
setup_axes("Rotation Strength")
plt.colorbar()

# 4 Gradient
plt.figure(figsize=(8, 6))
plt.imshow(gradient, origin="lower", aspect="auto")
setup_axes("Phase Gradient")
plt.colorbar()

# 5 Diversity
plt.figure(figsize=(8, 6))
plt.imshow(diversity, origin="lower", aspect="auto")
setup_axes("Topology Diversity")
plt.colorbar()

# 6 Angle
plt.figure(figsize=(8, 6))
plt.imshow(angle_grid, origin="lower", aspect="auto")
setup_axes("Dominant Angle")
plt.colorbar()

# 7 Flow
plt.figure(figsize=(8, 6))
X, Y = np.meshgrid(
    np.arange(len(helix_values)),
    np.arange(len(orbit_values))
)
plt.quiver(X, Y, flow_x, flow_y, scale=20)
setup_axes("Flow Field")

# 8 Transition
plt.figure(figsize=(8, 6))
plt.imshow(transition_overlay, origin="lower", aspect="auto")
setup_axes("Transition Map")
plt.colorbar()

# 9 Basins
plt.figure(figsize=(8, 6))
plt.imshow(basins, origin="lower", aspect="auto")
setup_axes("Basins (Eye of Storm)")

# 10 Meta Field
plt.figure(figsize=(8, 6))
plt.imshow(meta_field, origin="lower", aspect="auto")
setup_axes("META FIELD")
plt.colorbar()

# 11 Hot Zones
plt.figure(figsize=(8, 6))
plt.imshow(hot_zones, origin="lower", aspect="auto")
setup_axes("HOT ZONES")

# 12 Stable Zones
plt.figure(figsize=(8, 6))
plt.imshow(stable_zones, origin="lower", aspect="auto")
setup_axes("STABLE ZONES")

plt.show()

# 🔥 EXPORT RESULTS
def get_results():
    return results
