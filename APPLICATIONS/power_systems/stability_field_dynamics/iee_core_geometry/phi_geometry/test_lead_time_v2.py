import numpy as np
import csv
import os
import matplotlib.pyplot as plt

# ----------------------------------------
# CSV
# ----------------------------------------

def load_csv(filepath):
    time, voltage = [], []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time.append(float(row["time"]))
            voltage.append(float(row["voltage"]))

    return np.array(time), np.array(voltage)


# ----------------------------------------
# Features
# ----------------------------------------

def compute_features(v):

    dv = np.diff(v, prepend=v[0])
    ddv = np.diff(dv, prepend=dv[0])

    # smoothing
    kernel = np.ones(5) / 5
    ddv = np.convolve(ddv, kernel, mode='same')

    return np.abs(ddv), np.abs(dv)


# ----------------------------------------
# Detection
# ----------------------------------------

def detect_phi_split(time, voltage, collapse_threshold=0.7):

    acc, slope = compute_features(voltage)

    # adaptive threshold
    threshold = np.mean(acc) + 2.0 * np.std(acc)

    # ignore early noise
    start_idx = int(0.15 * len(time))

    indices = np.where(acc > threshold)[0]
    indices = indices[indices > start_idx]

    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]
        indices = indices[indices < collapse_idx]

    phi_idx = None
    if len(indices) > 0:
        phi_idx = indices[0]

    return phi_idx, collapse_idx, acc, threshold


# ----------------------------------------
# Plot
# ----------------------------------------

def plot(time, voltage, acc, threshold, phi_idx, collapse_idx, filename):

    plt.figure(figsize=(10,6))

    plt.subplot(2,1,1)
    plt.plot(time, voltage, label="Voltage")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    if phi_idx is not None:
        plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.legend()
    plt.grid()

    plt.subplot(2,1,2)
    plt.plot(time, acc, label="Acceleration")
    plt.axhline(threshold, linestyle="--", label="Threshold")

    if phi_idx is not None:
        plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ----------------------------------------
# RUN
# ----------------------------------------

if __name__ == "__main__":

    base_path = "APPLICATIONS/power_systems/stability_field_dynamics/data/"
    out_path = "APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/phi_geometry/plots/"

    os.makedirs(out_path, exist_ok=True)

    files = [
        "ieee_linear.csv",
        "ieee_accelerated.csv",
        "ieee_noisy.csv",
        "ieee_delayed.csv"
    ]

    for file in files:

        path = os.path.join(base_path, file)

        print("\n==============================")
        print(f"Testing: {file}")
        print("==============================")

        time, voltage = load_csv(path)

        phi_idx, collapse_idx, acc, threshold = detect_phi_split(time, voltage)

        print("\n--- RESULTS ---")

        if collapse_idx is not None:
            print(f"Collapse at t = {time[collapse_idx]}")

        if phi_idx is not None:
            print(f"Phi-Split at t = {time[phi_idx]}")
            print(f"Lead Time = {time[collapse_idx] - time[phi_idx]}")
        else:
            print("No Phi-Split detected")

        print(f"Threshold = {threshold:.6f}")

        plot_file = os.path.join(out_path, file.replace(".csv", "_final.png"))

        plot(time, voltage, acc, threshold, phi_idx, collapse_idx, plot_file)

        print("Saved:", plot_file)
