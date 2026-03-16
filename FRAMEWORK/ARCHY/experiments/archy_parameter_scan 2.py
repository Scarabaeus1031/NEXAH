from __future__ import annotations

import random
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)


def random_system(i: int):

    outside = {
        "thermal": random.uniform(10, 30),
        "pressure": 1,
        "acoustic": random.uniform(0.5, 5),
        "humidity": random.uniform(0.5, 2),
    }

    inside = {
        "thermal": random.uniform(0, 10),
        "pressure": random.uniform(0.1, 0.5),
        "acoustic": random.uniform(0.1, 2),
        "humidity": random.uniform(0.3, 1),
    }

    active_elements = {
        "mass": random.random(),
        "medium": random.random(),
        "geometry": random.random(),
        "location": random.random(),
        "layering": random.random(),
        "orientation": random.random(),
        "urban_form": random.random(),
    }

    return ArchySystemInput(
        name=f"sys_{i}",
        outside=outside,
        inside=inside,
        active_elements=active_elements,
        base_orientation=random.uniform(0, 20),
        architectural_delta=random.uniform(0, 0.1),
        environmental_delta=random.uniform(0, 0.1),
    )


def run_scan(n=200):

    systems = [random_system(i) for i in range(n)]

    results = [analyze_archy_system(s) for s in systems]

    si = [r.stability.weighted_score for r in results]
    hcf = [r.coherence.hybrid_coherence for r in results]
    score = [r.archy_score for r in results]

    plt.figure(figsize=(8,6))

    scatter = plt.scatter(
        si,
        hcf,
        c=score,
        s=40,
    )

    plt.xlabel("Stability Index (SI)")
    plt.ylabel("Hybrid Coherence (HCF)")
    plt.title("ARCHY Parameter Scan")

    plt.colorbar(scatter, label="ARCHY Score")

    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    run_scan(500)
