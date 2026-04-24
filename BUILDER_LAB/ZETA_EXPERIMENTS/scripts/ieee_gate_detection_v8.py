# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v8.py
#
# v8: Phase-space clustering of transition zones
#
# Core idea:
# v7 detects transition zones in time.
# v8 asks: where do these gates live in phase space?
#
# Transition =
# low coherence
# + high entropy
# + high phase-space dispersion
# + clustered geometry in (x, dx/dt)

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy
from sklearn.cluster import DBSCAN

np.random.seed(42)

OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v8.png"
PHASE_OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v8_phase_space.png"


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
        seg = x[i - window:i]
        vals = []

        for lag in range(1, max_lag + 1):
            a = seg[:-lag]
            b = seg[lag:]

            if np.std(a) > 1e-12 and np.std(b) > 1e-12:
                vals.append(abs(np.corrcoef(a, b)[0, 1]))

        C[i] = np.mean(vals) if vals else 0.0

    return C


# --------------------------------------------------
# 3. SPECTRAL ENTROPY
# --------------------------------------------------
def compute_entropy(x, window=40):
    S = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i - window:i]
        _, pxx = welch(seg, nperseg=len(seg))

        pxx = pxx + 1e-12
        pxx = pxx / np.sum(pxx)

        S[i] = entropy(pxx)

    return S


# --------------------------------------------------
# 4. PHASE-SPACE GEOMETRY
# --------------------------------------------------
def compute_geometry(t, x, window=30):
    dx = np.gradient(x, t)
    G = np.zeros(len(x))

    for i in range(window, len(x)):
        X = np.column_stack((x[i - window:i], dx[i - window:i]))
        cov = np.cov(X.T)

        eigvals = np.maximum(np.linalg.eigvalsh(cov), 1e-12)
        G[i] = np.sqrt(np.prod(eigvals))

    return dx, G


# --------------------------------------------------
# 5. RAW GATE MASK
# --------------------------------------------------
def compute_gate_mask(C, S, G):
    C_thr = np.percentile(C[C > 0], 15)
    S_thr = np.percentile(S[S > 0], 80)
    G_thr = np.percentile(G[G > 0], 80)

    mask = (C < C_thr) & (S > S_thr) & (G > G_thr)

    return mask, C_thr, S_thr, G_thr


# --------------------------------------------------
# 6. TIME CLUSTERING
# --------------------------------------------------
def cluster_gates(mask, min_length=10, max_gap=8):
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
        clusters.append((start, len(mask) - 1))

    return clusters


# --------------------------------------------------
# 7. PHASE-SPACE CLUSTERING
# --------------------------------------------------
def cluster_phase_space(x, dx, mask):
    """
    Cluster only points that are inside detected gate regions.

    DBSCAN:
    - cluster labels >= 0 are coherent transition clusters
    - label -1 means noise / unclustered transition fragments
    """

    gate_idx = np.where(mask)[0]

    if len(gate_idx) == 0:
        return gate_idx, np.array([]), np.array([])

    points = np.column_stack((x[gate_idx], dx[gate_idx]))

    # Normalize for stable clustering
    mean = points.mean(axis=0)
    std = points.std(axis=0) + 1e-12
    points_norm = (points - mean) / std

    clustering = DBSCAN(eps=0.35, min_samples=5).fit(points_norm)
    labels = clustering.labels_

    return gate_idx, points, labels


# --------------------------------------------------
# 8. PRECURSOR
# --------------------------------------------------
def detect_precursor(C, C_thr):
    for i in range(10, len(C)):
        if C[i] < C_thr and C[i - 1] >= C_thr:
            return i
    return None


# --------------------------------------------------
# 9. MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)

x = generate_signal(t)
C = compute_coherence(x)
S = compute_entropy(x)
dx, G = compute_geometry(t, x)

mask, C_thr, S_thr, G_thr = compute_gate_mask(C, S, G)
time_clusters = cluster_gates(mask)
precursor = detect_precursor(C, C_thr)

gate_idx, phase_points, phase_labels = cluster_phase_space(x, dx, mask)


# --------------------------------------------------
# 10. TIME VIEW VISUALIZATION
# --------------------------------------------------
fig, axs = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

axs[0].plot(t, x)
axs[0].set_title("System Dynamics")

axs[1].plot(t, C, label="C(t)")
axs[1].axhline(C_thr, linestyle="--", label="C threshold")
if precursor is not None:
    axs[1].axvline(t[precursor], color="orange", label="precursor")
axs[1].legend()
axs[1].set_title("Coherence")

axs[2].plot(t, S, label="S(t)")
axs[2].axhline(S_thr, linestyle="--", label="S threshold")
axs[2].legend()
axs[2].set_title("Spectral Entropy")

axs[3].plot(t, G, label="G(t)")
axs[3].axhline(G_thr, linestyle="--", label="G threshold")
axs[3].legend()
axs[3].set_title("Phase-Space Dispersion")

axs[4].set_title("Clustered Transition Zones")
axs[4].set_ylim(0, 1)

for s, e in time_clusters:
    s = min(s, len(t) - 1)
    e = min(e, len(t) - 1)

    for ax in axs:
        ax.axvspan(t[s], t[e], alpha=0.18)

    axs[4].axvspan(t[s], t[e], alpha=0.5)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 11. PHASE-SPACE VISUALIZATION
# --------------------------------------------------
fig2, ax = plt.subplots(figsize=(8, 7))

ax.plot(x, dx, alpha=0.25, label="full trajectory")

if len(gate_idx) > 0:
    unique_labels = sorted(set(phase_labels))

    for label in unique_labels:
        label_mask = phase_labels == label
        pts = phase_points[label_mask]

        if label == -1:
            ax.scatter(
                pts[:, 0],
                pts[:, 1],
                s=18,
                alpha=0.35,
                label="gate noise",
            )
        else:
            ax.scatter(
                pts[:, 0],
                pts[:, 1],
                s=30,
                alpha=0.75,
                label=f"phase gate cluster {label}",
            )

ax.set_title("Phase-Space Gate Clustering")
ax.set_xlabel("x(t)")
ax.set_ylabel("dx/dt")
ax.legend()

plt.tight_layout()
plt.savefig(PHASE_OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 12. LOGGING
# --------------------------------------------------
print("\n--- NEXAH IEEE Gate Detection v8 ---")

print(f"Coherence threshold: {C_thr:.3f}")
print(f"Entropy threshold:   {S_thr:.3f}")
print(f"Geometry threshold:  {G_thr:.3f}")

if precursor is not None:
    print(f"Precursor at t ≈ {t[precursor]:.2f}")

print(f"\nTime transition zones: {len(time_clusters)}")
for s, e in time_clusters:
    print(f"Zone: t = {t[s]:.2f} → {t[e]:.2f}")

if len(phase_labels) > 0:
    labels = sorted(set(phase_labels))
    real_clusters = [l for l in labels if l != -1]
    noise_count = int(np.sum(phase_labels == -1))

    print(f"\nPhase-space gate clusters: {len(real_clusters)}")
    print(f"Unclustered gate points: {noise_count}")

    for label in real_clusters:
        count = int(np.sum(phase_labels == label))
        print(f"Cluster {label}: {count} points")

else:
    print("\nNo phase-space gate clusters detected.")

print(f"\nSaved time view to: {OUTPUT_PATH}")
print(f"Saved phase view to: {PHASE_OUTPUT_PATH}")

plt.show()
