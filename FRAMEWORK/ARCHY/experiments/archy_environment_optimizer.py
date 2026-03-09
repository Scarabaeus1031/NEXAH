from __future__ import annotations

import random

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)

from FRAMEWORK.ARCHY.environments.archy_environments import get_environment


def random_architecture(environment):

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
        outside=environment.outside,
        inside=inside,
        active_elements=active_elements,
        base_orientation=random.uniform(0, 30),
        architectural_delta=random.uniform(0, 0.1),
        environmental_delta=random.uniform(0, 0.1),
    )


def search_best(environment_name, iterations=5000):

    env = get_environment(environment_name)

    best_result = None

    for i in range(iterations):

        candidate = random_architecture(env)

        result = analyze_archy_system(candidate)

        if best_result is None:
            best_result = result

        if result.archy_score > best_result.archy_score:
            best_result = result

    return best_result


def print_result(result):

    print("")
    print("BEST ARCHITECTURE")
    print("=" * 40)

    print("ARCHY SCORE:", round(result.archy_score, 3))
    print("REGIME:", result.regime_label)

    print("")
    print("STABILITY:", round(result.stability.weighted_score, 3))
    print("COHERENCE:", round(result.coherence.hybrid_coherence, 3))
    print("DRIFT:", round(result.delta.drift_magnitude, 3))


if __name__ == "__main__":

    environment = "desert"

    result = search_best(environment)

    print("Environment:", environment)

    print_result(result)
