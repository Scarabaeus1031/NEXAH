from __future__ import annotations

import random
import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.urban.archy_city_fields import simulate_city


CLIMATE_ZONES = [
    "desert",
    "coastal",
    "tropical",
    "urban_heat",
]


def generate_planet(size=6):

    planet = []

    for x in range(size):

        row = []

        for y in range(size):

            climate = random.choice(CLIMATE_ZONES)

            city_grid, field, modified = simulate_city(climate, 20, 10)

            stability = np.mean(modified)

            row.append((climate, stability))

        planet.append(row)

    return planet


def planet_matrix(planet):

    size = len(planet)

    grid = np.zeros((size, size))

    for x in range(size):
        for y in range(size):

            grid[x, y] = planet[x][y][1]

    return grid


def plot_planet(planet):

    grid = planet_matrix(planet)

    plt.figure(figsize=(6,6))

    plt.imshow(grid, cmap="viridis")

    plt.colorbar(label="Average City Stability")

    plt.title("ARCHY Planetary Stability Map")

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show()


def print_planet_info(planet):

    print("\nPlanet Cities\n")

    for x, row in enumerate(planet):

        for y, (climate, stability) in enumerate(row):

            print(
                f"City ({x},{y}) | climate={climate} | stability={round(stability,3)}"
            )


if __name__ == "__main__":

    planet = generate_planet(8)

    print_planet_info(planet)

    plot_planet(planet)
