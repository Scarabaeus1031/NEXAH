# ⚡ NEXAH IEEE FIELD NAVIGATION DEMO
# Minimal, clean, reproducible

import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Synthetic IEEE-like system (lightweight demo)
# --------------------------------------------------

def generate_system(n=200):
    np.random.seed(42)
    c = np.linspace(0.2, 1.2, n)
    dc = 0.8 * c + 0.1 * np.sin(6 * c)
    noise = 0.05 * np.random.randn(n)
    dc = dc + noise
    return c, dc


# --------------------------------------------------
# 2. Field (vector field approximation)
# --------------------------------------------------

def compute_field(c, dc):
    ddc = np.gradient(dc)
    return ddc


# --------------------------------------------------
# 3. Rift detection (zero residual region)
# --------------------------------------------------

def detect_rift(c, dc):
    residual = dc - (0.8 * c)
    idx = np.argsort(np.abs(residual))[:10]  # closest to zero
    return idx, residual


# --------------------------------------------------
# 4. Stability metric
# --------------------------------------------------

def compute_stability(c, dc, rift_idx):
    rift_c = c[rift_idx]
    rift_dc = dc[rift_idx]

    distances = []
    for i in range(len(c)):
        d = np.min((c[i] - rift_c) ** 2 + (dc[i] - rift_dc) ** 2)
        distances.append(np.sqrt(d))

    stability = 1.0 - np.mean(distances)
    return stability, np.array(distances)


# --------------------------------------------------
# 5. Intervention (simple correction)
# --------------------------------------------------

def apply_intervention(c, dc, critical_idx):
    dc_new = dc.copy()

    # pull critical point toward rift
    dc_new[critical_idx] = 0.8 * c[critical_idx]

    return dc_new


# --------------------------------------------------
# 6. Main demo
# --------------------------------------------------

def run_demo():

    # --- generate system
    c, dc = generate_system()

    # --- detect rift
    rift_idx, residual = detect_rift(c, dc)

    # --- compute stability BEFORE
    stability_before, distances = compute_stability(c, dc, rift_idx)

    # --- find critical point (max distance)
    critical_idx = np.argmax(distances)

    # --- apply intervention
    dc_new = apply_intervention(c, dc, critical_idx)

    # --- compute stability AFTER
    stability_after, _ = compute_stability(c, dc_new, rift_idx)

    # --------------------------------------------------
    # OUTPUT (Mic Drop)
    # --------------------------------------------------

    print("\n⚡ NEXAH FIELD NAVIGATION RESULT\n")
    print(f"Before Stability: {stability_before:.3f}")
    print(f"After Stability:  {stability_after:.3f}")
    print(f"\nCritical Point Index: {critical_idx}")
    print(f"Intervention applied at c = {c[critical_idx]:.3f}")

    # --------------------------------------------------
    # Visualization
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))

    # original system
    plt.scatter(c, dc, s=20, alpha=0.5, label="system")

    # rift
    plt.scatter(c[rift_idx], dc[rift_idx],
                color='green', s=50, label="rift")

    # critical point
    plt.scatter(c[critical_idx], dc[critical_idx],
                color='red', s=80, label="critical")

    # corrected point
    plt.scatter(c[critical_idx], dc_new[critical_idx],
                color='blue', s=80, label="after")

    # arrow (intervention)
    plt.arrow(
        c[critical_idx],
        dc[critical_idx],
        0,
        dc_new[critical_idx] - dc[critical_idx],
        head_width=0.01,
        length_includes_head=True,
        color='blue'
    )

    plt.xlabel("c (state)")
    plt.ylabel("dc (drift)")
    plt.title("NEXAH Field Navigation — Rift & Intervention")
    plt.legend()
    plt.grid()

    plt.show()


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    run_demo()
