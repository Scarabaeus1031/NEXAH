import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


def run_cycle(base_load, k, steps=24):
    results = []

    print(f"\n=== Testing k = {k} ===")

    for t in range(steps):
        phase = 2 * np.pi * t / steps

        # Tao (noise)
        noise = 0.15 * np.sin(phase) + 0.15

        # Dao (rotation) → jetzt mit Frequenzverhältnis!
        rotation = 0.5 + 0.3 * np.cos(k * phase)

        # Yin (damping)
        damping = 0.95 - 0.05 * np.sin(phase)

        print(f"t={t:02d} | noise={noise:.3f} | rot={rotation:.3f}")

        r = run_single_coupling(
            base_load=base_load,
            noise_strength=noise,
            flow_rotation=rotation,
            damping=damping,
        )

        results.append({
            "t": t,
            "k": k,
            "C": r["C"],
            "loops": r["loops"],
            "states": r["states"],
        })

    return pd.DataFrame(results)


def main():
    print("\n--- V31 Resonance Lock Scan ---\n")

    k_values = [1.0, 1.5, 2.0]  # 1:1, 3:2, 2:1

    all_results = []

    for k in k_values:
        df = run_cycle(base_load=1.0, k=k)
        all_results.append(df)

        # Plot direkt pro k
        plt.figure(figsize=(10, 6))
        plt.plot(df["t"], df["loops"], marker="o", label="loops")
        plt.plot(df["t"], df["C"], marker="o", label="C")
        plt.title(f"Time Series (k={k})")
        plt.legend()
        plt.xlabel("t")
        plt.show()

    full_df = pd.concat(all_results)
    full_df.to_csv("v31_resonance_lock.csv", index=False)

    print("\nSaved: v31_resonance_lock.csv")

    # =========================
    # SUMMARY
    # =========================
    print("\n--- SUMMARY ---")
    for k in k_values:
        subset = full_df[full_df["k"] == k]

        print(f"\nk = {k}")
        print(f"loops mean: {subset['loops'].mean():.2f}")
        print(f"loops std:  {subset['loops'].std():.2f}")
        print(f"C mean:     {subset['C'].mean():.4f}")
        print(f"C std:      {subset['C'].std():.4f}")


if __name__ == "__main__":
    main()
