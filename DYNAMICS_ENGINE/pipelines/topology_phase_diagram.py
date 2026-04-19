# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_phase_diagram.py

import numpy as np
import itertools


# --------------------------------------------------
# PHASE SCAN CORE
# --------------------------------------------------

def generate_parameter_grid(param_ranges):
    """
    param_ranges = {
        "orbit": [0.2, 0.3],
        "helix": [0.2, 0.4]
    }
    """
    keys = list(param_ranges.keys())
    values = list(param_ranges.values())

    combinations = list(itertools.product(*values))

    grid = []
    for combo in combinations:
        param_set = dict(zip(keys, combo))
        grid.append(param_set)

    return grid


# --------------------------------------------------
# MAIN PHASE DIAGRAM BUILDER
# --------------------------------------------------

def build_phase_diagram(
    param_grid,
    run_simulation_fn,
    pipeline_fn
):
    """
    param_grid: list of parameter dicts
    run_simulation_fn: function(params) → trajectory / points
    pipeline_fn: function(data) → signature, classification
    """

    results = []

    for i, params in enumerate(param_grid):
        print(f"\n--- Running {i+1}/{len(param_grid)} ---")
        print("Params:", params)

        try:
            data = run_simulation_fn(params)

            signature, classification = pipeline_fn(data)

            results.append({
                "params": params,
                "type": classification["type"],
                "confidence": classification["confidence"]
            })

        except Exception as e:
            print("Error:", e)
            continue

    return results


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

def summarize_phase_diagram(results):
    print("\n--- PHASE DIAGRAM SUMMARY ---")

    type_counts = {}

    for r in results:
        t = r["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    for t, count in type_counts.items():
        print(f"{t}: {count}")


def find_stable_regions(results, min_conf=0.5):
    stable = [r for r in results if r["confidence"] >= min_conf]

    print(f"\nStable Regions (conf >= {min_conf}): {len(stable)}")

    for r in stable:
        print(r)

    return stable


# --------------------------------------------------
# SIMPLE VISUALIZATION
# --------------------------------------------------

def plot_phase_diagram_2d(results, x_param, y_param):
    import matplotlib.pyplot as plt

    x = []
    y = []
    colors = []

    type_map = {}
    color_list = ["red", "blue", "green", "orange", "purple", "black"]

    def get_color(t):
        if t not in type_map:
            type_map[t] = color_list[len(type_map) % len(color_list)]
        return type_map[t]

    for r in results:
        px = r["params"].get(x_param)
        py = r["params"].get(y_param)

        if px is None or py is None:
            continue

        x.append(px)
        y.append(py)
        colors.append(get_color(r["type"]))

    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, c=colors)

    plt.xlabel(x_param)
    plt.ylabel(y_param)
    plt.title("Topology Phase Diagram")

    # legend
    for t, c in type_map.items():
        plt.scatter([], [], c=c, label=t)
    plt.legend()

    plt.show()


# --------------------------------------------------
# TEMPLATE PIPELINE (DU ERSETZT DAS)
# --------------------------------------------------

def example_run_simulation(params):
    """
    PLACEHOLDER – replace with your engine
    """

    # dummy spiral depending on param
    t = np.linspace(0, 20, 1000)
    scale = params.get("orbit", 0.3)

    x = np.cos(t) * (1 + scale * t)
    y = np.sin(t) * (1 + scale * t)

    return np.stack([x, y], axis=1)


def example_pipeline(data):
    """
    PLACEHOLDER – replace with real pipeline
    """

    # FAKE OUTPUT (replace!!)
    signature = {
        "degree_dist": {1: 0.5, 2: 0.5},
        "avg_loop": 10,
        "std_loop": 2,
        "avg_channel": 8,
        "std_channel": 1,
        "angle_profile": {120: 0.3}
    }

    classification = {
        "type": "Loop-Dominant (Shell / Orbital System)",
        "confidence": 0.7
    }

    return signature, classification


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    param_ranges = {
        "orbit": [0.2, 0.3, 0.4],
        "helix": [0.2, 0.3]
    }

    grid = generate_parameter_grid(param_ranges)

    results = build_phase_diagram(
        grid,
        example_run_simulation,
        example_pipeline
    )

    summarize_phase_diagram(results)
    plot_phase_diagram_2d(results, "orbit", "helix")
