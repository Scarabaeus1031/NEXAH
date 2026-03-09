from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# CLIMATE PARAMETERS
# ---------------------------------------------------

BASE_YEAR = 2025

# warming progression speed
CLIMATE_RATE = 0.015

# midpoint of climate acceleration
CLIMATE_MIDPOINT = 2080

# maximum climate stress index
MAX_STRESS = 5


# ---------------------------------------------------
# CLIMATE STRESS FUNCTION
# ---------------------------------------------------

def compute_climate_stress(lat, lon, year):

    t = year - BASE_YEAR

    # logistic warming curve
    warming = MAX_STRESS / (1 + np.exp(-CLIMATE_RATE * (year - CLIMATE_MIDPOINT)))

    # polar amplification
    lat_factor = 1 + (abs(lat) / 90) * 0.5

    # subtropical drought belt
    drought = np.exp(-((abs(lat) - 25) ** 2) / 200)

    # extreme weather probability
    extreme = 0
    if np.random.rand() > 0.97:
        extreme = np.random.uniform(0.2, 0.6)

    # regional noise
    noise = np.random.normal(0, 0.05)

    stress = warming * lat_factor * 0.5 + drought + extreme + noise

    return max(0, stress)


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    year = BASE_YEAR

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    for step in range(30):

        year += 10

        ax.clear()

        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)

        lats = []
        lons = []
        stress = []

        for city in cities:

            s = compute_climate_stress(city["lat"], city["lon"], year)

            lats.append(city["lat"])
            lons.append(city["lon"])
            stress.append(s)

        ax.scatter(
            lons,
            lats,
            c=stress,
            s=40,
            cmap="Reds",
            transform=ccrs.PlateCarree(),
            vmin=0,
            vmax=5
        )

        ax.set_title(f"ARCHY Climate Stress — {year}")

        print(
            "Year:", year,
            "Avg stress:", round(np.mean(stress),3),
            "Max stress:", round(max(stress),3)
        )

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
        year += 10

        ax.clear()

        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)

        lats = []
        lons = []
        stress = []

        for city in cities:

            s = compute_climate_stress(city["lat"], city["lon"], year)

            lats.append(city["lat"])
            lons.append(city["lon"])
            stress.append(s)

        ax.scatter(
            lons,
            lats,
            c=stress,
            s=40,
            cmap="Reds",
            transform=ccrs.PlateCarree(),
            vmin=0,
            vmax=5
        )

        ax.set_title(f"ARCHY Climate Stress — {year}")

        print(
            "Year:", year,
            "Avg stress:", round(np.mean(stress),3),
            "Max stress:", round(max(stress),3)
        )

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()        year += 10

        ax.clear()

        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)

        lats = []
        lons = []
        stress = []

        for city in cities:

            s = compute_climate_stress(city["lat"], city["lon"], year)

            lats.append(city["lat"])
            lons.append(city["lon"])
            stress.append(s)

        ax.scatter(
            lons,
            lats,
            c=stress,
            s=40,
            cmap="Reds",
            transform=ccrs.PlateCarree()
        )

        ax.set_title(f"ARCHY Climate Stress — {year}")

        print(
            "Year:", year,
            "Avg stress:", round(np.mean(stress), 3),
            "Max stress:", round(max(stress), 3)
        )

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
