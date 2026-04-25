# NEXAH_CORE/scripts/ieee_gate_detection_v7.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v7.png"


# --------------------------------------------------
# 1. SIGNAL
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
        seg = x[i-window:i]
        vals = []

        for lag in range(1, max_lag+1):
            a = seg[:-lag]
            b = seg[lag:]
            if np.std(a) > 1e-12 and np.std(b) > 1e-12:
                vals.append(abs(np.corrcoef(a, b)[0,1]))

        C[i] = np.mean(vals) if vals else 0

    return C


# --------------------------------------------------
# 3. ENTROPY
# --------------------------------------------------
def compute_entropy(x, window=40):
    S = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i-window:i]
        _, pxx = welch(seg, nperseg=len(seg))
        pxx = pxx + 1e-12
        pxx /= np.sum(pxx)
        S[i] = entropy(pxx)

    return S


# --------------------------------------------------
# 4. GEOMETRY
# --------------------------------------------------
def compute_geometry(t, x, window=30):
    dx = np.gradient(x, t)
    G = np.zeros(len(x))

    for i in range(window, len(x)):
        X = np.column_stack((x[i-window:i], dx[i-window:i]))
        cov = np.cov(X.T)
        eigvals = np.maximum(np.linalg.eigvalsh(cov), 1e-12)
        G[i] = np.sqrt(np.prod(eigvals))

    return dx, G


# --------------------------------------------------
# 5. RAW GATE MASK
# --------------------------------------------------
def compute_gate_mask(C, S, G):
    C_thr = np.percentile(C[C>0], 15)
    S_thr = np.percentile(S[S>0], 80)
    G_thr = np.percentile(G[G>0], 80)

    mask = (C < C_thr) & (S > S_thr) & (G > G_thr)

    return mask, C_thr, S_thr, G_thr


# --------------------------------------------------
# 6. CLUSTERING (CORE OF v7)
# --------------------------------------------------
def cluster_gates(mask, min_length=10, max_gap=8):
    """
    Merge nearby gate segments into clusters
    """

    clusters = []
    start = None
    gap_count = 0

    for i, val in enumerate(mask):

        if val:
            if start is None:
                start = i
            gap_count = 0

        else:
            if start is not None:
                gap_count += 1

                if gap_count > max_gap:
                    end = i - gap_count

                    if end - start >= min_length:
                        clusters.append((start, end))

                    start = None
                    gap_count = 0

    if start is not None:
        clusters.append((start, len(mask)-1))

    return clusters


# --------------------------------------------------
# 7. PRECURSOR
# --------------------------------------------------
def detect_precursor(C, C_thr):
    for i in range(10, len(C)):
        if C[i] < C_thr and C[i-1] >= C_thr:
            return i
    return None


# --------------------------------------------------
# 8. MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)
x = generate_signal(t)

C = compute_coherence(x)
S = compute_entropy(x)
dx, G = compute_geometry(t, x)

mask, C_thr, S_thr, G_thr = compute_gate_mask(C, S, G)
clusters = cluster_gates(mask)

precursor = detect_precursor(C, C_thr)


# --------------------------------------------------
# 9. VISUAL
# --------------------------------------------------
fig, axs = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

axs[0].plot(t, x)
axs[0].set_title("System Dynamics")

axs[1].plot(t, C)
axs[1].axhline(C_thr, linestyle="--")
if precursor:
    axs[1].axvline(t[precursor], color="orange")
axs[1].set_title("Coherence")

axs[2].plot(t, S)
axs[2].axhline(S_thr, linestyle="--")
axs[2].set_title("Entropy")

axs[3].plot(t, G)
axs[3].axhline(G_thr, linestyle="--")
axs[3].set_title("Phase Space Dispersion")

axs[4].set_title("Clustered Transition Zones")

for c in clusters:
    s = min(c[0], len(t)-1)
    e = min(c[1], len(t)-1)

    for ax in axs:
        ax.axvspan(t[s], t[e], alpha=0.2)

    axs[4].axvspan(t[s], t[e], alpha=0.5)

plt.tight_layout()
plt.savefig(OUTPUT_PATH)

print("\n--- NEXAH IEEE Gate Detection v7 ---")
print(f"Detected clusters: {len(clusters)}")

for c in clusters:
    print(f"Zone: t = {t[c[0]]:.2f} → {t[c[1]]:.2f}")

print(f"\nSaved to: {OUTPUT_PATH}")

plt.show()
