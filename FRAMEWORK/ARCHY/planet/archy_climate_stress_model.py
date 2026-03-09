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

# global warming trend per year
TEMP_TREND = 0.02

# amplification after tipping zones
TIPPING_POINT_YEAR = 2080


# ---------------------------------------------------
# CLIMATE STRESS FUNCTION
# ---------------------------------------------------

def compute_climate_stress(lat, lon, year):

    years = year - BASE_YEAR

    # base warming
    warming = TEMP_TREND * years

    # nonlinear acceleration
    if year > TIPPING_POINT_YEAR:
        warming *= 1.4

    # latitude amplification (polar amplification)
    lat_factor = 1 + (abs(lat) / 90) * 0.6

    # subtropical drought belt
    drought_belt = np.exp(-((abs(lat) - 25) ** 2) / 150)

    # extreme weather probability
    extreme_event = np.random.rand()

    extreme_multiplier = 0
    if extreme_event > 0.97:
        extreme_multiplier = np.random.uniform(0.2, 0.5)

    # regional variability
    regional_noise = np.random.normal(0, 0.05)

    stress = warming * lat_factor + drought_belt * 0.3 + extreme_multiplier + regional_noise

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

        lats=[]
        lons=[]
        stress=[]

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
            "Avg stress:", round(np.mean(stress),3),
            "Max stress:", round(max(stress),3)
        )

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()        )

        ax.set_title(f"ARCHY Climate Stress — {year}")

        plt.pause(0.6)

    plt.show()


if __name__ == "__main__":
    run()
