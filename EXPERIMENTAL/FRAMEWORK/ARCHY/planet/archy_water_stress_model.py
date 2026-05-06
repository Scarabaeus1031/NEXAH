from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# WATER STRESS MODEL
# ---------------------------------------------------

def compute_water_stress(lat, year):

    # climate drift
    warming = (year - 2025) * 0.0015

    # subtropical drought zones
    dry_zone = max(0, 1 - abs(lat - 25) / 25)

    # random hydrological variation
    noise = np.random.normal(0, 0.05)

    stress = warming * dry_zone + noise * 0.02

    return max(0, stress)


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    year = 2025

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

        for c in cities:

            s = compute_water_stress(c["lat"],year)

            lats.append(c["lat"])
            lons.append(c["lon"])
            stress.append(s)

        ax.scatter(
            lons,
            lats,
            c=stress,
            s=40,
            cmap="Blues_r",
            transform=ccrs.PlateCarree()
        )

        ax.set_title(f"ARCHY Water Stress — {year}")

        print("Year:",year,"Max water stress:",round(max(stress),3))

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
