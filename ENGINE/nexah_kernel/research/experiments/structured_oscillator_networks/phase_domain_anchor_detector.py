"""
NEXAH Experiment Tool
Phase Domain Anchor Detector

Purpose
-------
Detect stable phase domains ("plateaus") and anchor positions ("pillars")
in the three-layer counterrotation experiment.

Inputs
------
output/phase_history.npy

Outputs
-------
output/domain_anchor_map.png
output/domain_anchor_histogram.png
output/domain_lifetime_histogram.png
output/domain_anchor_report.txt

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python phase_domain_anchor_detector.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def contiguous_segments(mask):
    """
    Find contiguous True segments in a circular 1D mask.
    Returns list of index lists.
    """
    n = len(mask)
    visited = np.zeros(n, dtype=bool)
    segments = []

    for i in range(n):
        if not mask[i] or visited[i]:
            continue

        seg = []
        j = i

        while mask[j] and not visited[j]:
            visited[j] = True
            seg.append(j)
            j = (j + 1) % n
            if j == i:
                break

        segments.append(seg)

    return segments


def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))


# ------------------------------------------------
# Load history
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
# Infer layer structure
# ------------------------------------------------
def split_layers(history, n_inner=16, n_middle=32, n_outer=16):
    theta_inner = history[:, :n_inner]
    theta_middle = history[:, n_inner:n_inner + n_middle]
    theta_outer = history[:, n_inner + n_middle:n_inner + n_middle + n_outer]
    return theta_inner, theta_middle, theta_outer


# ------------------------------------------------
# Domain detection
# ------------------------------------------------
def local_phase_similarity_mask(theta_ring, threshold=0.45):
    """
    Mark positions where local phase jump to next site is small.
    Smaller threshold => stricter domain detection.
    """
    diffs = wrap_angle(np.roll(theta_ring, -1) - theta_ring)
    return np.abs(diffs) < threshold


def detect_domains_in_ring(theta_ring, threshold=0.45, min_length=3):
    """
    Detect contiguous domains in one ring snapshot.
    Returns list of segments (each segment is a list of indices).
    """
    mask = local_phase_similarity_mask(theta_ring, threshold=threshold)
    segments = contiguous_segments(mask)

    # Convert edge-mask segments into node segments
    node_segments = []
    n = len(theta_ring)

    for seg in segments:
        nodes = list(seg)
        end_node = (seg[-1] + 1) % n
        if end_node not in nodes:
            nodes.append(end_node)

        if len(nodes) >= min_length:
            node_segments.append(sorted(set(nodes)))

    return node_segments


# ------------------------------------------------
# Scan all time steps
# ------------------------------------------------
def scan_domains(layer_history, threshold=0.45, min_length=3):
    """
    Returns:
        domain_map: shape (T, N), counts where domain nodes occur
        anchor_counts: shape (N,), how often node belongs to domain
        domain_lengths: list of domain sizes across time
    """
    T, N = layer_history.shape
    domain_map = np.zeros((T, N), dtype=float)
    anchor_counts = np.zeros(N, dtype=float)
    domain_lengths = []

    for t in range(T):
        theta_ring = layer_history[t]
        domains = detect_domains_in_ring(theta_ring, threshold=threshold, min_length=min_length)

        for seg in domains:
            domain_lengths.append(len(seg))
            for idx in seg:
                domain_map[t, idx] = 1.0
                anchor_counts[idx] += 1.0

    return domain_map, anchor_counts, domain_lengths


# ------------------------------------------------
# Lifetime extraction
# ------------------------------------------------
def extract_anchor_lifetimes(domain_map):
    """
    For each ring index, measure consecutive runs of domain occupancy.
    """
    T, N = domain_map.shape
    lifetimes = []

    for j in range(N):
        run = 0
        for t in range(T):
            if domain_map[t, j] > 0:
                run += 1
            else:
                if run > 0:
                    lifetimes.append(run)
                run = 0
        if run > 0:
            lifetimes.append(run)

    return lifetimes


# ------------------------------------------------
# Plotting
# ------------------------------------------------
def plot_domain_maps(inner_map, middle_map, outer_map):
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    axes[0].imshow(inner_map.T, aspect="auto", origin="lower", cmap="viridis")
    axes[0].set_title("Inner shell domain anchors")
    axes[0].set_ylabel("inner index")

    axes[1].imshow(middle_map.T, aspect="auto", origin="lower", cmap="viridis")
    axes[1].set_title("Middle shell domain anchors")
    axes[1].set_ylabel("middle index")

    axes[2].imshow(outer_map.T, aspect="auto", origin="lower", cmap="viridis")
    axes[2].set_title("Outer shell domain anchors")
    axes[2].set_ylabel("outer index")
    axes[2].set_xlabel("time step")

    plt.tight_layout()
    plt.savefig("output/domain_anchor_map.png", dpi=300)
    plt.show()


def plot_anchor_histograms(inner_counts, middle_counts, outer_counts):
    plt.figure(figsize=(10, 5))

    x1 = np.arange(len(inner_counts))
    x2 = np.arange(len(middle_counts))
    x3 = np.arange(len(outer_counts))

    plt.plot(x1, inner_counts, label="inner")
    plt.plot(x2, middle_counts, label="middle")
    plt.plot(x3, outer_counts, label="outer")

    plt.title("Domain anchor counts by ring index")
    plt.xlabel("ring index")
    plt.ylabel("domain occupancy count")
    plt.legend()

    plt.savefig("output/domain_anchor_histogram.png", dpi=300)
    plt.show()


def plot_lifetime_histogram(inner_lifetimes, middle_lifetimes, outer_lifetimes):
    plt.figure(figsize=(10, 5))

    plt.hist(inner_lifetimes, bins=40, alpha=0.6, label="inner")
    plt.hist(middle_lifetimes, bins=40, alpha=0.6, label="middle")
    plt.hist(outer_lifetimes, bins=40, alpha=0.6, label="outer")

    plt.title("Domain anchor lifetimes")
    plt.xlabel("lifetime (time steps)")
    plt.ylabel("count")
    plt.legend()

    plt.savefig("output/domain_lifetime_histogram.png", dpi=300)
    plt.show()


# ------------------------------------------------
# Reporting
# ------------------------------------------------
def write_report(
    inner_counts,
    middle_counts,
    outer_counts,
    inner_lifetimes,
    middle_lifetimes,
    outer_lifetimes,
):
    def summarize(name, counts, lifetimes):
        return [
            f"{name}",
            f"  max anchor count      = {float(np.max(counts)):.1f}",
            f"  mean anchor count     = {float(np.mean(counts)):.3f}",
            f"  num active anchors    = {int(np.sum(counts > 0))}",
            f"  mean lifetime         = {float(np.mean(lifetimes)):.3f}" if lifetimes else "  mean lifetime         = n/a",
            f"  max lifetime          = {int(np.max(lifetimes))}" if lifetimes else "  max lifetime          = n/a",
            "",
        ]

    lines = []
    lines.append("Phase Domain Anchor Report")
    lines.append("--------------------------")
    lines.append("")

    lines += summarize("Inner shell", inner_counts, inner_lifetimes)
    lines += summarize("Middle shell", middle_counts, middle_lifetimes)
    lines += summarize("Outer shell", outer_counts, outer_lifetimes)

    with open("output/domain_anchor_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():
    Path("output").mkdir(exist_ok=True)

    history = load_history()
    inner_hist, middle_hist, outer_hist = split_layers(history)

    inner_map, inner_counts, inner_lengths = scan_domains(inner_hist, threshold=0.45, min_length=3)
    middle_map, middle_counts, middle_lengths = scan_domains(middle_hist, threshold=0.45, min_length=3)
    outer_map, outer_counts, outer_lengths = scan_domains(outer_hist, threshold=0.45, min_length=3)

    inner_lifetimes = extract_anchor_lifetimes(inner_map)
    middle_lifetimes = extract_anchor_lifetimes(middle_map)
    outer_lifetimes = extract_anchor_lifetimes(outer_map)

    plot_domain_maps(inner_map, middle_map, outer_map)
    plot_anchor_histograms(inner_counts, middle_counts, outer_counts)
    plot_lifetime_histogram(inner_lifetimes, middle_lifetimes, outer_lifetimes)

    write_report(
        inner_counts,
        middle_counts,
        outer_counts,
        inner_lifetimes,
        middle_lifetimes,
        outer_lifetimes,
    )

    print("Domain anchor analysis completed.")
    print("Saved:")
    print("  output/domain_anchor_map.png")
    print("  output/domain_anchor_histogram.png")
    print("  output/domain_lifetime_histogram.png")
    print("  output/domain_anchor_report.txt")


if __name__ == "__main__":
    main()
