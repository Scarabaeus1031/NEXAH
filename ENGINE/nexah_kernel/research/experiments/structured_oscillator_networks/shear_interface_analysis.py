"""
NEXAH Experiment Tool
Shear Interface Analysis

Purpose
-------
Measure shear strength and domain width in the three-layer oscillator system.

Inputs
------
output/phase_history.npy

Outputs
-------
output/shear_strength_vs_time.png
output/domain_width_histogram.png
output/domain_drift_estimate.txt
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
        raise RuntimeError("Missing output/phase_history.npy")
    return np.load(path)


# ------------------------------------------------
# Split layers
# ------------------------------------------------
def split_layers(history, n_inner=16, n_middle=32, n_outer=16):
    inner = history[:, :n_inner]
    middle = history[:, n_inner:n_inner+n_middle]
    outer = history[:, n_inner+n_middle:n_inner+n_middle+n_outer]
    return inner, middle, outer


# ------------------------------------------------
# Shear measurement
# ------------------------------------------------
def measure_shear(inner, middle, outer):
    T = inner.shape[0]

    shear_inner_middle = np.zeros(T)
    shear_middle_outer = np.zeros(T)

    for t in range(T):

        phase_inner = np.mean(inner[t])
        phase_middle = np.mean(middle[t])
        phase_outer = np.mean(outer[t])

        shear_inner_middle[t] = abs(wrap_angle(phase_inner - phase_middle))
        shear_middle_outer[t] = abs(wrap_angle(phase_middle - phase_outer))

    return shear_inner_middle, shear_middle_outer


# ------------------------------------------------
# Domain width
# ------------------------------------------------
def domain_widths(layer, threshold=0.45):

    widths = []

    for theta in layer:

        diffs = wrap_angle(np.roll(theta, -1) - theta)
        mask = np.abs(diffs) < threshold

        run = 0
        for m in mask:
            if m:
                run += 1
            else:
                if run > 0:
                    widths.append(run)
                run = 0

        if run > 0:
            widths.append(run)

    return widths


# ------------------------------------------------
# Drift estimate
# ------------------------------------------------
def estimate_drift(layer):

    T, N = layer.shape

    centers = []

    for t in range(T):

        theta = layer[t]
        diffs = wrap_angle(np.roll(theta, -1) - theta)

        domain = np.where(np.abs(diffs) < 0.45)[0]

        if len(domain) > 0:
            centers.append(np.mean(domain))

    centers = np.array(centers)

    if len(centers) < 2:
        return 0

    drift = np.mean(np.diff(centers))

    return drift


# ------------------------------------------------
# Plotting
# ------------------------------------------------
def plot_shear(s1, s2):

    plt.figure(figsize=(10,4))

    plt.plot(s1,label="inner-middle shear")
    plt.plot(s2,label="middle-outer shear")

    plt.title("Shear strength vs time")
    plt.xlabel("time step")
    plt.ylabel("phase difference")

    plt.legend()

    plt.savefig("output/shear_strength_vs_time.png",dpi=300)
    plt.show()


def plot_domain_widths(inner_w,middle_w,outer_w):

    plt.figure(figsize=(10,5))

    plt.hist(inner_w,bins=40,alpha=0.6,label="inner")
    plt.hist(middle_w,bins=40,alpha=0.6,label="middle")
    plt.hist(outer_w,bins=40,alpha=0.6,label="outer")

    plt.title("Domain width distribution")
    plt.xlabel("domain width")
    plt.ylabel("count")

    plt.legend()

    plt.savefig("output/domain_width_histogram.png",dpi=300)
    plt.show()


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():

    history = load_history()

    inner,middle,outer = split_layers(history)

    shear_im, shear_mo = measure_shear(inner,middle,outer)

    inner_w = domain_widths(inner)
    middle_w = domain_widths(middle)
    outer_w = domain_widths(outer)

    drift = estimate_drift(middle)

    plot_shear(shear_im,shear_mo)
    plot_domain_widths(inner_w,middle_w,outer_w)

    with open("output/domain_drift_estimate.txt","w") as f:
        f.write(f"Estimated middle-domain drift per step: {drift}\n")

    print("Shear analysis completed.")
    print("Outputs saved in output/")


if __name__ == "__main__":
    main()
