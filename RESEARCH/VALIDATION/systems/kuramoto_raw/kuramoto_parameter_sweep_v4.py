#!/usr/bin/env python3

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from field_projection_kuramoto_v4 import run_experiment, KuramotoConfig


def main():

    K_values = np.linspace(0.5, 3.0, 12)

    results = []

    for K in K_values:
        print(f"K={K:.3f}")
        config = KuramotoConfig(coupling_k=K)
        summary = run_experiment(config)
        results.append(summary)

    df = pd.DataFrame(results)

    # 🔥 sweep folder
    out = Path(__file__).parent / "outputs" / "kuramoto_v4" / "sweeps" / f"sweep_{int(time.time())}"
    out.mkdir(parents=True, exist_ok=True)

    df.to_csv(out / "sweep.csv", index=False)

    # ===== plots =====

    plt.plot(df["K"], df["iota_percent"], marker="o")
    plt.savefig(out / "iota_vs_K.png")
    plt.clf()

    plt.plot(df["K"], df["transition_rate"], marker="o")
    plt.savefig(out / "transition_vs_K.png")
    plt.clf()

    # 🔥 PHASE DIAGRAM
    plt.scatter(df["r_mean"], df["abs_delta_theta_std"], c=df["K"])
    plt.colorbar(label="K")
    plt.xlabel("r_mean")
    plt.ylabel("drift std")
    plt.savefig(out / "phase_diagram.png")
    plt.clf()

    print(df)


if __name__ == "__main__":
    main()
