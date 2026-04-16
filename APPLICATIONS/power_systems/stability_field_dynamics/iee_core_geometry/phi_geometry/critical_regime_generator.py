import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------
# 1. Synthetic Critical System Generator
# ----------------------------------------

def generate_critical_voltage(T=100):

    t = np.arange(T)
    voltage = np.zeros(T)

    for i in range(T):

        # Phase 1: stabil
        if i < 30:
            voltage[i] = 1.0 - 0.0005 * i

        # Phase 2: kritischer Übergang
        elif i < 70:
            x = i - 30
            voltage[i] = 0.985 - 0.002 * x - 0.00015 * x**2

        # Phase 3: Collapse
        else:
            x = i - 70
            voltage[i] = max(0.5, 0.8 - 0.02 * x - 0.002 * x**2)

    return t, voltage


# ----------------------------------------
# 2. Signals
# ----------------------------------------

def compute_drift(v):
    return np.gradient(v)


def compute_dual_score(v):

    drift = np.gradient(v)
    drift_abs = np.abs(drift)

    acc = np.abs(np.gradient(drift))

    # 🔥 Hybrid Signal (wichtig!)
    score = 0.7 * drift_abs + 0.3 * acc

    return drift, acc, score


# ----------------------------------------
# 3. Detection
# ----------------------------------------

def detect_regime(time, voltage):

    drift, acc, score = compute_dual_score(voltage)

    # Collapse
    collapse_idx = None
    collapse = np.where(voltage < 0.7)[0]
    if len(collapse) > 0:
        collapse_idx = collapse[0]

    # 🔥 robuster Threshold
    threshold = np.percentile(score, 90)

    candidates = np.where(score > threshold)[0]

    regime_idx = None
    if len(candidates) > 0:
        regime_idx = candidates[0]

    return drift, acc, score, regime_idx, collapse_idx, threshold


# ----------------------------------------
# 4. Plot
# ----------------------------------------

def plot(time, voltage, drift, acc, score, regime_idx, collapse_idx, threshold):

    plt.figure(figsize=(10, 9))

    # Voltage
    plt.subplot(4,1,1)
    plt.plot(time, voltage, label="Voltage")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    plt.legend()
    plt.title("Voltage")

    # Drift
    plt.subplot(4,1,2)
    plt.plot(time, drift, label="Drift")
    plt.legend()
    plt.title("Drift (dv/dt)")

    # Acceleration
    plt.subplot(4,1,3)
    plt.plot(time, acc, label="Acceleration")
    plt.legend()
    plt.title("Acceleration (d²v/dt²)")

    # Score
    plt.subplot(4,1,4)
    plt.plot(time, score, label="Hybrid Score")
    plt.axhline(threshold, linestyle="--", label="Threshold")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":")

    plt.legend()
    plt.title("Hybrid Detection Score")

    plt.tight_layout()
    plt.show()


# ----------------------------------------
# 5. MAIN
# ----------------------------------------

if __name__ == "__main__":

    time, voltage = generate_critical_voltage()

    drift, acc, score, regime_idx, collapse_idx, threshold = detect_regime(time, voltage)

    print("\n--- CRITICAL SYSTEM TEST (DUAL SIGNAL) ---")

    if regime_idx is not None:
        print(f"Regime change at t = {time[regime_idx]}")
    else:
        print("No regime detected")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")

    if regime_idx is not None and collapse_idx is not None:
        print(f"Lead time = {time[collapse_idx] - time[regime_idx]}")

    print(f"Threshold = {threshold:.6f}")

    plot(time, voltage, drift, acc, score, regime_idx, collapse_idx, threshold)
