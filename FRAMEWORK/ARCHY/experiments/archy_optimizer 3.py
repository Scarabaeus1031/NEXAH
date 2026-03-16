from __future__ import annotations

import random

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)


def random_architecture():

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
        name="candidate",
        outside=outside,
        inside=inside,
        active_elements=active_elements,
        base_orientation=random.uniform(0, 30),
        architectural_delta=random.uniform(0, 0.1),
        environmental_delta=random.uniform(0, 0.1),
    )


def search_best_architecture(iterations=2000):

    best_result = None

    for i in range(iterations):

        candidate = random_architecture()

        result = analyze_archy_system(candidate)

        if best_result is None:
            best_result = result

        if result.archy_score > best_result.archy_score:
            best_result = result

    return best_result


def print_best(result):

    print("")
    print("BEST ARCHY STRUCTURE FOUND")
    print("=" * 40)

    print("ARCHY SCORE:", round(result.archy_score, 3))
    print("REGIME:", result.regime_label)

    print("")
    print("STABILITY INDEX:", round(result.stability.weighted_score, 3))
    print("HYBRID COHERENCE:", round(result.coherence.hybrid_coherence, 3))
    print("DRIFT:", round(result.delta.drift_magnitude, 3))

    if result.notes:
        print("")
        print("NOTES:")
        for n in result.notes:
            print("-", n)


if __name__ == "__main__":

    best = search_best_architecture(3000)

    print_best(best)
