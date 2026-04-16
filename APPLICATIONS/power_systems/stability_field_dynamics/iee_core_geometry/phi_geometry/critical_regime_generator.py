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

        # Phase 2: kritischer Übergang (nichtlinear!)
        elif i < 70:
            x = i - 30
            voltage[i] = 0.985 - 0.002 * x - 0.00015 * x**2

        # Phase 3: Collapse
        else:
            x = i - 70
            voltage[i] = max(0.5, 0.8 - 0.02 * x - 0.002 * x**2)

    return t, voltage


# ----------------------------------------
# 2. Drift + Change Score
# ----------------------------------------

def compute_drift(v):
    return np.gradient(v)


def compute_change_score(drift):
    return np.abs(np.gradient(drift))


# ----------------------------------------
# 3. Detection
# ----------------------------------------

def detect_regime(time, voltage):

    drift = compute_drift(voltage)
    score = compute_change_score(drift)

    # Collapse
    collapse_idx = None
    collapse = np.where(voltage < 0.7)[0]
    if len(collapse) > 0:
        collapse_idx = collapse[0]

    # Threshold
    threshold = np.mean(score) + 2 * np.std(score)

    candidates = np.where(score > threshold)[0]

    regime_idx = None
    if len(candidates) > 0:
        regime_idx = candidates[0]

    return drift, score, regime_idx, collapse_idx, threshold


# ----------------------------------------
# 4. Plot
# ----------------------------------------

def plot(time, voltage, drift, score, regime_idx, collapse_idx, threshold):

    plt.figure(figsize=(10, 8))

    # Voltage
    plt.subplot(3,1,1)
    plt.plot(time, voltage, label="Voltage")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    plt.legend()
    plt.title("Voltage")

    # Drift
    plt.subplot(3,1,2)
    plt.plot(time, drift, label="Drift")
    plt.legend()
    plt.title("Drift")

    # Score
    plt.subplot(3,1,3)
    plt.plot(time, score, label="Change Score")
    plt.axhline(threshold, linestyle="--", label="Threshold")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":")

    plt.legend()
    plt.title("Change Score")

    plt.tight_layout()
    plt.show()


# ----------------------------------------
# 5. MAIN
# ----------------------------------------

if __name__ == "__main__":

    time, voltage = generate_critical_voltage()

    drift, score, regime_idx, collapse_idx, threshold = detect_regime(time, voltage)

    print("\n--- CRITICAL SYSTEM TEST ---")

    if regime_idx is not None:
        print(f"Regime change at t = {time[regime_idx]}")
    else:
        print("No regime detected")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")

    if regime_idx is not None and collapse_idx is not None:
        print(f"Lead time = {time[collapse_idx] - time[regime_idx]}")

    plot(time, voltage, drift, score, regime_idx, collapse_idx, threshold)
