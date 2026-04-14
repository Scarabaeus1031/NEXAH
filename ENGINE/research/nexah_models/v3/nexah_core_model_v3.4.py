# nexah_core_model_v3.4_ieee.py

import numpy as np
import matplotlib.pyplot as plt
import csv


# -----------------------------
# LOAD IEEE DATA
# -----------------------------

def load_ieee_data(filepath):

    t = []
    voltage = []

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row['time']))
            voltage.append(float(row['voltage']))

    t = np.array(t)
    voltage = np.array(voltage)

    return t, voltage


# -----------------------------
# EMBED INTO NEXAH FIELD
# -----------------------------

def build_field_from_voltage(t, voltage, n_nodes=8):

    N = len(t)

    # replicate voltage into nodes
    c = np.tile(voltage, (n_nodes, 1)).T

    # add tiny variation (important!)
    c += 0.01 * np.random.randn(*c.shape)

    # drift = derivative
    v = np.gradient(c, axis=0)

    return c, v


# -----------------------------
# DETECTOR (v3.3)
# -----------------------------

def detect_split_v3(t, c, v):

    coherence = 1 / (1 + np.std(c, axis=1))
    curvature = np.abs(np.gradient(np.mean(c, axis=1)))
    winding = np.abs(np.gradient(np.sign(np.mean(v, axis=1))))

    curvature_n = curvature / (np.max(curvature) + 1e-6)
    winding_n = winding / (np.max(winding) + 1e-6)

    score = (
        0.4 * (1 - coherence)
        + 0.3 * curvature_n
        + 0.3 * winding_n
    )

    # --- FIXES ---
    MIN_TIME = 5.0

    burn_idx = np.where(t < MIN_TIME)[0]
    baseline_mean = np.mean(score[burn_idx])
    baseline_std = np.std(score[burn_idx])

    threshold = baseline_mean + 1.5 * baseline_std

    WINDOW = 20

    for i in range(len(score) - WINDOW):

        if t[i] < MIN_TIME:
            continue

        if np.all(score[i:i+WINDOW] > threshold):
            return t[i]

    return None


def detect_classic(t, voltage):

    threshold = 0.7
    MIN_TIME = 5.0

    for i in range(len(voltage)):
        if t[i] < MIN_TIME:
            continue
        if voltage[i] < threshold:
            return t[i]

    return None


# -----------------------------
# MAIN TEST
# -----------------------------

def run_ieee_test(filepath):

    t, voltage = load_ieee_data(filepath)

    c, v = build_field_from_voltage(t, voltage)

    split_t = detect_split_v3(t, c, v)
    classic_t = detect_classic(t, voltage)

    lead = None
    if split_t and classic_t:
        lead = classic_t - split_t

    print("\nNEXAH v3.4 IEEE result")
    print("-----------------------")
    print(f"split:   {split_t}")
    print(f"classic: {classic_t}")
    print(f"lead:    {lead}")

    # plot
    plt.figure(figsize=(10, 4))
    plt.plot(t, voltage, label="voltage")

    if split_t:
        plt.axvline(split_t, color='green', label="split")

    if classic_t:
        plt.axvline(classic_t, color='red', label="classic")

    plt.axhline(0.7, linestyle="--")

    plt.legend()
    plt.title("NEXAH vs Classical (IEEE Data)")
    plt.show()


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    filepath = "data/ieee_sample.csv"

    run_ieee_test(filepath)
