"""
NEXAH Experiment Tool
Vortex Topology Map

Purpose
-------
Detect topological phase winding and local vortex-like activity
in the three-layer counterrotation experiment.

Inputs
------
output/phase_history.npy

Outputs
-------
output/vortex_winding_map.png
output/vortex_activity_map.png
output/vortex_topology_report.txt

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python vortex_topology_map.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------
# Load data
# ------------------------------------------------
def load_history():
    path = Path("output/phase_history.npy")
    if not path.exists():
        raise RuntimeError(
            "Missing output/phase_history.npy\n"
            "Run three_layer_counterrotation_longrun.py first."
        )
    return np.load(path)


# ------------------------------------------------
# Split layers
# ------------------------------------------------
def split_layers(history, n_inner=16, n_middle=32, n_outer=16):
    inner = history[:, :n_inner]
    middle = history[:, n_inner:n_inner + n_middle]
    outer = history[:, n_inner + n_middle:n_inner + n_middle + n_outer]
    return inner, middle, outer


# ------------------------------------------------
# Winding number
# ------------------------------------------------
def ring_winding_number(theta_ring):
    """
    Compute total wrapped phase winding around the ring.
    For a clean topological winding this should be near an integer.
    """
    diffs = wrap_angle(np.roll(theta_ring, -1) - theta_ring)
    total = np.sum(diffs)
    k = int(np.rint(total / (2 * np.pi)))
    return k, total, diffs


def scan_winding(layer_history):
    T, N = layer_history.shape
    winding_k = np.zeros(T, dtype=int)
    winding_total = np.zeros(T, dtype=float)
    local_activity = np.zeros((T, N), dtype=float)

    for t in range(T):
        k, total, diffs = ring_winding_number(layer_history[t])
        winding_k[t] = k
        winding_total[t] = total

        # local vortex-like activity:
        # strong local phase jump
        local_activity[t] = np.abs(diffs)

    return winding_k, winding_total, local_activity


# ------------------------------------------------
# Plotting
# ------------------------------------------------
def plot_winding_map(inner_k, middle_k, outer_k):
    winding_mat = np.vstack([inner_k, middle_k, outer_k])

    plt.figure(figsize=(12, 3))
    plt.imshow(
        winding_mat,
        aspect="auto",
        origin="lower",
        cmap="coolwarm"
    )
    plt.yticks([0, 1, 2], ["inner", "middle", "outer"])
    plt.xlabel("time step")
    plt.title("Topological winding number map")
    plt.colorbar(label="winding k")
    plt.tight_layout()
    plt.savefig("output/vortex_winding_map.png", dpi=300)
    plt.show()


def plot_activity_maps(inner_act, middle_act, outer_act):
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    axes[0].imshow(inner_act.T, aspect="auto", origin="lower", cmap="magma")
    axes[0].set_title("Inner shell local vortex activity")
    axes[0].set_ylabel("inner index")

    axes[1].imshow(middle_act.T, aspect="auto", origin="lower", cmap="magma")
    axes[1].set_title("Middle shell local vortex activity")
    axes[1].set_ylabel("middle index")

    axes[2].imshow(outer_act.T, aspect="auto", origin="lower", cmap="magma")
    axes[2].set_title("Outer shell local vortex activity")
    axes[2].set_ylabel("outer index")
    axes[2].set_xlabel("time step")

    plt.tight_layout()
    plt.savefig("output/vortex_activity_map.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Reporting
# ------------------------------------------------
def summarize_winding(name, winding_k):
    vals, counts = np.unique(winding_k, return_counts=True)
    parts = [f"{v}:{c}" for v, c in zip(vals, counts)]
    return [
        f"{name}",
        f"  winding states = {', '.join(parts)}",
        f"  nonzero count  = {int(np.sum(winding_k != 0))}",
        ""
    ]


def write_report(inner_k, middle_k, outer_k,
                 inner_total, middle_total, outer_total):
    lines = []
    lines.append("Vortex Topology Report")
    lines.append("----------------------")
    lines.append("")

    lines += summarize_winding("Inner shell", inner_k)
    lines += summarize_winding("Middle shell", middle_k)
    lines += summarize_winding("Outer shell", outer_k)

    lines.append("Mean total wrapped phase sum")
    lines.append(f"  inner  = {float(np.mean(inner_total)):.6f}")
    lines.append(f"  middle = {float(np.mean(middle_total)):.6f}")
    lines.append(f"  outer  = {float(np.mean(outer_total)):.6f}")
    lines.append("")

    with open("output/vortex_topology_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():
    Path("output").mkdir(exist_ok=True)

    history = load_history()
    inner, middle, outer = split_layers(history)

    inner_k, inner_total, inner_act = scan_winding(inner)
    middle_k, middle_total, middle_act = scan_winding(middle)
    outer_k, outer_total, outer_act = scan_winding(outer)

    plot_winding_map(inner_k, middle_k, outer_k)
    plot_activity_maps(inner_act, middle_act, outer_act)
    write_report(
        inner_k, middle_k, outer_k,
        inner_total, middle_total, outer_total
    )

    print("Vortex topology analysis completed.")
    print("Saved:")
    print("  output/vortex_winding_map.png")
    print("  output/vortex_activity_map.png")
    print("  output/vortex_topology_report.txt")


if __name__ == "__main__":
    main()
