from __future__ import annotations

import random

from FRAMEWORK.ARCHY.environments.archy_environments import get_environment
from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)


def random_elements():

    return {
        "mass": random.random(),
        "medium": random.random(),
        "geometry": random.random(),
        "location": random.random(),
        "layering": random.random(),
        "orientation": random.random(),
        "urban_form": random.random(),
    }


def create_candidate(environment):

    inside = {
        "thermal": random.uniform(0, 10),
        "pressure": random.uniform(0.1, 0.5),
        "acoustic": random.uniform(0.1, 2),
        "humidity": random.uniform(0.3, 1),
    }

    return ArchySystemInput(
        name="candidate",
        outside=environment.outside,
        inside=inside,
        active_elements=random_elements(),
        base_orientation=random.uniform(0, 30),
        architectural_delta=random.uniform(0, 0.1),
        environmental_delta=random.uniform(0, 0.1),
    )


def mutate(elements, rate=0.2):

    new = elements.copy()

    for k in new:

        if random.random() < rate:
            new[k] = min(1.0, max(0.0, new[k] + random.uniform(-0.2, 0.2)))

    return new


def evolve(environment_name="desert", generations=30, population_size=40):

    env = get_environment(environment_name)

    population = [create_candidate(env) for _ in range(population_size)]

    best_result = None

    for g in range(generations):

        results = []

        for p in population:

            r = analyze_archy_system(p)
            results.append((r.archy_score, p, r))

        results.sort(key=lambda x: x[0], reverse=True)

        best_score, best_candidate, best_result = results[0]

        print(f"Generation {g}  best_score={round(best_score,3)}")

        survivors = results[: population_size // 4]

        new_population = []

        for _, candidate, _ in survivors:

            new_population.append(candidate)

            for _ in range(3):

                mutated = create_candidate(env)
                mutated.active_elements = mutate(candidate.active_elements)

                new_population.append(mutated)

        population = new_population[:population_size]

    return best_result


if __name__ == "__main__":

    result = evolve("desert")

    print("")
    print("FINAL BEST ARCHITECTURE")
    print("=" * 40)

    print("ARCHY SCORE:", round(result.archy_score,3))
    print("REGIME:", result.regime_label)
