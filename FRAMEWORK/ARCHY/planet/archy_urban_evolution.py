from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_real_cities import (
    simulate_city_stability,
    CITIES
)


# -----------------------------
# URBAN EVOLUTION MODEL
# -----------------------------

def evolve_stability(stability, climate):

    noise = np.random.normal(0, 0.003)

    if climate == "urban_heat":
        trend = 0.002

    elif climate == "coastal":
        trend = 0.001

    elif climate == "tropical":
        trend = -0.001

    else:
        trend = 0

    return max(0.25, min(0.45, stability + trend + noise))


# -----------------------------
# ANIMATION
# -----------------------------

def run_simulation():

    cities = simulate_city_stability()

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats = [c[1] for c in cities]
    lons = [c[2] for c in cities]

    stability = [c[3] for c in cities]
    climates = [c[4] for c in cities]

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        cmap="viridis",
        s=200,
        transform=ccrs.PlateCarree(),
        vmin=0.28,
        vmax=0.40
    )

    plt.colorbar(sc, label="City Stability")

    year = 2025

    def update(frame):

        nonlocal stability, year

        year += 10

        stability = [
            evolve_stability(s, climates[i])
            for i, s in enumerate(stability)
        ]

        sc.set_array(np.array(stability))

        ax.set_title(f"ARCHY Urban Evolution — {year}")

        print(year)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=8,
        interval=1500
    )

    plt.show()


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    run_simulation()
