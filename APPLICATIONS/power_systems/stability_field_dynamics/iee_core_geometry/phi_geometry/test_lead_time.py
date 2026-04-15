import numpy as np
import csv
import os
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. CSV Laden
# ----------------------------------------

def load_csv(filepath):
    time = []
    voltage = []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time.append(float(row["time"]))
            voltage.append(float(row["voltage"]))

    return np.array(time), np.array(voltage)


# ----------------------------------------
# 2. Acceleration + Smoothing
# ----------------------------------------

def compute_acceleration(v, window=5):
    dv = np.diff(v)
    ddv = np.diff(dv)

    ddv = np.concatenate([[0, 0], ddv])

    kernel = np.ones(window) / window
    ddv_smooth = np.convolve(ddv, kernel, mode='same')

    return np.abs(ddv_smooth)


# ----------------------------------------
# 3. Analyse + Detection
# ----------------------------------------

def detect(time, voltage, collapse_threshold=0.7):

    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    acc = compute_acceleration(voltage)

    threshold = np.mean(acc) + 1.0 * np.std(acc)
    threshold = max(threshold, 1e-4)

    min_idx = 2

    abs_indices = np.where(acc > threshold)[0]
    abs_indices = abs_indices[abs_indices >= min_idx]

    rel_indices = np.array([])
    if np.max(acc) > 1e-6:
        rel_threshold = 0.5 * np.max(acc)
        rel_indices = np.where(acc > rel_threshold)[0]
        rel_indices = rel_indices[rel_indices >= min_idx]

    if collapse_idx is not None:
        abs_indices = abs_indices[abs_indices < collapse_idx]
        rel_indices = rel_indices[rel_indices < collapse_idx]

    combined = np.unique(np.concatenate([abs_indices, rel_indices]))

    # 🔥 Zone Filter (wichtig!)
    start = int(0.1 * len(time))
    end = int(0.9 * len(time))
    combined = combined[(combined >= start) & (combined <= end)]

    phi_idx = None
    if len(combined) > 0:
        phi_idx = combined[np.argmax(acc[combined])]

    return collapse_idx, phi_idx, acc, threshold


# ----------------------------------------
# 4. Plot
# ----------------------------------------

def plot_result(time, voltage, acc, collapse_idx, phi_idx, filename):

    plt.figure(figsize=(10, 6))

    # Spannung
    plt.subplot(2, 1, 1)
    plt.plot(time, voltage, label="Voltage")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    if phi_idx is not None:
        plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.title("Voltage Trajectory")
    plt.legend()
    plt.grid()

    # Acceleration
    plt.subplot(2, 1, 2)
    plt.plot(time, acc, label="Acceleration")

    if phi_idx is not None:
        plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.title("Acceleration")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ----------------------------------------
# 5. RUN
# ----------------------------------------

if __name__ == "__main__":

    base_path = "APPLICATIONS/power_systems/stability_field_dynamics/data/"
    output_path = "APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/phi_geometry/plots/"

    os.makedirs(output_path, exist_ok=True)

    test_files = [
        "ieee_linear.csv",
        "ieee_accelerated.csv",
        "ieee_noisy.csv",
        "ieee_delayed.csv"
    ]

    for file in test_files:

        filepath = os.path.join(base_path, file)

        print("\n==============================")
        print(f"Processing: {file}")
        print("==============================")

        if not os.path.exists(filepath):
            print("File not found:", filepath)
            continue

        time, voltage = load_csv(filepath)

        collapse_idx, phi_idx, acc, threshold = detect(time, voltage)

        out_file = os.path.join(output_path, file.replace(".csv", ".png"))

        plot_result(time, voltage, acc, collapse_idx, phi_idx, out_file)

        print("Saved plot to:", out_file)
