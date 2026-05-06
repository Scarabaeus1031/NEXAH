import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# SIGNAL (unchanged v3)
# ============================================================

def generate_signal(t, seed=0):
    np.random.seed(seed)
    x = np.zeros_like(t)

    x += 0.3 * np.sin(0.5 * t)

    mask2 = t > 30
    x[mask2] += 0.8 * np.sin(1.2 * t[mask2])

    mask3 = t > 60
    drift = np.cumsum(0.05 * np.random.randn(np.sum(mask3)))
    x[mask3] = np.sin(1.2 * t[mask3] + drift)

    mask4 = t > 75
    x[mask4] += 0.8 * np.random.randn(np.sum(mask4))

    return x


# ============================================================
# COHERENCE
# ============================================================

def compute_coherence(x, window=30):
    C = np.full(len(x), np.nan)

    for i in range(window, len(x)):
        segment = x[i-window:i]

        lags = [1,2,3,5,8]
        vals = []

        for lag in lags:
            if len(segment) > lag:
                c = np.corrcoef(segment[:-lag], segment[lag:])[0,1]
                if not np.isnan(c):
                    vals.append(c)

        if vals:
            C[i] = np.mean(vals)

    return C


# ============================================================
# PRECURSOR DETECTION (NEW)
# ============================================================

def detect_precursor(C, threshold=0.7):
    for i in range(len(C)):
        if not np.isnan(C[i]) and C[i] < threshold:
            return i
    return None


# ============================================================
# GATE DETECTION
# ============================================================

def detect_gates(C, epsilon=0.3):
    mask = C < epsilon
    indices = np.where(mask)[0]
    return indices


# ============================================================
# CLUSTER GATES → TRANSITION ZONE (NEW)
# ============================================================

def cluster_gates(indices, max_gap=10):
    if len(indices) == 0:
        return []

    zones = []
    start = indices[0]

    for i in range(1, len(indices)):
        if indices[i] - indices[i-1] > max_gap:
            zones.append((start, indices[i-1]))
            start = indices[i]

    zones.append((start, indices[-1]))
    return zones


# ============================================================
# DELAY ANALYSIS (NEW)
# ============================================================

def compute_delay(precursor_idx, zone):
    if precursor_idx is None or zone is None:
        return None
    return zone[0] - precursor_idx


# ============================================================
# MAIN
# ============================================================

def run():
    t = np.linspace(0, 100, 1200)

    x = generate_signal(t)
    C = compute_coherence(x)

    precursor = detect_precursor(C)
    gate_indices = detect_gates(C)
    zones = cluster_gates(gate_indices)

    print("\n--- NEXAH v3.1 ---")

    if precursor:
        print(f"Precursor at t ≈ {t[precursor]:.2f}")

    print(f"Gate zones: {len(zones)}")

    for z in zones:
        print(f"Zone: {t[z[0]]:.2f} → {t[z[1]]:.2f}")

    if zones:
        delay = compute_delay(precursor, zones[0])
        if delay:
            print(f"Delay (precursor → gate): Δt ≈ {t[delay]:.2f}")

    return t, x, C, precursor, zones


# ============================================================
# PLOT
# ============================================================

def plot(t, x, C, precursor, zones, save_path=None):

    fig, axes = plt.subplots(3, 1, figsize=(12,10))

    # Signal
    axes[0].plot(t, x)
    axes[0].set_title("System Dynamics")

    # Coherence
    axes[1].plot(t, C)
    axes[1].axhline(0.3, linestyle="--", label="gate threshold")
    axes[1].axhline(0.7, linestyle="--", alpha=0.5, label="precursor")

    if precursor:
        axes[1].axvline(t[precursor], color="orange", label="precursor")

    for z in zones:
        axes[1].axvspan(t[z[0]], t[z[1]], alpha=0.3)

    axes[1].legend()
    axes[1].set_title("Coherence")

    # Gates
    axes[2].set_title("Transition Zones")
    axes[2].set_ylim(0,1)

    for z in zones:
        axes[2].axvspan(t[z[0]], t[z[1]], alpha=0.5)

    if precursor:
        axes[2].axvline(t[precursor], color="orange")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"\nSaved to: {save_path}")

    plt.show()


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    t, x, C, precursor, zones = run()

    plot(
        t, x, C, precursor, zones,
        save_path="NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v3_1.png"
    )
