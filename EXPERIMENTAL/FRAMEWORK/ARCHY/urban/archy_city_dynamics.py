from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.urban.archy_city_generator import generate_city


def neighbor_effect(grid, strength=0.3):

    new_grid = grid.copy()

    size_x, size_y = grid.shape

    for x in range(size_x):
        for y in range(size_y):

            neighbors = []

            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:

                    if dx == 0 and dy == 0:
                        continue

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < size_x and 0 <= ny < size_y:
                        neighbors.append(grid[nx, ny])

            if neighbors:
                neighbor_mean = np.mean(neighbors)

                new_grid[x, y] = (
                    (1 - strength) * grid[x, y]
                    + strength * neighbor_mean
                )

    return new_grid


def evolve_city(environment="desert", size=30, steps=20):

    grid = generate_city(environment, size)

    history = [grid]

    for _ in range(steps):

        grid = neighbor_effect(grid)

        history.append(grid)

    return history


def plot_evolution(history):

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.title("Initial City")
    plt.imshow(history[0], cmap="viridis")
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.title("Evolved City")
    plt.imshow(history[-1], cmap="viridis")
    plt.colorbar()

    plt.show()


if __name__ == "__main__":

    history = evolve_city("desert", 30, 30)

    plot_evolution(history)
