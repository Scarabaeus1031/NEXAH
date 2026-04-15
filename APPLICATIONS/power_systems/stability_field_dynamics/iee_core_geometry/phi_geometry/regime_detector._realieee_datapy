import pandapower as pp
import pandapower.networks as pn
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------
# 1. IEEE Netz laden
# ----------------------------------------

def load_network():
    net = pn.case9()  # klein starten (IEEE 9-Bus)
    return net


# ----------------------------------------
# 2. "Stress-Test" Simulation
# ----------------------------------------

def simulate_voltage_drop(net, steps=50):

    voltages = []

    for t in range(steps):

        # künstliche Last-Erhöhung
        scale = 1 + 0.02 * t

        net.load["p_mw"] *= scale

        try:
            pp.runpp(net)
            v = net.res_bus.vm_pu.values.mean()
        except:
            v = 0.5  # Collapse

        voltages.append(v)

    return np.array(voltages)


# ----------------------------------------
# 3. Drift + Change Score
# ----------------------------------------

def compute_drift(v):
    return np.gradient(v)


def compute_change_score(drift):
    return np.abs(np.gradient(drift))


# ----------------------------------------
# 4. Detection
# ----------------------------------------

def detect_regime(time, voltage):

    drift = compute_drift(voltage)
    score = compute_change_score(drift)

    # Collapse
    collapse_idx = None
    collapse = np.where(voltage < 0.7)[0]
    if len(collapse) > 0:
        collapse_idx = collapse[0]

    # Threshold (robust)
    threshold = np.mean(score) + 2 * np.std(score)

    candidates = np.where(score > threshold)[0]

    regime_idx = None
    if len(candidates) > 0:
        regime_idx = candidates[0]

    return drift, score, regime_idx, collapse_idx


# ----------------------------------------
# 5. Plot
# ----------------------------------------

def plot(time, voltage, drift, score, regime_idx, collapse_idx):

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

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":")

    plt.legend()
    plt.title("Change Score")

    plt.tight_layout()
    plt.show()


# ----------------------------------------
# 6. MAIN
# ----------------------------------------

if __name__ == "__main__":

    net = load_network()

    voltage = simulate_voltage_drop(net)
    time = np.arange(len(voltage))

    drift, score, regime_idx, collapse_idx = detect_regime(time, voltage)

    print("\n--- REAL IEEE TEST ---")

    if regime_idx is not None:
        print(f"Regime change at t = {time[regime_idx]}")
    else:
        print("No regime detected")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")

    if regime_idx is not None and collapse_idx is not None:
        print(f"Lead time = {time[collapse_idx] - time[regime_idx]}")

    plot(time, voltage, drift, score, regime_idx, collapse_idx)
