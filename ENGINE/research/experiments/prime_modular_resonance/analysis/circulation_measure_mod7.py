import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CURL (ROTATION) MEASURE
# ============================================================

def compute_curl(U, V, dx, dy):
    dV_dx = np.gradient(V, axis=1) / dx
    dU_dy = np.gradient(U, axis=0) / dy
    curl = dV_dx - dU_dy
    return curl

# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():
    print("="*70)
    print("CIRCULATION MEASURE (mod 7)")
    print("="*70)

    # load from previous script (reuse your flux field)
    from energy_flux_field_mod7 import (
        primes_upto,
        build_transition_matrix,
        spectral_projection,
        project_flow,
        compute_flux_field
    )

    N_PRIMES = 2000

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)
    x, y = project_flow(residues, coords)

    X, Y, U, V = compute_flux_field(x, y)

    dx = (X.max() - X.min()) / X.shape[1]
    dy = (Y.max() - Y.min()) / Y.shape[0]

    curl = compute_curl(U, V, dx, dy)

    print("\nCurl stats:")
    print(f"Mean: {np.mean(curl):.6f}")
    print(f"Std:  {np.std(curl):.6f}")
    print(f"Max:  {np.max(curl):.6f}")
    print(f"Min:  {np.min(curl):.6f}")

    # ========================================================
    # PLOT 1: CURL HEATMAP
    # ========================================================

    plt.figure(figsize=(8,8))
    plt.imshow(curl, origin='lower',
               extent=[X.min(), X.max(), Y.min(), Y.max()])
    plt.colorbar(label="curl (rotation strength)")
    plt.title("Circulation Field (Curl)")
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.show()

    # ========================================================
    # PLOT 2: STRONG VORTEX ZONES
    # ========================================================

    threshold = np.std(curl) * 2

    mask = np.abs(curl) > threshold

    plt.figure(figsize=(8,8))
    plt.imshow(mask, origin='lower',
               extent=[X.min(), X.max(), Y.min(), Y.max()])
    plt.title("Strong Circulation Zones")
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.show()

# ============================================================

if __name__ == "__main__":
    main()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
