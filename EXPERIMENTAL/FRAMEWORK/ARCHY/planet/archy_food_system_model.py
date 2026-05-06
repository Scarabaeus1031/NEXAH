from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# FOOD PRODUCTION MODEL
# ---------------------------------------------------

def compute_food_index(lat, year):

    # baseline productivity
    base = 1.0

    # climate degradation
    climate_loss = (year - 2025) * 0.002

    # tropical heat penalty
    tropic_penalty = max(0, 1 - abs(lat)/30)

    # yield noise
    noise = np.random.normal(0,0.05)

    food_index = base - climate_loss * tropic_penalty + noise

    return max(0.3, food_index)


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
        food=[]

        for c in cities:

            f = compute_food_index(c["lat"],year)

            lats.append(c["lat"])
            lons.append(c["lon"])
            food.append(f)

        ax.scatter(
            lons,
            lats,
            c=food,
            s=40,
            cmap="YlGn",
            transform=ccrs.PlateCarree(),
            vmin=0.3,
            vmax=1.2
        )

        ax.set_title(f"ARCHY Food Production Index — {year}")

        print("Year:",year,"Global food avg:",round(np.mean(food),3))

        plt.pause(0.6)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
