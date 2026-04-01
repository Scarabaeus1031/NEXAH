import numpy as np
import matplotlib.pyplot as plt
import os
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_application.scripts.ieee_loader_v118 import load_ieee118  # Importiere den neuen Loader

# --------------------------------------------------
# 1. IEEE System laden
# --------------------------------------------------

def load_system():
    # Wählen Sie das IEEE 118-Netzwerk aus dem Loader
    net = load_ieee118()
    return net

# --------------------------------------------------
# 2. Synthetic IEEE-like system (lightweight demo)
# --------------------------------------------------

def generate_system(n=200):
    np.random.seed(42)
    c = np.linspace(0.2, 1.2, n)
    dc = 0.8 * c + 0.1 * np.sin(6 * c)
    noise = 0.05 * np.random.randn(n)
    dc = dc + noise
    return c, dc

# --------------------------------------------------
# 3. Field (vector field approximation)
# --------------------------------------------------

def compute_field(c, dc):
    ddc = np.gradient(dc)
    return ddc

# --------------------------------------------------
# 4. Rift detection (zero residual region)
# --------------------------------------------------

def detect_rift(c, dc):
    residual = dc - (0.8 * c)
    idx = np.argsort(np.abs(residual))[:10]
    return idx, residual

# --------------------------------------------------
# 5. Stability metric
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
# 6. Intervention (simple correction)
# --------------------------------------------------

def apply_intervention(c, dc, critical_idx):
    dc_new = dc.copy()
    dc_new[critical_idx] = 0.8 * c[critical_idx]
    return dc_new

# --------------------------------------------------
# 7. Main demo
# --------------------------------------------------

def run_demo():

    # --- load the system
    net = load_system()  # Laden des IEEE 118-Netzwerks

    # --- generate synthetic system
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

    improvement = stability_after - stability_before

    # --------------------------------------------------
    # OUTPUT (Mic Drop)
    # --------------------------------------------------

    print("\n⚡ NEXAH FIELD NAVIGATION RESULT\n")
    print(f"Before Stability: {stability_before:.3f}")
    print(f"After Stability:  {stability_after:.3f}")
    print(f"Improvement:      {improvement:+.3f}")

    print("\nCritical Point:")
    print(f"  index = {critical_idx}")
    print(f"  c = {c[critical_idx]:.3f}")
    print(f"  dc_before = {dc[critical_idx]:.3f}")
    print(f"  dc_after  = {dc_new[critical_idx]:.3f}")

    # --------------------------------------------------
    # Visualization
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))

    plt.scatter(c, dc, s=20, alpha=0.5, label="system")
    plt.scatter(c[rift_idx], dc[rift_idx], color='green', s=50, label="rift")
    plt.scatter(c[critical_idx], dc[critical_idx], color='red', s=80, label="critical")
    plt.scatter(c[critical_idx], dc_new[critical_idx], color='blue', s=80, label="after")

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

    # --------------------------------------------------
    # SAVE OUTPUT (🔥 important)
    # --------------------------------------------------

    output_dir = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_application/results"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "demo_plot.png")

    plt.savefig(output_path, dpi=200, bbox_inches="tight")

    print(f"\n📊 Plot saved to:\n{output_path}\n")

    plt.show()


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    run_demo()
