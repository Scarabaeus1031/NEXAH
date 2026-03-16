from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.urban.archy_city_dynamics import evolve_city


def wind_field(size, direction="east", strength=0.02):

    field = np.zeros((size, size))

    if direction == "east":

        for x in range(size):
            field[:, x] = x * strength

    elif direction == "west":

        for x in range(size):
            field[:, x] = (size - x) * strength

    elif direction == "north":

        for y in range(size):
            field[y, :] = y * strength

    elif direction == "south":

        for y in range(size):
            field[y, :] = (size - y) * strength

    return field


def apply_field(grid, field, influence=0.3):

    return (1 - influence) * grid + influence * field


def simulate_city(environment="desert", size=30, steps=20):

    history = evolve_city(environment, size, steps)

    grid = history[-1]

    field = wind_field(size, "east")

    modified = apply_field(grid, field)

    return grid, field, modified


def plot_result(grid, field, modified):

    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.title("City Stability")
    plt.imshow(grid, cmap="viridis")

    plt.subplot(1,3,2)
    plt.title("Wind Field")
    plt.imshow(field, cmap="coolwarm")

    plt.subplot(1,3,3)
    plt.title("Coupled System")
    plt.imshow(modified, cmap="viridis")

    plt.show()


if __name__ == "__main__":

    grid, field, modified = simulate_city()

    plot_result(grid, field, modified)
