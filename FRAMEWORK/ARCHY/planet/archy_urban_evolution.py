from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_climate_model import climate_stress


# ---------------------------------------------------
# CITY STABILITY EVOLUTION
# ---------------------------------------------------

def evolve_stability(stability, climate, lat, year):

    noise = np.random.normal(0, 0.002)

    stress = climate_stress(lat, year)

    if climate == "urban_heat":
        trend = 0.002 - stress

    elif climate == "coastal":
        trend = 0.001 - stress

    elif climate == "tropical":
        trend = -0.001 - stress

    else:
        trend = -stress

    new_value = stability + trend + noise

    return max(0.25, min(0.45, new_value))


# ---------------------------------------------------
# RUN GLOBAL SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = simulate_city_stability()

    names = [c[0] for c in cities]
    lats = [c[1] for c in cities]
    lons = [c[2] for c in cities]
    stability = [c[3] for c in cities]
    climates = [c[4] for c in cities]

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

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

    for name, lat, lon in zip(names, lats, lons):

        ax.text(
            lon + 1,
            lat + 1,
            name,
            fontsize=8
        )

    plt.colorbar(sc, label="City Stability")

    year = 2025

    def update(frame):

        nonlocal stability, year

        year += 10

        stability = [
            evolve_stability(stability[i], climates[i], lats[i], year)
            for i in range(len(stability))
        ]

        sc.set_array(np.array(stability))

        ax.set_title(f"ARCHY Urban Evolution — {year}")

        print(f"Year {year}")

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=10,
        interval=1500
    )

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
