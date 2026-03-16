from __future__ import annotations

import numpy as np


# ---------------------------------------------------
# ARCHY CLIMATE STRESS MODEL
# ---------------------------------------------------
# This module provides a simple planetary climate stress
# field that influences urban stability simulations.
#
# It models long-term warming trends and latitude-based
# climate pressure on cities.
# ---------------------------------------------------


def climate_stress(lat: float, year: int) -> float:
    """
    Compute climate stress for a location.

    Parameters
    ----------
    lat : float
        Latitude of the city.
    year : int
        Simulation year.

    Returns
    -------
    float
        Climate stress value.
    """

    lat = abs(lat)

    # Long-term warming component
    warming = (year - 2025) * 0.002

    # Base stress depending on latitude
    if lat < 15:
        base = 0.010  # tropical stress

    elif lat < 35:
        base = 0.006  # subtropical / coastal stress

    elif lat < 55:
        base = 0.004  # temperate zone

    else:
        base = 0.003  # cold regions

    return base + warming


# ---------------------------------------------------
# GLOBAL CLIMATE FIELD (optional)
# ---------------------------------------------------

def generate_climate_field(size: int, year: int):
    """
    Generate a global climate stress field for visualization.

    Parameters
    ----------
    size : int
        Grid resolution.
    year : int
        Simulation year.

    Returns
    -------
    numpy.ndarray
        Climate stress field.
    """

    field = np.zeros((size, size))

    for i in range(size):
        lat = (i / size) * 180 - 90

        for j in range(size):

            field[i, j] = climate_stress(lat, year)

    return field


# ---------------------------------------------------
# TEST / VISUALIZATION
# ---------------------------------------------------

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    year = 2100

    field = generate_climate_field(100, year)

    plt.imshow(field, cmap="inferno")
    plt.colorbar(label="Climate Stress")

    plt.title(f"ARCHY Global Climate Stress Field — {year}")

    plt.show()
