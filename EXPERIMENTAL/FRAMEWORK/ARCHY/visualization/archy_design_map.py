from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from FRAMEWORK.ARCHY.experiments.archy_parameter_scan import random_system
from FRAMEWORK.ARCHY.stability_models.archy_system_model import analyze_archy_system


def generate_dataset(n=600):

    systems = [random_system(i) for i in range(n)]
    results = [analyze_archy_system(s) for s in systems]

    si = np.array([r.stability.weighted_score for r in results])
    hcf = np.array([r.coherence.hybrid_coherence for r in results])
    score = np.array([r.archy_score for r in results])

    return si, hcf, score


def classify_zone(score):

    zones = []

    for s in score:

        if s < 0.3:
            zones.append("collapse")

        elif s < 0.45:
            zones.append("fragile")

        elif s < 0.6:
            zones.append("moderate")

        else:
            zones.append("stable")

    return zones


def plot_design_map():

    si, hcf, score = generate_dataset()

    zones = classify_zone(score)

    plt.figure(figsize=(9,7))

    scatter = plt.scatter(
        si,
        hcf,
        c=score,
        s=50,
        alpha=0.85
    )

    plt.xlabel("Stability Index (SI)")
    plt.ylabel("Hybrid Coherence (HCF)")
    plt.title("ARCHY Architectural Design Map")

    plt.colorbar(scatter, label="ARCHY Score")

    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    plot_design_map()
