import numpy as np
import matplotlib.pyplot as plt
import csv


# =========================
# HELPERS
# =========================

def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if w <= 1:
        return x
    kernel = np.ones(w) / w
    return np.convolve(x, kernel, mode="same")


def load_ieee_csv(path="data/ieee_sample.csv"):
    t, v = [], []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row["time"]))
            v.append(float(row["voltage"]))
    return np.array(t), np.array(v)


def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# =========================
# NEXAH v4 CORE
# =========================

def nexah_v4_detect(t, voltage, baseline_end=50.0, deviation_th=3.0):
    dv = np.gradient(voltage, t)
    d2v = np.gradient(dv, t)

    v_s = moving_average(voltage, 7)
    dv_s = moving_average(dv, 7)
    d2v_s = moving_average(d2v, 7)

    X = np.column_stack([v_s, dv_s, d2v_s])

    idx = np.where(t < baseline_end)[0]
    X0 = X[idx]

    mu = np.mean(X0, axis=0)
    cov = np.cov(X0.T) + 1e-6 * np.eye(3)
    cov_inv = np.linalg.inv(cov)

    diff = X - mu
    dist = np.sqrt(np.einsum("ij,jk,ik->i", diff, cov_inv, diff))
    dist_s = moving_average(dist, 9)

    base_mean = np.mean(dist_s[idx])
    base_std = np.std(dist_s[idx]) + 1e-8
    deviation_z = moving_average((dist_s - base_mean) / base_std, 9)

    # detection
    split = None
    for i in range(len(t)):
        if t[i] < 10:
            continue

        if voltage[i] < 0.95 and deviation_z[i] > deviation_th:
            split = t[i]
            break

    return split


# =========================
# v4.1 TEST LAYER
# =========================

def run_v41():
    t, voltage = load_ieee_csv()

    classic = classical_detection(voltage, t)

    print("\n=== NEXAH v4.1 Robustness Test ===\n")

    leads = []

    for i in range(30):
        noise = np.random.normal(0, 0.002, size=len(voltage))
        v_noisy = voltage + noise

        split = nexah_v4_detect(t, v_noisy)

        if split is not None and classic is not None:
            lead = classic - split
            leads.append(lead)
            print(f"run {i:02d} | split={split:.2f} | lead={lead:.2f}")
        else:
            print(f"run {i:02d} | split=None")

    leads = np.array(leads)

    print("\n--- Summary ---")
    print(f"mean lead: {np.mean(leads):.2f}s")
    print(f"std lead:  {np.std(leads):.2f}s")
    print(f"min lead:  {np.min(leads):.2f}s")
    print(f"max lead:  {np.max(leads):.2f}s")
    print(f"success rate: {len(leads)}/30")


# =========================
# PARAMETER SWEEP
# =========================

def parameter_sweep():
    t, voltage = load_ieee_csv()
    classic = classical_detection(voltage, t)

    print("\n=== Parameter Sweep ===\n")

    for deviation_th in [2.5, 3.0, 3.5]:
        for baseline_end in [40, 50, 60]:
            split = nexah_v4_detect(
                t, voltage,
                baseline_end=baseline_end,
                deviation_th=deviation_th
            )

            if split is not None:
                lead = classic - split
                print(f"th={deviation_th:.1f} | base={baseline_end} → lead={lead:.2f}")
            else:
                print(f"th={deviation_th:.1f} | base={baseline_end} → no split")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    run_v41()
    parameter_sweep()
