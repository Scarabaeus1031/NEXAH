from __future__ import annotations

import random
import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
)

from FRAMEWORK.ARCHY.environments.archy_environments import get_environment


def random_building(environment):

    inside = {
        "thermal": random.uniform(0, 10),
        "pressure": random.uniform(0.1, 0.5),
        "acoustic": random.uniform(0.1, 2),
        "humidity": random.uniform(0.3, 1),
    }

    elements = {
        "mass": random.random(),
        "medium": random.random(),
        "geometry": random.random(),
        "location": random.random(),
        "layering": random.random(),
        "orientation": random.random(),
        "urban_form": random.random(),
    }

    model = ArchySystemInput(
        name="building",
        outside=environment.outside,
        inside=inside,
        active_elements=elements,
        base_orientation=random.uniform(0, 30),
        architectural_delta=random.uniform(0, 0.1),
        environmental_delta=random.uniform(0, 0.1),
    )

    return analyze_archy_system(model)


def generate_city(environment_name="desert", size=20):

    env = get_environment(environment_name)

    grid = np.zeros((size, size))

    for x in range(size):
        for y in range(size):

            building = random_building(env)

            grid[x, y] = building.archy_score

    return grid


def plot_city(grid):

    plt.figure(figsize=(8, 8))

    plt.imshow(grid, cmap="viridis")

    plt.colorbar(label="ARCHY Stability Score")

    plt.title("ARCHY Urban Stability Map")

    plt.xlabel("City X")
    plt.ylabel("City Y")

    plt.show()


if __name__ == "__main__":

    city = generate_city("desert", 30)

    plot_city(city)
