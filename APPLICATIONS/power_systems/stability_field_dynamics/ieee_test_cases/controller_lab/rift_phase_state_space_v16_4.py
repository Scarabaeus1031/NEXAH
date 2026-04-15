# rift_phase_state_space_v16_4.py

import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export/rift_extraction"


def load_v16_3_results():
    # reuse saved arrays if needed later
    from rift_phase_state_space_v16_3 import load_data, run_state_model_v16_3

    traj, _ = load_data()
    results = run_state_model_v16_3(traj)
    return results


def extract_branches(results):
    phi_w = results["phi_wrapped"]
    branch = results["branch"]

    mask_0 = branch == 0
    mask_1 = branch == 1

    return phi_w[mask_0], phi_w[mask_1]


def plot_dual_pentagon(phi0, phi1):
    plt.figure(figsize=(7, 7))

    # map to unit circle
    x0 = np.cos(phi0)
    y0 = np.sin(phi0)

    x1 = np.cos(phi1)
    y1 = np.sin(phi1)

    plt.scatter(x0, y0, color="blue", label="Pentagon A (branch 0)", alpha=0.7)
    plt.scatter(x1, y1, color="red", label="Pentagon B (branch 1)", alpha=0.7)

    # connect points (structure emerges!)
    plt.plot(x0, y0, color="blue", alpha=0.4)
    plt.plot(x1, y1, color="red", alpha=0.4)

    # origin = cut center
    plt.scatter([0], [0], color="black", s=80, label="Cut / Threshold")

    plt.gca().set_aspect("equal")
    plt.title("V16.4 Dual Pentagon Split (Pre/Post Cut)")
    plt.legend()
    plt.grid(True)

    path = os.path.join(BASE_DIR, "v16_4_dual_pentagon.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_intersection_field(phi0, phi1):
    plt.figure(figsize=(7, 7))

    # overlay difference
    x0 = np.cos(phi0)
    y0 = np.sin(phi0)

    x1 = np.cos(phi1)
    y1 = np.sin(phi1)

    # difference vectors
    dx = x1[:len(x0)] - x0[:len(x1)]
    dy = y1[:len(x0)] - y0[:len(x1)]

    plt.quiver(
        x0[:len(dx)],
        y0[:len(dy)],
        dx,
        dy,
        angles='xy',
        scale_units='xy',
        scale=1,
        color="purple",
        alpha=0.5
    )

    plt.scatter(x0, y0, color="blue", alpha=0.4)
    plt.scatter(x1, y1, color="red", alpha=0.4)

    plt.scatter([0], [0], color="black", s=100)

    plt.title("V16.4 Intersection Field (Pentagon Transfer)")
    plt.gca().set_aspect("equal")
    plt.grid(True)

    path = os.path.join(BASE_DIR, "v16_4_intersection_field.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def main():
    results = load_v16_3_results()

    phi0, phi1 = extract_branches(results)

    plot_dual_pentagon(phi0, phi1)
    plot_intersection_field(phi0, phi1)

    print("V16.4 Dual Pentagon DONE")


if __name__ == "__main__":
    main()
