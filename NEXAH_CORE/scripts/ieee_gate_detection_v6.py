# NEXAH_CORE/scripts/ieee_gate_detection_v6.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v6.png"


# --------------------------------------------------
# 1. SIGNAL GENERATION
# --------------------------------------------------
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# 2. COHERENCE
# --------------------------------------------------
def compute_coherence(x, window=20, max_lag=5):
    C = np.zeros(len(x))

    for i in range(window, len(x)):
        segment = x[i-window:i]
        vals = []

        for lag in range(1, max_lag + 1):
            a = segment[:-lag]
            b = segment[lag:]

            if np.std(a) > 1e-12 and np.std(b) > 1e-12:
                vals.append(abs(np.corrcoef(a, b)[0, 1]))

        C[i] = np.mean(vals) if vals else 0.0

    return C


# --------------------------------------------------
# 3. SPECTRAL ENTROPY
# --------------------------------------------------
def compute_spectral_entropy(x, fs=1.0, window=40):
    S = np.zeros(len(x))

    for i in range(window, len(x)):
        segment = x[i-window:i]
        _, pxx = welch(segment, fs=fs, nperseg=len(segment))

        pxx = pxx + 1e-12
        pxx = pxx / np.sum(pxx)

        S[i] = entropy(pxx)

    return S


# --------------------------------------------------
# 4. PHASE SPACE GEOMETRY
# --------------------------------------------------
def compute_phase_geometry(t, x, window=30):
    """
    Geometry score:
    local phase-space dispersion.

    Low value  = coherent orbit / structured trajectory
    High value = scattered trajectory / geometric breakdown
    """
    dx = np.gradient(x, t)
    G = np.zeros(len(x))

    for i in range(window, len(x)):
        X = np.column_stack([
            x[i-window:i],
            dx[i-window:i],
        ])

        cov = np.cov(X.T)

        eigvals = np.linalg.eigvalsh(cov)
        eigvals = np.maximum(eigvals, 1e-12)

        # area-like dispersion in phase space
        G[i] = np.sqrt(np.prod(eigvals))

    return dx, G

# --------------------------------------------------
# 5. GATE DETECTION (MULTI-LAYER)
# --------------------------------------------------
def detect_gates(C, S, G):
    """
    Gate = simultaneous:
    - low coherence
    - high entropy
    - high phase-space dispersion
    """

    C_thr = np.percentile(C, 10)
    S_thr = np.percentile(S, 85)
    G_thr = np.percentile(G, 85)

    mask = (C < C_thr) & (S > S_thr) & (G > G_thr)

    gates = []
    in_gate = False
    start = 0

    for i, val in enumerate(mask):
        if val and not in_gate:
            in_gate = True
            start = i

        elif not val and in_gate:
            gates.append((start, i))
            in_gate = False

    if in_gate:
        gates.append((start, len(mask) - 1))

    return gates, C_thr, S_thr, G_thr


# --------------------------------------------------
# 6. PRECURSOR DETECTION
# --------------------------------------------------
def detect_precursor(C, threshold):
    """
    Precursor = first meaningful drop in coherence
    """
    for i in range(5, len(C)):
        if C[i] < threshold and C[i-1] >= threshold:
            return i
    return None


# --------------------------------------------------
# 7. MAIN EXECUTION
# --------------------------------------------------
if __name__ == "__main__":

    t = np.linspace(0, 100, 1000)

    x = generate_signal(t)
    C = compute_coherence(x)
    S = compute_spectral_entropy(x)
    dx, G = compute_phase_geometry(t, x)

    gates, C_thr, S_thr, G_thr = detect_gates(C, S, G)
    precursor = detect_precursor(C, C_thr)

    print("\n--- NEXAH IEEE Gate Detection v6 ---")
    print(f"Coherence threshold: {C_thr:.3f}")
    print(f"Entropy threshold: {S_thr:.3f}")
    print(f"Geometry threshold: {G_thr:.3f}")

    if precursor is not None:
        print(f"Precursor at t ≈ {t[precursor]:.2f}")

    print(f"Detected gates: {len(gates)}")
    for g in gates:
        print(f"Gate: t = {t[g[0]]:.2f} → {t[g[1]]:.2f}")


# --------------------------------------------------
# 8. VISUALIZATION
# --------------------------------------------------
    fig, axs = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

    # --- SIGNAL ---
    axs[0].plot(t, x)
    axs[0].set_title("System Dynamics x(t)")

    # --- COHERENCE ---
    axs[1].plot(t, C, label="C(t)")
    axs[1].axhline(C_thr, linestyle="--", label="C threshold")
    if precursor:
        axs[1].axvline(t[precursor], color="orange", label="precursor")
    axs[1].legend()
    axs[1].set_title("Coherence")

    # --- ENTROPY ---
    axs[2].plot(t, S, label="S(t)")
    axs[2].axhline(S_thr, linestyle="--", label="S threshold")
    axs[2].legend()
    axs[2].set_title("Spectral Entropy")

    # --- GEOMETRY ---
    axs[3].plot(t, G, label="G(t)")
    axs[3].axhline(G_thr, linestyle="--", label="G threshold")
    axs[3].legend()
    axs[3].set_title("Phase Space Dispersion")

    # --- GATES ---
    axs[4].set_title("Gate Detection")

    for g in gates:
        start = min(g[0], len(t)-1)
        end = min(g[1], len(t)-1)
        axs[4].axvspan(t[start], t[end], alpha=0.3)

    # --- SAVE ---
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    print(f"\nSaved to: {OUTPUT_PATH}")
    plt.show()
