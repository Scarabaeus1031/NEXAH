"""
NEXAH Experiment Tool
Defect–Triad Causality Analyzer

Purpose
-------
Analyze temporal causality between

    • phase defects
    • triadic closure collapse

Hypothesis
----------
Defect birth events are preceded by a local drop in triadic closure.

Outputs
-------
output/defect_triad_causality_lag_curve.png
output/defect_birth_vs_triad_drop_hist.png
output/defect_triad_event_examples.png

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python defect_triad_causality.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------
# Load maps
# ------------------------------------------------
def load_maps():

    defect_map = np.load("output/defect_map.npy")
    triad_map = np.load("output/triadic_closure_map.npy")

    return defect_map, triad_map


# ------------------------------------------------
# Detect defect birth events
# ------------------------------------------------
def defect_birth_events(defect_map):

    T, N = defect_map.shape
    births = []

    for t in range(1, T):

        prev_row = defect_map[t - 1]
        row = defect_map[t]

        new_defects = np.where((row == 1) & (prev_row == 0))[0]

        for i in new_defects:
            births.append((t, i))

    return births


# ------------------------------------------------
# Circular neighborhood
# ------------------------------------------------
def local_ring_window(arr, idx, radius=1):

    N = len(arr)
    vals = []

    for k in range(-radius, radius + 1):
        vals.append(arr[(idx + k) % N])

    return np.array(vals)


# ------------------------------------------------
# Local triadic signal
# ------------------------------------------------
def local_triad_signal(triad_map, t, i, radius=1):

    row = triad_map[t]

    window = local_ring_window(row, i, radius)

    return np.mean(window)


# ------------------------------------------------
# Birth-triggered average
# ------------------------------------------------
def compute_birth_triggered_average(defect_births, triad_map,
                                    lag_before=30, lag_after=10, radius=1):

    curves = []

    T, N = triad_map.shape

    for t0, i0 in defect_births:

        if t0 - lag_before < 0:
            continue

        if t0 + lag_after >= T:
            continue

        curve = []

        for tau in range(-lag_before, lag_after + 1):

            val = local_triad_signal(triad_map, t0 + tau, i0, radius)
            curve.append(val)

        curves.append(curve)

    if len(curves) == 0:
        return None, None

    curves = np.array(curves)

    mean_curve = np.mean(curves, axis=0)

    lags = np.arange(-lag_before, lag_after + 1)

    return lags, mean_curve


# ------------------------------------------------
# Triadic drop values
# ------------------------------------------------
def compute_drop_values(defect_births, triad_map,
                        pre_window=20, post_window=3, radius=1):

    drops = []

    T, N = triad_map.shape

    for t0, i0 in defect_births:

        if t0 - pre_window < 0:
            continue

        if t0 + post_window >= T:
            continue

        pre_vals = []
        post_vals = []

        for t in range(t0 - pre_window, t0):
            pre_vals.append(local_triad_signal(triad_map, t, i0, radius))

        for t in range(t0, t0 + post_window + 1):
            post_vals.append(local_triad_signal(triad_map, t, i0, radius))

        pre_mean = np.mean(pre_vals)
        post_mean = np.mean(post_vals)

        drops.append(pre_mean - post_mean)

    return np.array(drops)


# ------------------------------------------------
# Plot lag curve
# ------------------------------------------------
def plot_lag_curve(lags, mean_curve):

    Path("output").mkdir(exist_ok=True)

    plt.figure(figsize=(9,4))

    plt.plot(lags, mean_curve)

    plt.axvline(0, linestyle="--")

    plt.xlabel("Lag relative to defect birth")
    plt.ylabel("Mean local triadic closure")

    plt.title("Defect-triggered triadic closure average")

    plt.savefig("output/defect_triad_causality_lag_curve.png", dpi=300)

    plt.show()


# ------------------------------------------------
# Plot histogram
# ------------------------------------------------
def plot_drop_hist(drops):

    plt.figure(figsize=(7,4))

    plt.hist(drops, bins=30)

    plt.xlabel("Triadic closure drop before defect birth")
    plt.ylabel("Count")

    plt.title("Defect birth vs triadic closure drop")

    plt.savefig("output/defect_birth_vs_triad_drop_hist.png", dpi=300)

    plt.show()


# ------------------------------------------------
# Plot example events
# ------------------------------------------------
def plot_example_events(defect_births, triad_map,
                        lag_before=20, lag_after=10, radius=1, max_examples=6):

    plt.figure(figsize=(10,5))

    shown = 0

    for t0, i0 in defect_births:

        T, N = triad_map.shape

        if t0 - lag_before < 0:
            continue

        if t0 + lag_after >= T:
            continue

        lags = np.arange(-lag_before, lag_after + 1)

        curve = []

        for tau in lags:

            val = local_triad_signal(triad_map, t0 + tau, i0, radius)
            curve.append(val)

        plt.plot(lags, curve, alpha=0.8)

        shown += 1

        if shown >= max_examples:
            break

    plt.axvline(0, linestyle="--")

    plt.xlabel("Lag relative to defect birth")
    plt.ylabel("Local triadic closure")

    plt.title("Example defect-birth / triad-collapse events")

    plt.savefig("output/defect_triad_event_examples.png", dpi=300)

    plt.show()


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():

    defect_map, triad_map = load_maps()

    births = defect_birth_events(defect_map)

    print("Detected defect births:", len(births))

    lags, mean_curve = compute_birth_triggered_average(
        births,
        triad_map
    )

    drops = compute_drop_values(
        births,
        triad_map
    )

    if lags is None:
        print("No usable events.")
        return

    plot_lag_curve(lags, mean_curve)

    plot_drop_hist(drops)

    plot_example_events(births, triad_map)

    print("Mean triadic drop:", float(np.mean(drops)))
    print("Median triadic drop:", float(np.median(drops)))


if __name__ == "__main__":
    main()
