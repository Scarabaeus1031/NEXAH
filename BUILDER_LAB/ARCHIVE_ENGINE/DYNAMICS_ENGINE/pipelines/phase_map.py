import numpy as np
import matplotlib.pyplot as plt

from pipelines.real_pipeline import run_pipeline

from analysis.phase_transition_detector import analyze_phase_space
from analysis.phase_gradient import compute_phase_gradient
from analysis.topology_diversity import compute_diversity

from analysis.flow_field import compute_flow_field, normalize_flow
from analysis.transition_overlay import compute_transition_overlay
from analysis.basin_detector import detect_basins, compute_basin_strength
from analysis.meta_field import compute_meta_field, extract_meta_zones


# --------------------------------------------------
# PARAM GRID
# --------------------------------------------------

orbit_values = np.linspace(0.1, 0.5, 8)
helix_values = np.linspace(0.0, 0.5, 8)


# --------------------------------------------------
# GLOBAL STORAGE
# --------------------------------------------------

results = []


# --------------------------------------------------
# MAIN RUN FUNCTION
# --------------------------------------------------

def run_phase_map():

    global results

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

            # CLASSIFICATION
            label = res["classification"]

            if "Loop" in label:
                row.append(0)
            elif "Network" in label:
                row.append(1)
            else:
                row.append(2)

            # ROTATION
            rot = res.get("rotation", "NONE")
            strength = res.get("rotation_strength", 0.0)

            if rot == "CCW":
                rot_row.append(1)
            elif rot == "CW":
                rot_row.append(-1)
            else:
                rot_row.append(0)

            strength_row.append(float(strength))

            # ANGLE
            angle_data = res.get("angle_data", {})
            dominant_angle = angle_data.get("dominant_angle", 0.0)

            angle_row.append(float(dominant_angle))

        phase_grid.append(row)
        rotation_grid.append(rot_row)
        strength_grid.append(strength_row)
        angle_grid.append(angle_row)

    # NUMPY
    phase_grid_np = np.array(phase_grid)
    rotation_grid_np = np.array(rotation_grid)
    strength_grid_np = np.array(strength_grid)
    angle_grid_np = np.array(angle_grid)

    # ANALYSIS
    gradient = compute_phase_gradient(phase_grid_np)
    diversity = compute_diversity(results, phase_grid_np.shape)

    flow_x, flow_y = compute_flow_field(phase_grid_np)
    flow_x, flow_y = normalize_flow(flow_x, flow_y)

    basins = detect_basins(flow_x, flow_y)
    basin_strength = compute_basin_strength(flow_x, flow_y)

    transition_overlay = compute_transition_overlay(
        phase_grid_np,
        rotation_grid_np,
        angle_grid_np
    )

    meta_field = compute_meta_field(
        gradient,
        transition_overlay,
        basin_strength,
        flow_x,
        flow_y,
        rotation_grid_np
    )

    hot_zones, stable_zones = extract_meta_zones(meta_field)

    # PLOTS (optional behalten)
    plt.figure(figsize=(6, 5))
    plt.imshow(meta_field, origin="lower")
    plt.title("META FIELD")
    plt.colorbar()

    plt.show()

    return results


# --------------------------------------------------
# EXPORT FUNCTION
# --------------------------------------------------

def get_results():
    return results


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    run_phase_map()
