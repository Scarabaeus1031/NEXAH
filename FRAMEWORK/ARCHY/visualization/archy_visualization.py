from __future__ import annotations

import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    analyze_archy_system,
    ArchySystemInput,
)

# -------------------------------------------------------
# Example Systems
# -------------------------------------------------------

def cave_system():
    return ArchySystemInput(
        name="cave",
        outside={"thermal":20,"pressure":1,"acoustic":1,"humidity":1},
        inside={"thermal":5,"pressure":0.1,"acoustic":0.2,"humidity":0.6},
        domain_weights={"thermal":1.2,"pressure":1.0,"acoustic":1.0,"humidity":0.8},
        active_elements={"mass":1,"medium":1,"geometry":0.7,"location":0.8,"layering":0.6},
        base_orientation=0,
        architectural_delta=0.05,
        environmental_delta=0.02,
    )


def igloo_system():
    return ArchySystemInput(
        name="igloo",
        outside={"thermal":25,"pressure":1,"acoustic":1,"humidity":0.8},
        inside={"thermal":2,"pressure":0.2,"acoustic":0.3,"humidity":0.5},
        domain_weights={"thermal":1.3,"pressure":1.0,"acoustic":0.8,"humidity":0.7},
        active_elements={
            "mass":0.8,
            "medium":0.7,
            "geometry":1.0,
            "location":0.8,
            "layering":0.6,
            "orientation":0.6,
        },
        base_orientation=5,
        architectural_delta=0.03,
        environmental_delta=0.02,
    )


def city_block():
    return ArchySystemInput(
        name="city_block",
        outside={"thermal":18,"pressure":1,"acoustic":4,"humidity":1},
        inside={"thermal":8,"pressure":0.3,"acoustic":1,"humidity":0.7},
        domain_weights={"thermal":1.0,"pressure":0.8,"acoustic":1.2,"humidity":0.6},
        active_elements={
            "mass":0.7,
            "geometry":0.8,
            "location":0.9,
            "layering":0.5,
            "orientation":0.7,
            "urban_form":1.0,
        },
        base_orientation=10,
        architectural_delta=0.08,
        environmental_delta=0.05,
    )


# -------------------------------------------------------
# Visualization
# -------------------------------------------------------

def plot_archy_systems():

    systems = [
        cave_system(),
        igloo_system(),
        city_block(),
    ]

    results = [analyze_archy_system(s) for s in systems]

    si_values = [r.stability.weighted_score for r in results]
    hcf_values = [r.coherence.hybrid_coherence for r in results]
    scores = [r.archy_score for r in results]
    labels = [r.name for r in results]

    plt.figure(figsize=(8,6))

    scatter = plt.scatter(
        si_values,
        hcf_values,
        c=scores,
        s=200
    )

    for i, label in enumerate(labels):
        plt.text(
            si_values[i] + 0.01,
            hcf_values[i] + 0.01,
            label,
        )

    plt.xlabel("Stability Index (SI)")
    plt.ylabel("Hybrid Coherence (HCF)")
    plt.title("ARCHY Stability Landscape")

    plt.colorbar(scatter, label="ARCHY Score")

    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    plot_archy_systems()
