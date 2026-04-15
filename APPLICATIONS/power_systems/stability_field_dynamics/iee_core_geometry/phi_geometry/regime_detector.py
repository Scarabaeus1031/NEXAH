import numpy as np
import csv
import os
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. CSV laden
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
# 2. Glättung
# ----------------------------------------

def smooth(x, window=7):
    if window < 2:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


# ----------------------------------------
# 3. Features
# ----------------------------------------

def compute_features(time, voltage, smooth_window=7):
    dt = np.gradient(time)

    drift = np.gradient(voltage, time)           # dv/dt
    drift_s = smooth(drift, smooth_window)

    curvature = np.gradient(drift_s, time)      # d²v/dt²
    curvature_s = smooth(curvature, smooth_window)

    return drift, drift_s, curvature, curvature_s


# ----------------------------------------
# 4. Regime-Detektion
# ----------------------------------------

def detect_regime_change(time, voltage, collapse_threshold=0.7):
    drift, drift_s, curvature, curvature_s = compute_features(time, voltage)

    # Collapse
    collapse_idx = None
    collapse_candidates = np.where(voltage < collapse_threshold)[0]
    if len(collapse_candidates) > 0:
        collapse_idx = collapse_candidates[0]

    # Suchbereich: Anfang und Ende nicht überbewerten
    start_idx = max(3, int(0.10 * len(time)))
    end_idx = len(time) - 3
    if collapse_idx is not None:
        end_idx = min(end_idx, collapse_idx - 1)

    search_idx = np.arange(start_idx, end_idx + 1)

    # 1) Drift-Minimum = stärkster negativer Zug
    drift_min_local = np.argmin(drift_s[search_idx])
    drift_min_idx = search_idx[drift_min_local]

    # 2) Danach den ersten robusten Wendebereich suchen:
    #    curvature_s wird nach dem Minimum wieder positiv / weniger negativ
    post_idx = np.arange(drift_min_idx, end_idx + 1)

    # adaptive curvature threshold
    curv_abs = np.abs(curvature_s[search_idx])
    curv_thr = np.mean(curv_abs) + 0.5 * np.std(curv_abs)

    regime_idx = None
    for i in post_idx:
        # robust: curvature deutlich aktiv und drift beginnt sich zu entspannen
        if (
            abs(curvature_s[i]) > curv_thr
            and i + 1 < len(drift_s)
            and drift_s[i + 1] > drift_s[i]
        ):
            regime_idx = i
            break

    # Fallback: wenn kein robuster Punkt gefunden wird, nimm Drift-Minimum
    if regime_idx is None:
        regime_idx = drift_min_idx

    result = {
        "collapse_idx": collapse_idx,
        "drift_min_idx": drift_min_idx,
        "regime_idx": regime_idx,
        "drift": drift,
        "drift_s": drift_s,
        "curvature": curvature,
        "curvature_s": curvature_s,
        "curv_thr": curv_thr,
    }

    return result


# ----------------------------------------
# 5. Plot
# ----------------------------------------

def plot_result(time, voltage, result, filename):
    collapse_idx = result["collapse_idx"]
    drift_min_idx = result["drift_min_idx"]
    regime_idx = result["regime_idx"]
    drift_s = result["drift_s"]
    curvature_s = result["curvature_s"]
    curv_thr = result["curv_thr"]

    plt.figure(figsize=(10, 8))

    # Voltage
    plt.subplot(3, 1, 1)
    plt.plot(time, voltage, label="Voltage")
    plt.axvline(time[drift_min_idx], linestyle="--", label="Drift Minimum")
    plt.axvline(time[regime_idx], linestyle=":", label="Regime Change")
    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="-.", label="Collapse")
    plt.title("Voltage Trajectory")
    plt.legend()
    plt.grid()

    # Drift
    plt.subplot(3, 1, 2)
    plt.plot(time, drift_s, label="Smoothed Drift dv/dt")
    plt.axvline(time[drift_min_idx], linestyle="--", label="Drift Minimum")
    plt.axvline(time[regime_idx], linestyle=":", label="Regime Change")
    plt.title("Drift")
    plt.legend()
    plt.grid()

    # Curvature
    plt.subplot(3, 1, 3)
    plt.plot(time, curvature_s, label="Smoothed Curvature d²v/dt²")
    plt.axhline(curv_thr, linestyle="--", label="Curvature Threshold")
    plt.axhline(-curv_thr, linestyle="--")
    plt.axvline(time[drift_min_idx], linestyle="--", label="Drift Minimum")
    plt.axvline(time[regime_idx], linestyle=":", label="Regime Change")
    plt.title("Curvature")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ----------------------------------------
# 6. Report
# ----------------------------------------

def print_report(name, time, result):
    collapse_idx = result["collapse_idx"]
    drift_min_idx = result["drift_min_idx"]
    regime_idx = result["regime_idx"]

    print("\n==============================")
    print(f"Testing: {name}")
    print("==============================\n")

    print(f"Drift minimum at t = {time[drift_min_idx]:.2f}")
    print(f"Regime change at t = {time[regime_idx]:.2f}")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]:.2f}")
        print(f"Lead time (regime -> collapse) = {time[collapse_idx] - time[regime_idx]:.2f}")
        print(f"Lead time (drift min -> collapse) = {time[collapse_idx] - time[drift_min_idx]:.2f}")
    else:
        print("No collapse detected")


# ----------------------------------------
# 7. RUN
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
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        time, voltage = load_csv(filepath)
        result = detect_regime_change(time, voltage)

        print_report(file, time, result)

        out_file = os.path.join(output_path, file.replace(".csv", "_regime.png"))
        plot_result(time, voltage, result, out_file)
        print(f"Saved plot to: {out_file}")
