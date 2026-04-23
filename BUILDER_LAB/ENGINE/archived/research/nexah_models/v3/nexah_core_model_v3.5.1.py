# nexah_core_model_v3.5.1.py

import numpy as np
import matplotlib.pyplot as plt
import csv

# ----------------------------
# helpers
# ----------------------------

def zscore(x):
    x = np.array(x)
    return (x - np.mean(x)) / (np.std(x) + 1e-8)

# ----------------------------
# load IEEE-like data
# ----------------------------

def load_ieee_csv(path="data/ieee_sample.csv"):
    t, v = [], []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row["time"]))
            v.append(float(row["voltage"]))
    return np.array(t), np.array(v)

# ----------------------------
# classical detection
# ----------------------------

def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None

# ----------------------------
# NEXAH core v3.5.1 (FIXED)
# ----------------------------

def nexah_detection(t, voltage):

    dv = np.gradient(voltage)
    d2v = np.gradient(dv)

    curvature = np.abs(d2v)
    lyapunov_proxy = np.abs(dv)

    curvature_z = zscore(curvature)
    lyapunov_z = zscore(lyapunov_proxy)

    # 🔥 FIX 1: collapse only when falling
    collapse_signal = np.where(
        dv < 0,
        (-dv) + np.abs(d2v),
        0
    )
    collapse_z = zscore(collapse_signal)

    composite = curvature_z + lyapunov_z

    # 🔥 FIX 2: stronger thresholds
    composite_th = 2.5
    collapse_th = 2.8

    # 🔥 FIX 3: warmup
    MIN_TIME = 10

    split_time = None

    for i in range(len(t)):

        if t[i] < MIN_TIME:
            continue

        if (
            composite[i] > composite_th
            or collapse_z[i] > collapse_th
        ):
            split_time = t[i]
            break

    return split_time, {
        "curvature_z": curvature_z,
        "lyapunov_z": lyapunov_z,
        "collapse_z": collapse_z,
        "composite": composite
    }

# ----------------------------
# main
# ----------------------------

def run():

    t, voltage = load_ieee_csv()

    split, metrics = nexah_detection(t, voltage)
    classic = classical_detection(voltage, t)

    lead = None
    if split is not None and classic is not None:
        lead = classic - split

    print("\nNEXAH v3.5.1 IEEE result")
    print("------------------------")
    print(f"split:   {split}")
    print(f"classic: {classic}")
    print(f"lead:    {lead}")

    # ----------------------------
    # plot
    # ----------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(t, voltage, label="voltage")

    if split is not None:
        plt.axvline(split, color="green", label="split")

    if classic is not None:
        plt.axvline(classic, color="red", label="classic")

    plt.axhline(0.7, linestyle="--", alpha=0.5)

    plt.title("NEXAH v3.5.1 – IEEE Detection")
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("voltage")

    plt.show()

# ----------------------------

if __name__ == "__main__":
    run()
